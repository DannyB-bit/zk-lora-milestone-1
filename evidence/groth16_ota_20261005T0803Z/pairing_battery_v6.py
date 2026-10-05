#!/usr/bin/env python3
"""Pairing battery v6 — PERSISTENCE probe for the cycle-20 quarantine (2026-10-05T13:2xZ).

v5 (09:24Z) established the statement-class flip: cecbb8b8 (key-31 class,
committed VALID 01:5xZ same day) returned INVALID while 264a8fea (key-32
class, cycle-20 primary) returned VALID, 4th repeat, one session, sha-guarded
keys unchanged. Forensics since: memtester userspace PASS + clean dmesg ->
DRAM exonerated in the testable region; suspicion localized to on-die
compute path.

v6 re-runs the SAME pair ~4.5 h later to characterize PERSISTENCE of the
fault:
  - cecbb8b8 INVALID + 264a8fea VALID  -> flip is PERSISTENT (latched or
    deterministically input-triggered), not a transient soft-error;
  - cecbb8b8 VALID                     -> flip was INTERMITTENT (transient
    class) -> changes the hardware posture from cold power-cycle to
    stability/thermal investigation;
  - any other combination             -> compute path state changed again;
    disclose, still no verdict.
This battery CANNOT issue a cycle-20 pairing verdict on suspect silicon
(control-battery law: a quarantined run issues no verdict either direction).
It is fault characterization only. The decisive test remains RakMiner-A's
independent-silicon verification of the key-31 vectors.
"""
import hashlib
import os
import subprocess
import time

EVID = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(EVID, "pairing_verify_timed_v6.log")
REPO = os.path.expanduser("~/fleet-repos/zk-lorawan")
BIN = os.path.join(REPO, "target/debug/zk_lorawan_prove")
PRIM = os.path.join(EVID, "rx_payload_128b.bin")  # 264a8fea key-32 (cycle-20 primary)
CEC = os.path.expanduser("~/fleet-repos/zk-lora-milestone-1/evidence/groth16_ota_20261005T0148Z/rx_payload.bin")  # cecbb8b8 key-31 (PR#16)

GATEWAY = "0016c001ff18afa3903900000000000000000000000000000000000000000000"
FIRMWARE = "656e636c6176652d6669726d776172652d76657273696f6e2d76312e302e32"
K31_HASHES = ["cbe1d4d7220a8eb0649ceacda15a607287d2b0691689a774007acb6cb1b1290d",
              "a2624f76146976edc6221627204a603dee56acb5ee2ac6504024de0f6f6ae029",
              "8ed4c4688777c7ce5503bde3410831caec8ef1a2f768de4a4d3045eb47cdcd1a",
              "2261a97ccdfb4ce6111ff973fa732a81836c425d355781435512bec9e9549005"]
K32_HASHES = ["515d79c3c4a8f85f775b37eb6e0c2b1d335d0f78b34ba7d6a5c7f86f2ab71d0e",
              "507fdd3d109ac0a11cdc7f952893123bd8f893d35579fd3e6075e412a8df4d04",
              "23a2be793fe04545dfffa73da78ade2ae9da1957b10aa9d054b8b5f6129ad11d",
              "3618eed84a884b75539485359a6a9900c132f3d29538acb1acb5ab6d4c04c705"]


def slices(path):
    h = open(path, "rb").read().hex()
    assert len(h) == 256
    return [h[:64], h[64:192], h[192:256]]


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def verify(label, payload, hashes, deposit, out):
    args = [BIN, "verify", *slices(payload), *hashes, GATEWAY, deposit, FIRMWARE]
    t0 = time.time()
    r = subprocess.run(args, cwd=REPO, capture_output=True, text=True,
                       env={k: v for k, v in os.environ.items()
                            if k != "ZK_LORAWAN_REPRODUCIBLE_SETUP"})
    dt = time.time() - t0
    line = f"{label}: exit={r.returncode} wall_s={dt:.1f} stdout={r.stdout.strip()[:40]}"
    out.append(line)
    print(line, flush=True)
    return r.returncode


def main():
    lines = [f"BATTERY_V6_RUN_UTC={time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}",
             "persistence probe: same class-discrimination pair as v5 (09:24Z), t+~4.5h",
             f"keys sha-guard BEFORE: PK={sha(os.path.join(REPO,'keys/proving_key.bin'))[:16]} VK={sha(os.path.join(REPO,'keys/verifying_key.bin'))[:16]}"]
    assert sha(PRIM) == "264a8fea20714a487b38e92634480fcae707c22bf2d2dce6c1c53ec779f9d4e2"
    assert sha(CEC).startswith("cecbb8b8"), sha(CEC)

    c1 = verify("cecbb8b8 (key-31 flipped class, persistence repeat t+4.5h)", CEC, K31_HASHES, "100000", lines)
    c2 = verify("264a8fea (key-32 valid class, persistence repeat t+4.5h)", PRIM, K32_HASHES, "100001", lines)

    if c1 != 0 and c2 == 0:
        verdict = "PERSISTENT: flip reproduces at t+4.5h — latched or deterministically input-triggered, NOT a transient soft-error"
    elif c1 == 0:
        verdict = "INTERMITTENT: key-31 class recovered at t+4.5h — transient fault class; hardware posture shifts to stability/thermal"
    else:
        verdict = "STATE CHANGED: pattern differs from v5 — disclose, still no verdict on suspect silicon"
    lines.append(f"CHARACTERIZATION: {verdict}")
    lines.append(f"keys sha-guard AFTER: PK={sha(os.path.join(REPO,'keys/proving_key.bin'))[:16]} VK={sha(os.path.join(REPO,'keys/verifying_key.bin'))[:16]}")
    lines.append(f"BATTERY_V6_DONE={time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}")
    with open(LOG, "w") as f:
        f.write("\n".join(lines) + "\n")
    print("V6 COMPLETE", flush=True)


if __name__ == "__main__":
    main()
