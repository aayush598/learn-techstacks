# Root Locus - Concepts

## 1. Definition
- The **root locus** is a plot of the locations of closed-loop poles in the s-plane as the open-loop gain K varies from 0 to ∞.
- It shows how poles move (trajectories) with gain.
- Root locus of `1 + K·G(s)H(s) = 0` (characteristic equation) as K varies.

## 2. Condition for Points on Root Locus
For a point s to be on the root locus, it must satisfy:
1. **Magnitude condition**: |K·G(s)H(s)| = 1.
2. **Angle condition**: ∠G(s)H(s) = 180° (for the standard unity-feedback negative system).

### Angle condition (defines the locus)
For a given s, sum of angles from zeros minus sum of angles from poles = 180°(2k+1).

## 3. Rules for Construction (Standard Procedure)

### Rule 1: Number of branches
Number of branches = number of open-loop poles (n).

### Rule 2: Symmetry
Root locus is symmetric about the real axis.

### Rule 3: Real-axis segments
On the real axis, a point lies on the root locus if the number of open-loop poles and zeros to its RIGHT is **odd**.

### Rule 4: Start and end points
- Branches start at open-loop poles (K=0).
- Branches end at open-loop zeros (K=∞). If m < n, the remaining (n-m) branches end at infinity.

### Rule 5: Asymptotes
- Number of asymptotes = n - m.
- Angle of asymptotes: θ = (2k+1)·180°/(n-m), for k = 0,1,...,(n-m-1).
- Centroid (intersection of asymptotes on real axis):
  σ = (ΣP - ΣZ)/(n - m)
  where ΣP = sum of poles, ΣZ = sum of zeros.

### Rule 6: Breakaway / Break-in Points
- **Breakaway point**: where two branches leave the real axis.
- **Break-in point**: where two branches return to the real axis.
- Found by solving dK/ds = 0 (or roots of 1/(1+KG)=0 derivative).
- Common method: points on real axis where the root locus exists and dK/ds = 0.

### Rule 7: Angle of Departure (from complex poles)
Angle of departure from a pole p:
θ_dep = 180° - (Σ angles from other poles) + (Σ angles from zeros to pole).

### Rule 8: Angle of Arrival (at complex zeros)
Angle of arrival at a zero z:
θ_arr = Σ angles from poles - Σ angles from other zeros - 180°.

### Rule 9: Imaginary axis crossing
Find point where locus crosses the jω axis (marginal stability).
- Substitute s = jω into characteristic equation.
- Solve for ω and K (use Routh for K at margin, then ω from auxiliary equation, or set real/imag parts to zero).

### Rule 10: Gain at any point
K = 1/|G(s)H(s)| evaluated at the point: product of lengths from poles / product of lengths from zeros.

## 4. Magnitude of Gain K
At a point s on the locus:
K = (product of distances from s to poles) / (product of distances from s to zeros).

## 5. Angle of Departure/Arrival Formulas (detailed)
For open-loop TF G(s)H(s) = K·(s+z₁).../[(s+p₁)...]:
- Angle from pole p_k to point s: ∠(s+p_k).
- Departure from pole p_k:
  θ_d = 180° − Σ(angles from other poles) + Σ(angles from zeros).

## 6. Imaginary Axis Crossing in Detail
- Set s = jω in char. eq. 1+KG(s)H(s)=0.
- Separate real and imaginary parts.
- Solve simultaneous equations for ω (frequency of oscillation) and K (gain at margin).
- Alternatively: use Routh to find K_crit, then auxiliary equation for ω.

## 7. Gain Calculation for Desired Pole Locations
- Place poles at desired ζ, ω_n via root locus.
- K at a point = product of pole-distances / product of zero-distances.

## 8. Shape of Locus for Common Systems
- First order: locus is a straight rayon.
- Second order (two real poles): breakaway point midway, branches go to ±∞ at ±90°.
- Complex poles: locus arcs from the complex poles toward asymptotes.
- Extra zeros pull locus toward them.

## 9. Effect of Adding Poles / Zeros
- **Adding a pole**: pushes root locus to the right (destabilizing), reduces stability margin.
- **Adding a zero**: pulls root locus to the left (stabilizing), adds phase lead.
- Used in compensator design (lead compensation adds a zero).

## 10. Root Locus and Stability
- Portion of locus in LHP → stable.
- Crossing jω axis → marginal stability.
- Portion in RHP → unstable.
- The gain K at the jω crossing is the stability limit.

## 11. Stability Margin from Root Locus
- The gain range for stability is read from the jω-axis crossing gains.
- Damping ratio from radial line: ζ = cos(angle of pole from origin).

## 12. ISRO Exam Relevance
- Determine crossing of imaginary axis.
- Identify breakaway points.
- Compute K for specified damping or pole location.
- Identify asymptote angles and centroid.
