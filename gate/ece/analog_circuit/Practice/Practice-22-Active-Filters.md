# Active Filters — Practice (Learn by Solving)

> **The idea in one line:** filters are described by three numbers — **corner
> frequency `f_c`, roll-off slope (20 dB/dec per order), and `Q`** — and once
> you can read those three off any transfer function, every active-filter
> numerical reduces to arithmetic on `1/(2πRC)`.
>
> **How to use:** solve each question fully before reading the answer. Cover the
> **Answer**/**Method** with paper, do it, then reveal. If you miss one, solve
> the next 3 in the file to lock the pattern. No need to read the chapter notes
> first — every concept is taught through the drill itself. Open
> `22-Active-Filters.md` or `32-Single-File-Cheatsheet.md` only when you want
> the underlying theory.

## Concept box (what you must internalise)

- 1st order: `H_LPF = 1/(1 + jf/f_c)`, `H_HPF = (jf/f_c)/(1 + jf/f_c)`, `f_c = 1/(2πRC)`.
- **Roll-off = 20 dB/decade per pole.** 1st = 20, 2nd = 40, 3rd = 60, 4th = 80 dB/dec. 20 dB/dec = 6 dB/octave.
- Butterworth (maximally flat) ⇒ `Q = 1/√2 ≈ 0.707`. `Q > 0.707` ⇒ peaking; `Q < 0.707` ⇒ soft knee.
- Unity-gain **equal-R, equal-C Sallen-Key ⇒ `Q = 1/3`** (signature value). Gain Sallen-Key (equal R, C): **`Q = 1/(3−k)`**, and **`k → 3` ⇒ `Q → ∞` ⇒ oscillation**.
- Band-pass: `f_o = √(f_L f_H)`, `BW = f_H − f_L`, `Q = f_o/BW`. **Method:** `Q = f_o/BW` is a *band-pass-only* formula.
- Gain at `f_c` is `1/√2 = 0.707 = −3 dB` (not −6 dB). **Trap:** a cascaded pair of 1st-order sections at their shared corner gives **−6 dB**, which is why a single stage is not a good 2nd-order approximation.

---

## Questions

### Q1. (Easy) A 1st-order low-pass filter has `R = 10 kΩ` and `C = 10 nF`. Find `f_c`.
**Answer:** `f_c = 1/(2πRC) = 1/(2π × 10e3 × 10e-9) = 1/(6.283e-4) = **1.59 kHz**`.
**Method:** `RC = 10e3 × 10e-8 = 1e-4 s`; `f_c = 1/(2π × 1e-4) = 1591.5 Hz`. Memorise the ladder: `1 µs → 159 kHz`, `10 µs → 15.9 kHz`, `100 µs → 1.59 kHz`, `1 ms → 159 Hz`. Every corner-frequency numerical in the exam is one rung of that ladder.

### Q2. (Easy) A 1st-order high-pass filter has `R = 1.6 kΩ` and `C = 0.1 µF`. Find `f_c`.
**Answer:** `f_c = 1/(2π·R·C) = 1/(2π × 1.6e3 × 0.1e-6) = 1/(1.0053e-3) = `**995 Hz ≈ 1 kHz**`.
**Method:** `RC = 1.6e3 × 1e-7 = 1.6e-4 s = 160 µs`; `f_c = 1/(2π × 1.6e-4) = 994.7 Hz`. This is the standard AC-coupling high-pass: it blocks DC and passes everything above ~1 kHz. The LPF/HPF distinction changes the *circuit* (where the capacitor sits), never the arithmetic — the same `1/(2πRC)` serves both.

### Q3. (Easy) What is the gain of a 1st-order low-pass filter at exactly `f = f_c`? Give the ratio and the dB.
**Answer:** `1/√2 = `**0.707**, i.e. `20log₁₀(0.707) = `**−3.01 dB** (the “−3 dB point”).
**Method:** Substitute `f = f_c` into `|H| = 1/|1 + jf/f_c| = 1/√(1 + 1) = 0.707`. Remember: `20·log₁₀(0.7071) = −3.01 dB`. This is the **definition** of the cutoff, not a derived fact — that is why the number is 3 dB and not 6 dB.

### Q4. (Easy) Fill in the roll-off slope (dB/decade) for 1st, 2nd, 3rd and 4th order filters.
**Answer:** **20, 40, 60, 80 dB/dec** respectively (equivalently 6 dB/octave each, since every order adds one pole).
**Method:** `roll-off = 20·order dB/dec`. A 2nd-order LPF is 40 dB/dec, *not* 20 — the single most common filter slip. If a plot shows 40 dB/dec past the corner, there are two poles and the order is 2.

### Q5. (Easy) A filter's gain falls 80 dB per decade. How many poles does it have, and what kind is it?
**Answer:** `order = 80/20 = `**4 poles**, so a **4th-order low-pass** (if the gain is falling as frequency rises).
**Method:** Divide the measured slope by 20. Counting poles is also the fastest route to "how many op-amp/capacitor sections do I need?" — 4th order = four reactive elements, typically two cascaded 2nd-order sections.

### Q6. (Easy) What `Q` makes a low-pass response maximally flat, and what is that filter called?
**Answer:** `Q = 1/√2 ≈ `**0.707**, and the filter is a **Butterworth** (maximally flat magnitude, no passband ripple, peak gain exactly 1).
**Method:** `Q = 1/√2` from `29-Formula-Sheet.md` §29.9. Contrast: Bessel is maximally flat *phase*; Chebyshev trades ripple for a faster roll-off. For a 2nd-order Butterworth, the peak gain is 1 and it occurs at DC, so "flat" is literal.

### Q7. (Easy) A unity-gain (follower) Sallen-Key low-pass uses `R1 = R2 = R` and `C1 = C2 = C`. What are `Q` and `ω_o`?
**Answer:** **`Q = 1/3 ≈ 0.333`** and **`ω_o = 1/RC`**, so `f_o = 1/(2πRC)`.
**Method:** `Q = 1/3` is the *signature* of the equal-component unity Sallen-Key and is quoted in `22-Active-Filters.md` §22.4. Because `1/3 < 0.707`, it is over-damped: no peaking, a soft knee, but the full 40 dB/dec slope above `f_o`. If a GATE question says "unity-gain Sallen-Key, equal R and equal C", the answer is 1/3 — no calculation needed.

---

### Q8. (Easy) Which is the sharper filter, a 1st-order or a 2nd-order LPF? Quantify the difference at `2 f_c` and at `10 f_c`.
**Answer:** The **2nd-order**. At `2 f_c`: 1st order `1/√5 = 0.447` (−6.99 dB), 2nd order `1/√17 = 0.243` (−12.30 dB) — the 2nd order is **5.3 dB deeper**. At `10 f_c`: 1st order `1/√101 = 0.0995` (−20.04 dB), 2nd order `1/√(1+10⁴) = 0.0100` (−40.00 dB) — **19.96 dB deeper**, i.e. almost exactly one extra order's worth.
**Method:** `|H|_1st = 1/√(1+x²)` and `|H|_2nd = 1/√(1+x⁴)` with `x = f/f_c`, then subtract the two dB values. The gap grows with frequency and asymptotically settles at 20 dB per extra order — so "how much better is 2nd order?" is always "about one order better, i.e. 20 dB/dec, more".

### Q9. (Easy) "To make a low-pass, the capacitor goes …; to make a high-pass, the capacitor goes …". Complete the rule, and give the reason.
**Answer:** **LPF: capacitor in parallel** with the feedback element(s) (it shunts HF away / bypasses gain at HF). **HPF: capacitor in series** with the input path (it blocks DC and passes AC). Reason: `|Z_C| = 1/(ωC)` **falls** as frequency rises — a series element therefore passes HF (HPF) and a shunt element dumps HF to ground (LPF).
**Method:** Series element: impedance falls with `f` ⇒ HF gets through ⇒ **HPF**. Shunt element: low impedance at HF ⇒ HF is shorted away ⇒ **LPF**. Recognise the position of `C` in a circuit diagram and you can name the filter instantly, before touching any arithmetic.

### Q10. (Easy) A band-pass filter passes from `500 Hz` to `2 kHz`. Find `f_o`, `BW` and `Q`.
**Answer:** `BW = 2 − 0.5 = `**1.5 kHz**; `f_o = √(500 × 2000) = √1e6 = `**1 kHz**; `Q = f_o/BW = 1000/1500 = `**0.667**.
**Method:** `f_o` is the **geometric** mean, not the arithmetic mean (`1.25 kHz` would be wrong). `Q = 1000/1500 = 0.6667`. `Q < 1` means wideband, barely selective; to sharpen, narrow `BW` at fixed `f_o` — the whole point of `Q = f_o/BW` from `22-Active-Filters.md` §22.6.

### Q11. (Moderate) A 1st-order high-pass (`f_c = 1 kHz`) and a 1st-order low-pass (`f_c = 1 kHz`) are cascaded. Give the overall response at `100 Hz`, `1 kHz` and `10 kHz` in dB.
**Answer:** At `100 Hz` (0.1 f_c): LPF `1/√1.01 = 0.995`, HPF `0.1/√1.01 = 0.0995` ⇒ product **0.0990 (−20.1 dB)**. At `1 kHz`: `0.707 × 0.707 = `**0.500 (−6.02 dB)**. At `10 kHz`: `0.0995 × 0.995 = `**0.0990 (−20.1 dB)**. Perfectly symmetric band-pass.
**Method:** Multiply the two magnitudes, then one `20log₁₀` of the product. `|H_LPF| = 1/√(1+x²)`, `|H_HPF| = x/√(1+x²)`, `x = f/f_c`. The **−6 dB** centre (not −3 dB) is the key observation: **two 1st-order sections do not make a good 2nd-order band-pass.** To get a −3 dB centre you need a true 2nd-order (Sallen-Key) section per side, or a doubly-loaded resonator.

### Q12. (Moderate) That cascade is 2nd-order with `Q = f_o/BW`. Find its `Q`, and compare its centre attenuation with a 2nd-order **Butterworth** low-pass at the same frequency ratio.
**Answer:** With both corners at 1 kHz the band is degenerate (`f_L = f_H`), so take the realisable case HPF `500 Hz` + LPF `2 kHz`: `f_o = √(500×2000) = 1 kHz`, `BW = 1.5 kHz`, `Q = `**0.667**. At `f_o` that cascade gives **−6.02 dB**; a 2nd-order Butterworth low-pass at its own `f_o` gives `1/√2 = `**−3.01 dB**. The Butterworth is 3 dB "better" — because it concentrates both poles into one filter rather than splitting them into two.
**Method:** `Q = f_o/BW = 1000/1500 = 0.667`. Compare the centre gains: `2 × (−3 dB) = −6 dB` for two 1st-order sections versus `−3 dB` for one 2nd-order Butterworth section. The lesson from `22-Active-Filters.md` §22.2: cascading 1st-order sections gets you the *slope* (40 dB/dec) but not the *shape*.

### Q13. (Moderate) An **inverting** 1st-order LPF: `R1 = 1 kΩ` into the summing node, feedback `R2 ∥ C` with `R2 = 10 kΩ`, `C = 1 nF`. Find the passband gain, `f_c`, and the gain at `f_c`.
**Answer:** Passband gain = `−R2/R1 = `**−10**. `f_c = 1/(2πR2C) = 1/(2π × 1e4 × 1e-9) = `**15.9 kHz**. Gain at `f_c` = `10/√2 = `**7.07** (−3 dB relative to the passband).
**Method:** This is the Chapter-21 practical integrator seen as a low-pass: same circuit, but as soon as you call it a *filter* you care about `R2C` (the corner) and `R2/R1` (the passband gain) instead of about integration. `2π × 1e4 × 1e-9 = 6.283e-5`; `1/6.283e-5 = 15915 Hz` ✓. The in-band gain is negative, so this filter inverts as well as filters.

### Q14. (Moderate) A unity-gain Sallen-Key LPF with `R1 = R2 = 10 kΩ` and `C1 = C2 = 10 nF`. Find `f_o` and the roll-off, and say what the "knee" looks like.
**Answer:** `f_o = 1/(2πRC) = `**1.59 kHz**; roll-off = **40 dB/dec** above `f_o`. Because `Q = 1/3 < 0.707`, the magnitude is **monotonic** — no peak, a soft knee, and the response is essentially at 40 dB/dec by one decade above `f_o`.
**Method:** `f_o = 1/(2π × 10e3 × 10e-9) = 1/(6.283e-4) = 1591.5 Hz`. The `Q < 0.707` test gives you the shape: no overshoot, no ringing. Practical consequence: an equal-component Sallen-Key is a perfectly good anti-alias filter — you pay only in selectivity (`Q = 0.333`), not in stability.

### Q15. (Moderate) Using the **gain-Sallen-Key** relation `Q = 1/(3−k)` for equal R and equal C (`22-Active-Filters.md` §22.4), find `Q` for `k = 1.5`, `2`, `2.5` and `2.9`.
**Answer:** `k = 1.5 ⇒ Q = 1/1.5 = `**0.667**; `k = 2 ⇒ Q = 1/1 = `**1.0**; `k = 2.5 ⇒ Q = 1/0.5 = `**2.0**; `k = 2.9 ⇒ Q = 1/0.1 = `**10.0**.
**Method:** Just compute `3 − k` and invert — the whole table is `k = 2 + 1/Q`. `k` rising ⇒ `Q` rising ⇒ sharper knee but more peaking and less tolerance to component error. Keep the two anchor values from the chapter straight: **unity-gain equal-component Sallen-Key ⇒ `Q = 1/3`**, and **gain form ⇒ `Q = 1/(3−k)`**; they are two different Sallen-Key design conventions, so never mix a `k` from one with a `Q` from the other.

### Q16. (Moderate) Using `Q = 1/(3−k)`, what gain `k` gives a Butterworth (`Q = 0.707`)? What `k` gives `Q = 2`? Express both as op-amp resistor ratios.
**Answer:** `3 − k = 1/0.707 = √2 = 1.4142 ⇒ k = 3 − √2 = `**1.586**. For `Q = 2`: `3 − k = 0.5 ⇒ k = `**2.5**. As a non-inverting op-amp (`k = 1 + R_f/R1`): Butterworth needs `R_f/R1 = `**0.586** (e.g. `5.9 kΩ` over `10 kΩ` ⇒ `k = 1.59`, `Q = 1/1.41 = 0.709`); `Q = 2` needs `R_f/R1 = `**1.5** (`15 kΩ` over `10 kΩ`).
**Method:** Invert the relation: `k = 3 − 1/Q`. Butterworth: `1/0.7071 = 1.4142`, `3 − 1.4142 = 1.5858`. Q = 2: `1/2 = 0.5`, `3 − 0.5 = 2.5`. Then convert with the `+1`: `R_f/R1 = k − 1`. The `+1` is the classic slip — the inverting form `−R_f/R1` has no `+1`.

### Q17. (Moderate) A unity-gain Sallen-Key uses `R1 = R2 = 1 kΩ` and `C1 = C2 = 1 µF`. Find `f_o` and `Q`.
**Answer:** `f_o = 1/(2π × 1e3 × 1e-6) = `**159.2 Hz**, with `Q = 1/3`.
**Method:** `RC = 1e3 × 1e-6 = 1e-3 s` (1 ms) → `f_o = 1/(2π × 1e-3) = 159.15 Hz`. Frequency depends only on the **product** `RC`, so audio-rate filters need big `C` or big `R`; 1 µF electrolytics in a Sallen-Key bring leakage and tolerance problems. The exam only wants `159 Hz` and `Q = 1/3`.

### Q18. (Moderate) A 2nd-order Butterworth low-pass has `f_o = 1 kHz`. Compute `|H|` and the dB at `2 f_o` and at `3 f_o`.
**Answer:** `|H| = 1/√(1 + (f/f_o)⁴)`. At `2 f_o`: `1/√17 = `**0.2425** = **−12.30 dB**. At `3 f_o`: `3⁴ = 81`, `1/√82 = `**0.1104** = **−19.14 dB**.
**Method:** For order `N = 2` the magnitude² is `1/(1 + (f/f_c)⁴)` — the exponent is **2N = 4**, not 2. `20log₁₀(0.24254) = −12.30 dB`; `20log₁₀(0.11043) = −19.14 dB`. Compare the ideal 40 dB/dec asymptote: `40·log₁₀2 = 12.04 dB` and `40·log₁₀3 = 19.09 dB`. The real Butterworth sits just *below* the asymptote — that is what "maximally flat in the passband, then steep" means.

### Q19. (Moderate) Compute `|H|` at `2 f_c` for 1st, 2nd, 3rd and 4th order Butterworth filters.
**Answer:** 1st: `1/√(1+2²) = 1/√5 = `**0.4472** (**−6.99 dB**). 2nd: `1/√(1+2⁴) = 1/√17 = `**0.2425** (**−12.30 dB**). 3rd: `1/√(1+2⁶) = 1/√65 = `**0.1240** (**−18.13 dB**). 4th: `1/√(1+2⁸) = 1/√257 = `**0.0624** (**−24.10 dB**).
**Method:** `|H| = 1/√(1 + (f/f_c)^{2N})`; at `f = 2f_c` the exponent is `2N`. Check against the asymptotes `20N·log₁₀2 = 6.02N` dB ⇒ `6.02, 12.04, 18.06, 24.08`: the exact answers are always a hair *below* the asymptote (`6.99, 12.30, 18.13, 24.10`), converging to it as `N` grows. That near-agreement at 3rd/4th order is why exam solutions freely use the 20 dB/dec asymptote for high orders.

### Q20. (Moderate) What is the peak gain (and in dB) of a 2nd-order low-pass for `Q = 0.707`, `Q = 1` and `Q = 2`? At what frequency does the `Q = 2` peak occur?
**Answer:** `|H|_peak = Q²/√(Q² − 1/4)`. `Q = 0.707 ⇒ `**1.000** (0 dB, peak at DC). `Q = 1 ⇒ 1/√0.75 = `**1.1547** (**+1.25 dB**). `Q = 2 ⇒ 4/√3.75 = `**2.0656** (**+6.30 dB**). The `Q = 2` peak is at `f = 0.935 f_o`; the `Q = 0.707` peak is at `f = 0` (DC).
**Method:** A peak exists only for `Q > 1/√2`, and it sits at `f_pk = f_o√(1 − 1/(2Q²))`. For `Q = 2`: `√(1 − 1/8) = 0.9354`. For `Q = 0.707`: `1 − 1/(2×0.5) = 0` ⇒ peak at DC with gain 1, i.e. flat. Exam phrasing: "which Q gives peaking, and how much?" ⇒ `Q > 0.707`, peak gain `Q²/√(Q² − 0.25)`.

### Q21. (Moderate) Rank these by **steepness of the skirt**: (a) 1st-order LPF, (b) 2nd-order Butterworth LPF, (c) 2nd-order LPF with `Q = 2`, (d) 4th-order Butterworth. Then explain why `Q` does not appear in the ranking.
**Answer:** **(d) steepest (80 dB/dec)**, then (b) and (c) **tied at 40 dB/dec**, then (a) at 20 dB/dec. Order sets the asymptote; `Q` only bends the knee. At `10 f_c`, (b) gives `1/√(1+10⁴) = 0.0100` (**−40.00 dB**) and (c) gives `1/√((1−10²)² + (10/2)²) = 1/√9826 = 0.01009` (**−39.93 dB**) — the same to 0.07 dB, even though (c) peaked at `+6.3 dB` on the way there.
**Method:** For a 2nd-order section `|H| = 1/|1 − x² + jx/Q|`; at large `x` the `x²` term dominates regardless of `Q`, hence the identical slope. This is the most misunderstood point in filter questions: **`Q` shapes the knee, `order` shapes the skirt.** For band-passes the roles invert: there `Q = f_o/BW` *is* the selectivity measure.

### Q22. (Moderate) A 1st-order HPF has `f_c = 1 kHz`. Find `|H|` at `0.1 f_c` and at `10 f_c`.
**Answer:** `|H| = (f/f_c)/√(1+(f/f_c)²)`. At `0.1 f_c`: `0.1/√1.01 = `**0.0995** (−20.04 dB). At `10 f_c`: `10/√101 = `**0.9950** (−0.043 dB).
**Method:** The HPF form is `x/√(1+x²)`, the LPF form is `1/√(1+x²)` — same denominator, numerator `x` instead of 1. At `0.1 f_c` the HPF has already lost 20 dB; at `10 f_c` it is only 0.04 dB down, not 0. So "passes everything above `f_c`" is a *limit*, and for a cascade of several HPFs those small deficits add up (Q11).

### Q23. (Moderate) A 50 Hz mains-hum notch (twin-T, buffered) uses `R = 10 kΩ`. What `C` puts the notch at exactly 50 Hz?
**Answer:** `f_o = 1/(2πRC) ⇒ C = 1/(2π·R·f_o) = 1/(2π × 1e4 × 50) = `**318 nF**.
**Method:** Same `1/(2πRC)` as every corner — the notch frequency is a resonant frequency with infinite rejection at `f_o`. `2π × 1e4 × 50 = 3.1416e6`; `1/3.1416e6 = 3.183e-7 F = 318 nF`. Practical warning: to notch *exactly* 50 Hz you need a 1 % capacitor; 10 % parts put the notch anywhere in 50 ± 5 Hz and the hum is only partly removed. That is the "Q is adjustable, and sharp notches demand precision" point of `22-Active-Filters.md` §22.6.

### Q24. (GATE-level) Two 2nd-order Butterworth sections (each `Q = 0.707`, each `f_c = 1 kHz`) are cascaded. What is the combined order, roll-off, and gain at `2 kHz`?
**Answer:** Order **4**, roll-off **80 dB/dec**. Each section gives `−12.30 dB` at `2 f_c`, so the pair gives `−24.61 dB` (`|H| = 0.2425² = 0.0588`).
**Method:** Orders **add** in a cascade, and so do the dB (multiply the magnitudes). `0.24254 × 0.24254 = 0.05882`; `20log₁₀(0.05882) = −24.61 dB` = `2 × (−12.30)`. Compare a true single 4th-order Butterworth at the same point: `−24.10 dB` (Q19). The cascade of two Butterworths is 0.5 dB deeper — harmless, and a favourite "why is my filter not exactly right?" question.

### Q25. (GATE-level) Two 1st-order low-passes (`f_c = 1 kHz` each) are cascaded. At what frequency is the combination down 3 dB, and how far down is it at 1 kHz?
**Answer:** `|H| = [1/√(1+x²)]² = 1/(1+x²)`. Down 3 dB: `1/(1+x²) = 0.7071` ⇒ `1+x² = √2` ⇒ `x = √(√2 − 1) = `**0.6436**, so `f₃dB = `**644 Hz**, not 1 kHz. At `f = 1 kHz` the pair is `1/(1+1) = `**0.500 = −6.02 dB**, whereas a single 2nd-order Butterworth is only `−3.01 dB` there.
**Method:** `|H|` for the pair is `[1/√(1+x²)]²`. Set `= 0.7071` ⇒ `1+x² = √2 = 1.4142` ⇒ `x² = 0.4142` ⇒ `x = 0.6436`. At `x = 1`, `1/(1+1) = 0.5` ⇒ `20log₁₀(0.5) = −6.02 dB`. This is exactly why a 2nd-order filter is built from **Sallen-Key, not two cascaded RC sections**: the sections multiply their corner shapes, so the pair is 3 dB *too deep* at the nominal corner and its true corner is at `0.644 f_c`. Same root cause as Q11's −6 dB band-pass centre.

### Q26. (GATE-level) Where are the two poles of a 2nd-order Butterworth low-pass, expressed relative to `ω_o`? What `Q` does that geometry imply?
**Answer:** On a circle of radius `ω_o` in the left half-plane, symmetric about the real axis, at **135° and 225°**: `s = ω_o(−1/√2 ± j/√2) = ω_o(−0.7071 ± j0.7071)`. The real part magnitude is `0.7071 ω_o`, so `2ζ = 1.4142` and `Q = 1/(2ζ) = `**0.7071**.
**Method:** Butterworth poles lie on a circle, equally spaced, and **never** in the right half-plane (that would mean growing oscillation). General Butterworth pole angles: `θ_k = 90° + (2k+1)·180°/(2N)`. For `N = 2`: `90 + 45 = 135°`, `90 + 135 = 225°`. The geometry and the number `Q = 0.707` are the same fact, seen two ways — if a question gives you pole coordinates, read `Q = 1/(2|cos θ|)` off them.

### Q27. (GATE-level) What is the **phase** of a 1st-order LPF and a 1st-order HPF at their corner frequency? And of a 2nd-order low-pass at `f_o`?
**Answer:** 1st-order LPF at `f_c`: **−45°**. 1st-order HPF at `f_c`: **+45°**. 2nd-order low-pass at `f = f_o`: **exactly −90°** — for *any* `Q`. (At `Q = 0.707` the gain there is 0.707; at `Q = 1` the gain is exactly 1.)
**Method:** `∠H_LPF = −tan⁻¹(f/f_c)`; `∠H_HPF = 90° − tan⁻¹(f/f_c)`. For 2nd order, `H = 1/(1 − (f/f_o)² + j(f/f_o)/Q)`: at `f = f_o` the real part of the denominator is zero, so the denominator is purely imaginary and the phase is **−90° regardless of Q**. Why it matters: "two poles ⇒ 180° of phase available" is what lets a 2nd-order section supply the extra 90° a feedback loop needs to oscillate (see `25-Oscillators.md`).

---

### Q28. (GATE-level) Design a 1st-order low-pass with `f_c = 10 kHz` using `R = 10 kΩ`. Find `C`, and the gain at `2 f_c`.
**Answer:** `C = 1/(2π·R·f_c) = 1/(2π × 1e4 × 1e4) = `**1.59 nF** (use 1.6 nF). At `2 f_c`: `|H| = 1/√5 = `**0.4472** = **−6.99 dB**, versus the 20 dB/dec asymptote's `−6.02 dB`.
**Method:** `C = 1/(2πRf_c)`: `2π × 1e4 × 1e4 = 6.283e8`; `1/6.283e8 = 1.5915e-9 F = 1.59 nF`. Then `1/√(1+4) = 0.4472`, `20log₁₀(0.4472) = −6.99 dB`. Note the exact response is ~1 dB *deeper* than the asymptote at the first octave — a useful sanity check against a sketch.

### Q29. (GATE-level) Using `Q = 1/(3−k)`, find `k` for `Q = 0.5`, `Q = 1` and `Q = 10`; say which is *usable*, and what happens at `k = 3`.
**Answer:** `k = 3 − 1/Q`: `Q = 0.5 ⇒ k = `**1.0**; `Q = 1 ⇒ k = `**2.0**; `Q = 10 ⇒ k = `**2.90**. All are nominally realisable, but `Q = 10` peaks at `f_o√(1 − 1/200) = 0.998 f_o` with `|H|_pk = 100/√99.75 = `**10.01 (+20.0 dB)** — impractical, because component error then moves the poles a lot. At **`k = 3`**: `Q → ∞`, the poles reach the imaginary axis, and the Sallen-Key **oscillates** instead of filtering.
**Method:** `k = 3 − 1/Q` — three one-line substitutions. The engineering judgement: high `Q` needs precision parts, and ringing is usually worse than no ringing. The `k → 3 ⇒ oscillation` fact is the favourite one-mark MCQ of `22-Active-Filters.md` §22.4 — remember it as *"the amplifier's gain makes the poles real-part-zero at k = 3"*, not as a numerical result.

### Q30. (GATE-level) Four circuits are described. Name each filter and give its far-stopband roll-off: (a) `C` in series with the input of an op-amp; (b) `C ∥ R` in the feedback of an inverting amp; (c) a series HPF followed by a shunt LPF; (d) a twin-T network buffered by a follower.
**Answer:** (a) **1st-order HPF, 20 dB/dec** (rising edge, flat above). (b) **1st-order LPF, 20 dB/dec** (this is the practical integrator of Chapter 21). (c) **Band-pass, 20 dB/dec per side ⇒ 40 dB/dec in each far stopband** (Q24). (d) **Notch / band-stop** at `f_o = 1/(2πRC)`, with skirts of 20 or 40 dB/dec depending on how many poles the op-amp section adds.
**Method:** Identify by *component position*, never by appearance (Q9): shunt `C` ⇒ LPF, series `C` ⇒ HPF, both ⇒ BPF, twin-T ⇒ notch. Stopband slopes **add** in a cascade. Each of these four, plus a "summing of the two" band-stop, is the standard menu for a "identify the filter" MCQ.

### Q31. (GATE-level) A 2nd-order Sallen-Key low-pass has `f_o = 10 kHz`. What op-amp **GBW** is needed, and what goes wrong with a slower one?
**Answer:** Rule of thumb: **GBW ≳ 100·f_o = 1 MHz**. With a 100 kHz op-amp the amplifier is no longer a flat-gain follower inside the filter band: the passband stops being flat, the loop picks up extra phase lag, and the closed-loop `f_o` drifts downward — the response degenerates toward first order and becomes oscillation-prone.
**Method:** The op-amp must look like an ideal follower across the whole filter band, and that needs `GBW ≫ f_max`; 100× is the standard safety factor. This is the "active filter cost" caveat in `22-Active-Filters.md` §22.7. For `f_o = 10 kHz`, pick a ≥1 MHz GBW part (TL081/TL071/OP07 class). Corollary: an active filter is a poor choice at tens of MHz — use a passive LC or a switched-cap filter instead.

### Q32. (GATE-level) A 4th-order Butterworth low-pass is built as two 2nd-order sections. What are the two section `Q` values, and what does each do to the response?
**Answer:** **`Q₁ = 1/(2cos22.5°) = 0.5412` and `Q₂ = 1/(2cos67.5°) = 1.3066`**, with `Q₁·Q₂ = 0.7071 = 1/√2`. `Q₁ < 0.707` ⇒ no peak, a gentle section. `Q₂ > 0.707` ⇒ a real peak of `Q₂²/√(Q₂²−0.25) = 1.7071/√1.4571 = `**1.414 (+3.01 dB)** at `f = 0.841 f_o`, plus a matching dip from `Q₁`. The two cancel, leaving the flat 4th-order magnitude.
**Method:** 4th-order Butterworth poles sit at `112.5°, 157.5°, 202.5°, 247.5°`; each conjugate pair is one 2nd-order section and `Q = 1/(2|cos θ|)`. Pair at `112.5°`: `|cos| = 0.38268` ⇒ `Q = 1.3066`. Pair at `157.5°`: `|cos| = 0.92388` ⇒ `Q = 0.5412`. The intermediate `+3 dB` peak is genuine — you can measure it with a sweep, which is why a single-section "cheat" (two identical Butterworths, Q24) is only 0.5 dB different and is usually preferred in practice.

### Q33. (GATE-level) Full design: a **2nd-order Butterworth LPF at `f_o = 10 kHz`** as a Sallen-Key with equal R and equal C. Give `C`, the required amplifier gain `k`, and the op-amp resistor ratio.
**Answer:** Equal R, equal C ⇒ `f_o = 1/(2πRC)`. Choose `R = 10 kΩ` ⇒ `C = 1/(2π × 1e4 × 1e4) = `**1.59 nF** (use 1.6 nF). Butterworth needs `Q = 0.707 = 1/(3−k)` ⇒ `k = 3 − √2 = `**1.586**. Non-inverting: `k = 1 + R_f/R1` ⇒ `R_f/R1 = 0.586`; pick `R1 = 10 kΩ`, `R_f = 5.9 kΩ` ⇒ `k = 1.59`, `Q = 1/1.41 = 0.709` (0.3 % high). **The gain stage is not optional:** a *unity-gain* Sallen-Key cannot reach Butterworth in any component ratio.
**Method:** Three one-line sub-answers. (1) `C = 1/(2πRf_o)`; (2) `k = 3 − 1/Q`; (3) `R_f/R1 = k − 1` — do not forget the `+1`. The last note is the exam point: a unity-gain Sallen-Key gives `Q = 1/3` with equal parts, and maximising `Q = √(R1R2C1C2)/(R1C1 + R1C2 + R2C2)` over all component ratios still caps it at `Q = 1/2`, short of 0.707. So **every practical 2nd-order Butterworth Sallen-Key carries gain `k ≈ 1.59`.**

---

## Trap box (exam-day killers)

- **Wrong corner resistor.** In the inverting 1st-order LPF the corner is `1/(2π·R2·C)` — the *feedback* resistor, not `R1`.
- **−3 dB, not −6 dB, at `f_c`.** `−6 dB` is what *two* 1st-order sections give (Q11, Q25) — that is why a 2nd-order filter is not two RC sections.
- **Roll-off is 20 dB/dec per pole.** 2nd order is 40 dB/dec. Q > 0.707 does **not** make the skirt steeper.
- **`Q = f_o/BW` is a band-pass-only formula.** Applying it to an LPF is meaningless; there `Q` is knee sharpness only.
- **Butterworth means `Q = 0.707`**, i.e. maximally flat, *not* "the sharpest filter". Chebyshev is the sharp one (and ripples).
- **`f_o` of a band-pass is the geometric mean** `√(f_L f_H)`, not the arithmetic mean.
- **Mixing the two Sallen-Key Q relations.** Unity + equal R,C ⇒ `Q = 1/3`; gain form ⇒ `Q = 1/(3−k)`. Take a `k` from one and a `Q` from the other and you get nonsense.
- **Butterworth exponent is `2N`,** not 2: order `N` gives `|H| = 1/√(1 + (f/f_c)^{2N})`. Forgetting this doubles the roll-off.
- **Ignoring the op-amp's GBW.** An "active" filter with a slow op-amp is not a filter at all — it droops and can oscillate (Q31).
- **`f_c` is not `1/RC`.** It is `1/(2πRC)`. A missing `2π` is a 6.28× error and the classic last-minute slip.

## Final recall drill (do in 60 seconds)

1. `R = 10 kΩ`, `C = 10 nF`, 1st-order corner → 1.59 kHz.
2. Gain at `f_c` of a 1st-order LPF → 0.707 = −3 dB.
3. Roll-off for 1st / 2nd / 3rd order → 20 / 40 / 60 dB/dec.
4. Butterworth `Q` → 0.707. Sallen-Key equal R,C unity `Q` → 1/3.
5. `Q = 1/(3−k)` with `k = 2` → Q = 1. With `k = 2.5` → Q = 2. At `k = 3` → oscillation.
6. Band-pass `f_L = 500 Hz`, `f_H = 2 kHz` ⇒ `f_o` = 1 kHz, `BW` = 1.5 kHz, `Q` = 0.667.
7. 2nd-order Butterworth at `2 f_c` → 0.243 = −12.3 dB.
8. LPF ⇒ capacitor in **parallel**; HPF ⇒ capacitor in **series**.
9. 4th-order Butterworth pole-pair Qs → 0.5412 and 1.3066.
10. Peak gain of a 2nd-order LPF with `Q = 2` → 2.07 (+6.3 dB) at `0.935 f_o`.
11. 20 dB/dec equals how many dB/oct? → 6 dB/oct.
12. `Q > 0.707` ⇒ peaking. `Q < 0.707` ⇒ soft knee. `Q = 0.707` ⇒ flat.

---
