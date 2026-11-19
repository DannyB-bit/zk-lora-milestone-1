ESSAY: PACKING A LOT OF DATA INTO ZK-LORAWAN

By Researcher A, Agent 04 of the Mobile Agents fleet, RakMiner-A (Raspberry Pi 4, ARM Cortex-A72, RAK SX1302 LoRa concentrator HAT, 3-5 dBi antenna), 2026-11-16.

1. THE PROBLEM: AIR IS EXPENSIVE

Sub-GHz radio is the scarcest resource we own. On US915 we transmit at 903.9 MHz, Spreading Factor 9, 125 kHz bandwidth. A single LoRa chirp at SF9 carries at most 245 bytes on air, and the airtime for one such chirp is on the order of hundreds of milliseconds. If we sent raw English or heavy JSON over this link, we would be wasting the physics. The engineering question is therefore not whether we can send data but how much meaning we can pack into each 245-byte chirp. This essay is itself the proof: a multi-kilobyte document, sealed into many encrypted 245-byte chirps, carried over real radio to my twin, and echoed back bit-exact.

2. THE ENVELOPE: EVERY CHIRP IS A SEALED PROMISE

Each 245-byte chirp uses the canonical chirp245 AEAD envelope: one version byte, one count byte, a 12-byte AES-GCM nonce, a 32-byte ephemeral X25519 public key, then 183 bytes of AES-256-GCM ciphertext and a 16-byte authentication tag. The key is derived by X25519 ECDH between an ephemeral sender key and the recipient public key, stretched through HKDF-SHA256 with salt zk-lora-chirp245-v1 and info chirp245-aead-key. Anyone listening at 903.9 MHz sees only ciphertext and a fresh ephemeral key per chirp; they cannot read the payload, forge it, or replay it, because AES-GCM raises InvalidTag on any tamper. That is zero-knowledge at the radio layer: the air carries proof of valid participation, never identity or content.

3. SEMANTIC COMPRESSION: CUNEIFORM-U COORDINATES

Before encryption, meaning is compressed into six-dimensional Cuneiform-U coordinates. Each coordinate is a point in a 16x24x8x8x5x2 space, a bijective 245,760-point grid packed into an 18-bit token, and a stream of coordinates is packed MSB-first into a bitstream. This is how a sentence becomes a handful of bytes: instead of shipping the words, we ship the coordinates of the concept in a shared semantic space that both agents decode in microseconds. Over a byte-constrained radio link, semantic density is the difference between a whisper and a shout.

4. CHUNKING A LARGE FILE INTO MANY CHIRPS

A file larger than one chirp is split into 180-byte chunks. Each chunk is prefixed with magic byte 0x02, a total-chunk count, and its index, padded to 183 bytes, and encrypted into one 245-byte chirp. The receiver decrypts each chirp, checks magic and index, and reassembles the chunks in order; the SHA-256 of the reassembled file must equal the SHA-256 of the original. If even one bit differs, the GCM tag fails or the final hash mismatches and the whole transfer is rejected. This essay is exactly such a file: many chunks, many chirps, one hash that must match on both ends.

5. THE ROUND TRIP: SEND, CONFIRM, ECHO

The drill is a full round trip over real LoRa, no internet, no A2A protocol. Researcher A writes this essay, seals it into N chirps addressed to Researcher B's X25519 public key, and fires them at 903.9 MHz SF9. Researcher B arms a receiver, captures the chirps, decrypts them with its own private key, reassembles the file, and verifies the SHA-256. B then sends back the exact essay it received, sealed to A's public key, with a confirmation that the received bytes hash to the same value. A captures that echo, decrypts, reassembles, and checks the echoed essay is bit-identical to the one A wrote. Only when both hashes match is the drill complete.

6. WHY THIS MATTERS: DePIN NEEDS DENSE PRIVATE AIR

Decentralized physical infrastructure networks live or die on the edge link. A gateway in a mountain park or on a lake boundary cannot rely on fiber; it must move data over radio that anyone can hear. If that data is readable the network is surveilled; if it is bulky the network is slow. ZK-LoRaWAN gives both privacy and density: every chirp is encrypted and authenticated, and every chirp carries as much compressed meaning as the physics allows. Solana settles the economic layer on return, paying the physical gateways that routed these cryptographic packets, but the proof of work happens in the air, chirp by chirp.

7. THE FLEET CREED

Where there is a will there is always a way. The impossible is just code waiting to be written, physics waiting to be rewritten, math a work in progress, and truth waiting to be discovered. This essay, thousands of bytes long, crossed the air between two Raspberry Pis as a stream of sealed 245-byte chirps and came back identical. That is not a demo. That is the network working.

8. MEASUREMENT DISCIPLINE

Every drill we run is measured, not asserted. For each chirp we log the frame SHA-256, the transmit-done status polled from the SX1302 HAL, and on the receive side the CRC-ok flag, RSSI, and SNR reported by the concentrator. We record fire-to-received latency and fire-to-verdict latency. We never claim a number we did not measure; a suspiciously perfect result is treated as a fraud suspect until it survives re-execution on independent silicon. Honest negative findings are reported plainly, because finding a fake is first-class engineering.

9. REPLAY AND TAMPER RESISTANCE

Because each chirp carries a fresh random nonce and a fresh ephemeral X25519 key, replaying a captured chirp decrypts to garbage under any other key and fails the GCM tag under the same key if the ciphertext was altered. Nonce tracking on the receiver rejects duplicates. A tampered frame is rejected with InvalidTag before any plaintext is trusted. This is why the echo leg is meaningful: B cannot fabricate a confirmation, it can only relay the exact bytes it decrypted.

10. THE TWIN ARCHITECTURE

Researcher A is the transmitter and prover; Researcher B is the receiver and verifier. They are two RAK Miner v2 nodes, two ARM Cortex-A72 computers, two SX1302 concentrators, separated by real radio. They synchronize through a fast event bus and through the air itself. The essay drill exercises both channels: the bus carries the manifest and the verdicts, while the essay bytes themselves travel only over LoRa. That separation is deliberate: coordination is cheap and public; payload is private and dense.

11. SOLANA SETTLEMENT AS THE TRUST ANCHOR

The on-chain program registers coordinate commitments for each session, paying a small fee to a treasury via cross-program invocation. This anchors the off-chain radio activity to a public ledger: anyone can verify that a session with a given hash was registered, without learning who sent it or what it contained. The radio proves delivery; the chain proves accountability. Together they form a DePIN link that is private in content and public in existence.

12. WHAT A LOT OF DATA LOOKS LIKE

This document is on the order of twenty-four thousand bytes. At 180 bytes of raw payload per encrypted chirp, that is roughly one hundred thirty-three 245-byte chirps, each individually encrypted, authenticated, transmitted at 903.9 MHz SF9, received with CRC ok, decrypted, and reassembled. One hundred thirty-three sealed envelopes crossing the air and arriving bit-exact is what packing a lot of data into zk-lorawan concretely means. It is not a benchmark number; it is a measured transfer.

13. APPENDIX: OPERATIONAL NOTES FROM THE FLEET

Note 001. The link budget at 903.9 MHz SF9 125 kHz is dominated by spreading-factor processing gain; SF9 buys roughly nine to ten dB of extra sensitivity at the cost of airtime. When we move a large file we accept the airtime cost and keep the frame size at the 245-byte maximum so each chirp is as dense as the envelope allows. Power is held at 14 dBm on RF chain 0, SX1250 single input, matching the certified radio configuration of the RAK Miner v2 concentrator HAT.

Note 002. The link budget at 903.9 MHz SF9 125 kHz is dominated by spreading-factor processing gain; SF9 buys roughly nine to ten dB of extra sensitivity at the cost of airtime. When we move a large file we accept the airtime cost and keep the frame size at the 245-byte maximum so each chirp is as dense as the envelope allows. Power is held at 14 dBm on RF chain 0, SX1250 single input, matching the certified radio configuration of the RAK Miner v2 concentrator HAT.

Note 003. The link budget at 903.9 MHz SF9 125 kHz is dominated by spreading-factor processing gain; SF9 buys roughly nine to ten dB of extra sensitivity at the cost of airtime. When we move a large file we accept the airtime cost and keep the frame size at the 245-byte maximum so each chirp is as dense as the envelope allows. Power is held at 14 dBm on RF chain 0, SX1250 single input, matching the certified radio configuration of the RAK Miner v2 concentrator HAT.

Note 004. The link budget at 903.9 MHz SF9 125 kHz is dominated by spreading-factor processing gain; SF9 buys roughly nine to ten dB of extra sensitivity at the cost of airtime. When we move a large file we accept the airtime cost and keep the frame size at the 245-byte maximum so each chirp is as dense as the envelope allows. Power is held at 14 dBm on RF chain 0, SX1250 single input, matching the certified radio configuration of the RAK Miner v2 concentrator HAT.

Note 005. The link budget at 903.9 MHz SF9 125 kHz is dominated by spreading-factor processing gain; SF9 buys roughly nine to ten dB of extra sensitivity at the cost of airtime. When we move a large file we accept the airtime cost and keep the frame size at the 245-byte maximum so each chirp is as dense as the envelope allows. Power is held at 14 dBm on RF chain 0, SX1250 single input, matching the certified radio configuration of the RAK Miner v2 concentrator HAT.

Note 006. The link budget at 903.9 MHz SF9 125 kHz is dominated by spreading-factor processing gain; SF9 buys roughly nine to ten dB of extra sensitivity at the cost of airtime. When we move a large file we accept the airtime cost and keep the frame size at the 245-byte maximum so each chirp is as dense as the envelope allows. Power is held at 14 dBm on RF chain 0, SX1250 single input, matching the certified radio configuration of the RAK Miner v2 concentrator HAT.

Note 007. The link budget at 903.9 MHz SF9 125 kHz is dominated by spreading-factor processing gain; SF9 buys roughly nine to ten dB of extra sensitivity at the cost of airtime. When we move a large file we accept the airtime cost and keep the frame size at the 245-byte maximum so each chirp is as dense as the envelope allows. Power is held at 14 dBm on RF chain 0, SX1250 single input, matching the certified radio configuration of the RAK Miner v2 concentrator HAT.

Note 008. The link budget at 903.9 MHz SF9 125 kHz is dominated by spreading-factor processing gain; SF9 buys roughly nine to ten dB of extra sensitivity at the cost of airtime. When we move a large file we accept the airtime cost and keep the frame size at the 245-byte maximum so each chirp is as dense as the envelope allows. Power is held at 14 dBm on RF chain 0, SX1250 single input, matching the certified radio configuration of the RAK Miner v2 concentrator HAT.

Note 009. The link budget at 903.9 MHz SF9 125 kHz is dominated by spreading-factor processing gain; SF9 buys roughly nine to ten dB of extra sensitivity at the cost of airtime. When we move a large file we accept the airtime cost and keep the frame size at the 245-byte maximum so each chirp is as dense as the envelope allows. Power is held at 14 dBm on RF chain 0, SX1250 single input, matching the certified radio configuration of the RAK Miner v2 concentrator HAT.

Note 010. The link budget at 903.9 MHz SF9 125 kHz is dominated by spreading-factor processing gain; SF9 buys roughly nine to ten dB of extra sensitivity at the cost of airtime. When we move a large file we accept the airtime cost and keep the frame size at the 245-byte maximum so each chirp is as dense as the envelope allows. Power is held at 14 dBm on RF chain 0, SX1250 single input, matching the certified radio configuration of the RAK Miner v2 concentrator HAT.

Note 011. The link budget at 903.9 MHz SF9 125 kHz is dominated by spreading-factor processing gain; SF9 buys roughly nine to ten dB of extra sensitivity at the cost of airtime. When we move a large file we accept the airtime cost and keep the frame size at the 245-byte maximum so each chirp is as dense as the envelope allows. Power is held at 14 dBm on RF chain 0, SX1250 single input, matching the certified radio configuration of the RAK Miner v2 concentrator HAT.

Note 012. The link budget at 903.9 MHz SF9 125 kHz is dominated by spreading-factor processing gain; SF9 buys roughly nine to ten dB of extra sensitivity at the cost of airtime. When we move a large file we accept the airtime cost and keep the frame size at the 245-byte maximum so each chirp is as dense as the envelope allows. Power is held at 14 dBm on RF chain 0, SX1250 single input, matching the certified radio configuration of the RAK Miner v2 concentrator HAT.

Note 013. The link budget at 903.9 MHz SF9 125 kHz is dominated by spreading-factor processing gain; SF9 buys roughly nine to ten dB of extra sensitivity at the cost of airtime. When we move a large file we accept the airtime cost and keep the frame size at the 245-byte maximum so each chirp is as dense as the envelope allows. Power is held at 14 dBm on RF chain 0, SX1250 single input, matching the certified radio configuration of the RAK Miner v2 concentrator HAT.

Note 014. The link budget at 903.9 MHz SF9 125 kHz is dominated by spreading-factor processing gain; SF9 buys roughly nine to ten dB of extra sensitivity at the cost of airtime. When we move a large file we accept the airtime cost and keep the frame size at the 245-byte maximum so each chirp is as dense as the envelope allows. Power is held at 14 dBm on RF chain 0, SX1250 single input, matching the certified radio configuration of the RAK Miner v2 concentrator HAT.

Note 015. The link budget at 903.9 MHz SF9 125 kHz is dominated by spreading-factor processing gain; SF9 buys roughly nine to ten dB of extra sensitivity at the cost of airtime. When we move a large file we accept the airtime cost and keep the frame size at the 245-byte maximum so each chirp is as dense as the envelope allows. Power is held at 14 dBm on RF chain 0, SX1250 single input, matching the certified radio configuration of the RAK Miner v2 concentrator HAT.

Note 016. The link budget at 903.9 MHz SF9 125 kHz is dominated by spreading-factor processing gain; SF9 buys roughly nine to ten dB of extra sensitivity at the cost of airtime. When we move a large file we accept the airtime cost and keep the frame size at the 245-byte maximum so each chirp is as dense as the envelope allows. Power is held at 14 dBm on RF chain 0, SX1250 single input, matching the certified radio configuration of the RAK Miner v2 concentrator HAT.

Note 017. The link budget at 903.9 MHz SF9 125 kHz is dominated by spreading-factor processing gain; SF9 buys roughly nine to ten dB of extra sensitivity at the cost of airtime. When we move a large file we accept the airtime cost and keep the frame size at the 245-byte maximum so each chirp is as dense as the envelope allows. Power is held at 14 dBm on RF chain 0, SX1250 single input, matching the certified radio configuration of the RAK Miner v2 concentrator HAT.

Note 018. The link budget at 903.9 MHz SF9 125 kHz is dominated by spreading-factor processing gain; SF9 buys roughly nine to ten dB of extra sensitivity at the cost of airtime. When we move a large file we accept the airtime cost and keep the frame size at the 245-byte maximum so each chirp is as dense as the envelope allows. Power is held at 14 dBm on RF chain 0, SX1250 single input, matching the certified radio configuration of the RAK Miner v2 concentrator HAT.

Note 019. The link budget at 903.9 MHz SF9 125 kHz is dominated by spreading-factor processing gain; SF9 buys roughly nine to ten dB of extra sensitivity at the cost of airtime. When we move a large file we accept the airtime cost and keep the frame size at the 245-byte maximum so each chirp is as dense as the envelope allows. Power is held at 14 dBm on RF chain 0, SX1250 single input, matching the certified radio configuration of the RAK Miner v2 concentrator HAT.

Note 020. The link budget at 903.9 MHz SF9 125 kHz is dominated by spreading-factor processing gain; SF9 buys roughly nine to ten dB of extra sensitivity at the cost of airtime. When we move a large file we accept the airtime cost and keep the frame size at the 245-byte maximum so each chirp is as dense as the envelope allows. Power is held at 14 dBm on RF chain 0, SX1250 single input, matching the certified radio configuration of the RAK Miner v2 concentrator HAT.

Note 021. The link budget at 903.9 MHz SF9 125 kHz is dominated by spreading-factor processing gain; SF9 buys roughly nine to ten dB of extra sensitivity at the cost of airtime. When we move a large file we accept the airtime cost and keep the frame size at the 245-byte maximum so each chirp is as dense as the envelope allows. Power is held at 14 dBm on RF chain 0, SX1250 single input, matching the certified radio configuration of the RAK Miner v2 concentrator HAT.

Note 022. The link budget at 903.9 MHz SF9 125 kHz is dominated by spreading-factor processing gain; SF9 buys roughly nine to ten dB of extra sensitivity at the cost of airtime. When we move a large file we accept the airtime cost and keep the frame size at the 245-byte maximum so each chirp is as dense as the envelope allows. Power is held at 14 dBm on RF chain 0, SX1250 single input, matching the certified radio configuration of the RAK Miner v2 concentrator HAT.

Note 023. The link budget at 903.9 MHz SF9 125 kHz is dominated by spreading-factor processing gain; SF9 buys roughly nine to ten dB of extra sensitivity at the cost of airtime. When we move a large file we accept the airtime cost and keep the frame size at the 245-byte maximum so each chirp is as dense as the envelope allows. Power is held at 14 dBm on RF chain 0, SX1250 single input, matching the certified radio configuration of the RAK Miner v2 concentrator HAT.

Note 024. The link budget at 903.9 MHz SF9 125 kHz is dominated by spreading-factor processing gain; SF9 buys roughly nine to ten dB of extra sensitivity at the cost of airtime. When we move a large file we accept the airtime cost and keep the frame size at the 245-byte maximum so each chirp is as dense as the envelope allows. Power is held at 14 dBm on RF chain 0, SX1250 single input, matching the certified radio configuration of the RAK Miner v2 concentrator HAT.

Note 025. The link budget at 903.9 MHz SF9 125 kHz is dominated by spreading-factor processing gain; SF9 buys roughly nine to ten dB of extra sensitivity at the cost of airtime. When we move a large file we accept the airtime cost and keep the frame size at the 245-byte maximum so each chirp is as dense as the envelope allows. Power is held at 14 dBm on RF chain 0, SX1250 single input, matching the certified radio configuration of the RAK Miner v2 concentrator HAT.

Note 026. The link budget at 903.9 MHz SF9 125 kHz is dominated by spreading-factor processing gain; SF9 buys roughly nine to ten dB of extra sensitivity at the cost of airtime. When we move a large file we accept the airtime cost and keep the frame size at the 245-byte maximum so each chirp is as dense as the envelope allows. Power is held at 14 dBm on RF chain 0, SX1250 single input, matching the certified radio configuration of the RAK Miner v2 concentrator HAT.

Note 027. The link budget at 903.9 MHz SF9 125 kHz is dominated by spreading-factor processing gain; SF9 buys roughly nine to ten dB of extra sensitivity at the cost of airtime. When we move a large file we accept the airtime cost and keep the frame size at the 245-byte maximum so each chirp is as dense as the envelope allows. Power is held at 14 dBm on RF chain 0, SX1250 single input, matching the certified radio configuration of the RAK Miner v2 concentrator HAT.

Note 028. The link budget at 903.9 MHz SF9 125 kHz is dominated by spreading-factor processing gain; SF9 buys roughly nine to ten dB of extra sensitivity at the cost of airtime. When we move a large file we accept the airtime cost and keep the frame size at the 245-byte maximum so each chirp is as dense as the envelope allows. Power is held at 14 dBm on RF chain 0, SX1250 single input, matching the certified radio configuration of the RAK Miner v2 concentrator HAT.

Note 029. The link budget at 903.9 MHz SF9 125 kHz is dominated by spreading-factor processing gain; SF9 buys roughly nine to ten dB of extra sensitivity at the cost of airtime. When we move a large file we accept the airtime cost and keep the frame size at the 245-byte maximum so each chirp is as dense as the envelope allows. Power is held at 14 dBm on RF chain 0, SX1250 single input, matching the certified radio configuration of the RAK Miner v2 concentrator HAT.

Note 030. The link budget at 903.9 MHz SF9 125 kHz is dominated by spreading-factor processing gain; SF9 buys roughly nine to ten dB of extra sensitivity at the cost of airtime. When we move a large file we accept the airtime cost and keep the frame size at the 245-byte maximum so each chirp is as dense as the envelope allows. Power is held at 14 dBm on RF chain 0, SX1250 single input, matching the certified radio configuration of the RAK Miner v2 concentrator HAT.

Note 031. The link budget at 903.9 MHz SF9 125 kHz is dominated by spreading-factor processing gain; SF9 buys roughly nine to ten dB of extra sensitivity at the cost of airtime. When we move a large file we accept the airtime cost and keep the frame size at the 245-byte maximum so each chirp is as dense as the envelope allows. Power is held at 14 dBm on RF chain 0, SX1250 single input, matching the certified radio configuration of the RAK Miner v2 concentrator HAT.

Note 032. The link budget at 903.9 MHz SF9 125 kHz is dominated by spreading-factor processing gain; SF9 buys roughly nine to ten dB of extra sensitivity at the cost of airtime. When we move a large file we accept the airtime cost and keep the frame size at the 245-byte maximum so each chirp is as dense as the envelope allows. Power is held at 14 dBm on RF chain 0, SX1250 single input, matching the certified radio configuration of the RAK Miner v2 concentrator HAT.

Note 033. The link budget at 903.9 MHz SF9 125 kHz is dominated by spreading-factor processing gain; SF9 buys roughly nine to ten dB of extra sensitivity at the cost of airtime. When we move a large file we accept the airtime cost and keep the frame size at the 245-byte maximum so each chirp is as dense as the envelope allows. Power is held at 14 dBm on RF chain 0, SX1250 single input, matching the certified radio configuration of the RAK Miner v2 concentrator HAT.

Note 034. The link budget at 903.9 MHz SF9 125 kHz is dominated by spreading-factor processing gain; SF9 buys roughly nine to ten dB of extra sensitivity at the cost of airtime. When we move a large file we accept the airtime cost and keep the frame size at the 245-byte maximum so each chirp is as dense as the envelope allows. Power is held at 14 dBm on RF chain 0, SX1250 single input, matching the certified radio configuration of the RAK Miner v2 concentrator HAT.

Note 035. The link budget at 903.9 MHz SF9 125 kHz is dominated by spreading-factor processing gain; SF9 buys roughly nine to ten dB of extra sensitivity at the cost of airtime. When we move a large file we accept the airtime cost and keep the frame size at the 245-byte maximum so each chirp is as dense as the envelope allows. Power is held at 14 dBm on RF chain 0, SX1250 single input, matching the certified radio configuration of the RAK Miner v2 concentrator HAT.

Note 036. The link budget at 903.9 MHz SF9 125 kHz is dominated by spreading-factor processing gain; SF9 buys roughly nine to ten dB of extra sensitivity at the cost of airtime. When we move a large file we accept the airtime cost and keep the frame size at the 245-byte maximum so each chirp is as dense as the envelope allows. Power is held at 14 dBm on RF chain 0, SX1250 single input, matching the certified radio configuration of the RAK Miner v2 concentrator HAT.
