# P2F reproducibility package

Run from `afp_barrier_gate1` with the frozen P2E numerical stack:

```bash
python -m pure_math.p2f_hts.runner --output /tmp/P2F_RESULTS.json
python -m pure_math.p2f_hts.audit /tmp/P2F_RESULTS.json \
  --output /tmp/P2F_AUDIT.json
cmp benchmarks/p2f/P2F_RESULTS.json /tmp/P2F_RESULTS.json
cmp benchmarks/p2f/P2F_AUDIT.json /tmp/P2F_AUDIT.json
```

`P2F_MANIFEST.json` freezes geometry, incidence, group structure, reference
sizes, and the physics firewall.  `P2F_RESULTS.json` contains every reported
finite response and a scientific SHA-256.  `P2F_AUDIT.json` distinguishes
integrity PASS from the `BOUNDED_NEGATIVE` scientific outcome.

The model is deterministic because runtime and machine-dependent memory fields
are not included in the scientific result.
