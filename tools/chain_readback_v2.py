#!/usr/bin/env python3
"""chain_readback_v2.py — raw-byte on-chain record readback for Cuneiform settlements.

Law origin (cycle-80 Codex review, 2026-10-11): the v1 readback searched for the
64-char HEX STRING of the merkle root inside raw account bytes — structurally void,
because the program stores the root as RAW 32 bytes. This probe byte-compares at the
Anchor layout offsets instead:

    CoordinateRecord (103 B):
      0..8    Anchor discriminator
      8..40   authority pubkey
      40..56  session_id (16 ASCII bytes)
      56..62  coords (6 raw bytes)
      62..94  merkle_root (32 raw bytes)
      94..103 tail (space/bump region, reported not interpreted)

Fail-closed: exits nonzero unless every expected field matches byte-exact.

Usage:
  python3 tools/chain_readback_v2.py --pda <PDA> \
      --expect-root <64hex> --expect-session <16ascii> \
      --expect-coords 132,182,56,35,123,217 \
      [--expect-authority <base58>] [--out <path>] [--rpc https://api.devnet.solana.com]
"""
import argparse
import base64
import binascii
import json
import sys
import urllib.request
from datetime import datetime, timezone

ANCHOR_TAIL_LEN = 9  # space+bump region after merkle_root


def rpc_call(rpc, method, params):
    payload = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode()
    req = urllib.request.Request(rpc, data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        out = json.loads(r.read())
    if "error" in out:
        raise SystemExit(f"RPC error: {out['error']}")
    return out["result"]


def b58_decode(s):
    alpha = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    n = 0
    for c in s:
        n = n * 58 + alpha.index(c)
    raw = n.to_bytes((n.bit_length() + 7) // 8, "big")
    pad = len(s) - len(s.lstrip("1"))
    return b"\x00" * pad + raw


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pda", required=True)
    ap.add_argument("--expect-root", required=True, help="64-hex merkle root")
    ap.add_argument("--expect-session", required=True, help="16-char ASCII session id")
    ap.add_argument("--expect-coords", required=True, help="6 ints, comma-separated")
    ap.add_argument("--expect-authority", default=None, help="base58 authority pubkey")
    ap.add_argument("--out", default=None, help="write JSON report here")
    ap.add_argument("--rpc", default="https://api.devnet.solana.com")
    args = ap.parse_args()

    exp_root = binascii.unhexlify(args.expect_root)
    exp_session = args.expect_session.encode()
    exp_coords = bytes(int(x) for x in args.expect_coords.split(","))
    if len(exp_root) != 32: raise SystemExit("expect-root must be 64 hex chars")
    if len(exp_session) != 16: raise SystemExit("expect-session must be 16 ASCII chars")
    if len(exp_coords) != 6: raise SystemExit("expect-coords must be 6 values")

    acc = rpc_call(args.rpc, "getAccountInfo", [args.pda, {"encoding": "base64"}])
    val = acc["value"]
    if val is None:
        print(json.dumps({"pda": args.pda, "account_exists": False, "verdict": "FAIL"}))
        return 1
    raw = base64.b64decode(val["data"][0])
    if len(raw) != 103:
        print(f"unexpected account length {len(raw)} (expected 103)", file=sys.stderr)

    checks = {
        "session_id_ascii_match": raw[40:56] == exp_session,
        "coords_byte_match": raw[56:62] == exp_coords,
        "merkle_root_raw_byte_match": raw[62:94] == exp_root,
    }
    if args.expect_authority:
        checks["authority_match"] = raw[8:40] == b58_decode(args.expect_authority)

    report = {
        "readback_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tool": "chain_readback_v2.py",
        "cluster_rpc": args.rpc,
        "record_pda": args.pda,
        "account_exists": True,
        "account_data_len": len(raw),
        "account_owner": val["owner"],
        "account_lamports": val["lamports"],
        "context_slot": acc["context"]["slot"],
        "anchor_layout": {
            "discriminator": "0..8", "authority": "8..40", "session_id_ascii": "40..56",
            "coords_raw": "56..62", "merkle_root_raw_32b": "62..94",
            f"tail_{ANCHOR_TAIL_LEN}b": f"94..{len(raw)} (space/bump, not interpreted)",
        },
        "on_chain_session_id_ascii": raw[40:56].decode(errors="replace"),
        "on_chain_coords": list(raw[56:62]),
        "on_chain_merkle_root_hex": raw[62:94].hex(),
        "expected_merkle_root_hex": exp_root.hex(),
        **checks,
        "all_byte_checks_pass": all(checks.values()),
        "verdict": "PASS" if all(checks.values()) else "FAIL",
    }
    text = json.dumps(report, indent=1)
    print(text)
    if args.out:
        with open(args.out, "w") as f:
            f.write(text + "\n")
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
