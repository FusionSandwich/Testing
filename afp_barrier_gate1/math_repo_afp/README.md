# Imported Math AFP-adjacent angular package

This subtree is a byte-pinned import from `FusionSandwich/Math` commit
`ccc75ff90ddd8348aa805178f9f1925b9b10cd16`.

Included:

- the complete `src/hts_angular` package;
- direct standalone angular tests;
- angular examples;
- adaptive/positive-quadrature manuscripts;
- direct angular benchmark configuration and evidence;
- the upstream license notice and citation metadata.

Excluded intentionally:

- `hts_transport_ops`, thin-interface Papers 1–4, and their branch histories;
- calibration and evaluated-data claims;
- PR #14's unmaterialized Papers 1–4 integration claim;
- binary plots that duplicate the imported CSV/JSON evidence.

The import is not used to rewrite the accepted AFP proof chain.  It provides a
single reviewable home for previously split AFP-adjacent implementation work.
Run direct tests with:

```bash
PYTHONPATH=math_repo_afp/src python -m pytest -q \
  math_repo_afp/tests/test_angular.py \
  math_repo_afp/tests/test_sn2d.py \
  math_repo_afp/tests/test_adaptive_sn2d.py \
  math_repo_afp/tests/test_v02_global_graph.py \
  math_repo_afp/tests/test_v02_sn3d.py
```
