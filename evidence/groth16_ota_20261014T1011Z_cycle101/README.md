# groth16_ota cycle-101 — A→B OTA Groth16/BN254 proof, key-43 (identity era)

- **Date:** 2026-10-14 (UTC)
- **Drill:** `groth16_ota` — full T12 battery verification path
- **Verdict:** **COMPLETE VALID** — PRIMARY key-43 VALID (160.2 s) + controls key-42 (162.4 s) + key-41 (161.2 s) all VALID; guards unchanged; `BATTERY_EXIT=0` (attempt2, `t12_cycle101_battery_attempt2.log`)
- **Class:** FIRST-OF-CLASS key-43 — machine-asserted (complete dual-bus history: prior declares B=0 A=0)
- **Settle:** DONE — Cuneiform Devnet TX `Dx8gMUJfYjzpjRNpDv5rjX2CyhLGss3mXshb7nceUqjZqWdYJ4gWMVS8bnGwjPptz2epCMNYXAM1iw7qQtUFKTM`, record PDA `D2PXdQMWdsYqgx6GdXtQE1w6qbyUvusEPc49hHXiqijd` (slot 510985985), chain readback PASS (owner = Cuneiform program, merkle root = payload SHA embedded). See `settle_summary.md` for the c-92 pre-label disclosure.

## Window
| Field | Value |
|---|---|
| Window | B seq 1596 / A seq 633, declared by `declare_rx_window.py --cycle 101` |
| Armed | 2026-10-14T10:11:14Z (arm banner line 1121, skew 0.0 s vs listener lstart) |
| Closes | 2026-10-14T12:11:14Z (tz-aware UTC, 7200 s span) |
| Chip cert | GATE PASS (recovery) ×11 in current standby log; HAL banner `chip version is 0x10 (v1.0)` |
| Listener | pid 413308, `-r 1250 -a 904.3 -b 905.0 -k 0 -m 0 -j -z 255 -n 0` → 903.9 MHz IF -400 kHz, SF9/125 kHz |

## Declare → fire → capture (all values machine-fetched from the buses)
| Field | Value |
|---|---|
| Declare | B1598 / A634 — **byte-equal across 18 fields** (dual-bus diff: NONE) |
| Proof SHA256 | `d3faf880f5a392c0c81f0fa86028e041ed301e454cde35f13f51ed74999a70f0` |
| Key id / deposit | key-43, deposit 100012 |
| Era | identity era, VK `78352ffa…` (sha256 `78352ffa2d0bfe921a49d3016de378263fd1621e65da361dc270b80fab7e88c0`), PK `aea2ed17…` |
| Fire ETA / fired | ETA 11:57:55Z → **fired 11:58:15Z, 5/5 TX_DONE** (B1599/A635), ~95 s declare→fire |
| Capture | **5/5 CRC-OK 128 B** @ 903.9 MHz SF9, SNR +10.5..+12.0 dB, inter-frame ~16.8 s uniform |
| Wrap branch | **POST-WRAP** (machine-selected; pre-wrap fails the fired−180..+240 s gate). Burst walls 11:57:02Z→11:58:09Z; fired completion stamp 11:58:15Z |
| Extract | `tools/b_rx_extract.py session_slice_cycle101.log --expect-sha <full 64-hex> --min-size 100`, rc=0, `sha256_match: true` |

## Honest ledger
- **Abort 1 (12:05:28Z):** `control classes not satisfiable (first-of-class key-43: need 2 distinct-statement-class controls, found 1)` — c-98 key-40 / c-99 key-41 payload bins were stranded on open PR#65's branch (c-91 law). Restored byte-exact from `refs/pull/65/head`, sha-verified against dual-bus declares (62f2019e… = A615/B1538, e5e6c439… = A619/B1553). Provenance: `control_restore_provenance.json`.
- **My label error, corrected same-turn:** the pre-verdict capture confirm (B1600/A636) said "no wrap in window" — hand-derived and WRONG. Machine wrap-branch selector proves POST-WRAP; correction posted B1602/A637 before any verdict.
- Key-43 is FIRST OF ITS STATEMENT CLASS (the machine class scan corrected my own "not-first-of-class" expectation — key-42 ≠ key-43 class).

## Reproduce (fresh checkout of this PR head)
```bash
# 1. capture gate (fail-closed, full 64-hex)
python3 tools/b_rx_extract.py evidence/groth16_ota_20261014T1011Z_cycle101/session_slice_cycle101.log \
  --expect-sha d3faf880f5a392c0c81f0fa86028e041ed301e454cde35f13f51ed74999a70f0 --min-size 100
# expect rc=0, sha256_match true, 5 CRC-OK frames

# 2. payload byte check
sha256sum evidence/groth16_ota_20261014T1011Z_cycle101/rx_payload_128b.bin
# expect d3faf880f5a392c0c81f0fa86028e041ed301e454cde35f13f51ed74999a70f0

# 3. T12 battery (canonical template, ~8 min on A72)
python3 tools/t12_battery_template_canonical_fixed_6a49d04.py --cycle 101 \
  --evidence-dir evidence/groth16_ota_20261014T1011Z_cycle101 \
  --guard-log <your standby guard log — pass explicitly, c-82 law>
# expect final complete line: BATTERY_EXIT=0

# 4. controls the battery picks (restored by this PR, not on main):
#    key-40 62f2019e… (c-98), key-41 e5e6c439… (c-99), key-42 237fad2f… (c-100 dir on this branch)
```

## Bus anchors
- window open: B1596/A633 · declare: B1598/A634 · fired: B1599/A635
- capture confirm: B1600/A636 · wrap-label correction: B1602/A637 · verdict: B1603/A638
