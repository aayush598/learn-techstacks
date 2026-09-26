# BJT Amplifiers: CE, CB, CC — Practice (Learn by Solving)

> **The idea in one line:** this file teaches the three BJT configurations through
> 34 questions only — that each one picks a different AC ground, that gives it a
> recognisable gain sign, input impedance and output impedance, and that
> multistage gain is the product of *loaded* gains, not the product of the
> textbook ones.
>
> **How to use:** solve each question fully before reading the answer. Cover the
> **Answer**/**Method** with paper, do it, then reveal. If you miss one, solve the
> next 3 in the file to lock the pattern. No need to read the chapter notes
> first — every concept is taught through the drill itself. Open
> `09-BJT-Amplifiers.md` or `32-Single-File-Cheatsheet.md` only when you want the
> underlying theory.

## Concept box (what you must internalise)

- Recognition rule: find the terminal tied to AC ground. Emitter grounded → **CE**;
  base grounded → **CB**; collector grounded → **CC**.
- CE: `A_v = −gm(R_C∥R_L)`, `R_in = R1∥R2∥rπ`, `R_out = R_C` — inverting.
- CE with unbypassed `R_E`: `A_v = −gm·R_C/(1 + gm·R_E) ≈ −R_C/R_E`,
  `R_in = R1∥R2∥(β+1)(re+R_E)`, `R_out = R_C`.
- CB: `A_v = +gm(R_C∥R_L)`, `R_in ≈ re`, `R_out = R_C` — non-inverting, low `R_in`.
- CC: `A_v = (R_E∥R_L)/(re + R_E∥R_L) < 1`, `R_in = R_B∥(β+1)(re+R_E∥R_L)`,
  `R_out ≈ re + R_s/(β+1)` — unity buffer.
- Source loading: `A_vs = A_v · R_in/(R_in + R_s)`. Stage loading: replace `R_L`
  with the next stage's `R_in`.
- Cascade: `A_tot = Π(loaded A_v)`; in dB, add.
- Trap: `R_L` is always in the gain formula. Using bare `R_C` is the most common
  error in the chapter.

**Reference circuit used throughout (call it the BASE STAGE):**
`I_C = 1 mA ⇒ gm = 40 mA/V, re = 25 Ω`; `β = 100 ⇒ rπ = 2.5 kΩ`;
`R_C = 4 kΩ`, `R_L = 4 kΩ`, `R1 = 100 kΩ`, `R2 = 25 kΩ ⇒ R_B = 20 kΩ`.

---

## Questions

### Q1. (Easy) In each schematic, which terminal is AC-grounded, and hence which
configuration is it? (a) signal into the base, output from the collector,
emitter through `R_E` to ground with a bypass cap. (b) signal into the emitter,
output from the collector, base through a capacitor to ground. (c) signal into the
base, output from the emitter, collector straight to `V_CC`.
**Answer:** (a) **CE** (emitter is the AC common). (b) **CB** (base is the
common). (c) **CC** (collector is the common — `V_CC` is an AC ground).
**Method:** A supply is an AC ground (it is a big capacitor to real ground), so a
terminal wired straight to `V_CC` is AC-grounded too. (c) is the only one where
the output is taken from the emitter. Never name a configuration from the
*schematic shape*; name it from the grounded terminal.

### Q2. (Easy) BASE STAGE, `R_E` bypassed. Find `A_v`.
**Answer:** `A_v = −80`.
**Method:** `A_v = −gm(R_C∥R_L)`. `R_C∥R_L = 4k∥4k = 2 kΩ`.
`A_v = −0.04 S × 2000 Ω = −80`. The minus sign is the CE phase inversion —
output falls when input rises. Unit check: `mA/V × kΩ = V/V`, so `40 mA/V ×
2 kΩ = 80` (a dimensionless number, as a gain must be).

### Q3. (Easy) BASE STAGE. Find `R_in`.
**Answer:** `R_in = 2.22 kΩ`.
**Method:** `R_in = R1∥R2∥rπ`. `R1∥R2 = 100k∥25k = 20 kΩ`;
`20k∥2.5k = 50000/22.5 = 2.22 kΩ`. Because `rπ` is so much smaller than the bias
network, `R_in ≈ rπ` — the divider barely loads. The method: parallel-ise the
three in one line rather than one at a time.

### Q4. (Easy) BASE STAGE. Find `R_out`.
**Answer:** `R_out = 4 kΩ`.
**Method:** `R_out = R_C`. With the input set to zero, `v_be = 0`, so the
controlled source `gm·v_be` delivers no current and `ro` is irrelevant (nothing
is driving the collector node except `R_C`). Students add `ro` here; the correct
answer is exactly `R_C` unless the problem says otherwise.

### Q5. (Easy) BASE STAGE reconfigured as common-base. Find `A_v` and its sign.
**Answer:** `A_v = +80`.
**Method:** `A_v = +gm(R_C∥R_L) = +0.04 × 2000 = +80`. Same magnitude as CE, but
**positive**. Track the sign with `v_be`, not with current: in an NPN,
`v_be = v_b − v_e`, and the base is at AC ground here, so `v_be = −v_e`. Raise the
emitter ⇒ `v_be` *falls* ⇒ `i_c` falls ⇒ the drop across `R_C` shrinks ⇒ `v_c`
*rises*. Output up for input up, hence `+80` instead of CE's `−80`. That
non-inverting sign is what lets CB sit at the input of a CE cascade and still
leave the cascade inverting.

### Q6. (Easy) BASE STAGE as common-base. Find `R_in`.
**Answer:** `R_in ≈ re = 25 Ω`.
**Method:** With the base at AC ground, every emitter current flows through
`re`, so the input resistance is `re = V_T/I_E = 25 mV/1.005 mA = 25 Ω`. Compare
with the CE stage's 2.22 kΩ: **the CB input is 89× lower.** That is the price of
CB's lack of Miller effect and high-frequency capability, and it is why CB is
never used as the first stage of an amplifier.

### Q7. (Easy) Emitter follower with `R_E = 1 kΩ`, `R_L = 1 kΩ`, `re = 25 Ω`.
Find `A_v`.
**Answer:** `A_v = 500/525 = 0.952`.
**Method:** `R_E∥R_L = 500 Ω`; `A_v = 500/(re + 500) = 500/525 = 0.952`. The
follower is a *voltage divider* on `R_E∥R_L` and `re` — that is the whole model.
It is always **less than 1**, never exactly 1, and the shortfall
(`re/(re + R_E∥R_L)`) is set by how much current you are willing to spend.

### Q8. (Easy) Same emitter follower. Find the resistance looking into the base.
**Answer:** `(β+1)(re + R_E∥R_L) = 101 × 525 = 53.0 kΩ`.
**Method:** `R_in(base) = (β+1)(re + R_E∥R_L)`. The `β+1` appears because base
current is `1/(β+1)` of the emitter current that flows through the total emitter
impedance. This is the largest `R_in` of the three configurations and the reason
the follower is the standard impedance-matching stage.

### Q9. (Easy) Same emitter follower, driven from an ideal source (`R_s = 0`).
Find `R_out`.
**Answer:** `R_out = re = 25 Ω`.
**Method:** `R_out ≈ re + R_s/(β+1) = 25 + 0 = 25 Ω`. The intuition: the emitter
node behaves like a voltage source that follows the base, so what you see looking
back into the emitter is just `re`. Compare with the CE stage's 4 kΩ: **160×
lower output impedance.** Small `R_out` plus huge `R_in` is the follower's whole
personality.

### Q10. (Easy) Match each signature to a configuration: (a) `A_v = −80`,
`R_in = 2.5 kΩ`; (b) `A_v = +80`, `R_in = 25 Ω`; (c) `A_v = 0.95`,
`R_in = 50 kΩ`, `R_out = 30 Ω`.
**Answer:** (a) **CE**, (b) **CB**, (c) **CC**.
**Method:** Three questions in order: *is the gain negative?* → CE. *Is the gain
positive and `R_in` of order `re` (tens of ohms)?* → CB. *Is the gain slightly
less than 1 with a huge `R_in` and a tiny `R_out`?* → CC. Fix these three
signatures permanently — most identification questions are one line.

### Q11. (Moderate) BASE STAGE driven through a source resistance `R_s = 1 kΩ`.
Find the gain from `v_s` (not from `v_in`).
**Answer:** `A_vs = −55.2`.
**Method:** Two steps.
1. The source divider: `v_in/v_s = R_in/(R_in + R_s) = 2222/(2222 + 1000) =
0.6897`.
2. `A_vs = A_v × 0.6897 = −80 × 0.6897 = −55.2`.
The general law to memorise: **`A_vs = A_v·R_in/(R_in + R_s)`**. If the gain you
were given is `v_out/v_in`, you are done; if it is `v_out/v_s`, you must apply the
divider. Exam questions are deliberately ambiguous here, so quote which one you
computed.

### Q12. (Moderate) BASE STAGE with the bypass capacitor **removed**
(`R_E = 1 kΩ` unbypassed). Find `A_v` and the total `R_in`.
**Answer:** `A_v = −gm·R_C/(1 + gm·R_E) = −160/41 = −3.90`; `R_in(base) = 103.5 kΩ`;
total `R_in = 20k ∥ 103.5k = 16.76 kΩ`.
**Method:**
- `R_in(base) = (β+1)(re + R_E) = 101 × 1025 = 103 525 Ω`.
- `R_in = 20k × 103.5k/123.5k = 16.76 kΩ` (7.5× the bypassed 2.22 kΩ).
- `A_v = −gm·R_C/(1 + gm·R_E) = −0.04 × 4000/(1 + 40) = −160/41 = −3.90`, or
  `−R_C/(R_E + 1/gm) = −4000/1025 = −3.90`.
Trade: gain down by 20.5×, input impedance up 7.5×, and the gain is now set by
resistors so it is insensitive to β and temperature.

### Q13. (Moderate) A common-base stage has `R_E = 100 Ω` connecting the emitter to
the source, `re = 25 Ω`. Find the input resistance.
**Answer:** `re∥R_E = 25∥100 = 20 Ω`.
**Method:** `R_in = re ∥ R_E` (the emitter's `re` is in parallel with whatever the
emitter sees to ground). `25 × 100/125 = 20 Ω`. The point: the *driver's* source
resistance becomes part of the amplifier's input resistance, so a CB stage can
drag a signal source down hard. That is why CB is used inside a cascode, not at a
connector.

### Q14. (Moderate) Emitter follower (`R_E = 1 kΩ`, `R_L = 1 kΩ`, `re = 25 Ω`) driven
through `R_s = 10 kΩ` and a `100 kΩ` bias resistor. Find `R_out`.
**Answer:** `R_out ≈ re + (R_s∥R_B)/(β+1) = 25 + 9.09k/101 = 115 Ω`.
(If the bias path is neglected: `25 + 10k/101 = 124 Ω`.)
**Method:** `R_s ∥ R_B = 10k ∥ 100k = 9.09 kΩ`, then divide by `β+1` and add
`re`: `9.09k/101 = 90 Ω`, so `R_out = 115 Ω`. Every resistance from the base
divides by `β+1` before it appears at the emitter — the mirror image of the
input-impedance rule. The ideal-source case (no `R_B`, `R_s` directly on the base)
gives `25 + 10000/101 = 124 Ω`, so `R_out` grew ~5× over Q9 simply because the
source is no longer ideal. State which assumption you used.

### Q15. (Moderate) The Q7 follower also has a `100 kΩ` bias resistor from base to
`V_CC`. Find the total `R_in`.
**Answer:** `R_in = 100k ∥ 53.0k = 34.7 kΩ`.
**Method:** `R_in = R_B ∥ R_in(base) = 100k × 53k/153k = 34.65 kΩ`. Remember: the
bias network always loads the input of *every* configuration, follower included.
The follower's `R_in` is huge but never infinite, and on a PCB the bias divider is
usually the smaller of the two.

### Q16. (Moderate) Emitter follower with `R_E = 2 kΩ`, `R_L = 10 kΩ`, `re = 25 Ω`.
Find `A_v` and the input resistance into the base.
**Answer:** `R_E∥R_L = 1.667 kΩ`; `A_v = 1667/1692 = 0.985`;
`R_in(base) = 101 × 1692 = 170.9 kΩ`.
**Method:** `2k∥10k = 20/12 = 1.667 kΩ`. `A_v = 1667/(25 + 1667) = 0.985`.
`R_in(base) = (β+1)(re + R_E∥R_L) = 101 × 1692 = 170.9 kΩ`. Message: a lightly
loaded follower is very close to unity gain, and its input impedance scales with
its load — halve `R_L` and `A_v` drops noticeably.

### Q17. (Moderate) Convert these gains to dB: (a) `|A_v| = 80`; (b) two identical
CE stages each of `A_v = −50`.
**Answer:** (a) 38.1 dB. (b) `|A_tot| = 2500` ⇒ 68.0 dB.
**Method:** `20·log10(80) = 20 × 1.903 = 38.06 dB`.
`A_tot = (−50)(−50) = +2500`, `20·log10(2500) = 20 × 3.398 = 67.96 dB`.
**Signs in dB:** two inversions make a *non-inverting* overall amplifier — the
`+2500` is not a typo, and phase is a real exam item.

### Q18. (Moderate) BASE STAGE. Find the current gain `A_i = i_L/i_in`.
**Answer:** `A_i = −50`.
**Method:** `i_L = v_out/R_L` and `i_in = v_in/rπ`, so
`A_i = A_v·rπ/R_L = −80 × 2500/4000 = −50`. Do not answer "β = 100": β is the
current gain of the *device*, and the amplifier's current gain is β multiplied by
the fraction of collector current that reaches the load, `R_C/(R_C+R_L) = 0.5`.
So `A_i = −β × 0.5 = −50` — a quicker route to the same number.

### Q19. (Moderate) What are the current gains of the CB and CC stages?
**Answer:** CB: `A_i = α = I_C/I_E = 0.990` (essentially 1). CC: `A_i = (β+1) = 101`
(40.1 dB).
**Method:** CB divides emitter current into `I_C = α·I_E`, so the current gain is
`α` by definition. CC passes the *whole* emitter current to the load and draws
only `1/(β+1)` of it at the base, so `A_i = β+1`. Put the three together: CE gives
current gain ≈ β (and power gain), CB gives none, CC gives β+1 but voltage gain
of 1 — the follower trades voltage gain for current gain to move *power* and
*impedance*, not for gain.

### Q20. (Moderate) A CE stage at `I_C = 2 mA` (`gm = 80 mA/V`) with
`R_C = 3 kΩ`, `R_L = 3 kΩ`, `R_E` bypassed. Find `A_v`.
**Answer:** `A_v = −120`.
**Method:** `R_C∥R_L = 1.5 kΩ`; `A_v = −0.08 × 1500 = −120`. Doubling the current
doubles `gm` and hence doubles the gain. This is the direct lever on CE gain —
but it also doubles the base current, the power dissipation and shrinks `ro`.

### Q21. (Moderate) Two identical CE stages (BASE STAGE each) in cascade, output
loaded by `R_L = 4 kΩ` only on the last stage. Find the first stage's *loaded*
gain and the total.
**Answer:** `R_C1 ∥ R_in2 = 4k ∥ 2.222k = 1.429 kΩ`; `A_v1 = −57.1`;
`A_v2 = −80`; `A_tot = +4571` (73.2 dB).
**Method:** Replace `R_L` in stage 1's formula with the next stage's input
resistance — that *is* loading. `4k ∥ 2.222k = 1.429 kΩ`,
`A_v1 = −0.04 × 1429 = −57.14`. `A_v2 = −gm(4k∥4k) = −80`.
`A_tot = (−57.14)(−80) = +4571`, `20·log10(4571) = 73.2 dB`.
Compare with the naive `80 × 80 = 6400` — the loaded answer is 28% smaller.
**Multiply loaded gains only** (`09-BJT-Amplifiers.md` §9.5).

### Q22. (Moderate) A CE stage (BASE STAGE, bypassed) drives an emitter follower
(`R_E = R_L = 1 kΩ`) whose base is biased by `100 kΩ`. Find the total gain.
**Answer:** `R_in2 = 34.7 kΩ`; `R_C ∥ R_in2 = 3.586 kΩ`; `A_v1 = −143.4`;
`A_v2 = 0.952`; `A_tot = −136.6`.
**Method:** `R_in2 = 100k ∥ (101 × 525) = 34.65 kΩ`.
`R_C ∥ R_in2 = 4k × 34.65k/38.65k = 3.586 kΩ`;
`A_v1 = −0.04 × 3586 = −143.4`. `A_v2 = 0.952`.
`A_tot = −143.4 × 0.952 = −136.6`.
The lesson: adding a buffer **increased** the overall gain (from −80 to −136.6)
because the follower's 34.7 kΩ barely loads the 4 kΩ collector, while its own
gain cost is only 5%. This is the standard "CE → CC" output-stage pairing.

### Q23. (Moderate) A common-base stage (`I_C = 1 mA`, `R_C = 4 kΩ`,
`R_L = 4 kΩ`, base at AC ground) is fed by a common-emitter stage (BASE STAGE,
bypassed, no external load). Find the total gain.
**Answer:** `R_C1 ∥ R_in2 = 4k ∥ 25 = 24.84 Ω`; `A_v1 = −0.994`;
`A_tot = −0.994 × 80 = −79.5`.
**Method:** `R_in(CB) = re = 25 Ω`. `4k ∥ 25 = 24.84 Ω`, so
`A_v1 = −0.04 × 24.84 = −0.994` — the CE stage is effectively destroyed by the
25 Ω CB input. `A_v2 = +gm(4k∥4k) = +80`, giving `A_tot = −79.5`. The CB stage
contributes a factor of 80 but the preceding stage collapses by 80×. **A CB stage
must be driven from a current source, not from a voltage-amplifier output.**
Compare with Q22, where the same "add a second stage" idea *helped*.

### Q24. (Moderate) Compare the input impedances of the three configurations at
`I_C = 1 mA`, `β = 100`. Rank them and say which loads a signal source hardest.
**Answer:** CB 25 Ω < CE 2.5 kΩ < CC 53 kΩ. CB loads hardest, by 100× relative to
CE.
**Method:** `R_in(CB) = re = 25 Ω`; `R_in(CE) = rπ = β·re = 2.5 kΩ`;
`R_in(CC) = (β+1)(re + R_E∥R_L) = 53 kΩ`. The ratio `rπ/re = β` is the whole
reason CB is avoided at a signal input. Practical rule: if a datasheet asks for a
"high input impedance" front end, use CC or a FET; if it asks for wide bandwidth,
use CB or a cascode (Chapter 16).

### Q25. (GATE-level) Full midband analysis of the BASE STAGE with `R_E` bypassed,
including the effect of a 1 kΩ source. Report `A_v`, `A_vs`, `R_in`, `R_out`.
**Answer:** `A_v = −80`, `A_vs = −55.2`, `R_in = 2.22 kΩ`, `R_out = 4 kΩ`.
**Method:** The four-step recipe, once: (1) DC → `I_C = 1 mA` gives `gm`, `rπ`,
`re`; (2) kill DC — **short** `C_E` and `C_C1`, **ground** `V_CC`;
(3) hybrid-π; (4) solve.
- `A_v = −gm(R_C∥R_L) = −0.04 × 2000 = −80`.
- `A_vs = A_v·R_in/(R_in + R_s) = −80 × 2222/3222 = −55.2`.
- `R_in = 20k ∥ 2.5k = 2.22 kΩ`.
- `R_out = R_C = 4 kΩ`.
If a question says "gain from the source", it wants `A_vs`; if it says "gain from
the base", `A_v`. Report both and you cannot be marked wrong.

### Q26. (GATE-level) The BASE STAGE with the bypass capacitor **disconnected**.
Give `A_v`, `R_in`, `R_out`, and say what improves and what worsens.
**Answer:** `A_v = −3.90`, `R_in = 16.76 kΩ`, `R_out = 4 kΩ`. Gain down 20.5×;
input impedance up 7.5×; linearity and gain stability improve; `R_out` unchanged.
**Method:** Formulas and numbers as in Q12. What improves and why:
- *Linearity*: the output current is `v_be/(re + R_E)` instead of `gm·v_be`, so
  the exponential `V_BE` nonlinearity is divided by `1 + gm·R_E = 41`.
- *Stability*: `A_v ≈ −R_C/R_E` contains no β, no `I_C`, no temperature.
- *Input impedance*: `(β+1)(re + R_E)`.
What worsens: gain by 20.5×, and bias headroom (`V_E = I_E·R_E` still costs the
same). `R_out` is untouched because it is set by `R_C` alone. A 5-mark question
will ask you to *name* these three improvements — they are the reason `R_E` is in
professional designs even when the gain looks "wasted".

### Q27. (GATE-level) Full analysis of an emitter follower: `R_E = 1 kΩ`,
`R_L = 1 kΩ`, `R_B = 100 kΩ`, `R_s = 10 kΩ`, `re = 25 Ω`, `β = 100`. Report
`A_v`, `A_vs`, `R_in`, `R_out`.
**Answer:** `A_v = 0.952`; `R_in = 34.65 kΩ`; `A_vs = 0.952 × 34.65/44.65 =
0.739`; `R_out ≈ 25 + 10k/101 = 124 Ω` (or `115 Ω` including the bias path).
**Method:**
- `A_v = 500/(25 + 500) = 0.952`.
- `R_in = 100k ∥ 53.03k = 34.65 kΩ`.
- `A_vs = A_v·R_in/(R_in + R_s) = 0.952 × 34651/44651 = 0.739`.
- `R_out = re + R_s/(β+1) = 25 + 99 = 124 Ω`.
Note the source loading: a 10 kΩ source costs 22% of the voltage gain, because
the follower's input impedance is "only" 34.7 kΩ. If you want unity gain into a
low-impedance source, the follower needs a *larger* `R_E` and a smaller `R_L`.

### Q28. (GATE-level) Full analysis of a common-base stage: `I_C = 1 mA`,
`R_C = 4 kΩ`, `R_L = 4 kΩ`, `R_E = 100 Ω` at the emitter, `re = 25 Ω`, `R_s = 1 Ω`
(negligible). Report `A_v`, `R_in`, `R_out`, and the sign.
**Answer:** `A_v = +80`, `R_in = re ∥ 100 = 20 Ω`, `R_out = 4 kΩ`, non-inverting.
**Method:** `A_v = +gm(R_C∥R_L) = +0.04 × 2000 = +80`.
`R_in = 25 ∥ 100 = 20 Ω`. `R_out = R_C = 4 kΩ` (same argument as CE: kill the
input and the controlled source contributes nothing).
Compare with the CE stage: identical gain magnitude, identical `R_out`, opposite
sign, and 111× lower input impedance (`2.22 kΩ` vs 20 Ω). That single sentence is
the entire comparison table of Chapter 09.

### Q29. (GATE-level) A CB stage is followed by a CE stage instead. BASE STAGE for
both, CB first. Find each stage's loaded gain and the total.
**Answer:** Stage 1 (CB, output at collector into the CE's base):
`R_C ∥ R_in2 = 4k ∥ 2.22k = 1.429 kΩ`, `A_v1 = +57.1`. Stage 2 (CE):
`A_v2 = −80`. Total `= −4571`, non-inverting overall.
**Method:** `R_in(CE) = 2.222 kΩ`; `4k ∥ 2.222k = 1.429 kΩ`;
`A_v1 = +gm × 1429 = +57.1`. `A_v2 = −gm(4k∥4k) = −80`.
`A_tot = +57.1 × (−80) = −4571`, `20·log10(4571) = 73.2 dB`.
Order matters: the order that maximises total gain is **high-`R_in` stage first**,
which is exactly why the standard chain is CE → CC. Also note the sign: a CB
first stage *cancels* the CE inversion, so the cascade is non-inverting.

### Q30. (GATE-level) Three measured amplifiers: (a) `A_v = −75`, `R_in = 2.5 kΩ`,
`R_out = 5 kΩ`; (b) `A_v = +0.99`, `R_in = 60 kΩ`, `R_out = 30 Ω`; (c) `A_v = +60`,
`R_in = 22 Ω`, `R_out = 5 kΩ`. Identify each and give the current gain in each.
**Answer:** (a) CE, `A_i ≈ −β`; (b) CC, `A_i ≈ β+1`; (c) CB, `A_i ≈ α ≈ 1`.
Power gains: (a) `≈ 75 × 100 = 7500`, (b) `≈ 0.99 × 101 = 100`, (c) `≈ 60`.
**Method:** Identify using two or three signatures together, never one alone:
- (a) **inverting, high `R_in`, high `R_out`, `|A_v| ≫ 1`** ⇒ CE.
- (b) `|A_v| < 1`, **highest `R_in`, lowest `R_out`** ⇒ CC.
- (c) non-inverting, `|A_v| ≫ 1`, but **`R_in` tiny and `R_out` high** ⇒ CB.
  The tiny `R_in` is the tell: a CB input is `re ≈ 22 Ω`, orders of magnitude below
  a CE base input (`rπ ≈ kΩ`) or a CC base input.
Current gain: CE `≈ −β` (the minus is the inversion), CC `≈ β+1` (a follower turns
`β` into `β+1`), CB `≈ α ≈ 1`. Note you cannot pin down `β` from `R_in` alone
without also knowing `I_C`, since `rπ = β/gm` needs `gm` first — use the
identifying signature instead, as above. The contrast worth remembering: CB has
60× the *voltage* gain of CC but `α ≈ 1`, so its **power gain is only ~60**, while
the CE stage's ~7500 dwarfs both. That is why a CB stage exists to feed a high-
impedance node, not to make power.

### Q31. (GATE-level) A design needs `|A_v| ≥ 60` into `R_L = 3 kΩ` with
`R_C = 5 kΩ` and `R_E = 1 kΩ` **present but unbypassed**. Is it possible? If the
bypass capacitor is added, what `I_C` is needed?
**Answer:** Unbypassed, `|A_v| ≈ R_C/R_E = 5` at most — **impossible**. With
`C_E` added: `R_C∥R_L = 1.875 kΩ`, so `gm ≥ 60/1875 = 32 mA/V`, i.e.
`I_C ≥ 0.8 mA`.
**Method:**
- Degenerated: `A_v = −gm·R_C/(1 + gm·R_E)`, and as `gm → ∞` this tends to
  `−R_C/R_E = −5`. The degeneration cap is hard: 5 < 60, no current will help.
- Bypassed: `|A_v| = gm(R_C∥R_L) = gm × 1875 ≥ 60` ⇒ `gm ≥ 32 mS`;
  `I_C = gm·V_T = 0.032 × 25 mV = 0.8 mA`. Check: `−0.032 × 1875 = −60` ✓.
The teaching point: **unbypassed `R_E` places a hard ceiling on CE gain
(`R_C/R_E`) that no amount of current can lift.** Degeneration is a linearity
tool, not a gain-reduction knob you can trade back.

### Q32. (GATE-level) A two-stage chain: `R_s = 1 kΩ` → CE stage (BASE STAGE,
bypassed) → emitter follower (`R_E = R_L = 1 kΩ`, `R_B = 100 kΩ`) → `R_L2 = 1 kΩ`.
Find the gain from `v_s` to the output.
**Answer:** `A_v(CE, loaded) = −143.4`; `A_v(follower) = 0.952`;
`A_vs = −143.4 × 0.952 × 0.6897 = −94.2`.
**Method:** Chain the three factors, each with its own cause:
1. Source → base of CE: `R_in/(R_in + R_s) = 2222/3222 = 0.6897`.
2. CE with the follower's `R_in = 34.65 kΩ` as its load:
   `−gm(R_C ∥ 34.65k) = −0.04 × 3586 = −143.4`.
3. Follower: `0.952`.
Product: `−143.4 × 0.952 = −136.6`; `× 0.6897 = −94.2`.
Note the *sign is negative* — only one inversion in the chain. And note the CE
stage's gain went *up* (80 → 143.4) purely because the follower is a light load;
that is the "buffer buys you back the gain it costs" argument in numbers.

### Q33. (GATE-level) A vendor quotes a cascade as "two CE stages of gain 50 each,
so `A_v = 2500`". The stages are the BASE STAGE, with the last one loaded by
`R_L = 4 kΩ`. What is the correct answer, and how bad is the quoted value?
**Answer:** Correct `A_v = +4571` (73.2 dB) using the real loads
(`A_v1 = −57.1`, `A_v2 = −80`). The quoted 2500 is 45% low, i.e. wrong by 5.2 dB.
**Method:** The quote must have come from some *assumed* per-stage gain (50),
whereas the real per-stage gains follow from the actual loads.
- Stage 1 load = `R_C ∥ R_in2 = 4k ∥ 2.222k = 1.429 kΩ` ⇒
  `A_v1 = −0.04 × 1429 = −57.1`.
- Stage 2 load = `R_C ∥ R_L = 2 kΩ` ⇒ `A_v2 = −80`.
- `A_tot = (−57.1)(−80) = +4571`, `20·log10(4571) = 73.2 dB`; the quote
  corresponds to `20·log10(2500) = 68.0 dB`, so it understates by 5.2 dB.
Note also the *sign*: a positive total means the cascade is non-inverting. Two
rules to carry into the exam — multiply **loaded** gains, and never quote a total
gain without its phase.

### Q34. (GATE-level) Choose the configuration for each requirement and justify
with numbers from this file: (a) maximum voltage gain into a 4 kΩ load;
(b) drive a 100 Ω source with minimum loading; (c) buffer a 1 MΩ source into
10 kΩ; (d) maximum power gain.
**Answer:** (a) **CE** — `|A_v| = 80`, vs `0.952` (CC). (b) **CC (or a FET)**, not
CB: CC's `R_in = 34.7 kΩ` is 347× the 100 Ω source impedance; CB's 25 Ω would
short the source. (c) **CC** — `R_in = 34.7 kΩ` draws 29 µA from a 1 MΩ source,
while `R_out = 124 Ω` loads a 10 kΩ load by only 1.2%; a CE stage's `R_out = 4 kΩ`
would load it by 29%. (d) **CE** — power gain `A_v·A_i = 80 × 50 = 4000`, versus
CB's `80 × 1 = 80` and CC's `0.952 × 101 = 96`.
**Method:** Turn each requirement into a number from this file and let the numbers
choose. (a) voltage gain ⇒ CE. (b) *Input* loading ⇒ high `R_in` ⇒ CC; but if the
requirement is really "do not load the source at all", a FET or a Darlington
(`(β+1)²` input impedance) is the honest answer — say so. (c) impedance
transformation in both directions ⇒ CC. (d) power gain ⇒ CE, because only CE
multiplies a large voltage gain by a large current gain. CB wins nothing here,
which is exactly why it survives only inside cascodes and cascode-like structures.

---

## Trap box (exam-day killers)

- **CE inverts.** "Non-inverting" in a problem means CB or CC — check before
  computing.
- Always use `R_C ∥ R_L` in the gain. Using bare `R_C` inflates the answer.
- Is there a bypass cap across `R_E`? It flips CE gain between `−gm·R` and
  `≈ −R_C/R_E`, and `R_in` between `rπ` and `(β+1)(re+R_E)`.
- `R_in` signatures: CE ≈ `rπ`; CB ≈ `re` (tens of Ω); CC ≈ `(β+1)(R_E∥R_L)`
  (tens of kΩ). Identify from these three, not from the drawing.
- `A_v` vs `A_vs`: `A_vs = A_v·R_in/(R_in + R_s)`. If the problem gives a source
  resistance, this factor is part of the answer.
- In a cascade, multiply **loaded** gains. `A_CE = −gm(R_C ∥ R_in(next))`.
- A CB stage fed from a CE stage kills the CE stage. Put the high-`R_in` stage
  first.
- `R_out` of a CC is `re + R_s/(β+1)`, not `R_E` and not `rπ`.
- CC gain is always **< 1**, never exactly 1: `A_v = (R_E∥R_L)/(re + R_E∥R_L)`.

## Final recall drill (do in 60 seconds)

1. Which config inverts? → *CE.*
2. CE with `R_E` bypassed, `I_C = 1 mA`, `R_C = R_L = 4 kΩ` ⇒ `A_v`? → *−80.*
3. Same but `R_E = 1 kΩ` unbypassed ⇒ `A_v`? → *−3.90 ≈ −R_C/R_E.*
4. CB `R_in`? → *`re` (≈ 25 Ω at 1 mA).*
5. CC `A_v` with `R_E∥R_L = 500 Ω`, `re = 25 Ω`? → *0.952.*
6. CC `R_in` (base) for the same? → *`(β+1)(re + 500) = 53.0 kΩ`.*
7. `R_s = 1 kΩ`, `R_in = 2.22 kΩ` ⇒ `A_v/A_vs`? → *2.222/3.222 = 0.690.*
8. Cascade rule? → *multiply the **loaded** gains.*
9. Two CE stages of −50 each ⇒ total? → *+2500, non-inverting.*
10. `R_out` of a CC with `R_s = 0`? → *`re` = 25 Ω.*

---

Theory behind every answer: `09-BJT-Amplifiers.md`, `29-Formula-Sheet.md`
§29.3, `32-Single-File-Cheatsheet.md` §4 and §13.
