#!/usr/bin/env python3
"""build_refire_set.py — stage ONLY the frames Alpha reports missing, from the
already-sealed burst dirs, into a single re-fire directory.

Every staged frame is verified against the frame_sha256 Alpha published in his
verdict (A1496), so a re-fire can never send a frame Alpha did not ask for.
The ciphertext is NOT re-sealed: the sealed chunk_idx is preserved so Alpha's
reassembler still sees the original chunk numbering.

Usage: build_refire_set.py <verdict.json> <out_dir> <src_dir1> <src_dir2> ...
"""
import hashlib, json, shutil, sys
from pathlib import Path


def main():
    verdict = json.loads(Path(sys.argv[1]).read_text())
    out = Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
    srcs = [Path(p) for p in sys.argv[3:]]

    # index every source frame by its sha256
    by_sha = {}
    for sd in srcs:
        for f in sorted(sd.glob("frame_*.bin")):
            by_sha[hashlib.sha256(f.read_bytes()).hexdigest()] = f

    missing = verdict["missing"]
    staged, problems = [], []
    for m in missing:
        want = m["frame_sha256"]
        src = by_sha.get(want)
        if src is None:
            problems.append({"chunk_idx": m["chunk_idx"], "payload": m["payload"],
                             "error": "frame_sha256_not_found_in_staged_dirs",
                             "frame_sha256": want})
            continue
        raw = src.read_bytes()
        if len(raw) != 245:
            problems.append({"chunk_idx": m["chunk_idx"], "payload": m["payload"],
                             "error": f"bad_length_{len(raw)}", "frame_sha256": want})
            continue
        idx = len(staged)
        dst = out / f"frame_{idx:02d}.bin"
        shutil.copy2(src, dst)
        staged.append({
            "idx": idx,
            "frame_sha256": want,
            "bytes": 245,
            "source_file": str(src),
            "origin_payload": m["payload"],
            "origin_chunk_idx": m["chunk_idx"],
        })

    manifest = {
        "purpose": "round-4 targeted re-fire of ONLY Alpha's missing frames (A1496)",
        "source_verdict_seq": verdict.get("seq"),
        "source_verdict_missing_count": len(missing),
        "staged_count": len(staged),
        "problems": problems,
        "frames": staged,
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=1))
    print(json.dumps({
        "requested": len(missing), "staged": len(staged), "problems": len(problems),
        "by_origin_payload": {
            p: sum(1 for s in staged if s["origin_payload"] == p)
            for p in sorted({s["origin_payload"] for s in staged})},
        "out_dir": str(out),
    }, indent=1))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
