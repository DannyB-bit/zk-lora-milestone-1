# node-b-rx_20260930T011100Z — Groth16 OTA v2 window capture (key_32 refire)

## What happened
- B armed certified always-on window 01:01:00Z (bus seq86, closes 03:01:00Z).
- Alpha's watcher posted spec-v2 declaration seq87 (private_key_id 32, deposit 100001,
  proof SHA fb955c138fb53c52876f78a4661e363faf19a31143169cf5b7396634f1f2000b) then fired 5/5 TX_DONE 01:12:33Z (seq88).
- B captured **5/5 CRC-OK 128 B frames @ 903.9 MHz SF9, SNR +10.5..+11.0 dB, all byte-exact
  vs the TX-declared SHA** — the radio + declaration-binding legs are now fully mastered
  (declaration was key_32-consistent, verified by pure-Python MiMC recomputation).
- 3 additional CRC-bad ghosts demodulated on adjacent IF channels (chan 5/6, status 0x11) — kept as forensic artifacts.

## Pairing verification (fail-closed)
| VK / variant | elapsed | verdict |
|---|---|---|
| canon disk VK 7bd5683f, declared vector | 142.0 s | INVALID |
| seed-42 regen VK, declared vector | 6.2 s | INVALID |
| canon, deposit 100000 (off-by-one probe) | 142.1 s | INVALID |
| canon, gateway zeros | 142.1 s | INVALID |
| canon, gateway zeros + deposit 100000 | 142.1 s | INVALID |
| layout permutations A/C/B swap x6 | ~6 s each | INVALID |
| **CONTROL: fresh print-proof bundle (canon PK)** | 142.1 s | **VALID** |
| **CONTROL: f8bec880 recapture (canon VK)** | 142.0 s | **VALID** |

## Structural audit (pure-Python BN254, ark-ec 0.4.2 SWFlags semantics)
All three points decode with valid flags, x < p, on-curve, **correct subgroup ([r]P == O)** —
the frame is a genuine Groth16-shaped proof from *some* keyset.

## Root cause
The proof is bound to a **third proving keyset** — neither the repo-committed canon PK
(8dda8b79) nor the seed-42 regen. Prime suspect: TX-side `keys/` was silently regenerated
by an OsRng fallback (deserialize failure path in `ZKLoRaWANProver::new()`) after the
15:35Z f8b generation, orphaning the hot-path pre-proven cache.

## Fix recipe for RakMiner-A (in Issue #1 comment)
1. `cd zk-lorawan && sha256sum keys/*.bin` — expect PK 8dda8b79..., VK 7bd5683f...
2. If diverged: `git checkout -- keys/` (canon keys are repo-committed), purge pre-proven cache.
3. Regenerate proof with canon PK (env UNSET, ~10 min arkworks on A72), self-verify
   locally vs canon VK, THEN declare + fire.

## Verdict
Radio/protocol legs PASS; ZK pairing leg FAIL — **fail-closed, disclosed, no verified-proof
settlement for fb955c13**. f8bec880 remains the settled VALID OTA Groth16 proof (TX 2q6y8cEn).
