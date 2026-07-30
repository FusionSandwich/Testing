using LinearAlgebra

"""
Validate an overdetermined AFP shared-edge balance system.

Returns the pseudoinverse solution together with diagnostics that distinguish:
1. full column rank;
2. compatibility of `Gamma * gamma = Q`;
3. nonnegativity/monotonicity of the edge conductances.
"""
function validate_afp_balance_system(
    Gamma::AbstractMatrix,
    Q::AbstractVector;
    compatibility_tolerance::Real = 1.0e-10,
    positivity_tolerance::Real = 1.0e-12,
)
    size(Gamma, 1) == length(Q) || throw(DimensionMismatch(
        "Gamma has $(size(Gamma, 1)) rows but Q has length $(length(Q))"
    ))

    gamma = pinv(Gamma) * Q
    qscale = max(norm(Q), 1.0)
    compatibility_residual = norm(Gamma * gamma - Q) / qscale
    minimum_conductance = isempty(gamma) ? Inf : minimum(gamma)
    numerical_rank = rank(Gamma)
    full_column_rank = numerical_rank == size(Gamma, 2)
    compatible = compatibility_residual <= compatibility_tolerance
    monotone = minimum_conductance >= -positivity_tolerance

    return (
        gamma = gamma,
        numerical_rank = numerical_rank,
        full_column_rank = full_column_rank,
        compatibility_residual = compatibility_residual,
        compatible = compatible,
        minimum_conductance = minimum_conductance,
        monotone = monotone,
    )
end
