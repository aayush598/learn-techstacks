# MOSFET Small-Signal Model — Practice (Learn by Solving)

> **The idea in one line:** convert any MOSFET operating point into gm, r_o, g_mb,
> and redraw amplifiers with the small-signal model — learn through questions.
>
> **How to use:** solve, then reveal. Theory in `` `13-MOSFET-Small-Signal-Model.md` ``.

## Concept box (what you must internalise)

- `gm = k(V_GS − V_th) = 2I_D/V_ov = √(2k·I_D)` — all three forms
- `r_o = 1/(λ·I_D)` (or `V_A/I_D`)
- `g_mb = η·gm`, η ≈ 0.1–0.3 (body effect transconductance)
- Gate input resistance = ∞; drain current source `gm·v_gs` from D to S.
- `r_gs` infinite; `C_gs`/`C_gd` appear only at RF.
- Redraw: gate open, drain taps `gm·v_gs` current source and r_o to source.

---

## Questions

### Q1. (Easy) `I_D = 1 mA`, `V_ov = 0.5 V`, λ=0. gm?
**Answer:** `2·1m/0.5 = 4 mA/V`.
**Method:** `gm = 2I_D/V_ov`.

### Q2. (Easy) `k=1 mA/V²`, V_ov=1 V. gm?
**Answer:** `1·1 = 1 mA/V` (k·V_ov), also `2I_D/V_ov` with I_D=0.5 mA ✓.
**Method:** any of the three forms; check agreement.

### Q3. (Easy) `λ=0.02`, I_D=1 mA. r_o?
**Answer:** `1/(0.02·1m) = 50 kΩ`.
**Method:** r_o=1/(λI_D).

### Q4. (Moderate) `I_D=0.25 mA`, k=1, V_th=1 (saturation). gm via √(2kI_D)?
**Answer:** V_ov=√(2I_D/k)=√0.5=0.707; gm=√(2·1·0.25m)=0.707 mA/V. Also 2I_D/V_ov = 0.5m/0.707 = 0.707m ✓.
**Method:** gm depends only on I_D and k (not V_th): `√(2kI_D)`.

### Q5. (Moderate) Doubling I_D (λ=0, same device): how does gm change?
**Answer:** ×√2 (gm ∝ √I_D).
**Method:** in saturation gm ∝ √I_D, not linear (BJT was linear in I_C).

### Q6. (Moderate) At fixed V_ov, doubling W/L: gm change?
**Answer:** k doubles → gm = k·V_ov doubles.
**Method:** process+geometry scalings: gm ∝ W/L at fixed V_ov, ∝ √(W/L) at fixed I_D.

### Q7. (Moderate) Draw what replaces the MOSFET in small-signal midband (λ≠0).
**Answer:** between D and S a current source `gm·v_gs` and parallel r_o; gate open.
**Method:** no resistors at gate (infinite); source is the reference node for v_gs.

### Q8. (Moderate) What does body transconductance g_mb do?
**Answer:** adds `g_mb·v_bs` current term — a second dependent source to ground from source if body grounded.
**Method:** only if `v_bs ≠ 0` (source not tied to body). Often the source is the body = eliminated.

### Q9. (Moderate) Identify the AC model of a common-source stage with R_D and load R_L, λ≠0.
**Answer:** v_gs between G and S; `gm·v_gs` from D to S∥r_o; output node D with R_D∥R_L∥r_o to ground.
**Method:** redraw by replacing device, then combine parallels at each node.

### Q10. (GATE-level) CS gain with `gm=2 mA/V`, R_D∥R_L=2 k, r_o=50 k (parallel), λ gives r_o.
**Answer:** `−gm·(2k∥50k) = −2m·1.923k = −3.85`.
**Method:** combine every parallel path into one R_eff first.

### Q11. (GATE-level) Body effect in CS: source tied to body? v_bs?
**Answer:** v_bs=0 ⇒ g_mb inactive. If source separated from body (isolated well), v_bs=−v_s, adds g_mb term.
**Method:** check connection: grounded body kills the term.

### Q12. (Moderate) Gate node small-signal current from the model: value?
**Answer:** 0 (open) — infinite input resistance.
**Method:** use this to claim R_in = R_G (divider) with no loading.

### Q13. (Moderate) `gm=1 mA/V`, `r_o=100 kΩ`. The small-signal "µ" (gm·r_o)?
**Answer:** `100` — the intrinsic gain of a saturated MOS.
**Method:** gm·r_o = the max voltage gain of a single device.

### Q14. (GATE-level) CS with ideal current-source load (R_L=∞): gain?
**Answer:** `−gm·r_o = −100` (for Q13).
**Method:** the active/current-source load reaches gm·r_o — the "universal" MOS limit.

### Q15. (GATE-level) `k=2 mA/V²`, I_D=0.5 mA, r_o given by λ=0.04. gm, r_o?
**Answer:** gm=√(2·2m·0.5m)=1.414 mA/V; r_o=1/(0.04·0.5m)=50 kΩ.
**Method:** compute gm from √(2kI_D); r_o from λ.

### Q16. (GATE-level) g_mb = η gm with η=0.2: if body shared with source, the extra current source?
**Answer:** not present. If body tied to a separate node v_bs ≠ 0, output has an extra `g_mb·(v_s?)` path.
**Method:** model g_mb only when v_bs is nonzero.

### Q17. (Moderate) Is `r_gs` finite in the midband model?
**Answer:** No — gate junction is a capacitor, DC-isolated.
**Method:** memory hook: BJT has r_π, MOS has none.

### Q18. (GATE-level) Source follower: model and gain with `gm=2m, R_S=1k, r_o=50k`.
**Answer:** gain = `(R_S∥r_o · gm)/(1+gm(R_S∥r_o))` = `(1k∥50k)=0.9804k; 2m·0.9804k=1.961; /(1+1.961)=0.6624`.
**Method:** source follower: output at source; feedback factor = gm·R_eq.

### Q19. (GATE-level) CS gain sign and g_mb polarity check.
**Answer:** negative (inverting); g_mb adds source-current, lowering gain when present.
**Method:** inverting stage; body boosts equivalent gm if source is not body-tied.

### Q20. (Moderate) If gate and drain are tied (diode-connected) what is equivalent small-signal resistance?
**Answer:** `1/gm ∥ r_o ≈ 1/gm`.
**Method:** v_gs = v_gs = v_d → current gm·v_gs means a conductance gm at V: R_eq = 1/gm.

### Q21. (GATE-level) Use a diode-connected load in a CS amplifier: gain?
**Answer:** `−gm1/(gm2)` (ratio of transconductances).
**Method:** load R_eq=1/gm2; A_v=−gm1/gm2. A process-independent ratio (if same k) — a classic GATE question.

### Q22. (Moderate) What current does the CF (current-feedback)`gm`-source deliver when v_gs = 1 mV, gm=2 mA/V?
**Answer:** `2 m×1 m = 2 µA`.
**Method:** i_D = gm·v_gs.

### Q23. (GATE-level) CS with rc degeneration R_S but unbypassed: gain with `gm=2m, R_D=3k, R_S=1k`.
**Answer:** `−gm R_D/(1+gm R_S) = −6/(1+2) = −2`.
**Method:** feedback factor 1+gm R_S.

### Q24. (Moderate) The model of a CG stage: what's the input resistance?
**Answer:** `1/gm ∥ r_o... ≈ 1/gm (small)`; output like CS.
**Method:** looking into source you see ~1/gm — low input R.

### Q25. (GATE-level) CG gain with gm=2m, R_D∥R_L=3k, r_o=50k?
**Answer:** positive `gm·R_eff` = 2m·3k = 6 (r_o∥3k ≈ 2.83k → 5.66 incl. r_o; use full R_eff = 3k∥50k = 2.83k ⇒ +5.66).
**Answer (final): ≈ +5.7.**
**Method:** CG non-inverting; remember r_o parallel if asked.

### Q26. (GATE-level) A CS stage with both R_D and r_o: general gain expression?
**Answer:** `A_v = −gm·(R_D ∥ r_o)`.
**Method:** always parallel r_o with the drain load when λ≠0.

### Q27. (Moderate) Does gm depend on V_DD? Explain.
**Answer:** Not directly — through I_D only (and λ shifts V_DS slightly).
**Method:** gm ∝ √I_D; I_D depends on bias network, not V_DD per se.

### Q28. (GATE-level) If source is AC-grounded via C_S, the small-signal body effect if body is tied to source?
**Answer:** v_bs = 0 still; C_S only shorts the resistor; body drop if the source isn't the body node.
**Method:** two separate questions: bypassing (gain ↑) vs body (only if separate well).

### Q29. (Moderate) Compare BJT and MOS small-signal: what replaces r_π? gm ∝ ?
**Answer:** MOS has NO rπ (gate open); gm ∝ √I_D vs BJT ∝ I_C; r_o identical concept.
**Method:** the key distinction for parameter tests.

### Q30. (GATE-level) A MOS source follower with a load C_L switching: what limits slew (10–90%)?
**Answer:** current into C_L: `SL = I_source/C_L` (e.g. 1 mA/1 pF = 1 V/µs).
**Method:** SR = I/C for capacitive loads — outside the small-signal model but classic.

### Q31. (Moderate) `k=4`, V_ov=0.5, find gm and I_D (saturation).
**Answer:** gm=4·0.5=2 mA/V; I_D=½·4·0.25=0.5 mA; check gm=2I_D/V_ov=1/0.5=2 ✓.
**Method:** consistency of the family of formulas is your best exam check.

### Q32. (GATE-level) Two matched NMOS in parallel: gm and I_D scale?
**Answer:** ∥ doubles both (2 gm, 2 I_D) at same bias.
**Method:** parallel devices add currents/transconductances linearly.

---

## Trap box (exam-day killers)

- No r_π in MOS (students import the BJT habit).
- gm uses peak v_gs; small-signal values are AC — don't mix peak/rms in gain.
- r_o ∥ R_D always when λ≠0; forgetting r_o shrinks answers.
- Diode-connected → R_eq = 1/gm (not r_o).
- gc nguồn body effect only when v_bs≠0 (body not tied to source).

## Final recall drill (do in 60 seconds)

1. gm forms → `k·V_ov = 2I_D/V_ov = √(2kI_D)`
2. r_o → `1/(λI_D)`
3. Intrinsic gain → `gm·r_o`
4. Gate input → ∞ resistance
5. Diode-connected → 1/gm

---