# DC and AC Analysis Method — Practice (Learn by Solving)

> **The idea in one line:** every transistor-amplifier numerical in GATE is the
> **same four steps** — ① DC Q-point (open the caps, kill the AC sources) ② small-
> signal parameters from the Q-point ③ the AC equivalent (short the midband
> caps, ground the supplies) ④ solve gain, `R_in`, `R_out`. Learn the four steps
> once and every chapter reduces to arithmetic.
>
> **How to use:** solve each question fully before reading the answer. Cover the
> **Answer**/**Method** with paper, do it, then reveal. If you miss one, solve
> the next 3 in the file to lock the pattern. No need to read the chapter notes
> first — every concept is taught through the drill itself. Open
> `27-DC-and-AC-Analysis-Method.md` or `32-Single-File-Cheatsheet.md` only when
> you want the underlying theory.

## Concept box (what you must internalise)

- **Step ① DC Q-point:** replace **all capacitors by open circuits**; set AC
  sources to zero (voltage source → short, current source → open). Compute
  `I_C`/`I_D` and `V_CE`/`V_DS`, **then verify the region** (`V_C > V_B > V_E`
  for an NPN; `V_DS ≥ V_GS − V_th` for an NMOS).
- **Step ② parameters:** BJT `gm = I_C/V_T`, `rπ = β/gm`, `re = V_T/I_E`,
  `ro = V_A/I_C`. MOS `gm = 2I_D/(V_GS−V_th) = k(V_GS−V_th)`, `ro = 1/(λI_D)`.
  With `V_T = 25 mV`, `gm = 40·I_C[mA]` mA/V.
- **Step ③ AC equivalent:** **short every midband capacitor**, **ground every DC
  supply** (that is what "AC ground" means), then drop in the small-signal model
  (`rπ` and `gm·v_be` for a BJT; an open gate and `gm·v_gs` for a MOS).
- **Step ④ solve:** `A_v = −gm(R_C∥R_L)` (CE/CS, emitter/source bypassed),
  `R_in = R_b∥rπ` (bypassed) or `R_b∥(β+1)(re+R_E)` (unbypassed), `R_out = R_C`.
- **Method:** the order is not negotiable — you cannot build the AC circuit
  before you know the Q-point, because every parameter comes from the Q-point.
  Write the verify line (region check) on the page even if you are sure.
- **Trap:** `R_in` is measured at the amplifier terminals (source resistance
  **excluded**); if the question wants gain from the source it is `A_vs`, which
  is `A_v·R_in/(R_in+R_s)`.

---

## Questions

### Q1. (Easy) What do you replace capacitors by in the DC analysis, and in the AC (midband) analysis?
**Answer:** DC analysis: **open circuits** (a capacitor blocks DC). Midband AC analysis: **shorts** (at signal frequency their reactance is negligible).
**Method:** This single swap is the whole difference between the two analyses, and it is the reason the DC and AC results are independent. If a capacitor appears in your DC answer, you made the error. Source: `27-DC-and-AC-Analysis-Method.md` §27.1, §27.3.

### Q2. (Easy) What do you do to a DC supply rail (`V_CC`, `V_DD`) when building the AC equivalent circuit, and why?
**Answer:** You take it to **0 V (AC ground)**. The supply is an ideal DC voltage source, so it has no AC voltage across it — an ideal voltage source set to zero is a short to ground.
**Method:** This is what "AC ground" means: any node held at a constant DC potential by an ideal source is AC ground. The same logic makes a **bypassed** emitter or source an AC ground. Source: `27-DC-and-AC-Analysis-Method.md` §27.3.

### Q3. (Easy) Write the four small-signal parameters of a BJT in terms of the Q-point.
**Answer:** `gm = I_C/V_T`, `rπ = β/gm = βV_T/I_C`, `re = V_T/I_E ≈ V_T/I_C`, `ro = V_A/I_C` — with `V_T = 25 mV`.
**Method:** Memorise only `gm = I_C/V_T` and `rπ = β/gm`; everything else is derivable. Handy sanity check: at `I_C = 1 mA`, `gm = 40 mA/V`, `rπ = 2.5 kΩ` at β = 100, `re = 25 Ω`. Source: `08-BJT-Small-Signal-Models.md`, `29-Formula-Sheet.md` §29.3.

### Q4. (Easy) A CE amplifier has `R_C = 4 kΩ`, `R_L = 4 kΩ`, `I_C = 1 mA`. What is the midband voltage gain, and what is its sign?
**Answer:** `R_C∥R_L = 2 kΩ`; `gm = 1 mA/25 mV = 40 mA/V`; `A_v = −gm·(R_C∥R_L) = −0.04 × 2000 = −80`. The sign is **negative** (180° inversion) because CE inverts.
**Method:** The BJT sign rule: CE and CS invert; CB, CG and CC do not. Magnitude: `mA/V × kΩ = V/V` — 40 mA/V × 2 kΩ = 80, no unit conversion fumbles. Source: `09-BJT-Amplifiers.md`, `27-DC-and-AC-Analysis-Method.md` §27.4.

### Q5. (Easy) What is the input resistance of a CE amplifier whose emitter resistor is bypassed, and of one whose emitter resistor is *not* bypassed?
**Answer:** Bypassed: `R_in = R_b1∥R_b2∥rπ` — small, and it *falls* when you remove the bypass cap. Unbypassed: `R_in = R_b1∥R_b2∥(β+1)(re+R_E)` — multiplied by `β+1`, hence very large.
**Method:** Bypassing `R_E` at AC removes the emitter degeneration; the base then only sees `rπ`. Without the cap, emitter current is `(β+1)i_b` and that current must flow through `R_E`, so the base sees `(β+1)(re+R_E)`. Source: `27-DC-and-AC-Analysis-Method.md` §27.4.

### Q6. (Easy) List the four "tools" that make step ④ tractable.
**Answer:** (1) **Thevenin** — collapse a bias divider to `V_th + R_th`; (2) **test-source method** — to find `R_out`, kill the sources and apply a test `V`/`I`, then `R_out = V_test/I_test`; (3) **half-circuit** — by symmetry, a differential pair needs only half the work; (4) **virtual ground** — the inverting op-amp node.
**Method:** Recognise which tool the question needs: a divider → Thevenin; "find R_out" → test source; a diff pair → half-circuit; an op-amp in a feedback loop → virtual short. Source: `27-DC-and-AC-Analysis-Method.md` §27.5.

### Q7. (Easy) In a midband CE amplifier, what happens to the gain and the input resistance when the emitter bypass capacitor is removed?
**Answer:** Gain **drops** from `−gm·R_C'` to about `−R_C'/R_E`; input resistance **rises** (from `R_b∥rπ` to `R_b∥(β+1)(re+R_E)`); bandwidth **widens** (no bypass pole, and the gain is now resistor-ratio, so Miller shrinks).
**Method:** All three effects come from one fact: the emitter is no longer AC ground, so the circuit is degenerate (series) feedback. Learn them as a set — GATE asks "what happens if…" with all three at once. Source: `10-AC-Coupling.md`, `27-DC-and-AC-Analysis-Method.md` §27.4.

### Q8. (Easy) `R_in` is found as `R_b∥rπ = 1.37 kΩ` and the source resistance is `1 kΩ`. What is the gain from the *source* voltage?
**Answer:** `A_vs = A_v·R_in/(R_in+R_s) = A_v·1.37/2.37 = 0.578·A_v`. With `A_v = −131.5` that gives `A_vs = −76.0`.
**Method:** The source resistance and the input resistance form a divider. `A_v` is measured **at the amplifier input**; `A_vs` is measured **at the source**. Read the question's words carefully — they always tell you which. Source: `27-DC-and-AC-Analysis-Method.md` §27.3, §27.6.

### Q9. (Easy) Voltage-divider bias: `V_CC = 12 V`, `R1 = 100 kΩ` (top), `R2 = 25 kΩ` (bottom), `R_E = 1 kΩ`, `V_BE = 0.7 V`. Find `V_B`, `V_E` and `I_E`. Then say whether the base-current loading is negligible here.
**Answer:** `V_B = 12 × 25/(100+25) = 12 × 0.2 = 2.4 V`; `V_E = 2.4 − 0.7 = 1.7 V`; `I_E = 1.7/1k = 1.7 mA`. The loading is **not** negligible if `β = 100`: the validity test is `β·R_E ≥ 10·R2`, and here `100 × 1 kΩ = 100 kΩ < 10 × 25 kΩ = 250 kΩ`. The exact Thevenin solution (Q10's method) gives `I_B = 1.7/(20k + 101k) = 14.05 µA`, `I_C = 1.405 mA`, `V_E = 1.42 V`, `V_CE = 12 − 1.405m×4k − 1.42 = 4.96 V` ✓ active.
**Method:** The divider result `V_B` is exact only for a **negligible** base current. The practical test is `β·R_E ≥ 10·R2`. Here it fails by 2.5×, so the true `I_C` is 1.40 mA, not 1.7 mA. We deliberately carry the textbook approximation through Q11–Q15 (it is what the chapter does and it makes the arithmetic clean) — but you must be able to say when it is licensed and when it is not. Source: `07-BJT-Biasing.md`, `27-DC-and-AC-Analysis-Method.md` §27.6.

### Q10. (Easy) Thevenin the base network of Q9 and give `V_th` and `R_th`.
**Answer:** `V_th = 2.4 V`; `R_th = 100k∥25k = 20 kΩ`.
**Method:** `V_th` = the open-circuit (unloaded) divider output; `R_th` = the divider with the supply shorted, i.e. the two resistors in parallel. Then the base loop is one equation: `I_B = (V_th − 0.7)/(R_th + (β+1)R_E)`. This is the single most useful transformation in the subject. Source: `01-Prerequisites.md`, `27-DC-and-AC-Analysis-Method.md` §27.5.

### Q11. (Easy) CE amplifier, full analysis: `V_CC = 12 V`, `R1 = 100 kΩ`, `R2 = 25 kΩ`, `R_C = 4 kΩ`, `R_E = 1 kΩ` (bypassed), `R_L = 4 kΩ`, `β = 100`, `V_BE = 0.7 V`, `V_T = 25 mV`, `V_A = 100 V`. Find the full Q-point and **verify the region**.
**Answer:** `V_B = 2.4 V`; `V_E = 1.7 V`; `I_E = 1.7 mA`; `I_C ≈ 1.7 mA`; `V_C = 12 − 1.7m×4k = 5.2 V`; `V_CE = 12 − 1.7m×5k = 3.5 V`. Region: `V_C = 5.2 > V_B = 2.4 > V_E = 0` ✓ **active**.
**Method:** Write the verify line before moving on: `V_C > V_B > V_E` is the NPN active condition and `V_CE = 3.5 V ≫ 0.2 V` is its numeric form. A solution without a verify line is an incomplete solution. Source: `27-DC-and-AC-Analysis-Method.md` §27.1, §27.6.

### Q12. (Moderate) Small-signal parameters for the Q-point of Q11.
**Answer:** `gm = 1.7 mA/25 mV = 68 mA/V`; `rπ = β/gm = 100/0.068 = 1.47 kΩ`; `re = 25 mV/1.7 mA = 14.7 Ω`; `ro = V_A/I_C = 100/1.7 mA = 58.8 kΩ`.
**Method:** `1.7/0.025 = 68`. Then `rπ = 1/gm × β = 14.7 × 100 = 1.47 kΩ` — note `rπ = β·re` is the same statement. `ro` uses `V_A`, so if the question does not give `V_A`/`λ`, **omit** `ro`. Source: `08-BJT-Small-Signal-Models.md`.

### Q13. (Moderate) For the circuit of Q11, find the total AC collector load and the midband voltage gain (with `ro`).
**Answer:** `R_C∥R_L = 4k∥4k = 2 kΩ`; including `ro`: `2k∥58.8k = 1.934 kΩ`; `A_v = −gm·R_load = −0.068 × 1934 = −131.5 ≈ −132`. Ignoring `ro`: `−0.068 × 2000 = −136`.
**Method:** `ro` sits in parallel with everything else at the collector, so it always *reduces* the gain slightly. Include it whenever `V_A` or `λ` is given; the exam's "with `V_A` = …" is a deliberate instruction. Source: `27-DC-and-AC-Analysis-Method.md` §27.4, §27.6.

### Q14. (Moderate) For the circuit of Q11, find `R_in` and `R_out`.
**Answer:** `R_in = 100k∥25k∥rπ = 20k∥1.47k = 1.37 kΩ`. `R_out = R_C∥ro = 4k∥58.8k = 3.75 kΩ`; the common textbook approximation (dominant `R_C`) gives `R_out ≈ 4 kΩ`.
**Method:** `R_in` is dominated by `rπ` whenever `rπ ≪ R_b` — that is the standard signature of a badly-designed (low-impedance) bias network. `R_out` is set by whatever resistance hangs off the output node, here `R_C∥ro`. Source: `27-DC-and-AC-Analysis-Method.md` §27.4.

### Q15. (Moderate) Add a source resistance `R_s = 1 kΩ` to Q13/Q14. Find the gain from the source, `A_vs`.
**Answer:** `A_vs = A_v·R_in/(R_in+R_s) = −131.5 × 1.37/2.37 = −131.5 × 0.578 = −76.0`. So the source resistance and the low `R_in` throw away 42% of the available gain.
**Method:** Always do the divider *before* multiplying by `A_v`. If the ratio `R_in/(R_in+R_s)` is not close to 1, the design is source-resistance limited — the standard complaint about a 1.37 kΩ input resistance. Source: `27-DC-and-AC-Analysis-Method.md` §27.6.

### Q16. (Moderate) Now **remove** the emitter bypass capacitor from Q11 and recompute gain and `R_in`.
**Answer:** `R_C∥R_L = 2 kΩ`; `A_v = −gm·(R_C∥R_L)/(1 + gm·R_E) = −0.068×2000/(1 + 0.068×1000) = −136/69 = −1.97`; equivalently `≈ −(R_C∥R_L)/R_E = −2000/1000 = −2`. `R_in = 20k∥(β+1)(re+R_E) = 20k∥101×1014.7 = 20k∥102.5k = 16.7 kΩ`.
**Method:** The unbypassed formula is the *same* calculation with `1 + gm·R_E` in the denominator. The quick estimate `−R_C'/R_E` (using the **total** AC collector resistance `R_C∥R_L`, not `R_C` alone) is valid when `gm·R_E ≫ 1` — here `68 ≫ 1`, and 1.97 vs 2.0 confirms it. Source: `27-DC-and-AC-Analysis-Method.md` §27.4.

### Q17. (Moderate) CS amplifier, full analysis: `V_DD = 10 V`, `R1 = 60 kΩ` (to `V_DD`), `R2 = 20 kΩ` (to ground), `R_D = 2 kΩ`, `R_S = 1 kΩ` (bypassed), `R_L = 4 kΩ`, `k = 1 mA/V²`, `V_th = 1 V`. Find the Q-point.
**Answer:** `V_G = 10 × 20/80 = 2.5 V` (exact — no gate current). `V_GS = 2.5 − I_D·1k`. So `I_D = 0.5·1·(V_GS − 1)²` with `I_D` in mA: `x = 0.5(1.5 − x)²` → `x² − 5x + 2.25 = 0` → `x = 4.5` or `x = 0.5`. `x = 4.5` gives `V_GS = −2 V` (invalid, below `V_th`), so **`I_D = 0.5 mA`**, `V_GS = 2.0 V`, `V_DS = 10 − 0.5m×3k = 8.5 V`. Region: `8.5 ≥ 2.0 − 1.0 = 1.0` ✓ saturation.
**Method:** Write the quadratic in the single unknown `I_D` (or in the overdrive `V_GS − V_th`), keep the physical root only, then verify. Rejecting the root that gives `V_GS < V_th` is the essential step. Source: `12-MOSFET-Biasing.md`, `27-DC-and-AC-Analysis-Method.md` §27.1.

### Q18. (Moderate) For the CS amplifier of Q17, find the small-signal gain, `R_in` and `R_out`; then repeat including `ro` with `λ = 0.01`.
**Answer:** `gm = 2I_D/(V_GS−V_th) = 1 mA/1 V = 1 mA/V`; `R_D∥R_L = 1.333 kΩ`; `A_v = −gm·(R_D∥R_L) = −1.333`. `R_in = R1∥R2 = 60k∥20k = 15 kΩ`; `R_out = R_D = 2 kΩ`. With `λ = 0.01`: `ro = 1/(0.01×0.5 mA) = 200 kΩ`; load becomes `1.333k∥200k = 1.3245 kΩ`; `A_v = −1.325`. (The `−gm·R_D` result barely moves: `ro ≫ R_D`.)
**Method:** MOS `R_in` is the *bias network* resistance (the gate draws nothing), never `rπ`. Compare the BJT case, where `R_in` collapses to `rπ`. Source: `14-MOSFET-Amplifiers.md`, `27-DC-and-AC-Analysis-Method.md` §27.4.

### Q19. (Moderate) Remove the source bypass capacitor in Q17 (`R_S = 1 kΩ`) and find the gain.
**Answer:** `A_v = −gm·R_D/(1 + gm·R_S) = −0.001×2000/(1 + 0.001×1000) = −2/2 = −1.0`.
**Method:** Note `gm·R_S = 1`, which is **not** `≫ 1`, so the quick estimate `−R_D/R_S = −2` is *wrong* here (it overestimates by 2×). The estimate is only valid when `gm·R_S ≫ 1`. This is the trap in `27-DC-and-AC-Analysis-Method.md` §27.4 and `32-Single-File-Cheatsheet.md` §5. Source: `14-MOSFET-Amplifiers.md`.

### Q20. (Moderate) A common-gate amplifier uses the Q-point of Q17 with the same `R_D = 2 kΩ`, `R_L = 4 kΩ`. Give the gain, the sign, and the input resistance.
**Answer:** `A_v = +gm·(R_D∥R_L) = +1.333` — **positive**, because the input is applied at the source. `R_in ≈ 1/gm = 1/0.001 = 1 kΩ`.
**Method:** `1/gm` is the MOS analogue of `re`; `1/gm = 25 mV/I_D` for a BJT (`re`). CG/CB do not invert, and both have very low input resistance — that is the trade for not losing Miller effect. Source: `14-MOSFET-Amplifiers.md`, `29-Formula-Sheet.md` §29.4.

### Q21. (Moderate) An emitter follower: `V_CC = 12 V`, divider `100 kΩ/25 kΩ`, `R_E = 1 kΩ`, `R_L = 10 kΩ`, `β = 100`, `V_T = 25 mV`. Find the Q-point, the gain and `R_in`.
**Answer:** `V_B = 2.4`, `V_E = 1.7`, `I_E = 1.7 mA`, `V_CE = 12 − 1.7m×1k = 10.3 V` ✓ active. `re = 25 mV/1.7 mA = 14.7 Ω`; `R_E∥R_L = 1k∥10k = 909 Ω`; `A_v = 909/(909+14.7) = 0.984`. `R_in = 20k∥(β+1)(re + 909) = 20k∥93.3k = 16.5 kΩ`.
**Method:** The follower rule is `A_v = (R_E∥R_L)/(re + R_E∥R_L)`, i.e. a resistive divider between the emitter resistance and `re`. `R_in` is multiplied by `β+1` because the emitter current is `(β+1)i_b`. Source: `09-BJT-Amplifiers.md`, `29-Formula-Sheet.md` §29.3.

### Q22. (Moderate) Why can you not start step ② before step ①?
**Answer:** Because **every** small-signal parameter is computed *from* the Q-point current: `gm = I_C/V_T`, `rπ = βV_T/I_C`, `re = V_T/I_E`, `ro = V_A/I_C` (and `gm = 2I_D/(V_GS−V_th)`, `ro = 1/(λI_D)` for MOS). With no `I_C` there is no `gm`.
**Method:** The four-step order exists because of this dependency chain: DC circuit → Q-point → parameters → AC circuit → gain. A shortcut ("assume `I_C = 1 mA`") is only legitimate if the problem gives the Q-point directly. Source: `27-DC-and-AC-Analysis-Method.md` §27.0, §27.2.

### Q23. (Moderate) A CE amplifier is fed through a coupling capacitor from a source with `R_s = 500 Ω`. Does the coupling capacitor affect the DC Q-point?
**Answer:** **No.** A capacitor in series with the base blocks DC, so the base sees the bias network only — the Q-point is identical with or without the coupling cap. Its only role is AC: at midband it is a short, so `A_vs = A_v·R_in/(R_in+R_s)`.
**Method:** "No DC effect, all AC effect" is the one-line summary of every coupling capacitor. If a coupling cap appears in your DC equations, delete it (open circuit). Source: `10-AC-Coupling.md`, `27-DC-and-AC-Analysis-Method.md` §27.1.

### Q24. (Moderate) In the midband AC equivalent of Q11, list every element and say what happened to it.
**Answer:** `C_E` → **short** (emitter becomes AC ground); `V_CC` → **ground**; `R_C` → from collector to ground; `R_L` → from collector to ground; `R1`, `R2` → base to ground; the transistor → `rπ` (base–emitter) in parallel with `gm·v_be` (collector→emitter) and `ro` (collector–emitter); `R_E` → shorted out of the AC circuit by `C_E` (it is still there for DC).
**Method:** Read the schematic once and classify every element into {short, open, ground, keep}. Doing this explicitly is the difference between a clean small-signal drawing and the sign errors that come from sloppy ones (`27-DC-and-AC-Analysis-Method.md` GATE trap 6). Source: `27-DC-and-AC-Analysis-Method.md` §27.3.

### Q25. (Moderate) A CE stage (`A_v1 = −50`, `R_out1 = 2 kΩ`) drives a buffer with `R_in2 = 100 kΩ`. Find the effective collector load of stage 1 and the loaded gain of stage 1.
**Answer:** `R_load1 = 2k∥100k = 1.96 kΩ` (a 2% reduction from 2 kΩ). Loaded gain `= −gm·1.96k`; if stage 1's unloaded gain was `−gm·2k = −50`, then `gm = 50/2000 = 25 mA/V` and the loaded gain is `−0.025×1960 = −49.0`.
**Method:** Cascaded stages must be analysed **loaded**: the next stage's `R_in` is in parallel with this stage's `R_C`. Total gain is the *product of loaded gains*, not the product of unloaded ones. A high-`R_in` buffer (CC/CD) is the cheap way to avoid the loading. Source: `09-BJT-Amplifiers.md`, `27-DC-and-AC-Analysis-Method.md` §27.4.

---

### Q26. (GATE-level) A CE amplifier has `R_C = 2 kΩ`, `R_L = 2 kΩ`, and you need `|A_v| = 100` at midband with `R_E` bypassed. What collector current must the bias set, and what is `V_CE` if `V_CC = 12 V`, `R_E = 500 Ω`?
**Answer:** `R_C∥R_L = 1 kΩ`; `gm = 100/1000 = 0.1 S = 100 mA/V`; `I_C = gm·V_T = 0.1×0.025 = 2.5 mA`. `I_E ≈ 2.5 mA`; `V_E = 2.5 mA×500 = 1.25 V`; `V_C = 12 − 2.5m×2k = 7 V`; `V_CE = 7 − 1.25 = 5.75 V` ✓ active (`V_C = 7 > V_B = 1.95 > V_E = 1.25`).
**Method:** Invert the gain formula: `gm = |A_v|/(R_C∥R_L)`, then `I_C = gm·V_T`. Always finish with the Q-point check — a gain target can be unreachable because the required `I_C` pushes the transistor out of the active region, and that is a standard GATE trap. Source: `27-DC-and-AC-Analysis-Method.md` §27.2, §27.4.

### Q27. (GATE-level) In the amplifier of Q26 the bias current is raised to `5 mA` by halving `R_E` to `250 Ω` (so `V_E` stays at `1.25 V`). Re-verify the region, then find the new gain, and compute the maximum undistorted output swing before and after the change.
**Answer:** `V_E = 5m×250 = 1.25 V`; `V_B = 1.95 V`; `V_C = 12 − 5m×2k = 2 V`; `V_CE = 2 − 1.25 = 0.75 V > 0.2 V` ✓ **still active**. `gm = 5m/25m = 0.2 S`; `rπ = 100/0.2 = 500 Ω`; `re = 5 Ω`; `A_v = −0.2×1000 = −200` (the gain **doubles**, as `gm ∝ I_C` promises). But the maximum undistorted swing collapses: `V_pp = 2·min(V_CEQ − 0.2, V_CC − V_CEQ) = 2·min(0.55, 10) = 1.1 V`, versus `2·min(5.55, 6.25) = 11.1 V` for the 2.5 mA design — a **10× loss of swing** for a 2× gain.
**Method:** This is the single most important design trade-off in small-signal biasing. `gm ∝ I_C` so the *small-signal* gain improves with current, but the DC headroom to saturation shrinks as `V_CE − 0.2`, so the *large-signal* swing (and hence the linearity and output power) collapses. Gain improves, everything else degrades — so always re-verify the region and the swing, never just the gain. Source: `27-DC-and-AC-Analysis-Method.md` §27.1, §27.2, `28-Graphical-Interpretation.md` §28.2.

### Q28. (GATE-level) Full end-to-end on a MOSFET CS stage: `V_DD = 12 V`, `R1 = 100 kΩ` (to `V_DD`), `R2 = 50 kΩ` (to ground), `R_D = 3 kΩ`, `R_S = 2 kΩ` (bypassed), `R_L = 6 kΩ`, `k = 1 mA/V²`, `V_th = 1 V`, `λ = 0.02`. Give the Q-point, `A_v`, `R_in`, `R_out`, and the region check.
**Answer:** `V_G = 12×50/150 = 4 V`; `V_GS = 4 − 2I_D` (mA, kΩ). `x = 0.5(3 − 2x)²` → `x = 4.5 − 6x + 2x²` → `2x² − 7x + 4.5 = 0` → `x = [7 ± √(49−36)]/4 = [7 ± 3.606]/4 = 2.651 or 0.849`. The root 2.651 gives `V_GS = −1.30 V < V_th` (invalid), so **`I_D = 0.849 mA`**, `V_GS = 2.303 V`, `V_DS = 12 − 0.849m×5k = 7.757 V`. Region: `7.757 ≥ 2.303 − 1 = 1.303` ✓ saturation. `gm = k·V_ov = 1 mA/V² × 1.303 V = 1.303 mA/V`; `ro = 1/(0.02 × 0.849 mA) = 58.9 kΩ`; `R_D∥R_L = 2 kΩ`; load with `ro` = `2k∥58.9k = 1.934 kΩ`; `A_v = −1.303m × 1934 = −2.52`. `R_in = 100k∥50k = 33.3 kΩ`; `R_out = R_D∥ro = 2.85 kΩ`.
**Method:** The whole method in one question, in order: divider → quadratic in `I_D` → reject the unphysical root → region check → `gm`, `ro` → total AC load → gain → `R_in` (the divider) → `R_out`. Every step is the same as the BJT case; only the parameter formulas change. Note `gm = k·V_ov` here, and that with `V_GS = 2.3 V` and `V_DD = 12 V` a CS stage gives a gain of only `−2.5` — MOS CS stages need large `W/L` to compete with a CE stage. Source: `27-DC-and-AC-Analysis-Method.md` §27.0, `12-MOSFET-Biasing.md`, `14-MOSFET-Amplifiers.md`.

### Q29. (GATE-level) In Q28 the source bypass capacitor is removed. Find the new gain, and state the condition under which the estimate `−R_D/R_S` is valid.
**Answer:** `A_v = −gm·R_D/(1 + gm·R_S) = −0.001303×3000/(1 + 0.001303×2000) = −3.909/3.610 = −1.08`. The estimate `−R_D/R_S = −1.5` is valid only when `gm·R_S ≫ 1`; here `gm·R_S = 2.61`, so the estimate overestimates the gain by 38%. The exact form `A_v = −R_D/(1/gm + R_S)` makes the condition explicit: it needs `R_S ≫ 1/gm = 766 Ω`, and here `R_S = 2 kΩ` is only 2.6× that. `R_in` is unchanged at 33.3 kΩ.
**Method:** Always write the unbypassed gain as `−R_D/(1/gm + R_S)` — the `1/gm` term is the reason the quick estimate fails, and dropping it silently can be a 2–3× error. MOS analogue of the CE-degeneration condition `gm·R_E ≫ 1`. Source: `29-Formula-Sheet.md` §29.4.

### Q30. (GATE-level) A CE amplifier is designed with `β = 100` but the transistors that will be used are specified `β_min = 40`. The gain formula uses `rπ = β/gm`. By what factor is `R_in` optimistic, and what is the design lesson?
**Answer:** `rπ` scales linearly with `β`: with `I_C` fixed, `rπ = βV_T/I_C`, so `rπ(40)/rπ(100) = 0.4` — `R_in` is **2.5× larger** in reality than the nominal-β calculation suggests (`R_in` is `R_b∥rπ`, so the increase is even smaller than 2.5× if `R_b` is comparable). Lesson: for anything that depends on `rπ` (input impedance, bias current, input loading of the previous stage) use `β_min`; for the *gain* use `gm`, which does not contain `β` at all.
**Method:** Audit every formula for its β-dependence: `A_v = −gm·R_C'` — no β. `R_in = R_b∥rπ` — β. `R_in(unbypassed) = R_b∥(β+1)(re+R_E)` — β. Bias current — β. Design each with the pessimistic β, and say so on the page. Source: `07-BJT-Biasing.md`, `27-DC-and-AC-Analysis-Method.md` §27.2.

### Q31. (GATE-level) A CE stage is fed by a source with `R_s = 1 kΩ`. Its `R_in = 1.37 kΩ` and `A_v = −131.5`. Give the gain from the source, the current gain from source to output, and the comment GATE wants.
**Answer:** `A_vs = −131.5 × 1.37/2.37 = −76.0`. Source current `i_sig = v_sig/(R_s + R_in) = v_sig/2.37k`; output current `i_out = v_o/R_C = v_o/4k = −131.5·v_in/4000`. With `v_in = 0.578·v_sig`: `i_out = −76.0·v_sig/4k = −19.0·v_sig mA`; `i_sig = v_sig/2.37k = 0.422·v_sig mA`; current gain `= −19.0/0.422 = −45`. Comment: the stage is heavily source-resistance limited — 42% of the signal voltage is lost on `R_s` before the transistor sees it, which is a direct consequence of the low `R_in` caused by the low bias resistance.
**Method:** `A_vs` (voltage) and current gain are different numbers; the current gain additionally involves `R_C` and the input division. Whenever a question gives `R_s`, expect both `A_vs` and a comment about matching. Source: `27-DC-and-AC-Analysis-Method.md` §27.3, §27.6.

### Q32. (GATE-level) A CS amplifier has `R_D = 4 kΩ`, `R_L = 4 kΩ`, `I_D = 1 mA`, `V_GS − V_th = 2 V`, `λ = 0`. Find the gain, and then the gain if the same transistor runs at `I_D = 4 mA` (with `V_GS − V_th` unchanged at 2 V — i.e. W/L quadrupled).
**Answer:** `gm = 2I_D/(V_GS−V_th) = 2(1)/2 = 1 mA/V`; `R_D∥R_L = 2 kΩ`; `A_v = −1×2 = −2`. At `I_D = 4 mA`: `gm = 2(4)/2 = 4 mA/V`; `A_v = −4×2 = −8`. Gain scales linearly with `I_D` at fixed overdrive.
**Method:** `gm = 2I_D/V_ov` → `gm ∝ I_D` at fixed `V_ov`, and `gm = √(2kI_D)` → `gm ∝ √I_D` at fixed `k`. Two different scalings for two different constraints, and GATE likes to test which one applies: "fix the overdrive" gives linear, "fix the device (W/L)" gives the square root. Source: `13-MOSFET-Small-Signal-Model.md`.

### Q33. (GATE-level) An amplifier's frequency response is specified "midband, 100 Hz to 20 kHz". Which capacitors in a CE amplifier set `f_L`, and which internal capacitances set `f_H`? State the value of the Miller capacitance `C_M` in terms of `C_μ` and `|A_v|`.
**Answer:** `f_L` is set by the **external** capacitors: the two coupling caps (`C_1`, `C_2`) and the emitter bypass cap `C_E` (each a high-pass pole at `1/(2πCR_eq)`; for the bypass, `R_eq ≈ re + R_B/(β+1)`, **not** `R_E`). `f_H` is set by the **internal** device capacitances `C_π` and `C_μ` plus Miller multiplication: **`C_M = C_μ(1 + |A_v|)`**, valid only for inverting stages (CE/CS). Midband means: short the external caps, ignore `C_π`, `C_μ`.
**Method:** Low frequency = external (you chose those caps); high frequency = internal (the device made them). The bypass-cap `R_eq` is the single most-missed number in the subject — it is `re + R_B/(β+1)` because the bypass cap sees the emitter resistance *looking back into the base network*, not `R_E`. Source: `16-Frequency-Response.md`, `10-AC-Coupling.md`.

### Q34. (GATE-level) A CE amplifier has `A_m = −100` at midband with `f_H = 20 kHz`. Give the gain in dB at `100 kHz` and at `1 MHz`, and the gain-bandwidth product. Then repeat if the roll-off is 40 dB/dec instead of 20 dB/dec.
**Answer:** At 100 kHz (5× the corner): `20·log10(5) = 14 dB` down → `40 − 14 = 26 dB`. At 1 MHz (50×): `20·log10(50) = 34 dB` down → `6 dB`. `GBW = 100 × 20 kHz = 2 MHz`. With 40 dB/dec: at 100 kHz the drop is 2×14 = 28 dB → 12 dB; at 1 MHz, 68 dB down → −28 dB. The *same* `f_H` with a steeper slope means **two** poles, not a bigger gain.
**Method:** dB drop = `20·log10(f/f_H)` per pole, multiplied by the number of poles. Slope/20 = number of poles. Slope 40 dB/dec = 2 poles = 2× the droop. Source: `16-Frequency-Response.md`, `28-Graphical-Interpretation.md` §28.5.

### Q35. (GATE-level) A design uses a CE stage with `R_C = 4 kΩ` and a `4.7 nF` emitter bypass capacitor. Compute the bypass pole using the correct `R_eq`, for `I_C = 1.7 mA`, `β = 100`, `R_B = 20 kΩ`, and compare with the common wrong answer that uses `R_E = 1 kΩ`.
**Answer:** `re = 25 mV/1.7 mA = 14.7 Ω`; `R_B/(β+1) = 20k/101 = 198 Ω`; `R_eq = 14.7 + 198 = 212.7 Ω`. Correct pole: `f = 1/(2π×212.7×4.7n) = 1/(6.28e-6) = 159 kHz`. Wrong answer (using `R_E = 1 kΩ`): `f = 1/(2π×1000×4.7n) = 33.9 kHz` — a factor 4.7 too low, i.e. the bypass cap looks far more effective than it is.
**Method:** The bypass cap sees the resistance looking *into* the emitter (`re` in series with `R_B/(β+1)`), because a change in emitter current must be supplied through the base network. Using `R_E` alone is the standard low-frequency-analysis error. Source: `10-AC-Coupling.md`, `16-Frequency-Response.md`.

### Q36. (GATE-level) Two identical CE stages, each with an unloaded `A_v = −20` and `R_out = 5 kΩ` (`β = 100`, `ro` ignored), are cascaded with a direct coupling. What is the total gain, and how much is lost to interstage loading? Repeat with a CC buffer (`R_in = 200 kΩ`, `A_v ≈ 1`) in between.
**Answer:** `A_v = −gm·R_C` gives `gm = 20/5000 = 4 mA/V`, so `rπ = 100/0.004 = 25 kΩ`. **Direct coupling:** `R_load1 = 5k∥25k = 4.167 kΩ`; `A_v1,loaded = −0.004×4167 = −16.67`; total `= (−16.67)(−20) = +333` instead of `+400` — a **17% loss**. **Buffered:** `R_load1 = 5k∥200k = 4.878 kΩ`; `A_v1 = −0.004×4878 = −19.51`; total `= (−19.51)(−20)(1) = +390` — only a **2.4% loss**.
**Method:** The lesson is the *shape* of the numbers: a low-`R_out` stage loading a low-`R_in` stage destroys the product-of-gains rule (here 17% lost in a single stage, and the loss compounds down a long chain), while a high-`R_in` follower restores it. Always analyse cascaded stages **loaded**, and put a follower between a low-`R_out` stage and a low-`R_in` stage. Source: `09-BJT-Amplifiers.md`, `27-DC-and-AC-Analysis-Method.md` §27.4.

---

## Trap box (exam-day killers)

- **Forgetting the region check.** Every DC answer must end with `V_C > V_B > V_E` (BJT) or `V_DS ≥ V_GS − V_th` (MOS). The exam's favourite trap is an easy "saturation" assumption that is wrong.
- **Capacitors:** open for DC, short for midband AC. Any capacitor in a DC solution is an error.
- **Supplies become AC ground**; a bypassed emitter/source is AC ground. "Grounded" in the AC circuit ≠ "at 0 V DC".
- **`R_in` excludes the source resistance.** If the question wants the gain from the source, use `A_vs = A_v·R_in/(R_in+R_s)`.
- **Bypassed vs unbypassed** `R_E`/`R_S` flips the gain between `−gm·R` and `≈−R/R_E`, and multiplies `R_in` by `β+1`.
- **Don't forget `ro`/`V_A` when it is given** — the exam gives it precisely because it wants it. Including it *lowers* the gain and `R_out`.
- **The bypass-cap resistance is `re + R_B/(β+1)`, not `R_E`.** A factor-4 error if you get it wrong.
- **Reuse of a nominal β.** Use `β_min` for anything involving `rπ` or bias current; `A_v` needs only `gm`.

## Final recall drill (do in 60 seconds)

1. The four steps? → *DC Q-point → small-signal params → AC equivalent → solve.*
2. Capacitors in DC / midband AC? → *open / short.*
3. DC supplies in the AC circuit? → *grounded (AC ground).*
4. `gm`, `rπ`, `re`, `ro`? → *`I_C/V_T`, `β/gm`, `V_T/I_E`, `V_A/I_C`.*
5. `gm` at `I_C = 1 mA`? → *40 mA/V (`gm = 40·I_C[mA]`).*
6. `A_v` of a bypassed CE / CS? → *`−gm(R_C∥R_L)` / `−gm(R_D∥R_L)`.*
7. `R_in` of CE, bypassed / unbypassed? → *`R_b∥rπ` / `R_b∥(β+1)(re+R_E)`.*
8. `R_in` of a CS stage? → *the gate network `R_G` (gate draws no current).*
9. BJT active-region test? → *`V_C > V_B > V_E`.*
10. MOS saturation test? → *`V_DS ≥ V_GS − V_th`.*
11. Bypass-cap `R_eq`? → *`re + R_B/(β+1)`.*
12. Miller capacitance? → *`C_μ(1 + |A_v|)`, inverting stages only.*
