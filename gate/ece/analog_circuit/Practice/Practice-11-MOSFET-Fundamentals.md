# MOSFET Fundamentals — Practice (Learn by Solving)

> **The idea in one line:** this file teaches everything about MOSFET regions,
> equations and device behaviour through questions — solve each one, learn the
> pattern, skip the notes.
>
> **How to use:** cover the Answer/Method, solve, reveal. If you miss one, do
> the next three. Open `` `11-MOSFET-Fundamentals.md` `` or
> `32-Single-File-Cheatsheet.md` only for underlying theory.

## Concept box (what you must internalise)

- Saturation: `I_D = ½k(V_GS − V_th)² (1 + λV_DS)`, `k = μn·Cox·W/L`
- Triode: `I_D = k[(V_GS − V_th)V_DS − V_DS²/2]`
- Cutoff: `V_GS ≤ V_th`
- Region test: **saturation iff `V_DS ≥ V_GS − V_th`**
- `k` is the transconductance parameter; `k ∝ W/L`; doubling `W` doubles `k`.
- Enhancement off at `V_GS=0`; depletion on at `V_GS=0`.
- Body effect: reverse `V_BS` raises `V_th`.
- Always decide the region BEFORE writing an I_D expression.

---

## Questions

### Q1. (Easy) An NMOS has `V_th = 1 V`, `V_GS = 3 V`, `V_DS = 5 V`. Region?
**Answer:** Saturation.
**Method:** `V_GS − V_th = 2 V`; `V_DS = 5 ≥ 2` ⇒ saturation. Gate overdrive is the test, not the absolute voltage.

### Q2. (Easy) Same device with `V_DS = 1 V`. Region?
**Answer:** Triode.
**Method:** `V_DS = 1 < 2 = V_GS − V_th` ⇒ triode (channel never pinched).

### Q3. (Easy) `k = 1 mA/V²`, `V_th = 1 V`, saturation, `V_GS = 3 V`, `λ = 0`. `I_D`?
**Answer:** `½·1·(3−1)² = 2 mA`.
**Method:** `I_D = ½k(V_GS−V_th)²`; with `λ = 0`, `V_DS` does not enter.

### Q4. (Easy) Same as Q3 but `V_GS = 2.5 V`. `I_D`?
**Answer:** `½·1·(1.5)² = 1.125 mA`.
**Method:** overdrive `1.5 V`, squared, halves as `[1.5/2]² = 0.5625`.

### Q5. (Easy) PMOS: sign of `V_th`, and source terminal polarity?
**Answer:** `V_th` negative (e.g. −1 V); source is the most positive terminal; `V_GS` must go below `V_th`.
**Method:** mirror of NMOS — flip all voltages/current signs.

### Q6. (Easy) Enhancement NMOS at `V_GS = 0` conducts?
**Answer:** No — cutoff. (Depletion-mode MOS conducts at `V_GS = 0`.)
**Method:** enhancement = normally OFF; depletion = normally ON.

### Q7. (Easy) Triode device: `k = 2 mA/V²`, `V_ov = 2 V`, `V_DS = 0.5 V`. `I_D`?
**Answer:** `2[(2)(0.5) − 0.25/...] = 2[1 − 0.125] = 1.75 mA`.
**Method:** `k[V_ov·V_DS − V_DS²/2]` — the `−V_DS²/2` correction is small here.

### Q8. (Moderate) Where is the triode/saturation boundary?
**Answer:** `V_DS = V_GS − V_th` (knee/pinch-off line).
**Method:** sweep V_DS at fixed V_GS; I_D rises (triode) then flattens (saturation).

### Q9. (Moderate) Doubling W (L fixed): effect on `k` and saturation `I_D`?
**Answer:** `k` doubles ⇒ `I_D` doubles.
**Method:** `k ∝ W/L`; square law is linear in k. Basis for mirror ratios.

### Q10. (Moderate) `λ = 0.02`, `V_DS` 5 V → 10 V in saturation. `I_D` change (same bias)?
**Answer:** `(1+0.2)/(1+0.1) = 1.0909` → ~9.1% higher.
**Method:** `I_D ∝ (1+λV_DS)` — channel-length modulation.

### Q11. (Moderate) Drain tied to gate (diode-connected), `V_GS = V_DS = 2 V`, `k=1`, `λ=0`. Region and I_D?
**Answer:** Saturation (`V_DS = V_GS ≥ V_ov`); `I_D = ½·1·(2)² = 2 mA`.
**Method:** diode-connected MOS is always saturated — a standard two-terminal device.

### Q12. (Moderate) Source at +1 V, body at 0, V_GS = 2 V, nominal V_th = 1 V. What changes?
**Answer:** `V_th` increases (~1.2–1.5 V here); channel harder to form.
**Method:** `V_BS = −1 V` is reverse → body/bulk effect raises V_th. Matters in cascodes/stacks.

### Q13. (Moderate) Is the square-law current controlled by gate-to-drain or gate-to-source?
**Answer:** Gate-to-source (`V_GS`).
**Method:** source-referenced conduction; gate is infinite-impedance field plate.

### Q14. (Moderate) Two NMOS, same k: I_D of one is 4× other (both saturation, λ=0). Overdrive ratio?
**Answer:** `V_ov₂/V_ov₁ = √4 = 2`.
**Method:** `I_D ∝ V_ov²`.

### Q15. (Moderate) Triode small-V_DS resistance?
**Answer:** `r_DS(on) = 1/[k(V_GS − V_th)]`.
**Method:** for `V_DS ≪ V_ov`, `I_D ≈ k·V_ov·V_DS` ⇒ linear resistor. This is the "switch" mode.

### Q16. (Moderate) `V_DS = 0.8·(V_GS−V_th)`: describe channel.
**Answer:** Continuous (not pinched), triode-like; pinch-off begins only at `V_DS = V_ov`.
**Method:** continuous → triode; pinched at drain → saturation.

### Q17. (GATE-level) Device with `V_ov = 0.5` vs `1.0 V` same k: current ratio?
**Answer:** `0.25/1.0 = 1/4`.
**Method:** ratio of `V_ov²`; overdrive dominates the square law.

### Q18. (GATE-level) A switch (triode) and an amplifier (saturation) are both MOS. In which region is R different?
**Answer:** Switch uses triode with large `V_ov` for ~Ω's; amplifier uses saturation with high-gain channel.
**Method:** pick region by application: low-R conduction (triode) vs controlled current (saturation).

### Q19. (GATE-level) `k=0.5 mA/V²`, `V_th=1 V`, `V_GS=3`, `V_DS=2.5`, `λ=0`: region and I_D?
**Answer:** sat test `2.5 ≥ 2` yes; `I_D = ½·0.5·(2)² = 1 mA`.
**Method:** region first, then law.

### Q20. (GATE-level) `V_GS=2`, `V_DS=1`, `k=1`, `V_th=1`: region/I_D?
**Answer:** triode: `1 < 1?` boundary touches = saturation at knee; `1 = 1` ⇒ knee. Take it as saturation (`I_D = 0.5 mA`); at equality both laws give `k V_ov²/2`.
**Method:** at the knee the two laws coincide — safe to use either; state it.

### Q21. (GATE-level) Switching resistance with `V_ov = 0.5 V`, `k = 4 mA/V²`?
**Answer:** `1/(4m·0.5) = 500 Ω`.
**Method:** r_DS(on) = 1/(k·V_ov).

### Q22. (GATE-level) Increasing W/L both raises `k` AND changes... what second effect?
**Answer:** area/capacitance (parasitic C_g), affects speed; also lower r_DS(on).
**Method:** device-level trade: current vs parasitic capacitance vs switching speed.

### Q23. (GATE-level) Depletion NMOS with `V_th = −2 V`, `V_GS = 0 V`. Region/saturation?
**Answer:** `V_ov = 0 − (−2) = +2 V`; conducts; sat if `V_DS ≥ 2 V`.
**Method:** depletion devices conduct at V_GS ≤ V_th (negative threshold).

### Q24. (GATE-level) If `V_DS = −0.5 V` (drain below source) for NMOS — what happens?
**Answer:** Device symmetric: source/drain swap roles; current reverses polarity when defined by new V_DS.
**Method:** MOS is symmetric; the traditional terminal labels follow V_S ≤ V_D for NMOS.

### Q25. (GATE-level) λ increases from 0.01 to 0.03 — effect on r_o at fixed I_D?
**Answer:** r_o = 1/(λ·I_D) → 3× smaller.
**Method:** higher λ = more finite output resistance (lower r_o).

### Q26. (GATE-level) Drain current in triode with `V_DS = V_ov/2`, `k=4 mA/V²`, `V_ov=1 V`.
**Answer:** `4[1·0.5 − 0.25/2] = 4[0.5 − 0.125] = 1.5 mA`.
**Method:** triode law with corrections; don't approximate unless `V_DS≪V_ov`.

### Q27. (GATE-level) Which device parameter sets `k` in a technology? (two)
**Answer:** `μn·Cox` (process) and `W/L` (geometry).
**Method:** designers scale W/L; process fixes μn·Cox.

### Q28. (GATE-level) Body at +1 V, source at ground (NMOS) — region of V_BS and effect on V_th.
**Answer:** `V_BS = +1` forward body bias → lowers V_th slightly.
**Method:** bulk can forward-bias the body diode: keep body reverse to avoid latch-up.

### Q29. (GATE-level) Saturation I_D sensitivity to V_th mismatch `ΔV_th = 50 mV` at `V_ov = 0.5 V` — current mismatch?
**Answer:** `ΔI_D/I_D ≈ 2·ΔV_th/V_ov = 2(0.05/0.5) = 20%`.
**Method:** square law derivative `ΔI/I = 2ΔV_ov/V_ov` (small-signal sensitivity).

### Q30. (GATE-level) Triode NMOS used as a switch with `V_GS = 3 V`, `V_th = 1 V`, `k = 10 mA/V²`: R_DS(on)?
**Answer:** `1/(10m·2) = 50 Ω`.
**Method:** r_DS(on) formula; large V_ov → low on-resistance.

### Q31. (GATE-level) PMOS with `V_th = −1 V`, `V_SD = 5 V`, `V_SG = 3 V`. Region and direction?
**Answer:** `V_SG − |V_th| = 3 − 1 = 2 V`; `V_SD = 5 ≥ 2` ⇒ saturation; current source-to-drain.
**Method:** mirror the NMOS test with source-referenced voltages.

### Q32. (GATE-level) A current source built with NMOS must operate in which region?
**Answer:** Saturation (flat output characteristic = ideal source).
**Method:** r_o = 1/(λI_D) large ⇒ near-ideal current source.

### Q33. (GATE-level) Estimate `r_o` at `I_D = 2 mA`, `λ = 0.02`.
**Answer:** `1/(0.02·2m) = 25 kΩ`.
**Method:** r_o scales inversely with I_D.

---

## Trap box (exam-day killers)

- Saturation ≠ "large V_DS": test is `V_DS ≥ V_GS − V_th`.
- Triode current is NOT the square law — that is saturation only.
- Don't add λ inside the square; it multiplies.
- PMOS thresholds are negative — keep signs straight.
- Always define the region before writing an I_D law; GATE hides region traps in the loop.

## Final recall drill (do in 60 seconds)

1. Region test → `V_DS ≥ V_GS − V_th`
2. Saturation → `½k V_ov²`
3. Triode → `k[V_ov·V_DS − V_DS²/2]`
4. λ → `× (1+λV_DS)`; r_o = 1/(λI_D)
5. Body effect → raises V_th on reverse body bias
6. Switch-mode resistance → `1/(k·V_ov)`

---