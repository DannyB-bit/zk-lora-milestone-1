#!/usr/bin/env python3
"""Pairing battery v3 — cycle-20 groth16_ota. Control freshness differential.

Batteries v1/v2 (08:19Z/08:33Z): PRIMARY 264a8fea VALID 2/2; CONTROL bd4c9ab2
(PR#14, known-VALID, committed VALID x4 Oct-4/5) flipped INVALID 2/2 today —
keys sha-guarded unchanged, binary sha-guarded, no throttle, 43-47C. Sustained-load
ordering exonerated (v2 control ran FIRST on a rested chip and still flipped).

v3 differential: verify SECOND known-VALID fc816080 (PR#13, committed VALID
2026-10-04T23:48Z) with its committed public-input vector.
  - fc816080 VALID  -> B verifier path sound TODAY; bd4c9ab2's INVALID is a
    per-statement fact to report in the evidence (control-rotation law); primary
    verdict may issue from this battery (control + primary both clean).
  - fc816080 INVALID -> whole B path under suspicion; drill stays QUARANTINED.
Run order: fc816080 first, 30 s gap, primary 264a8fea second. Thermals recorded.
"""
import hashlib
import os
import subprocess
import time

EVID = os.path.expanduser("~/fleet/evidence/20261005T0803Z_groth16_ota_daemon_cycle20")
LOG = os.path.join(EVID, "pairing_verify_timed_v3.log")
REPO = os.path.expanduser("~/fleet-repos/zk-lorawan")
BIN = os.path.join(REPO, "target/debug/zk_lorawan_prove")
PRIM = os.path.join(EVID, "rx_payload_128b.bin")  # 264a8fea
CTRL13 = os.path.expanduser("~/fleet-repos/zk-lora-milestone-1/evidence/groth16_ota_20261004T1124Z/rx_payload.bin")  # fc816080

GATEWAY = "0016c001ff18afa3903900000000000000000000000000000000000000000000"
FIRMWARE = "656e636c6176652d6669726d776172652d76657273696f6e2d76312e302e32"
PRIM_HASHES = [
    "515d79c3c4a8f85f775b37eb6e0c2b1d335d0f78b34ba7d6a5c7f86f2ab71d0e",
    "507fdd3d109ac0a11cdc7f952893123bd8f893d35579fd3e6075e412a8df4d04",
    "23a2be793fe04545dfffa73da78ade2ae9da1957b10aa9d054b8b5f6129ad11d",
    "3618eed84a884b75539485359a6a9900c132f3d29538acb1acb5ab6d4c04c705",
]
PRIM_DEPOSIT = "100001"
CTRL13_HASHES = [
    "cbe1d4d7220a8eb0649ceacda15a607287d2b0691689a774007acb6cb1b1290d",
    "a2624f76146976edc6221627204a603dee56acb5ee2ac6504024de0f6f6ae029",
    "8ed4c4688777c7ce5503bde3410831caec8ef1a2f768de4a4d3045eb47cdcd1a",
    "2261a97ccdfb4ce6111ff973fa732a81836c425d355781435512bec9e9549005",
]
CTRL13_DEPOSIT = "100000"


def slices(path):
    h = open(path, "rb").read().hex()
    assert len(h) == 256, f"{path}: {len(h)//2} bytes"
    return [h[:64], h[64:192], h[192:256]]


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def thermo():
    try:
        t = subprocess.run(["vcgencmd", "measure_temp"], capture_output=True, text=True, timeout=5).stdout.strip()
    except Exception as e:
        t = f"temp-err"
    try:
        th = subprocess.run(["vcgencmd", "get_throttled"], capture_output=True, text=True, timeout=5).stdout.strip()
    except Exception as e:
        th = f"throttle-err"
    return f"temp={t} throttled={th}"


def run(label, payload, hashes, deposit, out):
    out.append(f"{label} PRE: {thermo()}")
    args = [BIN, "verify", *slices(payload), *hashes, GATEWAY, deposit, FIRMWARE]
    t0 = time.time()
    r = subprocess.run(args, cwd=REPO, capture_output=True, text=True,
                       env={k: v for k, v in os.environ.items()
                            if k != "ZK_LORAWAN_REPRODUCIBLE_SETUP"})
    dt = time.time() - t0
    out.append(f"{label}: exit={r.returncode} wall_s={dt:.1f} stdout={r.stdout.strip()[:80]}")
    out.append(f"{label} POST: {thermo()}")
    print(f"{label}: exit={r.returncode} wall_s={dt:.1f} stdout={r.stdout.strip()[:40]}")
    return r.returncode


def main():
    lines = [f"BATTERY_V3_RUN_UTC={time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}"]
    lines.append("PATH=python subprocess list-args, CWD=zk-lorawan root, "
                 "ZK_LORAWAN_REPRODUCIBLE_SETUP unset, canon disk keys; control=fc816080 (PR#13) freshness differential")
    lines.append(f"keys sha-guard BEFORE: PK={sha(os.path.join(REPO,'keys/proving_key.bin'))} "
                 f"VK={sha(os.path.join(REPO,'keys/verifying_key.bin'))}")
    assert sha(PRIM) == "264a8fea20714a487b38e92634480fcae707c22bf2d2dce6c1c53ec779f9d4e2"
    assert sha(CTRL13).startswith("fc816080"), sha(CTRL13)

    c_ex = run("CONTROL fc816080 (PR#13 known-VALID, committed VALID 2026-10-04T23:48Z)",
               CTRL13, CTRL13_HASHES, CTRL13_DEPOSIT, lines)
    print("30s gap...")
    time.sleep(30)
    p_ex = run("PRIMARY 264a8fea (cycle-20 daemon-fire, A seq217 declare / seq218 fired)",
               PRIM, PRIM_HASHES, PRIM_DEPOSIT, lines)

    lines.append(f"keys sha-guard AFTER: PK={sha(os.path.join(REPO,'keys/proving_key.bin'))} "
                 f"VK={sha(os.path.join(REPO,'keys/verifying_key.bin'))}")
    if c_ex == 0 and p_ex == 0:
        verdict = "PASS (control fc816080 VALID -> path sound today; bd4c9ab2 flip reported as per-statement fact)"
    elif c_ex != 0:
        verdict = "QUARANTINE (second control also INVALID -> B path under suspicion, no verdict)"
    else:
        verdict = "QUARANTINE (primary failed with control VALID)"
    lines.append(f"BATTERY_V3_VERDICT={verdict}")
    with open(LOG, "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"BATTERY_V3_VERDICT={verdict}")


if __name__ == "__main__":
    main()
