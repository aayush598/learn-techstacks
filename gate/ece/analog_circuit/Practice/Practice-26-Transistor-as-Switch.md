# Transistor as a Switch — Practice (Learn by Solving)

> **The idea in one line:** a transistor switch has only two useful states —
> **cutoff** (open, `V_CE ≈ V_CC`) and **saturation** (short, `V_CE ≈ 0.2 V`) —
> and every switching question is really the same three arithmetic steps:
> find `I_C(sat)`, compute the base drive, compare `β·I_B` against `I_C(sat)`.
>
> **How to use:** solve each question fully before reading the answer. Cover the
> **Answer**/**Method** with paper, do it, then reveal. If you miss one, solve
> the next 3 in the file to lock the pattern. No need to read the chapter notes
> first — every concept is taught through the drill itself. Open
> `26-Transistor-as-Switch.md` or `32-Single-File-Cheatsheet.md` only when you
> want the underlying theory.

## Concept box (what you must internalise)

- **OFF = cutoff:** no base current, `I_C = 0`, `V_CE ≈ V_CC`. The "open switch".
- **ON = saturation:** both junctions forward, `V_CE(sat) ≈ 0.2 V` (silicon) —
  **not 0**. `I_C(sat) = (V_CC − 0.2)/R_C`.
- **The one test:** `β·I_B ≥ I_C(sat)` → saturated. If it fails, the transistor is
  in the active region and `V_CE` is *not* 0.2 V. Forced β `= I_C/I_B`; design
  with forced β ≈ 5–10 so real β variation cannot knock you out of saturation.
- **MOSFET switch:** OFF for `V_GS < V_th`; ON means driving into the **triode**
  region, where `R_ds(on) = 1/[k(V_GS − V_th)]`. Gate current is **zero**.
- **Turn-off is the slow direction for a BJT:** excess stored minority charge in
  the base must be removed — that delay is the **storage time**. A MOSFET has no
  minority carriers, so it turns off much faster.
- **Method:** three lines, always in this order — (1) `I_C(sat) = (V_CC−0.2)/R_C`,
  (2) `I_B = (V_in − 0.7)/R_B`, (3) compare `β·I_B` with `I_C(sat)`. Then state
  `V_out` = 0.2 V (saturated) or `V_CC − βI_B·R_C` (active).
- **Trap:** `V_CE(sat)` is 0.2 V, not 0; and the BJT is saturated only if the
  base is driven *harder* than the collector load demands.

---

## Questions

### Q1. (Easy) Name the two regions in which a BJT must be operated to act as a switch, and the `V_CE` in each.
**Answer:** **Cutoff** (OFF): `I_C = 0`, `V_CE ≈ V_CC`. **Saturation** (ON): `V_CE ≈ 0.2 V` for a silicon device.
**Method:** "Switch" means the transfer characteristic is used as a step, so only the two flat parts of the curve count. The active region in between is the *amplifier* region — using it in a switch wastes power (`V_CE·I_C` is large there) and slows the edges. Source: `26-Transistor-as-Switch.md` §26.1.

### Q2. (Easy) Write the saturation current of a BJT switch with `V_CC = 10 V` and `R_C = 1 kΩ`.
**Answer:** `I_C(sat) = (V_CC − V_CE(sat))/R_C = (10 − 0.2)/1 kΩ = 9.8 mA`.
**Method:** Always subtract the saturation drop; the difference between 10 mA and 9.8 mA is exactly the mark GATE uses to check whether you remembered the 0.2 V. Source: `26-Transistor-as-Switch.md` §26.1.

### Q3. (Easy) What is the condition for a BJT to be in saturation, in terms of `I_B` and `I_C(sat)`?
**Answer:** `β·I_B ≥ I_C(sat)`, equivalently `I_B ≥ I_C(sat)/β`. Drive the base *harder* than the load demands.
**Method:** `β·I_B` is the largest collector current the base charge can support. If that exceeds what the collector circuit can pull, the transistor must saturate. Design margin = use `β_min`, or equivalently pick a **forced β** of 5–10. Source: `26-Transistor-as-Switch.md` §26.1.

### Q4. (Easy) In which MOSFET region is a MOSFET used as a switch when ON, and what is the corresponding `R_ds(on)`?
**Answer:** The **triode (linear)** region: `R_ds(on) = 1/[k·(V_GS − V_th)]`.
**Method:** This is the exact inverse of the amplifier usage, where a MOSFET runs in **saturation** as a current source. "MOSFET ON ⇒ triode; MOSFET amplifier ⇒ saturation" is a two-second GATE mark if you can state it cleanly. Source: `26-Transistor-as-Switch.md` §26.2.

### Q5. (Easy) Which switches faster at turn-off, a BJT or a MOSFET, and why?
**Answer:** The **MOSFET**. A saturated BJT stores excess minority charge in its base which must be swept out before the collector current falls — the **storage time**. A MOSFET has no minority carriers (it is a majority-carrier device), so its turn-off is limited only by capacitances.
**Method:** Name the mechanism, not just the device. "Storage time / stored base charge" is the answer GATE wants; "MOSFETs are faster because…" is not. Source: `26-Transistor-as-Switch.md` §26.3.

### Q6. (Easy) A BJT switch has `V_CC = 5 V`, `R_C = 1 kΩ`, `R_B = 10 kΩ`, `β = 100`. With `v_in = 0 V` and with `v_in = 5 V`, give `v_out` in each case.
**Answer:** `v_in = 0` → `I_B = 0` → cutoff → `v_out = V_CC = 5 V`. `v_in = 5` → `I_B = 4.3/10k = 430 µA`; `βI_B = 43 mA`; `I_C(sat) = 4.8/1k = 4.8 mA`; `43 ≫ 4.8` → saturated → `v_out = 0.2 V`.
**Method:** Run the three-line test twice, once per input state. This is the **inverter** truth table: 0 in → 5 V out, 5 V in → 0.2 V out. Source: `26-Transistor-as-Switch.md` §26.1.

### Q7. (Easy) A MOSFET switch has `k = 1 mA/V²`, `V_th = 1 V` and is driven with `V_GS = 5 V`. Compute `R_ds(on)`.
**Answer:** `R_ds(on) = 1/[k(V_GS − V_th)] = 1/[(10⁻³)(5−1)] = 1/(4×10⁻³) = 250 Ω`.
**Method:** Keep the units straight: `k` in A/V² means `k(V_GS−V_th)` is in A/V, and its reciprocal is in Ω. `250 Ω` is a *weak* switch — a real power MOSFET has a far larger `k` (or a bigger W/L), e.g. `k = 0.2 A/V²` with `V_GS = 5 V, V_th = 2 V` gives `1/(0.2×3) = 1.67 Ω`. Source: `26-Transistor-as-Switch.md` §26.2.

### Q8. (Easy) Why does a MOSFET switch need (almost) no steady input current, while a BJT switch needs base current?
**Answer:** The MOSFET **gate** is insulated and is charged only during switching: steady-state `I_G = 0`, so gate drive power is just the switching loss `≈ C_iss·V_GS²·f`. A BJT needs a continuous `I_B` to hold the base charge, so it burns `V_BE·I_B` continuously (e.g. `0.7 V × 0.5 mA = 0.35 mW`).
**Method:** Control terminal = "voltage-controlled, no DC current" for MOS; "current-controlled" for BJT. That single difference is why power supplies and motor drives use MOSFETs. Source: `26-Transistor-as-Switch.md` §26.2.

### Q9. (Easy) A BJT switch has `V_CC = 10 V`, `R_C = 1 kΩ`, `β_min = 50`, `v_in = 5 V`, `V_BE = 0.7 V`. Find the minimum `I_B`, then `R_B` for a comfortable `I_B = 0.5 mA`, and state the nearest standard value.
**Answer:** `I_C(sat) = 9.8 mA`; `I_B(min) = 9.8 mA/50 = 196 µA`; `0.5 mA` gives forced β `= 9.8/0.5 = 19.6` (safe margin); `R_B = (5 − 0.7)/0.5 mA = 4.3/0.5m = 8.6 kΩ` → nearest standard **8.2 kΩ** (which gives slightly *more* current: `4.3/8.2k = 524 µA`).
**Method:** `I_C(sat) → I_B(min) → pick a larger `I_B` → `R_B = (v_in − 0.7)/I_B`. When you round `R_B` **down** to a standard value you increase `I_B`, which is the safe direction. Source: `26-Transistor-as-Switch.md` §26.4.

### Q10. (Easy) A BJT switch has `V_CC = 10 V`, `R_C = 1 kΩ`, `β = 100`. Find the base resistor for a forced β of exactly 10, and give the resulting collector current and `V_CE`.
**Answer:** `I_C(sat) = 9.8 mA`; `I_B = 9.8 mA/10 = 980 µA`; `R_B = 4.3/980µ = 4.39 kΩ`. Then `βI_B = 98 mA ≫ 9.8 mA` → saturated, so `I_C = 9.8 mA` and `V_CE = 0.2 V`.
**Method:** Forcing β = 10 means the transistor carries 10× more "possible" collector current than the load needs, so saturation is guaranteed even if β doubles. Note `I_C` is set by the *load*, not by the base — overdriving the base raises `V_BE`, not `I_C`. Source: `26-Transistor-as-Switch.md` §26.1.

### Q11. (Easy) In the inverter of Q6 (`V_CC = 5 V`, `R_C = 1 kΩ`, `R_B = 10 kΩ`, `β = 100`), find the input voltage at which the transistor just leaves the active region and saturates.
**Answer:** Saturation needs `I_B = I_C(sat)/β = 4.8 mA/100 = 48 µA`; `v_in = 0.7 + 48 µA × 10 kΩ = 0.7 + 0.48 = 1.18 V`.
**Method:** Work backwards from the saturation boundary: required `I_B` → drop across `R_B` → add `V_BE`. This number is the inverter's "worst-case input low" limit; anything above 1.18 V guarantees a valid logic LOW output. Source: `26-Transistor-as-Switch.md` §26.1.

### Q12. (Moderate) The same inverter (`V_CC = 5 V`, `R_C = 1 kΩ`, `R_B = 10 kΩ`, `β = 100`) is fed `v_in = 1.0 V`. What is the output voltage, and is the device saturated?
**Answer:** `I_B = 0.3/10k = 30 µA`; `βI_B = 3 mA`; `I_C(sat) = 4.8 mA`. Since `3 < 4.8`, the device is in the **active** region: `I_C = 3 mA`, `v_out = 5 − 3 mA × 1 kΩ = 2.0 V`. `V_CE = 2 V` is nowhere near 0.2 V.
**Method:** Run the test; if it fails, fall back to `I_C = βI_B` and `v_out = V_CC − I_C·R_C`. A 2 V "low" output is not a valid logic level — this is why switch design is all about the margin in Q10. Source: `26-Transistor-as-Switch.md` §26.1.

### Q13. (Moderate) A BJT switch drives an LED from `12 V`: `V_LED = 2 V`, `R = 1 kΩ`, transistor saturated (`V_CE(sat) = 0.2 V`), `β = 100`, `v_in = 5 V`. Find the LED current, the minimum `I_B`, and `R_B` for a forced β of 10.
**Answer:** `I_LED = (12 − 2 − 0.2)/1 kΩ = 9.8 mA`; `I_B(min) = 98 µA`; for forced β = 10, `I_B = 0.98 mA`; `R_B = 4.3/0.98m = 4.39 kΩ` → 4.7 kΩ standard.
**Method:** The series chain is `V_supply → drop → R → load`. Subtract **both** the LED drop and `V_CE(sat)`: `(12 − 2 − 0.2)/1k`. Forgetting the 0.2 V gives 10 mA instead of 9.8 mA. Source: `26-Transistor-as-Switch.md` §26.1.

### Q14. (Moderate) Compute the power dissipated in the transistor in the two states of the switch: `V_CC = 10 V`, `R_C = 1 kΩ` saturated, and (for contrast) the same device biased in the *active* region at `V_CE = 5 V`, `I_C = 4.9 mA`.
**Answer:** Saturated: `P = V_CE(sat)·I_C = 0.2 × 9.8 mA = 1.96 mW`. Active: `P = 5 × 4.9 mA = 24.5 mW`. Ratio ≈ 12.5×.
**Method:** `P = V_CE·I_C` in both cases; only the operating point changes. Heat is the price of using the linear region in a switch, and it is why saturation (and BJT switches generally) needs a heat sink in power applications. Source: `26-Transistor-as-Switch.md` §26.1.

### Q15. (Moderate) A MOSFET switch has `k = 0.2 A/V²`, `V_th = 2 V`, `V_GS = 5 V`, in series with `R_D = 20 Ω` from a `12 V` supply. Find `R_ds(on)`, the on-current, `V_DS`, and the device loss.
**Answer:** `R_ds(on) = 1/(0.2×3) = 1.67 Ω`; `I_D = 12/(20 + 1.67) = 0.554 A`; `V_DS = 0.554 × 1.67 = 0.92 V`; `P = V_DS·I_D = 0.92 × 0.554 = 0.51 W`. Region check: `V_DS = 0.92 V < V_GS − V_th = 3 V` → triode ✓, so the `R_ds(on)` model was self-consistent.
**Method:** Treat the ON MOSFET exactly like a resistor: `I = V/(R_D + R_on)`, `V_DS = I·R_on`, `P = I²R_on`. Always finish with the region check — if `V_DS` came out *larger* than `V_GS − V_th`, you were really in saturation and the resistor model is invalid. Source: `26-Transistor-as-Switch.md` §26.2.

### Q16. (Moderate) A BJT switch turns ON in `t_on = 40 ns` and OFF in `t_off = 220 ns`, where `t_off = t_s + t_f` with storage time `t_s = 200 ns`. What fraction of the turn-off time is storage time, and what does it tell you about the design?
**Answer:** `200/220 = 91%` of the turn-off is storage time. So the BJT is *not* slow at switching itself — it is slow at **letting go of base charge**. Reducing the excess base drive shrinks `t_s`.
**Method:** Split the timing budget: `t_off = t_s + t_f`, `t_on = t_d + t_r`. If `t_s` dominates, the fixes are (a) less overdrive, (b) a turn-off path (resistor from base to emitter) so base current can reverse, or (c) a speed-up/Baker clamp. Source: `26-Transistor-as-Switch.md` §26.1.

### Q17. (Moderate) A relay coil is 5 V / 70 mA (`R_coil ≈ 71.4 Ω`) switched by a BJT whose `β = 20` (relay transistors are deliberately low-β) and `V_CE(sat) = 0.2 V`, driven from 5 V through `R_B`. Find `I_B(min)` and `R_B` for a forced β of 5.
**Answer:** `I_B(min) = 70 mA/20 = 3.5 mA`; `I_B = 70 mA/5 = 14 mA`; `R_B = (5 − 0.7)/14 mA = 4.3/14m = 307 Ω` → 330 Ω standard.
**Method:** Relays and solenoids draw huge current from a *low-β* device, so the base drive dominates the design. Note the base supply here is only 5 V, the same as the coil — the drive is barely adequate, which is exactly why a Darlington or a logic-level FET is preferred. Source: `26-Transistor-as-Switch.md` §26.1.

### Q18. (Moderate) In the relay circuit of Q17, what is the voltage at the transistor's collector just after the transistor turns off, and what happens without the flyback diode?
**Answer:** The coil current cannot change instantly, so it keeps flowing in the same direction (from the `+5 V` rail, down through the coil, into the collector). That forces the collector node **above** the rail, which forward-biases the diode (anode at the collector, cathode at `+5 V`): the collector clamps at `V_supply + V_F ≈ 5 + 0.7 = 5.7 V`, and the diode itself carries the current with a **0.7 V forward** drop, not a reverse voltage. The coil sees `−5.7 V` (a reversal of the `+5 V` it had). **Without the diode** nothing clamps the node: the collector rises toward the full coil back-EMF, well above the 5 V rail and past a typical `V_CEO` of 5–7 V, and the transistor avalanches — repeatedly, for every turn-off.
**Method:** Two things to separate that students routinely merge: the *diode's* voltage (forward, ≈`0.7 V`, because the diode is the clamp) and the *voltage the circuit forces across the switch* (the back-EMF, here ≈`5.7 V`). A flyback diode's *reverse* rating is set by other topologies (or by a series supply on the cathode), not by this circuit — here the diode is deliberately operated in its forward conduction to absorb the stored energy. Source: `26-Transistor-as-Switch.md` §26.1.

### Q19. (Moderate) Two NPN transistors are stacked in series as switches between `5 V` and ground, each with `1 kΩ` in its collector path. What collector current flows when the input is high, and what base current does the *bottom* transistor need?
**Answer:** Total collector resistance is `2 kΩ`, so `I_C(sat) = (5 − 0.2)/2 kΩ = 2.4 mA` — and *each* transistor carries the full 2.4 mA. The bottom device needs `I_B ≥ 2.4 mA/β` (e.g. 24 µA at β = 100).
**Method:** Series switches add their resistances: `R_total = ΣR_C`. The current is the same through both (series path), so each transistor must be sized for the *total* current, not half of it. Source: `26-Transistor-as-Switch.md` §26.1.

### Q20. (Moderate) A complementary push-pull (class-B) output stage is driven with `v_in = ±5 V`. What are the output levels, what is the total output swing, and what is the "dead zone"?
**Answer:** With `V_BE = 0.7`, the high level is `5 − 0.7 = 4.3 V` and the low level is `−5 + 0.7 = −4.3 V`; total swing **8.6 Vpp**. The dead zone is the input interval `−0.7 < v_in < +0.7` (1.4 V wide) in which *neither* transistor conducts, producing **crossover distortion**.
**Method:** Trace the two devices separately. The upper NPN turns on when `v_in > +0.7`; the lower PNP when `v_in < −0.7`. In between, the output is floating and the load holds it near 0 → the notch at the crossing. Source: `26-Transistor-as-Switch.md` §26.3.

### Q21. (Moderate) A Darlington pair of two identical BJTs (`β = 100` each) is used as a switch. Give the effective current gain and the effective `V_CE(sat)`.
**Answer:** `β_total = β₁·β₂ = 100 × 100 = 10⁴`; `V_CE(sat) ≈ V_CE(sat1) + V_BE2 = 0.2 + 0.7 = 0.9 V`.
**Method:** Two "costly" prices for the gain: a 0.9 V drop instead of 0.2 V (wasted power, `P = 0.9·I_C`) and a slower turn-off (twice the stored charge). The right answer to "why not always use a Darlington?" is those two costs. Source: `26-Transistor-as-Switch.md` §26.1.

### Q22. (Moderate) A CMOS inverter is built from a pMOS and an nMOS with `V_GS = 5 V` and `V_th = 1 V` for both. Give the two output levels for `v_in = 0` and `v_in = 5 V`, and the static supply current in each state.
**Answer:** `v_in = 0`: pMOS on (`V_GS = −5 V`, `|V_GS| ≫ V_th`), nMOS off → `v_out ≈ 5 V`. `v_in = 5 V`: nMOS on, pMOS off → `v_out ≈ 0 V`. In **both** steady states the supply current is ≈ 0 (only leakage), because a CMOS inverter has no static path from `V_DD` to ground.
**Method:** The two devices are complementary, so exactly one conducts in each state. That is the "CMOS inverter draws no static power" property — the reason CMOS dominates digital logic. Source: `26-Transistor-as-Switch.md` §26.2, `26.3` table.

### Q23. (Moderate) A switch node drives a 1 nF load capacitance through a switch whose on-resistance is 100 Ω. Estimate the 10–90% rise time and say which device type suits this better.
**Answer:** `t_r ≈ 2.2·R·C = 2.2 × 100 × 1 nF = 220 ns`. A **MOSFET** suits capacitive loads better: no storage time, and no continuous base current.
**Method:** `t ≈ 2.2RC` is the standard first-order rise-time estimate; use `R_on` (switch resistance + line resistance). Combine with Q5: for *capacitive* loads the RC edge dominates and the BJT's storage time is an extra penalty. Source: `26-Transistor-as-Switch.md` §26.1.

### Q24. (Moderate) A MOSFET switch is driven at 100 kHz through a gate capacitance `C_iss = 1 nF` with a 5 V swing. Estimate the switching (gate-charge) loss per device, per charging edge, and for a half bridge.
**Answer:** Energy per transition `= ½C_iss·V_GS² = ½ × 1 nF × 25 = 12.5 nJ`. There are `2f = 200k` transitions per second (charge **and** discharge), so `P = 12.5nJ × 200k = **2.5 mW** per device`. Per charging edge alone it is `½C V²f = 1.25 mW`. A half bridge has two such devices, so the bridge's total gate-drive loss is `2 × 2.5 = 5 mW`.
**Method:** `P_gate = C_iss·V_GS²·f` (both edges), or `Qg·V_GS·f` in the data-sheet form. The classic source of a factor-2 error here is forgetting that the *discharge* edge also dissipates `½CV²` in the driver. Note the *static* gate power is zero — 100% of MOSFET drive loss is dynamic, and it grows linearly with frequency, so gate drive becomes the dominant loss in a fast switch. Source: `26-Transistor-as-Switch.md` §26.2.

### Q25. (Moderate) Verify by measurement: a switch is measured with `I_C = 10 mA` and `I_B = 0.15 mA` (β = 100) and `V_CC = 12 V`, `R_C = 1.2 kΩ`. Is it saturated, and what is `V_CE`?
**Answer:** `I_C(sat) = (12 − 0.2)/1.2 kΩ = 9.83 mA`; `β·I_B = 15 mA > 9.83 mA` → **saturated**; `V_CE ≈ 0.2 V`; `I_C = 9.83 mA` (not 10 mA — the load sets it).
**Method:** The measurement must be self-consistent: the stated `I_C` and the computed `I_C(sat)` should agree once you know the state. If they disagree badly, your assumed state is wrong. The test is always `βI_B vs I_C(sat)`. Source: `26-Transistor-as-Switch.md` §26.1.

---

### Q26. (GATE-level) A BJT switch has `V_CC = 12 V`, `R_C = 2.2 kΩ`, `β = 100`, `V_BE = 0.7 V`, `R_B = 47 kΩ`, `v_in = 5 V`. Find the state, the forced β, `V_CE` and the device loss. Then `R_B` is mistakenly changed to 100 kΩ — what happens?
**Answer:** `I_B = 4.3/47k = 91.5 µA`; `βI_B = 9.15 mA`; `I_C(sat) = 11.8/2.2k = 5.36 mA`; `9.15 > 5.36` → **saturated**. Forced β = `5.36/0.0915 = 59`; `V_CE = 0.2 V`; `P = 0.2 × 5.36 mA = 1.07 mW`. With `R_B = 100 kΩ`: `I_B = 43 µA`, `βI_B = 4.3 mA < 5.36 mA` → **active**, `I_C = 4.3 mA`, `v_out = 12 − 4.3 mA × 2.2 kΩ = 2.54 V`. The "switch" no longer switches: 2.54 V is not a valid logic LOW and the swing collapses.
**Method:** The two-line comparison `βI_B` vs `I_C(sat)` decides everything; the state then fixes both the output voltage and the loss. GATE loves a single changed resistor that silently moves the device out of saturation — always re-run the test after any value change. Source: `26-Transistor-as-Switch.md` §26.1.

### Q27. (GATE-level) For the switch of Q26 (`I_C(sat) = 5.36 mA`, `V_in = 5 V`, `V_BE = 0.7 V`, `β = 100`), find the **largest** `R_B` that still guarantees saturation. What input voltage would be needed if `R_B` were 100 kΩ?
**Answer:** `I_B(min) = 5.36 mA/100 = 53.6 µA`; `R_B(max) = 4.3/53.6 µA = 80.2 kΩ` — so any `R_B ≤ 80 kΩ` saturates. With `R_B = 100 kΩ` you would need `v_in = 0.7 + 53.6 µA × 100 kΩ = 0.7 + 5.36 = 6.06 V`, which exceeds the 5 V supply — **impossible**. The 100 kΩ design can never saturate from a 5 V drive.
**Method:** `R_B(max) = (v_in − 0.7)·β/I_C(sat)`. The "impossible drive voltage" test is the sharpest way to expose an over-large base resistor: if the required `v_in` exceeds the rail, no valid design exists. Source: `26-Transistor-as-Switch.md` §26.1.

### Q28. (GATE-level) A TTL-style NAND uses two NPN switches in series, `1 kΩ` each, from `5 V`, with the bottom transistor's base driven from the *top transistor's collector*. When the top transistor is hard on, what happens to the bottom transistor?
**Answer:** The top transistor saturates, so its collector (= the bottom transistor's base) sits at `V_CE(sat) ≈ 0.2 V`. The bottom transistor then sees `V_BE = 0.2 V < 0.7 V` and **cannot turn on at all** — no base current, `I_C = 0`, the output never goes low. The series (stacked) BJT NAND cannot pull down properly; this is the fundamental structural weakness of the bipolar series stack.
**Method:** Chain the states: top saturated ⇒ node at 0.2 V ⇒ bottom `V_BE` too small ⇒ bottom in cutoff. The general lesson: in a bipolar series stack the *lower* device's drive is attenuated by the upper device's `V_CE(sat)`. The fix in real TTL is the multi-emitter input, which avoids stacking. Source: `26-Transistor-as-Switch.md` §26.1.

### Q29. (GATE-level) A switch design must not exceed `1 mW` in the transistor. `V_CC = 10 V`, `R_C = 2 kΩ` (proposed), `V_CE(sat) = 0.2 V`, `V_in = 5 V`, `β = 100`. Find the **smallest** `R_C` that keeps the saturated loss under 1 mW, then the `R_B` that saturates it. (Note: *larger* `R_C` only reduces the loss, so the interesting bound is the minimum.)
**Answer:** `P = 0.2·I_C`, so `I_C ≤ 1 mW/0.2 V = 5 mA`; `I_C = (10−0.2)/R_C ≤ 5 mA` → `R_C ≥ 9.8/5m = 1.96 kΩ` → use **2.2 kΩ** (gives `I_C = 4.45 mA`, `P = 0.89 mW`). Then `I_B(min) = 4.45 mA/100 = 44.5 µA`; for a forced β of 10, `I_B = 0.445 mA`; `R_B = 4.3/0.445m = 9.65 kΩ` → 10 kΩ.
**Method:** Work from the *specification* backwards: loss limit → maximum `I_C` → **minimum** `R_C` → the base drive that saturates it. This "specification first" ordering is what distinguishes a designed answer from a guessed one — and getting the inequality direction right is the whole question, since a rising `R_C` monotonically *reduces* both current and loss. Source: `26-Transistor-as-Switch.md` §26.1.

### Q30. (GATE-level) A BJT switch is driven from a source with `R_s = 1 kΩ` into `R_B = 10 kΩ`, `v_sig = 5 V`. What fraction of the available base drive actually reaches the base, and why does that matter for the saturation test?
**Answer:** The base sees a divider: `v_B = 5 × 10k/(10k + 1k) = 4.545 V`, so `I_B = (4.545 − 0.7)/10k = 384.5 µA` — only 89.5% of the `430 µA` an ideal 5 V source would give. With `β = 100`, `βI_B = 38.5 mA`; the design target of ~5 mA is still met, so the switch still saturates — but with a source resistance you must include the divider *before* running the saturation test.
**Method:** Never assume the gate/base node sees the full source voltage. Insert the source resistance, form the divider with `R_B` (or `R_B ∥ rπ` in the linear case), then compute `I_B`. This is the switch-side twin of the "kill the source, then attenuate" rule in `27-DC-and-AC-Analysis-Method.md`. Source: `26-Transistor-as-Switch.md` §26.1, `27-DC-and-AC-Analysis-Method.md` §27.3.

### Q31. (GATE-level) A "switch" uses the BJT in the **active** region on purpose (`V_CE = 5 V`, `I_C = 5 mA`) rather than saturated. Give the ratio of the on-state loss to the saturated-state loss for the same circuit, and explain why any competent design avoids this.
**Answer:** `P_active = 5 × 5 mA = 25 mW`; `P_sat ≈ 0.2 × 5 mA = 1 mW` → **25× more** heat. Worse, the transfer characteristic is now a ramp, so `v_out` is not a rail and the logic swing collapses — the device is no longer a switch at all.
**Method:** Two independent penalties for leaving saturation: dissipation and loss of the two-state (rail-to-rail) transfer. A switch problem that ends with `V_CE` near mid-supply is a design error, and the fix is always more base drive, never a smaller `R_B`. Source: `26-Transistor-as-Switch.md` §26.1.

### Q32. (GATE-level) The MOSFET switch of Q15 (`k = 0.2 A/V²`, `V_th = 2 V`, `V_GS = 5 V`, `R_D = 20 Ω`, `V_DD = 12 V`) dissipates 0.51 W. Compute the switch efficiency, then find the `R_ds(on)` that would give exactly 90% and the current at that point.
**Answer:** `I = 12/(20 + 1.667) = 0.554 A`; `P_in = 12 × 0.554 = 6.65 W`; `P_R = I²R_D = 0.554² × 20 = 6.14 W`; `η = 6.14/6.65 = 92.3%` (the missing 7.7% is the 0.51 W in the MOSFET), with `V_DS = 0.92 V`. For 90%: `V_DS` may be at most `0.1 × 12 = 1.2 V`. With `I = 12/(R_D + R_on)` and `I = 1.2/R_on`: `12R_on = 1.2(R_D + R_on)` → `10.8·R_on = 1.2×20` → **`R_on = 2.22 Ω`**, giving `I = 0.54 A`, `V_DS = 1.2 V`, `P_loss = 1.2 × 0.54 = 0.65 W`. Region check: `0.54 × 2.22 = 1.2 V < V_GS − V_th = 3 V` ✓ triode.
**Method:** `η = P_load/P_in = I·R_D/V_DD`, so the loss fraction is just `V_DS/V_DD`. Everything about a MOSFET switch's efficiency is the sentence *"the switch drop must be a few percent of the supply"*. That is why real power MOSFETs have `R_ds(on)` in milliohms and are driven with `V_GS` several volts above `V_th`. Source: `26-Transistor-as-Switch.md` §26.2.

### Q33. (GATE-level) Give the two complementary switch states of a CMOS inverter driving a load capacitance, and state the *dynamic* power per switching transition. Then say which of the two devices determines the ON resistance as `V_DD` scales down.
**Answer:** `v_in = 0` → pMOS on / nMOS off → `v_out = V_DD`; `v_in = V_DD` → nMOS on / pMOS off → `v_out = 0`. Dynamic energy per transition `= ½C_L·V_DD²` (two transitions per cycle → `C_L·V_DD²` per cycle), so `P = C_L·V_DD²·f`. As `V_DD` falls, `V_GS − V_th` shrinks, so `R_ds(on) = 1/[k(V_GS−V_th)]` **grows** — the nMOS on-resistance is the limiting factor and it degrades faster than the pMOS's (holes are 2–3× less mobile).
**Method:** Write the two states, then the `C·V²·f` energy, then the mobility asymmetry. The punchline for GATE: "CMOS dynamic power falls as `V_DD²` but `R_on` rises as `V_DD` falls" — the fundamental reason voltage scaling eventually stopped. Source: `26-Transistor-as-Switch.md` §26.2, `11-MOSFET-Fundamentals.md`.

### Q34. (GATE-level) A BJT switch has `I_B = 0.5 mA`, `β = 100`, `I_C(sat) = 9.8 mA`. Compute the **forced β**, the excess base charge (as a ratio of I_B to I_B(min)), and predict the effect on turn-off time. Then propose two circuit-level fixes.
**Answer:** Forced β = `9.8/0.5 = 19.6`; `I_B(min) = 98 µA`, so the overdrive is `0.5/0.098 = 5.1×`. The 5× excess charge must be removed at turn-off, so the storage time `t_s` is roughly proportional to the excess charge and dominates `t_off`. Fixes: (1) reduce `I_B` toward the minimum (at the cost of margin and slower `t_on`/lower noise immunity), (2) add a **turn-off path** — a resistor from base to emitter, or a Baker/speed-up clamp — so base charge can be swept out in reverse.
**Method:** Overdrive buys saturation margin but is paid for in turn-off speed; that trade-off is the central design tension of BJT switching. State it as "more `I_B` ⇒ safer saturation, worse `t_off`" and quote `t_off = t_s + t_f`. Source: `26-Transistor-as-Switch.md` §26.1.

### Q35. (GATE-level) A switch must work over `V_in = 0…5 V` with `V_CC = 5 V`, `R_C = 1 kΩ`, `β_min = 50`. Find the largest `R_B` that keeps the transistor saturated even at `v_in = 5 V`, and check whether `R_B = 10 kΩ` is acceptable.
**Answer:** `I_C(sat) = 4.8 mA`; `I_B(min) = 4.8/50 = 96 µA`; `R_B(max) = 4.3/96 µA = 44.8 kΩ`. So `R_B = 10 kΩ` is comfortably acceptable: it gives `I_B = 430 µA` and a forced β of `4.8/0.43 = 11` — 4.5× the minimum drive, so even with β varying from 50 to 150 the device stays saturated.
**Method:** Always design with `β_min`, not nominal β, and express the margin as a **forced β** so the reader can see it. The design is robust when the forced β is well below `β_min` (here 11 vs 50). Source: `26-Transistor-as-Switch.md` §26.1.

### Q36. (GATE-level) Summarise, in one comparison each, what changes if you replace a BJT switch with a MOSFET switch in the same circuit: (a) drive quantity, (b) ON drop, (c) turn-off speed, (d) region used when ON, (e) what happens with a bidirectional (AC) load.
**Answer:** (a) base **current** → gate **voltage**, zero steady gate current; (b) `V_CE(sat) ≈ 0.2 V` (fixed, and ~0.9 V for a Darlington) → `V_DS = I·R_ds(on)`, which falls with increasing current and with larger `k`; (c) BJT turn-off is **slow** (storage time) → MOSFET turn-off is **fast** (no minority carriers); (d) BJT ON = **saturation**, MOS ON = **triode**; (e) a BJT blocks reverse current, but a MOSFET has a **body diode** from source to drain, so it will conduct one direction even when "off" — the reason power designs add a blocking diode or a back-to-back pair.
**Method:** Five sub-answers, one mechanism each. If you can say (d) and (e) correctly you already own half the MOSFET-switch syllabus; (e) is the one students forget and it is a favourite one-mark question. Source: `26-Transistor-as-Switch.md` §26.2, §26.3, `15-BJT-vs-MOSFET.md`.

---

## Trap box (exam-day killers)

- **`V_CE(sat)` is 0.2 V, not 0.** `I_C(sat) = (V_CC − 0.2)/R_C`. Using `V_CC/R_C` is a 2% error that is exactly how a 0.2 V transistor drop gets "checked".
- **Always run `β·I_B ≥ I_C(sat)`.** If it fails you are in the active region and `V_CE` is *not* 0.2 V — and your `v_out` is not a rail.
- **Overdriving the base does not raise `I_C`.** The load sets `I_C`; extra base current only buys margin (and costs turn-off speed).
- **MOSFET ON = triode, BJT ON = saturation.** Swapping these two is the classic device-comparison slip.
- **A saturated BJT has stored charge** — turn-off (storage time) is the slow direction; MOSFETs win at switching.
- **The body diode makes an "off" MOSFET conduct one way.** Relevant to any AC or bidirectional load.
- **`R_ds(on) = 1/[k(V_GS − V_th)]`** needs `k` in A/V². With `k` in mA/V² you must convert, or your ohms value is 1000× wrong.

## Final recall drill (do in 60 seconds)

1. BJT OFF condition and `V_CE`? → *cutoff, `I_B = 0`, `V_CE ≈ V_CC`.*
2. BJT ON condition and `V_CE`? → *saturation, `V_CE(sat) ≈ 0.2 V`.*
3. `I_C(sat)`? → *`(V_CC − 0.2)/R_C`.*
4. The saturation test? → *`β·I_B ≥ I_C(sat)`; design with forced β ≈ 5–10.*
5. MOSFET OFF / ON conditions? → *`V_GS < V_th` / `V_GS ≫ V_th` (triode).*
6. `R_ds(on)`? → *`1/[k(V_GS − V_th)]`.*
7. Which switches faster at turn-off, and why? → *MOSFET; a BJT must remove stored base charge (storage time).*
8. Inverter output levels? → *`V_CC` (cutoff) and `0.2 V` (saturated) — a logic inverter.*
9. Darlington: β and `V_CE(sat)`? → *`β₁β₂ = 10⁴`; `0.2 + 0.7 = 0.9 V`.*
10. MOSFET gate power? → *zero static; dynamic `≈ C_iss·V_GS²·f`.*
