# Chapter 11 — MOSFET Fundamentals

> **The idea in one line:** A MOSFET is a *voltage-controlled* device: the
> gate-source voltage `V_GS` controls the drain current `I_D`. No gate current
> ever flows (gate is insulated). Three terminals do the work: G, S, D (the
> body/substrate is usually ignored). The drain current equation is a square,
> not an exponential — that's the MOSFET's personality.

---

## 11.1 The four-terminal device

```
  NMOS:              PMOS:
   D                  D
   │                  │
   G ├─┤ gate        G ├─┤ gate
   │                  │
   S                  S
```
- **Gate (G):** insulated (oxide); no DC current.
- **Source (S):** where carriers come from.
- **Drain (D):** where carriers go.
- **Body (B):** substrate; in most GATE problems call it connected to source.

Voltage signs to memorize once and forget:
- NMOS: `V_DS > 0` (drain above source), `V_GS > V_th(n)` to turn ON.
- PMOS: `V_DS < 0`, `V_SG > |V_th(p)|` to turn ON (mirror image; look at
  magnitudes).

---

## 11.2 Enhancement vs depletion

| Type | Symbol feature | Channel at V_GS = 0 | Turning ON |
|------|----------------|----------------------|------------|
| **Enhancement (E-NMOS)** | broken channel line | **No channel** (off) | apply `V_GS > V_th` |
| **Depletion (D-NMOS)** | solid channel line | **Has channel** (on) | `V_GS` above a negative `Vth` (V_GS > −V_p etc) keeps it on |

- **Enhancement** = normally OFF; used in most GATE amplifier problems.
- **Depletion** = normally ON; used in some amplifier/bias questions.
- GATE: identifying which by the symbol (broken vs solid line) is a 1-mark
  discriminator.

Region conditions below are for **NMOS**; PMOS mirrors signs.

---

## 11.3 Operating regions (the three states)

For NMOS with `V_GS > V_th`:

### Cutoff
- Condition: `V_GS ≤ V_th`.
- `I_D = 0` (no channel).

### Triode (linear) region
- Condition: `V_GS > V_th` **and** `V_DS < V_GS − V_th` (small V_DS).
- `I_D = μn·Cox·(W/L)·[ (V_GS − V_th)·V_DS − V_DS²/2 ]`
- Behaves like a **voltage-controlled resistor**: for very small V_DS:
  `R_ds ≈ 1/(μn·Cox·(W/L)·(V_GS − V_th))` = 1/(k·(V_GS − V_th)).
- Classic GATE: "MOSFET used as a switch/analog resistor" → triode region.

### Saturation (active) region
- Condition: `V_GS > V_th` **and** `V_DS ≥ V_GS − V_th`.
- `I_D = (1/2)·μn·Cox·(W/L)·(V_GS − V_th)²  ·  (1 + λ·V_DS)`
- The extra `(1+λV_DS)` = **channel-length modulation**.
- Without λ: `I_D = (1/2)·k·(V_GS − V_th)²`, a perfect square law
  (`k = μn·Cox·(W/L)`).
- Collector-style: acts like a **voltage-controlled current source**. This is
  the amplifier region.

### Summary table

| Region | Condition | I_D | Use |
|--------|-----------|-----|-----|
| Cutoff | V_GS ≤ V_th | 0 | switch OFF |
| Triode | V_GS>V_th, V_DS<V_GS−V_th | square-ish, resistor-like | switch ON / resistor |
| Saturation | V_GS>V_th, V_DS≥V_GS−V_th | ½k(V_GS−V_th)²(1+λV_DS) | amplifier |

**The most common exam trap:** GATE will give a MOSFET circuit and ask for the
region. Compute `V_GS − V_th`; compare with V_DS. If `V_DS < V_GS − V_th` →
triode; if `V_DS ≥ V_GS − V_th` → saturation.

---

## 11.4 Channel-length modulation (λ) — the "Early effect" of MOSFET

- With λ>0, drain current rises slightly with V_DS in saturation.
- `λ = 1/V_A` (inverse of the "Early voltage"-like parameter).
- Output resistance in saturation:
  `ro = 1/(λ·I_D)` (or `V_A/I_D`).
- With `λ = 0.02 /V` (V_A = 50 V) and `I_D = 1 mA`: `ro = 50 kΩ`.

### Body effect
- Source not tied to substrate → threshold rises as `V_SB` rises:
  `V_th = V_th0 + γ·(√(2φ_f + V_SB) − √(2φ_f))`
- For most GATE problems: bulk = source ⇒ no body effect. Read the figure.

---

## 11.5 Characteristic curves (sketch ability)

### Output (I_D vs V_DS, family of V_GS)
```
 I_D
  │  triode region (parabolic rise)
  │   │╱   saturation (flat lines, V_GS increasing upward)
  │   │/   /   /
  │   │/   /   /
  └────┴──────────────── V_DS
       V_GS − V_th (boundary line = V_DSat)
```
- Boundary `V_DS = V_GS − V_th` (the parabola knee) moves right with V_GS.

### Transfer (I_D vs V_GS)
- Saturation: `I_D = ½k(V_GS − V_th)²` — a *parabola* starting at V_th.
- Cutoff below V_th.

---

## 11.6 Summary of the classic numbers

- `V_th`: NMOS +0.5 to +1 V; PMOS −0.5 to −1 V (magnitude same).
- `k = μn·Cox·W/L` quoted in mA/V². Mobility: `μn ≈ 2–3× μp`.
- `½k(V_GS−V_th)²` is THE saturation EQ — nothing else needed for 90% of
  GATE MOS problems.

---

## Worked example — region check

NMOS: `k = 1 mA/V²`, `V_th = 1 V`, `V_GS = 3 V`, `V_DS = 5 V`.
- `V_GS − V_th = 2 V`. `V_DS = 5 > 2` → **saturation**.
- `I_D = ½·1m·(2)² = 2 mA`.

Same but `V_DS = 1 V`: `1 < 2` → **triode**. `I_D` = using triode formula:
`1m·[(2)·1 − 0.5] = 1.5 mA`. Compare: saturation would say 2 mA — don't!

---

## GATE traps (MOSFET)

1. **Region, region, region.** Compute `V_GS − V_th` vs `V_DS` first; using the
   saturation formula in triode = wrong.
2. Enhancement "normally OFF" at V_GS=0; depletion "normally ON".
3. `ro = 1/(λ·I_D)` only when saturated w/ λ given.
4. Watch polarity for PMOS: substitute magnitures or flip the sketch — don't get
   signs tangled.
5. "Voltage-controlled resistor" = triode; "voltage-controlled current source"
   = saturation.
6. Do not use `= ½k(V_GS−VDS)²`—the correct square term is `(V_GS − V_th)²`,
   with V_DS nowhere in the saturation expression (except via λ).

---

## 5-question self-check

1. NMOS saturation condition? → *V_GS > V_th, V_DS > V_GS − V_th.*
2. `k=2 mA/V², V_th=1 V, V_GS=2 V` in saturation: I_D? → *½·2·1 = 1 mA.*
3. V_DS left of knee → which region? → *triode.*
4. ro when λ=0.01, I_D=0.5 mA? → *200 kΩ.*
5. Which region for a MOSFET "on resistor"? → *triode.*

Next: **`12-MOSFET-Biasing.md`**