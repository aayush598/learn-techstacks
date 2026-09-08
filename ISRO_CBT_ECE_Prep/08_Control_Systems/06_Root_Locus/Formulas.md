# Root Locus - Formulas

## 1. Fundamental Equation
1 + K·G(s)H(s) = 0   (closed-loop characteristic equation)
⇒ K·G(s)H(s) = -1

## 2. Angle Condition
∠G(s)H(s) = (2k+1)·180°,  k = 0,±1,±2,...

For G(s)H(s) = K·Π(s+zᵢ)/Π(s+pⱼ):
Σ∠(s+zᵢ) − Σ∠(s+pⱼ) = (2k+1)·180°

## 3. Magnitude Condition
|K·G(s)H(s)| = 1
K = 1/|G(s)H(s)|

## 4. Number of Branches
= n (number of open-loop poles).

## 5. Real-Axis Segments
A point on real axis is on the locus if the count of open-loop poles + zeros to its RIGHT is odd.

## 6. Asymptotes
### Number
N = n − m

### Angles
θ_k = [(2k+1)·180°]/(n−m),  k = 0, 1, ..., (n−m−1)

### Centroid (real-axis intersection)
σ = [Σ(poles) − Σ(zeros)] / (n − m)

## 7. Breakaway / Break-in Points
Solve dK/ds = 0, where:
K = −1/[G(s)H(s)]

On real axis, breakaway/break-in occur at real roots of dK/ds = 0 where the point lies on the locus.

### Alternative
dK/ds = 0 ⇔ d[1/(G(s)H(s))]/ds = 0 (with sign).

## 8. Angle of Departure (approx. true formulas for standard unity-feedback)
From pole p_j:
θ_dep = 180° + Σ(angles from zeros to p_j) − Σ(angles from other poles to p_j)

## 9. Angle of Arrival
At zero z_i:
θ_arr = 180° − Σ(angles from poles to z_i) + Σ(angles from other zeros to z_i)

## 10. Imaginary Axis Crossing
Substitute s = jω:
1 + K·G(jω)H(jω) = 0
Separate real & imaginary parts:
Re[1+KG(jω)H(jω)] = 0
Im[1+KG(jω)H(jω)] = 0
Solve for ω and K.

### Using Routh
- Find K_crit from Routh (first column → 0).
- Substitute K=K_crit in auxiliary equation → solve for ω.

## 11. Gain K at a Point on Locus
K = Π(distances from s to poles) / Π(distances from s to zeros)

Distances measured geometrically along the s-plane.

## 12. Second-Order Characteristic Parameters (for design)
For closed-loop poles at s = −σ ± jω_d:
σ = ζω_n,  ω_d = ω_n·√(1−ζ²)
ζ = cos(angle the pole vector makes with negative real axis)
ω_n = √(σ² + ω_d²)

## 13. Angle Contribution from Poles/Zeros (calculation)
From a point s₀ to a pole p: angle = ∠(s₀ + p) = atan2(Im(s₀), Re(s₀)+p).
Angles measured counterclockwise from positive real axis.

## Formula Table
| Parameter | Formula |
|---|---|
| Asymptote angle | (2k+1)·180°/(n−m) |
| Centroid | (ΣP−ΣZ)/(n−m) |
| Breakaway | dK/ds=0 |
| Departure angle | 180°+Σzeros−Σpoles |
| Arrival angle | 180°−Σpoles+Σzeros |
| Crossing | s=jω into char eq |
| K at point | Π|pole dist|/Π|zero dist| |
| Damping | ζ=cos(angle) |
| ω_n | √(σ²+ω_d²) |

## Useful Observations
- Number of branches ending at infinity = n−m.
- Asymptote angles sum determined evenly; for n−m=2 they are at ±90°.
- For n−m=1, one asymptote along real axis (180°).
- Breakaway occurs where locus diverges from real axis; typically between two poles.

## 14. Computing Gain K for a Given Damping Ratio (design formula)
To place a pole on a 100%-settling design line at damping ζ:
- Draw a radial line from origin at angle θ=cos⁻¹(ζ) from the negative real axis.
- Find locus intersection; compute K from the distance ratios.

## 15. Angle Sum at a Test Point (magnitude formula re-expressed)
At a point s₀ on the locus with poles pᵢ and zeros zⱼ:
Π|s₀+pᵢ| / Π|s₀+zⱼ| = K
(distances measured in s-plane; this is the magnitude form of K·GH=−1.)

## 16. Number of Loci Reaching Each Zero
Each of the m finite zeros attracts a branch; the remaining (n−m) branches go to infinity along asymptotes.

## 17. Breakaway/break-in with Saddle Points
A breakaway/break-in point is where ∂K/∂s = 0. On the real axis within a locus segment, the value of K there is real and the point is where branches meet.

## 18. Imaginary-Axis Crossing Via Magnitude
Once ω at the crossing is found (via real/imag splitting), the gain is:
K_crit = Π|jω + pᵢ| / Π|jω + zⱼ| (product of distances).

## 19. Root Locus vs Characteristic Equation Equivalence
Every point on the root locus satisfies 1+KG(s)H(s)=0 for some real positive K. The locus is exactly the set of such s.

## 20. Quick Reference Magnitudes to Memorize
- n−m=2 → asymptotes ±90°.
- n−m=3 → 60°,180°,300°.
- n−m=4 → 45°,135°,225°,315°.
- Centroid always lies on the real axis.
