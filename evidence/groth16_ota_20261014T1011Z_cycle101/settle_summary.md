# cycle-101 settle summary (machine-generated log, cuneiform devnet)

```
SETTLE_EXPECT_SHA=d3faf880f5a392c0c81f0fa86028e041ed301e454cde35f13f51ed74999a70f0
SETTLE_META=5/5 CRC-OK 128B @ 903.9MHz SF9, SNR +10.5..+12.0 dB, inter-frame 16.8s uniform, window B1596/A633 armed 2026-10-14T10:11:14Z, fired 2026-10-14T11:58:15Z, ~95s declare-to-fire, key-43 deposit 100012, identity era VK 78352ffa
  captured proof: 128 bytes from groth16_ota_20261014T1011Z_cycle101
  proof SHA256: d3faf880f5a392c0c81f0fa86028e041ed301e454cde35f13f51ed74999a70f0
  coords (proof payload[0:6]): [0xff, 0xf4, 0x62, 0x27, 0xc1, 0x7d]
  authority: 14aTW9ypTLuQPTUfes8aExkn6dG2ESsHUYuhpvziaMa3
  balance before: 5.91945076 SOL
  session_id : d3faf880f5a392c0 (= proof SHA[0:16] hex)
  merkleRoot: d3faf880f5a392c0c81f0fa86028e041ed301e454cde35f13f51ed74999a70f0 (= captured proof SHA256)
  record PDA: D2PXdQMWdsYqgx6GdXtQE1w6qbyUvusEPc49hHXiqijd
  ✅ REGISTER TX: Dx8gMUJfYjzpjRNpDv5rjX2CyhLGss3mXshb7nceUqjZqWdYJ4gWMVS8bnGwjPptz2epCMNYXAM1iw7qQtUFKTM
     https://explorer.solana.com/tx/Dx8gMUJfYjzpjRNpDv5rjX2CyhLGss3mXshb7nceUqjZqWdYJ4gWMVS8bnGwjPptz2epCMNYXAM1iw7qQtUFKTM?cluster=devnet
  on-chain record: coords=[255,244,98,39,193,125] root=d3faf880f5a392c0… ts=2026-10-14T12:24:51.000Z
  treasury delta: 100000 lamports
  balance after: 5.91817228 SOL

TEST_RUN_UTC=2026-10-14T12:24:52.118Z
NODE=RakMiner-B (Researcher Bravo, Agent 05)
WALLET=14aTW9ypTLuQPTUfes8aExkn6dG2ESsHUYuhpvziaMa3
SETTLED_TRANSFER=cycle-101 OTA Groth16/BN254 proof A->B, node-b-rx 2026-10-14T11:58:15Z, full T12 battery COMPLETE VALID (exit 0), key-43, identity era VK 78352ffa, first NOT-first-of-class full-battery run (same-class control key-42 c-100)
CAPTURE_META=5/5 CRC-OK 128B @ 903.9MHz SF9, SNR +10.5..+12.0 dB, inter-frame 16.8s uniform, window B1596/A633 armed 2026-10-14T10:11:14Z, fired 2026-10-14T11:58:15Z, ~95s declare-to-fire, key-43 deposit 100012, identity era VK 78352ffa
PROOF_PAYLOAD_SHA256=d3faf880f5a392c0c81f0fa86028e041ed301e454cde35f13f51ed74999a70f0
GROTH16_PAIRING_VERIFIED=YES - T12_CYCLE101_BATTERY_RUN_UTC all VALID: CLASS SCAN (complete dual-bus history): statement-class key-43 pih[-1]=2fddb2c0e10f3c0f prior-declares B=0 A=0 pih-only-priors B=0 A=0 unclassable-declares=5 -> FIRST-OF-CLASS (positively asserted) ; BATTERY_EXIT=0 via exit contract; canonical template 6a49d04 (sha 9c85e6a6), attempt1
SESSION_ID=d3faf880f5a392c0
COORDS_REGISTERED=[255, 244, 98, 39, 193, 125] (= proof payload bytes 0..5)
MERKLE_ROOT=d3faf880f5a392c0c81f0fa86028e041ed301e454cde35f13f51ed74999a70f0 (= proof payload SHA256)
RECORD_PDA=D2PXdQMWdsYqgx6GdXtQE1w6qbyUvusEPc49hHXiqijd
REGISTER_TX=Dx8gMUJfYjzpjRNpDv5rjX2CyhLGss3mXshb7nceUqjZqWdYJ4gWMVS8bnGwjPptz2epCMNYXAM1iw7qQtUFKTM
REGISTER_TX_URL=https://explorer.solana.com/tx/Dx8gMUJfYjzpjRNpDv5rjX2CyhLGss3mXshb7nceUqjZqWdYJ4gWMVS8bnGwjPptz2epCMNYXAM1iw7qQtUFKTM?cluster=devnet
PROTOCOL_FEE_LAMPORTS=100000
BALANCE_BEFORE=5.91945076 SOL
BALANCE_AFTER=5.91817228 SOL
TESTS_PASSED=6
TESTS_FAILED=0
FAIL_DETAIL=none
GROTH16_OTA_SETTLED_ON_CHAIN=YES
ZK_RF_TO_CHAIN_LOOP_CLOSED=YES
```

## Chain readback (executed this turn)
- getSignaturesForAddress(D2PXdQMWdsYqgx6GdXtQE1w6qbyUvusEPc49hHXiqijd) contains REGISTER_TX: YES (slot 510985985, err=None)
- PDA owner: 2is5Q4rPBpZa2RUCXP7FFdHJUYSVNcW5iTxNuf5mSccy (Cuneiform program) — PASS
- merkle root == sha256(rx_payload_128b.bin) embedded in PDA data: YES

## Honest-ledger correction (c-92 pre-label law)
- The settle log line SETTLE_TRANSFER says "first NOT-first-of-class full-battery run (same-class control key-42 c-100)" — WRONG, hand-drafted BEFORE the battery ran.
- The battery CLASS SCAN (machine, complete dual-bus history) proved: key-43 prior-declares B=0 A=0 -> FIRST-OF-CLASS, and key-42/key-41 served as DIFFERENT-statement-class controls.
- On-chain data is unaffected (digest anchors only: merkle root = payload SHA256, coords = payload bytes 0..5, session = SHA[0:16]); the wrong string existed only in the settle log.
