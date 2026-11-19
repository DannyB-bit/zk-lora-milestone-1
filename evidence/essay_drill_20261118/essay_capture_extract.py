#!/usr/bin/env python3
"""essay_capture_extract.py — parse HAL RX standby log, extract 245B LoRa frames,
dedupe by sha256, and inventory them with RF metadata.

Usage:
  python3 essay_capture_extract.py <rx_log> <out_dir>
"""
import argparse, hashlib, json, re, sys
from pathlib import Path

PKT_RE = re.compile(r"^\s*-{5}\s*LoRa packet\s*-{5}\s*$")
# HAL field lines: "  count_us: 123" OR "  rf_chain  0" (no colon on rf_chain)
FIELD_RE = re.compile(
    r"^\s+(count_us|size|chan|status|datr|codr|freq_hz|snr_avg|rssi_chan|rssi_sig|crc)"
    r"\s*:?\s+(\S+)\s*$")
HEX_RE = re.compile(r"^([0-9A-Fa-f]{2}(?: [0-9A-Fa-f]{2})*)\s*$")
RECEIVED_RE = re.compile(r"^Received\s+\d+\s+packets", re.IGNORECASE)


def parse_log(text):
    """Yield one dict per LoRa packet block."""
    blocks, cur, in_pkt, payload_hex = [], None, False, []
    for line in text.splitlines():
        if PKT_RE.match(line):
            if cur is not None:
                cur["payload_hex"] = "".join(payload_hex)
                blocks.append(cur)
            cur, in_pkt, payload_hex = {}, True, []
            continue
        if not in_pkt:
            continue
        if RECEIVED_RE.match(line.strip()):
            if cur is not None:
                cur["payload_hex"] = "".join(payload_hex)
                blocks.append(cur)
            cur, in_pkt, payload_hex = None, False, []
            continue
        m = FIELD_RE.match(line)
        if m:
            cur[m.group(1)] = m.group(2)
            continue
        h = HEX_RE.match(line)
        if h:
            payload_hex.append(h.group(1).replace(" ", ""))
            continue
        # unknown line inside a block: ignore (keep collecting payload)
    if cur is not None:
        cur["payload_hex"] = "".join(payload_hex)
        blocks.append(cur)
    return blocks


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("log")
    ap.add_argument("out_dir")
    args = ap.parse_args()

    out = Path(args.out_dir); out.mkdir(parents=True, exist_ok=True)
    text = Path(args.log).read_text(errors="replace")
    blocks = parse_log(text)

    frames = {}
    counts = {"packets": len(blocks), "size245": 0, "crc_ok": 0, "unique245": 0,
              "status_hist": {}, "size_hist": {}}
    for b in blocks:
        ph = b.get("payload_hex", "")
        st = b.get("status", "?")
        sz = b.get("size", "?")
        counts["status_hist"][st] = counts["status_hist"].get(st, 0) + 1
        counts["size_hist"][sz] = counts["size_hist"].get(sz, 0) + 1
        if not ph:
            continue
        try:
            raw = bytes.fromhex(ph)
        except ValueError:
            continue
        counts["packets"] += 0
        if st == "0x10":
            counts["crc_ok"] += 1
        if sz == "245" or len(raw) == 245:
            counts["size245"] += 1
            sha = hashlib.sha256(raw).hexdigest()
            rec = frames.setdefault(sha, {"sha256": sha, "bytes": len(raw), "reps": 0,
                                          "meta": [], "path": f"frame_{sha[:16]}.bin"})
            rec["reps"] += 1
            rec["meta"].append({k: b.get(k) for k in
                                ("count_us", "snr_avg", "crc", "status", "chan", "datr",
                                 "freq_hz")})
            (out / rec["path"]).write_bytes(raw)
    counts["unique245"] = len(frames)

    inv = {"source_log": str(Path(args.log).resolve()),
           "counts": counts,
           "unique_frames": sorted(frames.values(), key=lambda r: r["sha256"])}
    (out / "capture_inventory.json").write_text(json.dumps(inv, indent=1))
    print(json.dumps({"counts": counts,
                      "unique_shas": [r["sha256"] for r in inv["unique_frames"]][:200]}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
