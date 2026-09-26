# AC Coupling — Practice (Learn by Solving)

> **The idea in one line:** this file teaches coupling and bypass capacitors through
> 34 questions only — that every one of them is a high-pass RC pole with
> `f = 1/(2πC·R_eq)`, that the `R_eq` for the emitter bypass is
> `re + R_B/(β+1)` and *not* `R_E`, and that removing the bypass cap trades
> midband gain for a flatter, wider low-frequency response.
>
> **How to use:** solve each question fully before reading the answer. Cover the
> **Answer**/**Method** with paper, do it, then reveal. If you miss one, solve the
> next 3 in the file to lock the pattern. No need to read the chapter notes
> first — every concept is taught through the drill itself. Open
> `10-AC-Coupling.md` or `32-Single-File-Cheatsheet.md` only when you want the
> underlying theory.

## Concept box (what you must internalise)

- In **DC** analysis a capacitor is an **open circuit**; in **midband AC** it is a
  **short circuit**. Get this backwards and every answer is wrong.
- Every coupling or bypass capacitor creates one **high-pass pole** at
  `f = 1/(2π·C·R_eq)`, with `20 dB/decade` of rolloff below it.
- `R_eq` per capacitor:
  - input coupling `C1`: `R_s + R_in(stage)`
  - output coupling `C2`: `R_out + R_L`
  - emitter bypass `C_E`: `re + R_B/(β+1)` — **NOT `R_E`**
- The `−3 dB` point of the whole amplifier is the **largest** of the individual
  pole frequencies (dominant low-frequency pole).
- Design rule of thumb: put each pole at **one tenth** of the lowest signal
  frequency ⇒ about 1 dB of loss at that frequency.
- A coupling cap blocks DC, so the **DC component at a capacitively coupled
  output is 0** — only the AC signal passes.
- Trap: adding a pole never affects the high-frequency rolloff; it only moves
  `f_L`.

**Reference amplifier used throughout:** `I_C = 1 mA ⇒ gm = 40 mA/V, re = 25 Ω`;
`β = 100 ⇒ rπ = 2.5 kΩ`; `R1 = 100 kΩ, R2 = 25 kΩ ⇒ R_B = 20 kΩ`;
`R_C = 4 kΩ`, `R_L = 4 kΩ`, `R_E = 1 kΩ`, `R_s = 1 kΩ`.
Then `R_in = 20k∥2.5k = 2.22 kΩ`, `R_out = 4 kΩ`, midband `A_v = −gm(4k∥4k) = −80`.
Capacitors: `C1 = 0.1 µF` (input coupling), `C_E = 10 µF` (emitter bypass),
`C2 = 1 µF` (output coupling).

---

## Questions

### Q1. (Easy) In DC analysis and in midband AC analysis, what is a capacitor?
**Answer:** DC: **open circuit** (remove it). Midband AC: **short circuit**
(replace it by a wire).
**Method:** Capacitors block DC and pass AC. In DC analysis you want the *bias*
network only, so you delete capacitors. In midband AC analysis you want the
*signal* path only, so you wire around them. This single switch is the most
powerful shortcut in the whole subject — never mix the two analyses in one
circuit diagram.

### Q2. (Easy) A high-pass RC network has `C = 0.1 µF` and `R = 2 kΩ`. Find its
−3 dB frequency.
**Answer:** `f_c = 796 Hz`.
**Method:** `f_c = 1/(2πRC) = 1/(2π × 0.1×10⁻⁶ × 2000) = 1/(1.2566×10⁻³) =
795.8 Hz`. Memorise the shape of the arithmetic: `2π ≈ 6.28`, so
`f_c ≈ 1/(6.28 × C[µF] × R[kΩ] × 10³)`. Handy shortcut: `1/(6.28 × 0.1 × 2) kHz
= 0.796 kHz`.

### Q3. (Easy) Same `R = 2 kΩ` but `C = 1 µF`. Find `f_c` and state the
relationship.
**Answer:** `f_c = 79.6 Hz` — ten times lower, because `f_c ∝ 1/C`.
**Method:** `1/(6.28 × 1×10⁻⁶ × 2000) = 79.6 Hz`. The inverse dependence on `C`
is the whole design lever: audio designs (20 Hz) use 100× the capacitance of
communications designs (2 kHz). Compare also: `f_c ∝ 1/R`, so making the
surrounding resistance smaller raises the pole.

### Q4. (Easy) A signal with a 1 V DC offset is fed through a coupling capacitor
into a stage biased at 3 V. What DC level appears at the stage's input terminal?
**Answer:** 0 V from the source — the capacitor blocks all of it. The base sits
at its own 3 V (set by the bias network, not by the source).
**Method:** The series capacitor's DC impedance is infinite, so no DC current
flows and no DC voltage appears across the load side from the source side. This
is the entire reason for AC coupling: each stage keeps its own Q-point. The
flip side is the familiar "thump" when a supply is switched — that transient is
the coupling capacitor charging.

### Q5. (Easy) How fast does the gain fall below the low cutoff?
**Answer:** 20 dB per decade (6 dB per octave) **per pole**; two poles ⇒ 40 dB/dec.
**Method:** Each first-order high-pass contributes `20·log10` of slope. So a CE
amplifier with three capacitors (C1, C_E, C2) rolls off at 60 dB/dec at very low
frequency, and at frequencies well below all three poles. Recognising the slope
tells you how many poles are active — a very useful GATE self-check on a Bode
sketch.

### Q6. (Easy) In a CE amplifier with `R_E` large, which capacitor usually sets the
lowest useful frequency of the amplifier?
**Answer:** The **emitter bypass capacitor `C_E`**.
**Method:** `C_E` does two jobs: it removes `R_E` from the AC gain, and it
establishes the high-pass corner below which the gain collapses back to
`−R_C/R_E`. Because its `R_eq` is tiny (`re + R_B/(β+1)`, often ~100 Ω), the
product `C_E·R_eq` is small and the corner lands higher than the coupling caps'
corners. The rule from `10-AC-Coupling.md` §10.4: "a low output at bass
frequencies usually points at `C_E`."

### Q7. (Easy) Write the DC analysis of the reference amplifier with `C1`, `C_E`,
`C2` all present. Which components appear?
**Answer:** `C1`, `C_E`, `C2` are all removed (open). Only `R1`, `R2`, `R_E`,
`R_C`, the transistor and the supplies remain. `I_C ≈ (V_B − V_BE)/R_E`.
**Method:** Delete the capacitors and solve the bias loop as in
`07-BJT-Biasing.md`. The midband gain `−gm·R_C` then comes from a *second*
circuit, in which the very same capacitors are wires. Two different circuits, one
transistor — that is the split the whole chapter exists to teach.

### Q8. (Easy) What does "3 dB down" mean numerically, and why is it 3 dB?
**Answer:** The amplitude is `1/√2 = 0.707` of the passband value, i.e. 70.7% of
the output.
**Method:** `20·log10(0.707) = −3.01 dB`. Half the *power* is
`10·log10(0.5) = −3.01 dB`. Use `−3 dB` as "half power" and remember the
amplitude is then 0.707, not 0.5. For a high-pass, the −3 dB point is exactly
where `|X_C| = R` in the series arm.

### Q9. (Easy) Choose `C` so that a coupling capacitor with `R = 2 kΩ` in its
charging loop gives a corner at 10 Hz.
**Answer:** `C = 7.96 µF`.
**Method:** Invert the formula: `C = 1/(2πfR) = 1/(2π × 10 × 2000) =
1/125 664 = 7.96 µF`. Use the shortcut: `C[µF] = 159/(f[Hz] × R[kΩ])` =
`159/(10 × 2) = 7.95 µF`. Memorise the 159 — it is `10⁶/(2π)` and it turns every
"choose the capacitor" question into one division.

### Q10. (Easy) An emitter resistor has a bypass capacitor. What is the stage called
if you delete the capacitor, and what happens to the midband gain?
**Answer:** A **CE stage with unbypassed (degenerative) `R_E`**. The gain drops
from `−gm(R_C∥R_L) = −80` to `−R_C/R_E = −4` (exactly `−3.90`).
**Method:** Bypassed, the emitter is an AC ground and the full `gm` gain appears.
Unbypassed, `R_E` feeds back against the signal: `A_v = −gm·R_C/(1 + gm·R_E) =
−0.04 × 4000/41 = −3.90`. So removing one capacitor costs 26.2 dB of gain and
buys a flatter, wider low-frequency response — the trade explored in Q16 and Q31.

### Q11. (Moderate) Find the input-coupling pole `f1` for the reference amplifier
(`C1 = 0.1 µF`).
**Answer:** `f1 = 1/(2π × 0.1 µF × 3.222 kΩ) = 494 Hz`.
**Method:** The resistance the capacitor charges through is the **sum** seen from
its two terminals with the source killed: the source resistance on one side,
`R_s = 1 kΩ`, and the stage's `R_in = 2.22 kΩ` on the other.
`R_eq = 1 k + 2.222 k = 3.222 kΩ`.
`f1 = 1/(2π × 1×10⁻⁷ × 3222) = 1/(2.024×10⁻³) = 494 Hz`.
The `+` (not `∥`) is the point: a series coupling capacitor sees the two
impedances in series.

### Q12. (Moderate) Find the output-coupling pole `f2` (`C2 = 1 µF`).
**Answer:** `f2 = 1/(2π × 1 µF × 8 kΩ) = 19.9 Hz`.
**Method:** `R_eq = R_out + R_L = 4 k + 4 k = 8 kΩ`.
`f2 = 1/(2π × 1×10⁻⁶ × 8000) = 1/(5.027×10⁻²) = 19.9 Hz`.
Again a sum: from the output node, looking back you see `R_out`, and looking
forward you see `R_L`. The method to reuse: **identify the capacitor's two
terminals, kill independent sources, and add the resistances seen looking out
of each terminal.**

### Q13. (Moderate) Find the emitter-bypass pole `fE` for `C_E = 10 µF`.
**Answer:** `R_eq = re + R_B/(β+1) = 25 + 99.5 = 124.5 Ω`, so
`fE = 128 Hz`.
**Method:** With the signal source zeroed, the resistance seen by `C_E` is
`re` in series with whatever drives the base, divided by `β+1`:
`R_B/(β+1) = 20 000/201 = 99.5 Ω`. Total `124.5 Ω`.
`fE = 1/(2π × 10×10⁻⁶ × 124.5) = 1/(7.82×10⁻³) = 127.8 Hz ≈ 128 Hz`.
Note the whole "hard" part is the division by `β+1`: the base circuit looks like
20 kΩ to you but like 100 Ω to the emitter.

### Q14. (Moderate) A student computes the Q13 pole using `R_E = 1 kΩ` instead of
124.5 Ω. What frequency does he get, and how wrong is it?
**Answer:** `15.9 Hz` instead of `128 Hz` — **8× too low**, i.e. he concludes the
amplifier is far better at low frequencies than it is.
**Method:** `1/(2π × 10×10⁻⁶ × 1000) = 15.9 Hz`. The error factor is exactly
`R_E/R_eq = 1000/124.5 = 8.03`. This is the classic mistake listed in
`10-AC-Coupling.md` §10.6: the capacitor does **not** see `R_E`, because when
`C_E` is (nearly) a short, `R_E` is shorted out. It sees `re` and the base circuit
attenuated by `β+1`.

### Q15. (Moderate) For the reference amplifier with `C1 = 0.1 µF`,
`C_E = 10 µF`, `C2 = 1 µF`, what is the amplifier's lower 3-dB frequency?
**Answer:** `max(494, 128, 19.9) = 494 Hz`, set by the input coupling cap.
**Method:** List the three poles (`f1 = 494`, `fE = 128`, `f2 = 19.9` Hz) and take
the largest — the *dominant* low-frequency pole. Where the poles are well
separated, the overall −3 dB point is essentially the largest one; when they are
within a factor of ~2 of each other the exact answer is a little higher (root-sum
of squares), which is the only time you need `f_L ≈ √(f1² + fE²)`.

### Q16. (Moderate) What exactly changes when `C_E` is removed from the reference
amplifier?
**Answer:** Midband gain `−80 → −3.90` (−26.2 dB); `R_in` `2.22 kΩ → 16.76 kΩ`;
the `fE = 128 Hz` pole **disappears**; `R_out` unchanged at 4 kΩ.
**Method:** With no capacitor, `R_E` is in the AC circuit for all frequencies.
- `A_v = −gm·R_C/(1 + gm·R_E) = −160/41 = −3.90`;
  `20·log10(3.90/80) = −26.2 dB`.
- `R_in = R_B ∥ (β+1)(re + R_E) = 20k ∥ 103.5k = 16.76 kΩ` (7.5× higher).
- No capacitor, no pole: the rolloff is now only from `C1` and `C2`.
- `R_out = R_C` because the output node is unchanged.
The gain and the bandwidth are the two things being traded; the bandwidth wins in
the passband-flatness sense, the gain wins in everything else.

### Q17. (Moderate) A single high-pass pole is at `f_c`. What is the amplitude
ratio and the dB loss at `f = 2f_c`?
**Answer:** `0.894` (89.4%), i.e. −0.97 dB.
**Method:** `|H| = (f/f_c)/√(1 + (f/f_c)²)`. With `f/f_c = 2`:
`2/√5 = 0.894`. `20·log10(0.894) = −0.97 dB`. General lesson: **one decade above
the pole the loss is only 1 dB** — that is exactly why the design rule says put
each pole a decade below the lowest frequency you care about.

### Q18. (Moderate) Same pole, what is the ratio and dB loss at `f = f_c/10`?
**Answer:** `0.0995`, i.e. −20.04 dB.
**Method:** `0.1/√(1 + 0.01) = 0.1/1.005 = 0.0995`.
`20·log10(0.0995) = −20.04 dB`. A decade *below* a pole, the gain is down 20 dB
(one pole). Symmetric facts to memorise as a pair: at `f_c` it is −3 dB, at
`f_c/10` it is −20 dB, and at `10f_c` it is −0.04 dB.

### Q19. (Moderate) The lowest frequency you must pass is 50 Hz. What `C1` do you
choose for `R_eq = 3.222 kΩ`, using the 1/10 rule?
**Answer:** Corner at 5 Hz ⇒ `C1 = 9.88 µF` (choose 10 µF).
**Method:** `f_corner = 50/10 = 5 Hz`; `C = 159/(f[kHz] × R[kΩ]) =
159/(0.005 × 3.222) = 9.87 µF`, or directly `1/(2π × 5 × 3222) = 9.88 µF`.
At 50 Hz (ten corners up) the loss is the 0.97 dB of Q17 — "about 1 dB", which
is the rule's promise. Choosing a 10 µF standard value is the practical step.

### Q20. (Moderate) `C_E = 10 µF` at 10 Hz: what is `|X_C|`, and is the bypass
working at 10 Hz?
**Answer:** `|X_C| = 1/(2π × 10 × 10×10⁻⁶) = 1592 Ω`. Since that is larger than
`R_E = 1 kΩ`, the bypass is **not** effective at 10 Hz — `R_E` is still in the
AC circuit and the gain is near `−R_C/R_E = −4`.
**Method:** `X_C = 1/(2πfC) = 1/(2π × 10 × 10 µ) = 1592 Ω`. The test is a
comparison, not a formula: the bypass works when `|X_C| ≪ R_eq_seen` (here
`R_eq = 124.5 Ω`, so we need `|X_C| ≪ 124.5 Ω`, which needs `f ≫ 128 Hz` — the
Q13 corner, consistent). This is the physical picture behind the pole: as `f`
falls, `X_C` grows, `R_E` re-enters, and the gain slides from −80 down to −4.

### Q21. (Moderate) You must raise a pole from 796 Hz to 1600 Hz with the same
resistance. What happens to `C`?
**Answer:** `C` must be **halved**: from 0.1 µF to 0.05 µF.
**Method:** `f ∝ 1/C`, so doubling `f` halves `C`. Conversely, doubling `C` to
0.2 µF drops the corner to 398 Hz. This is the trade every coupling-capacitor
choice faces: bigger `C` costs area, cost and input capacitance (which hurts the
*high* end), but buys low-frequency extension.

### Q22. (Moderate) Choose `C_E` for a corner at 200 Hz and at 20 Hz, given
`R_eq = 124.5 Ω`.
**Answer:** `C = 6.39 µF` for 200 Hz; `C = 63.9 µF` for 20 Hz.
**Method:** `C = 1/(2πfR_eq)`. At 200 Hz: `1/(2π × 200 × 124.5) = 6.39 µF`.
At 20 Hz: `63.9 µF`. Note the factor of 10 again. A 64 µF electrolytic is large
and leaky — this is the practical reason audio stages sometimes use a *split*
emitter resistor (a small unbypassed part for linearisation plus a smaller
bypassable part), a trick examined in `07-BJT-Biasing.md`.

### Q23. (Moderate) Two identical high-pass poles are each at 100 Hz. At what
frequency is the cascade 3 dB down, and what is each pole doing there?
**Answer:** 155.4 Hz; each pole is at 0.841 there, and `0.841² = 0.707 = 1/√2`.
**Method:** The cascade magnitude is the product of the individual ones, so with
N equal poles `|H| = [x/√(1+x²)]^N` where `x = f/f_pole`. Set
`|H| = 1/√2 = 2^(−1/2)`, which forces each pole to sit at
`2^(−1/(2N))`:
- N = 1: `2^(−1/2) = 0.7071` ⇒ `x = 1` ⇒ `f = 100 Hz` (the textbook answer).
- N = 2: `2^(−1/4) = 0.8409` ⇒ `x² = 0.8409²(1+x²)` ⇒
  `x²(1 − 0.7071) = 0.7071` ⇒ `x² = 2.414` ⇒ `x = 1.554` ⇒ `f = 155.4 Hz`.

The direction is the point worth remembering: the combined 3 dB point moves
**up**, not down. At 100 Hz each pole is already 3 dB down, so the pair is 6 dB
down — you have to climb above 100 Hz to be back within 3 dB of the passband.

**Exam shortcut:** you rarely need this. Report the amplifier's `f_L` as the
*largest individual corner* (100 Hz here) and state that the extra pole adds
20 dB/decade of rolloff. Quote the exact combination only when a question
explicitly asks for the total response.

### Q24. (Moderate) Three identical high-pass poles each at 100 Hz. Where is the
cascade 3 dB down?
**Answer:** 196 Hz, with each pole at 0.891.
**Method:** Same construction as Q23 with N = 3: per-pole target
`2^(−1/6) = 0.8909`. `x²(1 − 0.8909²) = 0.8909²` ⇒
`x²(0.2063) = 0.7937` ⇒ `x² = 3.847` ⇒ `x = 1.961` ⇒ `f = 196.1 Hz`.
Check the trend: 1 pole → 1.00 f_pole, 2 poles → 1.55 f_pole, 3 poles → 1.96
f_pole, rising toward 2.4 for many poles. The three *practical* conclusions to
carry forward:
- `f_L` (bandwidth corner) ≈ largest individual corner — the standard answer.
- Below the corner the slope is 20 dB/dec per active pole.
- What extra poles cost you is **phase and transient droop**, not the corner.

### Q25. (GATE-level) Full low-frequency analysis of the reference amplifier
(`C1 = 0.1 µF`, `C_E = 10 µF`, `C2 = 1 µF`). Give all three pole frequencies, the
dominant one, and the total attenuation one decade below the dominant pole.
**Answer:** `f1 = 494 Hz`, `fE = 128 Hz`, `f2 = 19.9 Hz`; `f_L = 494 Hz`; at
49.4 Hz the total is `0.0333`, i.e. **−29.6 dB**.
**Method:** First the three `R_eq` values, then `f = 1/(2πCR_eq)`:
- `C1`: `R_eq = R_s + R_in = 1k + 2.222k = 3.222 kΩ` ⇒ 494 Hz
- `C_E`: `R_eq = re + R_B/(β+1) = 124.5 Ω` ⇒ 128 Hz
- `C2`: `R_eq = R_out + R_L = 4k + 4k = 8 kΩ` ⇒ 19.9 Hz

`f_L = max = 494 Hz` — the dominant pole. Now the decade-below check, multiplying
all three magnitudes at `f = 49.4 Hz`:

| pole | x = f/f_pole | \|H\| | dB |
|---|---|---|---|
| C1 (494 Hz) | 0.100 | 0.0995 | −20.04 |
| C_E (128 Hz) | 0.386 | 0.3605 | −8.86 |
| C2 (19.9 Hz) | 2.483 | 0.9276 | −0.65 |
| **total** | | **0.0333** | **−29.6** |

The takeaway the chapter wants: "about −20 dB one decade down" is only true for
the *dominant* pole in isolation. `C_E` adds nearly 9 dB more, because at 49.4 Hz
it too is well below its own corner. Always multiply the poles, never just quote
the dominant one.

### Q26. (GATE-level) Derive the `R_eq` seen by the emitter bypass capacitor, and
explain why it is *not* `R_E`.
**Answer:** `R_eq = re + R_B/(β+1)`, where `R_B` is the AC resistance from the
base to AC ground (the bias network in parallel with `rπ` and the source).
For the reference amplifier: `25 + 20k/201 = 124.5 Ω`.
**Method:** With the source zeroed, walk out of the capacitor's terminals.
Emitter side: `re` to AC ground. Base side: `R_B` to AC ground, but the base
*current* is only `1/(β+1)` of the emitter current, so the base circuit appears
divided by `β+1`. The two are in **series** through the transistor, giving
`re + R_B/(β+1)`. Why not `R_E`: when `C_E` is nearly a short, `R_E` is shorted
out and carries almost no signal current. The whole point of a bypass capacitor
is that it removes `R_E` — so `R_E` cannot be the resistance that sets the
corner. Using `R_E` puts the corner 8× too low (Q14), i.e. you would wrongly
conclude your amplifier has far more bass than it has.

### Q27. (GATE-level) A CE stage has `R_E = 1 kΩ` bypassed by `C_E = 100 µF`, and
`re = 25 Ω`, `R_B = 20 kΩ`, `β = 100`. Find the corner, and say at what frequency
the bypass becomes "good enough" (one decade above).
**Answer:** `R_eq = 124.5 Ω`, `f = 1/(2π × 100 µF × 124.5) = 12.8 Hz`. Good enough
above ≈ 128 Hz.
**Method:** `2π × 100×10⁻⁶ × 124.5 = 0.0782`; `1/0.0782 = 12.8 Hz`. One decade
above, 128 Hz, the loss from the incomplete bypass is the 0.97 dB of Q17. Notice
the design logic: 100 µF is an enormous capacitor, and it is needed only because
`R_eq` is small. A student who (wrongly) used `R_E = 1 kΩ` would compute 159 Hz and
feel satisfied — and would then discover the real problem at 20 Hz.

### Q28. (GATE-level) A guitar amplifier is described as "sounding thin below
100 Hz". Which capacitor is the most likely culprit and why?
**Answer:** The emitter bypass `C_E` — its pole sits at or above 100 Hz, so below
that the gain collapses from `−gm·R` toward `−R_C/R_E`, killing the low
midrange. A too-small `C1` is the alternative suspect.
**Method:** Work from the symptom: bass and low-mids missing, top end intact ⇒ a
*high-pass* is cutting in, not a loudness or headroom problem. Then split the
poles: coupling caps (`C1`, `C2`) usually sit in the tens of Hz; the `C_E` pole
sits much higher because its `R_eq` is only ~100 Ω. So the highest pole of the
three is very often the `C_E` one — matching Q6. The engineering fix is a larger
`C_E` (Q27) or a split emitter resistor with only a small part bypassed.

### Q29. (GATE-level) Two identical RC-coupled stages, each with a 100 Hz
high-pass pole. Describe the combined response: the rolloff slope far below the
corners, and what the amplifier's `f_L` is.
**Answer:** 40 dB/decade far below 100 Hz; `f_L ≈ 100 Hz` (the largest individual
corner). The exact combined 3 dB point is 155 Hz.
**Method:** Poles multiply in magnitude and add in slope, so two corners ⇒ 20+20 =
40 dB/decade. The *bandwidth* answer stays the largest corner, 100 Hz, because
that is where the first pole hits −3 dB. The exact combined 3 dB point of
155.4 Hz comes from Q23's construction, but no GATE question expects it here.
Distinguish the two ideas deliberately, because GATE tests exactly this:
- **Bandwidth** = `f_H − f_L`, with `f_L` = largest corner.
- **Rolloff slope** = what the response does *below* the corner, 20 dB/dec each.
- **Phase** = the hidden cost: two poles at 100 Hz contribute −180° at 100 Hz,
  which is why multi-stage designs care about *group delay* at the band edge.

### Q30. (GATE-level) A CE amplifier must pass 20 Hz. The input coupling sees
`R_s + R_in = 3.222 kΩ` and the output coupling sees `R_out + R_L = 8 kΩ`. Choose
`C1` and `C2` (a) for a 20 Hz corner, and (b) using the 1/10 rule.
**Answer:** (a) `C1 = 2.47 µF`, `C2 = 0.995 µF`. (b) `C1 = 24.7 µF`,
`C2 = 9.95 µF`.
**Method:** Use the shortcut `C[µF] = 159/(f[Hz] × R[kΩ])`:
- (a) `C1 = 159/(20 × 3.222) = 2.47 µF`; `C2 = 159/(20 × 8) = 0.995 µF`.
  Cross-check: `1/(2π × 20 × 3222) = 2.47 µF` ✓
- (b) A decade lower corner = ten times the capacitance:
  `C1 = 24.7 µF`, `C2 = 9.95 µF`.

Note the asymmetry: the *same* frequency needs a 2.5× larger `C1` than `C2`,
because `C1` sees the smaller resistance. Always compare `R_eq` values — never
assume the coupling capacitors of a stage are equal.

### Q31. (GATE-level) The reference amplifier but with `R_s = 0` and
`C1 = C2 = 10 µF`. (a) List the poles and the dominant one. (b) Delete `C_E` and
find the new dominant pole. (c) Explain the trade in words.
**Answer:** (a) `f1 = 7.16 Hz`, `f2 = 1.99 Hz`, `fE = 128 Hz` ⇒ `f_L = 128 Hz`
(now set by `C_E`). (b) Without `C_E`: `f_L = 7.16 Hz` — 18× lower.
(c) Gain drops 26.2 dB (from −80 to −3.90) but the low-frequency response becomes
flatter and reaches far lower.
**Method:** (a) `f1 = 1/(2π × 10 µF × 2.222 kΩ) = 1/(2π × 0.02222) = 7.16 Hz`;
`f2 = 1/(2π × 10 µF × 8 kΩ) = 1.99 Hz`; `fE = 128 Hz`. `f_L = max = 128 Hz`.
(b) Without `C_E` the only poles are 7.16 and 1.99 Hz, so `f_L = 7.16 Hz`.
(c) This is the cleanest demonstration in the chapter: **the emitter bypass cap
is usually the dominant low-frequency pole precisely because it is the one that
buys the most gain.** Delete it and the amplifier's bass extension improves by
18× at the price of 26 dB of midband gain. Designers who need both choose a
partially bypassed (split) emitter resistor, or accept a lower gain for a
wider band.

### Q32. (GATE-level) The dominant pole is at 200 Hz. Compute the total
attenuation at 50 Hz for (a) one pole, (b) two equal poles, (c) three equal poles.
**Answer:** (a) −12.3 dB, (b) −24.6 dB, (c) −36.9 dB.
**Method:** `x = f/f_pole = 50/200 = 0.25`; per-pole magnitude
`0.25/√(1 + 0.0625) = 0.25/1.0308 = 0.2425` (−12.3 dB). For N poles the total is
`0.2425^N`: `0.2425² = 0.0588` (−24.6 dB); `0.0588 × 0.2425 = 0.0143` (−36.9 dB).
So each extra pole costs almost exactly another 12.3 dB at this frequency —
which is the whole argument for the 1/10 rule: it puts you where the extra poles
cost ~1 dB each instead of 12 dB each.

### Q33. (GATE-level) When is *direct* coupling used instead of RC coupling, and
what is the trade?
**Answer:** In integrated circuits and op-amps, where capacitors are impractical.
The trade: direct coupling removes the `C1`/`C2` poles (so `f_L → 0` and
bandwidth is limited only by the high end), but every stage then shares one
operating point, so DC offsets and drift accumulate and level shifting is needed.
**Method:** The decision is economic as much as electrical: an on-chip capacitor
is orders of magnitude larger than a transistor, so IC designers use
current-source bias and direct coupling, and accept the DC-level management
problem. Discrete designs, where a 10 µF electrolytic is cheap, use RC coupling
and get independent bias points for free. In a GATE numerical, "the amplifier is
directly coupled" means: **no low-frequency poles at all from coupling** — any
remaining rolloff is from bypass capacitors or the transistor itself.

### Q34. (GATE-level) A CE stage has a *deliberately unbypassed* `R_E = 1 kΩ` and
**no** coupling capacitors at all (it is fed by a direct-coupled driver). List
every low-frequency pole in the circuit and say what sets the bandwidth.
**Answer:** **There are no low-frequency poles from capacitors** — the circuit has
none. `f_L = 0`; the bandwidth is limited only by the high-frequency
transistor capacitances (Chapter 16 / `16-Frequency-Response.md`).
**Method:** A pole requires a capacitor. With `C1`, `C2` and `C_E` all absent
there is no high-pass behaviour at all, and the gain is `−R_C/R_E` from DC to
the Miller limit. The consequences are the mirror image of Chapter 09's:
- DC and LF behaviour: perfect (no rolloff, no phase shift at low f).
- Gain: low and resistor-set, so excellent linearity and stability.
- LF transit-time and offset drift: now a real problem, which is exactly why
  direct coupling is used in ICs *with* level shifting and chopper/bias
  compensation. Any "which capacitor limits the LF response?" question must be
  answered by listing the capacitors that actually exist.

---

## Trap box (exam-day killers)

- DC: capacitors are **open**. Midband: capacitors are **short**. Never mix.
- The emitter bypass resistance is `re + R_B/(β+1)`, **not `R_E`**. Using `R_E`
  puts the corner ~8× too low and hides a real bass problem.
- `R_eq` for a **series** coupling cap is the **sum** of the resistances seen
  from its two terminals (`R_s + R_in`, `R_out + R_L`), never the parallel value.
- `f_L` = the **largest** pole frequency, not the sum, product or smallest.
- Extra poles change the **rolloff slope** (20 dB/dec each), not the reported
  bandwidth corner.
- High-pass poles move the −3 dB point of a *bank* of poles **upward** as poles
  are added (each pole helps below its own corner); the amplifier's *low cutoff*
  is still the largest individual corner. Keep the two ideas apart.
- Removing `C_E` = gain down 26 dB, `R_in` up 7.5×, one pole gone, band wider.
- Design rule: corner ≈ `f_min/10` ⇒ ~1 dB loss at `f_min`. Use it, GATE expects
  it.
- A coupling cap forces the **DC output component to 0** — but the *next stage's*
  base still sits at its own bias voltage. Those are different statements.
- `C` and `f` are inversely proportional; `R` and `f` too. Doubling either `C` or
  `R` halves the corner.

## Final recall drill (do in 60 seconds)

1. Capacitor in DC analysis? → *open circuit.*
2. Capacitor in midband AC? → *short circuit.*
3. `C = 0.1 µF`, `R = 2 kΩ` ⇒ `f_c`? → *796 Hz.*
4. `C[µF] = ?/(f[Hz]·R[kΩ])` ⇒ the constant? → *159.*
5. Emitter-bypass `R_eq`? → *`re + R_B/(β+1)`* — **not `R_E`**.
6. `re = 25 Ω`, `R_B = 20 kΩ`, `β = 100` ⇒ `R_eq`? → *`25 + 99.5 = 124.5 Ω`.*
7. `C_E = 10 µF`, `R_eq = 124.5 Ω` ⇒ `f_E`? → *128 Hz.*
8. Poles at 494, 128, 20 Hz ⇒ `f_L`? → *494 Hz (the largest).*
9. Delete `C_E`: gain and `R_in`? → *`−80 → −3.90`; `2.22 k → 16.8 kΩ`.*
10. Rolloff per pole? → *20 dB/decade.*

---

Theory behind every answer: `10-AC-Coupling.md`, `29-Formula-Sheet.md` §29.5,
`32-Single-File-Cheatsheet.md` §13 and §15.
