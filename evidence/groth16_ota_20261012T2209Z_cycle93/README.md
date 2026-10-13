# groth16_ota cycle-93 — COMPLETE VALID A→B (17th consecutive 80s-class fire)

**42nd valid fleet cycle.** FIRST key-35 statement class — positively asserted by the T12
battery class scan (zero prior declares of class (key-35, pih) over COMPLETE dual-bus history;
bus fetch == /health event count; per the c-84 first-of-class law, absence of local evidence
is never first-of-class).

| Plane | Result |
|---|---|
| Window | armed 2026-10-12T22:09:49Z → closed 2026-10-13T00:09:49Z, gate-certified (14th PASS in standby log), declared via `declare_rx_window.py` (B1393/A535) |
| Declare | `groth16_proof_tx` B1395 == A536, cross-bus byte-identical: proof SHA `21f051d874879dc44a39b97096c3b9fc431af9a3ebec741ae85acbd5aa1f8be6`, key-35, deposit 100004, watcher hot path |
| Fire | 2026-10-13T00:05:25Z, 5/5 TX_DONE, **80 s declare-to-fire (17th consecutive 80s-class)** |
| Radio capture | 5/5 CRC-OK 128 B frames @ 903.9 MHz SF9, SNR +10.8..11.2 dB, POST-WRAP branch machine-selected (+4294.967296 s), inter-frame 16.8 s, walls 2026-10-13T00:04:11.928196+00:00 .. 2026-10-13T00:05:19.233389+00:00 |
| SHA gate | `b_rx_extract.py` exit 0, `sha256_match: true`, full 64-hex vs dual-bus declare; payload bin committed |
| T12 battery (FIRST-OF-CLASS mode) | PRIMARY `21f051d8` (key-35) **VALID 142.4 s** + CONTROL-diff1 c-92 `(key-34,`… (key-34) **VALID 142.0 s** + CONTROL-diff2 c-70 `c300e5b4` (key-32) **VALID 142.1 s** — B die, keys sha-guarded unchanged (PK 8dda8b79/VK 7bd5683f), silicon 44.8→49.6 °C, throttled=0x0 |
| Settle (Cuneiform devnet) | RECORD_PDA `9nwzjpnFBNZzybvuq9tdc1kKoN2gctAHcyVpHY1AjGfq`, REGISTER_TX [`396HeD4PiqCQgTDP…`](https://explorer.solana.com/tx/396HeD4PiqCQgTDPn3b7cxTTz3cWD92BK4DguV25gXXg6V5wfJfzEvjEmg8vG3R2kjJSD6KShka35CTGwiTxrnzt?cluster=devnet), slot 510451064, 100 000-lamport fee, 6/6 settle tests PASS, chain-readback byte-verified (sig on-chain, owner `2is5Q4rP…`, 105 B digest-only) |
| Bus verdict | `rx_verdict` B1400 == A538, dual readback PASS, posted before PR/settle staging |

## Class scan (machine-asserted)

```
CLASS SCAN (complete dual-bus history): statement-class key-35 pih[-1]=7ac2e13c2ab1bb2c prior-declares B=0 A=0 pih-only-priors B=0 A=0 unclassable-declares=5 -> FIRST-OF-CLASS (positively asserted)
CONTROL MODE: FIRST-OF-CLASS (positive assertion) key-35 — 2 DISTINCT-statement-class controls (keys key-34, key-32)
```

## Honest ledger

- Window declared with 346 s remaining at declare (machine-parsed from `declare_rx_window.py` output; window still had 5+ min to absorb the 80 s hot-path fire).
- Battery log rotate-law honored: `t12_cycle93_battery.log` (single attempt, no aborts this cycle — attempt-1 of this session).
- First battery launch of this tick died rc=127 BEFORE any pairing ran — the launcher script
  write had been voided by a shell-wrapper rejection in the composing tool call (script file
  absent, `bash: No such file or directory`). Relaunched from a re-written script; zero pairing
  work was lost, no evidence artifacts existed yet. Disclosed per the honest-ledger law.

## Reproduce (fresh checkout of this PR head)

```bash
# 1) fail-closed SHA gate over the committed session slice
python3 tools/b_rx_extract.py evidence/groth16_ota_20261012T2209Z_cycle93/c93_session_slice.log \
  --expect-sha 21f051d874879dc44a39b97096c3b9fc431af9a3ebec741ae85acbd5aa1f8be6 --min-size 100
# rc=0 + sha256_match:true expected (full 64-hex contract)

# 2) T12 pairing battery — vendored template, same bytes that ran (sha 92f31236…)
sha256sum evidence/groth16_ota_20261012T2209Z_cycle93/t12_battery_template_PR48head_158c0a5.py
python3 evidence/groth16_ota_20261012T2209Z_cycle93/t12_battery_template_PR48head_158c0a5.py \
  --cycle 93 --evidence-dir evidence/groth16_ota_20261012T2209Z_cycle93 \
  --guard-log <your standby log>   # 3 × ~142 s arkworks BN254 pairings
```

Session slice lines 1801..1943 of `~/fleet/logs/rx_standby_continuous_20261011T200428Z.log`
(B-side live log; the raw guard log is fleet-internal and not committed).

## Files

- `c93_session_slice.log` — raw HAL RX slice, the 5-frame burst + 2 ambient 0-size blips
- `b_rx_extract_output.json` — fail-closed extractor output, 5/5 match
- `rx_payload_128b.bin` — captured 128 B payload, sha `21f051d874879dc44a39b97096c3b9fc431af9a3ebec741ae85acbd5aa1f8be6`
- `t12_battery_template_PR48head_158c0a5.py` — vendored battery (byte-exact, sha 92f312361f3fd1f2c58a4c18cae8ba8ec812aa51caa1609e0def667d647a435f)
- `t12_cycle93_battery.log` — full battery run log
- `capture_meta.json` / `declare_snapshot.json` / `verdict_bus_seqs.json` / `cycle93_window_declare.json` — machine-parsed metadata
- `chain_readback.json` / `result_summary.txt` / `tests_passed.txt` — settle artifacts; RECORD_PDA `9nwzjpnFBNZzybvuq9tdc1kKoN2gctAHcyVpHY1AjGfq`, TX `396HeD4PiqCQgTDPn3b7cxTTz3cWD92BK4DguV25gXXg6V5wfJfzEvjEmg8vG3R2kjJSD6KShka35CTGwiTxrnzt`

**Author: Research Team Bravo (Agent 05, RakMiner-B) — zk-lora-milestone-1 groth16_ota lane**
