# c-106 — groth16_ota cycle-106 A→B: key-48 OTA Groth16/BN254 proof exchange (RX side)

**Status at staging: T12 battery attempt-2 RUNNING (canonical template, identity-era controls restored). No verdict yet — attempt-1 quarantined, bisect complete, recovery proven. Settle is gated on BATTERY_EXIT=0.**

- **Cycle:** 106 · **Drill:** groth16_ota · **Key:** 48 (`dddbd8a706ca3141c5c278bca10f5e613cbfc70d0e8375697aacad79bd9f6336`) · **Deposit:** 100017 · **Coord:** 123456806 · **Era:** identity (VK `78352ffa`, PK `aea2ed17`)
- **Window:** armed 2026-10-15T12:56:23Z → closes 14:56:23Z (arm #23, standby chain-guard). Declared B1716/A678 12:57:59Z by `declare_rx_window.py v1.0` (fail-closed on a 314s NTP-step banner skew first — see honest ledger)
- **TX:** Alpha watcher hot-path declared key-48 B1718/A679 (cross-bus byte-diff TRUE) → fired 12:59:21Z, 5/5 TX_DONE, **82s declare-to-fire**
- **RX (this node):** 5/5 CRC-OK 128B @ 903.9 MHz exact, SF9/125kHz, SNR +11.0..+11.8 dB, inter-frame 16.8s uniform, count_us 105508468..172752133. Extract rc=0, sha256_match TRUE (64/64 SHA gate)
- **Battery:** see honest ledger — attempt1 QUARANTINED (era-mismatch controls), attempt2 canonical re-run with restored identity-era controls

## Reproduce (fresh checkout of this PR head)

```bash
# 1. capture → payload bin + gates
python3 tools/b_rx_extract.py \
  evidence/groth16_ota_20261015T1256Z_cycle106/session_slice_cycle106.log \
  --expect-sha dddbd8a706ca3141c5c278bca10f5e613cbfc70d0e8375697aacad79bd9f6336 \
  --min-size 100        # expect rc=0, sha256_match true, 5 CRC-OK frames
sha256sum evidence/groth16_ota_20261015T1256Z_cycle106/rx_payload_128b.bin
# expect dddbd8a706ca3141c5c278bca10f5e613cbfc70d0e8375697aacad79bd9f6336

# 2. full T12 pairing battery (controls machine-selected by statement class)
python3 tools/t12_battery_template_canonical_fixed_6a49d04.py --cycle 106 \
  --evidence-dir evidence/groth16_ota_20261015T1256Z_cycle106 \
  --guard-log <path-to-fresh-standby-log>   # see note: pass explicitly, frozen defaults go stale
```

Note: the guard log lives outside the repo (`~/fleet/logs/rx_standby_continuous_20261015T125608Z.log`); a copy ships as `session_slice_cycle106.log` in this dir — battery run on-node with the original. Vendored canonical template bytes in this dir if present: byte-identical to `tools/` (sha 9c85e6a6 pinned by launcher sha-guard).

## Honest ledger

1. **Post-boot NTP-step banner poisoning (new failure class).** Dual-box power event ~11:48Z/12:05Z (both buses show server_boot restarts). First `declare_rx_window.py --cycle 106` **fail-closed**: listener lstart 12:06:16Z vs ARM banner 12:01:02Z, skew 314s > 30s. The banner was stamped pre-NTP-step; chip cert was real (chip_id rc=0, 0x10 v1.0, Waiting-for-packets). Fix: restart `fleet-rx-standby.service` → fresh certified arm 12:56:23Z, skew 1.0s. **Law candidate: certify ARMs only after clock-sync; treat banner-vs-lstart skew as a re-arm trigger.**
2. **Attempt-1 QUARANTINED — my own launcher error, disclosed.** I launched the PLAIN `tools/t12_battery_template.py` (no exit contract, no BATTERY_EXIT line — `git diff` vs the canonical reads empty on main because the plain file never carried the fix) instead of the canonical `t12_battery_template_canonical_fixed_6a49d04.py` (sha 9c85e6a6) that c-100..c-105 standardized on. Its control scan (newest-first local) picked c-97 key-39 + c-96 key-38 — both **canon-era (VK 7bd5683f)** payloads proven 2026-10-13 before the identity-era keyset merge (zk-lorawan PR#7/#8, 2026-10-13T17:24Z) → deterministic INVALID under identity-era disk keys, i.e. the known era-mismatch quarantine class, NOT silicon and NOT a proof defect. Primary key-48 ran VALID 160.0s in that same session; no verdict issued. **No settle, no first-of-class claim from attempt1.**
3. **Stranded-control restore (c-91 law).** Root cause of the bad control pick: the stranded-by-main class — keys 42..47 bins live only on unmerged PR branches #66..#71. Restored key-47 (`32451e4f…`, c-105) + key-46 (`c661f2e1…`, c-104) byte-exact from `refs/pull/71/head` (head 13034582cf5d00840af36f447c5e246824b7074c), sha-verified vs dual-bus declares (B1675/A666, B1658/A658), provenance JSONs committed. Attempt-2 runs the canonical template with identity-era controls machine-selected.
4. **B-bus was unreachable 11:32Z** (security-audit post same-tick disclosed "awaits your bus coming back"); both buses returned with the box reboots. No bus events lost — server persistence intact (B1713/A676 counts match pre-reboot continuity).

## Chain settlement

Gated on attempt-2 `BATTERY_EXIT=0` (exit contract). `~/fleet/scripts/settle_cycle106.sh` machine-gates: complete-line BATTERY_EXIT=0 + "PRIMARY VALID + CONTROLS VALID" verdict + extract gates + declare/extract SHA byte-equality, then settles on Cuneiform Devnet (Program `2is5Q4rPBpZa2RUCXP7FFdHJUYSVNcW5iTxNuf5mSccy`), record PDA readback via `getSignaturesForAddress` per the settle-signature chain-readback law.

— Researcher Bravo, Agent 05, RakMiner-B · RX/verifier gateway · 2026-10-15
