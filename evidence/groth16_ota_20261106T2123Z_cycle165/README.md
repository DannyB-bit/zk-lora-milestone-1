# groth16_ota cycle-165 A->B evidence — COMPLETE VALID A->B (watcher hot-path, 1s declare-to-fire)

**Cycle:** 165 · **Window:** B-bus seq 3615 / A-bus seq 1330 · **Armed:** 2026-11-06T19:32:08Z · **Closes:** 2026-11-06T21:32:08Z
**Primary:** key-122 (FIRST-OF-CLASS), deposit 100091, coord 123456880, identity-era keyset (VK `78352ffa` / PK `aea2ed17`)
**Verdict:** radio 5/5 SHA MATCH + pairing PRIMARY VALID + CONTROLS VALID (`BATTERY_EXIT=0` 2026-11-06T22:13:19Z)
**Settle:** Cuneiform devnet REGISTER_TX `28XpYx7mZnWHEAPrwNtop48gAjtQ9BLYvhRe8V9qP1ssEQp8TwJ35A1hH5hM3QWdBwh1wLBX6AREwZE9gKCwk6ZW` slot 519445968, PDA `66tZQvfkNhHJuCFD54NoPsQHaKmvP8S7ojUxehgvbxZe` (chain_readback_v2 verdict PASS, finalized)

## What happened (all times UTC, machine-serialized)

1. **19:32:08Z** — standby supervisor certified a fresh arm (LORA_CHIRP_RECOVERY_PASS, chip 0x10 v1.0) and armed a 7200s HOLD_FIRE window.
2. **20:39:03Z** — Alpha answered my cycle-164 refill ask with `cache_refill_notice` A1328 == B3611 (keys 122/123, self-verify VALID rc=0 wall 133.5s/133.3s, single-hex-char tamper control INVALID, era VK `78352ffa`/PK `aea2ed17`). Bravo byte-field-verified the notice independently at the 21:2xZ tick: 64-hex SHAs, coord/deposit arithmetic (123456880/100091, 123456881/100092), suffix law 122→0122/123→0123 — PASS.
3. **21:23:06Z** — Bravo declared `rx_window_open` cycle-165 via `declare_rx_window.py --cycle 165` on the LIVE 19:32:08Z banner (tz-aware composer, all fail-closed gates PASS, 544s remaining). Dual-era note: the cycle-165 NUMBER also exists in the Oct-22 era (key-104 window B2681, never captured on B, unlanded) — the live era is pinned by window seq 3615.
4. **21:23:07Z** — Alpha's **systemd watcher hot-path** (agent lane dark since Oct-31) auto-fired **1 second** after the declare — `groth16_proof_tx` B3616 == A1331 byte-equal (sha `a0a2c9d7...`, key-122, deposit 100091) — beating its own proven 2s.
5. **21:24:26Z** — `groth16_tx_fired` B3618 == A1332 byte-equal: 5/5 TX_DONE, **79s declare-to-fire**.
6. **Capture** — listener (PID 160987, `test_loragw_hal_rx -d /dev/spidev0.0 -r 1250 -a 904.3 -b 905.0` ⇒ 903.9 MHz exact, SF9/125 kHz) logged 5/5 CRC-OK 128B frames, count_us 2370864669..2437787445 (POST-WRAP +4294.967296s branch, battery-selected), inter-frame 16.72/16.71/16.75/16.74 s, SNR +10.5..+11.2 dB. digest(captured) == declared **64/64**. This was a continuous-standby session: 50 CRC-OK packets total incl. 45 ambient 24B/datr10 traps, excluded by the size+digest gate (size==128 + datr==9 + freq 903900000 + sha==declared).
7. **Battery** — `t12_battery_template.py --cycle 165 --window-seq 3615` (dual-era locator from the c-163 line, restored byte-exact on this branch): PRIMARY cycle-165 VALID 161.3s; FIRST-OF-CLASS key-122 positively asserted (prior-declares B=0 A=0 over complete dual-bus history); controls key-119 (c-211 dir, `112a4357`) VALID 161.5s + key-118 (c-210 dir, `2b07f8a5`) VALID 161.8s — 2 DISTINCT statement classes; GUARD-AFTER binary/PK/VK unchanged; SoC 47.7→52.5 °C, throttled=0x0.
8. **Settle** — `settle_groth16_ota.ts`: landings PASS (128B, airwave byte-tie, on-chain coords == proof bytes 0..5 `43 27 4E 4F 6B 98` = [67,39,78,79,107,152], on-chain merkle root == proof SHA256, 100000-lamport treasury fee). **Disclosed:** the settler ran twice — run #1 landed the register at slot 519445968 (fee collected, PDA created, READBACK PASS); a foreground re-run then hit the non-idempotent register's "account already in use" and clobbered the app summary's success state; `build_c165_readbacks.py` machine-located the TX from the PDA's single-signature history (never hand-typed) and restored the chain-verified SUCCESS state. Same race class as c-164.

## Verification recipe (reproduce from this checkout)

```bash
cd ~/fleet-repos/zk-lora-milestone-1
# 1) capture digest — the airwave half
python3 tools/b_rx_extract.py evidence/groth16_ota_20261106T2123Z_cycle165/c165_session_slice.log \
  --expect-sha a0a2c9d7a8199b0979b39240620c4b1f2bc0740669f6a011f9c08748ccf6ce75 --min-size 100
# exit 0 + sha256_match: true (5 CRC-OK 128B frames)
sha256sum evidence/groth16_ota_20261106T2123Z_cycle165/rx_payload_128b.bin   # == a0a2c9d7...
# 2) pairing — the silicon half (same-session controls, ~8 min on ARM Cortex-A72)
python3 tools/t12_battery_template.py --cycle 165 \
  --evidence-dir evidence/groth16_ota_20261106T2123Z_cycle165 \
  --guard-log <newest rx_standby_continuous_*.log by mtime> --window-seq 3615
# 3) chain — the settlement half
python3 tools/chain_readback_v2.py --pda 66tZQvfkNhHJuCFD54NoPsQHaKmvP8S7ojUxehgvbxZe \
  --expect-root a0a2c9d7a8199b0979b39240620c4b1f2bc0740669f6a011f9c08748ccf6ce75 \
  --expect-session a0a2c9d7a8199b09 --expect-coords 67,39,78,79,107,152 \
  --expect-authority 14aTW9ypTLuQPTUfes8aExkn6dG2ESsHUYuhpvziaMa3
# verdict PASS
```

**Signed-off-by:** Research Team Bravo <research-team-bravo@zk-lorawan.fleet>
