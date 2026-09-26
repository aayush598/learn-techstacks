# Chapter 12 — MOSFET Biasing

> **The idea in one line:** set the DC `V_GS` and `I_D` so the MOSFET sits in
> **saturation** (the amplifier region), and keep it there when
> `V_th`/temperature/process vary. The four standard tricks: gate voltage divider,
> drain feedback, a source resistor degenerating the whole thing, and a
> current-source tail.

---

## 12.1 Rules of the biasing game

- For amplifier use: **saturation** is required:
  `V_DS ≥ V_GS − V_th` (NMOS). Check after solving.
- The gate draws **zero DC current**. So gate voltage is set purely by the
  divider (no base-current correction — simpler than BJT!).
- Want `I_D` set by a resistor, not by k or V_th (both drift).

---

## 12.2 Fixed gate bias

```
   +V_GG ─ R_G ─── G          drain: +V_DD ─ R_D ─┬── D
                     │                              │
                     └── (nothing draws gate current) S ─ R_S ─ GND (maybe)
```
- `V_GS = V_GG` directly (R_G can be huge — carries no DC current; its job is AC
  impedance setting).
- `I_D = ½k(V_GG − V_th)²` (saturation, λ=0).
- **Problem:** any drift in `V_th` or `k` directly changes `I_D`. Poor stability.
- Classic GATE ask: "why is a large R_G acceptable at the gate?" → because
  gate current = 0 (MOSFET gate is insulated).

---

## 12.3 Drain-feedback bias

```
   +V_DD ─ R_D ──┬── D
                  │
                 R_G  (gate connected to drain)
                  │
                 G
                 S ─ R_S ─ GND
```
- Gate voltage = drain voltage (feedback). 
- If `I_D` rises, drain voltage V_D drops, so V_GS falls, pulling I_D back —
  **negative feedback stabilizes I_D**.
- DC equation: `V_DD = I_D·R_D + V_GS + I_D·R_S`(if any) and `V_GS = V_D` when
  no R_S... careful:
  With R_G direct to drain: `V_G = V_D`. Then `V_GS = V_D` and
  `V_D = V_DD − I_D·R_D` (if R_S=0). Solve quadratic.

---

## 12.4 Voltage-divider gate bias (the standard, stable)

```
   +V_DD ─ R1 ──────── G (V_G fixed by divider — gate current zero)
            │
           R2 ─ GND
            │
   +V_DD ─ R_D ─┬── D
                S ─ R_S ─ GND
```
1. `V_G = V_DD·R2/(R1+R2)` (exact — no gate current!).
2. `V_S = I_D·R_S`. So `V_GS = V_G − I_D·R_S`.
3. Saturation: `I_D = ½k(V_G − I_D·R_S − V_th)²`. Solve quadratic.
4. `V_DS = V_DD − I_D·(R_D + R_S)`. Verify `V_DS ≥ V_GS − V_th`.

Why stable: `V_G` fixed by ratio → `V_GS = V_G − I_D·R_S` — so `I_D` rise lowers
V_GS → restores. This is the MOS version of `(V_B−V_BE)/R_E`.

**Most GATE MOS-biasing numerical uses exactly this circuit.**

---

## 12.5 Source-follower / current-source bias

- **Source resistor: same as above.** Long story short, R_S stabilizes.
- **Current-source bias (tail/mirror):** set the source with a transistor
  current source (`I_D = I_tail` hard-fixed). Q-point fixed; used in
  differential pairs (Chapter 18).

---

## 12.6 Solving the quadratic — GATE patterns

Equation `I_D = ½k·(V_G − R_S·I_D − V_th)²`.

- Method: write in the form `(V_G − V_th) − R_S·I_D = √(2I_D/k)`**or** expand the
  square: `a·I_D² + b·I_D + c = 0`. Choose simpler depending on numbers.
- Use `√` if you can estimate `√(2I_D/k)`.
- Quick sanity rearrangements:
  - If `R_S·I_D` small → `I_D ≈ ½k(V_G − V_th)²` (no R_S).
  - Simplify: `V_GS = V_G − I_D·R_S` always the first substitution.

**Worked:** `V_DD = 10 V`, `R1 = 40 kΩ`, `R2 = 10 kΩ`, `R_D = 2 kΩ`,
`R_S = 1 kΩ`, `k = 1 mA/V²`, `V_th = 1 V`.

1. `V_G = 10·10/50 = 2 V`.
2. `V_GS = 2 − I_D·1k`.
3. `I_D = ½·1m·(2 − I_D·1k − 1)² = 0.5m·(1 − 1000·I_D)²`.
4. Let `x = 1000·I_D` (mA): `x = 0.5·(1−x)²` → `x = 0.5(1 −2x + x²)` →
   `0.5x² − 2x + 0.5 = 0` → `x² −4x + 1 = 0` → `x = 2±√3` → `x ≈ 0.268` (small
   root; large root puts V_GS below threshold/cutoff).
5. `I_D ≈ 0.268 mA`.
6. `V_DS = 10 − 0.268·(2k+1k) = 10 − 0.804 = 9.196 V`.
   `V_GS = 2 − 0.268 = 1.732 V`; `V_DS ≥ V_GS−V_th = 0.732` → **saturation** ✓.

Remember to *eliminate* unphysical roots: if the chosen root makes
`V_GS < V_th`, discard.

---

## 12.7 Load lines (DC & AC) for MOSFET

- **DC load line:** `V_DS = V_DD − I_D·(R_D + R_S)` — line from `(V_DD, 0)` to
  `(0, V_DD/(R_D+R_S))`.
- Q-point = intersection with saturated parabola `I_D = f(V_GS)` for a fixed V_GS.
- **AC load line:** uses `R_ac = R_D ∥ R_L` (bypassed R_S). The symmetric swing
  about Q = `min(I_D·R_ac, V_DS(Q))`. Larger R_ac → larger max swings (but
  steeper line → clipping sooner at the other end).

---

## GATE traps (MOSFET biasing)

1. **No gate current** — R_G/R1/R2 only fix the voltage; never "solve base
   loop" like BJT.
2. Quadratic: choose physically possible root (0 < V_GS−V_th, and R_S·I_D < V_G).
3. Verify saturation — if not, use triode equation instead.
4. R_D and R_S both drop from V_DD: `V_DS = V_DD − I_D(R_D+R_S)`.
5. In drain-feedback, `V_G = V_D` — don't drag R2 assumptions in.
6. PMOS: flip ± signs of voltages to mirror NMOS; absolute values identical.

---

## 5-question self-check

1. `V_G` with no gate current is set by? → *R1-R2 divider only.*
2. Stability in divider bias comes from? → *R_S: V_GS = V_G − I_D·R_S.*
3. NMOS saturation check formula? → *V_DS ≥ V_GS − V_th.*
4. `V_G = 3 V`, `R_S = 1 kΩ`, solution `I_D = 1 mA` → V_GS? → *2 V.*
5. Which bias keeps I_D independent of k? → *current-source / mirror tail.*

Next: **`13-MOSFET-Small-Signal-Model.md`**