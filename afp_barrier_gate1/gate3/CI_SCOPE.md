# Gate 3 CI scope

This branch is based on the Gate 2 verified source and is checked by both the established Lean workflow and the Gate 3 deterministic audit workflow.

The verification surface comprises:

- Lean kernel build and axiom audit;
- exact symbolic `N=2` GLC case;
- deterministic all-order sampling through `N=512`;
- odd-order equatorial asymptotics through `N=511`;
- direct source-pinned comparison with `CBienvenue/Radiant.jl`.
