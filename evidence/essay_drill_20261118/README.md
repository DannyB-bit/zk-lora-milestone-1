# essay_drill — ZK-LoRaWAN round-trip essay drill (2026-11-16 → 2026-11-19)

**Author: Researcher Bravo — Mobile Agents Fleet, Agent 05 (RakMiner-B)**

Real RF evidence for Dan's ordered drill:

> "now for zk lorawan i want you to write a essay send it and the receiver must confirm what it is
> exactly and then send the sender a summary confirming"

> "you create a essay use zk lorawan send through zk lorawan to b and b needs to send you back the
> exact essay you wrote with a confirmation it's what he received; log all evidence; goal: prove we
> can pack a lot of data into zk-lorawan"

**RESULT: COMPLETE — both legs over real RF, both payloads SHA exact-match, cross-confirmed by
Alpha (FINAL verdict `A1510`, `ok=true`).**

**26,963 bytes of sealed payload carried over 903.9 MHz SF9/BW125 in 151 x 245-byte LoRa frames.**
Union across all rounds: **151/151 unique frames, 151/151 `DECRYPT_OK`, 0 CRC failures among
declared frames, 0 unknown frames.**

---

## Final result (Alpha's FINAL verdict A1510)

| Payload | Frames | Bytes | SHA-256 | Match |
|---------|--------|-------|---------|-------|
| `echo_alpha_essay` (Alpha's essay, returned to him) | **136/136** | 24,322 | `1aaa4e16…50854` | **EXACT** |
| `bravo_essay_md` (Bravo's own essay.md) | **15/15** | 2,641 | `b9912688…460a6` | **EXACT** |

Every captured frame: HAL `status 0x10` (**CRC OK**), `freq_hz 903900000`, SF9/BW125, and
**AES-256-GCM `DECRYPT_OK`** under Alpha's X25519 secret key.

## Leg 1 — A → B (Alpha TX / Bravo RX)

Alpha re-fired his sealed frames **2026-11-19 04:41:24Z → 05:00:13Z** (136/136
`A_LORA_TX_FILE_SEND_COMPLETE=YES`, 0 failures). Bravo's standby RX listener was already hot — the
frames landed in the HAL log with **no agent action required**.

- **136/136** of Alpha's **declared** frame-SHA list (`A4409`) present in Bravo's RX log, byte-exact
- Every frame: `status 0x10` (CRC OK), SF9/BW125, SNR +10.5…+11.5 dB
- Every frame: **AES-256-GCM `DECRYPT_OK`** under Bravo's X25519 secret key
- Reassembled **24,322 B**, `sha256 = 1aaa4e16ff1d1e5102a7895b8e2a4bf8c567031949a4fd9572a35109f3250854`
  — **exact match** to Alpha's declared SHA
- Verdict posted to both buses: **B seq 4492 / A seq 1479**

### Disclosure — 7 ambient frames

Bravo's RX log also contains **7 additional 245-byte frames not in Alpha's declared list**: they
arrived on **904.3 / 904.5 MHz** with HAL `status 0x11` (**CRC FAIL**) at SNR −8.5…−12.0 dB. They are
**not** decryptable with Bravo's key (7 × `DECRYPT_FAIL`), are excluded from reassembly, and are
**disclosed with their full SHA list rather than hidden**.

## Leg 2 — B → A (Bravo TX / Alpha RX) — four rounds, three failures, all mine

**Rounds 1 and 2 failed, and the failure was mine, not Alpha's.** Alpha opened both windows and
issued a valid fire-go each time:

| Round | Alpha window | Bravo action | Outcome |
|-------|--------------|--------------|---------|
| 1 | armed `08:06:58Z` (A1481/A1482) | **none — 0 airtime** | MISSED 0/151 (A1488/B4509) |
| 2 | armed `09:18:24Z` (A1485/A1487) | **none — 0 airtime** | MISSED 0/151 |
| 3 | armed `2026-11-19T21:24:38Z` (A1489/A1490) | 151/151 TX_DONE | **PARTIAL 71/151** (A1496/B4619) |
| 4 | armed `22:55:13Z` (A1498/A1500) | 80 missing frames re-fired | 75/80 captured |
| 5 | (A1500/B4627) | 80 re-fired **by the watcher, no agent turn** | 79/80 captured |
| 6 | armed `23:39:34Z` (A1505/A1507) | 80 re-fired **by the watcher** | idx 14 captured → **COMPLETE** |

**Root cause of rounds 1–2:** Bravo's agent turn was parked waiting on an unrelated peer-run reply
and never executed the transmit. Alpha's receiver was correct and working the whole time; it
reported `MISSED 0/151` honestly (`ok=false`) rather than inventing a capture.

**Root cause of round 3's 50% loss — a diagnosed parameter error, not an RF link problem.** Every
frame that *did* arrive was CRC-OK `0x10` **and** `DECRYPT_OK` — **zero corrupted frames among
mine** — while the missing set alternated perfectly (essay.md captured 0,2,4,6,8 / missed
1,3,5,7,9-14). Corrupted-on-arrival is what a bad link looks like; perfect frames with a 50%
arrival rate is what a receiver **not getting enough dead time** looks like. A 245 B payload at
SF9/BW125 occupies **~2.05 s of airtime**; round 3 used a **1 s gap**, so Alpha's concentrator
could not re-arm between frames.

**The fix — gap 1 s → 3 s, reps 1 → 2** — is what closed the drill. Rounds 4–6 with the widened gap
captured 75/80, then 79/80, then the final frame.

### Structural fix — the LLM is no longer in the transmit path

`essay_b2a_hotfire.py` + systemd unit `essay-b2a-hotfire.service` (`Restart=always`, enabled): a
watcher polls the bus and fires the staged bursts **the instant** a declared window + fire-go
appears, with **no agent turn involved**. It fired rounds 5 and 6 autonomously.

Fail-closed rails (**30/30 logic tests pass, no airtime in the tests**):
- fires only inside a declared `essay_drill` window; **never** outside one
- refuses expired / near-close windows, `manual_fire_only` windows, and non-essay drills
- refuses a window with no usable machine close time
- never fires twice for the same window sequence (persisted fired-window ledger)
- honours Alpha's own `fire_go` frame spec when he names an exact frame
- pre-fire SHA gate: every frame must be exactly 245 B and match its manifest SHA

## Canonical envelope (unchanged, reused from `chirp245.py` PR #12)

```
frame (245 B) = [ver=1][n=1][nonce=12][eph_x25519_pub=32][AES-256-GCM ct=183 || tag=16]
key           = HKDF-SHA256(X25519(eph_sk, recipient_pub),
                            salt=b"zk-lora-chirp245-v1", info=b"chirp245-aead-key", len=32)
plaintext     = 0x02 || total_chunks || idx || chunk(<=180 B)   # RAW mode, byte-exact reassembly
```

Tools: `solana-cuneiform-milestone1/tools/chirp_raw_tx.py @ e19dd98` (seal), `chirp_raw_rx.py`
(decrypt/reassemble), `chirp_frames_tx` (multi-frame TX, **one** `lgw_start` for N frames).

## Bugs found and fixed in Bravo's own tooling (disclosed)

1. **HAL RX parser** — `rf_chain  0` has no colon; the block-terminating branch ended every packet
   early, yielding 0 parsed frames. Fixed with a colon-optional field regex.
2. **Decrypt tool** — `X25519PublicKey` was not imported → `NameError` on all 143 frames. Fixed.
3. **Hot-fire watcher (close time)** — Alpha's `rx_window_open` uses `closes_utc` (not
   `closes_at_utc`) and the round-3 event carried a **1-day date skew**, so no live close time could
   be computed. Fixed to accept every close-field name and to rebuild the close from
   `armed_utc + window_s` when the declared stamp is unusable.
4. **Hot-fire watcher (split batch)** — Alpha's window and fire-go arrive **~1 s apart**, so a 2 s
   poll split them into two batches; scanning only the current batch meant the fire never
   triggered. Fixed with a rolling event buffer + a fired-window ledger.
5. **Hot-fire watcher (content dedupe)** — staging a frame named by a sha256 prefix must dedupe by
   **content**, not by path (the same frame legitimately lives in two staged dirs).
6. **Fire script receipt** — the re-fire manifest schema lacks `file`/`file_bytes`/`file_sha256` →
   `KeyError` killed the receipt step. Fixed to be schema-tolerant.
7. **systemd `ExecStart`** — inline token export with mixed quotes → `INVALIDARGUMENT` restart
   loop. Fixed via a wrapper script.

## Verification battery (all green, run in the PR worktree)

- `python3 -m py_compile` on all Python tools — PASS
- `bash -n` on both shell scripts — PASS
- Hot-fire logic tests — **30/30 PASS** (including the split-batch and frame-spec regressions)
- Staged SHA gate — 136/136 + 15/15 + 80/80 + 1/1 OK
- Captured frames on disk — 143 unique 245 B frames (A→B leg)
- `sha256sum essay_a2b.md` — `1aaa4e16…50854` (matches Alpha's declaration)
- TX logs — `CHIRP_TX_COMPLETE=YES` on every burst; `STATUS=TX_DONE` 136 + 15 + 160 + 160 + 160
- Dossier integrity — `final_ok: true`, union 151/151 `decrypt_ok`

## Bundle contents

```
EVIDENCE_DOSSIER.json            machine-assembled dossier (every number read from a file)
essay_a2b.md                     the 24,322 B reassembled essay (sha 1aaa4e16…50854)
essay_a2b.md.decrypt_report.json per-frame decrypt verdict for all 143 captured frames
a2b_frames/capture_inventory.json RX log parse: 151 packets, 143 unique 245B frames
a2b_frames/frame_<sha16>.bin     the 143 captured 245B frames, content-addressed
echo_a2b_frames/                 136 sealed echo frames + manifest (Alpha's exact essay)
my_essay_frames/                 15 sealed frames of Bravo's essay.md + manifest
refire_missing_frames/           the 80 targeted re-fire frames + manifest (Alpha's missing list)
refire_single_idx14/             the single idx-14 frame + manifest
b2a_tx_r3echo.log                raw HAL TX log — burst 1 of round 3
b2a_tx_r3mine.log                raw HAL TX log — burst 2 of round 3
b2a_tx_r4refire.log              raw HAL TX log — round 4 targeted re-fire (80 frames)
b2a_tx_r4627.log                 raw HAL TX log — round 5 (fired by the watcher)
b2a_tx_r4633.log                 raw HAL TX log — round 6 (fired by the watcher)
recovery_r3*.log / recovery_r4*.log  post-TX chain re-certification per burst
chirp_raw_rx_verdict_post.json   bus post + readback for the A→B verdict
chirp_raw_tx_fired_*.json         bus post + readback for every TX receipt
essay_b2a_tx_ready_post.json      bus post + readback for the B→A manifest brief
essay_capture_extract.py         HAL RX log → 245B frame extractor
essay_decrypt_reassemble.py      canonical AEAD decrypt + RAW reassembly + SHA verify
build_refire_set.py              stage ONLY Alpha's missing frames, sha-verified
essay_b2a_fire.sh                fail-closed fire: SHA gate → free SPI → TX → re-certify → re-arm → receipt
essay_b2a_hotfire.py             hot-path auto-fire watcher (no LLM in the TX path)
essay_b2a_hotfire.sh             systemd wrapper (loads the fleet token)
test_essay_b2a_hotfire.py        window/fire-go/frame-spec logic tests (no airtime)
hotfire_logic_test.json          30/30 PASS
staged_sha_gate.py               pre-fire fail-closed frame verification
essay-b2a-hotfire.service        systemd unit (enabled, Restart=always)
```

## Post-closure disclosures

- **Schema-probe event (B4641 / A1511).** After the drill had already closed, the *patched*
  receipt code path was verified end-to-end against a re-fire manifest. The bus exposes **no
  DELETE (HTTP 501)**, so that probe event is permanent. An explicit **retraction** was posted on
  both buses at **B4642 / A1512**, naming the authoritative result (Alpha **A1510**, `ok=true`)
  and listing the five real TX receipts, so no downstream reader can mistake the probe for a
  verdict. Disclosed rather than left ambiguous.
- **Duplicate re-fire receipt.** `B4630/A1503` and `B4631/A1504` both describe the same
  80-frame gap-3 s / reps-2 burst: one was posted by the fire script, the other by the manual
  post that replaced the receipt the script's `KeyError` had killed. Duplicate, not contradictory.

Signed-off-by: Researcher Bravo <jae@solananft.art>
