using Radiant
using LinearAlgebra
using Printf
using Dates

const RADIANT_COMMIT = get(ENV, "RADIANT_COMMIT", "unknown")
const TOL = 5.0e-10

function independent_glc_matrix(N::Int)
    μ, w = Radiant.gauss_legendre(N)
    idx = sortperm(μ)
    μ = μ[idx]
    w = w[idx]
    ρ = sqrt.(max.(0.0, 1 .- μ.^2))
    h = π / N
    naz = 2N

    β = zeros(N + 1)
    d = zeros(N + 1)
    for n in 2:N
        β[n] = β[n - 1] - 2w[n - 1] * μ[n - 1]
        d[n] = (ρ[n] - ρ[n - 1]) / (μ[n] - μ[n - 1])
    end

    c = zeros(N)
    K = zeros(N)
    q = zeros(N)
    for n in 1:N
        c[n] = (β[n + 1] * d[n + 1] - β[n] * d[n]) / w[n]
        K[n] = 2(1 - μ[n]^2) + c[n] * ρ[n]
        q[n] = K[n] / (2ρ[n]^2 * (1 - cos(h)))
    end

    L = zeros(naz * N, naz * N)
    linear_index(n, i) = i + naz * (n - 1)
    for n in 1:N, i in 1:naz
        ii = linear_index(n, i)
        if n > 1
            a = β[n] / (w[n] * (μ[n] - μ[n - 1]))
            jj = linear_index(n - 1, i)
            L[ii, jj] += a
            L[ii, ii] -= a
        end
        if n < N
            a = β[n + 1] / (w[n] * (μ[n + 1] - μ[n]))
            jj = linear_index(n + 1, i)
            L[ii, jj] += a
            L[ii, ii] -= a
        end
        im = i == 1 ? naz : i - 1
        ip = i == naz ? 1 : i + 1
        L[ii, linear_index(n, im)] += q[n]
        L[ii, linear_index(n, ip)] += q[n]
        L[ii, ii] -= 2q[n]
    end
    return L, μ, w, ρ, K
end

function audit_order(N::Int)
    nd = 2N^2
    Iden = Matrix{Float64}(I, nd, nd)
    shifted, λ0 = Radiant.fokker_planck_finite_difference(
        N, "gauss-legendre-chebychev", 3, 3, Iden, Iden)
    Lradiant = shifted - λ0 * Iden
    Lind, μ, w, ρ, K = independent_glc_matrix(N)

    matrix_residual = norm(Lradiant - Lind, Inf)
    row_sum_residual = maximum(abs.(sum(Lradiant, dims=2)))

    naz = 2N
    xcoord = zeros(nd)
    ycoord = zeros(nd)
    zcoord = zeros(nd)
    points = zeros(3, nd)
    for n in 1:N, i in 1:naz
        k = i + naz * (n - 1)
        φ = π * (i - 0.5) / N
        points[:, k] = [ρ[n] * cos(φ), ρ[n] * sin(φ), μ[n]]
        xcoord[k], ycoord[k], zcoord[k] = points[:, k]
    end
    coordinate_residual = maximum([
        norm(Lradiant * xcoord + 2xcoord, Inf),
        norm(Lradiant * ycoord + 2ycoord, Inf),
        norm(Lradiant * zcoord + 2zcoord, Inf),
    ])

    defect_identity_residual = 0.0
    min_rate_defect = Inf
    max_defect = 0.0
    for i in 1:nd
        g = vec(transpose(points[:, i]) * points)
        defect = dot(Lradiant[i, :], g.^2) + 4
        jump_defect = 0.0
        for j in 1:nd
            if j != i && Lradiant[i, j] != 0
                jump_defect += Lradiant[i, j] * (g[j] - 1)^2
            end
        end
        defect_identity_residual = max(defect_identity_residual,
            abs(defect - jump_defect))
        rate = -Lradiant[i, i]
        min_rate_defect = min(min_rate_defect, rate * defect)
        max_defect = max(max_defect, defect)
    end

    status = matrix_residual ≤ TOL && row_sum_residual ≤ TOL &&
        coordinate_residual ≤ 2e-9 && defect_identity_residual ≤ 2e-9 &&
        minimum(K) > 0 && min_rate_defect ≥ 4 - 2e-8 ? "PASS" : "FAIL"

    return (
        order=N,
        directions=nd,
        lambda0=λ0,
        matrix_residual=matrix_residual,
        row_sum_residual=row_sum_residual,
        coordinate_residual=coordinate_residual,
        defect_identity_residual=defect_identity_residual,
        min_K=minimum(K),
        max_defect=max_defect,
        scaled_max_defect=N^2 * max_defect,
        min_rate_defect=min_rate_defect,
        status=status,
    )
end

orders = [2, 3, 4, 6, 8, 12, 16]
results = [audit_order(N) for N in orders]

open("radiant_glc_direct_audit.csv", "w") do io
    println(io, "order,directions,lambda0,matrix_residual,row_sum_residual,coordinate_residual,defect_identity_residual,min_K,max_defect,scaled_max_defect,min_rate_defect,status")
    for r in results
        @printf(io, "%d,%d,%.17g,%.17g,%.17g,%.17g,%.17g,%.17g,%.17g,%.17g,%.17g,%s\n",
            r.order, r.directions, r.lambda0, r.matrix_residual,
            r.row_sum_residual, r.coordinate_residual,
            r.defect_identity_residual, r.min_K, r.max_defect,
            r.scaled_max_defect, r.min_rate_defect, r.status)
    end
end

open("radiant_glc_direct_audit.md", "w") do io
    println(io, "# Direct Radiant GLC stencil audit")
    println(io)
    println(io, "- Timestamp UTC: `$(Dates.now(Dates.UTC))`")
    println(io, "- Radiant commit: `$RADIANT_COMMIT`")
    println(io, "- Julia: `$(VERSION)`")
    println(io)
    println(io, "| N | directions | lambda0 | matrix diff | row sum | coordinate residual | defect identity | min K | N^2 max defect | min(rate*defect) | status |")
    println(io, "|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|")
    for r in results
        @printf(io, "| %d | %d | %.6e | %.3e | %.3e | %.3e | %.3e | %.9f | %.9f | %.9f | %s |\n",
            r.order, r.directions, r.lambda0, r.matrix_residual,
            r.row_sum_residual, r.coordinate_residual,
            r.defect_identity_residual, r.min_K,
            r.scaled_max_defect, r.min_rate_defect, r.status)
    end
    println(io)
    println(io, "The audit calls Radiant's public GLC finite-difference constructor with identity moment transforms, removes its documented diagonal stabilization, and compares the result entry-by-entry with an independent implementation of the published formulas.")
end

for r in results
    println(r)
end

if any(r -> r.status != "PASS", results)
    error("Direct Radiant GLC audit failed")
end
