# Nyquist Stability - Practice Questions

## Section A: Conceptual

**Q1.** What does the Nyquist criterion assess?
**A1.** Closed-loop stability using the open-loop frequency response G(jω)H(jω) by counting encirclements of −1.

**Q2.** State the encirclement equation Z = N + P and its meaning.
**A2.** Z=closed-loop RHP poles, N=CCW encirclements of −1, P=open-loop RHP poles. Stable if Z=0.

**Q3.** For a stable open loop (P=0), when is the closed loop stable?
**A3.** When the Nyquist plot does NOT encircle the point −1.

**Q4.** What does the Nyquist plot passing through −1 indicate?
**A4.** Closed-loop poles on the imaginary axis → marginal stability.

## Section B: Encirclement Counting / Stability

**Q5.** A Nyquist plot (P=0) encircles −1 once clockwise. Stable?
**A5.** N = −1 (clockwise). Z = N+P = −1+0 = −1 ≠ 0 → NOT stable (Z must be 0). Actually Z can't be −1; interpretation: clockwise encirclement means closed-loop RHP poles exist → unstable.

**Q6.** Plot with P=2 encircles −1 twice counterclockwise. Find Z.
**A6.** N=+2. Z = N+P = 2+... wait, for stability need N = −P? Re-derive: Z=N+P. For stable Z=0 → N=−P. With P=2, need N=−2... but here N=+2. Z=2+2=4≠0 → unstable. Hmm let me use correct convention: For clockwise contour, stable requires Z=0 → N=−P. If P=2, need N=−2 (i.e., 2 clockwise encirclements). Here N=+2 CCW → Z=4 → 4 RHP closed-loop poles → unstable.

**Q7.** P=0, plot does not encircle −1. Stable?
**A7.** Yes. Z=0.

**Q8.** P=1, plot encircles −1 once CCW. Stable?
**A8.** N=+1. Z=N+P=1+1=2≠0 → unstable. Wait—need N=−P=−1 for stability. Here N=+1, so not stable.

## Section C: GM/PM from Nyquist

**Q9.** Nyquist plot crosses negative real axis at point with |GH|=0.4. Find GM.
**A9.** GM = 1/0.4 = 2.5 (linear) = 20log10(2.5) ≈ 7.96 dB.

**Q10.** Plot crosses unit circle at angle −160° (from positive real axis). Find PM.
**A10.** PM = 180° + (−160°) = 20°.

**Q11.** If negative real axis crossing has |GH|=0.25, find GM in dB.
**A11.** GM = 1/0.25 = 4 → 20log(4) = 12.04 dB.

**Q12.** Unit circle crossing at phase −120°. PM?
**A12.** PM = 180−120 = 60°.

## Section D: Conditionally Stable Systems

**Q13.** What makes a system conditionally stable?
**A13.** The Nyquist plot crosses the negative real axis at more than one point, giving a stability region bounded on both sides by gain limits K1 < K < K2.

**Q14.** In a conditionally stable system, what happens at very low gain?
**A14.** The system can become unstable (encirclement condition changes), i.e., reducing gain too much destroys stability.

**Q15.** Why does a conditionally stable system have multiple gain margins?
**A15.** Because the plot crosses −1 in several places as gain scales, producing several critical gains.

## Section E: Integrators/Poles at Origin

**Q16.** A type 1 system (one pole at origin) — how is the Nyquist contour indented and what does it map to on the plot?
**A16.** Indent around origin with small RHP semicircle; maps to an infinite-radius arc on the Nyquist plot (connecting the ±∞ branches).

**Q17.** For G(s)=K/[s(s+2)(s+4)], determine total number of infinite arcs and reason about start.
**A17.** One pole at origin → one infinite-radius arc on the left of the axis. As ω→0, |GH|→ ∞.

## Section F: ISRO-Style

**Q18.** The open-loop TF has P=0 and its Nyquist plot encloses −1 once in clockwise direction. Number of closed-loop RHP poles?
**A18.** N=−1. Z=N+P=−1 → indicates 1 RHP pole (magnitude) → closed loop unstable with 1 RHP pole.

**Q19.** Given G(s)H(s) with open-loop poles both in LHP (P=0), gain margin = +6 dB, phase margin = +45°. Stable?
**A19.** Yes. Positive GM and PM → no encirclement of −1 → stable.

**Q20.** A system has a Nyquist plot passing through −1. What gain change would you make and what happens?
**A20.** It's marginally stable. Scaling gain slightly will either encircle (unstable) or stop enclosing (stable). Gain must be tuned.

**Q21.** For a type 2 system (two poles at origin), how many 360° infinite arcs appear on the Nyquist plot?
**A21.** The two integrators produce a characteristic path with the plot starting at +∞ real on one side and going around; effectively the double pole at origin creates a large arc. For 2 integrators the plot starts at +∞ and rotates clockwise before coming in.

**Q22.** Determine the number of open-loop RHP poles given the plot must encircle −1 twice (CCW) for closed-loop stability.
**A22.** For stability Z=0 → N=−P. If N=+2 CCW needed... With P>0, need N=P (CCW) since N=−P is negative... Standard: for the chosen contour, Z=N+P, stable when N=−P. If the plot CCW-encircles −1 twice (N=+2), then for stability need... Actually for P=2 (2 RHP OL poles), a stabilizing plot encloses −1 with net CCW encirclement = P=2 region → N here → then Z=2+P... We take: stable requires N = −P. So N=+2 → −P=2 → P=−2 impossible. 

## Section G: Mapping & Misc

**Q23.** Explain why encirclements of −1 by GH correspond to encirclements of 0 by F=1+GH.
**A23.** Translating the plot by +1: point −1 maps to 0, preserving encirclement structure.

**Q24.** Which point must be encircled for the Nyquist criterion—origin or −1?
**A24.** Point −1 (= −1 + 0j) for the GH plot; equivalently origin for the 1+GH plot.

**Q25.** A system's Nyquist plot has GM=+∞. What does this imply about phase?
**A25.** Phase never reaches −180°, so no negative-real-axis crossing; infinite gain margin (e.g., low-order or first-order type systems).

## Common Mistakes
1. Encircling the wrong point (origin instead of −1).
2. Getting the sign/direction convention wrong.
3. Forgetting P (open-loop RHP poles) count.
4. Not indenting contour for jω-axis poles.
5. Confusing Z=N+P sign interpretation.

## Section H: Encirclement Practice (Sign-Convention Care)

**Q26.** P=1 (one open-loop RHP pole), and the Nyquist plot does not encircle −1. Determine closed-loop stability.
**A26.** N=0. Z=N+P=0+1=1 ≠ 0 → unstable (one closed-loop RHP pole).

**Q27.** P=1 and plot encircles −1 once CCW. Find Z.
**A27.** N=+1. Z=1+1=2 → unstable (two RHP poles). Wait — correct: Z=N+P=1+1=2≠0 → unstable.

**Q28.** Find required encirclements for a P=1 stable design.
**A28.** Need Z=0 → N=−P=−1 → exactly ONE clockwise encirclement of −1 (for this convention).

**Q29.** A plot with P=2 encircles −1 twice clockwise. Z?
**A29.** N=−2. Z=N+P=−2+2=0 → stable ✓.

## Section I: Margin and Delay Nyquist Checks

**Q30.** A delay of T=0.1 s is added at ω=20 rad/s. What phase does the delay contribute?
**A30.** −ωT = −20·0.1 = −2 rad ≈ −114.6°.

**Q31.** If that delay makes the plot cross −1, what does it imply?
**A31.** Closed-loop becomes unstable/marginal — delay reduces stability margin.

**Q32.** How does a pure delay change the Nyquist magnitude?
**A32.** Not at all (|e^{−jωT}|=1) — only phase.

## Section J: Nyquist Quick Numericals
**Q33.** Type 1 G(s)=K/[s(s+2)]. At what ω does the negative-real axis crossing occur if it occurs? (Given the second-order poles, check.)
**A33.** Phase = −90° − atan(ω/2). For −180°, atan(ω/2)=90°→ω→∞; no finite crossing → GM=+∞.

**Q34.** For the same system, PM at K=4 with ω_gc≈2.
**A34.** Phase at ω=2: −90−45=−135°. PM=45°.

**Q35.** Interpret: plot crosses negative real axis at (−0.5,0). GM?
**A35.** GM=1/0.5=2 (linear)=6.02 dB.

## Key Convention Reminder Table
| P | Stable needs N | Interpretation |
|---|---|---|
| 0 | 0 | no encirclement |
| 1 | −1 | 1 CW |
| 2 | −2 | 2 CW |
