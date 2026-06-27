# Zcash Community Grants Application — ZK-LoRa

## Title
Grant Application - ZK-LoRa: Shielded Micropayments & Privacy Layer

## Terms and Conditions
*(Make sure to check all agreement boxes in the GitHub Issue form)*

## Application Owners
@DannyB-bit

## Project Description

### What is the project?
ZK-LoRa is an offline, privacy-preserving mesh communication layer that combines babyjubjub/secp256k1 elliptic curve cryptography, zk-SNARKs, and Zcash shielded payments. 

In off-grid and physical IoT networks, radio frequency broadcasts are inherently public, exposing device hardware identifiers (UIDs/MACs) to physical triangulation and behavioral tracking. ZK-LoRa allows nodes to verify the legitimacy of packets via local zero-knowledge proofs without exposing device identities. Additionally, to incentivize gateway nodes for routing packets, the protocol integrates Zcash shielded micropayments (ZEC) into the relay loop. Relays receive private, shielded transactions for every packet routed, providing the world's first fully private physical DePIN mesh network.

### How does it benefit the Zcash ecosystem?
1. **Real-World DePIN Utility:** Introduces a functional utility case for Zcash (ZEC) in physical mesh networks and offline IoT setups, expanding the market scope of Zcash shielded pools.
2. **On-Chain Shielded Verification:** Integrates the Rust `zcash_client_backend` into edge nodes (Raspberry Pi/ESP32) and runs light client transaction verification locally, validating Zcash's portability.
3. **ZK Cryptographic Alignment:** Porting and optimizing zk-SNARK verifiers for low-power edge microcontrollers aligns directly with Zcash's mission to advance state-of-the-art privacy-preserving zero-knowledge research.

### Technical Deliverables
*   **zk-SNARK Embedded Verifier:** A compiled and benchmarked Groth16/PLONK verifier optimized to run under 100ms on low-power ARM architectures and browser WASM environments.
*   **Zcash Relay SDK:** A rust backend integration that generates shielded reward payment requests and scans the mempool/ledger for reference key confirmations.
*   **Operator CLI Node:** A cyberpunk-style node CLI (`zymatica_voice_app.py`) automating identity creation, ZK-proof generation, ECIES payload encryption, and ZEC payment triggers.
*   **Compliance:** Fully open-sourced under the MIT License (complying with FPF Grant Agreement Section 4). All code commits follow the `librustzcash` contributing guidelines.

---

## 📅 Goals and Milestones (6-Month Plan)

### 🎯 Milestone 1 (Months 1-2) — $8,500
* **Deliverables:** zk-SNARK embedded library design, microcontroller optimization, and first node assembly.
* **Tasks:** Port Groth16 verifiers to C++ and compile to WASM/native binaries, verifying local proof generation on Raspberry Pi. Stage the first node assembly.
* **Coverage:** Covers initial software development labor, operating lease, utilities, and AI API credits.

### 🎯 Milestone 2 (Months 3-4) — $8,000
* **Deliverables:** Zcash SDK Integration, AI Prior Model training, and remaining 2 Solar Gateways assembly.
* **Tasks:** Integrate `zcash_client_backend` into the LoRa gateway daemon. Procure parts and assemble the remaining 2 solar-powered outdoor gateways.
* **Coverage:** Covers Zcash SDK labor, hardware parts (solar panels, batteries, enclosures, SD cards), assembly labor ($500/node), operating lease, utilities, and AI training credits.

### 🎯 Milestone 3 (Months 5-6) — $8,000
* **Deliverables:** 4-Week Physical Field Testing, Mainnet Release, and Open-Source SDK.
* **Tasks:** Deploy the physical nodes in the field and run 4 weeks of range, obstruction, and over-water RF experiments across 3 test sites (State Park mountainous terrain, Urban site, and Lake Ontario). Deploy ZK-verification program on mainnet and publish the SDK npm package.
* **Coverage:** Covers field testing labor ($800/week), operating lease, utilities, and open-source documentation.

---

## 💰 Thorough Budget Breakdown ($24,500 Total)

The budget covers the development, hardware staging, and location lease costs for the 6-month operation:

### 1. Operating Location & Utilities (3 Months Requested, 3 Months Prefunded) — $4,500
*   **Location Lease:** $3,900 ($1,300/month for the development computer lab and active staging locations).
*   **Utilities:** $600 ($200/month electricity and high-speed network connectivity).
*   *Note:* To demonstrate commitment and maximize funding efficiency, the remaining 3 months of operating lease and utilities are prefunded out-of-pocket by the team.

### 2. AI Model prior training & Dataset credits (3 Months Requested, 3 Months Prefunded) — $1,500
*   **AI API Credits:** $1,500 ($500/month dataset generation and API parsing credits for model prior vocabulary mapping).
*   *Note:* The remaining 3 months of model dataset credits are prefunded out-of-pocket.

### 3. Physical Gateway Hardware Staging (3 Solar Nodes Requested, 2 Prefunded) — $4,440
*   **Hardware Parts:** $2,940 (Procuring parts for 3 devices @ $980 per device including RAK gateways, WisBlock LoRa modules, SD cards, solar panels, battery packs, and weather-proof outdoor enclosures).
*   **Assembly Labor:** $1,500 ($500 per device for physical wiring, mounting, OS flashing, and solar controller assembly).
*   *Note:* The initial 2 physical gateway devices and testing nodes have been prefunded out-of-pocket.

### 4. Labor & Engineering Fees (6 Months) — $14,060
*   **Core ZK Cryptographic Engineering:** $7,000 (140 hours @ $50/hr for embedded Groth16 optimizations and rust verifier compilation).
*   **Field Testing Labor:** $3,200 (4 weeks of active range and RF loop experiments @ $800/week).
*   **Zcash SDK Node Integration:** $3,860 (77.2 hours @ $50/hr for shielded payment construction and mempool verification).

---

## Proof of Work / Previous Credentials
* Main Repository: https://github.com/DannyB-bit/zymatica.space (Folder: `/34_ZK_LoRa_Privacy_Layer/`)
* Core Model (Hugging Face): https://huggingface.co/TheAiCollectiveART/zymatica.space
