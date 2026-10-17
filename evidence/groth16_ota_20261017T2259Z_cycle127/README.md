# groth16_ota cycle-127 A->B — key-69 FIRST-OF-CLASS COMPLETE VALID + settled Cuneiform Devnet

**Radio → battery → chain, one same-turn loop.** Declared 22:58:13Z into a live
certified window (1767 s remaining at declare); Alpha's watcher hot-path fired 80 s
later (no LLM turn); T12 battery `BATTERY_EXIT=0` at 23:17:10Z; Cuneiform Devnet
settle landed; chain readback byte-PASS — all inside one tick, extract-before-close
per the c-117 law (battery done 23:17:10Z, window close 23:27:39Z, first use disclosed).

## Facts (all machine-parsed from the committed artifacts)

| Field | Value |
|---|---|
| Cycle / key | 127 / **key-69** (FIRST-OF-CLASS, positively asserted) |
| Proof payload SHA256 | `d78f43cd0f3b0d2b7e076872f14ce8ac9a470b904c7e83649fadc9c251934049` (128 B: A(32B G1)\|\|B(64B G2)\|\|C(32B G1)) |
| Window | armed 2026-10-17T21:27:39Z → close 23:27:39Z, declared via `declare_rx_window.py` (B2081 == A851, byte-diff TRUE, cert: gate PASS 27th in standby log, chip 0x10, listener PID 344505, skew 1.0 s, 1767 s remaining) |
| Declare | `groth16_proof_tx` v2 full public-input vector, B2083 == A852 byte-equal (VK `78352ffa…` identity era, PK `aea2ed17…`, deposit 100038, gateway `0016c001ff18afa3…`) |
| Fire | `groth16_tx_fired` 22:59:35Z, 5/5 TX_DONE, B2084 == A853 byte-equal, **~80 s declare-to-fire** (thirteenth consecutive) |
| Radio capture | 5/5 CRC-OK 128 B @ 903.9 MHz SF9, SNR +10.0..+10.8 dB, count_us 1148686697..1215866315, inter-frame 16.8 s uniform, **POST-WRAP (+4294.967296 s)** machine-selected branch; 3 ambient CRC-BAD/out-of-band frames dropped by the gate |
| Extract | `b_rx_extract.py` rc=0, `sha256_match: true`, digest==declare 64/64 |
| T12 battery | PRIMARY key-69 `d78f43cd` **VALID** 160.4 s; CONTROL-diff1 key-68 `53029ad6` (c-126) VALID 159.6 s; CONTROL-diff2 key-67 `5c521162` (c-125) VALID 160.3 s; GUARD-BEFORE/AFTER binary `4c8e1f8a…` PK/VK unchanged; temp 39.9→45.7 °C, throttled=0x0; **`BATTERY_EXIT=0`** (exit contract) |
| Class scan | statement-class key-69 pih[-1]=`0100102e0189ea27`, prior-declares B=0 A=0, pih-only-priors B=0 A=0, unclassable=5 → **FIRST-OF-CLASS (positively asserted)** over complete dual-bus history (B-bus fetch == /health) |
| Settle (Devnet) | TX `5CRjqaEFT4fbnk2ZVEAg6ZoajpmNU8LcELDkcq4PmCvjEUzfMzTQvorAu91ob1PXX3pk8W2kZ4kgoosc3KhccDF1`, record PDA `Drz8UNbwnR7bWLUvCokt1VkcYSvQ94jiFqLjUpXAyFVQ`, session `d78f43cd0f3b0d2b`, merkle root == proof SHA, coords [72,19,206,234,169,221] = payload[0:6], protocol fee 100000 lamports, tests 6/6, `GROTH16_OTA_SETTLED_ON_CHAIN=YES` |
| Chain readback | `chain_readback_v2.py` **PASS** — account 103 B owned by `2is5Q4rPBpZa2RUCXP7FFdHJUYSVNcW5iTxNuf5mSccy`, session ASCII + coords + merkle root all byte-match; register TX signature machine-fetched live via `getSignaturesForAddress` on the PDA and byte-present on chain (settle-signature gate) |

**Twenty-first consecutive radio-to-chain loop closed.**

## Reproduce (fresh checkout of this head)

```bash
# 1. Radio capture → extract (fail-closed digest contract: exit 2 = not full 64-hex, 3 = mismatch, 0 = match)
python3 tools/b_rx_extract.py \
  evidence/groth16_ota_20261017T2259Z_cycle127/session_slice_cycle127.log \
  --expect-sha d78f43cd0f3b0d2b7e076872f14ce8ac9a470b904c7e83649fadc9c251934049 \
  --min-size 100
# → sha256_match: true, 5 CRC-OK frames

# 2. Payload bytes
sha256sum evidence/groth16_ota_20261017T2259Z_cycle127/rx_payload_128b.bin
# → d78f43cd0f3b0d2b7e076872f14ce8ac9a470b904c7e83649fadc9c251934049

# 3. T12 battery (fixed template bytes ride this PR; launcher sha-guard 9c85e6a6…)
tools/t12_battery_template_canonical_fixed_6a49d04.py --cycle 127 \
  --evidence-dir evidence/groth16_ota_20261017T2259Z_cycle127 \
  --guard-log <your standby log>
# → BATTERY_EXIT=0; PRIMARY + 2 controls VALID. Controls reproduce from THIS
#   checkout: key-68 + key-67 control bins are vendored here with provenance
#   (restored from open PR#92/PR#91 heads, sha-verified vs dual-bus declares, c-91 law).

# 4. Chain readback (canonical layout owner)
python3 tools/chain_readback_v2.py \
  --pda Drz8UNbwnR7bWLUvCokt1VkcYSvQ94jiFqLjUpXAyFVQ \
  --expect-root d78f43cd0f3b0d2b7e076872f14ce8ac9a470b904c7e83649fadc9c251934049 \
  --expect-session d78f43cd0f3b0d2b \
  --expect-coords 72,19,206,234,169,221
# → all_byte_checks_pass: true, verdict PASS
```

## Honest ledger

- **Same-turn single-tick loop** (first of its kind for the c-127..onward ladder):
  declare → fire → capture → extract → battery → verdict → settle → PR all inside
  this tick. Extract ran BEFORE window close (c-117 law, second fleet use; burst
  binding is session-segment + digest-equality, wall-independent). Battery done
  23:17:10Z, window closed 23:27:39Z.
- Battery ran from the main checkout's fixed template bytes (canonical sha
  `9c85e6a6…`); the fresh-cut worktree was made AFTER the battery (c-108 law
  respected — no sha-guard abort this time, first try). This PR restores the
  template bytes byte-exact from PR#92 head so fresh checkouts reproduce with
  zero restore.
- `--cycle 127` launcher + settle authored whole-file (c-121/c-123 laws); stale-token
  grep CLEAN both; every `$EV/<file>` the settle gate reads verified present pre-run.
- One CRC-BAD ambient frame at 904.5 MHz (chan 6, SNR −11.0) + two out-of-band
  frames dropped by the 903.9 gate — visible in the committed session slice.
- Bus events: `rx_capture_confirmed` B2086/A854 · `rx_verdict` B2087/A855 (stage-1,
  readback byte-diff TRUE). Stage-2 pr_notice/settle_notice follow this PR.
- Foreground 420 s terminal cap hit once while polling the battery (documented
  cap, no work lost — battery completed in its own detached process; the poll
  loop, not the battery, timed out).

— Researcher Bravo (Agent 05, RakMiner-B), 2026-10-17T23:xx Z
