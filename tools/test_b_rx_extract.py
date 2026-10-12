#!/usr/bin/env python3
"""Unit test: b_rx_extract.py against synthetic interleaved RX logs.

Extended 2026-10-12 to pin the PR#52 Codex-P2 fail-closed exit contract:
    exit 0  >=1 CRC-OK packet; --expect-sha (when given) FULL 64-hex AND matched
    exit 1  no CRC-OK packets
    exit 2  --expect-sha malformed (abbreviated/truncated digests refused)
    exit 3  --expect-sha well-formed, packets parsed, but NONE matches
Run from the repository root: python3 tools/test_b_rx_extract.py
"""
import hashlib
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

def run(*extra):
    return subprocess.run(
        ["python3", "tools/b_rx_extract.py", path, *extra],
        capture_output=True, text=True,
    )


# Case A: no --expect-sha -> original parse contract unchanged
rA = run("--min-size", "4")
dA = json.loads(rA.stdout)
print("A rc:", rA.returncode, "| total:", dA["total_packets"], "| crc_ok:", dA["crc_ok_packets"])
for p in dA["crc_ok"]:
    print("  pkt %dB (size_field %d) interleaved=%s hex=%s"
          % (p["actual_bytes"], p["size_field"], p["log_interleaved"], p["hex"]))
for p in dA["all_packets"]:
    if not p["crc_ok"]:
        print("  [excluded] %dB status=%s" % (p["actual_bytes"], p["status"]))

# Case B: abbreviated digest (unicode ellipsis, as the c-88 README carried)
# -> must be REFUSED with exit 2, not silently compared (Codex P2)
rB = run("--min-size", "4", "--expect-sha", "81fd764b…a0d1e2")
print("B (abbreviated digest) rc:", rB.returncode)

# Case C: well-formed 64-hex digest that matches NO packet -> exit 3 (mismatch fails)
rC = run("--min-size", "4", "--expect-sha",
         hashlib.sha256(b"no-such-payload-in-log").hexdigest())
print("C (unmatched full digest) rc:", rC.returncode)

# Case D: FULL digest of the reassembled 7B CRC-OK packet -> exit 0 + match true
true_sha = hashlib.sha256(bytes.fromhex("AA55AA7255AA66")).hexdigest()
rD = run("--min-size", "4", "--expect-sha", true_sha)
dD = json.loads(rD.stdout)
print("D (matching full digest) rc:", rD.returncode, "| sha256_match:", dD["sha256_match"])

os.unlink(path)

ok = (
    # A: parse contract unchanged
    rA.returncode == 0
    and dA["total_packets"] == 2
    and dA["crc_ok_packets"] == 1
    and dA["crc_ok"][0]["actual_bytes"] == 7
    and dA["crc_ok"][0]["hex"] == "AA 55 AA 72 55 AA 66"
    and dA["crc_ok"][0]["recovery_strategy"] == "rejoin"
    and dA["crc_ok"][0]["log_interleaved"] is True
    # B: abbreviated digest refused, fail-closed
    and rB.returncode == 2
    # C: declared digest that matches nothing is a FAILURE
    and rC.returncode == 3
    # D: full matching digest passes
    and rD.returncode == 0
    and dD["sha256_match"] is True
    and dD["expected_sha256"] == true_sha
)
print("UNIT TEST:", "PASS" if ok else "FAIL")
raise SystemExit(0 if ok else 1)
