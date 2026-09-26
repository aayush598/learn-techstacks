# Op-Amp Fundamentals — Practice (Learn by Solving)

> **The idea in one line:** one rule — with **negative feedback** and an
> **unsaturated** output, `v+ = v−` and no current enters the inputs — plus
> three numbers to memorise for the 741 (`A ≈ 2×10⁵`, `SR = 0.5 V/µs`,
> `GBW = 1 MHz`) unlock every op-amp numerical in the syllabus.
>
> **How to use:** solve each question fully before reading the answer. Cover the
> **Answer**/**Method** with paper, do it, then reveal. If you miss one, solve
> the next 3 in the file to lock the pattern. No need to read the chapter notes
> first — every concept is taught through the drill itself. Open
> `19-Op-Amp-Fundamentals.md` or `32-Single-File-Cheatsheet.md` only when you
> want the underlying theory.

## Concept box (what you must internalise)

- Ideal op-amp: `A = ∞`, `R_in = ∞`, `R_out = 0`, `V_os = 0`, `I_B = 0`,
  `CMRR = ∞`, `BW = ∞`, `SR = ∞`, output swings to both rails.
- The **golden rules**: (1) no current into `+` or `−`; (2) `v+ = v−` — *only*
  with negative feedback **and** in the linear (unsaturated) region;
  (3) the output takes whatever value the external network demands, until it
  hits a rail.
- Virtual **short** (`v+ = v−`) ≠ virtual **ground** (a virtual short that
  happens to sit at 0 V because `v+` is grounded).
- Saturation is the #1 killer: the output clamps, the virtual short **breaks**,
  and every downstream number becomes fiction. Always check `|v_o| < rail`.
- Slew rate: `SR = 2π·f·V_pk`. For the 741 (`SR = 0.5 V/µs`) a 10 V peak sine
  can only reach `0.5e6/(2π·10) = 7.96 kHz`.
- 741 in dB: `A = 2×10⁵` ⇒ `20 log10 2e5 = 106 dB`; dominant pole
  `= GBW/A = 1 MHz/2×10⁵ = 5 Hz`; closed-loop BW `= GBW / noise gain`.
- Offset: output error `= V_os · (1 + R_f/R_1)` for **both** topologies — the
  inverting stage's error uses the *noise* gain `1 + R_f/R_1`, not `R_f/R_1`.
- Trap: open loop (comparator) there is **no** virtual short — the output is
  `±V_sat` and `v+ = v−` is false.

---

## Questions

### Q1. (Easy) List the ideal parameters of an op-amp and the practical
consequence of each.
**Answer:** `A = ∞` ⇒ with feedback `v+ = v−` (virtual short);
`R_in = ∞` ⇒ input currents are 0; `R_out = 0` ⇒ the load does not drag the
output; `V_os = 0` and `I_B = 0` ⇒ zero output with equal inputs;
`CMRR = ∞` ⇒ no common-mode leakage; `BW = ∞` and `SR = ∞` ⇒ no
frequency/amplitude limits; output swing reaches both rails.
**Method:** Learn the list as **cause → effect**. In a numerical you only ever
use three of them: `R_in = ∞` (set input currents to 0), `A = ∞` (virtual
short), and "swing to the rails" (the saturation check).
(`19-Op-Amp-Fundamentals.md` §19.2.)

### Q2. (Easy) An ideal op-amp is open-loop with `v+ = 1 mV`, `v− = 0`. What
is the output?
**Answer:** `A·(1 mV) = ∞·1 mV = ∞` — unphysical. A **real** op-amp saturates
immediately: the output slams to the positive rail.
**Method:** Ideal `A = ∞` only makes sense *with feedback*. Whenever you see
"open loop", switch to comparator mode: output `= ±V_sat` (see Q28 for the
741's numbers). (`23-Schmitt-Trigger-Comparators.md`.)

### Q3. (Easy) Inverting amplifier: `R1 = 1 kΩ`, `R_f = 10 kΩ`,
`v_in = 0.5 V`, ideal op-amp on `±12 V` rails. Find `v_o`.
**Answer:** `A_v = −R_f/R1 = −10` ⇒ `v_o = −5 V`. Inside the rails ✓, so the
virtual short was valid.
**Method:** `v− = 0` (virtual ground), so `i = v_in/R1 = 0.5 mA` flows through
`R_f`: `v_o = −i·R_f = −0.5 mA × 10 kΩ = −5 V`. Detail in
`20-Op-Amp-Amplifiers-Summers.md`.

### Q4. (Easy) Can you apply the virtual-short rule to a comparator (op-amp
used open-loop as a switch)? Why or why not?
**Answer:** **No.** There is no feedback path, so nothing forces `v+ = v−`. A
microscopic difference is multiplied by `A ≈ 2×10⁵` and the output goes to a
rail. The op-amp is being used as a **comparator**, and it is not linear.
**Method:** Ask two questions before every op-amp problem: (1) is there a
feedback path from output to `v−`? (2) is the output inside the rails? If
either answer is no, the virtual short is unavailable and you must use
`v_o = ±V_sat`. (`19-Op-Amp-Fundamentals.md` §19.2, §19.6.)

### Q5. (Easy) What is the ideal input resistance, and what follows from it?
**Answer:** `R_in = ∞` ⇒ `i+ = i− = 0`. So an input node connected to the
op-amp draws no current: a resistor from `v−` to ground really is a full
divider, and a series resistor at the `+` input drops nothing.
**Method:** Set both input currents to zero *first*, then write KCL. Never write
an unknown current into an op-amp input — it is always 0. (Real 741:
`R_in ≈ 2 MΩ`, which is why bias currents matter at all — see Q15.)

### Q6. (Moderate) In Q3, what is the inverting-input voltage, and what current
flows through `R1`?
**Answer:** `v− = 0 V` (virtual ground) and `i(R1) = 0.5 V/1 kΩ = 0.5 mA`,
which must equal `|−i(R_f)|` since no current enters the op-amp.
**Method:** The full three-step method for an inverting stage:
`v− = v+ = 0` → `i = v_in/R1` → `v_o = −i·R_f`. The "virtual ground" name
comes from step 1: the node is at 0 V without being connected to ground.
(`20-Op-Amp-Amplifiers-Summers.md` §20.1.)

### Q7. (Moderate) Inverting amplifier, `R_f/R_1 = 100`, `v_in = 0.2 V`, output
rails at `±12 V` (a 741 on `±15 V`). Find the input range for which the stage
is linear, and the output for `v_in = 0.2 V`.
**Answer:** Linear for `|v_in| < 12/100 = 0.12 V`. At `0.2 V` the wanted output
is `−20 V`, so the output **clamps at −12 V**; the virtual short is broken.
**Method:** Saturation check in one line: compute `v_o` from the ideal gain,
then compare with the rail. `|v_o| = |A|·|v_in| ≤ V_rail`. This check is worth
more marks than any amplifier gain. (`19-Op-Amp-Fundamentals.md` §19.6.)

### Q8. (Moderate) A 741 has `SR = 0.5 V/µs`. What is the highest sine
frequency it can produce with `V_pk = 10 V`?
**Answer:** `f_max = SR/(2π·V_pk) = 0.5×10⁶/(2π × 10) = 0.5e6/62.83 =
7.96 kHz ≈ 8 kHz`.
**Method:** `SR = 2π·f·V_pk` ⇒ `f = SR/(2π·V_pk)`. Do the arithmetic in this
order: `2π×10 = 62.8`, then `0.5e6/62.8 = 7960 Hz`. Called the
**full-power bandwidth**. (`19-Op-Amp-Fundamentals.md` §19.4.)

### Q9. (Moderate) Same 741. Highest sine frequency for `V_pk = 1 V`? And what
output amplitude is safe at `f = 20 kHz`?
**Answer:** `f_max = 0.5e6/(2π × 1) = 79.6 kHz ≈ 80 kHz`. At 20 kHz:
`V_pk = 0.5e6/(2π × 2e4) = 3.98 V ≈ 4 V`.
**Method:** Same formula inverted. Notice the inverse relation: **frequency and
amplitude trade against each other** for a fixed SR — halve `V_pk`, double
`f_max`. Memorise `2π×1 = 6.283` and `2π×10 = 62.83` so these are one
division each.

### Q10. (Moderate) A 741 has `GBW = 1 MHz`. What is the closed-loop bandwidth
for (a) unity gain, (b) gain 10, (c) gain 100, (d) gain 1000?
**Answer:** (a) 1 MHz, (b) 100 kHz, (c) 10 kHz, (d) 1 kHz.
**Method:** `BW = GBW / closed-loop gain` (single dominant pole). The dB ladder:
1 MHz − 20 dB/decade. Sanity anchor: at gain 100 the usable band is only 10 kHz,
which is why multi-stage designs are used for high gain.
(`16-Frequency-Response.md`.)

### Q11. (Easy) Why is the closed-loop bandwidth of an inverting amplifier
with `R_f/R_1 = 9` equal to `GBW/10` and not `GBW/9`?
**Answer:** The op-amp sees `10` at its own input: the inverting stage's *noise*
gain is `1 + R_f/R_1 = 10` even though the signal gain is `−9`. Bandwidth is
set by the noise gain, not the signal gain.
**Method:** Trace the noise at the output back to the input: the feedback
divider is `R1/(R1+R_f) = 1/10`, so the amplifier must produce 10× the output
to overcome it ⇒ noise gain 10. Same reason offset error is
`V_os(1 + R_f/R1)`. This one idea unifies bandwidth **and** offset errors.

### Q12. (Moderate) A 741 has `A_OL = 2×10⁵` and `GBW = 1 MHz`. Give the
open-loop gain in dB, and estimate the dominant pole.
**Answer:** `20 log10(2×10⁵) = 20 × 5.301 = 106 dB`. Dominant pole
`f_p = GBW/A = 1e6/2e5 = 5 Hz`.
**Method:** `20 log10` for **voltage** ratios: `log10 2e5 = 5.301` ⇒ 106 dB.
`f_p` is where the open-loop gain has fallen to 0 dB divided by A; with a
single pole, `GBW = A·f_p` exactly. The "5 Hz" pole explains why a 741 needs AC
coupling for audio — you cannot get gain down to a few Hz.

### Q13. (Moderate) A 741 has `V_os = 2 mV`. It is wired as a non-inverting
amplifier with `R1 = 1 kΩ`, `R_f = 50 kΩ`. Find the DC output offset.
**Answer:** Gain `= 1 + 50 = 51`; `Δv_o = 51 × 2 mV = 102 mV`.
**Method:** `Δv_o = V_os(1 + R_f/R_1)` = `V_os × noise gain`. Never use
`V_os × |signal gain|` — the offset is a non-inverting quantity so it sees the
non-inverting gain. 102 mV of pure error at the output, from a 2 mV input
mismatch.

### Q14. (Moderate) The same 741 (`V_os = 2 mV`) is now wired **inverting** with
`R1 = 1 kΩ`, `R_f = 50 kΩ` (signal gain `−50`). Find the output offset and
explain why it is not `100 mV`.
**Answer:** `Δv_o = 2 mV × 51 = 102 mV` — the same as the non-inverting case.
**Method:** The offset is equivalent to a differential input at the op-amp's
own two pins, so it is amplified by the **noise gain** `1 + R_f/R_1 = 51`, not
by the signal gain 50. Both Q13 and Q14 give `V_os·(1 + R_f/R1)`; the topology
does not change the formula. This is the single most-missed op-amp formula.

### Q15. (Moderate) 741 input bias current `I_B = 80 nA`, input offset current
`I_os = 20 nA`. In an inverting stage with `R1 = 1 kΩ`, `R_f = 10 kΩ`, find the
DC output errors from `I_B` and from `I_os`.
**Answer:** `R1 ∥ R_f = 10/11 k = 909 Ω`. Bias-current error
`= 80 nA × 909 Ω = 72.7 µV`; offset-current error `= 20 nA × 909 Ω = 18.2 µV`.
The bias term dominates (4:1).
**Method:** The equivalent differential input voltage produced by bias current
is `I_B·(R1 ∥ R_f)`, then multiply by the noise gain. Use the **parallel**
combination, not `R1` and not `R_f` — the bias current sees the Thévenin
resistance of the two-terminal network. Same technique as the bias resistor of
a BJT stage.

### Q16. (Moderate) A 741 must output a `2 V` peak sine at `60 kHz`. Does it
slew-limit? By how much?
**Answer:** Required `SR = 2π × 60e3 × 2 = 753,982 V/s = 0.754 V/µs`.
Since `0.754 > 0.5 V/µs`, **yes — the output is slew-limited** (it becomes
approximately a triangle, not a sine).
**Method:** Always compute the required SR **before** deciding the circuit works.
`2π×60e3 = 376,991`; `×2 = 753,982`; `/1e6 = 0.754 V/µs`. The waveform becomes
a triangle of the right frequency and *smaller* amplitude — a classic GATE
"what does the output look like" answer. (`19-Op-Amp-Fundamentals.md` §19.4.)

### Q17. (Easy) A 741 slews a `10 V` step (the maximum output swing).
How long does it take?
**Answer:** `t = ΔV/SR = 10 V/(0.5 V/µs) = 20 µs`.
**Method:** Slew rate is literally "volts per microsecond" — the step time is
just a division. This 20 µs is the 741's datasheet slew time for a 10 V step, so
if you recognise 20 µs in a question, the answer is `SR = 0.5 V/µs`.

### Q18. (Moderate) A 741 has `CMRR = 90 dB` and both inputs see a `5 V`
common-mode voltage. Estimate the output error contributed by CMRR.
**Answer:** `A_cm = 1/CMRR = 10^(−90/20) = 3.16×10⁻⁵`; output error
`= 3.16e-5 × 5 V = 158 µV`.
**Method:** CMRR in dB is a voltage ratio, so use `20 log10` to convert:
`90 dB ⇒ 10^4.5 = 31,623` ⇒ `A_cm = 1/31,623`. Common-mode error in a real
amplifier is always present, never zero — and it grows with the input
common-mode level, which is why the ICM range is a hard limit.

### Q19. (Moderate) A 741 (`A = 2×10⁵`) is used as a non-inverting amplifier
with `R1 = 1 kΩ`, `R_f = 9 kΩ`. What is the *actual* gain, not the ideal one?
**Answer:** Ideal 10. `β = R1/(R1+R_f) = 0.1`; `Aβ = 20,000`;
`A_f = A/(1+Aβ) = 200,000/20,001 = 9.9995` — an error of only **0.005 %**.
**Method:** `A_f = A/(1 + Aβ)`. The check: because `Aβ = 20,000 ≫ 1`, the result
sits within `1/(Aβ) = 1/20,000` of the ideal gain. This is precisely why
feedback is used: the closed-loop gain is set by *resistors*, not by `A`.
(`24-Feedback.md` §29.11.)

### Q20. (Easy) Same 741, but `R1 = 1 kΩ`, `R_f = 99 kΩ` (non-inverting).
Give the ideal gain, the actual gain, and compare the error with Q19.
**Answer:** Ideal 100. `β = 1/100 = 0.01`; `Aβ = 2,000`;
`A_f = 200,000/2,001 = 99.95`. Error ≈ **0.05 %** — 10× worse than Q19.
**Method:** `1/Aβ = 1/2000 = 0.05 %`. The message: **accuracy falls as gain
rises**, because `Aβ` falls. Higher gain, less absolute accuracy, but a wider
`1/Aβ`-relative error — worth one mark in any feedback question.
Compare also with Q24, where the *inverting* stage of the same gain is worse
still.

### Q21. (Moderate) An ideal op-amp with negative feedback. When is the answer
`v+ = v−` actually valid?
**Answer:** Only when the output demanded by the network lies **inside** the
output swing range. If the required `v_o` exceeds the rails, the op-amp cannot
produce it, saturates, and `v+ = v−` no longer holds.
**Method:** Treat "virtual short" as a *proposal*: solve the circuit with it,
then **verify** `|v_o| ≤ rail`. If the check fails, the answer is a clamped
output, not the ideal formula. This verify-then-trust habit is the whole
method of `19-Op-Amp-Fundamentals.md` §19.5.

### Q22. (Moderate) In an inverting amplifier, why must the `+` input be
grounded? What happens if it is instead connected to `+1 V`?
**Answer:** Grounding `+` makes `v− = 0` (virtual ground), so the current
`v_in/R1` all flows through `R_f` and the gain is `−R_f/R1`. With `v+ = 1 V`,
`v− = 1 V`: the gain is unchanged (`−R_f/R1`) but the whole output is shifted
by `+R_f/R1 × 1 V` — i.e. `v_o = −(R_f/R1)(v_in − 1 V)`. A non-zero `v+` is a
*reference*, not a gain change.
**Method:** `v_o = −(R_f/R1)(v_in − v_ref)`. Adding a reference to `+` is how
you build a summing amplifier with an offset, and how the 4-resistor difference
amplifier works. (`20-Op-Amp-Amplifiers-Summers.md` §20.6.)

### Q23. (GATE-level) A 741 (`A = 2×10⁵`, `V_os = 1 mV`, rails `±12 V` on
`±15 V` supplies) is wired non-inverting with `R1 = 1 kΩ`, `R_f = 9 kΩ`.
Find: the ideal gain, the actual gain, the DC output offset, and the largest
input that avoids clipping.
**Answer:** Ideal gain 10; `β = 0.1`, `A_f = 200,000/20,001 = 9.9995`;
`Δv_o = V_os × 10 = 10 mV`; largest input `= 12/10 = 1.2 V` (then output
clips at 12 V).
**Method:** Ideal gain → finite-`A` gain (`A/(1+Aβ)`) → offset (× noise gain)
→ saturation check. Four separate ideas, one circuit, four marks. Note the
offset is *added* to the signal, so the practical linear input is slightly
below 1.2 V. (`19-Op-Amp-Fundamentals.md` §19.4, §19.5.)

### Q24. (GATE-level) The same 741 is now wired **inverting** with
`R1 = 1 kΩ`, `R_f = 99 kΩ`. Find the ideal gain, the actual gain, and compare
its gain error with Q23's.
**Answer:** Ideal signal gain `−99`; `β = R1/(R1+R_f) = 1/100 = 0.01`;
`Aβ = 2,000`; `A_f = −200,000/2,001 = −99.95` ⇒ error `0.05 %`.
Q23 (non-inverting, same *noise* gain of 100) had ideal 100 and actual 99.95,
error `0.05 %` as well — identical, because both stages have the **same noise
gain 100**. The signal gain differs (`−99` vs `+100`), the accuracy does not.
**Method:** The punchline: the finite-`A` error depends on the **noise gain**
`1 + R_f/R1 = 100`, not on whether the signal gain is 99 or 100. Compare with
Q20 (`R_f = 99 kΩ` *non-inverting*, noise gain 100 too) — all three circuits
have noise gain 100 and all three lose 0.05 %.

### Q25. (GATE-level) A 741 (`SR = 0.5 V/µs`, `GBW = 1 MHz`) must produce a
`5 V` peak sine. Find (a) the maximum frequency from the slew limit, (b) the
maximum frequency from the small-signal (GBW) limit, (c) which binds, and
(d) the largest output at `f = 20 kHz`.
**Answer:** (a) `0.5e6/(2π × 5) = 15.9 kHz`. (b) `1e6/(2π × 5) = 31.8 kHz`.
(c) **Slew limit binds** (always exactly 2× lower for a 741, since
`SR = 0.5 V/µs` and `GBW = 1 MHz` happen to give that ratio).
(d) `V_pk = 0.5e6/(2π × 2e4) = 3.98 V ≈ 4 V`.
**Method:** Compare *both* limits — a real op-amp can be slew-limited or
small-signal-limited, and the 741 is slew-limited at every amplitude. Use
`2π×5 = 31.4` and `2π×2e4 = 1.2566e5`. Recognising which limit binds is the
whole point of the question. (`16-Frequency-Response.md`.)

### Q26. (GATE-level) Two cascaded 741 stages: stage 1 non-inverting with
`R1 = 1 kΩ`, `R_f = 19 kΩ` (gain 20); stage 2 inverting with `R1 = 1 kΩ`,
`R_f = 5 kΩ` (gain −5). Find the total gain in V/V and dB, each stage's
bandwidth, and the overall bandwidth.
**Answer:** Total gain `= 20 × (−5) = −100` ⇒ `20 log10 100 = 40 dB` (inverting
overall). Stage 1 BW `= 1 MHz/20 = 50 kHz`. Stage 2 noise gain
`1 + 5 = 6` ⇒ BW `= 1 MHz/6 = 166.7 kHz`. Overall `≈ 50 kHz` (the lower one
sets the pole that matters; strictly the product rolls off at −40 dB/dec beyond
it).
**Method:** Gains multiply; dB add. Bandwidths are set by each stage's own
noise gain, so the **first** stage usually owns the bandwidth. Cascade
multiplies gain but not bandwidth — that is the entire reason op-amps are
multi-stage.
(`20-Op-Amp-Amplifiers-Summers.md`, `16-Frequency-Response.md`.)

### Q27. (GATE-level) A 741 is used open-loop as a comparator with inputs
`0 V` and `+5 mV`, on `±15 V` (output `±12 V`). What is the output, and what is
the smallest input difference that guarantees saturation?
**Answer:** Output `= +12 V` (positive saturation). Any
`|v_id| > V_sat/A = 12/2×10⁵ = 60 µV` saturates.
**Method:** Open loop: `v_o = A·v_id` until it hits the rail, so 5 mV × 2e5
would be 1000 V → clamps at 12 V. The 60 µV figure is the useful design
number: input noise above 60 µV guarantees correct switching. Note a bare 741
makes a *poor* comparator because `SR` is only 0.5 V/µs (a 5 V step takes
10 µs) — hence the dedicated comparators in
`23-Schmitt-Trigger-Comparators.md`.

### Q28. (GATE-level) A 741 is used in a non-inverting gain-of-51 stage, and
the signal source drifts slowly. Both inputs sit at 14 V DC while the supply
is `±15 V`. What happens?
**Answer:** 14 V is **outside** the 741's input common-mode range
(`±12 V` for `±15 V` supplies). The input stage saturates, feedback can no
longer control the output, and the output is undefined (typically driven to a
rail). The virtual short fails — and it fails even though the output
amplitude is small.
**Method:** Three separate limits to check on any op-amp question:
(i) **output** swing (±12 V), (ii) **input common-mode** range (±12 V),
(iii) supply rails. Item (ii) is the one students forget, and it is the classic
GATE trap: a circuit can be "correct" on paper and still fail because the
inputs are outside the ICM range. (`19-Op-Amp-Fundamentals.md` §19.4.)

### Q29. (GATE-level) A 741's worst-case input offset is `6 mV` and its
temperature drift is `5 µV/°C`. In a stage with noise gain 100, what is the
output offset at room temperature, and what extra output error appears over a
`50 °C` temperature change?
**Answer:** Room temperature: `6 mV × 100 = 0.6 V`. Drift: `5 µV/°C × 50 °C =
250 µV` input ⇒ `250 µV × 100 = 25 mV` output.
**Method:** Offset always scales with the **noise** gain (Q11, Q14). Drift is
an *input-referred* quantity, so treat it exactly like offset: multiply by the
noise gain. 0.6 V of offset is 5 % of a `±12 V` swing — high-gain single-741
stages are offset-limited, which is why auto-zeroing and chopper-stabilised
amps exist.

### Q30. (GATE-level) Your 741 inverting stage saturates (input `0.5 V`, gain
`−100`, rails `±12 V`) and then the input returns to `0 V`. Describe the output.
**Answer:** The wanted output is `−50 V`, so it clamps at `−12 V`. When the
input returns to 0 V the output **stays at −12 V** for a long time (tens of µs
while the internal stages re-linearise — a 741 is not self-clamping), and only
then returns to 0 V. A single 741 in a gain of 100 is prone to this.
**Method:** Saturation is a *latching* condition in a slow op-amp: the
feedback cannot pull the output back until the output stage becomes linear
again. Remedies: lower the gain and cascade, use a faster/rail-to-rail
comparator-clamped design, or add clamp diodes. The safe exam sentence: "the
virtual short is lost, and recovery requires the op-amp to come out of
saturation."

### Q31. (GATE-level) Four effects of negative feedback on an amplifier:
`gain`, `bandwidth`, `output resistance`, `distortion`. State each effect and
the mechanism.
**Answer:** Gain: `A_f = A/(1+Aβ)` — it *falls* (this is the price).
Bandwidth: *rises* by `(1+Aβ)`, since `GBW ≈ A·BW` is roughly constant.
Output resistance: *falls* by `(1+Aβ)` for voltage sampling. Distortion /
noise: *falls* by `(1+Aβ)`. The unifying statement: feedback makes the closed
loop depend on `1/β` (resistors) instead of `A` (the device).
**Method:** Mnemonic: feedback **trades gain for everything else**. Every
"effect of negative feedback" question is this list.
(`24-Feedback.md`, §29.11 of `29-Formula-Sheet.md`.)

### Q32. (GATE-level) Write the complete pre-flight checklist you run before
trusting a virtual short in a 741 numerical, and say which of your answers
above would have failed it.
**Answer:** (1) Is there a feedback path from output to `v−`? (2) Does the
computed `|v_o|` fit inside `±12 V`? (3) Are both inputs inside the `±12 V`
ICM range? (4) Is the frequency inside the closed-loop BW? (5) Is the required
SR `≤ 0.5 V/µs`? Failures caught: Q2/Q4 (no feedback), Q7 (`−20 V` needed),
Q16 (`0.754 V/µs`), Q28 (`14 V` inputs), Q25 (frequency).
**Method:** Make this a reflex. Points 1–2 are worth a mark each in almost
every op-amp numerical, and 3–5 are the "why did the real circuit fail"
follow-ups that GATE loves.

### Q33. (GATE-level) Design check: you need a closed-loop gain of `1000` at
`100 Hz` using only 741s (GBW = 1 MHz, `V_os ≤ 6 mV`). Is it possible? What
limits you?
**Answer:** Bandwidth is fine: `BW = 1 MHz/1000 = 1 kHz > 100 Hz` ✓
(`gain ≤ GBW/f` ⇒ at 100 Hz the maximum gain is `1e6/100 = 10,000`).
The real limit is **offset**: `6 mV × 1000 = 6 V` of DC error, 50 % of a 12 V
swing — the signal is buried. Also, one 741 cannot even *hold* gain 1000
linearly (it would need `Aβ ≫ 1`).
**Method:** For any "is this design feasible?" question, run three numbers:
gain (resistors), bandwidth (`GBW/gain` vs required `f`), and output error
(`V_os × noise gain` vs signal amplitude). The third is the one that kills
high-gain single-op-amp designs.

### Q34. (GATE-level) Why do op-amp datasheets quote *open-loop* gain
bandwidth (unity-gain) rather than a "closed-loop bandwidth", and what does
`GBW = 1 MHz` really tell you?
**Answer:** Because the closed-loop bandwidth **changes with the gain you
choose** — it is `GBW/noise gain`. The constant is the gain×bandwidth product.
`GBW = 1 MHz` means: the frequency at which the *open-loop* gain has fallen to
1 (0 dB); multiply by any closed-loop gain and you get that stage's bandwidth
(1 MHz at unity, 100 kHz at gain 10, 1 kHz at gain 1000).
**Method:** Anchor the ladder on one sentence: **gain 1 → 1 MHz; every ×10 of
gain costs one decade of bandwidth.** Anything GATE asks about op-amp
bandwidth reduces to that line. (`16-Frequency-Response.md`,
`32-Single-File-Cheatsheet.md` §8.)

---

## Trap box (exam-day killers)

- **Using the virtual short with no feedback** (open loop / comparator) — the
  output is `±V_sat` and `v+ ≠ v−`.
- **Forgetting to check saturation.** `|v_o| = |A|·|v_in| ≤ rail` — one line,
  one mark. Once clipped, every other number in the problem is invalid.
- **Using the signal gain instead of the noise gain** for offset and bandwidth:
  both use `1 + R_f/R_1`, for *both* topologies.
- **Writing an input current at the op-amp pins.** `i+ = i− = 0`, always.
- **Confusing `R_out = 0` (ideal) with the real `75 Ω`.** For loading questions
  on a *non-ideal* source you may need 75 Ω; for ideal analysis it is 0.
- **Dropping the `1 +` in the non-inverting gain** (`1 + R_f/R_1`).
- **Confusing `SR = 2πfV_pk` with the GBW limit.** For a 741 the slew limit is
  always 2× tighter — compute both.
- **Ignoring the input common-mode range.** A valid-looking answer can be
  impossible on real silicon.
- **Treating `R_s` (source resistance) as loading the `+` input.** It drops
  nothing, because no current flows.
- **Forgetting that a bare 741 is a poor comparator** (SR = 0.5 V/µs, no input
  clamp diodes).

## Final recall drill (do in 60 seconds)

1. Ideal op-amp: `A`, `R_in`, `R_out`? → *`∞`, `∞`, `0`.*
2. Virtual short needs? → *negative feedback **and** linear operation.*
3. 741: `A`, `SR`, `GBW`? → *`2×10⁵` (106 dB), `0.5 V/µs`, `1 MHz`.*
4. `SR = 0.5 V/µs`, `V_pk = 10 V` ⇒ `f_max`? → *7.96 kHz.*
5. `GBW = 1 MHz` at gain 100 ⇒ bandwidth? → *10 kHz.*
6. `V_os = 2 mV`, non-inverting gain 51 ⇒ output error? → *102 mV.*
7. `V_os = 2 mV`, **inverting** gain −50 ⇒ output error? → *102 mV (noise gain 51!).*
8. `I_B = 80 nA`, `R1 ∥ R_f = 909 Ω` ⇒ offset? → *73 µV.*
9. `A = 2×10⁵`, `V_sat = 12 V` ⇒ minimum `v_id` to saturate? → *60 µV.*
10. Dominant pole of a 741? → *`GBW/A` = 1e6/2e5 = 5 Hz.*

---

