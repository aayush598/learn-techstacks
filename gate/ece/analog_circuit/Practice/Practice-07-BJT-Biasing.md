# BJT Biasing — Practice (Learn by Solving)

> **The idea in one line:** this file teaches biasing through 34 questions only —
> that every bias circuit is one loop equation, that the "stable" ones are stable
> because the Q-point is set by *resistors* instead of by β, and that the
> stability factor `S` is just the number that tells you how much β leakage and
> temperature can move `I_C`.
>
> **How to use:** solve each question fully before reading the answer. Cover the
> **Answer**/**Method** with paper, do it, then reveal. If you miss one, solve the
> next 3 in the file to lock the pattern. No need to read the chapter notes
> first — every concept is taught through the drill itself. Open
> `07-BJT-Biasing.md` or `32-Single-File-Cheatsheet.md` only when you want the
> underlying theory.

## Concept box (what you must internalise)

- Fixed bias: `I_B = (V_BB − V_BE)/R_B`, `I_C = β·I_B`,
  `V_CE = V_CC − I_C·R_C`, and **`S = 1 + β`** (worst stability in the subject).
- Collector-to-base: `I_B = (V_CC − V_BE)/(R_B + β·R_C)`,
  `S ≈ (1+β)·R_C/(R_B + R_C)`.
- Emitter bias: `I_B = (V_BB − V_BE)/(R_B + (β+1)·R_E)`; when `R_B ≪ (β+1)R_E`,
  `I_C ≈ (V_B − V_BE)/R_E` — β disappears.
- Voltage divider: `V_B = V_CC·R2/(R1+R2)`, `V_th = V_B`, `R_th = R1∥R2`;
  **approximate is legal iff `β·R_E ≥ 10·R2`**.
- Exact divider: `I_B = (V_th − V_BE)/(R_th + (β+1)R_E)`,
  `V_CE = V_CC − I_C·R_C − I_E·R_E` (the `R_E` term is not optional).
- `S = ΔI_C/ΔI_CBO`. Smaller is better. Ideal `S = 1`; fixed bias gives `S = 1+β`.
- Method: DC analysis order is always **loop → I_B → I_C → V_CE → region check**.
- Trap: `V_CE = V_CC − I_C·R_C` only. Any `R_E` must appear as `I_C(R_C + R_E)`.

---

## Questions

### Q1. (Easy) Fixed bias with `V_BB = 2 V`, `R_B = 100 kΩ`, `V_BE = 0.7 V`.
Find `I_B`.
**Answer:** `I_B = 13 µA`.
**Method:** `I_B = (V_BB − V_BE)/R_B = (2 − 0.7)/100 kΩ = 1.3/100k = 13 µA`.
The loop is: stiff source `V_BB` → `R_B` → base-emitter drop → ground. The 0.7 V
is the only nonlinear part, and the rest is one Ohm's law. Work in consistent
units: 1.3 V over 100 kΩ is 13 µA (V/kΩ = mA).

### Q2. (Easy) Same circuit, plus `β = 100`, `V_CC = 10 V`, `R_C = 2 kΩ`. Find
`I_C` and `V_CE`.
**Answer:** `I_C = 1.3 mA`, `V_CE = 7.4 V`.
**Method:** `I_C = β·I_B = 100 × 13 µA = 1.3 mA`. Then the collector loop:
`V_CE = V_CC − I_C·R_C = 10 − (1.3 mA)(2 kΩ) = 10 − 2.6 = 7.4 V`. Notice the two
loops are *independent* here because there are two supplies — that is the whole
reason fixed bias uses `V_BB` separately from `V_CC`.

### Q3. (Easy) What is the stability factor of fixed bias for a transistor with
`β = 199`?
**Answer:** `S = 1 + β = 200`.
**Method:** Fixed bias is the one circuit where `S = 1 + β` exactly, because
`I_B` is set by a resistor and *any* extra collector current (leakage) is
amplified by the full gain: `I_C = β·I_B + (β+1)·I_CBO`, so
`ΔI_C/ΔI_CBO = β+1`. `β = 199` gives `S = 200`, i.e. one µA of leakage
produces 200 µA of collector-current error.

### Q4. (Easy) Which of the four standard bias circuits is the **most** stable and
which the **least**?
**Answer:** Most stable = voltage-divider bias with a large `R_E`. Least stable =
fixed bias.
**Method:** The single question that decides it: *is `I_C` set by β or by
resistors?* Fixed bias sets `I_C = β·(V_BB−V_BE)/R_B`, so `I_C ∝ β` — fully
unstable. In the voltage-divider circuit, if `β·R_E ≫ R_th + R_E` then
`I_C → (V_B − V_BE)/R_E`, which contains **no β at all** — perfectly stable.
`07-BJT-Biasing.md` §7.7 gives the ranking: divider > emitter > collector-to-base
> fixed.

### Q5. (Easy) Voltage-divider bias from `V_CC = 12 V` with `R1 = 100 kΩ`
(supply to base) and `R2 = 25 kΩ` (base to ground). Find the unloaded base
voltage `V_B`.
**Answer:** `V_B = 2.4 V`.
**Method:** `V_B = V_CC·R2/(R1+R2) = 12 × 25/125 = 2.4 V`. The lower resistor
sets the ratio — always identify which of `R1`,`R2` is the *bottom* one. Quick
check: 25/125 = 0.2, and 20% of 12 V is 2.4 V. This is the **unloaded** value;
it is only the true base voltage if `I_B` draws negligible current (Q7).

### Q6. (Easy) With `R_E = 1 kΩ` in Q5, estimate `I_C`.
**Answer:** `I_C ≈ (2.4 − 0.7)/1 kΩ = 1.7 mA`.
**Method:** `I_C ≈ I_E = V_E/R_E` and `V_E = V_B − V_BE = 2.4 − 0.7 = 1.7 V`.
So `I_C ≈ 1.7 mA`. The reason this is so clean: `I_C` is now decided by
`R_E` and a *voltage*, with β nowhere in sight. That is the entire design idea
of emitter degeneration.

### Q7. (Easy) `β = 200`, `R_E = 1 kΩ`, `R2 = 25 kΩ`. Is the Q6 approximation
legal?
**Answer:** No — it is borderline-to-illegal. `β·R_E = 200 kΩ` but
`10·R2 = 250 kΩ`, so the rule `β·R_E ≥ 10·R2` **fails**. Do the exact analysis.
**Method:** The test is `β·R_E ≥ 10·R2`, which comes from requiring
`I_B·R2 ≤ 0.1·I_E·R_E`, i.e. the base-current loading of the divider to be under
10%. Here `R2 = 25 kΩ` is a quarter of `β·R_E = 200 kΩ` — the divider current
(`12/125 kΩ = 96 µA`) is not much larger than the base current you actually need
(`~8 µA`… but see Q27 where the exact answer is `1.54 mA`, not 1.7 mA).
**When a GATE question prints the inequality, respect it.** If it does not,
either do exact or check the answer is within ~10%.

### Q8. (Easy) Collector-to-base bias: `V_CC = 10 V`, `R_C = 2 kΩ`, `R_B` from
collector to base `= 100 kΩ`, `β = 100`, `V_BE = 0.7 V`. Find `I_B`.
**Answer:** `I_B = 31 µA`.
**Method:** `I_B = (V_CC − V_BE)/(R_B + β·R_C) = 9.3/(100 kΩ + 200 kΩ) =
9.3/300 kΩ = 31 µA`. Derive it yourself once: the supply drives current through
`R_C` *and* `R_B` in series into the base, so
`V_CC − V_BE = I_C·R_C + I_B·R_B = β·I_B·R_C + I_B·R_B`. The `β·R_C` term in
the denominator is the feedback doing its job.

### Q9. (Easy) Emitter bias: `V_BB = 2 V`, `R_B = 10 kΩ`, `R_E = 1 kΩ`,
`β = 100`, `V_BE = 0.7 V`. Find `I_B`.
**Answer:** `I_B = 11.7 µA`.
**Method:** `I_B = (V_BB − V_BE)/(R_B + (β+1)R_E) = 1.3/(10 kΩ + 101 × 1 kΩ) =
1.3/111 kΩ = 11.71 µA`. The denominator uses **`(β+1)R_E`, not `βR_E`**, because
`R_E` carries the *emitter* current, and `I_E = (β+1)I_B`. That `+1` is the most
common single error in this chapter.

### Q10. (Easy) From Q9, find `I_C`, `I_E` and `V_E`.
**Answer:** `I_C = 1.171 mA`, `I_E = 1.183 mA`, `V_E = 1.183 V`.
**Method:** `I_C = 100 × 11.71 µA = 1.171 mA`; `I_E = 101 × 11.71 µA =
1.183 mA`; `V_E = I_E·R_E = 1.183 mA × 1 kΩ = 1.183 V`. `I_C` and `I_E` differ by
exactly `I_B`, so writing both is a free self-check.

### Q11. (Moderate) Full emitter bias: `V_BB = 2 V`, `R_B = 100 kΩ`, `R_E = 1 kΩ`,
`R_C = 3 kΩ`, `V_CC = 10 V`, `β = 100`. Find `I_C`, `V_E`, `V_C`, `V_CE` and the
region.
**Answer:** `I_B = 6.47 µA`, `I_C = 0.647 mA`, `I_E = 0.653 mA`, `V_E = 0.653 V`,
`V_C = 8.06 V`, `V_CE = 7.41 V` — **active**.
**Method:** `I_B = (2 − 0.7)/(100 kΩ + 101 × 1 kΩ) = 1.3/201 kΩ = 6.468 µA`.
Then `I_C = 0.6468 mA`, `I_E = 0.6532 mA`. `V_E = 0.6532 V`;
`V_C = 10 − (0.6468 mA)(3 kΩ) = 10 − 1.940 = 8.06 V`; `V_CE = V_C − V_E =
7.41 V`. Region: `V_C = 8.06 > V_B = 2 > V_E = 0.65` ✓. Always finish with the
region check — a Q-point "answer" without it is half an answer.

### Q12. (Moderate) For the circuit in Q11, the "rough" estimate
`I_C ≈ (V_BB − V_BE)/R_E` gives what value, and what is the percentage error?
**Answer:** 1.3 mA; the exact answer 0.647 mA is 50% lower (the approximation
over-estimates by 101%).
**Method:** `(2 − 0.7)/1 kΩ = 1.3 mA`. The rough form drops `R_B/(β+1)` from the
denominator: exact is `I_C = β(V_BB−V_BE)/(R_B + (β+1)R_E)`, rough is
`I_C ≈ β(V_BB−V_BE)/((β+1)R_E)`. They agree only when
`R_B ≪ (β+1)R_E`; here `100 kΩ` vs `101 kΩ` — they are equal, so the base
resistor is *dominating* and the rough form is useless. Lesson: check
`R_B/(β+1) ≪ R_E` before you use it.

### Q13. (Moderate) The base supply is stiff and `V_BE` falls by 10 mV (≈ 5 °C).
How much does `I_C` move in (a) fixed bias `R_B = 10 kΩ`, `β = 100`, versus
(b) emitter bias `R_B = 10 kΩ`, `R_E = 1 kΩ`, `β = 100`?
**Answer:** (a) `ΔI_C = +100 µA`; (b) `ΔI_C = +9.0 µA`. Emitter bias is ~11×
less sensitive.
**Method:** Both currents are `(V_BB − V_BE)` divided by a constant, so
`ΔI_C = (β/R_total)·ΔV_BE`.
(a) `I_C = β(V_BB−V_BE)/R_B` ⇒ `dI_C/dV_BE = −100/10 kΩ = −10 mA/V` ⇒
`ΔI_C = 10 mA/V × 10 mV = 100 µA`.
(b) `I_C = β(V_BB−V_BE)/(R_B+(β+1)R_E) = 100/(10 kΩ+101 kΩ) = 0.901 mA/V` ⇒
`ΔI_C = 9.0 µA`. The `R_E` feedback divides the sensitivity by
`(1 + (β+1)R_E/R_B) ≈ 11.1`.

### Q14. (Moderate) Emitter bias `V_BB = 2 V`, `R_B = 10 kΩ`, `R_E = 1 kΩ`.
Find `I_C` for `β = 50` and for `β = 200`. How much does the Q-point move?
**Answer:** `β = 50` → `I_C = 1.066 mA`; `β = 200` → `I_C = 1.232 mA`. Only a
15.6% spread for a 4× spread in β.
**Method:** `I_C = β(V_BB−V_BE)/(R_B+(β+1)R_E)`.
`β=50`: `50 × 1.3/(10 k + 51 k) = 65/61k = 1.066 mA`.
`β=200`: `200 × 1.3/(10 k + 201 k) = 260/211k = 1.232 mA`.
Ratio 1.232/1.066 = 1.156. Compare with Q18: fixed bias under the same β spread
moves by 4×. The `R_E` term `(β+1)R_E` cancels most of the β.

### Q15. (Moderate) Collector-to-base bias of Q8: find `I_C` and `V_CE`, and verify
with a second route.
**Answer:** `I_C = 3.1 mA`, `V_CE = 3.8 V`.
**Method:** `I_C = β·I_B = 100 × 31 µA = 3.1 mA`.
Route 1 (from the supply): `V_CE = V_CC − I_C·R_C = 10 − (3.1 mA)(2 kΩ) =
3.8 V`.
Route 2 (from the collector down through `R_B`): `V_CE = V_BE + I_B·R_B =
0.7 + (31 µA)(100 kΩ) = 0.7 + 3.1 = 3.8 V` ✓.
Route 2 works because `R_B` and the base-emitter junction sit in series between
collector and emitter. Getting the same number two ways is how you catch a sign
or factor slip. Region: `V_B = V_CE − I_B·R_B = 3.8 − 3.1 = 0.7 V`, and
`V_C = 3.8 V > 0.7 V` ⇒ active ✓.

### Q16. (Moderate) Compute the stability factor of the collector-to-base circuit
in Q15 and comment.
**Answer:** `S ≈ (1+β)R_C/(R_B+R_C) = 101 × 2k/102k = 1.98` — about 2, i.e. ~50×
better than the fixed-bias `S = 101`.
**Method:** `S = (1+β)·R_C/(R_B + R_C)`. Substitute: `101 × 2000/102000 = 1.98`.
Interpretation: an increase in `I_C` drops `V_C`, which drops `I_B` through
`R_B`, which pulls `I_C` back — negative feedback. The weakness: `R_B` hangs on
the collector, so for AC it loads the output (poor gain) — that is why
collector-to-base bias is a DC-analysis teaching example, not a design choice.

### Q17. (Moderate) Voltage divider `V_CC = 12 V`, `R1 = 100 kΩ`, `R2 = 22 kΩ`,
`R_C = 4 kΩ`, `R_E = 1 kΩ`, `β = 200`, `V_BE = 0.7 V`. Do the **exact**
analysis: `I_C`, `V_CE`.
**Answer:** `V_th = 2.164 V`, `R_th = 18.03 kΩ`, `I_B = 6.68 µA`,
`I_C = 1.337 mA`, `V_CE = 5.31 V` — active.
**Method:** Replace the divider by its Thevenin equivalent first:
`V_th = 12 × 22/122 = 2.164 V`, `R_th = 100k∥22k = 2.2M/122 = 18.03 kΩ`.
Then the base loop is identical to emitter bias:
`I_B = (V_th − V_BE)/(R_th + (β+1)R_E) = 1.464/(18.03 k + 201 k) = 1.464/219.03 k
= 6.68 µA`. `I_C = 200 × 6.68 µA = 1.337 mA`, `I_E = 1.343 mA`.
`V_C = 12 − (1.337 mA)(4 kΩ) = 12 − 5.347 = 6.653 V`; `V_CE = 6.653 − 1.343 =
5.31 V`. Region: `6.65 > 2.16 > 1.34` ✓.

### Q18. (Moderate) For Q17, what does the divider-rule approximation give, and
how big is the error?
**Answer:** Approximate `I_C = 1.464 mA` (and `V_CE = 4.68 V`); the exact value
1.337 mA is **9.5% lower**.
**Method:** `I_C ≈ (V_B − V_BE)/R_E = (2.164 − 0.7)/1 kΩ = 1.464 mA`;
`V_CE ≈ 12 − 1.464 × (4 k + 1 k) = 12 − 7.32 = 4.68 V`. Error
`(1.464 − 1.337)/1.337 = 9.5%`. Check the rule: `β·R_E = 200 kΩ` vs
`10·R2 = 220 kΩ` — it just fails, and the error is just under 10%. The 10% rule
is not a guess; it is precisely this statement.

### Q19. (Moderate) Voltage divider `V_CC = 10 V`, `R1 = 90 kΩ`, `R2 = 10 kΩ`,
`R_C = 2 kΩ`, `R_E = 1 kΩ`, `β = 100`. Exact `I_C` and `V_CE`.
**Answer:** `V_th = 1.0 V`, `R_th = 9 kΩ`, `I_B = 2.73 µA`, `I_C = 0.273 mA`,
`V_CE = 9.18 V` — active.
**Method:** `V_th = 10 × 10/100 = 1.0 V`; `R_th = 90k∥10k = 9 kΩ`.
`I_B = (1.0 − 0.7)/(9 k + 101 k) = 0.3/110 k = 2.727 µA`.
`I_C = 0.2727 mA`, `I_E = 0.2755 mA`, `V_E = 0.2755 V`,
`V_C = 10 − (0.2727 mA)(2 kΩ) = 10 − 0.545 = 9.455 V`,
`V_CE = 9.455 − 0.276 = 9.18 V`. The approximation gives 0.3 mA, ~10% high —
`β·R_E = 100 kΩ` equals `10·R2 = 100 kΩ` exactly, i.e. the rule is met *at its
boundary*, which is why the error is 10% and not 2%.

### Q20. (Moderate) Stability factor of the exact divider in Q19, compared with
fixed bias at the same β.
**Answer:** `S = (1+β)(R_th+R_E)/(R_th+(β+1)R_E) = 101 × 10k/110k = 9.18`.
Fixed bias would be 101 — this is **11× better**.
**Method:** `S = (1+β)·(R_th + R_E)/(R_th + (β+1)·R_E)`. Substitute
`R_th = 9 kΩ`, `R_E = 1 kΩ`, `β = 100`: `101 × 10000/(9000 + 101000) =
1010000/110000 = 9.18`. Read the formula as physics: `S` collapses toward 1 when
`(β+1)R_E ≫ R_th + R_E`, because then base-current error is a tiny fraction of
the emitter voltage. Make `R_E` bigger and `R_th` smaller and `S` falls.

### Q21. (Moderate) The Q17 circuit, but with `R_C = 10 kΩ`. Is the transistor
still active? If not, what is `I_C`?
**Answer:** No — it saturates. `I_C ≈ (12 − 0.2)/(10 kΩ + 1 kΩ) = 1.073 mA`
(the forced `β` is 172, not 200).
**Method:** First the *active* trial, using the Q17 numbers
(`V_th = 2.164 V`, `R_th = 18.03 kΩ`): `I_B = 6.68 µA`, so `I_C = 1.337 mA`
and `V_C = 12 − (1.337 mA)(10 kΩ) = −1.37 V`. A negative collector voltage is
impossible, and `V_C < V_E` proves the B-C junction is forward biased ⇒
**saturation**. Re-solve with the circuit, not the device, setting the current:
with `V_CE ≈ 0.2 V` both `R_C` and `R_E` are in the loop, so
`I_C ≈ I_E = (12 − 0.2)/11 kΩ = 1.073 mA`.

Now confirm saturation rather than assuming it — `I_B` *does* change, because
`V_BE` rises to ≈ 0.8 V: `I_B = (2.164 − 0.8)/(18.03 k + 201 k) = 6.23 µA`.
Two checks that agree:
- `β·I_B = 200 × 6.23 µA = 1.245 mA > 1.073 mA` — the device *could* pass more
  current than the circuit allows, so it is clamped in saturation.
- The base can supply what the circuit needs: `1.073 mA/201 = 5.34 µA < 6.23 µA` ✓

The forced `β` is `1.073 mA/6.23 µA ≈ 172` — a 14% drop, which is exactly the
"β collapses in saturation" effect of `06-BJT-Fundamentals.md`. The pattern
"check the region, then re-solve, then confirm" is non-negotiable.

### Q22. (Moderate) Design: `V_CC = 12 V`, divider `R1 = 20 kΩ`, `R2 = 10 kΩ`,
`R_E = 1 kΩ`, `β = 100`. Choose `R_C` so that `V_CE = 6 V = V_CC/2`.
**Answer:** `R_C ≈ 818 Ω`.
**Method:** Three steps.
1. `V_B = 12 × 10/30 = 4.0 V` ⇒ `V_E = 3.3 V` ⇒ `I_C ≈ I_E = 3.3 mA`.
2. `V_CE = V_CC − I_C(R_C + R_E)` ⇒ `6 = 12 − (3.3 mA)(R_C + 1 kΩ)` ⇒
   `R_C + 1 kΩ = 6/3.3 mA = 1.818 kΩ` ⇒ `R_C = 818 Ω`.
3. Verify: `I_C = 3.3 mA`, `V_C = 12 − (3.3 mA)(818 Ω) = 9.30 V > V_B = 4 V` ✓
   active, and `V_CE = 9.30 − 3.3 = 6.0 V` ✓.
Centering the Q-point at `V_CC/2` maximises the symmetric output swing — the
same idea as Q33 in `Practice-06-BJT-Fundamentals.md`.

### Q23. (Moderate) Write the DC load-line equation, intercepts and slope for the
Q17 circuit, and where does the Q-point sit?
**Answer:** `V_CE = 12 − I_C(5 kΩ)`; intercepts 12 V and 2.4 mA; slope
−0.2 mA/V; Q-point `(1.337 mA, 5.31 V)`, i.e. 56% of the way up the line.
**Method:** `V_CE = V_CC − I_C·R_C − I_E·R_E ≈ V_CC − I_C(R_C + R_E)`.
- `I_C = 0` ⇒ `V_CE = 12 V`.
- `V_CE = 0` ⇒ `I_C = 12/(4 k + 1 k) = 2.4 mA`.
- Slope `−1/5 kΩ = −0.2 mA/V`.
- Q = (1.337 mA, 5.31 V): fraction along = `1.337/2.4 = 0.557`. A Q-point above
  mid-line (it should be 0.5) means the design tolerates more signal toward
  saturation than toward cutoff.

### Q24. (Moderate) Emitter bias with `R_B = 10 kΩ`, `R_E = 1 kΩ`. Its stability
factor, and how does it compare with fixed bias at the same `R_E`?
**Answer:** `S ≈ 1 + R_E/R_B = 1 + 0.1 = 1.1` — better than fixed bias (`S = 101`)
but *worse* than the Q19 divider (`S = 9.18`).
**Method:** `S ≈ 1 + R_E/R_B`. Read it as "how much of the emitter-loop error
voltage lands on `R_B`". The rule of thumb: to improve stability, make `R_E`
**large** and `R_B` **small** — then `R_E/R_B → ∞` and `S` approaches 1. Note the
conflict with the Q12 lesson (a small `R_B` is what makes `I_B` large, so the
rough formula `I_C ≈ (V_B−V_BE)/R_E` needs `V_B` stiff, e.g. from a divider,
not from a small `R_B` and a weak `V_BB`).

### Q25. (GATE-level) Emitter bias with two supplies: `V_BB = 2 V`, `R_B = 100 kΩ`,
`R_E = 1 kΩ`, `R_C = 3 kΩ`, `V_CC = 10 V`, `β = 100`, `V_BE = 0.7 V`. Full DC
analysis, plus `S`.
**Answer:** `I_B = 6.47 µA`, `I_C = 0.647 mA`, `I_E = 0.653 mA`,
`V_E = 0.653 V`, `V_C = 8.06 V`, `V_CE = 7.41 V`, active, `S ≈ 1 + R_E/R_B = 1.01`.
**Method:** The order is fixed — see the concept box. Loop: `I_B = (V_BB−V_BE)/
(R_B + (β+1)R_E) = 1.3/201 k = 6.468 µA`. Multiply out, compute `V_E` and `V_C`
separately (do not use `I_C` for the `R_E` drop), then region-check, then `S`.
`S = 1 + R_E/R_B = 1 + 1/100 = 1.01` — 100× better than fixed bias. In
exams this circuit's stability is a gift: `R_E/R_B` is the whole answer.

### Q26. (GATE-level) Explain *why* collector-to-base bias is stable, and derive
its two `V_CE` expressions.
**Answer:** It is stable because an increase in `I_C` lowers `V_C`, which lowers
`V_B` through `R_B`, which lowers `I_B` and therefore `I_C` — negative feedback.
And `V_CE = V_CC − I_C·R_C = V_BE + I_B·R_B`.
**Method:** Write the loop: `V_CC = I_C·R_C + I_B·R_B + V_BE`. Since
`I_B = I_C/β`, the same `I_C` appears in both drops, so the circuit *contains its
own correction*. The second form comes from reading the loop from collector to
emitter through `R_B` and the base-emitter junction. Use whichever is more
convenient — but always sanity-check with the region test, since the feedback
stops working once `I_B` would need to go negative.

### Q27. (GATE-level) `V_CC = 12 V`, `R1 = 100 kΩ`, `R2 = 25 kΩ`, `R_C = 4 kΩ`,
`R_E = 1 kΩ`, `β = 200`. Both the approximate and the exact `I_C`, and the
percentage error. Is the approximation justified?
**Answer:** Approximate `I_C = 1.7 mA`; exact `I_C = 1.538 mA`; the
approximation is **10.5% high**. The rule `β·R_E ≥ 10·R2` fails
(`200 k < 250 k`), so do not quote 1.7 mA.
**Method:** Approximate: `V_B = 12 × 25/125 = 2.4 V`, `I_C ≈ (2.4−0.7)/1 kΩ =
1.7 mA`. Exact: `V_th = 2.4 V`, `R_th = 100k∥25k = 20 kΩ`,
`I_B = 1.7/(20 k + 201 k) = 1.7/221 k = 7.69 µA`, `I_C = 200 × 7.69 µA =
1.538 mA`. Error `0.162/1.538 = 10.5%`. The whole point: the shortcut is not a
different theory, it is the *same* equation with the base-loading term dropped —
so it is always approximately right and exactly right only in the limit.

### Q28. (GATE-level) Prove the "10% rule" numerically. `V_CC = 12 V`,
`R1 = 45 kΩ`, `R2 = 5 kΩ`, `R_E = 500 Ω`, `β = 100`. Compare
`I_C ≈ (V_B−V_BE)/R_E` with the exact value, and identify the small quantity
that the rule actually bounds.
**Answer:** `V_B = 1.0 V`, so `V_B − V_BE = 0.3 V`. Approximate `I_C = 0.600 mA`;
exact `I_C = 0.545 mA` — the approximation is **10.0% high**. The dropped term
is `I_B·R_th = 5.45 µA × 4.5 kΩ = 24.5 mV`, which is 8.2% of the 300 mV that
drives the current.
**Method:** `V_B = 12 × 5/50 = 1.0 V`. Approximate:
`I_C ≈ 0.3/500 = 0.6 mA`. Exact: `R_th = 45k∥5k = 4.5 kΩ`,
`I_B = 0.3/(4500 + 101 × 500) = 0.3/55 000 = 5.455 µA`, `I_C = 0.5455 mA`.
Error `0.0545/0.5455 = 10.0%`. The rule in one line: base current is
`I_B = I_C/β`, so it drops `I_B·R2 ≤ I_C·R2/β` across the divider. Requiring
that to be at most 10% of the `I_C·R_E` that sets the current gives
`R2 ≤ 10·β·R_E`, i.e. **`β·R_E ≥ 10·R2`**. Check: `100 × 500 = 50 kΩ` vs
`10 × 5 kΩ = 50 kΩ` — exactly at the boundary, and the error is exactly 10%.
The rule is not folklore; it *is* the statement "base-current loading of the
divider stays under 10% of the driving voltage".

### Q29. (GATE-level) Rank these four bias circuits by stability, all at `β = 100`,
and give the `S` for each: (a) fixed with `R_B = 10 kΩ`; (b) collector-to-base
with `R_C = 2 kΩ, R_B = 100 kΩ`; (c) emitter with `R_B = 10 kΩ, R_E = 1 kΩ`;
(d) divider with `R_th = 9 kΩ, R_E = 1 kΩ`.
**Answer:** (a) 101, (b) 1.98, (c) 1.1, (d) 9.18. Best to worst: (c) < (d) < (b)
< (a). Note (c) beats (d) here only because (d)'s divider is badly proportioned.
**Method:** (a) `1+β = 101`. (b) `(1+β)R_C/(R_B+R_C) = 101 × 2k/102k = 1.98`.
(c) `1 + R_E/R_B = 1 + 0.1 = 1.1`. (d) `(1+β)(R_th+R_E)/(R_th+(β+1)R_E) =
101 × 10k/110k = 9.18`.
**The lesson:** `S` is not a property of the circuit *name*, it is a property of
the numbers. (d) is worse than (c) only because its `R_th` is 9 kΩ against a
1 kΩ `R_E` — a badly proportioned divider that is not loading the base hard
enough. The single design lever is `β·R_E ≫ R_th + R_E`.

### Q30. (GATE-level) `I_CBO` grows from 1 µA to 10 µA (a ~10 °C rise). Compare
the resulting `I_C` error in (a) fixed bias `β = 100` and (b) a divider with
`R_th = 4.44 kΩ`, `R_E = 2 kΩ`, `β = 100`, both biased at `I_C ≈ 0.307 mA`.
**Answer:** (a) `ΔI_C = S·ΔI_CBO = 101 × 9 µA = 909 µA` — a ~296% error, i.e. the
device is destroyed. (b) `S = 3.15`, `ΔI_C = 28.4 µA` — 9.3%. The divider is
**32× better**.
**Method:** (a) `S = 1+β = 101`; `ΔI_CBO = 9 µA`; `ΔI_C = 101 × 9 = 909 µA`;
as a fraction of 0.307 mA that is 909/307 = 296% — far more than "drift", it is
a different operating point entirely.
(b) `S = (1+β)(R_th+R_E)/(R_th+(β+1)R_E) = 101 × 6.444k/(4.444k + 202k) =
650.8k/206.4k = 3.15`; `ΔI_C = 3.15 × 9 µA = 28.4 µA`; `28.4/307 = 9.3%`.
Ratio of the two errors: `909/28.4 = 32`. This is thermal runaway made
quantitative: with `S > 1/(1−something)` positive feedback starts, and `S = 1+β`
has no hope.

### Q31. (GATE-level) Design `R_B` for collector-to-base bias: `V_CC = 10 V`,
`R_C = 2 kΩ`, and you want `I_C = 2 mA` with `β = 100`. Then give `V_CE` and
comment on the Q-point.
**Answer:** `I_B = 20 µA`, so `(V_CC − V_BE) = I_B(R_B + βR_C) = 20 µA × (R_B +
200 kΩ)` ⇒ `R_B = 465 kΩ − 200 kΩ = 265 kΩ`. Then `V_CE = 10 − 4 = 6 V`.
**Method:** Rearrange the Q8 formula for `R_B`:
`R_B = (V_CC−V_BE)/I_B − β·R_C = 9.3/20 µA − 200 kΩ = 465 kΩ − 200 kΩ =
265 kΩ`. Verify: `I_B = 9.3/(265 k + 200 k) = 9.3/465 k = 20 µA` ✓, `I_C = 2 mA` ✓.
Comment: for maximum swing you want `I_C(Q) = V_CC/(2R_C) = 2.5 mA`, so 2 mA sits
slightly low and the usable swing is `I_C(Q)·R_C = 4 V` toward cutoff versus
`6 − 0.2 = 5.8 V` toward saturation. Also: a 265 kΩ `R_B` on the collector is a
terrible AC load, so this circuit is for DC biasing only.

### Q32. (GATE-level) A well-designed divider: `V_CC = 12 V`, `R1 = 40 kΩ`,
`R2 = 5 kΩ`, `R_E = 2 kΩ`. Find `I_C` for `β = 50` and `β = 200`, plus the
approximate value. How much of the original 4× β spread survives?
**Answer:** `V_B = 1.333 V`, `R_th = 4.444 kΩ`. `β = 50` → `I_C = 0.297 mA`;
`β = 200` → `I_C = 0.312 mA`; approximate `I_C = 0.317 mA`. Only a **4.7%**
spread survives (down from 4× in fixed bias).
**Method:** `V_th = 12 × 5/45 = 1.333 V`; `R_th = 40k∥5k = 4.444 kΩ`.
`I_B = (1.333 − 0.7)/(4444 + (β+1)·2000)`.
`β=50`: `0.6333/(4444 + 102000) = 0.6333/106444 = 5.950 µA` ⇒ `I_C = 0.2975 mA`.
`β=200`: `0.6333/(4444 + 402000) = 0.6333/406444 = 1.558 µA` ⇒ `I_C = 0.3116 mA`.
Ratio `0.3116/0.2975 = 1.047`. Sanity: the rule `β·R_E ≥ 10·R2` gives
`100 × 2 k = 200 k` vs `50 k` — comfortably satisfied, which is exactly why the
spread shrank from 4× to 1.05×.

### Q33. (GATE-level) A circuit is described as: "one resistor `R_C` from `V_CC` to
the collector, and one resistor `R_B` from the **collector** to the base; the
emitter is grounded." Name it, give its DC formula and its two main drawbacks.
**Answer:** Collector-to-base (voltage-feedback / self-bias) bias.
`I_B = (V_CC − V_BE)/(R_B + β·R_C)`, and `S ≈ (1+β)R_C/(R_B + R_C)` (typically
2–5). Drawbacks: (i) `R_B` loads the collector, so the AC gain drops and the
output impedance is degraded; (ii) the Q-point is still β-sensitive through
`β·R_C`, so it is only moderately stable.
**Method:** Recognition is by *where the feedback resistor attaches*. Base
resistor to the supply = fixed bias. Base resistor to the collector = negative
feedback. The AC drawback is the reason a designer reaches for a divider: you
cannot have a big `R_B` (needed for DC stability) and a light AC load at the
same time. The classic repair is a split collector resistor with a small
unbypassed part for HF feedback and a big bypassed part for DC.

### Q34. (GATE-level) Which single change improves stability most, and which
changes should you never make? Quantify with `S = (1+β)(R_th+R_E)/
(R_th + (β+1)R_E)`, `β = 100`, `R_E = 1 kΩ`.
**Answer:** Reduce `R_th` and increase `R_E`. `R_th = 9 kΩ` → `S = 9.18`;
`R_th = 4.5 kΩ` → `S = 5.27`; `R_th = 1 kΩ` → `S = 1.98`. Never reduce `R_E`
(that raises `S` and also destroys the Q-point by moving it toward saturation),
and never let `I_B` become a significant fraction of the divider current (you
would then have thrown away the whole point of the divider).
**Method:** Read the `S` formula: `S` falls as `(β+1)R_E` grows relative to
`R_th + R_E`. Since `β` is fixed by the process, the only handles are `R_E` (up)
and `R_th` (down, i.e. a lower divider impedance / heavier loading). The limit
`S → 1` requires `(β+1)R_E ≫ R_th + R_E`. But every one of these moves is paid
for elsewhere: bigger `R_E` eats headroom (`V_E` rises), smaller `R_th` wastes DC
current, and both eventually push the Q-point toward saturation — which is why
every real design ends with the Q33 loop: check the region *after* the bias is
designed.

---

## Trap box (exam-day killers)

- `V_CE = V_CC − I_C·R_C − I_E·R_E`. Dropping the `R_E` term is the single most
  common numerical error in biasing.
- Emitter-bias denominator is `R_B + (β+1)R_E` — **not** `β·R_E`.
- Divider shortcut is legal only when `β·R_E ≥ 10·R2`. The 10% error is a
  *consequence*, not a coincidence.
- `S = 1 + β` is for **fixed bias only**. Reusing it for the other three circuits
  is a guaranteed wrong answer.
- In saturation, the circuit sets `I_C`: `I_C ≈ (V_CC − 0.2)/(R_C + R_E)`.
- `I_C ≈ I_E` is an *approximation*; when you must find `I_E`, use `(β+1)I_B`.
- `V_B = V_CC·R2/(R1+R2)` uses the **bottom** resistor in the numerator. Check by
  asking: if `R2 → 0`, does `V_B → 0`? It must.
- Stability improves with **large `R_E`, small `R_th`** — not the other way round.

## Final recall drill (do in 60 seconds)

1. Fixed bias, `V_BB = 2 V`, `R_B = 100 kΩ` ⇒ `I_B`? → *13 µA.*
2. `S` for fixed bias at `β = 99`? → *100.*
3. Collector-to-base `I_B` formula? → *`(V_CC−V_BE)/(R_B+βR_C)`.*
4. `V_CC = 12`, `R1 = 100 kΩ`, `R2 = 25 kΩ` ⇒ `V_B`? → *2.4 V.*
5. `V_B = 2.4 V`, `R_E = 1 kΩ` ⇒ `I_C` (approx)? → *1.7 mA.*
6. When is the divider shortcut legal? → *`β·R_E ≥ 10·R2`.*
7. `R_th` of `100 kΩ ∥ 25 kΩ`? → *20 kΩ.*
8. Emitter bias `S` with `R_E = 1 kΩ`, `R_B = 10 kΩ`? → *≈ 1.1.*
9. Most stable bias circuit? → *voltage-divider with large `R_E`.*
10. Least stable? → *fixed bias (`S = 1+β`).*

---

Theory behind every answer: `07-BJT-Biasing.md`, `29-Formula-Sheet.md` §29.3,
`32-Single-File-Cheatsheet.md` §4.
