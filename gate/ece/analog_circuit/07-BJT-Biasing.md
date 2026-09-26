# Chapter 07 — BJT Biasing

> **The idea in one line:** Biasing fixes the DC operating point (Q-point:
> `I_C`, `V_CE`) in the middle of the active region, and it must *stay there*
> when `β` or `V_BE` changes with temperature. The whole chapter is about: which
> circuit pins the Q-point firmly.

---

## 7.1 What "good biasing" means

- Q-point in active region, not near saturation/cutoff.
- **Stable** against:
  - `β` variation (transistor-to-transistor, and with temperature),
  - `V_BE` drift (~−2 mV/°C),
  - `I_CBO` growth,
  - supply change.
- Stability is measured by **stability factor** `S`:
  `S = ΔI_C / ΔI_CBO` (change in collector current caused by change in leakage).
- Smaller `S` = more stable. Ideal `S = 1`. Large `S` (fixed bias) = unstable.
- `S(β)` and `S(V_BE)` exist too — GATE mostly asks qualitative which circuit is
  most/least stable, plus a numeric `S` for fixed/emitter/collector-to-base bias.

---

## 7.2 Fixed bias (base bias)

```
        +V_CC
         │
        R_C ──► C
         │
       V_C
   R_B  │
    ├───┤
    │   V_B   (E to ground)
   V_BB  │   ├─ E
        E_NPN ground
```
Simpler figure: `V_BB − R_B − (B→E) − ground` and `V_CC − R_C − (C→E) − ground`.

**DC analysis:**
1. `I_B = (V_BB − V_BE)/R_B`.
2. `I_C = β·I_B`.
3. `V_CE = V_CC − I_C·R_C`.
4. Check `V_C > V_B` for active.

**Stability — the problem:** 
`S = 1 + β` for fixed bias! (derived: `I_C = β·I_B`, `I_B` is fixed DC so
`dI_C/dI_CBO = 1+β`). So a β of 100 gives `S = 101` → very unstable.
- Temperature rises → `I_CBO` rises → `I_C` rises a lot → Q-point wanders.

---

## 7.3 Collector-to-base bias (self-bias / voltage feedback)

One resistor `R_B` from **collector to base** (plus `R_C` from supply to
collector).
**DC analysis:**
1. `I_C ≈ β·I_B`.
2. Base loop: `V_CC = I_C·R_C + I_B·R_B + V_BE`
   (current through R_B = I_B + ... exactly `I_B` when collector current through R_C).
3. Solve for `I_B`: `V_CC − V_BE = β·I_B·R_C + I_B·R_B`
   → `I_B = (V_CC − V_BE)/(R_B + β·R_C)`.
4. `V_CE = V_CC − I_C·R_C` (or `= V_BE + I_B·R_B`).

**Stability:** better than fixed because *if `I_C` rises, V_C falls, which lowers
`I_B`, which pulls `I_C` back* (negative feedback). 
- `S ≈ (1+β)·R_C/(R_B + R_C)` — significantly < (1+β). Usually `2 to 5`.
- Poor for output swing: `R_B` loads the collector signal.

---

## 7.4 Emitter bias (with emitter resistor)

Insert `R_E` between emitter and ground (no emitter bypass yet in DC analysis —
bypass is for AC, Chapter 10).
DC loop:
1. Base loop: `V_BB = I_B·R_B + V_BE + I_E·R_E`.
   With `I_E = (β+1)·I_B`:
   `V_BB − V_BE = I_B·(R_B + (β+1)·R_E)`.
2. `I_B = (V_BB − V_BE)/(R_B + (β+1)·R_E)`.
3. `I_C → β·I_B`; `V_CE = V_CC − I_C·R_C − I_E·R_E ≈ V_CC − I_C(R_C + R_E)`.
4. `V_E = I_E·R_E ≈ I_C·R_E`.

**Stability:** the `(β+1)·R_E` term — because `R_E` dominates `R_B`, `β`*shrinks* out
of the answer:
`I_B ≈ (V_BB − V_BE)/((β+1)·R_E)` → `I_C = β·I_B ≈ (V_BB − V_BE)/R_E`.

This is the key insight: **with a stiff emitter resistor, I_C is set by the
voltage at the base minus V_BE, divided by R_E — almost independent of β.**
- Stability `S ≈ 1 + R_E/R_B` (approximately) or more precisely with `R_E`
  large, `S → 1`. Very stable.

---

## 7.5 Voltage-divider bias (the standard, most stable, GATE favourite)

```
        +V_CC
         │
        R_C ──► C
         │        V_C
        R1 │
        ├──► B ── R2 ── GND
        │          (V_B from divider)
        │        E
        │    ── R_E ── GND
        V_CC        │
     (R1 between V_CC and B, R2 between B and GND)
```

Two resistors `R1 (R_B1)` from supply to base and `R2 (R_B2)` from base to
ground create a **base voltage** by the divider rule; `R_E` then sets `I_C`.

**Approximate analysis (valid when β·R_E > 10·R2, i.e., base current negligible):**
1. `V_B = V_CC · R2/(R1 + R2)`.   (divider, ignoring I_B)
2. `V_E = V_B − V_BE`.
3. `I_E = V_E / R_E`;  `I_C ≈ I_E`.
4. `V_CE = V_CC − I_C·(R_C + R_E)`.

**Exact analysis (when base current matters):**
1. `R_th = R1||R2`, `V_th = V_CC·R2/(R1+R2)` (Thevenin of the divider).
2. Base loop: `V_th = I_B·R_th + V_BE + I_E·R_E`, with `I_E=(β+1)I_B`.
   `I_B = (V_th − V_BE)/(R_th + (β+1)·R_E)`.
3. `I_C = β·I_B`, `V_CE = V_CC − I_C·R_C − I_E·R_E`.

**When GATE says "approximate"** it expects the divider-rule shortcut (step 1-4).
Look for "β·R_E ≥ 10·R2" or "neglect base current".

**Stability:** 
- `S ≈ (1+β)/(1 + β·R_E/(R_E+R_th))`... the full formula:
  `S = (1+β)·(R_th + R_E)/(R_th + (β+1)·R_E)`.
- With large `R_E` → `S ≈ 1`. Most stable of all four circuits. **Default answer
  for "most stable biasing"?** Voltage-divider (with R_E).

---

## 7.6 Load line concept (both DC and AC)

- **DC load line:** plot of `I_C` vs `V_CE` as `R_C` (and `R_E`, if present)
  fixes the relationship `V_CE = V_CC − I_C(R_C + R_E)`.
  Intercepts: `I_C = 0 → V_CE = V_CC` ; `V_CE = 0 → I_C = V_CC/(R_C+R_E)`.
  Q-point = where this line meets the transistor curve `I_C = β·I_B`.
- **AC load line:** uses only the AC resistors seen by the collector
  (`R_C || R_L`, with bypassed `R_E` in the picture varied). The AC load line
  passes through the Q-point but *steeper*; it decides how large a signal can be
  before clipping. Slope = `−1/R_ac` where `R_ac = R_C||R_L` (plus source side).

- Clipping: signal hits cutoff (I_C → 0) or saturation (V_CE → 0.2)
  at the ends of the AC load line — GATE asks the maximum unclipped swing
  `= min(V_CE(Q) − ... , I_C(Q)·R_ac ...)`.

---

## 7.7 Summary comparison (stability & features)

| Bias | Stability S | β-dependence | Use in GATE |
|------|-------------|--------------|-------------|
| Fixed | 1 + β (worst) | Strong — Q-point varies with β | Simple, shows why bias matters |
| Collector-to-base | ≈ (1+β)R_C/(R_B+R_C) | Moderate | Feedback case |
| Emitter | ≈ 1 + R_E/R_B | Low (if R_E dominates) | Temperature stable |
| Voltage-divider | ≈ 1 (best) | Very low | The standard answer |

**Rule of thumb for the "which is most stable?" question: voltage-divider bias.**
**For "least stable": fixed bias.**

---

## Worked example (voltage-divider, approximate)

`V_CC = 12 V`, `R1 = 100 kΩ`, `R2 = 25 kΩ`, `R_C = 4 kΩ`, `R_E = 1 kΩ`,
`β = 200`, `V_BE = 0.7 V`. Check if approximate justified: `β·R_E = 200·1k =
200 kΩ ≥ 10·R2 = 250 kΩ`? Borderline — do exact to be safe; but the shortcut:

- `V_B = 12·25/(125) = 2.4 V`.
- `V_E = 2.4 − 0.7 = 1.7 V`.
- `I_E = 1.7/1k = 1.7 mA` → `I_C ≈ 1.7 mA`.
- `V_CE = 12 − 1.7m·(4k + 1k) = 12 − 8.5 = 3.5 V`.

Check active: `V_C = 12 − 1.7m·4k = 5.2 V > V_B = 2.4 V` ✓ active.

---

## GATE traps (biasing)

1. **Approximate vs exact:** the divider shortcut needs `I_B` negligible
   (`β·R_E ≳ 10·R2`). If a number is chosen to make `I_B` large, use exact
   Thevenin method.
2. Forgot `R_E` in the `V_CE` equation: `V_CC − I_C·R_C − I_E·R_E` (emitter drops
   too). Students drop the R_E term.
3. In emitter bias the formula uses `(β+1)·R_E` in the denominator, not `β·R_E`.
4. Stability factor `S = ΔI_C/ΔI_CBO` is NOT `1+β` for all circuits — only for
   fixed bias.
5. "Bias stable when R_E is large, R_B is small" — know the reason: base
   voltage is determined by the source, emitter current by `(V_B − V_BE)/R_E`.
6. The DC Q-point and the AC load line share a point (Q) — any symmetry swing
   must be about Q.

---

## 5-question self-check

1. Which bias has the highest stability factor S? → *Fixed bias (S=1+β).*
2. Which circuit is most β-independent? → *Voltage-divider bias.*
3. Fixed bias, β=99. S? → *100.*
4. Divider: V_B = 2.4 V, R_E = 1 kΩ. I_C ≈? → *(2.4 − 0.7)/1k = 1.7 mA.*
5. R_E big, I_B small → collector current is set by? → *(V_B − V_BE)/R_E.*

Next chapter: **`08-BJT-Small-Signal-Models.md`**