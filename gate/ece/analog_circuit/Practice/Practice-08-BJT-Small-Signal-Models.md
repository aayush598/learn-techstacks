# BJT Small-Signal Models — Practice (Learn by Solving)

> **The idea in one line:** this file teaches the linear BJT through 34 questions
> only — that the exponential transistor collapses into two resistors and one
> controlled source at the Q-point, that `gm`, `rπ`, `re`, `ro` are all *the same
> four numbers* reachable from `I_C`, `β`, `V_A`, and that converting between
> hybrid-π and T-model is a two-line algebraic habit.
>
> **How to use:** solve each question fully before reading the answer. Cover the
> **Answer**/**Method** with paper, do it, then reveal. If you miss one, solve the
> next 3 in the file to lock the pattern. No need to read the chapter notes
> first — every concept is taught through the drill itself. Open
> `08-BJT-Small-Signal-Models.md` or `32-Single-File-Cheatsheet.md` only when you
> want the underlying theory.

## Concept box (what you must internalise)

- `gm = I_C/V_T` with `V_T = 25 mV` ⇒ the "40" rule: `gm = 40·I_C[mA]` mA/V.
- `rπ = β/gm = β·V_T/I_C` — the **base-side** resistance (hybrid-π).
- `re = V_T/I_E ≈ V_T/I_C` — the **emitter-side** resistance (T-model).
- `ro = V_A/I_C` — Early effect; ignore it only when `ro ≫ R_C`.
- Golden identities: `gm·rπ = β`, `gm·re = α`, `rπ = (β+1)·re`, and
  `1/gm ≈ re ≈ rπ/β`.
- The classic set to memorise: `I_C = 1 mA, β = 100, V_A = 100 V` ⇒
  `gm = 40 mA/V`, `rπ = 2.5 kΩ`, `re = 25 Ω`, `ro = 100 kΩ`.
- Method: fix `I_C` first (that fixes `gm`, `re`, `ro`), then let β fix `rπ`.
- Trap: do not put `rπ` and `re` in the same circuit — one is base-side, the
  other emitter-side.

---

## Questions

### Q1. (Easy) `I_C = 1 mA` at the Q-point. Find `gm`.
**Answer:** `gm = 40 mA/V`.
**Method:** `gm = I_C/V_T = 1 mA/25 mV = 40 mA/V` (equivalently `0.04 S`). The
units are the tell: transconductance is mA/V, i.e. millisiemens. Memorise the
conversion `gm = 40·I_C[mA] mA/V` — it turns every future BJT numerical into
one multiplication.

### Q2. (Easy) `I_C = 1 mA`, `β = 100`. Find `rπ`.
**Answer:** `rπ = 2.5 kΩ`.
**Method:** `rπ = β/gm = 100/0.04 = 2500 Ω`. Or directly `rπ = β·V_T/I_C =
100 × 25 mV/1 mA = 2.5 kΩ`. Recognise this as the most common number in the
subject — if you see `I_C = 1 mA, β = 100` on a GATE paper, `rπ = 2.5 kΩ` is
almost certainly one of the intermediate answers.

### Q3. (Easy) `I_C = 1 mA`, `β = 100`. Find `re`.
**Answer:** `re ≈ 25 Ω` (exactly `24.75 Ω`).
**Method:** `re = V_T/I_E` with `I_E = I_C(1 + 1/β) = 1.005 mA` ⇒
`re = 25 mV/1.005 mA = 24.75 Ω`. Every textbook rounds to 25 Ω using
`re ≈ V_T/I_C`; state that you did so. Note the magnitude difference: `rπ` is
`β` times bigger than `re`, which is the whole reason a common-base stage has
such a low input resistance.

### Q4. (Easy) `V_T = 25 mV`, `I_E = 2 mA`. Find `re`.
**Answer:** `re = 12.5 Ω`.
**Method:** `re = V_T/I_E = 25 mV/2 mA = 12.5 Ω`. Emitter current doubles, so
`re` halves — `re` is a *reciprocal* of current, unlike `gm` which is directly
proportional. If you ever catch yourself multiplying by `I_E` instead of
dividing, you are thinking of `1/re`, not `re`.

### Q5. (Easy) `V_A = 75 V` and `I_C = 0.5 mA`. Find `ro`.
**Answer:** `ro = 150 kΩ`.
**Method:** `ro = V_A/I_C = 75/0.5m = 150 000 Ω`. `V_A` (Early voltage) is tens
of volts, `I_C` is milliamps, so `ro` is always tens of kΩ — big enough that you
can usually drop it, which is exactly why GATE says "ignore `ro`" so often.

### Q6. (Easy) `I_C = 2.5 mA`. Find `gm` using the "40" rule and check with the
formula.
**Answer:** `gm = 100 mA/V`.
**Method:** `40 × 2.5 = 100 mA/V`. Check: `2.5 mA/25 mV = 100 mA/V` ✓. Also
`1/gm = 10 Ω`. The "40" is nothing more than `1/25 mV`; keep it as a shortcut
for speed, but always be able to fall back on `I_C/25 mV` when the current is
not a round number.

### Q7. (Easy) Which model contains `rπ` and which contains `re`? Where do they
sit?
**Answer:** `rπ` is the **base-side** resistor of the **hybrid-π** model (from
base to emitter). `re` is the **emitter-side** resistor of the **T-model** (from
emitter to the internal reference node).
**Method:** Memorise the mnemonics: "**π** is at the **B**ase" and "**T** has
resistance at the e**T**ernal emitter". They describe the *same* transistor;
`rπ` and `re` are never in one circuit. If a question hands you `re` (T-model
data), you are probably looking at a common-base or emitter-follower problem;
if it hands you `rπ`, expect a common-emitter problem.

### Q8. (Easy) Check `rπ = (β+1)·re` for `β = 100`, `re = 25 Ω`.
**Answer:** `(101)(25) = 2525 Ω` vs `rπ = 2500 Ω` — agreement to 1%.
**Method:** Substitute both. The 1% gap is the difference between `(β+1)·V_T/I_C`
and `(β+1)·V_T/I_E`. Use `(β+1)re` when you know `re` (T-model) and `β/gm` when
you know `gm`; they are interchangeable. For β ≥ 50 the distinction is never
worth worrying about.

### Q9. (Easy) `I_C = 1 mA`, `β = 100`. Compute `1/gm`, `re` and `rπ/β`.
**Answer:** All three ≈ 25 Ω.
**Method:** `1/gm = 1/0.04 = 25 Ω`; `re = 25 mV/1.005 mA = 24.75 Ω`;
`rπ/β = 2500/100 = 25 Ω`. This is a useful sanity check before any amplifier
calculation: at high β, "the transistor looks like a 25 Ω resistor" from base to
emitter, and the current gain is 100 on top of that.

### Q10. (Easy) Prove `gm·rπ = β`.
**Answer:** `gm·rπ = (I_C/V_T)(βV_T/I_C) = β`. At `I_C = 1 mA, β = 100`:
`0.04 × 2500 = 100` ✓.
**Method:** Multiply the two definitions and every `I_C` and `V_T` cancels. This
is your fastest consistency check: if `gm·rπ ≠ β`, one of the two numbers came
from a different operating point and you have made an error.

### Q11. (Moderate) Give the full parameter set at `I_C = 1 mA`, `β = 100`,
`V_A = 100 V`.
**Answer:** `gm = 40 mA/V`, `rπ = 2.5 kΩ`, `re ≈ 25 Ω`, `ro = 100 kΩ`.
**Method:** `gm = 1m/25m = 40 mS`; `rπ = 100/0.04 = 2.5 kΩ`;
`re = 25m/1.005m ≈ 25 Ω`; `ro = 100/1m = 100 kΩ`. Sanity-check the ordering by
magnitude: `ro` (100 kΩ) ≫ `rπ` (2.5 kΩ) ≫ `re` (25 Ω). That ordering is itself
the answer to "when can I ignore this element?"

### Q12. (Moderate) Same but `I_C = 2 mA`, `β = 200`, `V_A = 100 V`.
**Answer:** `gm = 80 mA/V`, `rπ = 2.5 kΩ`, `re ≈ 12.5 Ω`, `ro = 50 kΩ`.
**Method:** `gm = 2m/25m = 80 mS`; `rπ = 200/0.08 = 2500 Ω` (unchanged, because β
doubled along with `I_C`); `re = 25m/2.01m = 12.4 Ω`; `ro = 100/2m = 50 kΩ`.
Notice `rπ` is *insensitive* here — that is not a coincidence but a design
choice: designers raise β whenever they double `I_C` to keep input impedance
constant. Also note `ro` halved, so the Early effect gets relatively worse at
higher current.

### Q13. (Moderate) `I_C = 0.1 mA`, `β = 100`, `V_A = 50 V`. All four parameters.
**Answer:** `gm = 4 mA/V`, `rπ = 25 kΩ`, `re ≈ 250 Ω`, `ro = 500 kΩ`.
**Method:** `gm = 0.1m/25m = 4 mS`; `rπ = 100/0.004 = 25 kΩ`;
`re = 25m/0.1005m = 248.8 Ω`; `ro = 50/0.1m = 500 kΩ`. Everything scales the
right way: at low current the transistor is a *poor* amplifier (small `gm`) but a
*good* input impedance and a *good* output impedance. That trade-off is why
low-`I_C` stages are chosen for impedance, not gain.

### Q14. (Moderate) `I_C = 5 mA`, `β = 100`, `V_A = 50 V`. All four parameters.
**Answer:** `gm = 200 mA/V`, `rπ = 500 Ω`, `re ≈ 5 Ω`, `ro = 10 kΩ`.
**Method:** `gm = 5m/25m = 200 mS`; `rπ = 100/0.2 = 500 Ω`; `re = 25m/5.05m =
4.95 Ω`; `ro = 50/5m = 10 kΩ`. At 5 mA the transistor looks like a 5 Ω emitter
resistor — which is why a common-base stage at this current presents a ~5 Ω load
to its driver. `ro = 10 kΩ` is now comparable to a typical `R_C`, so **you can no
longer ignore `ro`** at high current.

### Q15. (Moderate) You are given `rπ = 4 kΩ` and `β = 200`. Recover `gm`, `I_C`
and `re`.
**Answer:** `gm = 50 mA/V`, `I_C = 1.25 mA`, `re ≈ 20 Ω`.
**Method:** `gm = β/rπ = 200/4000 = 0.05 S = 50 mA/V`. Then
`I_C = gm·V_T = 0.05 × 25 mV = 1.25 mA`. Then
`I_E = I_C(1+1/β) = 1.2563 mA`, `re = 25 mV/1.2563 mA = 19.9 Ω`. The move
`rπ → gm → I_C` is the standard escape route whenever a problem gives you `rπ`
instead of a current.

### Q16. (Moderate) You are given `re = 20 Ω` and `β = 100`. Recover `I_E`, `I_C`,
`gm` and `rπ`.
**Answer:** `I_E = 1.25 mA`, `I_C = 1.238 mA`, `gm = 49.5 mA/V`, `rπ = 2.02 kΩ`.
**Method:** `I_E = V_T/re = 25 mV/20 Ω = 1.25 mA`. `I_C = α·I_E = (100/101) ×
1.25 mA = 1.238 mA`. `gm = I_C/V_T = 1.238m/25m = 49.5 mS`. `rπ = β/gm =
100/0.0495 = 2.02 kΩ` (and `(β+1)re = 101 × 20 = 2.02 kΩ` ✓). If you round
`I_C ≈ I_E` first, you get the cleaner textbook pair `gm = 50 mA/V`,
`rπ = 2 kΩ` — both are acceptable, but say which you did.

### Q17. (Moderate) Prove `gm·re = α` and `1/re = I_E/V_T`.
**Answer:** `gm·re = (I_C/V_T)(V_T/I_E) = I_C/I_E = α` (= 0.995 at β=100);
`1/re = I_E/V_T` by definition.
**Method:** Multiply the definitions. The physical reading is beautiful: `gm·re`
is the ratio of collector to emitter current, so the product of the
transconductance and the emitter resistance *is* the current gain α. It also
gives a fast check on any pair of numbers you have computed.

### Q18. (Moderate) `I_C = 1 mA`. A 1 mV small-signal excursion on the
base-emitter junction produces what collector-current excursion?
**Answer:** `40 µA`.
**Method:** `i_c = gm·v_be = 40 mA/V × 1 mV = 40 µA`. This is the entire
physical content of "the BJT is a voltage-controlled current source *after*
linearisation". Note the units discipline: mA/V × mV = µA, not mA. Getting the
decimal wrong here is the classic cause of a 1000× error in gain.

### Q19. (Moderate) Describe the hybrid-π model: which element goes where?
**Answer:** `rπ` from base to emitter; a dependent current source `gm·v_be` from
collector to emitter (into the collector for an NPN); `ro` from collector to
emitter, in parallel with the source. The base is the only "port in", and the
model is unilateral (no feedback from output to input, ignoring `rµ`).
**Method:** Draw it from memory as a T turned sideways: the `rπ` bar spans
B→E, the `gm·v_be` arrow hangs off the collector leg pointing into the
collector, and `ro` closes the triangle. The recipe for every AC problem is
then mechanical: **replace the device with this, kill the supplies, short the
midband capacitors, and solve the linear circuit** (see `27-DC-and-AC-Analysis-Method.md`).

### Q20. (Moderate) Describe the T-model and the value of its current source.
**Answer:** `re` sits in the emitter leg; the collector current source equals
`α·I_E` (≈ `I_C`).
**Method:** The T-model routes the *emitter* current through `re` and taps off
`α·I_E` at the collector, so the source value is `I_C` by definition, not `gm·v_be`.
Use it when the emitter is the signal node (common-base, emitter follower) or when
the problem hands you `re`. The two models are the same transistor: convert with
`rπ = (β+1)re`, `gm = α/re`.

### Q21. (Moderate) `I_C = 1 mA` (`gm = 40 mA/V`), `R_C = 5 kΩ`, `R_L = 10 kΩ`,
`V_A = 100 V`. Compute `A_v` with and without `ro`.
**Answer:** Without `ro`: `R = 3.333 kΩ`, `A_v = −133.3`. With `ro`:
`R = 3.226 kΩ`, `A_v = −129.0` (3.2% smaller).
**Method:** `A_v = −gm(R_C ∥ R_L ∥ ro)`.
- No `ro`: `5k∥10k = 3.333 kΩ`; `A_v = −0.04 × 3333 = −133.3`.
- With `ro = 100 kΩ`: `1/R = 1/5000 + 1/10000 + 1/100000 = 0.00031` ⇒
  `R = 3226 Ω`; `A_v = −0.04 × 3226 = −129.0`.
The rule that emerges: include `ro` when `ro` is within about 10× of the
parallel combination. Here `100 k/3.33 k = 30`, so a 3% error — usually ignorable
in a 2-mark question, mandatory in a 5-mark one.

### Q22. (Moderate) `I_C = 1 mA`, `β = 100` (`re = 25 Ω`). The emitter resistor
is `R_E = 500 Ω`. With and without a bypass capacitor, find the resistance seen
looking into the **base**.
**Answer:** Bypassed: `rπ = 2.5 kΩ`. Unbypassed: `(β+1)(re + R_E) = 101 × 525 =
53.0 kΩ` — 21× larger.
**Method:** Bypassed, the emitter is at AC ground, so you look into `rπ`.
Unbypassed, the emitter current develops `i_e·(re + R_E)`, and base current is
`i_e/(β+1)`, so the input resistance is `(β+1)(re + R_E)`. The method to
remember: **unbypassed `R_E` appears multiplied by β+1 at the input.** Any
unbypassed emitter impedance is a β-multiplier. This is the single biggest
input-impedance lever in a CE stage.

### Q23. (Moderate) At fixed `I_C` and β, temperature doubles from 300 K to
600 K. What happens to `gm`, `re`, `rπ`, `ro`?
**Answer:** `V_T` doubles (25 → 50 mV), so `gm` **halves**, `re` **doubles**,
`rπ` **doubles**, and `ro` is **unchanged**.
**Method:** `gm = I_C/V_T` falls with `V_T`; `re = V_T/I_E` and
`rπ = βV_T/I_C` both rise with `V_T`; `ro = V_A/I_C` contains neither `V_T` nor
`T` explicitly. The corollary is a design lesson: **CE voltage gain
`−gm·R_C` shrinks with temperature** while a degenerated gain `−R_C/R_E` does
not — which is the argument for emitter degeneration in precision stages.

### Q24. (Moderate) A design needs `rπ = 1 kΩ` with `β = 50`. Find `I_C` and `gm`.
**Answer:** `gm = 50 mA/V`, `I_C = 1.25 mA`.
**Method:** `gm = β/rπ = 50/1000 = 0.05 S = 50 mA/V`; `I_C = gm·V_T = 0.05 ×
25 mV = 1.25 mA`. Equivalently `I_C = βV_T/rπ = 50 × 25 mV/1 kΩ = 1.25 mA`.
Design backwards from impedance is a normal GATE move — `rπ` is what the source
sees, so it is often the given quantity.

### Q25. (GATE-level) A CE stage has `I_C = 1 mA` (so `gm = 40 mA/V`, `rπ = 2.5 kΩ`
at β=100), `R_C = 4 kΩ`, `R_L = 4 kΩ`, `R_E = 1 kΩ` **fully bypassed**, `V_A = 100 V`.
Redraw the AC equivalent in hybrid-π and find `A_v` including `ro`.
**Answer:** `R_ac = 4k ∥ 4k ∥ 100k = 1.961 kΩ`, so `A_v = −gm·R_ac = −78.4`.
**Method:** Recipe, in order.
1. Midband: **short** `C_E` (so `R_E` disappears from the AC circuit) and short
   `V_CC` to ground.
2. Replace the transistor by hybrid-π: `rπ` from base to emitter (emitter now at
   AC ground), `gm·v_be` from collector to emitter, `ro` across the source.
3. The collector sees three resistors in parallel: `R_C`, `R_L`, `ro`.
   `1/1.961 kΩ = 1/4000 + 1/4000 + 1/100000`.
4. `A_v = −gm·R_ac = −0.04 × 1961 = −78.4`.
The minus sign is the phase inversion of the CE stage and it is not optional.
Compare with the `ro`-neglected answer `−80`: only 2% different.

### Q26. (GATE-level) Same stage but the bypass capacitor is **removed**. Give
`A_v` and the total input resistance (with `R1 = 100 kΩ`, `R2 = 25 kΩ` from
Q21's bias divider, i.e. `R_B = 20 kΩ`).
**Answer:** `A_v = −gm·R_C/(1 + gm·R_E) = −160/41 = −3.90`; `R_in(base) =
(β+1)(re+R_E) = 103.5 kΩ`; total `R_in = 20k ∥ 103.5k = 16.76 kΩ`.
**Method:**
- `R_in(base) = (β+1)(re + R_E) = 101 × (25 + 1000) = 103 525 Ω = 103.5 kΩ`.
- `R_B = 100k ∥ 25k = 20 kΩ`; `R_in = 20k × 103.5k/123.5k = 16.76 kΩ`.
- Gain: `A_v = −gm·R_C/(1 + gm·R_E) = −0.04 × 4000/(1 + 0.04 × 1000) =
−160/41 = −3.90`. Or `−R_C/(R_E + 1/gm) = −4000/(1000+25) = −3.90`.
The two effects: gain collapses by a factor of 20.5 (from −78.4), and input
impedance rises by 7.5× (from 2.22 kΩ). The gain is now set by *resistors*, so it
barely moves with β or temperature — that is the point of degeneration.

### Q27. (GATE-level) `I_C = 1 mA`, `V_A = 100 V`, `R_C = 4.7 kΩ`, no load.
Compare `A_v` with and without `ro`, and state when you may drop `ro`.
**Answer:** Without: `−188`. With: `R = 4.489 kΩ`, `A_v = −179.6`. `ro` costs
4.5% of the gain; you may ignore it when `ro ≥ 10(R_C ∥ R_L)`, i.e. here
`100 k/4.7 k = 21` (borderline-acceptable).
**Method:** `4.7k ∥ 100k = (4.7 × 100)/104.7 = 4.489 kΩ`.
`A_v(no ro) = −0.04 × 4700 = −188`; `A_v(with ro) = −0.04 × 4489 = −179.6`.
Ratio `4489/4700 = 0.955`. The decision rule: `ro` enters in *parallel* with
`R_C ∥ R_L`, so the error is `[1 − (R_C∥R_L)/((R_C∥R_L) + ro)]`. Read "ignore
`ro`" as "the answer is a 2-mark number" and "include `ro`" as "show the
Early-effect reasoning".

### Q28. (GATE-level) A circuit has `I_C = 1 mA`, `β = 100`. State the input
resistance looking into (a) the base with the emitter at AC ground, (b) the
emitter with the base at AC ground.
**Answer:** (a) `2.5 kΩ`; (b) `25 Ω` (≈ `re`).
**Method:** (a) `rπ = β/gm = 100/0.04 = 2.5 kΩ`. (b) with the base at AC
ground, all emitter current must flow through `re`, so you see `re = 25 Ω`
(T-model made trivial). The 100× ratio `rπ/re ≈ β` is the reason a CB stage
loads its driver 100× more heavily than a CE stage. If a GATE question gives you
a measured input resistance and asks which configuration it is, **25 Ω ⇒ CB,
2.5 kΩ ⇒ CE, 50 kΩ and up ⇒ CC**.

### Q29. (GATE-level) `I_C = 1.5 mA`, `β = 150`, `V_A = 90 V`. Find all four
parameters two independent ways.
**Answer:** `gm = 60 mA/V`; `rπ = 2.5 kΩ`; `re = 16.6 Ω`; `ro = 60 kΩ`.
**Method:** Route 1 (from `I_C`): `gm = 1.5m/25m = 60 mS`; `rπ = 150/0.06 =
2500 Ω`; `I_E = 1.51 mA`, `re = 25m/1.51m = 16.56 Ω`; `ro = 90/1.5m = 60 kΩ`.
Route 2 (check the identities): `(β+1)re = 151 × 16.56 = 2500 Ω = rπ` ✓;
`gm·rπ = 0.06 × 2500 = 150 = β` ✓; `gm·re = 0.06 × 16.56 = 0.995 = α` ✓.
Doing both routes takes 20 seconds and catches every arithmetic slip.

### Q30. (GATE-level) Show that `1/gm`, `re` and `rπ/β` are all within 1% at
`I_C = 1 mA`, `β = 100`, and say which one to use in a hand calculation.
**Answer:** `1/gm = 25.00 Ω`, `re = 24.75 Ω`, `rπ/β = 25.00 Ω` — all within 1%.
Use `1/gm` (or `re`) whenever the formula shows `1/gm`, e.g. the degenerated
gain `−R_C/(R_E + 1/gm)`.
**Method:** Compute all three from their definitions (Q9). The near-equality
follows from `I_E ≈ I_C`, which is valid whenever `1/β ≪ 1`. Practical rule: in
gain formulas written as `R_C/(R_E + 1/gm)`, use `1/gm = 25 mV/I_C`; in
impedance formulas written with `re`, use `V_T/I_E`. Same physics, different
habit, and mixing them up is how students lose 20 dB in a cascade calculation.

### Q31. (GATE-level) A CE stage has `I_C = 1 mA`, `R_C = 4 kΩ`, `R_E = 1 kΩ`
unbypassed (no load attached). Show that the gain is set by resistors, and find
its value and the ratio to the bypassed gain.
**Answer:** `A_v = −gm·R_C/(1 + gm·R_E) = −160/41 = −3.90 ≈ −R_C/R_E = −4`.
Bypassed gain (no load) is `−160`, so the ratio is exactly `1 + gm·R_E = 41`.
**Method:** Substitute `gm·R_E = 0.04 × 1000 = 40 ≫ 1`, so
`1 + gm·R_E ≈ gm·R_E` and `A_v ≈ −R_C/R_E = −4`. That approximation is *exactly*
the statement that the stage is resistor-determined. The ratio is worth noticing:
it is **independent of the load**, because `A_v ∝ R_C∥R_L` in both the bypassed and
unbypassed cases, so

  `(−gm(R_C∥R_L)) / (−gm(R_C∥R_L)/(1 + gm R_E)) = 1 + gm R_E = 41`.

With `R_L = 4 kΩ` the two gains become `−80` and `−1.95` — still a factor of 41.
Two consequences to say out loud in an exam: (i) the gain no longer depends on β,
`I_C` or temperature, so `ΔA_v/A_v` is a few percent instead of a factor of two;
(ii) linearity improves because the exponential `V_BE` variation is divided by
`1 + gm·R_E = 41`.

### Q32. (GATE-level) A CE amplifier must drive `R_L = 4 kΩ` and must have
`|A_v| ≥ 150`. `I_C` may be chosen; `R_C = 4 kΩ`, `V_A = 100 V`. Is it possible,
and what is the gain with and without `ro`?
**Answer:** `R_C ∥ R_L = 2 kΩ`, `ro = 100 kΩ`. Without `ro`: `A_v = −gm × 2 kΩ`,
so `|A_v| ≥ 150` needs `gm ≥ 75 mA/V`, i.e. `I_C ≥ 1.875 mA`. With `ro`:
`2k ∥ 100k = 1.961 kΩ`, needing `gm ≥ 76.5 mA/V` ⇒ `I_C ≥ 1.91 mA`. Yes, both
are possible.
**Method:** Invert the gain requirement instead of guessing a current.
`gm = |A_v|/R_ac = 150/2000 = 75 mA/V`; `I_C = gm·V_T = 0.075 × 25 mV = 1.875 mA`.
Including `ro` needs `gm = 150/1961 = 76.5 mA/V`, `I_C = 1.91 mA`. This is the
standard GATE trick: **requirements are given in `A_v`, but `A_v` lives in `gm`,
and `gm` lives in `I_C`** — so convert twice and back-solve the current.

### Q33. (GATE-level) Two transistors sit at the same `I_C = 1 mA` but have
`β = 50` and `β = 200`. Which of `gm`, `rπ`, `re`, `ro` differ, and by how much?
**Answer:** Only `rπ`: 1.25 kΩ vs 5 kΩ (4×). `gm = 40 mA/V`, `re = 25 Ω`,
`ro = 100 kΩ` are all identical.
**Method:** `rπ = β/gm` is the *only* parameter that contains β. Everything else
is set by `I_C` (and `V_A`). This is the cleanest statement of what β actually
controls in a circuit, and it explains the whole motivation for emitter
degeneration: the unbypassed `R_E` is a β-multiplier at the input and a
resistor-set gain at the output, so it converts the one β-dependent quantity
into a β-independent one.

### Q34. (GATE-level) A design wants `gm = 20 mA/V` with `β = 100`. Give the
whole operating point (all four parameters) and the CE gain into
`R_C = R_L = 5 kΩ` with `R_E` bypassed.
**Answer:** `I_C = 0.5 mA`, `gm = 20 mA/V`, `rπ = 5 kΩ`, `re = 50 Ω`,
`ro = V_A/0.5m` (= 200 kΩ at `V_A = 100 V`); `A_v = −gm·(5k ∥ 5k) = −50`.
**Method:** Work down the chain: `I_C = gm·V_T = 0.02 × 25 mV = 0.5 mA`;
`rπ = 100/0.02 = 5 kΩ`; `re = 25 mV/0.505 mA = 49.5 Ω`; `ro = 100/0.5m = 200 kΩ`.
Gain: `5k ∥ 5k = 2.5 kΩ`, `A_v = −0.02 × 2500 = −50`. Notice how modest the gain
is at only 0.5 mA — the whole point of the chapter is that voltage gain in a CE
stage is bought with *current*, one 25 mV per 40 mA/V.

---

## Trap box (exam-day killers)

- `re = V_T/I_E` (emitter current), `rπ = β·V_T/I_C` (base side). Mixing them
  gives a 1.25× error that will not cancel.
- `gm = 40·I_C[mA]` mA/V. Unit slip (mA/V vs A/V) is worth a factor of 1000.
- `rπ = (β+1)·re`, not `β·re` exactly — but the difference is 1% at β=100, so do
  not agonise.
- `ro = V_A/I_C`, and it must appear in **parallel** with `R_C ∥ R_L`.
- Unbypassed `R_E` gives `R_in = (β+1)(re + R_E)` and
  `A_v = −gm·R_C/(1 + gm·R_E)`. Bypassed gives `R_in = rπ` and `A_v = −gm·R_C`.
  Always ask: **is there a bypass cap across `R_E`?**
- `rπ` and `re` never go in the same circuit; nor `β·re` and `gm·v_be` for the
  same source.
- Verify with `gm·rπ = β` before you start any gain calculation.
- Bypassing is an **AC** statement. For DC, `R_E` is always in the circuit.

## Final recall drill (do in 60 seconds)

1. `I_C = 2 mA` ⇒ `gm`? → *80 mA/V.*
2. `I_C = 1 mA`, `β = 100` ⇒ `rπ`? → *2.5 kΩ.*
3. `V_T = 25 mV`, `I_E = 2 mA` ⇒ `re`? → *12.5 Ω.*
4. `V_A = 75 V`, `I_C = 0.5 mA` ⇒ `ro`? → *150 kΩ.*
5. `re = 12.5 Ω`, `β = 100` ⇒ `rπ`? → *1.26 kΩ ≈ 1.25 kΩ.*
6. `gm·rπ` = ? → *β.*
7. `gm·re` = ? → *α.*
8. `I_C = 1 mA` ⇒ `1/gm`? → *25 Ω.*
9. Unbypassed `R_E = 1 kΩ`, `β = 100`, `re = 25 Ω` ⇒ `R_in(base)`? →
   *`101 × 1025 = 103.5 kΩ`.*
10. Which model holds `re`? → *T-model (emitter side).*

---

Theory behind every answer: `08-BJT-Small-Signal-Models.md`,
`29-Formula-Sheet.md` §29.3, `32-Single-File-Cheatsheet.md` §4.
