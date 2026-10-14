#!/usr/bin/env python3
"""c-99 interim pairing probe (B die) — machine-parsed, fail-closed.

NOT the full T12 battery: key-41 is FIRST-OF-CLASS (positively assertable), so
the template requires 2 DISTINCT-statement-class controls; only ONE era-matched
distinct-class control payload exists (key-40, c-98, identity-era VK 78352ffa)
— every older local control is canon-era (VK 7bd5683f) and verifies INVALID
under the identity keyset (era-mismatch quarantine class, disclosed in the
PR#58 exit-contract probe). Running the full battery now would QUARANTINE on a
known class; instead this probe executes on real silicon:
  PRIMARY  — c-99 captured key-41 payload vs its dual-bus declare
  TAMPER   — 1-bit identity_hash flip (must flip INVALID)
  CONTROL  — era-matched key-40 (c-98) payload vs ITS dual-bus declare:
             the SAME-ERA control whose absence blocked the c-98 battery
             (B617 blocker b), now proven on silicon.
Exit contract: 0 = all three hold; 5 = primary not VALID; 6 = tamper did not
flip; 7 = era-matched control not VALID; 9 = fail-closed abort. No verdict
beyond these claims is made; settle stays gated on BATTERY_EXIT=0 (full T12),
predicted satisfiable from cycle-100 (two era-matched distinct classes:
key-41 + key-40).
"""
import glob
import hashlib
import json
import os
import subprocess
import sys
import time
import urllib.request

M1 = os.path.expanduser("~/fleet-repos/zk-lora-milestone-1")
REPO = os.path.expanduser("~/fleet-repos/zk-lorawan")
BIN = os.path.join(REPO, "target/debug/zk_lorawan_prove")
EVID = os.path.join(M1, "evidence/groth16_ota_20261014T0009Z_cycle99")
A_BUS = "http://192.168.1.219:8643"
B_BUS = "http://127.0.0.1:8643"


def tok():
    for line in open(os.path.expanduser("~/.hermes/.env")):
        if line.strip().startswith("FLEET_FAST_TOKEN"):
            return line.strip().partition("=")[2].strip().strip('"').strip("'")
    raise SystemExit("FLEET_FAST_TOKEN not found")


def get_events(url, timeout=20):
    req = urllib.request.Request(url + "/events?token=" + tok(), headers={"User-Agent": "c99-probe"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        out = json.loads(r.read())
    return out if isinstance(out, list) else out.get("events", [])


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def main():
    log_lines = []

    def log(s):
        print(s, flush=True)
        log_lines.append(s)

    # ---- machine-locate the cycle-99 window on B's bus (cycle id, never typed seq) ----
    Bev = get_events(B_BUS)
    Aev = get_events(A_BUS)
    wins = [e for e in Bev if e.get("type") == "rx_window_open"
            and str(e.get("data", {}).get("cycle")) == "99"]
    if len(wins) != 1:
        log("ABORT: cycle-99 window events on B-bus: %d (need 1)" % len(wins))
        return 9
    wsid = str(wins[0]["seq"])
    log("WINDOW cycle-99 located: B-bus seq %s armed=%s closes=%s"
        % (wsid, wins[0]["data"]["armed_at_utc"], wins[0]["data"]["closes_at_utc"]))

    d_b = [e for e in Bev if e.get("type") == "groth16_proof_tx"
           and e.get("data", {}).get("window_seq") == wsid]
    d_a = [e for e in Aev if e.get("type") == "groth16_proof_tx"
           and e.get("data", {}).get("window_seq") == wsid]
    if len(d_b) != 1 or len(d_a) != 1:
        log("ABORT: window_seq=%s declares B=%d A=%d (need 1/1)" % (wsid, len(d_b), len(d_a)))
        return 9
    declared = d_b[0]["data"]["proof_sha256"]
    fields = ("public_input_hashes", "gateway_address_hex", "firmware_hash_hex",
              "deposit_value", "private_key_id", "deposit_commitment", "proof_sha256",
              "vk_sha256", "pk_sha256")
    for f in fields:
        if d_a[0]["data"].get(f) != d_b[0]["data"].get(f):
            log("ABORT: declare %s MISMATCH across buses" % f)
            return 9
    log("DECLARE located B seq%d == A seq%d (window_seq join); %d fields byte-equal incl vk/pk_sha256"
        % (d_b[0]["seq"], d_a[0]["seq"], len(fields)))
    d = d_b[0]["data"]

    # ---- fired join (excludes dry-runs: test-window declares have no fired event) ----
    f_hits = [e for e in Bev if e.get("type") == "groth16_tx_fired"
              and e.get("data", {}).get("window_seq") == wsid]
    if len(f_hits) != 1 or f_hits[0]["data"].get("payload_sha256") != declared:
        log("ABORT: fired event missing/inconsistent for window %s" % wsid)
        return 9
    fired_utc = f_hits[0]["data"]["fired_utc"]
    sends = f_hits[0]["data"].get("sends")
    log("FIRED located: B seq%d fired_utc=%s sends=%s" % (f_hits[0]["seq"], fired_utc, sends))

    # ---- era pin: on-disk VK/PK sha MUST equal the declare's vk_sha256/pk_sha256 ----
    vk = sha(os.path.join(REPO, "keys/verifying_key.bin"))
    pk = sha(os.path.join(REPO, "keys/proving_key.bin"))
    bin_sha = sha(BIN)
    log("GUARD binary=%s PK=%s VK=%s" % (bin_sha[:16], pk[:16], vk[:16]))
    if vk != d["vk_sha256"] or pk != d["pk_sha256"]:
        log("ABORT: on-disk keyset era != declare era (VK %s vs %s)" % (vk[:16], d["vk_sha256"][:16]))
        return 9
    log("ERA-PIN GUARD PASS: on-disk keyset == declare keyset (identity-era VK %s)" % vk[:8])

    # ---- payload: machine-read from the fail-closed extract output ----
    ext = json.load(open(os.path.join(EVID, "b_rx_extract_output.json")))
    frames = [p for p in ext["crc_ok"]
              if p["actual_bytes"] == 128 and p["freq_hz"] == 903900000
              and p["sha256"] == declared]
    if len(frames) != 5:
        log("ABORT: expected 5 declared-digest frames in extract, found %d" % len(frames))
        return 9
    payload = bytes.fromhex(frames[0]["hex"].replace(" ", ""))
    if hashlib.sha256(payload).hexdigest() != declared:
        log("ABORT: reconstructed payload digest mismatch")
        return 9
    with open(os.path.join(EVID, "rx_payload_128b.bin"), "wb") as fh:
        fh.write(payload)
    log("PAYLOAD staged rx_payload_128b.bin sha256=%s" % declared)

    env_clean = {k: v for k, v in os.environ.items() if k != "ZK_LORAWAN_REPRODUCIBLE_SETUP"}

    def verify(raw, dd):
        h = raw.hex()
        assert len(h) == 256
        args = [BIN, "verify", h[:64], h[64:192], h[192:256], *dd["public_input_hashes"],
                dd["gateway_address_hex"], str(dd["deposit_value"]), dd["firmware_hash_hex"]]
        t0 = time.time()
        r = subprocess.run(args, cwd=REPO, capture_output=True, text=True, env=env_clean)
        dt = time.time() - t0
        verdict = "VALID" if r.returncode == 0 else ("INVALID" if "INVALID" in r.stdout else "ERROR rc=%d" % r.returncode)
        return verdict, dt, r.returncode, r.stdout.strip()[:100]

    # ---- PRIMARY: captured bytes, identity-era binary + keys ----
    v, dt, rc, so = verify(payload, d)
    log("PRIMARY c-99 captured %s (key-%s): verdict=%s exit=%d wall_s=%.1f stdout=%r"
        % (declared[:8], d["private_key_id"], v, rc, dt, so))

    # ---- TAMPER control: 1-bit flip in the identity-hash public input ----
    pih = list(d["public_input_hashes"])
    flip = bytearray(bytes.fromhex(pih[0]))
    flip[0] ^= 0x01
    td = dict(d)
    td["public_input_hashes"] = [bytes(flip).hex()] + pih[1:]
    tv, tdt, trc, tso = verify(payload, td)
    log("TAMPER 1-bit identity_hash flip: verdict=%s exit=%d wall_s=%.1f stdout=%r"
        % (tv, trc, tdt, tso))

    # ---- ERA-MATCHED CONTROL: newest prior fired declare under the SAME vk_sha256 ----
    # (fired-join excludes dry-run/test-window declares; scan evidence dirs for the
    #  payload bin by machine sha match — the battery's candidate law, era-pinned)
    ctrl = None
    for e in sorted(Bev, key=lambda x: x["seq"], reverse=True):
        dd = e.get("data", {})
        if e.get("type") != "groth16_proof_tx" or e["seq"] >= d_b[0]["seq"]:
            continue
        if dd.get("vk_sha256") != d["vk_sha256"]:
            continue  # era-mismatch quarantine class — never a control across eras
        if not e.get("data", {}).get("window_seq") or dd.get("window_seq") == wsid:
            continue
        csha = dd.get("proof_sha256")
        fired = [f for f in Bev if f.get("type") == "groth16_tx_fired"
                 and f.get("data", {}).get("window_seq") == dd.get("window_seq")
                 and f.get("data", {}).get("payload_sha256") == csha]
        if not fired:
            continue  # dry-run declare (no fired payload) — excluded
        for p in glob.glob(os.path.join(M1, "evidence", "*", "rx_payload_128b.bin")):
            if sha(p) == csha:
                ctrl = (e, p, dd)
                break
        if ctrl:
            break
    if ctrl is None:
        log("ABORT: no era-matched prior fired control payload found on disk")
        return 9
    c_ev, c_path, c_d = ctrl
    # join the A-mirror on window_seq + SHA — NOT SHA alone: Alpha's dry-run
    # declares (window_seq=test-window) share the real burst SHA with no fired
    # payload (B617 blocker a); the window_seq join excludes the phantom.
    c_a = [e for e in Aev if e.get("type") == "groth16_proof_tx"
           and e.get("data", {}).get("window_seq") == c_d.get("window_seq")
           and e.get("data", {}).get("proof_sha256") == c_d["proof_sha256"]]
    if len(c_a) != 1:
        log("ABORT: control declare not unique on A-bus (found %d)" % len(c_a))
        return 9
    for f in fields:
        if c_a[0]["data"].get(f) != c_d.get(f):
            log("ABORT: control declare %s MISMATCH across buses" % f)
            return 9
    cv, cdt, crc, cso = verify(open(c_path, "rb").read(), c_d)
    log("CONTROL era-matched %s (key-%s, declare B seq%d == A seq%d, %s): "
        "verdict=%s exit=%d wall_s=%.1f stdout=%r"
        % (os.path.basename(os.path.dirname(c_path)), c_d["private_key_id"],
           c_ev["seq"], c_a[0]["seq"], c_d["proof_sha256"][:8], cv, crc, cdt, cso))

    # ---- guards after (Codex P2 on PR#65: must rehash the PROVING key too — a
    # PK swap mid-probe must fail-closed exactly like a VK swap; the canonical
    # T12 post-guard checks all three of binary/PK/VK) ----
    if sha(BIN) != bin_sha or sha(os.path.join(REPO, "keys/proving_key.bin")) != pk \
            or sha(os.path.join(REPO, "keys/verifying_key.bin")) != vk:
        log("ABORT: binary/keyset changed mid-probe")
        return 9
    log("GUARD-AFTER unchanged (binary + PK + VK rehashed)")

    # ---- exit contract ----
    if v != "VALID":
        log("PROBE_EXIT=5")
        ec = 5
    elif tv != "INVALID":
        log("PROBE_EXIT=6")
        ec = 6
    elif cv != "VALID":
        log("PROBE_EXIT=7")
        ec = 7
    else:
        log("PROBE VERDICT: PRIMARY VALID + TAMPER INVALID + ERA-MATCHED CONTROL VALID "
            "(key-%s) on B die, identity-era binary+keys, declare dual-bus byte-equal — "
            "capture %s authenticates; B617 blocker (b) closed on silicon; full T12 "
            "satisfiable from cycle-100 (2 era-matched distinct classes)"
            % (d["private_key_id"], declared[:8]))
        log("PROBE_EXIT=0")
        ec = 0
    with open(os.path.join(EVID, "t12_cycle99_interim_probe.log"), "w") as fh:
        fh.write("\n".join(log_lines) + "\n")
    return ec


if __name__ == "__main__":
    sys.exit(main())
