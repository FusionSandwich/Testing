using Radiant
using LinearAlgebra
using Printf
using Dates

const RADIANT_COMMIT = get(ENV, "RADIANT_COMMIT", "unknown")
const TOL = 1.0e-9

struct AuditResult
    family::String
    order::Int
    nodes::Int
    edges::Int
    rank::Int
    centroid_inf::Float64
    residual_minus2_inf::Float64
    residual_minus4_inf::Float64
    min_gamma::Float64
    negative_gamma_count::Int
    first_mode_residual_inf::Float64
    defect_identity_residual_inf::Float64
    min_degree2_defect::Float64
    max_degree2_defect::Float64
    min_rate_times_defect::Float64
    status::String
    message::String
end

edge_map(edges) = Dict{Tuple{Int,Int},Int}(e => k for (k, e) in enumerate(edges))

function build_balance_system(Ω, w, voronoi_data, edges)
    nd = length(w)
    ne = length(edges)
    Γ = zeros(3 * nd, ne)
    b2 = zeros(3 * nd)
    b4 = zeros(3 * nd)
    emap = edge_map(edges)
    row = 1
    for i in 1:nd, q in 1:3
        for entry in voronoi_data[i]["data_triangle_ij"]
            j = entry["index"]
            e = emap[(min(i, j), max(i, j))]
            Γ[row, e] += Ω[q][j] - Ω[q][i]
        end
        b2[row] = -2 * w[i] * Ω[q][i]
        b4[row] = -4 * w[i] * Ω[q][i]
        row += 1
    end
    return Γ, b2, b4
end

function audit_case(family::String, order::Int)
    try
        Ω, w = Radiant.quadrature(order, family, 3, 3)
        vor = Radiant.voronoi_sphere(Ω)
        γ, edges = Radiant.fokker_planck_weights_3D(Ω, w, vor)
        Γ, b2, b4 = build_balance_system(Ω, w, vor, edges)
        nd = length(w)
        emap = edge_map(edges)

        centroid = [sum(w[i] * Ω[q][i] for i in 1:nd) for q in 1:3]
        centroid_inf = maximum(abs.(centroid))
        residual2 = maximum(abs.(Γ * γ - b2))
        residual4 = maximum(abs.(Γ * γ - b4))
        minγ = minimum(γ)
        nneg = count(x -> x < -TOL, γ)

        first_res = 0.0
        defect_identity_res = 0.0
        defects = zeros(nd)
        rate_defect = zeros(nd)
        for i in 1:nd
            lhs = zeros(3)
            eps = 0.0
            sq_action = 0.0
            total_rate = 0.0
            for entry in vor[i]["data_triangle_ij"]
                j = entry["index"]
                e = emap[(min(i, j), max(i, j))]
                aij = γ[e] / w[i]
                t = sum(Ω[q][i] * Ω[q][j] for q in 1:3)
                for q in 1:3
                    lhs[q] += aij * (Ω[q][j] - Ω[q][i])
                end
                eps += aij * (t - 1)^2
                sq_action += aij * (t^2 - 1)
                total_rate += aij
            end
            first_res = max(first_res,
                maximum(abs.(lhs .+ 2 .* [Ω[q][i] for q in 1:3])))
            defects[i] = eps
            defect_identity_res = max(defect_identity_res,
                abs((sq_action + 4) - eps))
            rate_defect[i] = total_rate * eps
        end

        status = residual2 ≤ 1e-7 && nneg == 0 &&
            first_res ≤ 1e-7 && defect_identity_res ≤ 1e-7 &&
            minimum(rate_defect) ≥ 4 - 1e-7 ? "PASS" : "FAIL"
        return AuditResult(
            family, order, nd, length(edges), rank(Γ), centroid_inf,
            residual2, residual4, minγ, nneg, first_res,
            defect_identity_res, minimum(defects), maximum(defects),
            minimum(rate_defect), status, "")
    catch err
        return AuditResult(family, order, 0, 0, 0, NaN, NaN, NaN, NaN, 0,
            NaN, NaN, NaN, NaN, NaN, "ERROR", sprint(showerror, err))
    end
end

cases = [
    ("gauss-legendre-chebychev", 2),
    ("gauss-legendre-chebychev", 3),
    ("gauss-legendre-chebychev", 4),
    ("carlson", 2),
    ("carlson", 4),
    ("carlson", 6),
    ("lebedev", 3),
    ("lebedev", 5),
    ("lebedev", 7),
    ("lebedev", 9),
]

results = [audit_case(family, order) for (family, order) in cases]

open("radiant_afp_audit.csv", "w") do io
    println(io, "family,order,nodes,edges,rank,centroid_inf,residual_minus2_inf,residual_minus4_inf,min_gamma,negative_gamma_count,first_mode_residual_inf,defect_identity_residual_inf,min_degree2_defect,max_degree2_defect,min_rate_times_defect,status,message")
    for r in results
        msg = replace(r.message, '"' => "''")
        @printf(io, "%s,%d,%d,%d,%d,%.17g,%.17g,%.17g,%.17g,%d,%.17g,%.17g,%.17g,%.17g,%.17g,%s,\"%s\"\n",
            r.family, r.order, r.nodes, r.edges, r.rank, r.centroid_inf,
            r.residual_minus2_inf, r.residual_minus4_inf, r.min_gamma,
            r.negative_gamma_count, r.first_mode_residual_inf,
            r.defect_identity_residual_inf, r.min_degree2_defect,
            r.max_degree2_defect, r.min_rate_times_defect, r.status, msg)
    end
end

open("radiant_afp_audit.md", "w") do io
    println(io, "# Radiant AFP compatibility audit")
    println(io)
    println(io, "- Timestamp (UTC): `$(Dates.now(Dates.UTC))`")
    println(io, "- Radiant commit: `$RADIANT_COMMIT`")
    println(io, "- Julia: `$(VERSION)`")
    println(io, "- Source balance target: `sum_j gamma_ij (Omega_j - Omega_i) = -2 w_i Omega_i`")
    println(io)
    println(io, "| Family | Order | Nodes | Edges | rank(Gamma) | weighted centroid | ||Gamma gamma-b2||inf | ||Gamma gamma-b4||inf | min gamma | negative gamma | max first-mode residual | min defect | max defect | min(rate*defect) | Status |")
    println(io, "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|")
    for r in results
        if r.status == "ERROR"
            println(io, "| $(r.family) | $(r.order) | - | - | - | - | - | - | - | - | - | - | - | - | ERROR: $(replace(r.message, '|' => '/')) |")
        else
            @printf(io, "| %s | %d | %d | %d | %d | %.3e | %.3e | %.3e | %.3e | %d | %.3e | %.3e | %.3e | %.6f | %s |\n",
                r.family, r.order, r.nodes, r.edges, r.rank,
                r.centroid_inf, r.residual_minus2_inf, r.residual_minus4_inf,
                r.min_gamma, r.negative_gamma_count,
                r.first_mode_residual_inf, r.min_degree2_defect,
                r.max_degree2_defect, r.min_rate_times_defect, r.status)
        end
    end
    println(io)
    println(io, "## Interpretation")
    println(io)
    println(io, "A `PASS` is a finite-instance certificate that Radiant's pseudoinverse output is nonnegative (up to the stated tolerance), satisfies the current source code's `-2` coordinate balance equation, obeys the exact degree-two defect identity, and satisfies the Lean-verified inequality `4 <= rate_i * defect_i`. It is not a family-wide proof.")
    println(io)
    println(io, "The `-4` residual is only a normalization diagnostic. The audited Radiant source constructs the right-hand side with factor `-2`, which matches the Cartesian-coordinate eigenvalue of the Laplace--Beltrami operator on `S^2`. Any rendered manuscript equation should be checked manually before asserting a typographical discrepancy.")
end

for r in results
    println(r)
end

if any(r -> r.status != "PASS", results)
    error("One or more Radiant AFP audit cases did not pass; inspect radiant_afp_audit.md")
end
