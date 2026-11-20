#!/usr/bin/env python3
"""essay_decrypt_reassemble.py — decrypt captured 245B chirps with bravo_sk and
reassemble the source file (RAW-byte mode), verifying against a declared sha256.

Usage:
  python3 essay_decrypt_reassemble.py <frames_dir> <sk_hex_file> <out_file> [--expect-sha HEX]
"""
import argparse, hashlib, json, sys
from pathlib import Path

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.asymmetric.x25519 import (
    X25519PrivateKey, X25519PublicKey)
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes

CHIRP_LEN = 245


def decrypt_frame(frame: bytes, sk_hex: str) -> bytes:
    if len(frame) != CHIRP_LEN:
        raise ValueError(f"bad frame length {len(frame)}")
    ver, n = frame[0], frame[1]
    if ver != 1:
        raise ValueError(f"unsupported version {ver}")
    nonce = frame[2:14]
    eph_pub = X25519PublicKey.from_public_bytes(frame[14:46])
    ct_tag = frame[46:245]
    priv = X25519PrivateKey.from_private_bytes(bytes.fromhex(sk_hex))
    shared = priv.exchange(eph_pub)
    key = HKDF(algorithm=hashes.SHA256(), length=32,
               salt=b"zk-lora-chirp245-v1", info=b"chirp245-aead-key").derive(shared)
    return AESGCM(key).decrypt(nonce, ct_tag, None)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("frames_dir")
    ap.add_argument("sk_hex_file")
    ap.add_argument("out_file")
    ap.add_argument("--expect-sha", default=None)
    args = ap.parse_args()

    sk_hex = Path(args.sk_hex_file).read_text().strip()
    fd = Path(args.frames_dir)
    frames = sorted(fd.glob("frame_*.bin"))
    results, chunks = [], {}
    for fp in frames:
        raw = fp.read_bytes()
        sha = hashlib.sha256(raw).hexdigest()
        rec = {"file": fp.name, "frame_sha256": sha, "bytes": len(raw)}
        try:
            pt = decrypt_frame(raw, sk_hex)
        except Exception as e:
            rec.update({"ok": False, "verdict": "DECRYPT_FAIL", "error": type(e).__name__})
            results.append(rec); continue
        if pt[0] != 2:
            rec.update({"ok": False, "verdict": "BAD_MAGIC", "magic": pt[0]}); results.append(rec); continue
        total, idx = pt[1], pt[2]
        chunk = pt[3:].rstrip(b"\x00")
        rec.update({"ok": True, "verdict": "DECRYPT_OK", "magic": pt[0], "total": total,
                    "idx": idx, "chunk_bytes": len(chunk),
                    "chunk_sha256": hashlib.sha256(chunk).hexdigest()})
        results.append(rec)
        # keep highest-precedence copy: first occurrence wins (reps are identical)
        chunks.setdefault((total, idx), chunk)

    groups = {}
    for (total, idx), ch in chunks.items():
        groups.setdefault(total, {})[idx] = ch

    out_path = Path(args.out_file)
    report = {"frames_dir": str(fd.resolve()), "frames_seen": len(frames),
              "decrypt_ok": sum(1 for r in results if r.get("verdict") == "DECRYPT_OK"),
              "decrypt_fail": sum(1 for r in results if r.get("verdict") == "DECRYPT_FAIL"),
              "groups": {}, "per_frame": results}

    for total, idxmap in sorted(groups.items()):
        missing = [i for i in range(total) if i not in idxmap]
        data = b"".join(idxmap[i] for i in sorted(idxmap))
        sha = hashlib.sha256(data).hexdigest()
        g = {"total_chunks": total, "have": len(idxmap), "missing": missing,
             "reassembled_bytes": len(data), "reassembled_sha256": sha}
        if not missing:
            out_path.write_bytes(data)
            g["wrote"] = str(out_path.resolve())
        if args.expect_sha:
            g["expect_sha256"] = args.expect_sha
            g["sha_match"] = (sha == args.expect_sha) and not missing
        report["groups"][str(total)] = g

    print(json.dumps({k: v for k, v in report.items() if k != "per_frame"}, indent=1))
    Path(str(out_path) + ".decrypt_report.json").write_text(json.dumps(report, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
