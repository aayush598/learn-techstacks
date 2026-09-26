# MOSFET Amplifiers — Practice (Learn by Solving)

> **The idea in one line:** learn every MOS amplifier configuration (CS, CG, CD,
> cascode, active load) by solving — gain, input/output resistance, phase,
> degeneration, and Miller effects.
>
> **How to use:** solve each before revealing. Theory in `` `14-MOSFET-Amplifiers.md` ``.

## Concept box (what you must internalise)

- CS: `A_v = −gm(R_D∥R_L)`, R_in = R_G, R_out = R_D — inverts
- CS with source R_S (unbypassed): `A_v ≈ −R_D/R_S` when gm·R_S≫1
- CG: `+gm(R_D∥R_L)`, R_in ≈ 1/gm, R_out = R_D — non-inverting
- CD (source follower): `A_v ≈ 1`, R_out ≈ 1/gm, R_in = R_G
- Active load: `A_v = −gm·r_o` (or −gm1/gm2 with diode load)
- Cascode = CS + CG: keeps gain, kills Miller.

---

## Questions

### Q1. (Easy) CS with `gm=2 mA/V`, `R_D=4 k`, no load. Gain?
**Answer:** `−2m·4k = −8`.
**Method:** A_v = −gm·R_D (no R_L).

### Q2. (Easy) Same stage loaded by 4 k: gain?
**Answer:** `−gm(4k∥4k) = −2m·2k = −4`.
**Method:** R_eff = R_D∥R_L.

### Q3. (Easy) CS: sign of the gain and what that means for output phase?
**Answer:** negative; output is 180° out of phase with the gate signal.
**Method:** inverting configuration.

### Q4. (Easy) CG stage gain sign?
**Answer:** positive (non-inverting), `+gm·R_eff`.
**Method:** source input, drain output.

### Q5. (Moderate) CS, `R_S` unbypassed (1k), gm=2m, R_D=3k. Gain?
**Answer:** `−2m·3k/(1+2) = −2`.
**Method:** degeneration `1+gm·R_S` denominator.

### Q6. (Moderate) When is `A_v ≈ −R_D/R_S` valid for the CS?
**Answer:** when `gm·R_S ≫ 1`.
**Method:** large degeneration → ratio of resistors, immune to gm.

### Q7. (Moderate) CS input resistance with gate divider R1,R2?
**Answer:** `R1∥R2` (gate never loads it).
**Method:** R_in = R_G exactly.

### Q8. (Moderate) CS output resistance with only R_D (λ=0)?
**Answer:** `R_D`.
**Method:** no r_o in first-order.

### Q9. (Moderate) Source follower: gm=2m, R_S=1k. Gain?
**Answer:** `1k/(1k + 1/2m) = 1/(1+0.5) = 0.67`.
**Method:** A_v = R_S/(R_S + 1/gm).

### Q10. (GATE-level) Source follower: gm=1m, R_S=1m? pick practical value gm=10m, R_S=1k.
**Answer:** `1k/(1k+0.1k) = 0.909`.
**Method:** high-gm MOS follows better (near 1).

### Q11. (GATE-level) CD output resistance?
**Answer:** `1/gm` (e.g. 2m → 500 Ω).
**Method:** looking from source, the source drives through 1/gm.

### Q12. (GATE-level) Which MOS stage(s) show the Miller effect? Which don't?
**Answer:** CS (inverting) suffers it; CG and CD (source follower) avoid because the fed-back node isn't inverted or huge.
**Method:** Miller needs inverting gain between input and output.

### Q13. (GATE-level) Cascode: identify the stages and its purpose.
**Answer:** CS (gm1) stacked inside CG (gm2). CS keeps transconductance, CG provides low R at the drain to suppress Miller and raises output impedance.
**Method:** gain `≈ gm1·(gm2·r_o1·r_o2)`, huge R_out, gun-shot GATE topic.

### Q14. (GATE-level) CG input resistance shortcut?
**Answer:** `1/gm` (plus r_o/(A) terms when asked precisely).
**Method:** source port → low impedance follower input.

### Q15. (GATE-level) CS with active load (PMOS mirror): gain?
**Answer:** `−gm1·(r_o1∥r_o2)` — the classic "gm·r_o" stage.
**Method:** active load replaces R_D with a mirror's high r_o.

### Q16. (Moderate) CS with diode-connected PMOS load: gain?
**Answer:** `−gm_N/gm_P` (ratio; ~−1 to −few).
**Method:** load R_eq = 1/gm_P.

### Q17. (GATE-level) A CS with both R_D and r_o: full gain?
**Answer:** `−gm(R_D∥r_o)`.
**Method:** add r_o in parallel whenever λ≠0.

### Q18. (GATE-level) Design a CS for gain −10 with gm=2m: needed R_D (λ=0, no load)?
**Answer:** `R_D = 10/2m = 5 kΩ`.
**Method:** scale R_D linearly with gm.

### Q19. (GATE-level) Same but loaded by 10k: needed R_D?
**Answer:** `R_eff = 5k → 1/R_D + 1/10k = 1/5k → 1/R_D = 1/5k − 1/10k = 1/10k → R_D = 10 kΩ`.
**Method:** include load in R_eff.

### Q20. (Moderate) Why is a CS more loaded by a following low-R stage? Which fix?
**Answer:** gain falls; add a source follower (buffer) between.
**Method:** CD isolates the load (high R_in) and drives it at low R_out.

### Q21. (GATE-level) Source-follower driving a 50-Ω load—practical R_out including r_o?
**Answer:** `(1/gm)∥r_o` ≈ `(500Ω)∥50k` ~ `495Ω`; still too large vs 50→ add another stage or power follower; conceptually: R_out≈1/gm when gm large.
**Method:** source followers give 1/gm, NOT 0 like an op-amp.

### Q22. (GATE-level) Compare CE (BJT) vs CS (MOS) small-signal input resistances.
**Answer:** CE ~ rπ (kΩ); CS ~ ∞.
**Method:** BJT draws base current; MOS doesn't.

### Q23. (GATE-level) Which config has the highest input impedance and ~1 gain; used as buffer?
**Answer:** Common-drain (source follower).
**Method:** impedance transformation from ∞ to 1/gm.

### Q24. (GATE-level) CS with unbypassed R_S: R_out changes?
**Answer:** R_out still R_D (degeneration affects gain & input, not drain-side output).
**Method:** R_out sees no degeneration term directly.

### Q25. (GATE-level) Cascode load R_out formula for BJT/MOS?
**Answer:** ~`gm·r_o·r_o` (BJT/MOS cascode) — several MΩ.
**Method:** the stacking multiplies output resistances.

### Q26. (GATE-level) A common-gate amplifier is driven from a current source: gain description?
**Answer:** transresistance: `v_o/i_in = R_D (current-to-voltage)`, A_v still `+gm·R_D` when voltage-driven.
**Method:** the current-in view: R_out at the drain converts current to voltage.

### Q27. (GATE-level) Handle a CS with gate grounded through resistor (no source degeneration): gain?
**Answer:** still `−gm R_D`; the gate bias rés not in the AC path (AC ground).
**Method:** capacitor/AC ground references remove R_G.

### Q28. (Moderate) If C_S(MOS source bypass)is removed at higher frequency? Gain…
**Answer:** falls (degeneration returns at f where C_S no longer short).
**Method:** bypass → high gain midband; removed/poor C_S → lower gain + wider band.

### Q29. (GATE-level) Find the small-signal gain of the cascade CS+CD: `gm1=2m, RD1=4k, gm2=10m, R_L2=1k`.
**Answer:** Stage1 `−2m·4k = −8`; Stage2 `0.909` (Q10 with gm2=10m R_S=1k). Total `−8·0.909 = −7.27`.
**Method:** multiply the two loaded gains with the follower ≈1.

### Q30. (GATE-level) A CS stage biased mid-V_DD — max unclipped swing?
**Answer:** `2·min(V_DSQ − V_ov, I_DQ·R_D_AC)` around Q (class-A limit).
**Method:** the load-line exercise applies exactly as BJT.

### Q31. (GATE-level) Rail-to-rail output: which MOS follower gives low R_out near both rails?
**Answer:** complementary pairs (PMOS+NMOS followers); single device loses headroom to V_th.
**Method:** push-pull output stage.

---

## Trap box (exam-day killers)

- CS inverts; don't drop the minus sign.
- Miller ONLY on inverting amplifier stages.
- Source follower gain is close to 1, never >1.
- CG and CD input resistances: R_in ≈ 1/gm for CG.
- Active load gains hit gm·r_o (usually > the R_D number students expect).

## Final recall drill (do in 60 seconds)

1. CS gain → `−gm·R_D (or −R_D/R_S)`; inverting
2. CG → `+gm·R_D`; R_in ≈ 1/gm
3. Source follower → ≈1; R_out ≈ 1/gm
4. Active load → −gm·r_o
5. Cascode → kills Miller, R_out≈gm·r_o²

---