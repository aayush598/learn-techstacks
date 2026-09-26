# Op-Amp Amplifiers and Summers — Practice (Learn by Solving)

> **The idea in one line:** there are only two shapes of op-amp amplifier —
> *inverting* (`A_v = −R_f/R1`, `R_in = R1`) and *non-inverting*
> (`A_v = 1 + R_f/R1`, `R_in = ∞`) — and every summer, difference amplifier and
> cascade is just those two with more terminals attached.
>
> **How to use:** solve each question fully before reading the answer. Cover the
> **Answer**/**Method** with paper, do it, then reveal. If you miss one, solve
> the next 3 in the file to lock the pattern. No need to read the chapter notes
> first — every concept is taught through the drill itself. Open
> `20-Op-Amp-Amplifiers-Summers.md` or `32-Single-File-Cheatsheet.md` only when
> you want the underlying theory.

## Concept box (what you must internalise)

- Inverting: `v− = 0` (virtual ground), so `A_v = −R_f/R1` and `R_in = R1`.
  The **resistor** defines the gain; the `+` input must be grounded (0 V).
- Non-inverting: `v− = v+ = v_in` through a divider, so
  `A_v = 1 + R_f/R1` (never 0, never without the 1) and `R_in = ∞`.
- Follower: output straight to `v−` ⇒ `A_v = +1`, `R_in = ∞`, `R_out = 0`.
  The universal impedance transformer.
- Summer: `v_o = −R_f·(Σ v_i/R_i)`. Each input sees its own `R_i` to ground and
  the inputs are isolated from each other.
- Difference amplifier: `v_o = (R2/R1)(v2 − v1)` **only if** `R2/R1 = R4/R3`.
  Resistor mismatch is what limits CMRR.
- Cascade: `A_tot = Π A_i` (dB adds), but bandwidth does **not** multiply —
  each stage's own `GBW/noise gain` is what matters, and the first stage
  dominates.
- Trap: `R_out ≈ 0` is an *ideal-op-amp* statement. Cascade loading is only
  visible when a stage has a real output resistance.
- Trap: saturation clips the output and the virtual short dies. Always test
  `|v_o| ≤ rail` (for a 741, ±12 V on ±15 V supplies).

---

## Questions

### Q1. (Easy) Inverting amplifier with `R1 = 1 kΩ`, `R_f = 10 kΩ`. Give the
closed-loop gain and the input resistance seen by the source.
**Answer:** `A_v = −R_f/R1 = −10`; `R_in = R1 = 1 kΩ`.
**Method:** Two formulas, no analysis. `v− = 0` ⇒ the source sees `R1` to a
virtual ground. `R_in` for an inverting amplifier is the *input resistor* — not
infinity, not `R_f`. (`20-Op-Amp-Amplifiers-Summers.md` §20.1.)

### Q2. (Easy) Non-inverting amplifier with `R1 = 1 kΩ`, `R_f = 9 kΩ`. Gain and
input resistance?
**Answer:** `A_v = 1 + R_f/R1 = 1 + 9 = +10`; `R_in = ∞` (no input current,
so the source is unloaded).
**Method:** The divider at `v−` must equal `v_in`:
`v_o·R1/(R1+R_f) = v_in` ⇒ `v_o = v_in(1 + R_f/R1)`. If your answer is `9`,
you dropped the 1 — the single most common error in this topic.

### Q3. (Easy) Voltage follower. Gain, input resistance, output resistance, and
its one-line job.
**Answer:** `A_v = +1`; `R_in = ∞`; `R_out = 0`. It is a buffer: copies a
voltage without loading the source and without being loaded by the load.
**Method:** `v−` tied directly to `v_o` ⇒ `v+ = v−` ⇒ `v_o = v_in`. The
`R_in = ∞ / R_out = 0` pair is the maximum impedance-transforming property any
circuit can offer, and it is why a follower can drive a 1 kΩ load from a
1 MΩ source.

### Q4. (Easy) Weighted summer: `R_f = 4 kΩ`, `R1 = 1 kΩ`, `R2 = 2 kΩ`,
`R3 = 4 kΩ`, with `v1 = 1 V`, `v2 = 2 V`, `v3 = 1 V`. Find `v_o`.
**Answer:** `v_o = −R_f(v1/R1 + v2/R2 + v3/R3) = −4k(1/1k + 2/2k + 1/4k) =
−4k(1 + 1 + 0.25) = −9 V`.
**Method:** Write each input current `v_i/R_i`, sum them, multiply by `−R_f`.
Work in **mA and kΩ** to keep it clean: `1 mA + 1 mA + 0.25 mA = 2.25 mA`,
times `−4 kΩ` = `−9 V`. (`20-Op-Amp-Amplifiers-Summers.md` §20.4.)

### Q5. (Easy) Which of the two classic amplifiers inverts the signal, and which
amplifies by *at least* 1?
**Answer:** Inverting (`A_v = −R_f/R1`, always negative, can be any magnitude);
non-inverting (`A_v = 1 + R_f/R1`, always positive, `≥ 1`).
**Method:** Two checks, both instant: sign of `A_v`, and whether `|A_v| < 1` is
possible. Only the inverting stage can attenuate (`R_f < R1`) and only the
non-inverting stage can give a gain between 1 and `1+R_f/R1`.

### Q6. (Easy) Why must the `+` input of an inverting amplifier be connected to
ground? What if it were left floating?
**Answer:** To make `v− = 0` (a virtual ground) so that `i = v_in/R1` is the
*only* current in the input resistor and `v_o = −i·R_f` follows. Floating `+`
means the feedback forces `v+ = v−` at whatever unknown voltage — the circuit
is indeterminate (and in reality picks up offset/noise).
**Method:** Grounding `+` is what creates the "virtual ground". This is also why
a summing amplifier gets its property from that ground: the node is at 0 V
without being connected to ground, so each input resistor sees its own `v_i`.

### Q7. (Moderate) Inverting amplifier, `R1 = 2 kΩ`, `R_f = 40 kΩ`. Gain and
input resistance. Now put a `1 MΩ` load on the output: does anything change?
**Answer:** `A_v = −40/2 = −20`; `R_in = 2 kΩ`. The `1 MΩ` load changes
nothing (ideal `R_out = 0` holds the output voltage).
**Method:** Gain from resistors, `R_in = R1`, and loading is a non-issue because
`R_out = 0`. For a real 741 (`R_out ≈ 75 Ω`) the gain would drop by
`(1 + 75/40,000) ≈ 0.2 %` — negligible, which is exactly why op-amps can drive
heavy loads. (`19-Op-Amp-Fundamentals.md`.)

### Q8. (Moderate) A source with `R_s = 10 kΩ` drives a non-inverting amplifier
(`R1 = 1 kΩ`, `R_f = 9 kΩ`). What gain does the source see?
**Answer:** **10** — unchanged. The `+` input draws no current, so `R_s` drops
nothing.
**Method:** Contrast with the inverting case (Q9): there, the source current
*must* equal `v_in/R1`, so `R_s` is in series with `R1` and reduces the gain.
One of these two topologies is the answer to "my source is too high-impedance" —
use the non-inverting one. (`20-Op-Amp-Amplifiers-Summers.md` §20.6.)

### Q9. (Moderate) A source with `R_s = 5 kΩ` drives an **inverting**
amplifier with `R1 = 1 kΩ`, `R_f = 10 kΩ`. Find the gain from the *source* EMF
and compare it with the stage's own gain.
**Answer:** `A_v = −R_f/(R_s + R1) = −10 k/(5 k + 1 k) = −1.67`, instead of the
stage's ideal `−10` — the source resistance costs a factor of 6.
**Method:** For an inverting stage the source current *must* equal `v_in/R1`, so
`R_s` ends up in series with `R1` and reduces the gain seen by the source. This
is the mirror image of Q8 (non-inverting: `R_s` drops nothing) and the reason
sensor front-ends that must not load a high-impedance source use the
non-inverting topology.

### Q10. (Moderate) Three equal inputs of `1 V` each into a summer with all
input resistors `1 kΩ` and `R_f = 3 kΩ`. Find `v_o`.
**Answer:** `v_o = −3k(1/1k + 1/1k + 1/1k) = −3k(3 mA) = −9 V`.
**Method:** Equal resistors ⇒ `v_o = −(R_f/R_i)(v1+v2+v3) = −3(3 V) = −9 V`.
Note the polarity: an inverting summer outputs the **negative** of the sum.
The single-resistor-per-input rule makes a 3-bit "digital-to-analogue"
converter. (`20-Op-Amp-Amplifiers-Summers.md` §20.4.)

### Q11. (Moderate) Difference amplifier: `R1 = R3 = 10 kΩ`, `R2 = R4 = 100 kΩ`,
with `v1 = 1.0 V` (inverting side) and `v2 = 1.5 V` (non-inverting side). Find
`v_o`.
**Answer:** `A_d = R2/R1 = 10`; `v_o = 10(v2 − v1) = 10(0.5) = 5 V`.
**Method:** Condition first: the gain formula `v_o = (R2/R1)(v2 − v1)` needs
`R2/R1 = R4/R3` (here both are 10) — that is what cancels the common mode.
Then just subtract and multiply. Never mix up which labeled input is
inverting. (`20-Op-Amp-Amplifiers-Summers.md` §20.6.)

### Q12. (Moderate) Inverting amplifier, `R_f/R_1 = 100`, `v_in = 0.5 V`, output
rails `±12 V` (741 on ±15 V). What is the output, and what is the linear input
range?
**Answer:** Wanted output `−50 V` ⇒ the output **clamps at −12 V**. Linear range
is `|v_in| ≤ 12/100 = 0.12 V`.
**Method:** Ideal gain first, then the rail check. Clipping is a *hard* result
in GATE questions: the answer is the rail, and the virtual short must be
declared invalid. (`19-Op-Amp-Fundamentals.md` §19.6.)

### Q13. (Moderate) Verify the Q4 summer by superposition: find the
contribution of `v1` alone, then of `v2` alone, then of `v3` alone.
**Answer:** `v1` alone: `−4k(1/1k) = −4 V`. `v2` alone: `−4k(2/2k) = −4 V`.
`v3` alone: `−4k(1/4k) = −1 V`. Sum `= −9 V` ✓.
**Method:** Linear circuit ⇒ superposition is legal (never for power). Hit one
input at a time, zero the others (a zeroed *voltage* source is a short). The
cross-check is instant and catches any sign slip. (`32-Single-File-Cheatsheet.md`
§1.)

### Q14. (Moderate) Cascade: stage 1 non-inverting with `R1 = 1 kΩ`,
`R_f = 9 kΩ`; stage 2 inverting with `R1 = 1 kΩ`, `R_f = 10 kΩ`. Total gain,
in V/V, in dB, and its sign.
**Answer:** `A_1 = +10`, `A_2 = −10`; `A_tot = −100` ⇒ `20 log10 100 = 40 dB`,
**inverting overall** (one inverting stage in the chain).
**Method:** Multiply the gains, add the dB, and track the **sign**: an odd
number of inverting stages gives an overall inversion. The number of `−`
signs is a one-mark question in its own right.

### Q15. (Moderate) You need a gain of `−25` and you have a `4 kΩ` resistor.
Size `R_f`. What is the resulting input resistance?
**Answer:** `R_f = 25 × 4 kΩ = 100 kΩ`; `R_in = 4 kΩ`.
**Method:** `R_f = |A_v|·R1` — design the feedback resistor from the wanted gain
and the one resistor you have. Always state `R_in = R1` as well; exam
questions that ask "gain and input impedance" want both numbers.

### Q16. (Moderate) Design a non-inverting amplifier of gain 51.
**Answer:** Need `R_f/R1 = 50`, so e.g. `R1 = 1 kΩ`, `R_f = 50 kΩ`
(`20 log10 51 = 34.1 dB`).
**Method:** `A_v = 1 + R_f/R1` ⇒ `R_f = (A_v − 1)·R1`. The subtraction of 1 is
the whole difficulty. In practice keep `R1 ≥ 1 kΩ` (loading the `+` input) and
`R_f` below a few hundred kΩ (offset and bias-current errors), which is why
`51` is often built as two stages.

### Q17. (Moderate) A summer has `R_f = 10 kΩ`; inputs are `R1 = 10 kΩ`
(`v1 = 2 V`) and `R2 = 5 kΩ` (`v2 = −4 V`). Find `v_o`, and explain the sign of
the second term.
**Answer:** `v_o = −10k(2/10k + (−4)/5k) = −10k(0.2 mA − 0.8 mA) = −10k(−0.6 mA)
= +6 V`. The `−4 V` input gives a **positive** contribution because the summer
inverts every input.
**Method:** Keep the resistor and the voltage signed separately:
`v_o = −R_f·Σ(v_i/R_i)`. A negative input voltage → negative current → the
inverting summer flips it to a positive output. Sign errors here are the most
common arithmetic slip; write the currents with signs.

### Q18. (Moderate) A high-impedance source (`1 MΩ` output) must drive a
`1 kΩ` load. Compare (a) direct connection and (b) via a follower.
**Answer:** (a) Load voltage `= 1 V × 1k/(1M + 1k) = 0.999 V` but the source
sees `1 MΩ ∥ 1 kΩ = 999 Ω` — the source is effectively shorted to ground.
(b) Follower: the source sees `R_in = ∞` (unloaded) and the load sees
`R_out = 0`, so the load gets the full 1 V and the source keeps its full
signal.
**Method:** Two numbers per case: the input resistance the source sees and the
voltage division into the load. `1k∥1M = 999 Ω` shows the damage. The follower
restores both. This is the classic "buffer" numerical.

### Q19. (Easy) What does an inverting amplifier become if you short
`R_f` (`R_f = 0`)?
**Answer:** `v_o = 0` for any input — the op-amp output is tied to its own
inverting input (a **voltage follower of zero**, i.e. a clamp, not a follower).
It is *not* a unity-gain follower; a follower requires the feedback to come
from the output to the `−` input with the signal on the `+` input.
**Method:** `A_v = −R_f/R1 = 0`. The popular confusion is "0 feedback gain =
follower"; the follower is a *non-inverting* unity stage (`R_f = ∞` from output
to `−` with the input on `+`). (`20-Op-Amp-Amplifiers-Summers.md` §20.1.)

### Q20. (Easy) In a 3-input summer, what is the input resistance seen by
each source? Does `v2` affect the current drawn by the `v1` branch?
**Answer:** Each source sees its own resistor: `R1`, `R2`, `R3` respectively. No
crosstalk — `v2` draws no extra current through `R1`.
**Method:** The summing node is a **virtual ground at 0 V**, so the current in
`R1` is `v1/R1` and nothing else. That input isolation *is* the reason the
summer is useful (and why an inverting summer is preferable to a
non-inverting-average summer, whose `+` input is a real node where inputs
interact).

### Q21. (Moderate) Stage 1 is a **transistor** stage with `A_1 = 10` and
`R_out1 = 1 kΩ`. Stage 2 is an inverting op-amp with `R1 = 10 kΩ`,
`R_f = 100 kΩ`. Find the total gain and compare with the unloaded `−100`.
**Answer:** Divider: `10 k/(1 k + 10 k) = 0.909`; so `A_tot = 10 × 0.909 × (−10)
= −90.9`, instead of `−100` — a **9.1 % loss**.
**Method:** Loading happens *before* you apply the second stage's gain:
`v_at_stage2 = A_1·v_in·(R_in2/(R_in2 + R_out1))` with `R_in2 = R1 = 10 kΩ`.
Rule: a stage loads the one before it; op-amp stages do not load each other
(`R_out = 0`), but a transistor stage's `R_C` absolutely does.
(`09-BJT-Amplifiers.md`.)

### Q22. (GATE-level) A 741 non-inverting amplifier has gain 11
(`R1 = 10 kΩ`, `R_f = 100 kΩ`), rails ±12 V. Largest input sine peak before
clipping?
**Answer:** `V_pk,max = 12/11 = 1.09 V`.
**Method:** `V_pk,max = V_rail/A_v`. Convert if needed: rms
`= 1.09/√2 = 0.77 V`. Always state the peak, since rails are peak limits.
(`19-Op-Amp-Fundamentals.md`.)

### Q23. (Moderate) A non-inverting amplifier must have gain exactly 3. What
resistor ratio is required, and is it convenient?
**Answer:** `R_f/R1 = 2`. Convenient — but note the small ratios are awkward
in practice: `R1 = 100 kΩ`, `R_f = 200 kΩ` also works, whereas
`R1 = 1 kΩ, R_f = 2 kΩ` wastes current through the `+`-to-ground leg.
**Method:** Design rule: keep `R1` in the `1 kΩ`–`100 kΩ` window — too small
wastes current in the divider, too large amplifies bias-current and offset
errors. A gain of 3 with `R1 = 1 kΩ` gives a divider current of 1 mA — pure
waste.

### Q24. (Easy) A cascade has a total gain of `1000`. Express it in dB, and
say how the gain falls with frequency once the first pole arrives.
**Answer:** `20 log10 1000 = 60 dB`. Beyond the closed-loop bandwidth it falls at
`−20 dB/decade` (one pole per stage ⇒ `−40 dB/decade` for a two-stage cascade).
**Method:** `20 log10` for voltage; note the ladder 1→0, 10→20 dB, 100→40 dB,
1000→60 dB. The slope comes from the number of stages, not from the gain
(`16-Frequency-Response.md`).

### Q25. (GATE-level) Instrumentation-style difference amplifier: `R1 = R3 = 10 kΩ`,
`R2 = R4 = 110 kΩ`. Find the differential gain, and the output for
`v1 = 2.0 V`, `v2 = 2.02 V`.
**Answer:** `A_d = 110/10 = 11`; `v_o = 11(2.02 − 2.00) = 0.22 V`.
**Method:** Two steps: check `R2/R1 = R4/R3` (both 11) so the common mode
cancels, then subtract-then-multiply. Using 11 gives a high differential gain
with small resistors — the standard instrumentation-amplifier front end.
(`20-Op-Amp-Amplifiers-Summers.md` §20.6.)

### Q26. (GATE-level) Design a weighted summer with `R_f = 10 kΩ` that computes
`v_o = −(5v1 + 10v2 + 2.5v3)`. Give the input resistors, then evaluate for
`v1 = 1 V`, `v2 = 0.5 V`, `v3 = 2 V` on a `±12 V` op-amp.
**Answer:** `R1 = R_f/5 = 2 kΩ`; `R2 = R_f/10 = 1 kΩ`; `R3 = R_f/2.5 = 4 kΩ`.
Then `v_o = −10k(1/2k + 0.5/1k + 2/4k) = −10k(0.5 + 0.5 + 0.5) = −15 V` ⇒
**clipped at −12 V**.
**Method:** `v_o = −R_f·Σ(v_i/R_i)` ⇒ coefficient of `v_i` is `R_f/R_i`, so
`R_i = R_f/coefficient`. Then do the DC evaluation and the rail check — the
design "works" but the *chosen inputs* overdrive the output. That combination
(sound design, inadmissible inputs) is a favourite GATE trap.

### Q27. (GATE-level) In Q12 the inverting stage is railed at −12 V with
`v_in = 0.5 V`, `R1 = 1 kΩ`. Where does the inverting-input voltage actually
sit, and why is the "virtual ground" claim now false?
**Answer:** No longer at 0 V. Once saturated, feedback cannot hold the node, and
`v−` moves toward the input side (roughly `v_in` for a hard-clamped output,
limited by the internal saturation and the input clamp diodes). The claim
"virtual ground" depended on the op-amp being **linear**: with the output
pinned, the amplifier is not responding, so KCL at the node is no longer
`v_in/R1 = −v_o/R_f` with `v− = 0`.
**Method:** The virtual ground is a *consequence* of high open-loop gain times
negative feedback, not a property of the node. Once the output cannot follow,
`v+ ≠ v−`. The correct analysis of a saturated op-amp: "output at the rail, all
other answers invalid". (`19-Op-Amp-Fundamentals.md` §19.2.)

### Q28. (GATE-level) A difference amplifier has `R1 = R3 = 10 kΩ`,
`R2 = 100 kΩ`, but `R4 = 101 kΩ` (1 % high). Find the differential gain, the
common-mode gain, and the CMRR in dB for `v1 = v2 = 1 V` common mode.
**Answer:** `A_cm`: with both inputs at `v_cm`, `v_o = (R2/R1)v_cm − (R4/R3)v_cm
= 10v_cm − 10.1v_cm = −0.1v_cm` ⇒ for `v_cm = 1 V`, `v_o = −0.1 V`,
`|A_cm| = 0.1`. Differential gain (matched path) `= 10`. 
`CMRR = 10/0.1 = 100` ⇒ `20 log10 100 = **40 dB**`.
**Method:** Apply the *unmatched* formula `v_o = (R2/R1)v2 − (R4/R3)v1` — it is
valid with or without matching, so never assume cancellation. Then
`CMRR = |A_d/A_cm|`. One 1 % resistor error cost the CMRR from ∞ to 40 dB;
that is why instrumentation resistors must be matched, not merely accurate.
(`20-Op-Amp-Amplifiers-Summers.md` §20.6, `32-Single-File-Cheatsheet.md` §8.)

### Q29. (GATE-level) How accurate must the resistor ratios be for a difference
amplifier to reach 100 dB of CMRR? Derive it, then check what 0.1 % resistors
actually give.
**Answer:** With `R2/R1 = k(1+ε)` and `R4/R3 = k(1−ε)`:
`v_o(diff) = k·v_id`; common mode gives `v_o = v_cm[k(1+ε) − k(1−ε)] = 2kε·v_cm`,
so `CMRR = k/(2kε) = 1/(2ε)`. For `CMRR = 10⁵`: `ε = 5×10⁻⁶` = **0.0005 %**.
With 0.1 % (`ε = 10⁻³`): `CMRR = 500` ⇒ `20 log10 500 = 54 dB`.
**Method:** The insight: **CMRR depends on the *ratio mismatch*, not on the
absolute tolerance** — two 0.1 % resistors can still be a perfectly matched
10:1 ratio if they came from the same thin-film network. Also note the dB
result: 0.1 % matching gives only 54 dB, which is why real instrumentation
amplifiers use laser-trimmed networks and/or a second (differential) stage.

### Q30. (GATE-level) Cascade of two op-amp stages: (1) a 741 non-inverting
stage of gain 10, (2) a 741 inverting stage of `R1 = 1 kΩ`, `R_f = 10 kΩ`.
Find the total gain, each stage's bandwidth, the overall bandwidth, and say
whether stage 1 is loaded by stage 2.
**Answer:** `A_tot = 10 × (−10) = −100` (40 dB, inverting).
Stage 1 BW `= 1 MHz/10 = 100 kHz`. Stage 2 noise gain 11 ⇒
`BW = 1 MHz/11 = 90.9 kHz`. Overall `≈ 90–100 kHz` (both stages are close, so
the roll-off becomes steeper after ~100 kHz). **Not loaded**: stage 2's
`R_in = R1 = 1 kΩ` is driven by stage 1's `R_out = 0`, so the divider is
`1k/(1k+0) = 1`.
**Method:** Three numbers per stage: gain (multiply), noise-gain bandwidth
(`GBW/noise gain`, take the smallest), and loading (zero for op-amp→op-amp).
Contrast Q21, where the first stage was a transistor with `R_out = 1 kΩ` and
9.1 % of the gain was lost. (`16-Frequency-Response.md`,
`21-Op-Amp-Integrators-Differentiators.md`.)

### Q31. (GATE-level) You must combine three 0–1 V sensor signals into one
signal. (a) Design an inverting **averaging** inverter:
`v_o = −(v1 + v2 + v3)/3`. (b) Give the full-scale output. (c) Now design
`v_o = −2(v1 + v2 + v3)` and give its full-scale output. (d) Which of the two
has the smaller input-offset error, and why?
**Answer:** (a) coefficient per input `= −R_f/R_i = −1/3` ⇒ `R_f = R_i/3`:
`R1 = R2 = R3 = 30 kΩ`, `R_f = 10 kΩ`. (b) Full scale (all inputs 1 V):
`v_o = −3/3 = −1 V`. (c) `R_f/R_i = 2` ⇒ `R1 = R2 = R3 = 10 kΩ`,
`R_f = 20 kΩ`; full scale `= −2 × 3 = −6 V`. (d) The **averaging** version:
offset error `= V_os(1 + R_f/R1) = V_os(1 + 1/3) = 1.33·V_os` versus
`V_os(1 + 2) = 3·V_os` for the ×2 summer — a factor of 2.25 less offset error,
because a *large* feedback resistor also multiplies the offset.
**Method:** Turn each wanted coefficient into a resistor ratio
(`R_i = R_f / |coefficient|`), then evaluate at full scale and check the rails.
For (d) the governing fact is the offset formula from `Practice-19`:
`Δv_o = V_os·(noise gain) = V_os(1 + R_f/R_1)`, so keeping `R_f/R_1` small
minimises offset **and** bias-current error — at the cost of needing large
input resistors, which then pick up noise.
(`19-Op-Amp-Fundamentals.md` §19.4.)

### Q32. (GATE-level) Inverting amplifier, gain `−10`, input `2 V pk` sine,
rails `±12 V`. Describe the output waveform, its peak, and the input value at
which the waveform starts to clip.
**Answer:** Ideal output would be `20 V pk`, so the output is a **clipped sine**:
it follows the input until `10|v_in| = 12 V`, i.e. `|v_in| = 1.2 V`, then stays
flat at `±12 V` (flat tops for a sine input). Peak output = 12 V; clipping starts
at `v_in = ±1.2 V`, i.e. `sin θ = 0.6` ⇒ `θ = 36.9°`. Clipping therefore covers
`180° − 36.9° − 36.9° = 106.2°` in **each** half cycle, and there are two of
them: `2 × 106.2° = 212.4°` of 360°, i.e. **≈ 59 % of the period** is clipped
(only the two 36.9° corners near each zero crossing are undistorted).
**Method:** For a clipped-sine description GATE wants three things: the
**clipped level** (the rail), the **input value where clipping starts**
(`V_rail/|A_v|`), and the **conduction angle**. Work from
`v_o = A_v·v_in` clipped at the rails — do not try to redraw the waveform
algebraically. Count the clipped fraction per *half cycle* and remember to
double it (`36.9°` and `143.1°` bound one flat region; `216.9°` and `323.1°`
bound the other). (`19-Op-Amp-Fundamentals.md` §19.6.)

### Q33. (GATE-level) A non-inverting amplifier (`R1 = 1 kΩ`, `R_f = 4 kΩ`, gain
5) has a load `R_L = 2 kΩ` and drives a following inverting stage
(`R1 = 2 kΩ`, `R_f = 20 kΩ`, gain −10). Find the total gain, and then repeat
with the first stage's `R_out` taken as a realistic 75 Ω.
**Answer:** Ideal: `5 × (−10) = −50` (`20 log10 50 = 34.0 dB`).
With `R_out = 75 Ω`: divider `2k/(75 + 2k) = 0.9643`; stage 2 sees
`5 × 0.9643 = 4.82`; total `= 4.82 × (−10) = −48.2` — a **3.6 % loss**.
**Method:** Insert the load `R_in2 = R1` of the *next* stage into a divider with
the previous `R_out`. Rule of thumb: the error is `R_out/R_in2`, i.e. `75/2000 =
3.75 %`. Op-amp→op-amp cascades are therefore accurate to a few per cent, but
transistor→op-amp cascades lose much more (Q21). (`09-BJT-Amplifiers.md`.)

### Q34. (GATE-level) A capacitor `C` is placed **in parallel** with `R_f` in an
inverting amplifier (`R1 = 10 kΩ`, `R_f = 100 kΩ`, `C = 10 nF`). Give the DC
gain, the high-frequency behaviour, and the corner frequency.
**Answer:** DC gain `= −100` (the capacitor is open, so the gain is the normal
`−R_f/R1`). At high frequency the capacitor shorts `R_f`, so
`A_v → −(1/jωC)·(1/R1)` — the gain falls at `−20 dB/decade` and the circuit
becomes an **integrator**. Corner `f_c = 1/(2πR_fC) = 1/(2π × 100 k × 10 n)
= 1/(6.283×10⁻³) = 159 Hz`.
**Method:** The DC gain is set by the resistor that is *there* at DC; the pole
is set by the parallel combination `R_f ∥ (1/jωC)`. Check the arithmetic:
`R_f C = 1e5 × 1e-8 = 1e-3 s` ⇒ `f_c = 1/(2π × 1 ms) = 159 Hz`.
(`21-Op-Amp-Integrators-Differentiators.md` — the same resistor-plus-capacitor
trick, seen from the amplifier side.)

---

## Trap box (exam-day killers)

- **Dropping the `1 +` in the non-inverting gain.** `1 + R_f/R1`, always.
- **Writing the inverting gain as `R_f/R1` without the minus sign.**
- **`R_in` of a non-inverting stage quoted as `R1`.** It is `∞`; only the
  inverting stage loads the source with `R1`.
- **Confusing the signal gain with the noise gain** — bandwidth and offset both
  use `1 + R_f/R1` (see `Practice-19`).
- **Assuming `R_f = 0` makes a follower.** It makes `v_o = 0`.
- **Summer sign errors.** `v_o = −R_f·Σ(v_i/R_i)`: a negative input voltage gives
  a positive output contribution.
- **Assuming an inverting summer's inputs interact.** They do not (virtual
  ground isolates them).
- **Using the difference-amplifier formula with unmatched resistors.** Use
  `v_o = (R2/R1)v2 − (R4/R3)v1` always; the cancellation is a *consequence* of
  matching, not an assumption you may skip.
- **Forgetting loading in a cascade** when the first stage has a real
  `R_out` (Q21, Q33).
- **No saturation check.** `|v_o| ≤ rail` before you believe any answer.
- **Summing several `1` V inputs and forgetting the total** — check the sum,
  not each term (`|Σ|` can be 3× each term).

## Final recall drill (do in 60 seconds)

1. Inverting `R1 = 1 kΩ`, `R_f = 5 kΩ`, `v_in = 0.2 V` → `v_o`, `R_in`? →
   *`−1 V`, `1 kΩ`.*
2. Non-inverting `R_f = 9 kΩ`, `R1 = 1 kΩ` → gain, `R_in`? → *`+10`, `∞`.*
3. Follower: gain / `R_in` / `R_out`? → *`+1` / `∞` / `0`.*
4. `R_f = 4 kΩ`, `R1 = 1 kΩ`, `R2 = 2 kΩ`, `R3 = 4 kΩ`, `v = 1, 2, 1` V → `v_o`? →
   *`−9 V`.*
5. Three equal 1 V inputs, `R_i = 1 kΩ`, `R_f = 3 kΩ` → `v_o`? → *`−9 V`.*
6. Difference amp, ratios matched at 2, `v2 − v1 = 3 V` → `v_o`? → *`+6 V`.*
7. Cascade: non-inv 3 then non-inv 4 → total? → *`12`.*
8. Inverting amp, gain −100, rails ±12 V, `v_in = 0.2 V` → `v_o`? → *clips at
   `−12 V`.*
9. `R_f = 0` in an inverting stage → ? → *`v_o = 0` (clamp).*
10. `A_tot = 1000` in dB? → *60 dB.*

---

