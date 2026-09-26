# Chapter 14 — MOSFET Amplifiers: CS, CG, CD

> **The idea in one line:** three MOSFET amplifier configurations mirror BJT:
> **Common-Source** (inverting, high gain), **Common-Gate** (non-inverting,
> low input R), **Common-Drain** (source follower, gain ≈ 1, buffer). The
> transistor becomes the 3-element model of Chapter 13; the rest is resistors.

---

## 14.0 Comparison table — commit it

| | Common-Source (CS) | Common-Gate (CG) | Common-Drain (CD) |
|---|---|---|---|
| Input | Gate | Source | Gate |
| Output | Drain | Drain | Source |
| A_v | −gm(R_D∥R_L) (inverting, large) | +gm(R_D∥R_L) (non-inv) | ≈ RL/(RL + 1/gm) ≈ 1 |
| R_in | ≈ ∞ (gate) | ≈ 1/gm ≈ low | ≈ ∞ |
| R_out | ≈ R_D | ≈ R_D | ≈ 1/gm ≈ low |
| Phase | 180° | 0° | 0° |
| Classic role | voltage amplifier | coax/high-freq | buffer / level shift |

---

## 14.1 Common-Source (CS) amplifier

```
  +V_DD
   │
  R_D ─── D ───► v_out
   │
  G ── v_in (through C1, gate resistor R_G to ground)
   │
  S ── R_S (bypassed by C_S) ── GND
```

**Small-signal results (rop included only if given):**
```
A_v   = −gm·(R_D ∥ R_L)               [if ro ignored]
      = −gm·(R_D ∥ R_L ∥ ro)
R_in  = R_G (gate biased resistor; intrinsic R = ∞)
R_out = R_D
```
- Inverting: `v_out` is 180° out of phase.
- Gain grows with `gm` and with `R_D∥R_L`.

### CS with unbypassed source resistor (source degeneration)
If `R_S` appears in the AC path (no bypass cap):
```
A_v   = −gm·R_D / (1 + gm·R_S)
      ≈ −R_D/R_S           (when gm·R_S ≫ 1)
R_in  = R_G                (unchanged)
R_out = R_D
```
- Same trade-off story as CE: less gain, more linear/stabilized, higher
  bandwidth (reduces the gm-sensitivity).
- GATE trick: look for a bypass cap across R_S. If present → use the big gain.

### The "gm vs resistors" insight
Gain `≈ −gm·R_D` vs `≈ −R_D/R_S`. Bypassed: gm (device, drifty).
Unbypassed: resistor ratio (precise). GATE asks "which is more
process-stable?" → unbypassed (resistor-defined).

---

## 14.2 Common-Gate (CG) amplifier

Input at **source**, output at **drain**; gate AC-grounded (bypass cap C_G to
ground).

```
  source: v_in → C1 → S ── (into the transistor)
  gate: G ── C_G ── GND
  drain: R_D ──► v_out
```

**Results:**
```
A_v   = +gm·(R_D ∥ R_L)         (non-inverting)
R_in  = 1/gm                    (very low, tens of ohms)
R_out = R_D
A_i   ≈ 1                       (current buffer — input current ≈ output)
```
- No Miller effect (gate grounded) → good for high frequency.
- Low input impedance — matching for 50 Ω transmission lines in RF contexts.

---

## 14.3 Common-Drain (CD) / source follower

Input at gate, output at **source**; drain tied to V_DD (AC ground).

```
  G ── v_in
  D ── V_DD (AC short)
  S ── R_S ── GND
       └──► v_out
```

**Results:**
```
A_v   = R_S/(R_S + 1/gm)  ≈ 1 (but < 1)
R_in  = R_G                (high)
R_out = 1/gm ∥ R_S∥...     ≈ 1/gm (low)
```
- Output *follows* input with `≈ gm·R_S/(1+gm·R_S)` gain — a **buffer**.
- Prevents a high-impedance source from being loaded; used as the output stage.

---

## 14.4 Worked CS example

Given: `V_DD = 10 V`, `R_D = 4 kΩ`, `R_L = 4 kΩ`, bias gives `V_GS = 2 V`,
`I_D = 1 mA`, `λ = 0.01 (ro = 100 kΩ)`, gate resistor `R_G = 1 MΩ`.

- `gm = 2·I_D/(V_GS−V_th)` — need V_th. Suppose bias yields `V_GS − V_th = 1 V`
  → `gm = 2·1m/1 = 2 mA/V`.
- `R_D ∥ R_L = 2 kΩ`.
- `A_v = −gm·2k = −4`. (With ro: `2k ∥ 100k ≈ 1.96 kΩ` → barely changes.)
- `R_in = R_G = 1 MΩ`. `R_out = R_D = 4 kΩ`.

---

## 14.5 Cascoding (a GATE love-letter)

- Cascade a **common-source input** with a **common-gate output** — the
  **cascode**.
- Gain ≈ `gm·(R_D∥R_L)` but the CG shields the CS drain from V_DS variation →
  high output R, wider bandwidth, less Miller loading. GATE asks *why the
  cascode*: isolates Miller, improves bandwidth and gain stability.

---

## GATE traps (MOSFET amplifiers)

1. CS **inverts**; CG/CD **don't**. Same gotcha as BJT — minus sign decisive.
2. R_in at gate is **huge** (R_G), not `1/gm` — the 1/gm is a *source*
   impedance (CG/CD).
3. Bypassed vs unbypassed R_S switches the CS gain between `−gm·R_D` and
   `−R_D/R_S`.
4. Source follower gain `R_S/(R_S + 1/gm)` → never exactly 1 (unless gm·R_S→∞).
5. ro parallel with R_D in CS/CG whenever λ is nonzero.
6. Recognizing the config by the AC-ground terminal (gate/source/drain
   grounded); misidentifying inverts everything.

---

## 5-question self-check

1. Which MOSFET amp has R_in ≈ 1/gm? → *CG.*
2. Name the non-inverting config(s). → *CG, CD.*
3. CS with bypassed R_S: A_v = ? → *−gm(R_D∥R_L).*
4. Source follower R_out? → *≈ 1/gm.*
5. Cascode = ? → *CS input + CG output (bandwidth/gain benefit).*

Next: **`15-BJT-vs-MOSFET.md`**