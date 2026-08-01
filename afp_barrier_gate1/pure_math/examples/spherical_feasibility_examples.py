#!/usr/bin/env python3
from shared_edge_examples import run as run_shared
from tangent_antipodal_examples import run as run_local

if __name__ == "__main__":
    run_local()
    run_shared()
    print("PASS: exact tangent, antipodal, perturbation, and shared-edge examples")
