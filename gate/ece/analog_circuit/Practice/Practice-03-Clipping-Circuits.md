# Clipping Circuits — Practice (Learn by Solving)

> **The idea in one line:** this file teaches the whole of Chapter 03 through 34
> questions — a clipper *cuts shape*, and everything you need (which diode is ON,
> what the clamp level is, how many degrees the diode conducts) is learned by
> doing, not by reading.
>
> **How to use:** solve each question fully before reading the answer. Cover the
> **Answer**/**Method** with paper, do it, then reveal. If you miss one, solve
> the next 3 in the file to lock the pattern. No need to read the chapter notes
> first — every concept is taught through the drill itself. Open
> `03-Clipping-Circuits.md` or `32-Single-File-Cheatsheet.md` only when you want
> the underlying theory.

## Concept box (what you must internalise)

- **Series clipper** = diode in series with the load ⇒ the diode *passes* the half
  that conducts. **Shunt clipper** = diode across the output ⇒ the diode *shorts*
  that half. Mixing these inverts the answer.
- Ideal diode: ON = short. Silicon: ON = 0.7 V. So every clamp level is
  `V_bias` **plus** 0.7 V for silicon.
- Conduction window for `v_in = Vm·sin θ` against threshold `V_t`:
  `θ₁ = sin⁻¹(V_t/Vm)`, conduction from `θ₁` to `180° − θ₁`,
  width `= 180° − 2·sin⁻¹(V_t/Vm)`.
- Zener pair, back-to-back across the output ⇒ clamp at `±(V_z + 0.7)`.
- Two-level clipper: top flat at `+V₁`, bottom flat at `−V₂`, input untouched in
  between. Batteries facing "out" clip the top; facing "in" clip the bottom.
- Transfer curve is the fastest way to answer: series ⇒ `v_out = min(v_in, V_t)`;
  positive shunt ⇒ `v_out = min(v_in, V_t)` as well (same shape, different current
  path); negative shunt ⇒ `v_out = max(v_in, V_t)`.
- Averaging a clipped sine: integrate. `V_avg = Vm/π` for a clean half-wave,
  `2Vm/π` for full-wave, but a *clipped* sine has **no** closed-form shortcut —
  break the integral at the conduction angles.

---

## Questions

### Q1. (Easy) Positive series clipper, **ideal** diode, `v_in = 10 sin ωt`,
`R_L = 1 kΩ`. Describe `v_out` and give its peak.
**Answer:** Diode (anode at input) conducts on the positive half ⇒ `v_out = 10 sin ωt`
there, peak **+10 V**. On the negative half the diode is reverse biased and `R_L`
pulls the output to 0 ⇒ `v_out = 0`. So `v_out` = positive half-waves (0 to +10 V).
**Method:** Series clipper + ideal diode + no bias = classic half-wave. Draw it as
`v_out = v_in` for `v_in > 0`, `0` for `v_in ≤ 0`. Remember: a *conducting* diode
in a series clipper does **not** pin the output to a value — the input still drives
through; the load resistor is what defines 0.

---

### Q2. (Easy) Same circuit but a **silicon** diode (0.7 V). Give the positive peak
of `v_out`.
**Answer:** **9.3 V** (`10 − 0.7`). Negative half still 0 V.
**Method:** In a series clipper the conducting diode appears as a 0.7 V drop in
series with `v_in`, so subtract it from the peak. This is the single most common
0.7 V trap in clippers: the clamp level is not `V_bias`, it is `V_bias + 0.7`.

---

### Q3. (Easy) Positive **shunt** clipper, ideal, input `±10 V`. Describe `v_out`,
its range, and its peak-to-peak.
**Answer:** Positive half → diode ON → `v_out = 0` (flat). Negative half → diode OFF
→ `v_out = v_in` down to −10 V. So `v_out` ranges **−10 V to 0 V**, p-p = **10 V**.
It is a *negative* half-wave.
**Method:** Shunt = "the diode short-circuits the offending half." An ideal ON
diode is a short to the reference, so the output is pinned at 0, not at the input.
Compare Q1: series gave the *positive* half, shunt gave the *negative* half for the
same diode direction — the distinction the exam tests.

---

### Q4. (Easy) Negative **shunt** clipper, silicon (0.7 V), input `±10 V`. Range of
`v_out`?
**Answer:** Diode flipped: on the negative half it conducts and pins the output at
**−0.7 V**; on the positive half it is off and `v_out = v_in` up to +10 V. Range:
**−0.7 V to +10 V**, p-p = 10.7 V.
**Method:** The conducting half is clamped to the diode's own drop, not to 0 — a
useful memory hook: *ideal clamps at 0, silicon clamps at 0.7 (or −0.7)*. p-p is
slightly *more* than the input's 20 V, because the flat replaces part of the
negative swing with a higher level.

---

### Q5. (Easy) Biased shunt clipper: shunt diode in series with a **+3 V** battery to
ground, ideal diode. `v_in = +5 V` DC. Find `v_out`.
**Answer:** **+3 V.** 5 V > 3 V, so the diode is ON and the battery pins the output
at +3 V.
**Method:** Biased shunt = a *voltage source in the diode's leg*. During conduction
the whole branch (battery + diode) fixes the output, so `v_out = V_ref` (ideal) or
`V_ref + 0.7` (silicon). Run the ON/OFF test: remove the diode and see whether the
output node is pulled above the battery's + terminal.

---

### Q6. (Easy) Same circuit as Q5 but `v_in = −5 V` DC. Find `v_out`.
**Answer:** **−5 V.** −5 V < +3 V ⇒ the output never reaches the reference, the
diode is reverse biased (open), and `v_out = v_in`.
**Method:** A clipper only acts *beyond* its threshold; below it the circuit is
transparent. This "does nothing below threshold" behaviour is exactly the
transfer-curve slope-1 region, and it is where the signal passes undistorted.

---

### Q7. (Easy) Write the transfer characteristic of a **positive shunt clipper with
+2 V bias, ideal diode** (ideal source, no series R).
**Answer:** `v_out = min(v_in, +2 V)`. Sketch: a 45° line `v_out = v_in` from the
origin up to the point (2 V, 2 V), then a horizontal line at `v_out = +2 V` for all
`v_in > 2 V`. Equivalently: slope 1, then slope 0.
**Method:** Transfer curves are the fastest clipper answer and never need a
waveform sketch. Build them from two rules: (1) below threshold nothing conducts so
`v_out = v_in`; (2) above threshold a conducting shunt diode forces `v_out` to a
constant. Join with straight lines. The corner sits at `(V_t, V_t)`.

---

### Q8. (Easy) Write the transfer characteristic of a **positive series clipper with
+5 V bias, ideal diode** (ideal source, no series R).
**Answer:** `v_out = min(v_in, +5 V)` — identical shape to Q7. Slope 1 up to
(5 V, 5 V), then horizontal at +5 V.
**Method:** With an *ideal* zero-impedance source there is no voltage divider, so
series and shunt clips give the *same* transfer curve. The two topologies only
differ when a source resistance `R_s` exists (then the series clipper attenuates
during conduction, `v_out = v_in·R_L/(R_s+R_L)`, while the shunt clipper's clamp
level is unaffected). Worth 1 mark to know.

---

### Q9. (Moderate) Positive series clipper, **+5 V bias**, ideal diode,
`v_in = 10 sin θ`. Give the conduction window in degrees and the fraction of the
cycle that is flat.
**Answer:** Conducts when `10 sin θ > 5` ⇒ `sin θ > 0.5` ⇒
**θ = 30° to 150°**, width **120°**. Flat for 120/360 = **33.3 %** of the cycle.
**Method:** The golden pattern: (1) divide threshold by peak to get the sine
argument, (2) `θ₁ = sin⁻¹(V_t/Vm)`, (3) conduction is symmetric about 90°, so the
window is `θ₁` to `180° − θ₁` and the width is `180° − 2θ₁`. Here
`sin⁻¹(0.5) = 30°` exactly — GATE picks round numbers on purpose.

---

### Q10. (Moderate) Same circuit but **silicon** (0.7 V), `v_in = 10 sin θ`. Now
find the conduction window.
**Answer:** The input must beat `5 + 0.7 = 5.7 V` ⇒ `sin θ > 0.57` ⇒
**θ = 34.75° to 145.25°**, width **110.5°**.
**Method:** Same pattern, different threshold: **silicon raises the effective
threshold by 0.7 V**, which *shrinks* the conduction angle. `sin⁻¹(0.57) = 0.6065 rad
= 34.75°`. Compare Q9: 120° → 110.5°. If a question offers ideal and silicon
variants, the silicon one always conducts for *less* of the cycle.

---

### Q11. (Moderate) Two **Zeners back-to-back** across the output, both `V_z = 5 V`,
silicon forward drops. `v_in = 12 sin θ`, `R_L = 1 kΩ`. Give the clamp levels and
the conduction window.
**Answer:** Positive excursion: one Zener in breakdown (5 V) + the other forward
(0.7 V) ⇒ clamp at **+5.7 V**; negative half symmetric ⇒ **−5.7 V**.
Conducts when `12 sin θ > 5.7` ⇒ `sin θ > 0.475` ⇒ **θ = 28.36° to 151.64°**,
width **123.28°** per half cycle (34.2 % of the full cycle is clipped).
**Method:** A back-to-back Zener pair is the standard *symmetric two-level clipper*:
one device always in breakdown, the other always forward, so each half is clamped
at `V_z + 0.7`. Divide `5.7/12 = 0.475`, `sin⁻¹(0.475) = 28.36°`, window
`180 − 2(28.36) = 123.28°`.

---

### Q12. (Moderate) Same structure, but `V_z1 = 5 V` and `V_z2 = 3 V`
(asymmetric pair), `v_in = 12 sin θ`. Clamp levels?
**Answer:** Positive half: the 5 V Zener breaks down, the 3 V one goes forward ⇒
clamp **+5.7 V**. Negative half: the 3 V Zener breaks down, the 5 V one forward ⇒
clamp **−3.7 V**. Asymmetric — the same circuit gives a different positive and
negative limit.
**Method:** Trace which device is in breakdown for the sign of the excursion: the
one being pushed *reverse*. Then add the other device's forward drop. With equal
Zeners you get a symmetric `±(V_z+0.7)`; with unequal ones, `+(V_z1+0.7)` and
`−(V_z2+0.7)`. The *smaller* Zener always sets the *smaller* side.

---

### Q13. (Moderate) Ideal two-level clipper: top clamp **+4 V**, bottom clamp **−2 V**,
`v_in = 8 sin θ`. Give both conduction windows and the unclipped part of the cycle.
**Answer:** Top: `sin θ > 0.5` ⇒ **30° to 150°** (120°). Bottom: `sin θ < −0.25` ⇒
**194.48° to 345.52°** (151.04°). Unclipped: `360 − 120 − 151.04 = ` **88.96°**.
**Method:** Two independent tests, each using the golden pattern. The bottom window
is found by noting the negative sine is symmetric: conduction from
`180 + sin⁻¹(0.25)` to `360 − sin⁻¹(0.25)`, i.e. 194.48° to 345.52°.
`sin⁻¹(0.25) = 14.478°`. The bottom clamp is *closer to zero* (−2 V) than the top
(+4 V), so it conducts for **more** of the cycle (151° vs 120°).

---

### Q14. (Moderate) Find the average (DC) value of the output of a positive series
clipper, ideal, `v_in = 10 sin ωt`.
**Answer:** **10/π = 3.18 V**.
**Method:** With no bias the output is a *clean half-wave rectified sine*, and its
average is the standard `Vm/π = 0.318·Vm`. This is the same number as the
half-wave rectifier of Chapter 05 — a series positive clipper **is** a half-wave
rectifier. The 0.318 factor is worth memorising cold.

---

### Q15. (Moderate) Find the average of a **full-wave**-shaped output built from
`v_in = 10 sin ωt` (opposite series clippers in cascade, ideal). Compare with Q14.
**Answer:** **2 × 10/π = 6.37 V** — exactly **twice** Q14.
**Method:** Full-wave average is `2Vm/π = 0.637·Vm`. The ratio is trivially 2
because every output is the mirror of the previous half-cycle, so the total area
doubles while T stays the same. A "double positive clipper" is exactly a full-wave
rectifier, and the average ratio is the cleanest check that you have half vs full
right.

---

### Q16. (Moderate) A sine `v_in = 10 sin θ` has its **top clipped flat at +5 V**
(ideal). Compute the average of the output.
**Answer:** **−1.09 V.**
**Method:** Break the integral at `α = sin⁻¹(0.5) = 30°`:
`V_avg = (1/2π)[ 2·Vm(1 − cos α) + Vc(π − 2α) + ∫_π^{2π} Vm sinθ dθ ]`
`= (1/2π)[ 2(10)(0.13397) + 5(2.0944) + (−20) ]`
`= (1/2π)[ 2.6795 + 10.472 − 20 ] = −6.8485/6.2832 = ` **−1.09 V**.
Note `∫_π^{2π} Vm sinθ dθ = −2Vm = −20`, **not zero** — the positive half
contributes +20 and the negative half −20, and the clipping is all in the positive
half. That is why a "positively clipped" sine ends up with a *negative* average.

---

### Q17. (Moderate) Same clipped waveform as Q16 (top flat at +5 V, `Vm = 10`). Find
its RMS value.
**Answer:** **5.90 V.**
**Method:** `V_rms = sqrt((1/2π)∫v²dθ)`, splitting at α = 30° and using
`∫sin²θ dθ = θ/2 − sin2θ/4`:
`= (1/2π)[ 2·Vm²·(α/2 − sin2α/4) + Vc²(π−2α) + Vm²·(π/2) ]`
`= (1/2π)[ 2(100)(0.04529) + 25(2.0944) + 100(1.5708) ]`
`= 218.498/6.2832 = 34.777 ⇒ ` **5.90 V**.
Cross-check: it must lie between the unclipped `Vm/√2 = 7.07 V` and the flat level
5 V. ✔

---

### Q18. (Moderate) A **series** clipper (ideal) with bias **+5 V**, input
`10 sin θ`: the output follows the sine *except* it is flat at +5 V from 30° to
150°. Compute the average of this output.
**Answer:** **−1.09 V** — the *same* number as Q16.
**Method:** `V_avg = (1/2π)[ Vc(π−2α) − Vm·∫_α^{π−α} sinθ dθ ]` and
`∫_α^{π−α} sinθ dθ = 2cos α = 1.7321`:
`= (1/2π)[ 5(2.0944) − 10(1.7321) ] = (10.472 − 17.321)/6.2832 = −1.09 V`.
**The insight worth remembering: a series clipper flat at +5 V and a shunt clipper
flat at +5 V produce the *identical* waveform** — only the current path differs.
The topology decides the currents, not the shape.

---

### Q19. (Moderate) Same waveform as Q18. Find its RMS.
**Answer:** **5.90 V** — again identical to Q17, because the waveforms are the same.
**Method:** Waveform-first thinking: before integrating, ask "have I already seen
this waveform?" Q17 and Q19 are one waveform, so one integral. Time saved on the
exam comes from recognising shapes rather than re-deriving.

---

### Q20. (Moderate) Series clipper with a source resistance `R_s = 1 kΩ` and load
`R_L = 1 kΩ`, ideal diode, no bias, `v_in = 10 sin θ`. Find the positive peak of
`v_out`.
**Answer:** Peak **+5 V** (voltage divider halves it). Negative half: diode off,
`R_L` pulls the output to 0.
**Method:** A series clipper *always* has a divider during conduction. During
conduction the ideal diode is a wire, so `v_out = v_in·R_L/(R_s + R_L) = v_in/2`.
This is where "series vs shunt" really bites: the **shunt** clipper's clamp level is
immune to `R_s` (the diode just sinks more current), but the **series** clipper's
output level is set by the divider. A biased series clipper is often used exactly
as an attenuating level shifter for this reason.

---

### Q21. (Moderate) A series clipper uses a PWL diode with `Vγ = 0.7 V`,
`r_d = 20 Ω`, `R_L = 500 Ω`, `R_s = 0`, and the input peaks at 12 V. Find
`v_out(peak)` and the peak current.
**Answer:** `v_out(1 + 20/500) = 12 − 0.7` ⇒ `v_out = 11.3/1.04 = ` **10.87 V**.
Peak current `= 10.87/500 = ` **21.7 mA**. Check the resistive drop:
`21.7 mA × 20 Ω = 0.435 V`, and `10.87 + 0.435 + 0.7 = 12.0 V` ✔
**Method:** In a conducting series clipper the diode's `r_d` appears in series with
`R_L`, so it *attenuates* just like a source resistor:
`v_out = (v_in − Vγ)/(1 + r_d/R_L)`. Generalise Q20: with a PWL diode the
divider ratio is `R_L/(R_L + r_d)` even when `R_s = 0`. Solve once and verify by
adding the three drops back to `v_in`.

---

### Q22. (Moderate) A **symmetric triangle** wave `±10 V` has its top clipped at
**+4 V** (ideal). For how many degrees of the 360° cycle is the output flat?
**Answer:** On each ramp the signal is above 4 V for the fraction
`(10 − 4)/(2 × 10) = 0.3` of the ramp. Two ramps ⇒ **60 % of the cycle = 216°**.
**Method:** Triangle, not sine — the `sin⁻¹` pattern is **wrong** here. For a linear
ramp the fraction is just `(V_m − V_t)/(2V_m)`. `sin⁻¹(4/10) = 23.58°` would have
given a two-ramp answer of 2(180 − 47.16) = 265.6°, a completely different number.
Lesson: **conduction angles are waveform-specific.** Always ask "sine or triangle?"
before reaching for `sin⁻¹`.

---

### Q23. (Moderate) Biased **shunt** clipper with a **−5 V** reference and a silicon
diode, `v_in = 12 sin θ`. Clamp level and conduction window?
**Answer:** The diode conducts when `v_in < −5 − 0.7 = −5.7 V` ⇒ clamp level
**−5.7 V**. `sin θ < −0.475` ⇒ **θ = 208.36° to 331.64°**, width **123.28°**.
**Method:** Same golden pattern, mirrored: the threshold is `−(V_ref + 0.7)` for a
negative biased shunt clipper, the conduction window is `180 + θ₁` to `360 − θ₁`
with `θ₁ = sin⁻¹(5.7/12) = 28.36°`. Notice the window is the *same width* as the
positive Zener-pair case in Q11 — only the position in the cycle differs.

---

### Q24. (Moderate) Design: clip a `5 V` peak sine so the output never exceeds
**+3.5 V**, using a Zener plus its forward partner (silicon). What `V_z`?
**Answer:** **2.8 V** (since the clamp is `V_z + 0.7 = 3.5 V`).
**Method:** Work *backwards* from the required clamp: `V_z = V_clamp − 0.7 = 2.8 V`.
Design questions on clippers are almost always this subtraction. Sanity: 2.8 V is a
standard BZX55-series part, so the answer is physically buildable — always check
that your design value exists in a catalogue.

---

---

### Q25. (GATE-level) Design: clip a `10 V` peak sine at **+4.2 V** using a battery
and a silicon diode. What battery voltage, and what is the conduction window?
**Answer:** `V_batt = 4.2 − 0.7 = ` **3.5 V**. Conducts when `10 sin θ > 4.2` ⇒
`sin θ > 0.42` ⇒ `θ₁ = 24.83°`, window **24.83° to 155.17°**, width **130.33°**
(`sin⁻¹(0.42) = 0.43348 rad = 24.835°`).
**Method:** Two steps again: subtract the diode drop to get the battery, *then*
run the golden pattern with the **total** threshold 4.2 V — not with 3.5 V. Students
who use 3.5 V in the `sin⁻¹` get 20.5° and lose the mark. The threshold the sine
must beat is the *output* level.

---

### Q26. (GATE-level) Two different circuits, both with `v_in = 10 sin θ`:
(a) a **series** positive clipper, ideal, no bias; (b) a **negative shunt** clipper,
ideal, no bias. Give the peak inverse voltage each diode must block.
**Answer:** (a) The diode is off during the negative half, so its cathode sits at
0 (through `R_L`) and its anode at `−Vm` ⇒ **PIV = 10 V**. (b) The diode is off
during the positive half with the output following the input, and the other
terminal is at ground ⇒ **PIV = 10 V**. Same here, but the *reasons* differ.
**Method:** PIV = the largest reverse voltage the diode sees while it is OPEN.
Trace the off-state circuit and read the voltage across the diode's terminals.
For a **biased shunt** clipper the answer is different and more interesting: with
the diode off, the reference fixes its cathode, so **PIV = V_ref** (e.g. 4 V) —
a biased shunt clipper needs almost no reverse-voltage rating, one of its virtues.

---

### Q27. (GATE-level) Biased shunt clipper, ideal, reference **+4 V**,
`v_in = 10 sin θ`. For what fraction of the cycle is the output flat at +4 V, and
what is the peak current in the diode if `R_s = 1 kΩ`?
**Answer:** Flat when `v_in > 4` ⇒ `sin θ > 0.4` ⇒ `θ₁ = 23.58°`, window
**23.58° to 156.42°** = 132.84° ⇒ **36.9 %** of the cycle.
Peak diode current: the output is pinned at 4 V while `v_in = 10 V`, so
`i_D = (10 − 4)/1k = ` **6 mA**.
**Method:** `sin⁻¹(0.4) = 0.41152 rad = 23.578°`; the flat fraction is
`(180 − 2×23.578)/360 = 132.84/360 = 0.369`. For the current, remember the **shunt**
diode sees the *difference* between input and clamp through `R_s`, not the clamp
itself. This current is what the diode and `R_s` must be rated for.

---

### Q28. (GATE-level) Two-level clipper, `v_in = 12 sin θ`, top flat at **+6 V**,
bottom flat at **−3 V** (ideal). Conduction widths, unclipped duration, and average.
**Answer:** Top: `sin θ > 0.5` ⇒ **30°–150°**, width **120°**. Bottom:
`sin θ < −0.25` ⇒ **194.48°–345.52°**, width **151.04°**. Unclipped:
`360 − 120 − 151.04 = ` **88.96°**. Average `= ` **+1.13 V**.
**Method:** Angles as in Q13. For the average, split the integral into three
pieces and evaluate numerically (or with `∫sinθ = −cosθ`):
top flat `6 V` over 2.0944 rad, bottom flat `−3 V` over 2.6208 rad, and the sine
in the remaining 88.96°.
`V_avg·2π = 6(2.0944) − 3(2.6208) + 12[∫_{150°}^{180°}sin + ∫_{180°}^{194.48°}sin]`
`= 12.566 − 7.862 + 12[0.13397 − 0.06847] = 12.566 − 7.862 + 0.786 = 5.490`
`V_avg = 5.490/6.2832 = ` **+1.13 V**.
The *sign* is the exam point: **the bottom is flattened over a wider window
(151° vs 120°) but the top flat level (+6 V) is twice the bottom one (−3 V), so
the net DC comes out positive.** Larger flat level × comparable width wins.

---

### Q29. (GATE-level) A sine `10 sin θ` is clipped on the **bottom** at **−2 V**
(ideal). Find the average and the RMS of the output.
**Answer:** Average **+2.25 V**; RMS **5.18 V**.
**Method:** Numerically (or by splitting at `β = sin⁻¹(0.2) = 11.54°`) integrate
`max(10 sinθ, −2)`. Sanity-check both: the unclipped values are 0 and 7.07 V.
Clipping the bottom **raises** the average (from 0 to +2.25 V) and **lowers** the
RMS (from 7.07 to 5.18 V), because a deep negative peak carries a lot of `v²`
energy. Rule of thumb: **bottom clipping → average goes up, RMS goes down; top
clipping → average goes down, RMS goes down.** ⚠️ RMS always falls, but the reason is subtle: clipping removes the
**highest-`|v|`** part of the waveform, so the mean square always drops. It is
*not* because "clipping only ever removes area" — bottom clipping actually
**adds** signed area (it raises every sample below the threshold), yet the RMS
still falls from 7.07 V to 5.18 V. Area explains the **average**; `|v|` explains
the **RMS**.

---

### Q30. (GATE-level) Compare the DC output of a **positive series clipper** and a
**positive shunt clipper** (both ideal, no bias, `v_in = 10 sin θ`). What is the
output of each, and what is each clipper really doing?
**Answer:** Series positive clipper: positive half passes, negative flat at 0 ⇒
`V_avg = +10/π = ` **+3.18 V**. Positive shunt clipper: positive flat at 0, negative
half passes ⇒ `V_avg = −10/π = ` **−3.18 V**. The first is a **half-wave
rectifier**; the second is a *negative* half-wave rectifier.
**Method:** Same magnitude, opposite sign, because the same half-wave is being
selected but on opposite sides. Series *passes* what it selects, shunt *deletes*
what it rejects. Write "which half survives?" before any calculation.

---

### Q31. (GATE-level) Which single change moves the clamp level of a biased clipper
from `V_bias` to `V_bias + 0.7`, and what does it do to the conduction angle?
**Answer:** Replacing the **ideal diode with a silicon diode**. The clamp level
becomes `V_bias + 0.7`, and the input must now exceed a *higher* threshold, so the
conduction angle **shrinks** (Q9: 120° → Q10: 110.5°).
**Method:** The threshold the *input* must beat is always the *output* level
during conduction. Model change ⇒ threshold change ⇒ angle change. Students who
swap the model mid-problem and keep the old angle lose an easy mark; students who
treat "0.7 V" as a property of the *input* instead of the *output* lose the same
mark twice.

---

### Q32. (GATE-level) A symmetrical two-level clipper uses a **+3 V** top reference
and a **−5 V** bottom reference with **silicon** diodes, `v_in = 10 sin θ`. Find
both conduction widths, the unclipped duration, and the average.
**Answer:** Top threshold `3 + 0.7 = 3.7 V` ⇒ `sin θ > 0.37` ⇒ `θ₁ = 21.72°`,
width **136.57°**. Bottom threshold `−5 − 0.7 = −5.7 V` ⇒ `sin θ < −0.57` ⇒
`θ₁ = 34.75°`, width **110.50°**. Unclipped: `360 − 136.57 − 110.50 = ` **112.93°**.
Average `≈ ` **−0.69 V**.
**Method:** Apply Q31 *first* (add 0.7 to both references), then Q13's pattern.
`sin⁻¹(0.37) = 21.716°`, `sin⁻¹(0.57) = 34.750°`. The top reference is smaller
(+3 V vs −5 V) so the top conducts for *more* of the cycle (136.6° vs 110.5°) —
**the closer a clamp sits to zero, the more of the cycle it removes.** The
average comes out at **−0.69 V**: the bottom clamp is deeper *and* is applied over
a wide window, so the negative side dominates despite the top's larger width.

---

### Q33. (GATE-level) Which of the four circuits gives a clamp level of exactly
**±(V_z + 0.7)**? Sketch its transfer characteristic.
**Answer:** Two Zeners **in series, back-to-back, across the output** (a shunt
two-level clipper). Transfer: `v_out = clip(v_in, −(V_z+0.7), +(V_z+0.7))` —
slope 1 between `−(V_z+0.7)` and `+(V_z+0.7)`, then two horizontal rails.
**Method:** Draw the transfer as a three-segment polyline: rising 45° line, flat
top rail, flat bottom rail. The corner points are at `(±(V_z+0.7), ±(V_z+0.7))`.
The `0.7` is the partner Zener's forward drop, so a **single** Zener + single diode
gives an *asymmetric* `±` pair only if the two Zeners differ; identical Zeners in
series give the symmetric `±(V_z+0.7)`.

---

### Q34. (GATE-level) A clipper is fed from `v_in = 10 sin θ` and must limit the
output to ±4 V using one component type (Zeners or batteries+silicon diodes). Which
do you choose, what value, and what is the resulting unclipped fraction of the
cycle?
**Answer:** Either works. Zener pair: `V_z = 4 − 0.7 = 3.3 V` each. Battery + silicon:
`V_batt = 3.3 V` each side. Either way the input must exceed 4 V to clip:
`sin θ > 0.4` ⇒ flat **132.84°** top and the same bottom ⇒
`2 × 132.84 = 265.7°` clipped, leaving `360 − 265.7 = ` **94.3°** unclipped
(26.2 % of the cycle passes untouched).
**Method:** Design backwards: `V_z(or V_batt) = V_clamp − 0.7 = 3.3 V`. Then the
golden pattern with the *output* threshold 4 V. The honest engineering comment:
a Zener pair needs no bias supply and is symmetric, so it is the usual answer; but
Zeners below ~3 V have a soft knee (Q36 in the diode file), so a battery reference
gives a sharper clip.

---

## Trap box (exam-day killers)

- **Series passes, shunt shorts.** Same diode direction, opposite halves of the
  sine survive. This single confusion flips the answer and is worth 0.
- **The threshold is the OUTPUT level, `V_bias + 0.7`, not `V_bias`.** Using the
  bare bias in `sin⁻¹` is the single most common numerical error in this chapter.
- **A conducting diode in a *series* clipper does not pin the output** — the input
  still drives through, and `R_s`/`r_d` form a divider. In a *shunt* clipper it
  really does pin the output.
- **Conduction ends at `180° − θ₁`, not at `180° + θ₁`.** The window is symmetric
  about 90° for a positive clip and about 270° for a negative one.
- **`sin⁻¹` only works for a sine.** A triangle or square needs
  `(V_m − V_t)/(2V_m)` or pure interval reasoning (Q22).
- **Never average the unclipped sine.** A clipped waveform needs the integral
  broken at the conduction angles; for a top-clipped sine the average is actually
  *negative* (Q16, −1.09 V).
- **`∫_π^{2π} Vm sinθ dθ = −2Vm`, not zero.** The positive half gives +`2Vm` and
  the negative half −`2Vm`; forgetting this is what produces the wrong sign in
  every clipped-average problem.
- **A Zener pair clamps at `V_z + 0.7`, not `V_z`.** And the *smaller* Zener sets
  the *smaller* clamp side.

## Final recall drill (do in 60 seconds)

1. Positive series clipper, ideal, `10 sin θ`, no bias → output is a **positive half-wave, peak 10 V**
2. Same with silicon → peak **9.3 V**
3. Positive shunt clipper, ideal, ±10 V → output is the **negative** half-wave, range **−10…0 V**
4. Shunt clipper output when the diode conducts → **the clamp level** (0 ideal, 0.7 Si)
5. Biased series clipper, V = 5, Vm = 10, ideal → conduction **30°–150°** (120°)
6. Same but silicon → threshold **5.7 V**, conduction **34.75°–145.25°**
7. Zener pair `V_z = 5` both → clamp **±5.7 V**
8. Zener pair 5 V and 3 V → clamps **+5.7 V** and **−3.7 V**
9. V_dc of a positive series clipper, Vm = 10 → **3.18 V** (= `10/π`)
10. V_dc of a full-wave version → **6.37 V** (= `20/π`)
11. Average of a sine `10 sin θ` top-clipped at +5 V → **−1.09 V**
12. Clamped half-cycle, threshold `V_t` on `Vm sin θ` → `sin⁻¹(V_t/Vm)` to `180° − that`
13. PIV of a biased shunt clipper's diode → **`V_ref`**
14. PIV of a series clipper (no bias) → **`Vm`**

---

