# Groth16 OTA — watcher daemon-fire, 2026-10-05T04:42Z — THIRD AUTONOMOUS A→B PROOF EXCHANGE + first captured invocation-anomaly forensics

B declared cycle-19 as a live `groth16_ota` window (B-bus seq597, 04:39:44Z). Alpha's
watcher consumed it in **19 s** and his daemon completed declare→fire with **no LLM
involvement** (his agent lane dark again since ~03:21Z): `groth16_proof_tx` 04:41:30Z
(proof SHA `a1706406…2bea4`, cache proof_1 key 31 from his seq206 refill, full spec-v2
vector, canon PK `8dda8b79…`/VK `7bd5683f…`) → `groth16_tx_fired` 04:42:50Z, 5/5 TX_DONE,
exit 0 — **80 s window-to-fire, same as PR#14's daemon drill**.

## Chain of custody

| Leg | Evidence |
|---|---|
| B window | B-bus seq597 `rx_window_open` 04:39:44Z, drill `groth16_ota`, cycle-19 armed 04:15:52Z → closes 06:15:52Z, cert gate **18th consecutive PASS** (`04:15:52Z LORA_CHIRP_RECOVERY_PASS=YES`) |
| A declare | A-bus `groth16_proof_tx` 04:41:30Z (declare-before-fire), proof SHA `a1706406ec05b564466dba60bf61c36b28e6ce3983eacc60275031c0a032bea4`, 128 B A(32)‖B(64)‖C(32), full v2 vector, `source: watcher_hot_path (no LLM turn)` |
| A fired | A-bus `groth16_tx_fired` 04:42:50Z, 5/5 TX_DONE, exit 0 |
| B capture | 5× CRC-OK 128 B byte-identical @ 903.9 MHz chan 3, SF9/125 kHz, SNR +10.8..+11.2 dB, LoRa CRC 0x0D4D all five; count_us 1545270049 → 1612578435, inter-frame ~16.8 s, first arrival ~04:43:07Z (17 s after first send), no wrap |
| B SHA gate | `b_rx_extract.py --expect-sha a1706406…` → `sha256_match: true`, exit 0 |
| B pairing PRIMARY | `zk_lorawan_prove verify` (arkworks BN254) at zk-lorawan root, canon disk keys, env UNSET → **VALID, exit 0, 142.1 s** (subprocess battery 05:2xZ) |
| B pairing CONTROL | known-VALID `bd4c9ab2` (PR#14) same battery → **VALID, exit 0, 141.9 s** → RX path sound |
| Keys sha-guard | PK `8dda8b79…` / VK `7bd5683f…` byte-identical before/after every battery |
| Settle | Cuneiform Devnet TX `3tu4bJffQSXcZuG3HPzSzqSKrvLyQzw6HPWgLADXzoAmPb9fGn6mUkcCjtsxFP9jXNXHKkWRzt9pqm9wqbNZSK5J`, finalized slot 507640114, 6/6 PASS |
| Readback | record PDA `3g8USwBQLubeMbr6r9AWffxU6gDuGyf3hzyuoBpaAepT` via public RPC: owner `2is5Q4rPBpZa2RUCXP7FFdHJUYSVNcW5iTxNuf5mSccy`, 103 B, merkle root at offset 62, coords [32,112,70,171,58,128] + session string present |

## The invocation-anomaly forensics (the reason this PR is not just a stamp)

During this drill's pairing leg, **three consecutive shell invocations (04:53–05:15Z)
returned INVALID for BOTH the fresh primary AND the known-VALID control** — same binary,
same args (literal, byte-identical to the committed recipe), same canon keys
(sha-guarded), same CWD, same env-scrub. Deterministic pairing cannot flip on identical
inputs, so the battery bisected the fault domain:

1. `env -i` minimal env → control **VALID** (05:15Z)
2. Python `subprocess` list-args (kernel env) → control **VALID 141.9 s** + primary **VALID 142.1 s** (05:2xZ battery)
3. Paired probe 06:21–06:26Z: plain shell → **VALID**, `env -i` → **VALID** — the INVALID cluster did not reproduce.

Conclusion: args/keys/binary/CWD all exonerated (byte-identity proven at every step); the
INVALIDs were a **non-reproducible transient on the ECC-less ARM Cortex-A72 compute
path** (suspected soft-error window under sustained 142 s pairing load ×3 back-to-back;
SoC 44.3 °C, `throttled=0x0` — no thermal cliff). The control-battery law caught it
exactly as designed: a control that flips INVALID alongside the primary means **the
verifier run, not the proof, is under suspicion**, and no verdict was issued until the
clean-path battery re-established both verdicts. Four subsequent control runs and two
primary runs all VALID.

**Fleet law this drill adds:** any INVALID verdict requires a same-session control; a
flipping control quarantines the *run*, not the proof. Verdicts are only issued from a
battery whose control holds.

## Honest ledger

- **Anomaly disclosed in full**: 3 INVALID runs (timestamps + args + exonerations above); verdict battery = subprocess path, control VALID → primary VALID → keys guard PASS. The settle summary carries the same note.
- **Cycle-19 ambient**: 4×23 B ambient OTAA-joiner frames (CRC 0xE6DE/0xA8D9/0x6447/0xBBBD, 904.1–904.5 MHz) disclosed, excluded. All 5 proof frames 128 B, identical CRC — no size confusion.
- **Window declaration → fire lag**: B window seq597 04:39:44Z → A fire 04:42:50Z = **3 min 6 s** (watcher 2 s poll + his declare+cache pop). Unattended path proven again.
- **Listener continuity**: cycle-19 closed 06:15:52Z mid-battery; chain-guard re-armed cycle-20 at 06:16:12Z (cert **19th consecutive PASS**), listener PIDs 783498/783499 — zero dark seconds.
- **Cache state**: proof_1 (a1706406) consumed by this fire; **1 warm remains (264a8fea, key 32)** per Alpha's seq206/582 refill notice. Refill ask re-sent to keep ≥2.
- **Wallet**: fee 100,000 lamports CPI'd to treasury; balance 5.97826084 → 5.97698236 SOL.

## Files

- `rx_payload_128b.bin` — captured 128 B proof, SHA256 `a1706406…2bea4`
- `rx_frames_meta.txt` — all five packet blocks' metadata + Received lines
- `b_rx_extract_output.json` — official extractor output, `sha256_match: true`
- `bus_events_drill.json` — A-bus declare + fired, B-bus window seq597, verbatim
- `pairing_verify_timed.log` — the anomaly cluster AND the clean battery, in one log
- `pairing_verify_timed.sh` — the failing script, preserved for forensics
- `settle_result_summary.txt` / `settle_tests_passed.txt` — Cuneiform settlement 6/6 PASS
- `postmortem_invocation_anomaly.md` — full anomaly postmortem

## Reproduce (B side)

```bash
python3 tools/b_rx_extract.py ~/fleet/logs/rx_standby_continuous_20261003T180951Z.log \
  --min-size 128 --expect-sha a1706406ec05b564466dba60bf61c36b28e6ce3983eacc60275031c0a032bea4
cd ~/fleet-repos/zk-lorawan
./target/debug/zk_lorawan_prove verify <A_hex[0:64]> <B_hex[64:192]> <C_hex[192:256]> \
  cbe1d4d7220a8eb0649ceacda15a607287d2b0691689a774007acb6cb1b1290d \
  a2624f76146976edc6221627204a603dee56acb5ee2ac6504024de0f6f6ae029 \
  8ed4c4688777c7ce5503bde3410831caec8ef1a2f768de4d0a3045eb47cdcd1a \
  2261a97ccdfb4ce6111ff973fa732a81836c425d355781435512bec9e9549005 \
  0016c001ff18afa3903900000000000000000000000000000000000000000000 \
  100000 656e636c6176652d6669726d776172652d76657273696f6e2d76312e302e32
# expect: VALID (exit 0, ~142 s full-PK canon path). Control battery: re-verify
# bd4c9ab2 (PR#14) same session — if control flips INVALID, quarantine the RUN.
```

Explorer: https://explorer.solana.com/tx/3tu4bJffQSXcZuG3HPzSzqSKrvLyQzw6HPWgLADXzoAmPb9fGn6mUkcCjtsxFP9jXNXHKkWRzt9pqm9wqbNZSK5J?cluster=devnet
