# Vendored control payload (cycle-87 battery)

`rx_payload_128b.bin` in this dir is VENDORED, not captured on this branch:
byte-exact checkout of `158c0a52` (PR#48 head, `evidence/groth16_ota_20261011T1840Z_cycle84/rx_payload_128b.bin`),
the c-84 PRIMARY capture of `4b4160488a948fa96117efa820065c07bf7cd85fb2cda7def8be6cf4954912c0`
(key-33, declare B1250 == A484, the prior same-statement-class of cycle-87's PRIMARY e703bfd3).

The c-87 T12 battery ABORTED fail-closed on first run (NORMAL mode, NOT first-of-class,
no locally verifiable same-class payload — see `t12_cycle87_battery_attempt1_abort.no-local-sameclass-control.log`
in the c-87 evidence dir); per the template's own instruction and the c-84 precedent
(e6a6b296 vendored from origin/main PR#10 blob 6b82efc4), the prior same-class payload
is vendored and the battery re-run. Provenance: `git show 158c0a52:...` on this node,
2026-10-12T03:4xZ. Verify: sha256(file) == 4b4160488a948fa96117efa820065c07bf7cd85fb2cda7def8be6cf4954912c0.
