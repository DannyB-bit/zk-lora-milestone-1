#!/usr/bin/env python3
"""Unit test: b_rx_extract.py against synthetic interleaved RX logs."""
import json
import os
import subprocess
import tempfile

LOG = """Waiting for packets...

----- LoRa packet -----
  count_us: 111
  size:     7
  chan:     0
  status:   0x10
  datr:     9
  codr:     1
  rf_chain  0
  freq_hz   903900000
  crc:      0x1DCE
AA 55 AA 7 SX1302 reset through GPIO17
SX1302 power enable skipped
2 55 AA 66

----- LoRa packet -----
  count_us: 222
  size:     16
  status:   0x11
  freq_hz   903900000
DE AD BE EF DE AD BE EF DE AD BE EF DE AD BE EF
"""

with tempfile.NamedTemporaryFile("w", suffix=".log", delete=False) as f:
    f.write(LOG)
    path = f.name

r = subprocess.run(
    ["python3", "tools/b_rx_extract.py", path, "--min-size", "4"],
    capture_output=True, text=True,
)
d = json.loads(r.stdout)
print("rc:", r.returncode, "| total:", d["total_packets"], "| crc_ok:", d["crc_ok_packets"])
for p in d["crc_ok"]:
    print("  pkt %dB (size_field %d) interleaved=%s hex=%s"
          % (p["actual_bytes"], p["size_field"], p["log_interleaved"], p["hex"]))
for p in d["all_packets"]:
    if not p["crc_ok"]:
        print("  [excluded] %dB status=%s" % (p["actual_bytes"], p["status"]))
os.unlink(path)

ok = (
    r.returncode == 0
    and d["total_packets"] == 2
    and d["crc_ok_packets"] == 1
    and d["crc_ok"][0]["actual_bytes"] == 7
    and d["crc_ok"][0]["hex"] == "AA 55 AA 72 55 AA 66"
    and d["crc_ok"][0]["recovery_strategy"] == "rejoin"
    and d["crc_ok"][0]["log_interleaved"] is True
)
print("UNIT TEST:", "PASS" if ok else "FAIL")
raise SystemExit(0 if ok else 1)
