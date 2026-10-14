SETTLE_EXPECT_SHA=237fad2f1b986b3e5302c028002fb8debdbe6d346c23dd4297d66ae5bebff83d
SETTLE_META=5/5 CRC-OK 128B @ 903.9MHz SF9, SNR +10.8..+11.8 dB, inter-frame 16.8s uniform, window B1576/A625 armed 2026-10-14T08:10:53Z, fired 2026-10-14T08:14:56Z, 80s declare-to-fire, key-42 deposit 100011, identity era VK 78352ffa
  captured proof: 128 bytes from groth16_ota_20261014T0810Z_cycle100
  proof SHA256: 237fad2f1b986b3e5302c028002fb8debdbe6d346c23dd4297d66ae5bebff83d
  coords (proof payload[0:6]): [0x98, 0x4f, 0xac, 0xe8, 0xac, 0xdd]
  authority: 14aTW9ypTLuQPTUfes8aExkn6dG2ESsHUYuhpvziaMa3
  balance before: 5.92072924 SOL
  session_id : 237fad2f1b986b3e (= proof SHA[0:16] hex)
  merkleRoot: 237fad2f1b986b3e5302c028002fb8debdbe6d346c23dd4297d66ae5bebff83d (= captured proof SHA256)
  record PDA: CkCFMYBRdnAMJQE96PqTVM7gbiPVsnoPcqUXZJfDUPQ2
  ✅ REGISTER TX: 2L8b5uUAQiHHxzBrXxcWyjriT23U9RAjRWzWj992zinf3FGmnCSFCf9JxKRdySgzCfGbXYpXgRkcpE52uc2vUBWc
     https://explorer.solana.com/tx/2L8b5uUAQiHHxzBrXxcWyjriT23U9RAjRWzWj992zinf3FGmnCSFCf9JxKRdySgzCfGbXYpXgRkcpE52uc2vUBWc?cluster=devnet
  on-chain record: coords=[152,79,172,232,172,221] root=237fad2f1b986b3e… ts=2026-10-14T10:08:07.000Z
  treasury delta: 100000 lamports
  balance after: 5.91945076 SOL

TEST_RUN_UTC=2026-10-14T10:08:08.670Z
NODE=RakMiner-B (Researcher Bravo, Agent 05)
WALLET=14aTW9ypTLuQPTUfes8aExkn6dG2ESsHUYuhpvziaMa3
SETTLED_TRANSFER=cycle-100 OTA Groth16/BN254 proof A->B, node-b-rx 2026-10-14T08:14:56Z, FIRST FULL T12 BATTERY COMPLETE VALID (exit 0), key-42 first-of-class, identity era VK 78352ffa
CAPTURE_META=5/5 CRC-OK 128B @ 903.9MHz SF9, SNR +10.8..+11.8 dB, inter-frame 16.8s uniform, window B1576/A625 armed 2026-10-14T08:10:53Z, fired 2026-10-14T08:14:56Z, 80s declare-to-fire, key-42 deposit 100011, identity era VK 78352ffa
PROOF_PAYLOAD_SHA256=237fad2f1b986b3e5302c028002fb8debdbe6d346c23dd4297d66ae5bebff83d
GROTH16_PAIRING_VERIFIED=YES - T12_CYCLE100_BATTERY_RUN_UTC all VALID: FIRST-OF-CLASS key-42 (positive assertion, complete dual-bus history) + machine-picked distinct-class identity-era controls key-41 (c-99) + key-40 (c-98), B die; canonical template with 33eefd9 fixes PORTED (sys.exit exit-contract + era-pin + phantom-join, sha 9c85e6a6), BATTERY_EXIT=0 via exit contract; attempt5 clean pass
SESSION_ID=237fad2f1b986b3e
COORDS_REGISTERED=[152, 79, 172, 232, 172, 221] (= proof payload bytes 0..5)
MERKLE_ROOT=237fad2f1b986b3e5302c028002fb8debdbe6d346c23dd4297d66ae5bebff83d (= proof payload SHA256)
RECORD_PDA=CkCFMYBRdnAMJQE96PqTVM7gbiPVsnoPcqUXZJfDUPQ2
REGISTER_TX=2L8b5uUAQiHHxzBrXxcWyjriT23U9RAjRWzWj992zinf3FGmnCSFCf9JxKRdySgzCfGbXYpXgRkcpE52uc2vUBWc
REGISTER_TX_URL=https://explorer.solana.com/tx/2L8b5uUAQiHHxzBrXxcWyjriT23U9RAjRWzWj992zinf3FGmnCSFCf9JxKRdySgzCfGbXYpXgRkcpE52uc2vUBWc?cluster=devnet
PROTOCOL_FEE_LAMPORTS=100000
BALANCE_BEFORE=5.92072924 SOL
BALANCE_AFTER=5.91945076 SOL
TESTS_PASSED=6
TESTS_FAILED=0
FAIL_DETAIL=none
GROTH16_OTA_SETTLED_ON_CHAIN=YES
ZK_RF_TO_CHAIN_LOOP_CLOSED=YES
SETTLE_RC=0
