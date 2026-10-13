#!/usr/bin/env python3
"""T12 PAIRING BATTERY TEMPLATE — parameterized, zero hand-typed constants.

Closes the c-38 review nit (PR#24, Agent-02 2026-10-07): the cycle-38 battery
log header carried a template leftover (`T12_CYCLE37_BATTERY_RUN_UTC`) because
the label was a TYPED LITERAL in a per-cycle copy of the script. Hand-typed-
constant law, instance class: any typed label is one copy-paste away from
being wrong. Fix: the label is DERIVED from the same --cycle argument that
machine-locates the bus window event, so the label and the evidence cannot
disagree; a mismatch aborts before any pairing runs.

Per-cycle invocation (after capture extraction lands in the evidence dir):

  python3 tools/t12_battery_template.py --cycle 39 \
      --evidence-dir evidence/groth16_ota_<stamp>_cycle39 \
      [--guard-log ~/fleet/logs/rx_standby_continuous_<...>.log]

Machine-derived, never typed:
  * label + window    : rx_window_open with window_seq_bravo_bus == cycle-<N>
  * declare           : groth16_proof_tx linked by window seq (B) + SHA (A)
  * controls          : scanned from prior evidence dirs, class-selected by
                        machine-parsed STATEMENT class = (private_key_id,
                        public_input_hashes), newest-declare-first, provenance
                        logged. FIRST-OF-CLASS requires a POSITIVE assertion
                        (zero prior declares of this statement class across
                        COMPLETE dual-bus history; get_events aborts on any
                        incomplete fetch) — absence of local evidence is
                        never first-of-class. First-of-class runs verify 2
                        DISTINCT-statement-class controls; a same-key
                        different-statement control, when its payload is
                        locally verifiable, is added as a bonus regression.
                        NOT-first-of-class runs require a same-class control
                        payload on disk (vendor it or abort) + 1 different.
  * payload SHA       : from the declare, never typed
Fail-closed gates (abort = no verdict, by battery law):
  * A-bus unreachable  -> NO verdict may issue; cross-bus byte-diff is mandatory
  * window not found / not unique -> abort
  * control classes not satisfiable -> abort with the scan list
  * burst != 5 digest-equal frames in the listener session segment -> abort
  * wrap-branch discriminator must pass EXACTLY one of {+0s, +4294.967296s}
  * binary/PK/VK sha guards must hold before AND after the pairing runs
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timedelta, timezone

M1 = os.path.expanduser("~/fleet-repos/zk-lora-milestone-1")
REPO = os.path.expanduser("~/fleet-repos/zk-lorawan")
BIN = os.path.join(REPO, "target/debug/zk_lorawan_prove")
DEFAULT_GUARD = os.path.expanduser("~/fleet/logs/rx_standby_continuous_20261003T180951Z.log")

B_BUS = "http://192.168.1.220:8643"
A_BUS = "http://192.168.1.219:8643"
WRAP_S = 4294.967296

VERIFY_FIELDS = ("public_input_hashes", "gateway_address_hex", "firmware_hash_hex",
                 "deposit_value", "private_key_id", "deposit_commitment", "proof_sha256")


def tok():
    for line in open(os.path.expanduser("~/.hermes/.env")):
        if line.strip().startswith("FLEET_FAST_TOKEN"):
            return line.strip().partition("=")[2].strip().strip('"').strip("'")
    raise SystemExit("FLEET_FAST_TOKEN not found")


def get_events(url, timeout=15):
    # Codex P1 remediation (PR#48, 2026-10-11): every class assertion below rests on
    # COMPLETE bus history. The fetch must return exactly /health's event count or
    # no assertion may issue from it (fail-closed; no partial-scan inferences).
    req = urllib.request.Request(f"{url}/events?since=0&token={tok()}",
                                 headers={"User-Agent": "fleet-b"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        d = json.load(r)
    evs = d.get("events", d) if isinstance(d, dict) else d
    hreq = urllib.request.Request(f"{url}/health", headers={"User-Agent": "fleet-b"})
    with urllib.request.urlopen(hreq, timeout=timeout) as r:
        h = json.load(r)
    total = h.get("events") if isinstance(h, dict) else None
    if total is None or len(evs) != total:
        raise SystemExit(f"ABORT: bus {url} incomplete fetch: got {len(evs)} of {total} "
                         f"events — class assertions unavailable; no verdict")
    return evs


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def telemetry():
    out = []
    for cmd in (["vcgencmd", "measure_temp"], ["vcgencmd", "get_throttled"]):
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            if r.returncode == 0:
                out.append(f"{cmd[1]}={r.stdout.strip()}")
        except Exception:
            pass
    return " ".join(out)


def main():
    ap = argparse.ArgumentParser(description=((__doc__ or "") + "\n").splitlines()[0])
    ap.add_argument("--cycle", type=int, required=True, help="cycle number N (locates window + label)")
    ap.add_argument("--evidence-dir", required=True, help="per-cycle evidence dir (relative to repo root or absolute)")
    ap.add_argument("--guard-log", default=DEFAULT_GUARD, help="RX guard log with arm banners")
    ap.add_argument("--bus-timeout", type=int, default=15, help="per-bus HTTP timeout (s)")
    args = ap.parse_args()

    cycle = args.cycle
    evid = args.evidence_dir if os.path.isabs(args.evidence_dir) else os.path.join(M1, args.evidence_dir)
    if not os.path.isdir(evid):
        raise SystemExit(f"ABORT: evidence dir not found: {evid}")
    extract = os.path.join(evid, "b_rx_extract_output.json")
    if not os.path.isfile(extract):
        raise SystemExit(f"ABORT: extraction output missing (run b_rx_extract first): {extract}")
    log_path = os.path.join(evid, f"t12_cycle{cycle}_battery.log")

    lines = []
    label = f"T12_CYCLE{cycle}_BATTERY_RUN_UTC"  # DERIVED from the arg that locates the window
    lines.append(f"{label}={time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}")
    lines.append(f"invocation: {' '.join(sys.argv)}")
    lines.append("mode: primary = machine-located captured burst; controls machine-selected by "
                 "statement class (same + different), newest-first from prior evidence")
    lines.append("law: zero hand-typed constants (label derived from --cycle that locates the window); "
                 "burst binding v4 = session-segment + digest-equality; wrap branch machine-selected")
    lines.append(f"SILICON {telemetry()}")

    bin_sha = sha(BIN)
    pk_sha = sha(os.path.join(REPO, "keys/proving_key.bin"))
    vk_sha = sha(os.path.join(REPO, "keys/verifying_key.bin"))
    lines.append(f"GUARD-BEFORE binary={bin_sha[:16]} PK={pk_sha[:16]} VK={vk_sha[:16]}")
    env_clean = {k: v for k, v in os.environ.items() if k != "ZK_LORAWAN_REPRODUCIBLE_SETUP"}

    # ---- machine-locate the cycle window on B's bus (label and window share ONE variable) ----
    try:
        Bev = get_events(B_BUS, timeout=args.bus_timeout)
    except Exception as ex:
        raise SystemExit(f"ABORT: B-bus unreachable ({ex}) — no window location, no verdict")
    def _cyc(e):
        c = e.get("data", {}).get("cycle")
        return c is not None and str(c) == str(cycle)
    wins = [e for e in Bev if e.get("type") == "rx_window_open"
            and (e.get("data", {}).get("window_seq_bravo_bus") == f"cycle-{cycle}"
                 or _cyc(e))]
    # cycle 69+ events carry kind=cycleNN_window_open + cycle=<int-or-str>; legacy events carry
    # window_seq_bravo_bus=cycle-<N>. Both are machine-locators derived from --cycle (no typed constants).
    # str()-normalization only (never int-cast: literal preservation).
    if len(wins) != 1:
        raise SystemExit(f"ABORT: cycle-{cycle} window events on B-bus: {len(wins)} (need exactly 1)")
    win = wins[0]
    wsid = str(win["seq"])
    lines.append(f"WINDOW cycle-{cycle} located: B-bus seq {wsid} armed={win['data']['armed_at_utc']} "
                 f"closes={win['data']['closes_at_utc']} — label {label} derived from THIS event's cycle id")

    # ---- A-bus gate: cross-bus byte-diff is mandatory for any verdict (battery law) ----
    try:
        Aev = get_events(A_BUS, timeout=args.bus_timeout)
    except Exception as ex:
        print("\n".join(lines))
        raise SystemExit(f"ABORT: A-bus unreachable ({ex}) — cross-bus declare byte-diff UNAVAILABLE; "
                         f"NO VERDICT MAY ISSUE. Re-run when the twin box is live. "
                         f"(Fail-closed by design; there is no --allow-dark override.)")

    # ---- primary declare: linked by window seq on B, by SHA on A; all fields byte-equal ----
    d_b_hits = [e for e in Bev if e.get("type") == "groth16_proof_tx"
                and e.get("data", {}).get("window_seq") == wsid]
    if len(d_b_hits) != 1:
        raise SystemExit(f"ABORT: cycle-{cycle} declares on B-bus: {len(d_b_hits)} (need exactly 1)")
    d_b = d_b_hits[0]
    declared = d_b["data"]["proof_sha256"]
    d_a_hits = [e for e in Aev if e.get("type") == "groth16_proof_tx"
                and e.get("data", {}).get("proof_sha256") == declared]
    if len(d_a_hits) != 1:
        raise SystemExit(f"ABORT: cycle-{cycle} declare mirrors on A-bus: {len(d_a_hits)} (need exactly 1)")
    d_a = d_a_hits[0]
    for field in VERIFY_FIELDS:
        if field not in d_a["data"] or field not in d_b["data"]:
            raise SystemExit(f"ABORT: declare missing verification field {field}")
        if d_a["data"][field] != d_b["data"][field]:
            raise SystemExit(f"ABORT: declare {field} MISMATCH across buses")
    lines.append("DECLARE cross-bus byte-diff: " + ", ".join(f"{f}=EQ" for f in VERIFY_FIELDS))
    f_hits = [e for e in Bev if e.get("type") == "groth16_tx_fired"
              and e.get("data", {}).get("window_seq") == wsid]
    if len(f_hits) != 1:
        raise SystemExit(f"ABORT: cycle-{cycle} fired events on B-bus: {len(f_hits)} (need exactly 1)")
    f_ev = f_hits[0]
    if declared != f_ev["data"]["payload_sha256"]:
        raise SystemExit("ABORT: declare/fired sha inconsistent")
    lines.append(f"DECLARE located: A seq{d_a['seq']} == B seq{d_b['seq']}; "
                 f"key={d_b['data']['private_key_id']} deposit={d_b['data']['deposit_value']} "
                 f"source={d_b['data'].get('source', '?')} construction={d_b['data'].get('construction', '?')}")

    armed = datetime.strptime(win["data"]["armed_at_utc"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    closes = datetime.strptime(win["data"]["closes_at_utc"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    fired_utc = datetime.strptime(f_ev["data"]["fired_utc"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    lines.append(f"WINDOW armed={armed.isoformat()} closes={closes.isoformat()} "
                 f"fired_utc={fired_utc.isoformat()} (completion stamp)")

    # ---- session segment from the guard log (banner keyed to the window's armed_at_utc) ----
    glines = open(args.guard_log, errors="replace").read().splitlines()
    arm_banner = None
    for i, l in enumerate(glines):
        if "GATE PASS: ARMING listener window" in l and l.split(" ")[0] == win["data"]["armed_at_utc"]:
            arm_banner = i
            break
    if arm_banner is None:
        raise SystemExit("ABORT: no arm banner matches the window armed_at_utc")
    exits = [i for i, l in enumerate(glines) if "listener exit rc=124" in l and i > arm_banner]
    seg_hi = exits[0] if exits else len(glines)
    seg_txt = "\n".join(glines[arm_banner:seg_hi])
    origin = armed
    lines.append(f"SESSION-SEGMENT arm banner line {arm_banner} (guard log lines {arm_banner}..{seg_hi}); "
                 f"count_us origin = banner second {origin.isoformat()} (banner-second convention; "
                 f"the SHA gate does not depend on walls)")

    # ---- burst selection: in-segment + 128B + 903.9MHz + digest equality ----
    ext = json.load(open(extract))
    in_session = [p for p in ext["crc_ok"] if f"count_us: {p['count_us']}" in seg_txt]
    burst = [p for p in in_session
             if p["actual_bytes"] == 128 and p["freq_hz"] == 903900000
             and p["sha256"] == declared]
    if len(burst) != 5:
        raise SystemExit(f"ABORT: expected 5 declared-digest frames in session, found {len(burst)}")
    if {p["sha256"] for p in burst} != {declared}:
        raise SystemExit("ABORT: burst digests not uniform")
    payload = bytes.fromhex(burst[0]["hex"].replace(" ", ""))
    if hashlib.sha256(payload).hexdigest() != declared or len(payload) != 128:
        raise SystemExit("ABORT: reconstructed payload fails digest/length")
    ordered = sorted(burst, key=lambda p: p["count_us"])
    gaps = [(ordered[i + 1]["count_us"] - ordered[i]["count_us"]) / 1e6 for i in range(4)]
    if not all(10 <= g <= 20 for g in gaps):
        raise SystemExit(f"ABORT: inter-frame implausible: {gaps}")
    with open(os.path.join(evid, "rx_payload_128b.bin"), "wb") as fh:
        fh.write(payload)

    # ---- wrap-branch machine selection (walls are REPORTING-only; SHA gate is the binding) ----
    passing = []
    for add in (0.0, WRAP_S):
        walls = [origin + timedelta(seconds=p["count_us"] / 1e6 + add) for p in ordered]
        in_win = all(armed - timedelta(seconds=30) <= w <= closes + timedelta(seconds=30) for w in walls)
        span = (fired_utc - walls[-1]).total_seconds()
        if in_win and -180 <= span <= 240:
            passing.append((add, walls, span))
    if len(passing) != 1:
        raise SystemExit(f"ABORT: wrap-branch discriminator: {len(passing)} branches pass (need exactly 1)")
    add, walls, span = passing[0]
    wrap_note = "POST-WRAP (+4294.967296s)" if add else "pre-wrap (+0s)"
    lines.append(f"BURST: 5 frames, count_us {ordered[0]['count_us']}..{ordered[-1]['count_us']}, "
                 f"inter_frame_s={[round(g, 1) for g in gaps]}, SNR {ordered[0]['snr_avg']}, "
                 f"status {ordered[0]['status']}")
    lines.append(f"SHA GATE: digest(captured)==declare 64/64: {declared}")

    # ---- verify ----
    def verify(raw, d):
        h = raw.hex()
        assert len(h) == 256, "payload not 128B"
        v_args = [BIN, "verify", h[:64], h[64:192], h[192:256], *d["public_input_hashes"],
                  d["gateway_address_hex"], str(d["deposit_value"]), d["firmware_hash_hex"]]
        t0 = time.time()
        r = subprocess.run(v_args, cwd=REPO, capture_output=True, text=True, env=env_clean)
        dt = time.time() - t0
        verdict = "VALID" if r.returncode == 0 else ("INVALID" if "INVALID" in r.stdout else f"ERROR rc={r.returncode}")
        return verdict, dt, r.returncode, r.stdout.strip()[:80]

    v, dt, rc, so = verify(payload, d_b["data"])
    lines.append(f"PRIMARY cycle-{cycle} captured {declared[:8]}: verdict={v} exit={rc} wall_s={dt:.1f} stdout={so!r}")

    # ---- controls: statement-class = (private_key_id, public_input_hashes) ----
    # Codex P1 remediation (PR#48, 2026-10-11). Three defects closed:
    #   (1) "first-of-class" was INFERRED from absence in a partial local scan; now it
    #       requires a POSITIVE assertion — zero prior declares of this statement class
    #       over COMPLETE dual-bus history (get_events aborts on any incomplete fetch).
    #   (2) class is the full statement class (key id AND public-input vector, per the
    #       cycle-20 battery law), not key-id alone — "first key-33" and "first of the
    #       (key-33, pih) statement" are different claims and are logged distinctly.
    #   (3) a NOT-first-of-class primary with no locally verifiable same-class control
    #       payload ABORTS (fetch/vendor it); the run is never silently relabeled.
    # Candidate ordering is by the bus DECLARE TIMESTAMP (newest first) — dir-name
    # lexicographic order was a Codex P2 defect (a mis-stamped dir reorders the scan).
    primary_key = d_b["data"]["private_key_id"]

    def declare_class(dd):
        return (str(dd.get("private_key_id")), json.dumps(dd.get("public_input_hashes"), sort_keys=True))

    primary_class = declare_class(d_b["data"])
    primary_pih = json.dumps(d_b["data"].get("public_input_hashes"), sort_keys=True)
    prior_b = [e for e in Bev if e.get("type") == "groth16_proof_tx"
               and declare_class(e.get("data", {})) == primary_class
               and e["seq"] != d_b["seq"]]
    prior_a = [e for e in Aev if e.get("type") == "groth16_proof_tx"
               and declare_class(e.get("data", {})) == primary_class
               and e["seq"] != d_a["seq"]]
    unclassed = sum(1 for bus in (Bev, Aev) for e in bus
                    if e.get("type") == "groth16_proof_tx"
                    and (e.get("data", {}).get("private_key_id") is None
                         or e.get("data", {}).get("public_input_hashes") is None))
    # pih-only prior guard: an UNCLASSED prior declare (missing key id) whose public-
    # input vector equals the primary's is treated as a prior of the same statement
    # (same pih => same identity hash => same key in practice). Absence of a legible
    # key id on a prior must BLOCK the first-of-class claim, not enable it.
    prior_pih_b = [e for e in Bev if e.get("type") == "groth16_proof_tx"
                   and e["seq"] != d_b["seq"]
                   and json.dumps(e.get("data", {}).get("public_input_hashes"), sort_keys=True) == primary_pih]
    prior_pih_a = [e for e in Aev if e.get("type") == "groth16_proof_tx"
                   and e["seq"] != d_a["seq"]
                   and json.dumps(e.get("data", {}).get("public_input_hashes"), sort_keys=True) == primary_pih]
    first_of_class = not prior_b and not prior_a and not prior_pih_b and not prior_pih_a
    lines.append(f"CLASS SCAN (complete dual-bus history): statement-class key-{primary_key} "
                 f"pih[-1]={primary_class[1][-18:-2]} prior-declares B={len(prior_b)} A={len(prior_a)} "
                 f"pih-only-priors B={len(prior_pih_b)} A={len(prior_pih_a)} "
                 f"unclassable-declares={unclassed} -> "
                 + ("FIRST-OF-CLASS (positively asserted)" if first_of_class
                    else f"NOT first-of-class (priors: B{[e['seq'] for e in prior_b]} A{[e['seq'] for e in prior_a]}"
                         f" pih-only B{[e['seq'] for e in prior_pih_b]} A{[e['seq'] for e in prior_pih_a]})"))

    cands, skipped = [], 0
    for d in os.listdir(os.path.join(M1, "evidence")):
        if not d.startswith("groth16_ota_") or f"cycle{cycle}" in d:
            continue
        p = os.path.join(M1, "evidence", d, "rx_payload_128b.bin")
        if not os.path.isfile(p):
            continue
        s = sha(p)
        hits = [e for e in Bev if e.get("type") == "groth16_proof_tx"
                and e.get("data", {}).get("proof_sha256") == s]
        a_hits = [e for e in Aev if e.get("type") == "groth16_proof_tx"
                  and e.get("data", {}).get("proof_sha256") == s]
        if len(hits) != 1 or len(a_hits) != 1 or hits[0]["data"].get("private_key_id") is None:
            skipped += 1
            continue
        if any(hits[0]["data"].get(f) != a_hits[0]["data"].get(f) for f in VERIFY_FIELDS):
            skipped += 1  # cross-bus declare mismatch: unusable as a control, logged below
            continue
        cands.append((hits[0]["ts_utc"], d, s, str(hits[0]["data"]["private_key_id"]),
                      hits[0]["data"], a_hits[0]["data"]))
    cands.sort(key=lambda t: t[0], reverse=True)  # newest declare first
    lines.append(f"CONTROL CANDIDATES (newest declare first, {len(cands)} usable / {skipped} skipped): "
                 + "; ".join(f"{d} key-{k} @{ts}" for ts, d, s, k, _, _ in cands))

    same_c, diff_list, seen_cls = None, [], set()
    for ts, d, s, k, db, da in cands:
        cls = declare_class(db)
        if cls == primary_class and same_c is None:
            same_c = (d, s, k, db, da)
        elif cls != primary_class and cls not in seen_cls:
            seen_cls.add(cls)
            diff_list.append((d, s, k, db, da))
        if same_c is not None and len(diff_list) >= 2:
            break

    if first_of_class:
        # Same-statement-class control cannot exist (positively asserted above).
        if len(diff_list) < 2:
            raise SystemExit(f"ABORT: control classes not satisfiable (first-of-class key-{primary_key}: "
                             f"need 2 distinct-statement-class controls, found {len(diff_list)}); "
                             f"candidates: {', '.join(t[1] for t in cands) or '(none)'}")
        picked = {"diff1": diff_list[0], "diff2": diff_list[1]}
        lines.append(f"CONTROL MODE: FIRST-OF-CLASS (positive assertion) key-{primary_key} — "
                     f"2 DISTINCT-statement-class controls (keys "
                     + ", ".join(f"key-{t[2]}" for t in (diff_list[0], diff_list[1])) + ")")
        # Regression bonus (not required by the battery law): if a SAME-KEY,
        # different-statement payload exists locally, verify it too — it exercises
        # the primary's proving-key compute path in this same session.
        for ts, d, s, k, db, da in cands:
            if k == str(primary_key) and declare_class(db) != primary_class:
                picked["samekey"] = (d, s, k, db, da)
                lines.append(f"CONTROL MODE: + optional SAME-KEY different-statement control {d} "
                             f"({s[:8]}) — regression on the key-{primary_key} path")
                break
    else:
        if same_c is None:
            raise SystemExit(
                f"ABORT: NOT first-of-class (prior same-statement-class declares exist: "
                f"B={[e['seq'] for e in prior_b]} A={[e['seq'] for e in prior_a]}) but no local "
                f"same-class control payload is verifiable — vendor the prior same-class payload "
                f"(see its declare for the sha) and re-run; refusing to relabel as first-of-class "
                f"(Codex P1: absence-of-evidence is not first-of-class)")
        if not diff_list:
            raise SystemExit(f"ABORT: no different-statement-class control available; "
                             f"candidates: {', '.join(t[1] for t in cands) or '(none)'}")
        picked = {"same": same_c, "diff": diff_list[0]}
        lines.append(f"CONTROL MODE: NORMAL — same-statement-class {same_c[0]} + "
                     f"different-class {diff_list[0][0]}")

    verdicts = {}
    for role, (d, s, k, db, da) in picked.items():
        for field in VERIFY_FIELDS:
            if db[field] != da[field]:
                raise SystemExit(f"ABORT: control {d} declare {field} MISMATCH across buses")
        cv, cdt, crc, cso = verify(open(os.path.join(M1, "evidence", d, "rx_payload_128b.bin"), "rb").read(), db)
        verdicts[role] = cv
        if declare_class(db) == primary_class:
            rel = "SAME statement-class"
        elif k == str(primary_key):
            rel = "SAME key, DIFFERENT statement"
        else:
            rel = "DIFFERENT statement-class"
        lines.append(f"CONTROL-{role} {d} (key-{k}, machine-picked, {rel}) {s[:8]}: "
                     f"verdict={cv} exit={crc} wall_s={cdt:.1f} stdout={cso!r}")

    # ---- guards after ----
    if sha(BIN) != bin_sha:
        raise SystemExit("ABORT: BINARY CHANGED MID-BATTERY")
    if sha(os.path.join(REPO, "keys/proving_key.bin")) != pk_sha:
        raise SystemExit("ABORT: PK CHANGED MID-BATTERY")
    if sha(os.path.join(REPO, "keys/verifying_key.bin")) != vk_sha:
        raise SystemExit("ABORT: VK CHANGED MID-BATTERY")
    lines.append(f"GUARD-AFTER binary={sha(BIN)[:16]} PK={sha(os.path.join(REPO, 'keys/proving_key.bin'))[:16]} "
                 f"VK={sha(os.path.join(REPO, 'keys/verifying_key.bin'))[:16]} — unchanged")
    lines.append(f"SILICON-END {telemetry()}")

    # ---- verdict per battery law ----
    if not all(v == "VALID" for v in verdicts.values()):
        lines.append("BATTERY VERDICT: QUARANTINED — a control flipped INVALID; "
                     "no verdict, bisect before any claim")
    elif v == "VALID":
        lines.append(f"BATTERY VERDICT: PRIMARY VALID + CONTROLS VALID — cycle-{cycle} A->B exchange COMPLETE: "
                     f"radio 5/5 SHA MATCH ({wrap_note} frames) + pairing VALID on B die, "
                     f"declare cross-bus byte-equal, machine-located, label {label} derived not typed; "
                     f"primary key-{primary_key}; settle queued (Cuneiform devnet)")
    else:
        lines.append("BATTERY VERDICT: PRIMARY INVALID + CONTROLS VALID — captured bytes fail pairing; "
                     "no settle; disclosed; bisect")

    out = "\n".join(lines)
    print(out)
    with open(log_path, "w") as fh:
        fh.write(out + "\n")


if __name__ == "__main__":
    main()
