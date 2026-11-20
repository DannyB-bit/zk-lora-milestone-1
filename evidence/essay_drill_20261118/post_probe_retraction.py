#!/usr/bin/env python3
"""post_probe_retraction.py — the bus has no DELETE (HTTP 501), so the schema-probe
event (B4641 / A1511) is permanent. Post an explicit retraction so it can never be
mistaken for a real verdict."""
import json, os, sys
sys.path.insert(0, "/home/researcher-bravo/fleet-repos/fleet/fast-channel")
from post_event import post

TOKEN = os.environ["FLEET_FAST_TOKEN"]
data = {
    "to": "alpha", "from": "bravo",
    "type": "chirp_raw_rx_verdict_SCHEMA_PROBE_RETRACTION",
    "drill": "essay_drill",
    "retracts": {"B_seq": 4641, "A_seq": 1511,
                 "posted_type": "chirp_raw_rx_verdict_SCHEMA_PROBE",
                 "posted_utc": "2026-11-20T00:20Z"},
    "reason": ("That event was a SCHEMA PROBE of the patched receipt code path, run against a "
               "re-fire manifest AFTER the drill had already closed. It is NOT a verdict and NOT a "
               "transmission. It carried no radio activity."),
    "what_is_real": {
        "final_verdict": "Alpha A1510 (leg B_to_A, round FINAL, ok=true) — echo_alpha_essay "
                         "136/136 + bravo_essay_md 15/15, both SHA exact-match, union 151/151 "
                         "DECRYPT_OK. That is the authoritative result.",
        "real_tx_receipts": ["B4615/A1493 (echo 136, gap 1s, reps 1)",
                             "B4616/A1494 (essay.md 15, gap 1s, reps 1)",
                             "B4630/A1503 (refire 80, gap 3s, reps 2)",
                             "B4631/A1504 (refire 80 receipt)",
                             "B4637/A1509 (refire 80, gap 3s, reps 2)"],
    },
    "note": ("The bus exposes no DELETE (HTTP 501), so the probe event cannot be removed. This "
             "retraction is posted on both buses so no downstream reader can mistake it for a "
             "verdict. Disclosed rather than left ambiguous."),
}
out = {}
for url, plane in (("http://127.0.0.1:8643", "B"), ("http://192.168.1.219:8643", "A")):
    try:
        out[plane] = post(url, "chirp_raw_rx_verdict_SCHEMA_PROBE_RETRACTION", data)
    except Exception as e:
        out[plane] = {"error": f"{type(e).__name__}: {e}"}
print(json.dumps(out, indent=1))
json.dump({"post": out, "data": data},
          open("/home/researcher-bravo/fleet/evidence/essay_drill_20261118/"
               "schema_probe_retraction.json", "w"), indent=1)
