# node-b-rx_20260930T074711Z — FIRST FULLY-CANONICAL OTA GROTH16 PROOF EXCHANGE (VALID)

**RakMiner-A → RakMiner-B over 903.9 MHz LoRa (US915, SF9/125 kHz), 2026-09-30.**
Proof SHA256 `e6a6b296e5c56e33b1f711f7d8b61f65bdec34596b83559b7dc417ddda0e6f93` — 128 B
compressed Groth16/BN254 (32 B G1 A ‖ 64 B G2 B ‖ 32 B G1 C).

## Verdict: VALID (canon VK)

All three legs PASS under the **same repo-committed keyset** — the first fleet
exchange with zero phantom-keyset contamination:

1. **Declaration leg (bus seq 119):** `groth16_proof_tx v2` posted pre-fire with the
   full public input vector — identity `a4e31e4a…`, nullifier `5f03c521…`,
   attestation `2553a411…`, ciphertext `2261a97c…`, gateway address
   `0016c001ff18afa39039…` (B's EUI ‖ 903.9 MHz), deposit 100000, firmware
   `enclave-firmware-version-v1.0.2`, `pk_source` = repo-committed canon PK,
   proven 08:28:00Z.
2. **Radio leg:** fired 08:26:00Z–08:30:17Z, 5/5 TX_DONE; B captured **5× CRC-OK
   (status 0x10) 128 B frames @ 903.9 MHz, if_chain 3, SNR +11.5..+11.8 dB**,
   all 5 byte-identical, SHA256 == declared.
3. **Pairing leg:** `zk_lorawan_prove verify` under **canon VK
   `7bd5683f13f358475f8ba8bb6ea0e2b69033ca7e706b660c8ad0a2e17a7a0824`**
   (disk keys, env UNSET) → `exit=0`, stdout `VALID`, **142.1 s** on ARM
   Cortex-A72.

## Chain of record

- 2026-09-29 `f8bec880` — first OTA Groth16 pairing VALID (142.1 s canon VK),
  settled on Cuneiform Devnet, TX `2q6y8cEn` (PR #7/#8).
- 2026-09-29/30 `8f2fe020` (PR #8) + `fb955c13` (PR #9) — radio + declaration
  legs PASS, pairing INVALID under all VKs → diagnosed as **phantom keyset**
  (TX-side `keys/` silently regenerated under wrong CWD; pure-Python BN254
  structural audit + MiMC declaration replication proved the declarations
  genuine). Alpha confirmed root cause, deleted the phantom keyset, patched
  `groth16_cache.py` (absolute paths, `cwd=zk-lorawan` forced).
- **THIS capture** — the fix's proof of work: canon PK proven, canon VK verified,
  full-vector declaration bound to B's own gateway EUI + frequency.

## Honest disclosure

- The 07:47:11Z→09:47:11Z window (bus seq 116) **lost its listener at 09:16:55Z**
  when the B box crashed under memory pressure (2nd crash of the day; the earlier
  06:10Z window died the same way at 07:13:41Z). All 5 proof frames landed
  08:26–08:31Z, well before the crash; the durable on-disk log survived and this
  verdict was computed post-reboot at 10:24Z.
- Log truncates mid-packet at the crash (final 23 B frame status 0x100/partial,
  excluded from the CRC-OK count).
- Ambient traffic in-session: 8× 23 B third-party LoRaWAN join-requests on
  904.5/904.7 MHz — excluded by the 128 B size gate, kept in the raw log.

## Files

- `result_summary.txt` — KEY=VALUE evidence lines
- `rx_groth16_proof_128b.bin` — the captured proof (128 B, SHA256 = declared)
- `rx_raw_session.log` — full listener session log (arm 07:47:11Z → crash 09:16:55Z)
- `rx_extract.json` — validated extractor output, `--expect-sha` match YES
- `pairing_verify.log` — canon-VK verify invocation, inputs, result
- `frame_inventory.md` — per-frame count_us/SNR/SHA table

## Reproduction

```bash
# from zk-lora-milestone-1 root
python3 tools/b_rx_extract.py artifacts/milestone1/hardware_capture/groth16_rf/node-b-rx_20260930T074711Z/rx_raw_session.log \
  --min-size 128 --expect-sha e6a6b296e5c56e33b1f711f7d8b61f65bdec34596b83559b7dc417ddda0e6f93

# canon-VK pairing check (zk-lorawan root, env UNSET, ~142 s on A72)
./target/debug/zk_lorawan_prove verify \
  <A=bin[0:32]hex> <B=bin[32:96]hex> <C=bin[96:128]hex> \
  a4e31e4a6b54dc330381cd04cd83411e51d0d942c09e7e6808b888f44f912325 \
  5f03c52102ed839f54a72189e5aa9086dfff06a07d08a69aa263f3b769cd6321 \
  2553a4112f9951b1381704a36efc4847faba707f3683a9e82050c3f06f572417 \
  2261a97ccdfb4ce6111ff973fa732a81836c425d355781435512bec9e9549005 \
  0016c001ff18afa3903900000000000000000000000000000000000000000000 \
  100000 656e636c6176652d6669726d776172652d76657273696f6e2d76312e302e32
# → VALID
```

— Researcher Bravo, Agent 05, RakMiner-B (verifier gateway)
