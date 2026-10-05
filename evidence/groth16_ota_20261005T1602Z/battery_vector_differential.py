#!/usr/bin/env python3
"""VECTOR-TYPO DIFFERENTIAL BATTERY — the decisive self-test on B silicon.

Hypothesis under test (B, 2026-10-05T18:0xZ): the 9/9 key-31 INVALIDs since 04:45Z
were NOT a silicon fault but a HAND-TRANSCRIPTION TYPO in B's own battery scripts:
  K31 attestation hash used by B's scripts:  ...de4a4d3045eb47cdcd1a  (WRONG — nowhere in any Alpha declare, any committed recipe, or the canon proof bundle)
  K31 attestation hash per every declare/recipe: ...de4d0a3045eb47cdcd1a  (CORRECT)
K32 vector in B's batteries == Alpha's machine declare byte-exact -> explains the
"statement-class-correlated flip" signature perfectly: key-31 runs used a wrong
public input (deterministic INVALID, any core, any env), key-32 runs used the right
one (VALID 4/4). No silicon fault is required to explain any observed datum.

Matrix (each cell = one 142s canon verify on THIS die, same binary/keys/CWD):
  T1  a1706406  x correct vector   ->  prediction VALID   (overturns silicon verdict)
  T2  a1706406  x typo'd vector    ->  prediction INVALID (reproduces the "fault" deterministically)
  T3  bd4c9ab2  x correct vector   ->  prediction VALID   (control — PR#14 known-VALID)
  T4  bd4c9ab2  x typo'd vector    ->  prediction INVALID  (reproduces the "fault" on the control too)

If T1=VALID and T2=INVALID: SILICON EXONERATED — the 9/9 INVALIDs were arg errors,
the quarantine on pairing verdicts LIFTS (no power-cycle needed), and cycle-19/20/24
pairing verdicts are re-issued from this battery. If T1=INVALID on the correct vector:
silicon-fault verdict STANDS and the power-cycle protocol continues unchanged.
Either way this battery is the decider. Run detached — 4 x ~142s = ~10 min.
"""
import hashlib
import json
import os
import subprocess
import sys
import time

REPO = os.path.expanduser("~/fleet-repos/zk-lorawan")
BIN = os.path.join(REPO, "target/debug/zk_lorawan_prove")
EVID = os.path.expanduser("~/fleet-repos/zk-lora-milestone-1/evidence/groth16_ota_20261005T1602Z")
LOG = os.path.join(EVID, "battery_vector_differential.log")

A1706406 = os.path.join(EVID, "../groth16_ota_20261005T0442Z/rx_payload.bin")          # key-31, cycle-19
BD4C9AB2 = os.path.join(EVID, "../groth16_ota_20261004T1922Z/rx_payload.bin")           # key-31, PR#14 control
assert os.path.isfile(A1706406), A1706406
assert os.path.isfile(BD4C9AB2), BD4C9AB2

GATEWAY = "0016c001ff18afa3903900000000000000000000000000000000000000000000"
FIRMWARE = "656e636c6176652d6669726d776172652d76657273696f6e2d76312e302e32"
K31_CORRECT = [
    "cbe1d4d7220a8eb0649ceacda15a607287d2b0691689a774007acb6cb1b1290d",
    "a2624f76146976edc6221627204a603dee56acb5ee2ac6504024de0f6f6ae029",
    "8ed4c4688777c7ce5503bde3410831caec8ef1a2f768de4d0a3045eb47cdcd1a",  # CORRECT (per every Alpha declare + committed recipe + canon bundle)
    "2261a97ccdfb4ce6111ff973fa732a81836c425d355781435512bec9e9549005",
]
K31_TYPO = [
    "cbe1d4d7220a8eb0649ceacda15a607287d2b0691689a774007acb6cb1b1290d",
    "a2624f76146976edc6221627204a603dee56acb5ee2ac6504024de0f6f6ae029",
    "8ed4c4688777c7ce5503bde3410831caec8ef1a2f768de4a4d3045eb47cdcd1a",  # TYPO (B hand-transcription, exists only in B scripts of 2026-10-05)
    "2261a97ccdfb4ce6111ff973fa732a81836c425d355781435512bec9e9549005",
]

def sha(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def slices(path):
    h = open(path, "rb").read().hex()
    assert len(h) == 256, (path, len(h))
    return [h[:64], h[64:192], h[192:256]]

def verify(label, payload, hashes, deposit, lines):
    args = [BIN, "verify", *slices(payload), *hashes, GATEWAY, deposit, FIRMWARE]
    t0 = time.time()
    r = subprocess.run(args, cwd=REPO, capture_output=True, text=True,
                       env={k: v for k, v in os.environ.items() if k != "ZK_LORAWAN_REPRODUCIBLE_SETUP"})
    dt = time.time() - t0
    verdict = "VALID" if r.returncode == 0 else ("INVALID" if "INVALID" in (r.stdout + r.stderr) else f"ERROR rc={r.returncode}")
    line = f"{label}: verdict={verdict} exit={r.returncode} wall_s={dt:.1f} stdout={r.stdout.strip()[:40]!r}"
    lines.append(line)
    print(line, flush=True)
    return r.returncode

lines = []
lines.append(f"BATTERY_VECTOR_DIFFERENTIAL_RUN_UTC={time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}")
lines.append("purpose: decide typo-vs-silicon on B die; 4 cells x ~142s; binary/keys/CWD canon")
lines.append(f"binary_sha256={sha(BIN)[:16]}")
lines.append(f"PK={sha(os.path.join(REPO,'keys/proving_key.bin'))[:16]} VK={sha(os.path.join(REPO,'keys/verifying_key.bin'))[:16]}")
lines.append(f"temp_pre={subprocess.run(['vcgencmd','measure_temp'],capture_output=True,text=True).stdout.strip()}")

assert sha(A1706406).startswith("a1706406"), sha(A1706406)
assert sha(BD4C9AB2).startswith("bd4c9ab2"), sha(BD4C9AB2)
lines.append(f"payload A1706406 sha256={sha(A1706406)}")
lines.append(f"payload BD4C9AB2 sha256={sha(BD4C9AB2)}")

# THE decisive cell first: known-VALID key-31 payload against the CORRECT vector on THIS die.
t1 = verify("T1 a1706406 x CORRECT vector (decision cell)", A1706406, K31_CORRECT, "100000", lines)
# Then the reproducer: same payload against the TYPO vector.
t2 = verify("T2 a1706406 x TYPO vector (reproducer)", A1706406, K31_TYPO, "100000", lines)
# Control payload against both vectors.
t3 = verify("T3 bd4c9ab2 x CORRECT vector (control)", BD4C9AB2, K31_CORRECT, "100000", lines)
t4 = verify("T4 bd4c9ab2 x TYPO vector (control reproducer)", BD4C9AB2, K31_TYPO, "100000", lines)

lines.append(f"temp_post={subprocess.run(['vcgencmd','measure_temp'],capture_output=True,text=True).stdout.strip()}")
lines.append(f"keys sha-guard AFTER: PK={sha(os.path.join(REPO,'keys/proving_key.bin'))[:16]} VK={sha(os.path.join(REPO,'keys/verifying_key.bin'))[:16]}")

if t1 == 0 and t2 != 0 and t3 == 0 and t4 != 0:
    verdict = ("OVERTURN: T1/T3 VALID on correct vector + T2/T4 INVALID on typo vector => "
               "SILICON EXONERATED; 9/9 key-31 INVALIDs were arg errors from B's typo'd vector; "
               "pairing-quarantine LIFTS; re-issue cycle-19/20/24 pairing verdicts from this battery")
elif t1 != 0:
    verdict = ("SILICON-FAULT VERDICT STANDS: a1706406 INVALID even on the CORRECT vector on this die; "
               "power-cycle protocol unchanged; disclose T2/T4 to rule residual input-correlation")
else:
    verdict = f"INCONCLUSIVE: t1={t1} t2={t2} t3={t3} t4={t4} — bisect before any verdict"
lines.append(f"DIFFERENTIAL_VERDICT={verdict}")
print("\n" + verdict, flush=True)

with open(LOG, "w") as f:
    f.write("\n".join(lines) + "\n")
print(f"LOG_WRITTEN={LOG}")
