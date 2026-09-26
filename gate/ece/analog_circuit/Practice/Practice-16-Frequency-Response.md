# Frequency Response — Practice (Learn by Solving)

> **The idea in one line:** learn low-frequency (coupling/bypass) and high-frequency
> (Miller) behaviour of amplifiers by solving — pole positions, −3 dB points,
> bandwidth vs gain trade, multi-stage rules.
>
> **How to use:** solve each before revealing. Theory in `` `16-Frequency-Response.md` ``.

## Concept box (what you must internalise)

- Coupling/bypass caps → high-pass poles: `f = 1/(2π·C·R_eq)`
  - Bypass: `R_eq ≈ re + R_B/(β+1)` (BJT) — NOT R_E directly
  - Coupling: R_eq is the Thevenin R looking into the cap
- Miller (inverting only): `C_in_M = C·(1+|A|)`, `C_out_M = C·(1+1/|A|)`
- High cutoff: `f_H = 1/(2π·R_eff·C_total)`
- GBW ≈ const: gain × bandwidth preserved with feedback
- N identical stages: `f_H,tot = f_H·√(2^(1/N) − 1)`

---

## Questions

### Q1. (Easy) Coupling cap `C=1 µF`, `R_eq=2 kΩ`. Lower pole?
**Answer:** `1/(2π·1µ·2k) = 1/(2π·2m) ≈ 79.6 Hz`.
**Method:** f = 1/(2πRC).

### Q2. (Easy) The −3 dB point equals what in terms of the pole frequency?
**Answer:** exactly the pole: `|H|=1/√2` at ω=ω_p.
**Method:** pole frequency = corner frequency.

### Q3. (Easy) Which class of response do coupling/bypass caps give (low or high cut)?
**Answer:** High-pass (low-frequency cut).
**Method:** caps block DC/AC at low f; series C = HPF.

### Q4. (Easy) Frequency where a 20 dB/dec roll-off has dropped 20 dB?
**Answer:** one decade up from the corner (f = 10·f_c).
**Method:** −20 dB/dec means 20 dB per 10×.

### Q5. (Moderate) BJT bypass cap: `C_E=10 µF`, `re=25 Ω`, R_B/(β+1) with R_B=2k, β=99 → R_B/(β+1)=20 Ω. R_eq, f_p?
**Answer:** `R_eq = 25 + 20 = 45 Ω`; `f_p = 1/(2π·10µ·45) ≈ 354 Hz`.
**Method:** remember R_eq is re + (source∥bias)/β; NOT R_E.

### Q6. (Moderate) Same but R_E=1k bypassed cap: does the pole use R_E?
**Answer:** No — the bypass path replaces R_E with the small re+... impedance; using 1k would drop the pole by 20×.
**Method:** the classic trap.

### Q7. (Moderate) CS (MOS): source bypass C_S with R_eq = 1/gm ∥ ...? give a number gm=2m, R_eq=0.5k, C=10µ.
**Answer:** f = 1/(2π·10µ·500) = 31.8 Hz.
**Method:** MOSFET bypass sees ~1/gm.

### Q8. (Moderate) Upper cutoff with `C_in_total=15 pF`, `R_s+... R_eff=1 kΩ`.
**Answer:** `f_H = 1/(2π·1k·15p) ≈ 10.6 MHz`.
**Method:** f_H = 1/(2π R_eff C_total).

### Q9. (GATE-level) Miller: CS with C_gd=2 pF, gain |A|=50, input R_s=1k (no other caps). C_in_M, f_H?
**Answer:** `C_in_M = 2p·(1+50) = 102 pF`; `f_H = 1/(2π·1k·102p) ≈ 1.56 MHz`.
**Method:** Miller multiplies the fed-back capacitor by (1+|A|).

### Q10. (GATE-level) CE: same numbers (C_cb=2 pF, |A|=50, R_s=1k): same result?
**Answer:** yes ~1.56 MHz — BJT/MOS inversion both suffer Miller.
**Method:** Miller applies to any inverting amplifier.

### Q11. (Moderate) Which amplifier config avoids the Miller penalty entirely?
**Answer:** CG/CC (non-inverting or unidirectional); cascode reduces it in CS/CE.
**Method:** non-inverting stage ⇒ no Miller multiplication.

### Q12. (GATE-level) The cascode removes Miller because…
**Answer:** the CG transistor pins the drain of the CS at a low-impedance node, so gain of the first device ≈ small, and C_gd1 isn't amplified.
**Method:** virtual ground at the middle node.

### Q13. (Moderate) Gain–bandwidth: midband gain 40, BW 1 MHz. If gain must drop to 10 (feedback):
**Answer:** BW rises to `40·1M/10 = 4 MHz`.
**Method:** A·f = const.

### Q14. (GATE-level) If you DOUBLE the miller cap of a CS with R_s=1k: f_H changes?
**Answer:** halves (R_eff fixed, C doubles).
**Method:** f_H ∝ 1/C.

### Q15. (GATE-level) Multi-stage: two identical stages each f_H=2 MHz. Combined f_H?
**Answer:** `2M·√(√2 − 1) = 2M·0.6436 = 1.287 MHz`.
**Method:** √(2^(1/N)−1).

### Q16. (GATE-level) Three identical stages, each f_H=2 MHz: combined?
**Answer:** `2M·√(2^(1/3)−1) = 2M·√0.26 = 2M·0.5098 = 1.02 MHz`.
**Method:** N=3→0.5098×.

### Q17. (Moderate) What sets the low-frequency −3 dB of an amplifier typically?
**Answer:** largest of the coupling/bypass pole frequencies dominates.
**Method:** the biggest f_L wins.

### Q18. (GATE-level) Coupling cap between two stages: R_eq is?
**Answer:** output resistance of stage1 in series/∥ with input resistance of stage2. For CE: `R_out1 + R_in2` view — for series cap the pole uses (R_out1 + R_in2) (or whatever the current path sees).
**Method:** redraw at the capacitor and Thévenize.

### Q19. (Moderate) A cap charges with τ=RC; voltage reaches ~95% of the target in?
**Answer:** 3τ (95% actually at 3τ: e^{-3}=0.0498).
**Method:** settle times used in transient vs pole discussions.

### Q20. (GATE-level) The −3 dB high freq total with input Miller AND C_gs/c_js: combine?
**Answer:** add all caps at input node: `C_total = C_M + C_gs(+...)`, then f_H.
**Method:** parallel input caps sum.

### Q21. (GATE-level) Feedback: open-loop BW 100 Hz, closed gain factor 100... closed BW?
**Answer:** `100·100/1? careful: A_f=A/(1+Aβ)`. If 40 dB loop gain (100×), A_f reduces by 100, BW×100 → 10 kHz.
**Method:** BW_cl ≈ BW_ol·(1+Aβ).

### Q22. (Moderate) Does the emitter/source bypass RC affect the high or low cut?
**Answer:** Low cut (high-pass pole at f_LE).
**Method:** bypass only affects the low end.

### Q23. (GATE-level) Why does unbypassing R_E/R_S improve bandwidth in wideband designs?
**Answer:** replaces the midband gain with a large part of the roll-off? — no: removes the bypass low-f pole and lowers high-f gain (less Miller).
**Method:** two books: (1) low-f pole gone (or moved down); (2) if midband gain falls, Miller shrinks ↔ bandwidth rises.

### Q24. (GATE-level) A CS with bypass: low-f pole of C_S at 35 Hz; without bypass none at 35 Hz — true/false?
**Answer:** True-ish: the bypass *introduces* a pole near f=1/(2πC_S·R_eq); removing C_S removes that pole (gain drops, wide-band).
**Method:** bypass trades bandwidth for gain.

### Q25. (Moderate) What "bandwidth" measure does GATE want in a spectrum graph?
**Answer:** the −3 dB points: `BW = f_H − f_L` (leading to f_L≪f_H → BW≈f_H).
**Method:** read corners from the flat-top ±3 dB.

### Q26. (GATE-level) Relate `f_T` (unity-gain frequency) to GBW for CE/CS.
**Answer:** `f_T = gm/(2π·(C_π+C_µ))` for BJT; CS analog: gm/(2π(C_gs+C_gd)). The f where |A|=1.
**Method:** f_T ≈ GBW of the single stage.

### Q27. (GATE-level) If f_T=100 MHz and midband gain is 50 (first order): actual f_H?
**Answer:** `f_H = f_T/A = 2 MHz`.
**Method:** single-pole: H_f = f_T/A_mid.

### Q28. (GATE-level) A CS with `C_gd=1 pF`, gain=−20, source R=50Ω, extra C_gs=5p. C_input, f_H?
**Answer:** C_M=1p·(1+20)=21 pF; C_tot=21+5=26 pF; `f_H = 1/(2π·50·26p) = 122 MHz`.
**Method:** R_eff·C_tot = output corner for the source side.

### Q29. (Moderate) Name the three "BJT/MOS coupling" caps of a typical two-stage amp.
**Answer:** C1 (input), C2 (interstage), C3? (output load), plus C_E/C_S bypass.
**Method:** each series cap → its own pole.

### Q30. (GATE-level) If the bypass cap is chosen too small, what becomes the dominant low-frequency break?
**Answer:** the bypass pole rises toward midband and dominates f_L — recheck for bypass corner vs coupling corners.
**Method:** follow the largest corner.

---

## Trap box (exam-day killers)

- Bypass pole R_eq uses `re + R_B/(β+1)` (or `1/gm` for MOS), never R_E.
- Miller only for inverting; cascode ~removes it.
- Multi-stage f_H shrinks by √(2^(1/N)−1); don't just take the min.
- GBW constant ⇒ lower gain = wider BW.
- Big coupling cap = big τ = low pole; tiny = high pole into band.

## Final recall drill (do in 60 seconds)

1. Low pole → `1/(2π C R_eq)`
2. Miller in → `C(1+|A|)`
3. f_H → `1/(2π R_eff C_tot)`
4. N stages → `f_H√(2^(1/N)−1)`
5. Bypass R_eq → `re + R_B/(β+1)`

---