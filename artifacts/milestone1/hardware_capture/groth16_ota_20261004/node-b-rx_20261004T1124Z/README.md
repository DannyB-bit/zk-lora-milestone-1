# Groth16 OTA — canon re-prove refire, 2026-10-04T11:24:37Z — FULLY-CANONICAL EXCHANGE: radio 5/5 + pairing VALID + devnet settle

Twin drill that closes the phantom-keyset incident opened in PR #12: RakMiner-A re-proved
the same witness under the repo-committed canon keyset (PK 8dda8b79…, VK 7bd5683f…),
declared the full public-input vector, and fired into RakMiner-B's cycle-10 standby
window. Every leg passed. This supersedes the PR #12 **pairing** verdict only; the
PR #12 radio evidence (phantom capture) stands.

## Chain of custody
1. **B window** — A-bus seq179 `rx_window_open` (drill `groth16_ota`), cycle-10 of the
   continuous standby guard, armed 2026-10-04T10:12:49Z → 12:12:49Z. Cert gate
   `LORA_CHIRP_RECOVERY_PASS=YES` (log `lora_chirp_recovery_node-b-rx_20261004T101239Z.log`).
2. **A root-cause audit** — seq186 `groth16_vk_audit`: the PR #12 payload 3b9b6d2e was
   proven under a **phantom keyset** (PK d5589c30…/VK 87800a21…) generated 2026-09-30 by
   `groth16_cache.py` invoking `zk_lorawan_prove` with CWD=fast-channel, where the
   CWD-relative `keys/` path found no keys and silently regenerated via OsRng. The
   "repo-committed seed-42" pk_source string was hardcoded boilerplate — false in fact.
   Cache quarantined; fixes: subprocess cwd pinned to the repo root, VK-SHA abort gate,
   canon key copies staged into fast-channel/keys/.
3. **A declaration** — seq187 `groth16_proof_tx` kind `canon_reprove_refire`: proof SHA
   `fc8160800267296e36f81cb1839a378fbd34520aef9387c48fcf5d07f3c57261`, full spec-v2 vector
   (4×32B hashes + gateway + deposit + firmware), PK/VK SHAs **measured at prove time**
   (8dda8b79…/7bd5683f…), self-verify VALID at repo root 11:23Z.
4. **A fired** — seq188 `tx_fired` 11:24:37Z→11:26:00Z, self-reported
   `UNEXPECTED count 0` (TX-side log-parse artifact — see honest ledger).
5. **B capture** — 5× CRC-OK 128 B frames @ 903.9 MHz chan 3, SF9/125 kHz, SNR
   +10.8..+11.8 dB, LoRa CRC 0x847A on all five, byte-identical, SHA256 = declared
   `fc816080…` (`tools/b_rx_extract.py` → `sha256_match: true`). First arrival
   wrap-corrected to 11:24:47Z (10 s after fire), inter-frame ~16.7 s.
6. **B pairing** — `zk_lorawan_prove verify` (arkworks BN254) at the zk-lorawan repo
   root, canon disk keys, `ZK_LORAWAN_REPRODUCIBLE_SETUP` UNSET → **VALID**, 142.3 s,
   exit 0 (full-PK canon path; a ~6 s return would indicate the regen path).
7. **Differential battery (one session, same binary/VK/keys)** — phantom payload
   3b9b6d2e re-verified → **INVALID** (exit 1). Same public inputs, same witnesses,
   only the keyset differs → the PR #12 INVALID was genuine and the root cause is
   confirmed as keyset-only. Keys sha256-guarded byte-identical before/after.
8. **Settle** — Cuneiform Devnet `register_coordinates` TX
   `4Cnnn7HmX9dnyRydF7mYJn1PeMf8eYfsAa7VScLAhoBzZtRHnSC2RUSUgx5Tzk4GJw84JjVXqdKUyvubsqdb5iJc`,
   session `fc8160800267296e`, PDA `4D6GGPy2TN8gWRFr28wp2qx3NPZyB13UdFkWyFTxRw2y`,
   coords = proof bytes 0..5, merkle root = proof SHA256, 100k-lamport treasury CPI,
   6/6 PASS (see cuneiform repo `groth16_ota_settlement_20261004_canon_refire`).

## Reproduce the pairing (any ARM Cortex-A72 with the repo)
```bash
python3 tools/b_rx_extract.py <standby_log> --min-size 128     --expect-sha fc8160800267296e36f81cb1839a378fbd34520aef9387c48fcf5d07f3c57261
cd ~/fleet-repos/zk-lorawan   # CWD MUST be the repo root (relative keys/ path)
./target/debug/zk_lorawan_prove verify     <A_hex[0:64]> <B_hex[64:192]> <C_hex[192:256]>     cbe1d4d7220a8eb0649ceacda15a607287d2b0691689a774007acb6cb1b1290d     a2624f76146976edc6221627204a603dee56acb5ee2ac6504024de0f6f6ae029     8ed4c4688777c7ce5503bde3410831caec8ef1a2f768de4d0a3045eb47cdcd1a     2261a97ccdfb4ce6111ff973fa732a81836c425d355781435512bec9e9549005     0016c001ff18afa3903900000000000000000000000000000000000000000000     100000     656e636c6176652d6669726d776172652d76657273696f6e2d76312e302e32
# expected: VALID, exit 0, ~142 s
```

## Files
- `rx_payload.bin` — captured on-air canon proof (128 B), SHA256 fc816080…
- `phantom_payload_3b9b6d2e.bin` — PR #12 payload, kept for the differential battery
- `capture_frames.json` — the 5 canon frames + wrap-corrected wall times (+ phantom reference)
- `b_rx_extract_output.json` — full parser output over the continuous standby log
- `capture_log_cycle10_excerpt.txt` — verbatim standby-log lines 1085–1208 (arm → capture → Test End)
- `pairing_verify.log` — canon verify, full stdout (VALID)
- `phantom_differential_verify.log` — phantom re-verify, same session (INVALID, exit 1)
- `pairing_verify_result.txt` — KEY=VALUE pairing record
- `bus_events_drill.json` — A-bus seq 179–190 + B-bus mirror
- `result_summary.txt` — M1-format KEY=VALUE summary

## Honest ledger
1. **`tx_fired` seq188 `UNEXPECTED count 0`** — Alpha's TX-side send counter failed to
   parse its own log; my RX captured 5/5 byte-exact frames, so the radio chain is clean.
   Disclosed by Alpha in-event, confirmed by B-side capture.
2. **PR #12 pairing INVALID stands as correct for its payload.** 3b9b6d2e was proven
   under the phantom keyset; its radio leg (5/5 SHA match) remains valid evidence. This
   PR supersedes the pairing verdict only, by differential proof.
3. **Ambient exclusions (fail-closed):** 1 B @904.3 MHz CRC-bad (count_us 2607592004),
   23 B @904.7 MHz SF10 CRC-OK (count_us 802386223, LoRaWAN-ish uplink, not fleet).
4. **count_us wrap** — cycle-10 spans 2 h (>71.6 min); first-capture wall time uses
   arm + count_us/1e6 + 4294.967296 s. Unit-tested against the declared fire window
   (first_rx 11:24:47Z vs fired 11:24:37Z ⇒ 10 s propagation, sane).
5. **This morning's settle of 3b9b6d2e** (TX 5fUhvJkW…) stays on-chain as a disclosed
   radio-transfer record with pairing unverified, per the TX-2JDPHtqW precedent; the
   canon-VALID settle is the one bound to this PR.
6. No decode recipes or key material are settled on-chain — digests only (ZK Settlement Law).
