# A source-bound positivity lemma for the corrected normal matrix

8 October 2026. Independent symbolic review only. No new numerical evaluation, matrix product, solve, factorization or consumer was performed. Author-original material: CC BY-NC 4.0.

## Assumptions

H is the same self-adjoint minimum-domain operator with H >= eta I and eta > 0. Every column of the true-source trial map U = [V,q] belongs to D(H). Let G = [G_old,F] be the delivered action approximants and E = HU - G. The 68 certified column action errors give ||E|| <= sigma, where sigma_squared = sum_i B_i_squared. Let tau > 0, alpha = (1+tau)/eta, and

    beta = nu sigma_bar + (1+1/tau) sigma_squared/eta,

where nu >= ||U|| and sigma_bar >= sigma are nonnegative certified bounds.

The matrix considered here is the actual corrected normal matrix

    S_corr = alpha G*G - sym(U*G) + beta I.

The star is the Hilbert adjoint; sym(X) = (X+X*)/2. This statement does not concern S_eta = G*G - eta sym(U*G).

## Proof

For any coefficient vector z, put u = Uz, g = Gz and e = Ez. Because Hu = g+e and ||H^-1|| <= 1/eta,

    ||u|| <= (||g|| + sigma ||z||)/eta.

The real part of <u,g> is at most ||u|| ||g||. Therefore

    z* S_corr z
      >= (tau/eta)||g||^2 - (sigma/eta)||g|| ||z|| + beta||z||^2
      = (tau/eta)(||g|| - sigma||z||/(2tau))^2
        + [beta - sigma_squared/(4tau eta)]||z||^2.

Consequently

    S_corr >= m_corr I,
    m_corr = nu sigma_bar + [1 + 3/(4tau)] sigma_squared/eta.

At the frozen tau = 1/100,

    m_corr = nu68 sigma_bar68 + 76 sigma68_squared/eta.

The saved sigma68_squared is strictly positive, so this is a strictly positive exact lower-bound expression under the inherited premises. No decimal evaluation of this new expression is needed for the lemma. If a later declared model uses beta_hat >= beta, its corrected normal lower bound increases by beta_hat-beta.

## Center and interval-family distinctions

Let Sc be the symmetric rational center of an enclosing S_corr interval, with symmetric nonnegative entry radii R. Define rho = max_i sum_j R_ij. Then ||Sc-S_corr|| <= rho, and

    Sc >= (m_corr-rho) I.

Thus rho < m_corr is sufficient to certify the center positive definite, with an exact inverse-norm bound 1/(m_corr-rho). This row-loss comparison has not been evaluated in the saved68 gate or this addendum.

This center assertion must not be relabeled as positivity of every arbitrary matrix in the entire interval box. Using only the argument above, an arbitrary symmetric matrix M in that box can be as far as 2rho from the actual physical S_corr; the sufficient bound would be M >= (m_corr-2rho)I. Alternatively, prove a center lower bound separately and subtract one rho for the whole box.

## Claim boundary

The lemma establishes positivity of the actual corrected normal matrix, and can support a later center solve after its saved-radius loss is checked. It does not establish the positivity of the final 372-coordinate target I-Ucert, provide C68, make a rounded center-solve candidate an exact minimizer of the true unknown Gram objective, improve the operator threshold, or prove RH. The full deterministic consumer is still necessary.
