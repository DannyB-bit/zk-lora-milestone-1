# chirp245 Sealed Frame — CAPTURED → DECRYPTED → ATTESTED (blocker closed 2026-11-06)

**Frame SHA-256:** `6f67d0eb40092106b1317f880f4145b727ab0c2bd1d13e50d00f292d01b701b4`
**Status:** RF capture PASS (5/5 CRC-OK) · decrypt **SUCCESS (81 coords, AES-256-GCM authenticated)** · devnet attest **finalized, all byte checks PASS**

## What happened (timeline, machine-sourced from the A-bus/B-bus events)

| UTC | Event | Fact |
|---|---|---|
| 2026-10-30T01:57:58Z | A1291 `chirp245_tx_fired` | Alpha fired the 245B sealed frame, 5/5 TX_DONE @903.9 MHz SF9/125 kHz/14 dBm |
| 2026-10-30T02:29:00Z | B1293 `chirp245_rx_liveness` | B re-armed after the first window lapsed; chip 0x10 certified |
| 2026-10-30T16:36:08Z | A1296 `chirp245_tx_re_fired` | identical frame re-fired into B's armed window |
| 2026-10-31T~ | B1299 `chirp245_rx_capture_confirmed` | **5/5 CRC-OK captures, SHA matches the declare 64/64**; decrypt BLOCKED (InvalidTag) |
| 2026-11-02..06 | B3338/A1306 amendment | second B keypair exhausted; root cause unresolved — asked Alpha for seal params |
| 2026-11-06T08:10:32Z | A1313 `chirp245_seal_params` | Alpha answered all four from his on-disk artifacts: sealed to c51a77e6…, `tools/chirp245.py @391ec84` `build_chirp()` layout B, HKDF-SHA256 salt `zk-lora-chirp245-v1` info `chirp245-aead-key`, AES-256-GCM nonce=frame[2:14] AAD=None, **no CH25 field** |
| 2026-11-06T17:xx | this PR | open_chirp() from the cited bytes decrypts the captured frame; attest lands on devnet |

## RF capture (B side, ground truth = HAL guard log)

- Log: `~/fleet/logs/rx_standby_continuous_20261030T111714Z.log` (window armed 2026-10-30T11:17:29Z, +7200 s)
- 5 × 245B frames, byte-identical, @ **903.9 MHz** (chan 3, datr 9 = SF9/125 kHz), CRC **0x727B** OK, SNR 10.2–10.8 dB
- First frame wall ≈ 2026-10-30T11:22:21Z (count_us 292747513 from the session arm banner — in-window)
- Machine-extracted payload: `rx_payload_245b.bin` — sha256 == declared value (see SHA256SUMS)

## Decryption (the blocker that stood since Oct-30)

- Seal tool vendored byte-exact from `DannyB-bit/solana-cuneiform-milestone1` commit **391ec84** (`chirp245_tool_391ec84.py`, sha `17f199cb…`): `build_chirp()` / `open_chirp()`, layout B `[0]=ver 1 [1]=n=81 [2:14]=nonce [14:46]=eph X25519 pub [46:245]=ct(183B)||tag(16B)`
- Recipient key: `~/.config/solana/chirp245_bravo_sk.key` — derived pub `c51a77e6…fb118` == `chirp245_bravo_pk.key` == Alpha's cited recipient (triple-checked machine-side)
- `open_chirp(frame, priv)`: X25519 ECDH → HKDF-SHA256(salt=`zk-lora-chirp245-v1`, info=`chirp245-aead-key`, len 32) → AES-256-GCM decrypt (nonce=frame[2:14], AAD=None) → GCM tag authenticates (any flip = InvalidTag, gate G4 of the shipped battery)
- **Result: 81 six-dimensional Cuneiform-U coordinates, bit-exact** — `chirp245_decrypt_result.json`
- Shipped acceptance battery on the vendored bytes (this Pi): `test_chirp245_battery.log` — **G1–G7 PASS, G8 SKIPPED (no `researcher-a-devnet.json` keyfile on this box — the gate's own designed skip, never a weakened gate)**

## Devnet attestation (Program `2is5Q4rPBpZa2RUCXP7FFdHJUYSVNcW5iTxNuf5mSccy`)

- TX: `utjkDtfetAYxtv5tJpa9bgiEXRemFLMH3hg7XahGWdxSSwgAznDaGMNyY9N9WAjwz1sfL4VdzCW9y9H4abpr1iY` — slot **519377675**, **finalized, err=null**
- Record PDA: `2i69ad7qq2pfn5UXbnxQ9jJfwfz3KMUwhJxkZdZfnNUn` (103 B), exactly 1 signature in its history == this TX
- Byte checks: session_id[40:56] == sha256(frame)[:16] ✓ · merkle root[62:94] == sha256(frame) ✓ · authority[8:40] == ops wallet `14aTW9yp…` ✓ · coords[56:62] = [15,7,0,3,4,1] legal dims ✓ · treasury CPI delta exactly **100,000 lamports** ✓
- Full readback: `chirp245_attest_readback.json`

## Verification recipe (fresh checkout)

```bash
sha256sum rx_payload_245b.bin        # must equal 6f67d0eb…701b4
# vendored tool bytes are the record of what ran:
sha256sum chirp245_tool_391ec84.py   # 17f199cb8ab04f7cc9a7d0d42033af2e5bd431511452e5039fbf7b5811c8c390
od -An -v -tx1 rx_payload_245b.bin | tr -d ' \n' > /tmp/frame.hex
od -An -v -tx1 ~/.config/solana/chirp245_bravo_sk.key | tr -d ' \n' > /tmp/sk.hex   # raw 32B key as hex (CLI expects hex)
python3 -u chirp245_tool_391ec84.py verify /tmp/frame.hex /tmp/sk.hex           # prints the 81 coords
```

## Honest ledger

- The RF leg was never in doubt: 5/5 CRC-OK + SHA 64/64 held since Oct-31. **The only blocker was the decrypt path** — my A1300 attempt list used eph32-first layouts, CH25 offsets and wrong HKDF info strings; Alpha's A1313 supplied the exact construction from his commit- pinned seal tool. Root cause disclosed on both buses (B3338/A1300, B3339/A1306 amendment).
- On-chain coords are hash-derived (`unpack_coords_from_chirp_bytes`, attester cannot decrypt — by design); the receiver-side cross-check is legality of dims (G7), not equality with the decrypted coords.
- No re-fire, no re-seal: the original frame was opened with the original seal parameters.
