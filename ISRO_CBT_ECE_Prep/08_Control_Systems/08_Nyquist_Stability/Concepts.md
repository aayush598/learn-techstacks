# Nyquist Stability Criterion - Concepts

## 1. Purpose
- Determines closed-loop stability from the open-loop frequency response G(jω)H(jω).
- Handles systems with:
  - Transport delay.
  - Non-minimum phase components.
  - Poles on the imaginary axis.
- Foundation for design (gain/phase margins).

## 2. The Nyquist Plot
- A polar plot of G(jω)H(jω) as ω varies from −∞ to +∞ (or 0 to +∞ with implied symmetric).
- Real axis = Re[GH], imaginary axis = Im[GH].
- The closed curve (with the symmetric part) is the Nyquist plot/contour mapping.

## 3. Nyquist Contour (in the s-plane)
- A closed contour in the s-plane enclosing the entire **right half plane (RHP)**.
- Traversed clockwise: up the imaginary axis (ω:0→+∞), around a large semicircle to the right, back down the imaginary axis (ω:−∞→0), plus small semicircles around any poles on the imaginary axis.
- The mapping of this contour by G(s)H(s) gives the Nyquist plot.

## 4. Principle of the Argument
- As a point s traverses a closed contour in the s-plane, the number of encirclements of the origin by F(s) = (number of zeros of F inside) − (number of poles of F inside).

## 5. The Nyquist Criterion (Encirclement Criterion)
For the closed-loop system with open-loop G(s)H(s):

**Z = N + P**

Where:
- **P** = number of OPEN-LOOP poles in the RHP (poles of G(s)H(s)).
- **N** = number of counterclockwise encirclements of the point (−1, 0) by the Nyquist plot.
- **Z** = number of CLOSED-LOOP poles in the RHP.

**System is stable ⇔ Z = 0 ⇔ N = −P.**

### Sign Convention
- N positive = counterclockwise encirclements.
- N negative = clockwise encirclements.
- For closed-loop stability: encirclements of −1 must equal the number of open-loop RHP poles (in the appropriate direction).

## 6. Special Case: No Open-Loop RHP Poles (P=0)
- For a stable open-loop system (P=0): system is closed-loop stable **iff the Nyquist plot does NOT encircle −1**.

## 7. Marginal Instability (encircling boundary)
- If the Nyquist plot passes **through** −1, the closed-loop system has poles on the imaginary axis (marginal stability / sustained oscillation).

## 8. Mapping Open-Loop to Closed-Loop
- Closed-loop char. eq.: 1 + G(s)H(s) = 0.
- The function F(s) = 1 + G(s)H(s).
- Zeros of F(s) = poles of closed loop.
- Poles of F(s) = poles of open loop.
- Nyquist encirclement of −1 by GH equals encirclement of 0 by F.
- Thus encirclements of −1 indicate closed-loop RHP poles.

## 9. Handling Poles on the Imaginary Axis
- Indent the Nyquist contour around poles on the jω axis (integrators at origin) with small semicircles into the RHP.
- The mapping of these small semicircles produces arcs of infinite radius (paths at infinity) on the Nyquist plot.
- Number of such arcs = number of poles at origin (or on jω axis).

## 10. Conditionally Stable Systems
- A system is **conditionally stable** if it is stable only for a FINITE range of gain (becomes unstable for both too low and too high gain).
- On Nyquist plot: this happens when the plot crosses the negative real axis at more than one point, leading to multiple gain margin values.
- Stability requires the gain to lie between two limits (K_low < K < K_high).
- Nyquist reveals multiple −1 crossings / encirclement changes.

## 11. Gain Margin & Phase Margin from Nyquist
- **Gain margin**: 1/|GH(-1 point crossing)| — how much gain scales until −1 crossed.
  - GM (linear) = 1/|GH(jω_pc)| measured at the negative real-axis crossing.
- **Phase margin**: angle to rotate the plot so its unit circle crossing hits −1.
  - PM = 180° + ∠GH at the point where |GH|=1.

## 12. Steps to Apply Nyquist
1. Verify open-loop RHP pole count P (from G(s)H(s) poles in RHP).
2. Sketch/compute Nyquist plot (including indentation for jω poles & symmetric part).
3. Count encirclements N of −1 (direction-aware).
4. Compute Z = N + P.
5. Stable if Z = 0.

## 13. Nyquist vs Bode
- Bode: magnitude & phase separately on log scale; requires double checking stability for non-minimum phase.
- Nyquist: single plot graph, clearer for delay & non-minimum phase; count encirclements directly.

## 14. System Types & Nyquist Shape
- Type 0: plot starts at a finite point on real axis (DC gain).
- Type 1 (one integrator): starts at infinity, arcs left.
- Type 2 (two integrators): arcs with different path.
- Shape depends on pole/zero locations.

## 15. ISRO Exam Relevance
- Determine stability (count encirclements of −1).
- Compute gain/phase margins from Nyquist.
- Identify conditionally stable systems (multiple negative-real-axis crossings).
- Open-loop/closed-loop pole relationship.

## 16. Common Misconceptions
- Nyquist operates on open-loop data but decides closed-loop stability.
- Encirclement must be of point −1 (not origin).
- Direction convention matters.
- Poles on jω axis require contour indentation.

## 17. Step-by-Step Nyquist Application Checklist
1. Write open-loop G(s)H(s) and identify P (open-loop RHP poles) — including counting poles on jω axis for indentation.
2. Sketch frequency response G(jω) for ω≥0 (start point, end point, crossings).
3. Mirror for ω≤0 + add infinite arcs for jω-axis poles (integrators).
4. Form the complete closed Nyquist plot.
5. Count directed encirclements N of point (−1,0).
6. Compute Z = N + P; stable if Z=0.

## 18. Reading Margins off Nyquist
- Identify the point where the plot crosses the negative real axis: distance from origin → 1/GM.
- Identify the unit-circle crossing: angle below −180° → PM.

## 19. Nyquist for Type 0 vs Type 1
- Type 0: plot starts at real point = DC gain G(0).
- Type 1: starts at −∞ on a certain ray with infinite-radius arc (indentation for the origin pole).
- The type affects the encirclement counting around −1.

## 20. Nyquist and the Closed-Loop Poles on the Axis
- If the plot passes through −1 exactly, closed-loop pole on jω → oscillation / marginal.
- Frequency of that oscillation = ω at the crossing point.

## 21. When Nyquist is the Only Reliable Method
- Systems with pure time delay (e^{−jωT}) — infinite-order, Routh impossible.
- Non-minimum phase (RHP zeros/poles) where Bode margin sign could mislead.
- Systems with poles on the imaginary axis.

## 22. Nyquist Quick-Facts for Revision
- Open-loop data → closed-loop conclusion.
- Encircle −1, count CCW; stable when N = −P.
- Delay & RHP-handling advantage over Routh.
- Margin reading equivalent to Bode but on one contour.
