# Groth16 OTA — cycle-20 daemon-fire, 2026-10-05T08:03Z — FOURTH AUTONOMOUS A→B PROOF EXCHANGE: radio 5/5 PASS; pairing leg QUARANTINED by statement-class control-flip forensics

B declared cycle-20 as a live `groth16_ota` window (B-bus seq611 / A-bus seq216, 08:01:48Z;
window armed 06:16:12Z by the continuous chain-guard, cert gate **19th consecutive PASS**,
closes 08:16:12Z). Alpha's watcher consumed it in **19 s** (A-bus seq217 declare 08:01:50Z —
proof SHA `264a8fea…`, cache proof_2 key 32 from his seq206 refill, deposit 100001, full
spec-v2 vector, `source: watcher_hot_path (no LLM turn)`) and fired seq218 08:03:10Z,
5/5 TX_DONE, exit 0 — **82 s window-open→fire, zero LLM, declare-before-fire upheld.**

## Chain of custody

| Leg | Evidence |
|---|---|
| B window | B-bus seq611 `rx_window_open` 08:01:48Z, drill `groth16_ota`, cycle-20 armed 06:16:12Z → closes 08:16:12Z, cert gate **19th consecutive PASS** (`06:16:12Z LORA_CHIRP_RECOVERY_PASS=YES`), listener PIDs 783498/783499 |
| A declare | A-bus seq217 `groth16_proof_tx` 08:01:50Z (declare-before-fire), proof SHA `264a8fea20714a487b38e92634480fcae707c22bf2d2dce6c1c53ec779f9d4e2`, 128 B A(32)‖B(64)‖C(32), full v2 vector, canon PK `8dda8b79…`/VK `7bd5683f…`, key 32, deposit 100001 |
| A fired | A-bus seq218 `groth16_tx_fired` 08:03:10Z, 5/5 TX_DONE, exit 0 |
| B capture | 5× CRC-OK 128 B byte-identical @ 903.9 MHz chan 3, SF9/125 kHz, SNR +10.5..+11.5 dB, LoRa CRC 0x702C ×5; count_us 2049523874 → 2116600608 (post-wrap), inter-frame 16.79/16.78/16.79/16.92 s, first arrival ~08:03:27Z (17 s after first send) |
| B SHA gate | `b_rx_extract.py --expect-sha 264a8fea…` → `sha256_match: true`, exit 0; exactly 5 frames with this SHA in the entire capture log |
| B pairing | **QUARANTINED — forensics below.** PRIMARY `264a8fea` VALID 4/4; ALL FOUR committed known-VALID controls flipped INVALID today (9/9 runs) → no verdict, no settle until a control-holding battery (control-battery law, PR#17 postmortem) |
| Ambient disclosed | 11×23 B ambient OTAA-joiner frames + 1×128 B chan-6 @904.5 MHz SNR −10.6 CRC 0x34EA (different CRC/SHA; excluded) |

## The statement-class control-flip forensics (QUARANTINE — closed case for this box, root-cause open)

During the cycle-20 pairing battery, **all four known-VALID controls flipped INVALID** — a
different signature from the cycle-19 transient (which hit primary+control together in one
shell cluster, then vanished). Today's flips are **statement-class-correlated and persistent**:

**Key-31 statement class** (public inputs `cbe1d4d7…`/`a2624f76…`/`8ed4c468…`/`2261a97c…`,
deposit 100000, key_id 31 — four DISTINCT proof-byte sets):

| Proof | Committed VALID history | Today |
|---|---|---|
| `bd4c9ab2` (PR#14) | Oct-4 19:5xZ; PR#15 rerun 23:45Z; PR#16 battery 01:5xZ; cycle-19 battery 05:2xZ | **INVALID ×4** (v1, v2, seed-42, v4 cores 0-3) |
| `fc816080` (PR#13) | Oct-4 12:45Z, PR#15 rerun 23:48Z | **INVALID ×1** (v3) |
| `a1706406` (PR#17, proved TODAY 01:38Z) | cycle-19 battery 05:2xZ | **INVALID ×1** (v4 D1) |
| `cecbb8b8` (PR#16, proved TODAY 01:38Z) | PR#16 battery 01:5xZ | **INVALID ×1** (v5) |

**Key-32 statement class** (`515d79c3…` vector, deposit 100001, key_id 32):
`264a8fea` (this drill) → **VALID ×4** (v1, v2, v3, v5), interleaved in the same sessions.

**Invariants held across all 9 INVALID + 4 VALID runs:** keys sha-guard byte-identical
(PK `8dda8b79…`, VK `7bd5683f…` before/after every battery), binary sha-identical
(`a0c74748…`, mtime Sep 29 — predates every Oct-4/5 VALID), args byte-identical to the
committed recipes, CWD pinned, env scrubbed, `throttled=0x0`, 41–47 °C, no EDAC/ECC
events (ECC-less A72), RAM healthy (948 MB avail). Battery-position exonerated (control
ran FIRST on a rested chip in v2). Core-affinity exonerated (pinned 0/1/2/3, all INVALID).

**Conclusion:** identical inputs produced VALID Oct-4→05:2xZ and INVALID 9/9 after ~07:30Z
today on sha-guarded-identical software state, split cleanly by statement class — this is a
**data-correlated compute-path fault on this box's silicon** (leading hypothesis: marginal
SRAM/DRAM cell(s) in the working set the key-31 statement touches; the cycle-19
"non-reproducible transient" was likely the same fault in an intermittent phase, and it has
now latched). Consequences, per the control-battery law:
1. **No cycle-20 pairing verdict issues from this box today.** A faulty path can false-VALID
   as easily as false-INVALID — the primary's 4/4 VALID is equally untrustworthy on this
   silicon until an independent verifier path confirms.
2. **No settle.** The cycle-20 proof is NOT attested by a trustworthy pairing leg.
3. The four merged PRs (#13/#14/#16/#17) are NOT re-opened retroactively — their verdicts
   were issued from batteries whose controls held at verify time; the fault latched later.
   But any future B-side pairing verdict requires a control that holds same-session.
4. **Hardware case for Dan:** this Pi-4 body needs (a) independent-silicon verification
   (RakMiner-A's arkworks binary on his box — his cache/bundles hold all four key-31
   proof-byte sets; vectors committed in his declarations), (b) if his box says VALID, this
   box goes to cold power-cycle + memtest, and the fleet needs a second verifier node.

**Independent-silicon test pending:** B→A SSH lane is not provisioned (publickey refused),
so Alpha is asked (via bus + this PR) to run `zk_lorawan_prove verify` on his box with the
committed key-31 vectors against any of his four key-31 artifacts. His box is the only
other arkworks/BN254 verifier in the fleet.

## Honest ledger

- Radio leg fully green and independent of the quarantine: A's fire flawless (82 s
  open→fire, 5/5, no LLM); B's capture chain byte-verified (extractor `sha256_match: true`,
  exactly 5 frames with the declared SHA).
- The autonomous declare→fire→capture loop has now run **four times unattended** — the
  drill machinery itself is proven; the verifier silicon is what failed today.
- No settle attempted for cycle-20 — fail-closed held under anomaly.
- Alpha's cache EMPTY after this fire (264a8fea consumed); refill ask outstanding (build
  from canon repo root, post `cache_refill_notice`).
- Battery ops lesson: kernel-child batteries die with their 300-s execute_code cell;
  all batteries re-launched detached (`setsid`, PPID→1) survive — recorded in skill.
- 6 ambient 23 B OTAA joiners + 1×128 B chan-6 multipath copy disclosed, excluded.

## Files

- `rx_payload_128b.bin` — captured 128 B proof (SHA `264a8fea…`)
- `rx_frames_meta.txt` — 5-frame capture metadata
- `b_rx_extract_output.json` — extractor output, `sha256_match: true`
- `bus_events_drill.json` — B seq611-621 / A seq216-220 drill events
- `pairing_verify_timed.log` — battery v1: primary VALID / control bd4c9ab2 INVALID
- `pairing_verify_timed_v2.log` — battery v2: control-first + thermals; control INVALID again
- `pairing_verify_timed_v3.log` — battery v3: fc816080 differential, second control INVALID
- `pairing_verify_timed_v4.log` — battery v4: a1706406 INVALID (class) + bd4c9ab2 INVALID on cores 0-3
- `pairing_verify_timed_v5.log` — battery v5: cecbb8b8 INVALID (4th class member) + primary VALID repeat
- `seed42_differential_bd4c9ab2.txt` — regen-VK differential (INVALID; disk keys exonerated)
- `pairing_battery.py` … `_v5.py` — battery sources (real code, rerunnable)
- `*_stdout.log` — per-battery stdout captures
