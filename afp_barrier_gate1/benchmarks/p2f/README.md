# P2F reproducibility package

Run from `afp_barrier_gate1` with the frozen numerical stack:

```bash
python -m pure_math.p2f_hts.runner --output /tmp/P2F_RESULTS.json
python -m pure_math.p2f_hts.audit /tmp/P2F_RESULTS.json \
  --output /tmp/P2F_AUDIT.json
cmp benchmarks/p2f/P2F_RESULTS.json /tmp/P2F_RESULTS.json
cmp benchmarks/p2f/P2F_AUDIT.json /tmp/P2F_AUDIT.json
```

`P2F_MANIFEST.json` freezes geometry, incidence, group structure, the
50/72/98/128-direction reference sweep, convergence and operator-sensitivity
tolerances, and the physics firewall.  `P2F_RESULTS.json` contains every
reported finite response and a scientific SHA-256.  `P2F_AUDIT.json`
distinguishes structural integrity PASS from the scientific outcome
`INCONCLUSIVE_REFERENCE_NOT_CONVERGED`.

The audit deliberately permits a structurally valid run to have an
inconclusive scientific outcome.  No response-performance claim is allowed
unless the declared reference convergence gate passes and a method-error
difference is resolved.
