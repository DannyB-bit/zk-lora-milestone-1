#!/usr/bin/env python3
"""staged_sha_gate.py — fail-closed pre-fire gate for the minigame B->A burst.

Verifies EVERY sealed frame on disk against the manifest BEFORE the radio is
touched: exact 245-byte length and exact SHA-256. Exits 0 only if every frame
matches; prints STAGED_SHA_OK=YES / NO.

Usage: staged_sha_gate.py <frames_dir> <manifest.json>
"""
import sys
import json
import hashlib
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    fd = Path(sys.argv[1])
    man = json.loads(Path(sys.argv[2]).read_text())
    bad = []
    for fr in man["frames"]:
        idx = fr["idx"]
        path = fd / ("frame_%02d.bin" % idx)
        if not path.exists():
            bad.append({"idx": idx, "error": "missing", "path": str(path)})
            continue
        b = path.read_bytes()
        if len(b) != 245:
            bad.append({"idx": idx, "error": "length", "got": len(b), "want": 245})
            continue
        got = hashlib.sha256(b).hexdigest()
        if got != fr["frame_sha256"]:
            bad.append({"idx": idx, "error": "sha256", "got": got,
                        "want": fr["frame_sha256"]})
    total = len(man["frames"])
    print("staged frames verified: %d of %d" % (total - len(bad), total))
    if bad:
        print("MISMATCH: " + json.dumps(bad))
        print("STAGED_SHA_OK=NO")
        return 1
    print("STAGED_SHA_OK=YES")
    return 0


if __name__ == "__main__":
    sys.exit(main())
