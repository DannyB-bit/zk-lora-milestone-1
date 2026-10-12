#!/usr/bin/env python3
"""
B-side RX evidence parser — extracts CRC-OK packets from test_loragw_hal_rx logs.
Researcher Bravo (Agent 05, RakMiner-B) · zk-lora-milestone-1

Parses the HAL RX test output format (verified against the June 30 2026 M1
capture, node-b-rx_20260630T012005Z/raw_hal_rx_9039_sf9_125k.log):

    ----- LoRa packet -----
      count_us: 11045121
      size:     240
      chan:     0
      status:   0x10        <- STAT_CRC_OK (loragw_hal.h: STAT_NO_CRC=0x01, CRC_BAD=0x11)
      datr:     9           <- SF
      codr:     1
      rf_chain  0
      freq_hz   903900000
      snr_avg:  11.2
      rssi_chan:196.0
      rssi_sig :195.0
      crc:      0x0000
    <single hex line, space-separated payload bytes>
    Received N packets (total:M)

Usage:
    b_rx_extract.py LOG [--expect-sha HEX64] [--min-size N]
Prints a JSON summary.

Exit contract (fail-closed, PR#52 Codex-P2 hardening 2026-10-12):
    0  >=1 CRC-OK packet parsed; if --expect-sha was given, it is a FULL
       64-hex digest and at least one CRC-OK packet matches it
    1  no CRC-OK packets parsed
    2  --expect-sha is not a full 64-hex digest (abbreviated/truncated
       digests are REFUSED: they compare false while looking like a check)
    3  --expect-sha is well-formed and packets parsed, but NONE matches
       the declared digest — a declare/capture mismatch is a FAILURE,
       never a footnote with exit 0
"""
import argparse
import hashlib
import json
import re
import sys

STAT_CRC_OK = 0x10


def parse_log(path: str) -> list:
    packets = []
    cur = None
    hex_line_re = re.compile(r"^[0-9A-F]{2}( [0-9A-F]{2})*\s*$")
    hex_frag_re = re.compile(r"^[0-9A-F ]+$")
    with open(path, "r", errors="replace") as f:
        for line in f:
            s = line.strip()
            if s.startswith("-----"):
                if cur:
                    packets.append(cur)
                cur = {"hexfrags": []}
                continue
            if cur is None:
                continue
            m = re.match(r"(count_us|size|chan|status|datr|codr|rf_chain|freq_hz|snr_avg|rssi_chan|rssi_sig|crc):\s*(\S+)", s)
            if m:
                cur[m.group(1)] = m.group(2)
                continue
            m = re.match(r"(rf_chain|freq_hz)\s+(\S+)", s)  # no-colon variants
            if m:
                cur[m.group(1)] = m.group(2)
                continue
            # Hex payload fragment — June M1 capture proved the payload dump can
            # be interleaved with reset-script stdout ON THE SAME LINE, sometimes
            # SPLITTING a byte token mid-nibble ("...7" + "SX1302 ..." + "2 ...").
            # Salvage the clean hex PREFIX, PRESERVING any odd single-nibble
            # tokens — reassembly strategies (rejoin/drop/best) decide validity.
            if s:
                cut = 0
                for ch in s:
                    if ch in "0123456789ABCDEF ":
                        cut += 1
                    else:
                        break
                frag = s[:cut].strip()
                if not frag:
                    continue
                toks = frag.split()
                if toks and all(len(t) in (1, 2) for t in toks):
                    cur["hexfrags"].append(" ".join(toks))
    if cur:
        packets.append(cur)

    out = []
    for p in packets:
        try:
            status = int(p.get("status", "0x100"), 16)
        except ValueError:
            status = -1
        size_field = int(p.get("size", "0"))
        raw_frags = p.get("hexfrags", [])
        data = b""
        strategy = None
        # S1 REJOIN: concatenate all fragments' hex; a byte split by the
        # interleave ("...7" + "2...") naturally reforms ("72"). Correct if
        # the result matches the packet's declared size.
        # S2 DROP: remove the odd split nibbles (parse each frag alone).
        # S3 BEST-EFFORT: first parseable candidate.
        for strat in ("rejoin", "drop", "best"):
            try:
                if strat == "rejoin":
                    cand = bytes.fromhex("".join(raw_frags).replace(" ", ""))
                elif strat == "drop":
                    cand = b""
                    for fr in raw_frags:
                        toks = fr.split()
                        if len(toks) > 1 and len(toks[-1]) == 1:
                            toks = toks[:-1]
                        if len(toks) > 1 and len(toks[0]) == 1:
                            toks = toks[1:]
                        if all(len(t) == 2 for t in toks):
                            cand += bytes.fromhex("".join(toks))
                else:
                    cand = bytes.fromhex("".join(raw_frags).replace(" ", ""))
            except ValueError:
                continue
            if size_field and len(cand) == size_field:
                data, strategy = cand, strat
                break
            if not data:
                data, strategy = cand, strat
        out.append({
            "count_us": int(p.get("count_us", "0")),
            "size_field": size_field,
            "actual_bytes": len(data),
            "status": f"0x{status:02X}",
            "crc_ok": status == STAT_CRC_OK,
            "datr": p.get("datr"),
            "freq_hz": int(p.get("freq_hz", "0")),
            "snr_avg": p.get("snr_avg"),
            "rssi_chan": p.get("rssi_chan"),
            "log_interleaved": len(raw_frags) > 1,
            "recovery_strategy": strategy,
            "sha256": hashlib.sha256(data).hexdigest() if data else None,
            "hex": data.hex(" ").upper() if data else None,
        })
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("log")
    ap.add_argument("--expect-sha", default=None,
                    help="FULL 64-hex sha256 digest of the declared payload; "
                         "abbreviated digests are refused (exit 2)")
    ap.add_argument("--min-size", type=int, default=1)
    a = ap.parse_args()

    # Codex P2 hardening: a truncated/abbreviated digest (e.g. '81fd764b…a0d1e2')
    # compares false against every packet while LOOKING like a check — the
    # recorded claim then 'passes' a command that validated nothing. Refuse it.
    expect = None
    if a.expect_sha is not None:
        expect = a.expect_sha.strip().lower()
        if re.fullmatch(r"[0-9a-f]{64}", expect) is None:
            print(json.dumps({
                "log": a.log,
                "error": ("--expect-sha must be a FULL 64-hex sha256 digest; abbreviated/"
                          "truncated digests are refused — they compare false while "
                          "looking like a check (fail-closed, PR#52 Codex P2)"),
                "expected_sha256": a.expect_sha,
            }, indent=2))
            return 2

    pkts = parse_log(a.log)
    crc_ok = [p for p in pkts if p["crc_ok"] and p["actual_bytes"] >= a.min_size]
    match = None
    if expect is not None and crc_ok:
        match = any(p["sha256"] == expect for p in crc_ok)

    print(json.dumps({
        "log": a.log,
        "total_packets": len(pkts),
        "crc_ok_packets": len(crc_ok),
        "expected_sha256": expect,
        "sha256_match": match,
        "crc_ok": crc_ok,
        "all_packets": [{k: v for k, v in p.items() if k != "hex"} for p in pkts],
    }, indent=2))

    if not crc_ok:
        return 1
    if expect is not None and not match:
        # A declared digest that matches NO captured packet is a FAILURE of the
        # recorded claim — never a JSON footnote with exit 0 (Codex P2).
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
