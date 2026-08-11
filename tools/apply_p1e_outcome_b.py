#!/usr/bin/env python3
"""Apply the publication-wide Outcome B migration for the P1E blocker.

The migration is deliberately deterministic and idempotent. It edits only
accepted/live publication surfaces on the dedicated repair branch. Historical
rejected-route documents and frozen branches are not rewritten.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Callable

CHANGED: list[str] = []


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise AssertionError(f"{label}: expected one literal occurrence, found {count}")
    return text.replace(old, new, 1)


def sub_once(text: str, pattern: str, replacement: str, label: str, flags: int = 0) -> str:
    result, count = re.subn(pattern, lambda _: replacement, text, count=1, flags=flags)
    if count != 1:
        raise AssertionError(f"{label}: expected one regex occurrence, found {count}")
    return result


def update(root: Path, relative: str, transform: Callable[[str], str]) -> None:
    path = root / relative
    text = path.read_text(encoding="utf-8")
    new = transform(text)
    if new != text:
        path.write_text(new, encoding="utf-8")
        CHANGED.append(relative)
        print(f"UPDATED {relative}")
    else:
        print(f"UNCHANGED {relative}")


def flagship(text: str) -> str:
    if "### Proposition 7.3 (fixed-level local persistence)" in text:
        return text

    text = replace_once(
        text,
        "The three-dimensional robustness proposition is restricted to\n"
        "support-preserving reflected latitude perturbations.",
        "At each fixed three-dimensional level, the construction is locally persistent\n"
        "under sufficiently small support-preserving reflected latitude perturbations;\n"
        "the radius is existential and level dependent.",
        "flagship abstract",
    )

    old_contribution = (
        "7. It constructs matching-order local positive families in `d=2,3`. The\n"
        "   circle family is an exact regular-polygon calculation. The spherical\n"
        "   family uses shared conductances on adaptive reflected rings, proves every\n"
        "   row moment equation at all levels, and gives the explicit constants\n"
        "   $\\mathsf R_3=64\\pi^2$ and $C_3=75/2$."
    )
    new_contribution = old_contribution + (
        " At each fixed spherical level,\n"
        "   nonsingularity and strict positivity also give an existential local\n"
        "   persistence radius; no radius uniform over the levels is claimed."
    )
    text = replace_once(text, old_contribution, new_contribution, "flagship contribution")

    text = replace_once(
        text,
        "| 6 | Matching-order local positive construction | Theorems 7.1--7.2 | accepted P1E for `d=2,3` |",
        "| 6 | Matching-order local positive construction and fixed-level persistence | Theorems 7.1--7.2 and Proposition 7.3 | accepted for `d=2,3`; persistence radius existential at fixed `J` |",
        "flagship theorem hierarchy",
    )

    text = sub_once(
        text,
        r"\nFor the structured robustness proposition below, set\n\$\$\nK_\*=.*?\n\$\$\n\n#### Proof",
        "\n#### Proof",
        "remove rejected constant block",
        re.S,
    )
    text = replace_once(text, "\\tag{7.20}", "\\tag{7.19}", "renumber normalization")
    text = replace_once(text, "\\tag{7.21}", "\\tag{7.20}", "renumber covariance")

    new_prop = r'''### Proposition 7.3 (fixed-level local persistence)

Fix one level $J$ of the unperturbed construction in Theorem 7.2. Preserve
the pole, equator, every ring count and longitude phase, every radial mask and
horizontal jump integer, the undirected support, and north--south reflection.
Assume the finitely many unperturbed local systems are nonsingular and the
finitely many recovered unperturbed conductances are strictly positive, as in
the construction proof. Then there exists
$$
\delta_J>0
$$
such that every reflected latitude displacement of sup norm less than
$\delta_J$ leaves the same local systems uniquely solvable and all recovered
shared conductances strictly positive. After the normalization used in
Theorem 7.2, the resulting generator is positive and reversible and satisfies
$$
L_{J,\eta}\mathbf1=0,
\qquad
L_{J,\eta}\Omega=-2\Omega .
$$
One common ambient rotation is also permitted. The radius is existential and
may depend on $J$. No positive lower bound uniform in $J$, no prescribed power
of $h$, and no perturbed all-level rate or quadratic-defect constants are
asserted.

#### Proof

At fixed $J$ there are finitely many latitude variables, local systems, and
support edges. On the open parameter set where latitude order, support
incidences, active chord losses, and every displayed geometric denominator are
preserved, each local matrix $A_q(\eta)$ and right-hand side $b_q(\eta)$ is
continuous. Since $\det A_q(0)\ne0$, inverse continuity makes every finite
recursive solution continuous near $\eta=0$. Thus the final vector
$(\Gamma_e(\eta))_{e\in E_J}$ of one conductance per undirected edge is
continuous. Its unperturbed minimum is positive, so all conductances remain
positive on a sufficiently small open sup-norm ball.

For such a perturbation, the re-solved exact row equations give
$$
\sum_j\Gamma_{ij}(\eta)(\Omega_j-\Omega_i)
=-2\mu_i(\eta)\Omega_i,
\qquad
\mu_i(\eta)=\frac12\sum_j\Gamma_{ij}(\eta)
 (1-\Omega_i\cdot\Omega_j)>0.
$$
Normalizing by $W(\eta)=\sum_i\mu_i(\eta)$ yields positive masses and shared
symmetric conductances, hence reversibility, constant reproduction, and the
coordinate eigenvalue $-2$. A common rotation preserves every inner product
and rotates both sides of the force identity. The complete fixed-level proof,
including a well-defined choice of radius, is
`../P1E_FIXED_LEVEL_LOCAL_PERSISTENCE.md`. $\square$

## 8. Exact examples'''
    text = sub_once(
        text,
        r"### Proposition 7\.3 \(structured support-preserving robustness\)\n.*?\n## 8\. Exact examples",
        new_prop,
        "replace Proposition 7.3",
        re.S,
    )

    text = sub_once(
        text,
        r"^\| Proposition 7\.3, structured robustness.*$",
        "| Proposition 7.3, fixed-level local persistence | `docs/publication_program/P1E_FIXED_LEVEL_LOCAL_PERSISTENCE.md` | `p1e_fixed_level_persistence_audit.py` contract and mutation checks | P1E-LOCAL-PERSIST | accepted with existential level-dependent radius; no uniform rate/defect conclusion |",
        "flagship source map",
        re.M,
    )

    text = sub_once(
        text,
        r"8\. The `d=3` perturbation proposition fixes ring counts, phases, masks, horizontal\n"
        r"   jumps, pole/equator data, and reflection\. It does not cover arbitrary node\n"
        r"   motion or independent longitude perturbations\.",
        "8. Proposition 7.3 is only a fixed-level local persistence result. Its radius is\n"
        "   existential and level dependent, and it fixes counts, phases, masks, jumps,\n"
        "   support, pole/equator data, and reflection. It supplies no perturbed\n"
        "   all-level rate or quadratic-defect constants.",
        "flagship limitations",
    )

    rejected_anchor = "| Positivity universally forbids higher-order graph Laplacians."
    rejected_row = (
        "| A prose operation-count recurrence proves a universal perturbation radius. | "
        "The repository had no generated expression graph, complete denominator ledger, "
        "intermediate enclosures, or independent certificate consumer. | Use Proposition "
        "7.3 only at fixed level with an existential level-dependent radius. |\n"
    )
    text = replace_once(text, rejected_anchor, rejected_row + rejected_anchor, "flagship rejected claim row")
    return text


def construction_source(text: str) -> str:
    if "## 10. Fixed-level local persistence" in text:
        return text
    new_section = r'''## 10. Fixed-level local persistence

The unperturbed all-level construction and the constants in Section 9 are
unchanged. The perturbation result is instead local at each fixed level.

Fix a level $J$ and freeze the pole, equator, counts, longitude phases, radial
masks, horizontal jumps, undirected support, and north--south reflection. Let
$\eta\in\mathbb R^{m_J}$ be the vector of northern-ring latitude
displacements, reflected in the south. Index the finite collection of polar,
ordinary, transition, and equatorial systems by $q$ and write
\[
 A_q(\eta)x_q(\eta)=b_q(\eta).                         \tag{10.1}
\]
On the open set where latitude order, active chord losses, support incidences,
and all geometric denominators are preserved, the entries of every
$A_q(\eta)$ and $b_q(\eta)$ are continuous. At the unperturbed point every
$A_q(0)$ is nonsingular and every recovered preliminary conductance is
strictly positive by Sections 4--8.

Because there are only finitely many systems and edges at fixed $J$, inverse
continuity and finite recursive substitution make the final shared-edge vector
\[
 X_J(\eta)=(\Gamma_e(\eta))_{e\in E_J}                \tag{10.2}
\]
continuous near zero. The good set
\[
 \mathcal U_J=\{\eta:\det A_q(\eta)\ne0\ \forall q,
                      \ \Gamma_e(\eta)>0\ \forall e\} \tag{10.3}
\]
is open and contains zero. Hence there exists an existential, level-dependent
$\delta_J>0$ such that $\|\eta\|_\infty<\delta_J$ implies unique solvability
and positive shared conductances.

The exact row force equations still give
\[
 \sum_j\Gamma_{ij}(\eta)(\Omega_j-\Omega_i)
 =-2\mu_i(\eta)\Omega_i,
 \qquad
 \mu_i(\eta)=\frac12\sum_j\Gamma_{ij}(\eta)\ell_{ij}>0. \tag{10.4}
\]
The normalization (9.3) therefore produces a positive reversible generator
with exact $H_0\oplus H_1$ fidelity. A common ambient rotation is harmless.

This radius is existential and level dependent. No level-uniform lower bound,
no prescribed mesh-power scale, and no perturbed all-level rate or
quadratic-defect constants are proved. The full ordinary proof is
`P1E_FIXED_LEVEL_LOCAL_PERSISTENCE.md`.

### Corrected certification boundary

The literal unperturbed checks remain:

1. `p1e_short_gap_symbolic_matrix_audit.py` for the exact transition algebra;
2. `p1e_short_gap_cauchy_guard_audit.py` and
   `p1e_short_gap_cauchy_hostile_audit.py` for the unperturbed all-orders
   guards;
3. `p1e_short_gap_polar_guard_audit.py` for the first polar row;
4. `p1e_short_gap_family_audit.py` for finite row-class regressions and failed
   mutations; and
5. `p1e_short_gap_proof_audit.py` for exact phase, recurrence, and constant
   arithmetic.

`p1e_no_guard_ring_independent_audit.py` retains independent schedule,
determinant, recurrence, and rate regressions. Its former abstract exponent
recurrence is explicitly noncertifying and is not a proof of a derivative
program. The fixed-level theorem contract and its independent mutations are
checked by `p1e_fixed_level_persistence_audit.py`; that verifier checks scope,
not the analytic unperturbed family.

The superseded universal statement is retained only as a rejected historical
claim in `P1E_REJECTED_UNIFORM_ROBUSTNESS_CLAIM.md`.
'''
    return sub_once(
        text,
        r"## 10\. Support-preserving robustness and certification manifest\n.*\Z",
        new_section,
        "construction Section 10",
        re.S,
    )


def independent_audit_doc(text: str) -> str:
    if "## 11. Corrected perturbation disposition" in text:
        return text
    verdict = r'''## Final verdict

**ACCEPTED FOR THE UNPERTURBED $d=3$ CONSTRUCTION; THE FORMER UNIVERSAL
PERTURBATION CLAIM IS REJECTED.**

The opening audit correctly identified defects in the early schedule,
transition recurrence, first-row guard, and perturbation scope. The later
reachable-domain, Cauchy, first-row, and recurrence repairs support the
unperturbed all-level theorem. They do not supply a literal differentiated
expression graph or a level-uniform perturbation certificate. Sections 11 and
12 of the former version are therefore superseded by the corrected disposition
below. The fixed-level replacement is proved independently in
`P1E_FIXED_LEVEL_LOCAL_PERSISTENCE.md`.

The integer schedule'''
    text = sub_once(
        text,
        r"## Final verdict\n\n.*?\n\nThe integer schedule",
        verdict,
        "independent-audit verdict",
        re.S,
    )
    corrected_tail = r'''## 11. Corrected perturbation disposition

The abstract scalar recurrence formerly printed in this section proves only
the following conditional statement: if a specified arithmetic program has a
given length and if every leaf, analytic atom, and reciprocal already obeys
the assumed bounds, then a very large bound follows by induction. The
repository did not instantiate those premises with a complete expression DAG,
mechanically derived operation count, denominator ledger, or output map for
all row classes. The recurrence is therefore not a certificate for the
construction.

At fixed level $J$, the correct argument is finite-dimensional. The finitely
many local matrices and right-hand sides depend continuously on the reflected
latitude parameters on a guarded open domain. Their determinants are nonzero
at the unperturbed point, and the finitely many unperturbed shared
conductances have a positive minimum. Thus the set on which every determinant
is nonzero and every conductance is positive is open and contains zero. It
contains a positive sup-norm ball, giving an existential radius $\delta_J>0$.
Exact $H_0\oplus H_1$ fidelity follows from the re-solved force equations and
the one-half mass normalization.

Nothing in this argument bounds $\delta_J$ below uniformly in $J$ or supplies
perturbed all-level rate or quadratic-defect constants.

## 12. Final audit classification

| Component | Classification |
|---|---|
| unperturbed schedule, row systems, Cauchy/first-row guards, and recurrence | accepted ordinary proof with exact regression surfaces |
| unperturbed positivity, reversibility, exact coordinates, rate, and sampled quotient constants | accepted for the stated `d=3` family |
| abstract exponent recurrence in the former audit script | historical arithmetic regression; noncertificate |
| universal all-level perturbation radius and perturbed constants | rejected |
| fixed-level support-preserving local persistence | proved in `P1E_FIXED_LEVEL_LOCAL_PERSISTENCE.md` |

## 13. Reproduction

Run

    python afp_barrier_gate1/pure_math/covariance/p1e_no_guard_ring_independent_audit.py
    python afp_barrier_gate1/pure_math/covariance/p1e_fixed_level_persistence_audit.py --root .

The first command checks retained exact fixtures. The second independently
checks the corrected theorem contract, required repository markers, and
mutation failures. Neither command replaces the ordinary analytic proofs.
'''
    return sub_once(
        text,
        r"## 11\. An explicit analytic all-orders closure\n.*\Z",
        corrected_tail,
        "independent-audit tail",
        re.S,
    )


def independent_audit_script(text: str) -> str:
    if "historical arithmetic regression; not a construction certificate" in text:
        return text
    text = replace_once(
        text,
        '"""Exact regressions for the independent no-guard ring audit."""',
        '"""Exact retained regressions for the no-guard ring audit.\n\nThe exponent check below is a historical arithmetic regression; not a\nconstruction certificate, derivative graph, or all-level perturbation proof.\n"""',
        "independent script docstring",
    )
    replacement = '''def historical_exponent_recurrence() -> None:\n    """Check only the old conditional scalar recurrence, not its premises."""\n    length = 10**6\n    exponent = 28 * 2**length - 12\n    require(exponent == (16 + 12) * 2**length - 12, "compiler exponent arithmetic")\n    base_exponent = 28 * 2**length + 100\n    require(base_exponent - exponent > 100, "arithmetic margin")\n'''
    text = sub_once(
        text,
        r"def straight_line_compiler\(\) -> None:\n.*?\n\ndef main\(\) -> None:",
        replacement + "\n\ndef main() -> None:",
        "independent script compiler function",
        re.S,
    )
    text = replace_once(text, "    straight_line_compiler()", "    historical_exponent_recurrence()", "independent script call")
    text = replace_once(
        text,
        '    print("no-guard ring independent audit: exact regressions PASS")',
        '    print("historical compiler recurrence: NONCERTIFICATE")\n    print("no-guard ring independent audit: exact regressions PASS")',
        "independent script output",
    )
    return text


def theorem_registry(text: str) -> str:
    if "| P1E-LOCAL-PERSIST | PROVED |" in text:
        return text
    text = sub_once(
        text,
        r"^\| F-CONSTRUCT \|.*$",
        "| F-CONSTRUCT | PROVED | Matching-order positive reversible local families exist in `d=2,3`. In `d=3`, the unperturbed no-guard adaptive-ring family has `R_3=64 pi^2`, `C_3=75/2`, exact `H_0,H_1`, and rowwise `B_i=0`. Fixed-level local persistence is recorded separately. | P1E shortened-gap theorem Sections 1--9; final hostile Cauchy/first-row audit; exact construction audits | no `d>3` construction; no uniform perturbation radius or perturbed all-level constants | I |",
        "registry F-CONSTRUCT",
        re.M,
    )
    ring_line = "| P1E-RING | PROVED | The explicit unperturbed reflected adaptive-ring family on `S^2` has positive shared conductances, bounded degree and angular window, exact `L1=0`, exact `L Omega=-2 Omega`, `r_max<=64pi^2 h^-2`, and `mathfrak D_2<=75h^2/2`; P1B gives lower constant `3/(32pi^2)`. | `P1E_SHORT_GAP_S2_CONSTRUCTION.md`, Sections 1--9; `P1E_SHORT_GAP_CAUCHY_HOSTILE_AUDIT.md`; exact audits | `d=3` only; this entry is unperturbed | I |"
    local_line = "| P1E-LOCAL-PERSIST | PROVED | For every fixed level `J` whose unperturbed local systems are nonsingular and recovered conductances strictly positive, there exists an existential level-dependent radius `delta_J>0` on which frozen-support reflected latitude perturbations retain solvability, positivity, reversibility, and exact `H_0 direct-sum H_1`. | `P1E_FIXED_LEVEL_LOCAL_PERSISTENCE.md`; source-first theorem audit | radius nonexplicit and not uniform in `J`; no mesh-power law or perturbed rate/defect constants; no arbitrary node motion | I |"
    text = sub_once(
        text,
        r"^\| P1E-RING \|.*$",
        ring_line + "\n" + local_line,
        "registry P1E rows",
        re.M,
    )
    text = sub_once(
        text,
        r"^\| P1E-FORMAL \|.*$",
        "| P1E-FORMAL | PROVED | The finite algebraic implications from a shared positive stress to detailed balance, exact `H_1`, moment normalization, rate conversion and polygon residual identities are machine-checked. | `QuadraticFidelityConstruction.lean`; `PureMathAxiomAudit.lean` | does not formalize the analytic ring schedule, Cauchy guards, fixed-level continuity, or existence of `delta_J` | I |",
        "registry P1E formal",
        re.M,
    )
    return text


def approach_registry(text: str) -> str:
    if "fixed-level reflected latitude persistence" in text:
        return text
    return sub_once(
        text,
        r"^\| structured latitude perturbation \| robustness \|.*$",
        "| fixed-level reflected latitude persistence | robustness | PROVED_FIXED_LEVEL | for each fixed level, frozen-support reflected perturbations retain positivity and exact `H_0,H_1` below an existential `delta_J` | no radius uniform in level and no perturbed all-level constants | a complete uniform determinant/inverse/conductance certificate | I/III |",
        "global approach registry",
        re.M,
    )


def p1e_approach_registry(text: str) -> str:
    if "fixed-level local persistence theorem" in text:
        return text
    text = sub_once(
        text,
        r"^\| structured perturbation theorem \|.*$",
        "| fixed-level local persistence theorem | PROVED_FIXED_LEVEL | for each fixed level, support-preserving reflected latitude perturbations plus a common rotation | radius is existential and level dependent; retain counts, phases, masks, jumps, support, and reflection |",
        "P1E approach row",
        re.M,
    )
    text = replace_once(
        text,
        "- Robustness is only the explicitly support-preserving structured class unless\n  a global six-moment right inverse is proved.",
        "- Perturbation persistence is proved only at each fixed level for the frozen\n  support-preserving reflected class. A uniform all-level statement requires a\n  new determinant/inverse/conductance certificate or a global right inverse.",
        "P1E approach boundary",
    )
    return text


def p1e_stage(text: str) -> str:
    if "FORMER_UNIFORM_PERTURBATION_CLAIM_REJECTED" in text:
        return text
    text = sub_once(
        text,
        r"## Current publication status\n\n```text\n.*?```\n\nThe ordinary `d=3` proof.*?claim\.",
        "## Current publication status\n\n```text\nUNPERTURBED_D3_THEOREM_RETAINED\nFIXED_LEVEL_LOCAL_PERSISTENCE_PROVED\nFORMER_UNIFORM_PERTURBATION_CLAIM_REJECTED\nREPAIR_BRANCH_NOT_MERGED\n```\n\nThe ordinary unperturbed `d=3` proof remains supported by the rational-Cauchy, first-row, recurrence, and positivity arguments. This repair does not rewrite the frozen P1E archive; it corrects the live publication descendant and records the former universal perturbation statement as rejected.",
        "P1E stage status",
        re.S,
    )
    text = sub_once(
        text,
        r"These constants are accepted for the stated `d=3` family\. They are not\nasserted for `d>3`\. The perturbation statement is deliberately\nrestricted to support-preserving latitude perturbations with the fixed ring\ncounts, phases, masks, horizontal jumps, equatorial reflection, and a common\nambient rotation\. It is not a theorem for independent longitude motion or\narbitrary node perturbations\.",
        "These constants are accepted only for the stated unperturbed `d=3` family and are not asserted for `d>3`. The perturbation replacement is a fixed-level local persistence theorem: for each fixed `J`, the stated nonsingularity and positivity margins imply an existential level-dependent `delta_J>0` for frozen-support reflected latitude perturbations and a common rotation. It gives no radius uniform in `J`, no prescribed mesh-power scale, and no perturbed rate or defect constants.",
        "P1E stage theorem boundary",
    )
    text = sub_once(
        text,
        r"^\| independent schedule/recurrence audit \|.*$",
        "| independent schedule/recurrence audit | `docs/publication_program/P1E_NO_GUARD_RING_INDEPENDENT_AUDIT.md` | retains exact schedule, determinant, rate, and recurrence findings; its former compiler arithmetic is noncertifying |",
        "P1E stage independent doc",
        re.M,
    )
    text = sub_once(
        text,
        r"^\| independent exact fixtures \|.*$",
        "| independent exact fixtures | `p1e_no_guard_ring_independent_audit.py` | reachable-floor, determinant, recurrence, and rate regressions; no perturbation certificate |",
        "P1E stage independent script",
        re.M,
    )
    return text


def p1f_stage(text: str) -> str:
    if "FORMER_UNIFORM_PERTURBATION_CLAIM_REJECTED" in text:
        return text
    text = sub_once(
        text,
        r"## Status\n\n```text\n.*?```\n\nThe manuscript now assembles.*?occurred\.",
        "## Status\n\n```text\nMANUSCRIPT_THEOREM_HIERARCHY_CORRECTED\nUNPERTURBED_P1E_CONSTRUCTION_RETAINED\nFIXED_LEVEL_LOCAL_PERSISTENCE_PROVED\nFORMER_UNIFORM_PERTURBATION_CLAIM_REJECTED\nREPAIR_BRANCH_NOT_MERGED\n```\n\nThe manuscript assembles the P1A--P1E mathematics with Proposition 7.3 weakened to the strongest proved fixed-level statement. The prior P1E and P1F release objects remain historical and unmodified; the dedicated repair branch is a descendant of the live pull-request head and is not an archive or merged release.",
        "P1F stage status",
        re.S,
    )
    text = sub_once(
        text,
        r"The frontier, equality, and stability theorems remain all-dimensional\. The\nconstruction does not extend to `d>3`, and the `d=3` robustness proposition covers\nonly fixed-support reflected latitude perturbations with the construction's\ncounts, phases, masks, horizontal jumps, pole/equator data, and a common\nambient rotation preserved\.",
        "The frontier, equality, and stability theorems remain all-dimensional. The construction does not extend to `d>3`. At each fixed `d=3` level, frozen-support reflected latitude perturbations persist below an existential level-dependent radius. No all-level perturbation radius or perturbed rate/defect constants are claimed.",
        "P1F stage scope",
    )
    text = replace_once(
        text,
        "| construction/formal release audit | `FORMAL_AND_RELEASE_AUDIT.md` | finite Lean surface and deterministic P1E audit boundary |",
        "| construction/formal release audit | `FORMAL_AND_RELEASE_AUDIT.md` | finite Lean surface; no formal perturbation continuity claim |\n"
        "| fixed-level persistence proof | `../P1E_FIXED_LEVEL_LOCAL_PERSISTENCE.md` | ordinary continuity proof and exact scope |\n"
        "| theorem-by-theorem audit | `../P1E_FLAGSHIP_THEOREM_AUDIT.md` | hypotheses, dependencies, Lean scope, and final classification for all 16 results |",
        "P1F evidence table",
    )
    text = sub_once(
        text,
        r"\| publication artifact \| `output/pdf/FLAGSHIP_MANUSCRIPT\.pdf` \| rendered 23-page paper built from the checked-in source and bibliography \|",
        "| publication artifact | `output/pdf/FLAGSHIP_MANUSCRIPT.pdf` | rebuilt corrected paper; exact page count and hashes are in the repair reproducibility manifest |",
        "P1F artifact row",
    )
    return text


def value_registry(text: str) -> str:
    if "No perturbed all-level rate or defect constant is registered" in text:
        return text
    return sub_once(
        text,
        r"The accepted `d=3` perturbation constants apply only to support-preserving\nlatitude perturbations with fixed combinatorial data\. No exact-head workflow\nstatus is inferred from these mathematical constants\.",
        "The unperturbed `d=3` constants apply only to the exact adaptive-ring family. At each fixed level the corrected theorem supplies an existential level-dependent persistence radius for frozen combinatorial data. No perturbed all-level rate or defect constant is registered, and no workflow status is inferred from the mathematics.",
        "value registry perturbation boundary",
    )


def prose_audit(text: str) -> str:
    if "PASS AFTER EXACT WEAKENING" in text:
        return text
    text = replace_once(
        text,
        "**PASS WITH EXPLICIT DIMENSION AND ROBUSTNESS BOUNDARIES.**",
        "**PASS AFTER EXACT WEAKENING AND REPOSITORY-WIDE SCOPE RECONCILIATION.**",
        "prose verdict",
    )
    text = sub_once(
        text,
        r"^\| Generic perturbation robustness inferred \|.*$",
        "| Uniform or generic perturbation persistence inferred | Proposition 7.3; abstract; limitations | PASS | only fixed-level frozen-support reflected latitude perturbations are proved, with existential `delta_J`; no mesh-power law or perturbed all-level constants |",
        "prose perturbation row",
        re.M,
    )
    text = replace_once(
        text,
        "- [x] structured robustness stated at exactly the proved scale;",
        "- [x] fixed-level local persistence stated with an existential level-dependent radius and no unproved scale;",
        "prose checklist",
    )
    return text


def priority_audit(text: str) -> str:
    if "fixed-level local-persistence boundary" in text:
        return text
    return replace_once(
        text,
        "   remainder, sampling-quotient, and structured-robustness hypotheses proved by P1E.",
        "   remainder and sampling-quotient hypotheses proved by the unperturbed P1E construction, together with the corrected fixed-level local-persistence boundary.",
        "priority item 8",
    )


def referee_audit(text: str) -> str:
    if "fixed-level local persistence theorem are now proved" in text:
        return text
    return replace_once(
        text,
        "mask moment, no-guard schedule, adaptive integer bracket, literal finite\nmatrices, global conductance recurrence, direct quotient identity, and narrow\nrobustness theorem are now proved.",
        "mask moment, no-guard schedule, adaptive integer bracket, literal finite\nmatrices, global conductance recurrence, direct quotient identity, and the\nfixed-level local persistence theorem are now proved. The former uniform\nperturbation claim is separately retained as rejected history.",
        "referee opening",
    )


def formal_audit(text: str) -> str:
    if "fixed-level continuity theorem or any radius uniform in the refinement level" in text:
        return text
    text = replace_once(
        text,
        "- structured perturbation robustness.",
        "- the fixed-level continuity theorem or any radius uniform in the refinement level.",
        "formal scope bullet",
    )
    text = replace_once(
        text,
        "This acceptance covers the finite formal identities described below.  It does\nnot upgrade the ordinary analytic mesh proof, Cauchy enclosure, or global\nrecurrence to machine-checked status.",
        "This acceptance covers the finite formal identities described below. It does\nnot upgrade the ordinary analytic mesh proof, Cauchy enclosure, global\nrecurrence, or fixed-level persistence argument to machine-checked status.\nIn particular, Lean proves neither continuity of the local systems nor the\nexistence of the level-dependent radius.",
        "formal verdict boundary",
    )
    return text


def lean_scope(text: str) -> str:
    if "fixed-level continuity argument" in text:
        return text
    return replace_once(
        text,
        "construction.  The analytic mesh construction and its uniform constants live\nin the ordinary proof; the statements here certify the identities that turn a\nshared positive moment stress into a reversible generator with exact linear\nreproduction.  No injectivity of a sampling map is used.",
        "construction. The analytic unperturbed mesh construction and its constants live\nin the ordinary proof; the statements here certify only the finite identities\nthat turn a shared positive moment stress into a reversible generator with exact\nlinear reproduction. They do not formalize the fixed-level continuity argument,\nthe existence of a persistence radius, or any radius uniform in the refinement\nlevel. No injectivity of a sampling map is used.",
        "Lean module scope",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--check", action="store_true", help="fail if migration would change files")
    args = parser.parse_args()
    root = args.root.resolve()

    updates: tuple[tuple[str, Callable[[str], str]], ...] = (
        ("docs/publication_program/p1f_manuscript/FLAGSHIP_MANUSCRIPT.md", flagship),
        ("docs/publication_program/P1E_SHORT_GAP_S2_CONSTRUCTION.md", construction_source),
        ("docs/publication_program/P1E_NO_GUARD_RING_INDEPENDENT_AUDIT.md", independent_audit_doc),
        ("afp_barrier_gate1/pure_math/covariance/p1e_no_guard_ring_independent_audit.py", independent_audit_script),
        ("docs/publication_program/THEOREM_REGISTRY.md", theorem_registry),
        ("docs/publication_program/APPROACH_REGISTRY.md", approach_registry),
        ("docs/publication_program/P1E_APPROACH_REGISTRY.md", p1e_approach_registry),
        ("docs/publication_program/P1E_STAGE_REPORT.md", p1e_stage),
        ("docs/publication_program/p1f_manuscript/P1F_STAGE_REPORT.md", p1f_stage),
        ("docs/publication_program/VALUE_REGISTRY.md", value_registry),
        ("docs/publication_program/p1f_manuscript/PROSE_OVERCLAIM_AUDIT.md", prose_audit),
        ("docs/publication_program/p1f_manuscript/PRIORITY_AND_HOSTILE_REFEREE_AUDIT.md", priority_audit),
        ("docs/publication_program/P1E_SHORT_GAP_S2_REFEREE_AUDIT.md", referee_audit),
        ("docs/publication_program/p1f_manuscript/FORMAL_AND_RELEASE_AUDIT.md", formal_audit),
        ("afp_barrier_gate1/AFPBarrier/QuadraticFidelityConstruction.lean", lean_scope),
    )
    for relative, transform in updates:
        update(root, relative, transform)

    print(f"MIGRATION_CHANGED_COUNT {len(CHANGED)}")
    for relative in CHANGED:
        print(f"MIGRATION_CHANGED {relative}")
    if args.check and CHANGED:
        raise SystemExit("Outcome B migration is not yet applied")


if __name__ == "__main__":
    main()
