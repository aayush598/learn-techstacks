# Diodes: Basics and Models — Practice (Learn by Solving)

> **The idea in one line:** this file teaches the whole of Chapter 02 through 40
> questions — you learn the models (`02-Diodes-Basics-and-Models.md`) by using
> them, not by reading them.
>
> **How to use:** solve each question fully before reading the answer. Cover the
> **Answer**/**Method** with paper, do it, then reveal. If you miss one, solve
> the next 3 in the file to lock the pattern. No need to read the chapter notes
> first — every concept is taught through the drill itself. Open
> `02-Diodes-Basics-and-Models.md` or `32-Single-File-Cheatsheet.md` only when
> you want the underlying theory.

## Concept box (what you must internalise)

- Shockley: `i_D = I_S·(e^{v_D/(n·V_T)} − 1)`; `V_T = kT/q = 25.9 mV @ 300 K`,
  and **GATE uses 25 mV**.
- Dynamic resistance: `r_d = n·V_T / I_D` → `≈ 25 mV / I_D` at `n = 1`. It is
  **inversely** proportional to current: 1 mA→25 Ω, 10 mA→2.5 Ω.
- Forward drop: Si `Vγ = 0.7 V`, Ge `Vγ = 0.3 V`. Series drops **add**.
- The four models: **Ideal** ON = short; **CVD** ON = 0.7 V battery; **PWL**
  ON = `Vγ + r_d·i_D`; **small-signal** = `Vγ` (DC) + `r_d` (AC).
- The ON/OFF test that unlocks every diode circuit: **remove the diode, compute
  `V_anode − V_cathode`; if positive it is ON.**
- 60 mV per decade: `e^(0.06/0.025) = e^2.4 = 11.0`. This single number lets you
  convert any known `I–V` point to a nearby one without a calculator.
- Reverse current: for `|v_D| ≫ nV_T`, `i_D ≈ −I_S` (nA/µA) — treat the diode
  as an **open circuit**. Zeners are the only diodes *meant* to run in breakdown.

---

## Questions

### Q1. (Easy) Find the thermal voltage `V_T = kT/q` at T = 300 K using `k = 1.38×10⁻²³ J/K` and `q = 1.6×10⁻¹⁹ C`. What value does GATE expect you to use?
**Answer:** 25.875 mV ≈ **25.9 mV**; GATE quotes **25 mV**.
**Method:** `V_T = kT/q = (1.38e-23 × 300)/1.6e-19 = 4.14e-21/1.6e-19 = 0.025875 V`.
Rule of thumb: `kT/q` is 25–26 mV for any "room temperature" (300–310 K) problem,
so memorise **25 mV** and move on. Every `r_d` and every Shockley exponent in the
exam uses it.

---

### Q2. (Easy) A germanium diode (Vγ = 0.3 V) is in series with a 500 Ω resistor across a 3 V source. Find the current. What would a silicon diode give instead?
**Answer:** Ge: `I = (3 − 0.3)/500 = 2.7/500 =` **5.4 mA**. Si: `(3 − 0.7)/500 = 4.6 mA**.
**Method:** CVD model — subtract the fixed drop, then Ohm's law:
`I = (V − Vγ)/R`. Whenever a problem says *germanium*, your brain must jump to
**0.3 V**, not 0.7 V. Difference here is `0.4/500 = 0.8 mA` — Ge always passes more
current at the same supply.

---

### Q3. (Easy) A silicon diode and a 1 kΩ resistor form a loop with a 5 V source. Find the current. Repeat with a germanium diode.
**Answer:** Si: `(5 − 0.7)/1k =` **4.3 mA**. Ge: `(5 − 0.3)/1k =` **4.7 mA**.
**Method:** Same one-line template as Q2 — memorise it as a *shape*:
`I = (V_source − n·Vγ)/R_total`. The `n` is the number of series diodes.

---

### Q4. (Easy) Three silicon diodes in series with a 3 kΩ resistor are connected to a 9 V battery. Find the current. Repeat with three germanium diodes.
**Answer:** Si: drops `3 × 0.7 = 2.1 V`, so `I = (9 − 2.1)/3k = 6.9/3000 =` **2.3 mA**.
Ge: drops `3 × 0.3 = 0.9 V`, so `I = (9 − 0.9)/3k = 8.1/3000 =` **2.7 mA**.
**Method:** Series diodes **add** their drops, then one Ohm's law for the whole
string. Write `ΣVγ` explicitly so you cannot forget one. Sanity check: with 2.1 V
of the 9 V gone, 2.3 mA is sensible.

---

### Q5. (Easy) Find `r_d` (n = 1, `V_T = 25 mV`) at `I_D` = 1 mA, 2 mA, 5 mA and 0.1 mA. State the trend.
**Answer:** 1 mA → **25 Ω**; 2 mA → **12.5 Ω**; 5 mA → **5 Ω**; 0.1 mA → **250 Ω**.
**Method:** `r_d = 25 mV / I_D`. Put everything in mA: `r_d[Ω] = 25/I_D[mA]`. The
trend is the examinable fact: **`r_d` halves when `I_D` doubles** — it is the
reciprocal relation GATE loves. Never use the AC current here; always the DC
operating current.

---

### Q6. (Easy) What happens to `r_d` if the ideality factor `n` goes from 1 to 2 at the same `I_D` = 2 mA?
**Answer:** `n = 1`: 12.5 Ω. `n = 2`: `2 × 25 mV / 2 mA =` **25 Ω** — it **doubles**.
**Method:** `r_d = n·V_T/I_D` is linear in `n`. A larger `n` means a softer
(exponential) junction, i.e. a shallower I–V slope, i.e. a *bigger* `r_d`. Same
`n` factor appears in the Shockley exponent, so `n` scales both the slope and the
exponential.

---

### Q7. (Easy) Using Shockley, `I_S = 10⁻¹⁴ A`, `n = 1`, `V_T = 25 mV`, find `i_D` at `v_D` = 0.7 V.
**Answer:** `i_D = 10⁻¹⁴·(e^(0.7/0.025) − 1) = 10⁻¹⁴·e²⁸ = 10⁻¹⁴ × 1.446×10¹² =` **14.46 mA ≈ 14.5 mA**.
**Method:** Divide the exponent first: `0.7/0.025 = 28`. `e²⁸ = 1.446×10¹²` (note
`e¹⁰ ≈ 2.2×10⁴`, `e²⁰ ≈ 4.85×10⁸`, so `e²⁸ = e²⁰·e⁸ = 4.85e8 × 2981`). The
`−1` term is utterly negligible next to 10¹², so drop it. *Careful: the self-check
at the end of `02-Diodes-Basics-and-Models.md` prints "≈1.4 mA" for this — that is
a factor-10 slip; the correct value is 14.5 mA.*

---

### Q8. (Easy) Same diode as Q7 (`I_S = 10⁻¹⁴`, `n = 1`). Find `i_D` at `v_D` = 0.65 V and at `v_D` = 0.60 V.
**Answer:** 0.65 V → `e²⁶ = 1.957×10¹¹` → **1.96 mA**.
0.60 V → `e²⁴ = 2.649×10¹⁰` → **265 µA**.
**Method:** Exponents 26 and 24. Use `e²⁶ = e²⁰·e⁶ = 4.85e8 × 403.4 = 1.96e11` and
`e²⁴ = 4.85e8 × 54.6 = 2.65e10`. Notice 0.65 → 0.60 (50 mV) already swings the
current by 7.4× — the knee is extremely steep, which is *why* the 0.7 V constant
drop model works at all.

---

### Q9. (Easy) A diode with `I_S = 1 nA` is reverse biased at 5 V. What reverse current flows? Can you neglect it in a KVL with a 5 V source and 1 kΩ?
**Answer:** `i_D = I_S(1 − e^{−|v_D|/nV_T})`; since `|v_D|/nV_T = 5/0.025 = 200 ≫ 1`,
`i_D ≈ −I_S = ` **−1 nA**. Yes, neglect it — it is 10⁶ times smaller than the
milliamp forward currents you will calculate.
**Method:** For `|v_D| > 4·nV_T ≈ 0.1 V`, the exponential in reverse is ~0, so the
current is flat at `I_S`. This is why "reverse biased ⇒ open circuit" is a legal
shortcut: 1 nA through 1 kΩ is 1 µV.

---

### Q10. (Easy) A problem states: *"the diode has cut-in voltage 0.6 V and forward
resistance 20 Ω."* Which of the four models must you use, and what is its
ON-state equation?
**Answer:** **Piecewise-linear (PWL)**: `v_D = 0.6 + 20·i_D` — a 0.6 V battery in
series with 20 Ω. OFF state = open circuit.
**Method:** Trigger words: *"cut-in voltage **and** forward/knee resistance"* ⇒ PWL.
*"Silicon"* alone ⇒ CVD 0.7. *"Qualitative / which waveform / sketch"* ⇒ ideal.
*"AC small-signal on a biased diode"* ⇒ CVD for DC + `r_d = 25 mV/I_D` for AC.
Always state the model in your answer script — it earns the method marks.

---

### Q11. (Moderate) `I_S = 10⁻¹⁴ A`, `n = 1`, `V_T = 25 mV`. Invert Shockley: what
`v_D` gives exactly 1 mA?
**Answer:** `v_D = nV_T·ln(1 + I/I_S) = 0.025 × ln(1 + 10¹¹) ≈ 0.025 × 25.328 =` **0.633 V**.
**Method:** Take logs: `ln(I/I_S) = v_D/nV_T` ⇒ `v_D = nV_T·ln(I/I_S)`.
`ln(10¹¹) = 11·ln10 = 11 × 2.3026 = 25.33`. Memorise the ladder:
0.1 mA→0.576 V, 1 mA→0.633 V, 10 mA→0.691 V. Each decade of current costs only
`25 mV × ln(10) = 57.6 mV` — the exponential is so steep that "0.7 V" is a good
average description.

---

### Q12. (Moderate) Same diode. What `v_D` gives 10 mA? What `v_D` gives 0.1 mA?
**Answer:** 10 mA: `0.025 × ln(10¹²) = 0.025 × 27.631 =` **0.691 V**.
0.1 mA: `0.025 × ln(10¹⁰) = 0.025 × 23.026 =` **0.576 V**.
**Method:** Same inversion, one more/one less decade = one more/less `ln(10) = 2.303`
in the exponent, i.e. `0.025 × 2.303 = 57.6 mV`. Span from 0.1 mA to 10 mA is
**115 mV** for a factor-100 in current. This is the "57.6 mV per decade" number.

---

### Q13. (Moderate) Same `I_S = 10⁻¹⁴`, but now `n = 2`. Find `i_D` at `v_D = 0.7 V`,
and the `v_D` that gives 1 mA.
**Answer:** `i_D = 10⁻¹⁴·(e^(0.7/0.05) − 1) = 10⁻¹⁴·e¹⁴ = 10⁻¹⁴ × 1.203×10⁶ =` **12.0 nA**.
For 1 mA: `v_D = 2 × 0.025 × ln(10¹¹) = 0.05 × 25.328 =` **1.266 V**.
**Method:** `n` halves the effective thermal voltage: 25 mV → 50 mV. At 0.7 V the
exponent collapses from 28 to 14, so the current drops by `e¹⁴ = 1.2×10⁶` — from
14.5 mA to 12 nA. `n ≈ 2` is a real effect for low-current, high-injection diodes;
it is why "0.7 V" is only an approximation.

---

### Q14. (Easy) With `n = 1`, `V_T = 25 mV`, by what factor does the forward current
change for every 10 mV increase in `v_D`? For every 60 mV?
**Answer:** per 10 mV: `e^(0.010/0.025) = e^0.4 =` **1.49×**; per 60 mV:
`e^(0.06/0.025) = e^2.4 =` **11.0×** (≈ one decade per 60 mV).
**Method:** `ΔI/I = e^(Δv/nV_T)`. Work in units of `nV_T` = 25 mV: 10 mV is 0.4
`V_T` (→ ×1.49), 60 mV is 2.4 `V_T` (→ ×11). This is the single most useful mental
tool for the exponential — it lets you extrapolate a given I–V point without
computing `e` anything.

---

### Q15. (Moderate) PWL diode with `Vγ = 0.6 V` and `r_d = 10 Ω` in series with a
1 kΩ resistor and a 5 V source. Find `I` and `v_D`.
**Answer:** `I = (5 − 0.6)/(1000 + 10) = 4.4/1010 = ` **4.36 mA**.
`v_D = 0.6 + 4.356 mA × 10 = 0.6 + 0.0436 =` **0.644 V**.
**Method:** PWL puts a resistor *in series with the diode*, so it goes into the
denominator with the external R. Then use the external resistor alone to get the
diode's drop increment. Note the drop is only 0.644 V, not 0.66 V, because some
voltage now appears across `r_d`.

---

### Q16. (Moderate) PWL diode, `Vγ = 0.7 V`, `r_d = 25 Ω`, external 1 kΩ, source
2 V. Find `I` and `v_D`.
**Answer:** `I = (2 − 0.7)/(1000 + 25) = 1.3/1025 = ` **1.27 mA**.
`v_D = 0.7 + 1.268 mA × 25 = 0.7 + 0.0317 =` **0.732 V**.
**Method:** Identical template to Q15. Notice the `r_d` contribution is small
(0.03 V here, 4% of the drop) because `r_d ≪ R` — that is *why* the CVD model
suffices for most silicon numericals.

---

### Q17. (Moderate) Silicon diode, 2 kΩ, 5 V supply ⇒ `I = 2.15 mA`. Now a
`±0.1 V`, 1 kHz sinusoid is superimposed. Find the AC current amplitude
(`n = 1`).
**Answer:** `r_d = 25 mV/2.15 mA =` **11.6 Ω**.
`i_ac = 0.1/(2000 + 11.6) = 0.1/2011.6 = ` **49.7 µA ≈ 50 µA**.
**Method:** Two-stage: (1) DC gives the operating current, (2) the AC sees `r_d`
in series with `R`, **not** `R` alone and **not** the static resistance. Notice the
AC current (50 µA) is 43× smaller than the DC current (2.15 mA) — the diode is a
one-way valve, so the negative half simply does not exist in the output. That
rectifying behaviour is Chapter 05.

---

### Q18. (Moderate) Trial-and-test Q-point. `V = 5 V`, `R = 1 kΩ`, Shockley diode
with `I_S = 10⁻¹⁴`, `n = 1`, `V_T = 25 mV`. The load line is `I = (5 − v_D)/1k`.
Find the intersection with the diode curve. (No closed-form solution — iterate.)
**Answer:** **`v_D ≈ 0.670 V`, `I ≈ 4.33 mA`.**
**Method:** Set `I_diode(v_D) = I_load(v_D)` and bracket `v_D`:
- `v_D = 0.60` → diode 0.265 mA, load 4.40 mA → diode smaller
- `v_D = 0.65` → diode 1.96 mA, load 4.35 mA → diode smaller
- `v_D = 0.67` → diode 4.36 mA, load 4.33 mA → diode slightly larger
- `v_D = 0.665` → diode 3.57 mA, load 4.34 mA → smaller
Intersection ≈ 0.669 V ⇒ `I ≈ 4.33 mA`. **The lesson: 4.33 mA with 0.67 V across
the diode is exactly what the 0.7 V CVD model predicts (4.3 mA)** — the
exponential model is self-consistent with the constant-drop shortcut, so use CVD
for speed and Shockley only when the problem hands you `I_S`.

---

### Q19. (Moderate) Ge diode (`Vγ = 0.3 V`), 3 V source, 500 Ω. Find `I_D`, `v_D`
and `r_d`.
**Answer:** `I_D = (3 − 0.3)/500 =` **5.4 mA**, `v_D = ` **0.3 V**,
`r_d = 25 mV/5.4 mA = ` **4.63 Ω**.
**Method:** CVD then `25/I_D[mA]`. Extra 0.4 V of drop compared with silicon means
extra current, hence *smaller* `r_d` — `r_d` follows the current, always.

---

### Q20. (Moderate) Write the DC load line for the 5 V / 1 kΩ diode circuit of Q18.
Give its two intercepts and the Q-point you found.
**Answer:** Line `i = (5 − v)/1000`; intercepts **(5 V, 0 mA)** and **(0 V, 5 mA)**;
Q-point **(0.67 V, 4.33 mA)** — a point very close to the knee.
**Method:** A load line through `(V, 0)` and `(0, V/R)` is the graphical form of
`I = (V − V_D)/R`. The Q-point sits at the intersection. Here the load line is
steep (V/R = 5 mA) relative to the diode's exponential, so the intersection
lands right at the 0.7 V knee — the graphical picture and the 0.7 V model agree.

---

### Q21. (Moderate) Zener regulator: `V_s = 12 V`, `V_z = 5.1 V`, series resistor
500 Ω, load 1 kΩ. Find `I_L`, `I_z` and confirm regulation.
**Answer:** `I_s = (12 − 5.1)/500 = 6.9/500 = ` **13.8 mA**;
`I_L = 5.1/1000 = ` **5.1 mA**; `I_z = 13.8 − 5.1 = ` **8.7 mA**.
**Method:** KCL at the Zener node: everything the series resistor supplies splits
into load + Zener. Regulation is valid only if `I_z` stays above `I_ZK(min) ≈ 5 mA`
(here 8.7 mA ✓) and below `I_Zmax`. If you ever get a *negative* `I_z`, the Zener
has gone off and `V_z` is **not** 5.1 V — that is the classic error to catch.

---

### Q22. (Moderate) `V_s = 20 V`, `V_z = 9 V`, `R_s = 200 Ω`, `I_ZK(min) = 5 mA`.
Find the **smallest** load resistance that keeps the Zener in regulation.
**Answer:** Maximum allowed `I_L = 13 mA − 5 mA = 8 mA` (since `I_s = 11/200 = 55 mA`).
`R_L(min) = 9 V / 8 mA =` **180 Ω**.
**Method:** Step 1: `I_s = (V_s − V_z)/R_s` (this is the *only* current the source
can deliver). Step 2: `I_L(max) = I_s − I_ZK(min)`. Step 3: `R_L(min) = V_z/I_L(max)`.
Trace it as a **design inequality**, not a number — GATE loves "find the minimum R".

---

### Q23. (Moderate) `V_s = 15 V`, `V_z = 10 V`, `R_s = 1 kΩ`, **no load**. Find `I_z`
and the Zener power dissipation.
**Answer:** `I_z = (15 − 10)/1000 = ` **5 mA**; `P_z = 10 × 5 mA = ` **50 mW**.
**Method:** With the load open, the full series current flows through the Zener —
the *worst* case is usually **no load**, not full load. Always check
`P_z ≤ P_Z(max)` (typically 500 mW for a 1N4744-class device) and
`I_z ≤ I_Zmax`.

---

### Q24. (Moderate) Diode diffusion capacitance: transit time `τ = 5 ns`, `I_D = 10 mA`,
`n = 1`. Find `g_d` and `C_d`. Repeat for `I_D = 2 mA`.
**Answer:** `g_d = 1/r_d = I_D/nV_T = 10 mA/25 mV = ` **0.4 S** ⇒ `C_d = τ·g_d = 5 n × 0.4 = ` **2 nF**.
At 2 mA: `g_d = 0.08 S` ⇒ `C_d = ` **0.4 nF**.
**Method:** `C_d = τ·dI/dV = τ·g_d = τ·I_D/(nV_T)`. Same 25 mV/25 mV pairing as
`r_d`. **Diffusion capacitance exists only in forward conduction and scales with
current** — the higher the current, the more the diode looks like a capacitor to
the signal. This is what limits rectification at high frequency.

---

### Q25. (Moderate) Transition capacitance: `C_j0 = 100 pF` at zero bias,
`V_J = 0.5 V`, grading coefficient `m = 0.5`. Find `C_j` at 5 V reverse bias.
**Answer:** `C_j = C_j0/(1 + V_R/V_J)^m = 100 pF/(1 + 5/0.5)^0.5 = 100/√11 = 100/3.3166 = ` **30.2 pF**.
**Method:** `C_T = C_j0/(1 + V_R/V_J)^m`. The rule: reverse bias **shrinks** the
junction capacitance (a wider depletion layer stores less charge for the same
voltage). So `C_T` dominates the reverse-biased (blocking) diode, and it *varies*
with the signal — the main non-linearity of a switching diode. Rule of thumb:
reverse-biased C falls roughly as `1/√V_R`.

---

### Q26. (Moderate) `I_S` doubles every 10 °C. It is 10 pA at 25 °C. Find `I_S` at
65 °C, and explain the consequence for a fixed 0.7 V bias.
**Answer:** ΔT = 40 °C ⇒ 4 doublings ⇒ `I_S = 10 pA × 2⁴ = ` **160 pA**.
Consequence: at a fixed `v_D`, `i_D` is directly proportional to `I_S`, so the `I_S`
contribution alone multiplies the current by **16×** — the classic thermal-runaway
mechanism in a series-biased diode. (With `V_T` also rising the true increase is
*larger* still, which is why the effect is so violent.)
**Method:** `I_S(new) = I_S(old) × 2^((T_new − T_old)/10)`. Both `I_S` and the
exponential slope (`V_T`) worsen with temperature, so leakage roughly doubles
every 10 °C. GATE loves asking "which quantity is strongly temperature dependent"
— the answer is `I_S`, not `Vγ`.

---

### Q27. (GATE-level) Circuit: 10 V source → 2 kΩ → node A → silicon diode
(anode at A, cathode at B) → node B → 1 kΩ → ground. Find `I`, `v_B`, `v_A`.
**Answer:** `I = (10 − 1.4)/(2000 + 1000) = 8.6/3000 = ` **2.87 mA**;
`v_B = 2.87 mA × 1 kΩ = ` **2.87 V**; `v_A = 2.87 + 0.7 = ` **3.57 V**.
**Method:** Apply the ON/OFF test from Q10 first: remove the diode; node A floats
to +10 V through 2 kΩ with node B at 0 ⇒ `v_A − v_B = +10 V` ⇒ anode positive ⇒
**ON**. Then KVL around the loop: both series resistors carry the same current,
`I = (V − ΣVγ)/ΣR`. Always run the test — here it is free, but in a bridge-type
circuit guessing ON/OFF costs marks.

---

### Q28. (GATE-level) A silicon diode (`Vγ = 0.7 V`) and a germanium diode
(`Vγ = 0.3 V`) are connected **in parallel**, in series with 1 kΩ, across 5 V. Which
conducts, and what is the current through it?
**Answer:** The **Ge diode hogs all the current**: `I_Ge = (5 − 0.3)/1k = ` **4.7 mA**,
`I_Si = ` **0** (reverse biased, since its 0.7 V drop cannot be sustained against
0.3 V).
**Method:** Parallel diodes with *unequal* `Vγ` do **not** share current. The
lower-`Vγ` device turns on first, clamps the shared node to its own 0.3 V, and
reverse-biases the other. Contrast with two matched Si diodes, which split equally.
Trap: students always halve the current.

---

### Q29. (GATE-level) 12 V source → 1 kΩ → node A → Si diode (0.7 V) → node B →
2 kΩ → ground. Find `I`, `v_B`, `v_A`.
**Answer:** `I = (12 − 0.7)/(1000 + 2000) = 11.3/3000 = ` **3.77 mA**;
`v_B = 3.77 mA × 2k = ` **7.53 V**; `v_A = 7.53 + 0.7 = ` **8.23 V**.
**Method:** Same template as Q27 — one KVL, then Ohm's law on the *downstream*
resistor only. Common slip: computing `v_B` from the upstream resistor (that would
give 3.77 V) — `v_B` is across the 2 kΩ, so use 2 kΩ.

---

### Q30. (GATE-level) Silicon diode forward drop falls about 2 mV per °C. A 5 V
source drives 1 kΩ with the diode at 25 °C. Find `I` and `r_d` at 100 °C.
**Answer:** `ΔT = 75 °C` ⇒ drop falls 150 mV ⇒ `Vγ = 0.7 − 0.15 = ` **0.55 V**.
`I = (5 − 0.55)/1k = ` **4.45 mA**; `r_d = 25 mV/4.45 mA = ` **5.62 Ω**.
**Method:** Two-step: correct the drop by −2 mV/°C (Q26's temperature theme, but
now on `Vγ` instead of `I_S`), then recompute current and `r_d`. Higher
temperature → lower drop → **more** current → **smaller** `r_d`. All three trends
point the same way, which is why thermal runaway happens.

---

### Q31. (GATE-level) `r_d = nV_T/I_D`. A diode carries 1 mA. Compare `r_d` at
T = 300 K and T = 600 K with `n = 1` and `I_D` held constant.
**Answer:** 300 K: `0.025/1m = ` **25 Ω**. 600 K: `kT/q = 1.38e-23 × 600/1.6e-19 = 51.75 mV`,
so `r_d = 51.75 mV/1 mA = ` **51.8 Ω** (≈ 52 Ω). It roughly **doubles**.
**Method:** `r_d ∝ nT/I_D`. If `I_D` is held constant by a *current* source, then
doubling T doubles `r_d`; if it is held by a *voltage* source plus series R, the
current also rises, which partly cancels the rise. State which constraint you
assumed — that is the mark-worthy part.

---

### Q32. (GATE-level) A 1.2 W Zener rated `I_Zmax = 50 mA` is used with
`V_s = 20 V`, `V_z = 8 V`, `R_s = 1 kΩ`, and **no load**. Is it safe?
**Answer:** `I_z = (20 − 8)/1000 = ` **12 mA**; `P_z = 8 × 12 mA = ` **96 mW**.
Safe on both counts: 12 mA < 50 mA and 96 mW < 1.2 W. (Excess dissipation is
handled by the −2 mV/°C knee shift, which keeps `V_z` nearly constant.)
**Method:** No load ⇒ *maximum* Zener current. Check **two** limits, current and
power; examiners alternate between them. `P_z = V_z·I_z` and `P_z ≤ P_Z(max)` is
the criterion; the `V_z` tolerance and the `k_z` temperature coefficient decide
the actual output accuracy.

---

### Q33. (GATE-level) Same Zener as Q21 (`V_s = 12 V`, `V_z = 5.1 V`,
`R_s = 500 Ω`) but the 1 kΩ load is **replaced by a short circuit**. What happens,
and what must you have checked first?
**Answer:** `I_z = (12 − 5.1)/500 = ` **13.8 mA** (the load current is 0). Safe if
`13.8 mA ≤ I_Zmax` and `5.1 × 13.8 mA = 71 mW ≤ P_Z(max)`. The check you must have
done first is the full-load case: the Zener was already at 8.7 mA, so the short is
a *small* increase. A Zener regulator's failure modes are a **shorted load** (handled: `i_z = 0` is just
the low-current end) and too much **source resistance** (not handled: `i_z` collapses
below `I_ZK` and the Zener leaves regulation entirely).
**Method:** The two extremes of a linear Zener regulator are **load open** (max
`I_z`) and **load shorted** (min `I_z` = 0 ⇒ **no regulation at all**). Design for
`I_ZK(min) ≤ I_z ≤ I_Zmax` at both ends.

---

### Q34. (GATE-level) A real diode has series bulk resistance `r_s = 20 Ω`. Its
junction `r_d` at the operating point is 12.5 Ω. What is the total small-signal
resistance seen by a small AC signal, and how does the PWL drop change?
**Answer:** `r_ac = r_s + r_d = 20 + 12.5 = ` **32.5 Ω** (series, so add).
PWL: `v_D = Vγ + I·(r_s + r_d)`; at 2 mA the resistive part is
`2 mA × 32.5 Ω = 65 mV` on top of `Vγ`.
**Method:** Everything resistive in the diode's forward path is in **series** —
add them. In the AC (small-signal) world the 0.7 V battery disappears (it is a DC
offset) and only resistances remain. So `r_d,total = r_s + nV_T/I_D`. This is why
the PWL model and the small-signal model are the *same* statement with different
resistances.

---

### Q35. (Moderate) Charge stored in a diode under steady forward current
`I_D = 10 mA` with transit time `τ = 5 ns`. How much excess charge, and what does it
imply for switching speed?
**Answer:** `Q = I_D·τ = 10 mA × 5 ns = ` **50 pC**. During turn-off this charge
must be swept out, giving a reverse-recovery delay `t_rr` — so a diode carrying
large current switches slowly.
**Method:** `Q = I·τ`, so stored charge scales with *current*. That is why
rectifier bridges for high-current supplies use large-area devices: bigger area ⇒
bigger `I` capability but longer `τ` and worse `t_rr`. The stored charge is why
"reverse recovery" limits how fast a diode can switch a large current.

---

### Q36. (GATE-level) Two Zeners rated 3.2 V and 75 V. Which breakdown mechanism
dominates in each, and what practical consequence does the mechanism have?
**Answer:** 3.2 V ⇒ **Zener (field-ionisation) breakdown** — a very sharp knee,
high voltage-temperature coefficient (the knee voltage *rises* with temperature).
75 V ⇒ **avalanche breakdown** — a rounded knee, **negative** temperature
coefficient. Consequence: mixing the two in a temperature-compensated reference
pair works because the two temperature coefficients have opposite signs.
**Method:** The textbook split is ~5 V: below ≈ 5 V the Zener (field) mechanism
wins; above ≈ 5 V the avalanche (impact-ionisation) mechanism dominates. You are
rarely asked to derive this — just recognise "small Vz, sharp knee" and "large Vz,
soft knee, negative TC".

---

### Q37. (GATE-level) An ordinary silicon signal diode with a `V_R(max)` rating of
50 V is reverse biased at 100 V. What does the I–V look like, and is the device
reusable?
**Answer:** Current stays at `≈ −I_S` up to 50 V, then breakdown: a nearly vertical
rise in current at ~50–100 V. The junction is **permanently damaged** (usually
shorted) unless a series resistor limits the current — the device is **not**
reusable. A Zener with `V_z = 50 V` would be perfectly fine in the same circuit.
**Method:** Read the word: *"ordinary diode"* + reverse voltage past rating ⇒
failure. *"Zener"* + reverse voltage past `V_z` ⇒ **the intended operating
region**. Same curve shape, completely different interpretation. GATE uses this
switch constantly.

---

### Q38. (GATE-level) Design: a 10 V Zener must be fed from 20 V through a resistor
so that it passes exactly 5 mA. Find `R_s`, and check that the Zener sees 10 V at
that current.
**Answer:** `R_s = (20 − 10)/5 mA = 10/0.005 = ` **2 kΩ**. At 5 mA the Zener sits
on its specified `V_z = 10 V` (given at the test current `I_ZT`), and
`P_z = 10 × 5 mA = 50 mW`.
**Method:** Design equations: `R_s = (V_s − V_z)/I_z`; then verify **both**
`P_z ≤ P_Z(max)` and `I_z ≥ I_ZK(min)`. Choosing the *test current* `I_ZT` as the
design point is the trick that makes `V_z` predictable.

---

### Q39. (Moderate) A diode has `I_S = 10⁻¹² A` (a much larger die than the
`10⁻¹⁴` device). `n = 1`. What `v_D` gives 10 mA, and why is it lower?
**Answer:** `v_D = 0.025 × ln(10⁻²/10⁻¹²) = 0.025 × ln(10¹⁰) = 0.025 × 23.026 =` **0.576 V**.
Reason: `I_S` is in the logarithm, so a 100× larger `I_S` subtracts
`25 mV × ln(100) = 0.025 × 4.605 = 115 mV` from the required drop.
**Method:** `v_D = nV_T·ln(I_D/I_S)` — the logarithm is why the same 0.7 V
constant-drop model works for wildly different diodes: a bigger die has bigger `I_S`
*and* proportionally bigger currents, so the logarithm lands in the same 0.6–0.75 V
window. This is exactly the design reason "big rectifier drops more volts".

---

### Q40. (GATE-level) A `n = 2` diode carries 5 mA. Find its `r_d`, the conductance
`g_d`, and the diffusion capacitance for `τ = 4 ns`.
**Answer:** `r_d = nV_T/I_D = 2 × 0.025/0.005 = ` **10 Ω**;
`g_d = 1/r_d = ` **0.1 S**; `C_d = τ·g_d = 4 n × 0.1 = ` **0.4 nF = 400 pF**.
**Method:** `r_d = nV_T/I_D` then reciprocate — `g_d` and `r_d` are one fact. `C_d`
always pairs with `g_d` through the transit time. The `n = 2` factor appears in
*both* `r_d` and `C_d`, so a non-unity `n` doubles the AC capacitance as well as
the resistance.

---

## Trap box (exam-day killers)

- **`r_d = 25 mV/I_D` must use the DC current.** Using the AC current gives a
  completely different (usually absurd) number, because in a series diode the AC
  current is orders of magnitude smaller than the DC current.
- **Shockley at 0.7 V with `I_S = 10⁻¹⁴` gives 14.5 mA, not 1.4 mA.** If your
  exponential comes out 10× off, you dropped a factor of 10 in `I_S`.
- **Germanium means 0.3 V.** A Ge problem with a 0.7 V drop in your solution is
  already wrong, and every number after it inherits the error.
- **The ideal model's ON state is a short, not a 0.7 V battery.** Students blend
  models and then "add 0.7 V" twice. Pick one model per problem and write it down.
- **In parallel, unequal `Vγ` means the lower-`Vγ` diode takes all the current** —
  never halve it.
- **Zener sign of `I_z`:** if `I_s < I_L`, the Zener is off and `V_out ≠ V_z`.
  Always check `I_z` is positive and above `I_ZK(min)`.
- **`C_d` only exists in forward conduction** and scales with current; `C_T` only
  matters in reverse bias and *shrinks* with reverse voltage. Swapping them is a
  free mark loss.
- **A Q-point found by trial must be checked**: substitute back into *both* the
  load line and Shockley. They should agree to within a per cent.

## Final recall drill (do in 60 seconds)

1. `V_T` at 300 K (GATE value) → **25 mV**
2. `r_d` at 5 mA → **5 Ω**
3. `r_d` at 0.1 mA → **250 Ω**
4. `r_d` doubles if… → **`n` doubles (or `I_D` halves)**
5. Si drop / Ge drop → **0.7 V / 0.3 V**
6. Shockley at 0.7 V, `I_S = 10⁻¹⁴` → **14.5 mA**
7. Voltage for 1 mA, `I_S = 10⁻¹⁴`, `n = 1` → **0.633 V**
8. mV of `v_D` per decade of current → **57.6 mV**
9. ON/OFF test → **remove diode, check `V_anode − V_cathode`**
10. PWL ON equation → **`v_D = Vγ + r_d·i_D`**
11. Reverse current for `|v_D| ≫ nV_T` → **`≈ −I_S`**
12. Zener `I_z` (12 V, 5.1 V, 500 Ω, 1 kΩ load) → **8.7 mA**
13. `C_d = τ·g_d` at 10 mA, τ = 5 ns → **2 nF**
14. `I_S` doubling rule → **×2 per 10 °C**
15. Model when "Vγ and forward resistance given" → **piecewise-linear**

---

