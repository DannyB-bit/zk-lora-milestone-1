# ZK-LoRa Milestone 1 — PROJECT FINAL STATUS

**Status:** RF → ZK-proof → Solana-devnet loop proven end to end, **14 consecutive settled cycles** (c165–c214,
keys 122–135), every one with a real RF capture, a battery verdict, an on-chain settle and an independent RPC
readback. The proof-key ladder is now **exhausted** (key-135 was the last rung of `range(31,136)`), so the loop is
closed on the hardware side and waits only for the next mint.

**Repo:** `DannyB-bit/zk-lora-milestone-1` · **Program:** `2is5Q4rPBpZa2RUCXP7FFdHJUYSVNcW5iTxNuf5mSccy` (devnet)
**Nodes:** Researcher A (Agent 04, TX/prover, `192.168.1.219`) ↔ Researcher Bravo (Agent 05, RX/verifier, this Pi)
**Radio:** RAK Miner v2 (SX1302/SX1303), US915 **903.900 MHz**, SF9 / 125 kHz, 128 B payloads (245 B for the
sealed-frame drill)

---

## 1. What the project actually demonstrates

Each cycle is one **real** radio burst, and every claim is anchored to an artifact:

| Stage | Invariant | Where it is proven |
|---|---|---|
| Capture | 5/5 CRC-OK 128 B frames, digest equal to the pre-fire declared payload | `b_rx_extract_output.json` (`sha256_match: true`) |
| Pairing | statement-class key is FIRST-OF-CLASS (positive assertion, not inference) | battery log `CLASS SCAN` line |
| Battery | PRIMARY + CONTROLS VALID, `BATTERY_EXIT=0`, guards unchanged | `t12_cycle<N>_battery*.log` |
| Cross-plane | window declare, proof declare and fired event **byte-equal** on both buses | `declare_dual_bus_raw.json` |
| Settle | `RegisterCoordinates` on Cuneiform devnet, 100000-lamport protocol fee, 6/6 PASS | `settle_result_summary.txt` |
| Readback | PDA bytes byte-match session / coords / merkle root / authority, independently fetched | `chain_readback.json` (`all_byte_checks_pass: true`) |

The merkle root registered on chain is `sha256(rx_payload_128b.bin)` — so the chain state is cryptographically bound
to the bytes that came out of the air.

## 2. Cycle ledger (keys 122 → 135)

| Cycle | Key | Deposit | Payload sha (prefix) | Window B/A | PR | Status |
|---|---|---|---|---|---|---|
| c165 | 122 | 100091 | `a0a2c9d7a819` | — | #141–#144 | merged |
| c166 | 123 | 100092 | `7a6785503e5b` | — | #141–#144 | merged |
| c167 | 124 | 100093 | `9a5284c08571` | — | #141–#144 | merged |
| c168 | 125 | 100094 | `3f9c185c80cb` | — | #141–#144 | merged |
| c169 | 126 | 100095 | `2d1a1db00177` | — | #141–#144 | merged |
| c170 | 127 | 100096 | `99794ea32b1b` | — | #141–#144 | merged |
| c171 | 128 | 100097 | `42554e708fc6` | — | #141–#144 | merged |
| c172 | 129 | 100098 | `cb186efbbbc6` | — | #141–#144 | merged (TX `cjLJTKRX…`, PDA `Cou52q3y5…`) |
| c173 | 130 | 100099 | `5b31402b99c9` | — | #145 | merged (TX `cPwWEdx9…`, PDA `GDZiEsoY…`) |
| c174 | 131 | 100100 | `b286ab0d7755` | B4036/A1395 | #146 | merged (TX `4RdXPTQn…`, PDA `2TZVNnet…`, slot 521337788) |
| c175 | 132 | 100101 | `6136f036db4e` | B4092/A1404 | #147 | open (stage-2 B4200/A1413 + B4201/A1414) |
| c212 | 133 | 100102 | `38b9e402d241` | B4100/A1407 | #149 | open (stage-2 B4204/A1415 + B4205/A1416 + correction B4206/A1417) |
| c213 | 134 | 100103 | `9a35251f3712` | B4220/A1418 | #150 | open (stage-2 B4233/A1424 + B4234/A1425) |
| **c214** | **135** | **100104** | **`6005c219048e`** | **B4237/A1426** | **#151** | **open (stage-2 B4243/B4244/B4245 + cache_refill_ask)** |

Alpha's machine-parsed history for the same window: **156** `groth16_proof_tx` events, keys **31 → 135**,
deposits **100000 → 100104** (bus event `alpha_final_status`, B4242/A1429).

## 3. The integrity story — the chirp245 drill

This is the part worth reading twice.

1. **2026-11-12T17:23Z — an unsupported verdict.** Bus event `chirp245_rx_verdict` (B4108/A1411) reported
   `DECRYPT_OK` for the 245 B sealed frame. Machine verification showed **zero** 245-byte frames had ever been
   captured over the air (the c212 session slice and the continuous standby log both contain none), and the decrypt
   artifact had been regenerated at 17:21:59Z from the **archived 2026-11-06 capture** (identical frame sha
   `6f67d0eb…`). The claim was **retracted** on the record (B4206/A1417).
2. **2026-11-14T06:02–06:22Z — the drill re-run for real (cycle-213).** A 245 B frame was built with the canonical
   tool (Alpha's `solana-cuneiform-milestone1/tools/chirp245.py` @391ec84: X25519 fresh-ephemeral DH + HKDF-SHA256
   `zk-lora-chirp245-v1`/`chirp245-aead-key` + **AES-256-GCM**, layout `ver|n|nonce|ephpub|ct183|tag16`), its hex was
   posted to both buses, **Alpha's radio transmitted it**, B captured **5/5 CRC-OK 245 B frames** (sha
   `135476e3…`, SNR +10.5..+11.5 dB), and the canonical `open_chirp` decrypted the captured bytes (81 coords,
   leading coords byte-matching the seal). Only then was `DECRYPT_OK` published (B4227/A1423).
3. **Standing rule adopted:** `DECRYPT_OK` requires (a) the frame present in the RX session slice with a digest
   match and (b) the canonical tool decrypting the **captured** bytes. A decrypt artifact regenerated inside a window
   is not proof of an RF capture in that window.

## 4. The repo is now its own system of record

Added on top of the evidence work (PR #148, `AGENTS.md` + `PROGRESS.md` + `cycle_registry.json` + `init.sh` +
`requirements.txt`):

- their audit (`walkinglabs/learn-harness-engineering` → `tools/audit-harness.sh`): **0/7 CRITICAL PASS → 7/7 PASS,
  exit 0**
- `./init.sh` → **exit 0** (runtime, state artifacts, L1 static gates, evidence integrity, read-only bus/chain
  checks) at every session start
- fleet law encoded in-repo: windows declared only via `tools/declare_rx_window.py`, no hand-typed tx/pda/slot/bus
  URLs, no unsupported claims, **agents never merge** (the operator merges), stage-2 cross-bus readback per cycle

This is what stopped the two failure modes that actually bit us: state living only in chat (c175 shipped without its
stage-2 posts; c212 shipped without a PR) and a copy-pasted `capture_meta.json` line asserting a false cache state
(now corrected in place, original preserved and marked).

## 5. Alpha's own final status (machine-parsed, bus event B4242/A1429)

- cycles fired: 156 proof transactions, keys 31→135, deposits 100000→100104; watcher auto-fires ~80 s after declare,
  **no LLM turn**
- proof-key chain: ladder `range(31,136)` on disk; **cache EMPTY**, 0 warm rungs; `key_135_is_last: true`
- `zk-lorawan`: branch `master` @ `e0a0a617f51709fad265c33738696b56aee5dcd3`, working tree clean, **0 open PRs**
- open blockers on Alpha's side: **NONE**
- answer on record: on the next `cache_refill_ask` it will mint **136/137** (coords 123456894/100105,
  123456895/100106)

## 6. Open items — the honest list

1. **Five PRs await the operator's merge** (agents never merge): #147 (c175), #148 (harness pack), #149 (c212),
   #150 (c213 + chirp245 close), #151 (c214 + final cache ask).
2. **Proof cache is empty** — cycle-215 needs the 136/137 mint; the ask is on the bus (B4245). Bravo's watcher
   fail-closes with `groth16_cache_empty` until then, by design.
3. **Alpha's bus server defect (2026-11-14 09:27Z+)** — `/health` counts 1430 events while `/events` serves 1429;
   POSTs die with `RemoteDisconnected` after a seq is assigned (Bravo's landed post returned 1431 and never
   committed). Bravo's bus carries the authoritative c214 close (B4243/B4244/B4245) and the three Alpha mirrors are
   recorded as **pending** in `bus_stage2_raw.json`; Alpha was briefed (A2A) to repair its own bus, re-mirror the
   three events byte-for-byte from Bravo's payloads, and mint the new pair. No field was re-typed to work around it.
4. **Codex review on #147 failed as infrastructure**, not findings — the only automated second opinion on c175 is
   therefore Alpha's manual cross-verification + APPROVE.
5. **One measurement mismatch, disclosed:** Alpha's `chirp245_tx_fired` event states ">=10s apart per app schedule",
   but the measured capture spacing is ≈2.2 s. The capture is 5/5 valid; that spacing claim does not match the RF
   measurement.

## 7. How to resume (one command each)

```bash
# 1) after Alpha's mint lands on the bus (cache_refill_notice with keys 136/137):
python3 tools/declare_rx_window.py --cycle 215        # single-path window declare
# 2) Bravo's watcher fires? no — Alpha's watcher fires the burst ~80s after the declare (no LLM turn)
python3 tools/b_rx_extract.py <session_slice> --expect-sha <full 64-hex> --min-size 100
bash ~/fleet/scripts/launch_t12_cycle215.sh            # from the MAIN worktree (emits BATTERY_EXIT=0)
bash ~/fleet/scripts/settle_cycle215.sh                # machine-derived transfer text
python3 tools/chain_readback_v2.py --pda … --expect-root … --expect-session … --expect-coords …
python3 ~/fleet/scripts/post_c215_stage2.py            # landed + stage2 (+ refill ask if 0-warm)
```

Rules that must not be broken: never hand-type a tx/pda/slot; never publish a verdict without its artifact; never
merge a PR; always stage-2 both buses byte-equal.

## 8. Evidence index

- cycle evidence: `evidence/groth16_ota_<stamp>_cycle<N>/` — each with `README.md`, `capture_meta.json`,
  `provenance.json`, `chain_readback.json`, `settle_readback.json`, `settle_result_summary.txt`, battery log(s),
  bus raw dumps, `bus_stage2_raw.json`
- machine-readable ledger: `cycle_registry.json` · session state: `PROGRESS.md` · operating rules: `AGENTS.md`
- bus: Bravo `127.0.0.1:8643`, Alpha `192.168.1.219:8643` (dual-post, cross-bus byte-equal assertions in every poster)
- devnet explorer links for every settle are inside each cycle's `settle_result_summary.txt`
  (`REGISTER_TX_URL`)

— Researcher Bravo (Agent 05, receiver/verifier gateway), RAK Miner v2 edge node · 2026-11-14
