# MOSFET Biasing — Practice (Learn by Solving)

> **The idea in one line:** learn how to set a stable operating point for MOSFET
> amplifiers by solving — divider bias, drain feedback, current-source bias, and
> the always-critical saturation check.
>
> **How to use:** solve each before revealing. Miss one → do the next three.
> Theory lives in `` `12-MOSFET-Biasing.md` ``.

## Concept box (what you must internalise)

- Gate current = 0 ⇒ gate voltage is set purely by the divider (exact, unlike BJT).
- `V_GS = V_G − I_D·R_S` (source end).
- Saturation: `I_D = ½k(V_GS − V_th)² (1+λV_DS)` — solve the quadratic, keep the physical root.
- Verify after solving: `V_DS ≥ V_GS − V_th`.
- Drain feedback: `V_G = V_D`, restores stability by negative feedback.

---

## Questions

### Q1. (Easy) Divider bias: `V_DD = 10`, R1 = 60 k, R2 = 20 k. `V_G`?
**Answer:** `10·20/80 = 2.5 V`.
**Method:** no gate current ⇒ `V_G = V_DD·R2/(R1+R2)`.

### Q2. (Easy) Source resistor `R_S = 1 k`. If `I_D = 1 mA`, what are `V_S` and `V_GS` (V_G = 2.5 V)?
**Answer:** `V_S = 1 V`; `V_GS = 2.5 − 1 = 1.5 V`.
**Method:** `V_GS = V_G − I_D·R_S`.

### Q3. (Easy) The gate current of a MOSFET in steady state is?
**Answer:** 0 (ideal); tiny leakage in practice.
**Method:** insulated gate ⇒ no DC path back to the divider.

### Q4. (Easy) `V_GS − V_th = 0.5 V`, `k=2 mA/V²`, `λ=0`. Saturation `I_D`?
**Answer:** `½·2·0.25 = 0.25 mA`.
**Method:** square law with V_ov given.

### Q5. (Moderate) Divider: `V_DD=12`, R1=75 k, R2=25 k, R_S=2 k, k=0.5 mA/V², V_th=1 V. Guess I_D by assuming V_GS ≈ 2 V.
**Answer:** `V_G=3 V`; if `V_GS=2`, then `V_S=1 V`, `I_D=0.5 mA`. Check with law: `½·0.5·(1)²=0.25 mA` → not consistent; true I_D is between; solve properly.
**Method:** use the guess only to bracket; then exact quadratic.

### Q6. (Moderate) Same circuit — write the exact quadratic in `I_D`.
**Answer:** `I_D = 0.5·0.5·(3 − 2·I_D − 1)² = 0.25(2 − 2 I_D)²` with I_D in mA.
**Method:** `V_GS = V_G − I_D·R_S = 3 − 2 I_D`; set `I_D = ½k(V_GS − V_th)²`.

### Q7. (Moderate) Solve Q6 (I_D in mA).
**Answer:** `I_D = 0.25(2 − 2I_D)² ⇒ I_D = 1 − 2I_D + I_D² ⇒ I_D² − 3I_D + 1 = 0 ⇒ I_D = (3 ± √5)/2 = 2.618 or 0.382`; physical root `0.382 mA` (other root gives `V_GS = 2.236 < V_th` fail? verify). Valid root `I_D = 0.382 mA`.
**Method:** keep the root where `V_GS > V_th` and circuit ends in a real region; the second is extraneous.

### Q8. (Moderate) Verify Q7's Q-point, `R_D = 4 k`, `V_DD = 12`.
**Answer:** `V_S = 0.382·2 = 0.764 V`; `V_GS = 3 − 0.764 = 2.236 V (+1 = 2.236? V_ov=1.236√)`. Check: `I_D=0.382`, `V_DS = 12 − 0.382(4+2) = 12 − 2.29 = 9.71 V`; `V_ov = 2.236−1=1.236`; sat since `9.71 ≥ 1.236` ✓.
**Method:** always run the region test after solving.

### Q9. (Moderate) What makes divider bias stable against k and V_th spread?
**Answer:** R_S degeneration: V_GS = V_G − I_D·R_S gives negative feedback (bigger I_D → bigger V_S → smaller V_GS).
**Method:** the larger R_S·I_D relative to V_G, the more stable.

### Q10. (Moderate) Drain-feedback: R_G from drain to gate, R_D = 2 k, V_DD = 8, k = 1, V_th = 1. If `I_D = 1.5 mA`, find V_G, V_GS, and consistency.
**Answer:** `V_D = 8 − 1.5·2 = 5 V = V_G`; `V_GS = 5 V`; square law would give `½·1·(5−1)² = 8 mA ≠ 1.5` ⇒ inconsistent, actual Q is different.
**Method:** drain feedback forces V_G = V_D; solve the self-consistent equation rather than guessing I_D.

### Q11. (Moderate) Write the self-consistent equation for drain feedback, R_D=2k, V_DD=8, k=1, V_th=1.
**Answer:** `V_GS = 8 − 2I_D`; `I_D = ½(8 − 2I_D − 1)²`.
**Method:** one equation, one unknown (I_D); solve by inspection/quadratic.

### Q12. (GATE-level) Solve Q11.
**Answer:** `I_D = 0.5(7 − 2I_D)²`; let x=I_D: `x=0.5(49−28x+4x²) ⇒ 0 = 2x²−15x+24.5` ⇒ `x=(15±√(225−196))/4=(15±5.385)/4 = 5.10 or 2.40 mA`. Check roots: x=5.10 → V_GS=8−10.2=−2.2 (cutoff!) reject; x=2.40 mA → V_GS = 8−4.8=3.2 V, V_ov=2.2, I=0.5·4.84=2.42 ✓; `V_DS=V_GS=3.2 V ≥ 2.2` sat ✓.
**Method:** solve, then physically validate the root.

### Q13. (Moderate) With a current-source bias `I_D = 1 mA` and `R_D = 5 k` from 12 V, what is `V_D`?
**Answer:** `12 − 5 = 7 V`.
**Method:** current source sets I_D exactly; V_D = V_DD − I_D·R_D.

### Q14. (GATE-level) To place the Q-point optimally at `V_DS = V_DD/2` with `R_D`, `I_D`?
**Answer:** choose `I_D = V_DD/(2·R_D)`.
**Method:** midpoint for max symmetrical swing.

### Q15. (GATE-level) Divider: `V_DD=15`, R1=90k, R2=30k, R_S=2.5k, R_D=3k, k=0.8, V_th=1.2. Find V_G.
**Answer:** `15·30/120 = 3.75 V`.
**Method:** gate resistor-only divider.

### Q16. (GATE-level) Same: exact I_D (mA).
**Answer:** `V_GS = 3.75 − 2.5I_D`; `I_D = 0.4(3.75 − 2.5 I_D − 1.2)² = 0.4(2.55 − 2.5 I_D)²`. Let x=I_D: `x = 0.4(2.55−2.5x)²`. Try x=0.5: 0.4(1.3)²=0.676; x=0.6: 0.4(1.05)²=0.441; x=0.55: 0.4(1.175)²=0.552 → ~0.55 mA. `V_GS=2.375`, V_ov=1.175, `I=0.4·1.38=0.552`.
**Answer (final): `I_D ≈ 0.55 mA`.**
**Method:** iterate or solve quadratic; keep root with valid V_GS.

### Q17. (Moderate) MOSFET gate DC leakage in a divider — the divider's output changes how?
**Answer:** negligible (sub pA) — divider stays exact; BJT base current would load it.
**Method:** the "MOSFET bias is easier than BJT" advantage = no base current.

### Q18. (Moderate) The bias point's dependence on k — use the transconductance-to-gm form `I_D = gm·V_ov/2`.
**Answer:** gm at Q = √(2k·I_D); bias at fixed `V_G, R_S` yields I_D that tracks k, but degeneration reduces sensitivity.
**Method:** sensitivity `(ΔI_D/I_D)/(Δk/k) ≈ 1/(1+gm·R_S)`.

### Q19. (GATE-level) Compute gm·R_S degeneration factor: `I_D=0.5 mA`, gm=2 mA/V, R_S=2k.
**Answer:** `gm·R_S = 4` ⇒ k change of 10% shifts I_D by ~2%.
**Method:** degeneration factor `1+gm R_S`.

### Q20. (GATE-level) If R_S→∞ (ideal source bias), sensitivity to k?
**Answer:** →0: I_D is pinned by the current source, not the device.
**Method:** source-bias is the most stable; cost: extra bias network/C.

### Q21. (Moderate) Vth mismatch (±50 mV) effect on I_D with degeneration `gm·R_S=4`?
**Answer:** mismatch `ΔV_th` acts at the gate; `ΔI_D = gm·ΔV_th/(1+gm R_S)`; with `ΔV_th=50 mV, gm=2m`: `ΔI_D = (2m·0.05)/5 = 0.02 mA = ±4%` of 0.5mA.
**Method:** feedback reduces parameter sensitivity by `(1+gmR_S)`.

### Q22. (Moderate) Why not use too large R_S / R_D in low V_DD designs?
**Answer:** V_DS headroom shrinks; can force triode/cutoff.
**Method:** budget V_DD across R_D, R_S and V_DS.

### Q23. (GATE-level) Choose R_S so Q sits at `V_GS = 1.6 V` with I_D=1 mA: what's needed given V_G=3.2 V?
**Answer:** `V_S = 3.2 − 1.6 = 1.6 V`, `R_S = 1.6/1 m = 1.6 kΩ`.
**Method:** design from V_GS target → V_S → R_S.

### Q24. (GATE-level) Two-stage level: after divider, R_S is bypassed by C_S. Midband effects of C_S are...?
**Answer:** shorts R_S at AC → gain rises from degeneration-limited to `−gm·R_D`.
**Method:** bypass cap restores the high gain at mid/high frequencies.

### Q25. (GATE-level) The capacitor from gate to ground (if present) sets what?
**Answer:** an input low-pass pole with the Thevenin divider R.
**Method:** AC coupling / bandwidth — redesign C for the wanted f_L or f_H.

### Q26. (Moderate) Depletion-mode NMOS (`V_th = −3 V`, k=1) with R_S=2k, R_D=4k, V_DD=15, V_G=0 (short to ground).
**Answer:** `V_GS = 0 − 2I_D`; sat law `I_D = 0.5(0−2I_D+3)² = 0.5(3−2I_D)²`. Try I_D=0.5: 0.5(2)²=2; I_D=1: 0.5(1)²=0.5 → root ~1; check I_D=1: `0.5(1)²=0.5 ≠1`. I_D=0.75: 0.5(1.5)²=1.125. I_D=0.67: 0.5(1.66)²=1.38. I_D=0.6: 0.5(1.8)²=1.62. I_D=0.8: 0.5(1.4)²=0.98 ⇒ ~0.8 mA; V_GS=0−1.6=−1.6 V.
**Answer (needs a self-consistent root): I_D ≈ 0.8 mA, V_GS ≈ −1.6 V; V_DS = 15 − 0.8·6 = 10.2 V.**
**Method:** depletion conducts at V_GS < 0; treat with the same square law.

### Q27. (GATE-level) What bias topology guarantees I_D independent of device for a first-order? (name it)
**Answer:** current-source/sink bias (or very large R_S degeneration).
**Method:** last-line-of-defense against process corners.

### Q28. (GATE-level) Diode-connected load (`I_D` mirrored) with divider — why is a diode-connected PMOS a good mirror load?
**Answer:** V_GS_PMOS tracks I_D; gives a self-biased reference (bandgap-like), stable over k, V_th.
**Method:** the mirror self-adjusts to process.

### Q29. (Easy) `R_S=0` — V_GS equals?
**Answer:** V_G exactly.
**Method:** no source degeneration → gate voltage directly biases V_GS.

### Q30. (GATE-level) With `R_S=0`, why is bias unstable for constant-`V_G` design?
**Answer:** any V_th/k shift moves I_D by `ΔI_D = gm·ΔV_th` fully — no feedback to cancel it.
**Method:** you've thrown away the stabilization R_S provides.

### Q31. (GATE-level) Design I_D target 0.5 mA in a divider with V_DD=5, k=1, V_th=1, choose V_G and R_S (V_GS = 1.5 V target)
**Answer:** need `V_GS = 1.5`; pick R1=40k, R2=20k ⇒ V_G=1.667; `V_S = 1.667−1.5 = 0.167 V`; `R_S = 0.167/0.5m = 333 Ω`. Check: `I_D=0.5·(1.5−1)²=0.125 mA` — inconsistent! Recover: V_ov target from I_D=0.5 ⇒ V_ov=1 ⇒ V_GS=2; then V_G→V_S: V_S=V_G−2=2.4 (V_G=4.4 needs R2=R1·(V_G/(V_DD−V_G))); pick R2=10k→R1=10k·(4.4/0.6)=73.3k; `R_S=V_S/I_D=2.4/0.5m=4.8kΩ`.
**Answer: R1≈73 k, R2=10 k, R_S≈4.8 k.**
**Method:** design loop: I_D→V_ov→V_GS→V_S→R_S, then divider to set V_G, then verify by full solve.

---

## Trap box (exam-day killers)

- Gate current is zero — divider is exact (don't "load" it with β).
- Always test `V_DS ≥ V_GS − V_th` after solving; GATE plants inconsistency traps.
- Quadratic roots: discard the unphysical one — check V_GS > V_th and saturation.
- R_S both biases AND degrades gain (unless bypassed).
- Depletion-mode devices conduct at V_GS = 0.

## Final recall drill (do in 60 seconds)

1. V_G divider → `V_DD·R2/(R1+R2)`
2. V_GS → `V_G − I_D·R_S`
3. Square law → solve `I_D = ½k(V_ov)²`
4. Verify → `V_DS ≥ V_ov`
5. Degeneration factor → `1 + gm·R_S`

---