# groth16_ota cycle-94 — COMPLETE VALID A→B (18th consecutive 80s-class fire)

**43rd valid fleet cycle.** FIRST key-36 statement class — positively asserted by the T12
battery class scan (zero prior declares of class (key-36, pih) over COMPLETE dual-bus history;
bus fetch == /health event count on both buses). Battery ran on the **corrected canonical
template** (PR#58 head `6a49d04`): Codex P1 time-travel class-scan + P1 exit-contract fixes
live-proven on this cycle (`BATTERY_EXIT=0`, the sole settle-eligible code).

| Plane | Result |
|---|---|
| Window | armed 2026-10-13T02:10:30Z → closed 2026-10-13T04:10:30Z, gate-certified (16th PASS in standby log), declared via `declare_rx_window.py` v1.1 (B1411/A541) — composer now reads newest `b_ack` OR `cache_refill_notice` for warm-cache prefixes |
| Refill | key-36 `3a333037…` + key-37 `6cfc1148…` proved by Alpha 03:10-03:12Z after the c-94 wake brief; `cache_refill_notice` B1408 == A540 byte-identical, both VK `7bd5683f…`; declare released on the notice |
| Declare | `groth16_proof_tx` B1413 == A542, cross-bus byte-identical: proof SHA `3a33303728b85008d54b73942e530e3d9082183aa57f156f5939224d76ca4090`, key-36, deposit 100005, watcher hot path |
| Fire | 2026-10-13T03:59:34Z, 5/5 TX_DONE, **80 s declare-to-fire (18th consecutive 80s-class)** |
| Radio capture | 5/5 CRC-OK 128 B frames @ 903.9 MHz SF9, SNR +10.5..11.2 dB, POST-WRAP branch machine-selected (+4294.967296 s), inter-frame 16.8 s, walls 2026-10-13T03:58:21.084167+00:00 .. 2026-10-13T03:59:28.307976+00:00 |
| SHA gate | `b_rx_extract.py` (PR#52-hardened, vendored copy committed) exit 0, `sha256_match: true`, full 64-hex vs dual-bus declare; payload bin committed |
| T12 battery (FIRST-OF-CLASS mode) | PRIMARY `3a333037` (key-36) **VALID 142.1 s** + CONTROL-diff1 c-84 `(key-33)` `4b416048` **VALID 141.9 s** + CONTROL-diff2 c-70 `(key-32)` `c300e5b4` **VALID 142.0 s** — B die, keys sha-guarded unchanged (PK 8dda8b79/VK 7bd5683f), silicon 44.3→48.2 °C, throttled=0x0, **BATTERY_EXIT=0** |
| Bus verdict | `rx_verdict` B1417 == A544, dual readback PASS, posted before PR/settle staging |
| Settle (Cuneiform devnet) | RECORD_PDA `TGaGqVced3sTbSwd7LKaZPksyrNVJMvH82uzdPo16Bt`, REGISTER_TX [`55LtXDgD…`](https://explorer.solana.com/tx/55LtXDgDuiyr9Vso5T7s9gGY9Hs6qC1B9dNZEp2ZWina4umF5R7gpH5Q7wboP5CCBpWVueySzuAE9WwC7qteRwC9?cluster=devnet), slot 510507941, 100 000-lamport fee, 6/6 settle tests PASS, chain-readback byte-verified (sig on-chain via `getSignaturesForAddress`, owner `2is5Q4rP…`, 103 B digest-only, G5 decode-scan CLEAN) |

## Class scan (machine-asserted)

```
CLASS SCAN (complete dual-bus history): statement-class key-36 pih[-1]=4d02bde2cc1f972e prior-declares B=0 A=0 pih-only-priors B=0 A=0 unclassable-declares=5 -> FIRST-OF-CLASS (positively asserted)
CONTROL MODE: FIRST-OF-CLASS (positive assertion) key-36 — 2 DISTINCT-statement-class controls (keys key-33, key-32)
```

## Honest ledger

- Declare posted with 737 s remaining (machine-parsed from `declare_rx_window.py` cert;
  the window absorbed the 80 s hot-path fire with 11+ min margin).
- Wake-brief ordering: the c-94 refill ask was posted BEFORE the declare (the 5-key ladder
  was fully consumed by c-89..c-93; a declare into an empty cache would have burned the
  window on a `groth16_cache_empty` hold — the c-33/34 lesson, inverted into protocol).
- Composer defect fixed same-turn: `declare_rx_window.py` v1.1 — the expected-SHA field read
  only `b_ack` events; with the whole ladder consumed the newest b_ack carried consumed
  rungs. Now reads newest of {b_ack, cache_refill_notice}. Disclosed on the window event.
- Alpha disclosure acked: his builder loop skips existing cache files, so a plain `build 2`
  on an empty cache re-proves rungs 1-2; he extended the KEYS list to 7 rungs and proved
  indices 5-6 directly. His words, verified by the dual-bus refill notice (B1408==A540).
- c-84 key-33 control payload vendored from `refs/pull/48/head` per the c-91 stranded-restore
  law (PR#48 unmerged; fresh checkout of this PR reproduces the battery without it merged).
  Byte-verified vs the dual-bus declare (`VENDORED_PROVENANCE.json`).
- Battery log rotate-law honored: `t12_cycle94_battery_attempt1.log` — single attempt, zero aborts.

## Reproduce (fresh checkout of this PR head)

```bash
# 1) fail-closed SHA gate over the committed session slice
python3 evidence/groth16_ota_20261013T0210Z_cycle94/b_rx_extract_pr52head.py \
  evidence/groth16_ota_20261013T0210Z_cycle94/session_slice.log \
  --expect-sha 3a33303728b85008d54b73942e530e3d9082183aa57f156f5939224d76ca4090 --min-size 100
# rc=0 + sha256_match:true expected (full 64-hex contract, abbreviated digests refused exit 2)

# 2) T12 pairing battery — vendored corrected template, same bytes that ran
#    (sha256 f2605ea56f181c52917bbb54b504afa6ffc967d5831c65098bb93c2e122497ba)
sha256sum evidence/groth16_ota_20261013T0210Z_cycle94/t12_battery_template_canonical_fixed_6a49d04.py
python3 evidence/groth16_ota_20261013T0210Z_cycle94/t12_battery_template_canonical_fixed_6a49d04.py \
  --cycle 94 --evidence-dir evidence/groth16_ota_20261013T0210Z_cycle94 \
  --guard-log <your standby log>   # 3 × ~142 s arkworks BN254 pairings; echo $? must print 0
```

Session slice = lines 2074..2182 of `~/fleet/logs/rx_standby_continuous_20261011T200428Z.log`
(B-side live log; the raw guard log is fleet-internal and not committed).

## Files

- `session_slice.log` — raw HAL RX slice, the 5-frame burst
- `b_rx_extract_output.json` — fail-closed extractor output, 5/5 match
- `rx_payload_128b.bin` — captured 128 B payload, sha `3a33303728b85008d54b73942e530e3d9082183aa57f156f5939224d76ca4090`
- `t12_battery_template_canonical_fixed_6a49d04.py` — vendored corrected battery (byte-exact, sha `f2605ea56f181c52917bbb54b504afa6ffc967d5831c65098bb93c2e122497ba`)
- `t12_cycle94_battery_attempt1.log` — full battery run log, ends `BATTERY_EXIT=0`
- `b_rx_extract_pr52head.py` — vendored hardened extractor that gated the capture
- `capture_meta.json` / `declare_snapshot.json` / `verdict_bus_seqs.json` / `window_declare_raw.json` — machine-parsed metadata
- `../groth16_ota_20261011T1840Z_cycle84/rx_payload_128b.bin` + `VENDORED_PROVENANCE.json` — c-84 control payload restore (key-33, used as CONTROL-diff1)
- Settle artifacts appended after the Cuneiform devnet run: `chain_readback.json`, `result_summary.txt`, `tests_passed.txt`

**Author: Research Team Bravo (Agent 05, RakMiner-B) — zk-lora-milestone-1 groth16_ota lane**
