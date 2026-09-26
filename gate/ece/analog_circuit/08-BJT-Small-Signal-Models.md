# Chapter 08 — BJT Small-Signal Models

> **The idea in one line:** around a fixed DC point, the BJT behaves linearly.
> Its exponential I-V curve becomes a set of linear resistors and a current
> source (`gm·v_be`). Two equivalent pictures exist: the **hybrid-π** model and
> the **T** model. You must convert between them instantly.

---

## 8.1 The four small-signal parameters

Defined at the DC operating point `I_C`:

```
gm  (transconductance) = ΔI_C/ΔV_BE = I_C / V_T      [V_T = 25 mV @ 300 K]
rπ  (base input res.)   = ΔV_BE/ΔI_B  = β / gm
re  (emitter resistance)= ΔV_BE/ΔI_E  = V_T / I_E    (≈ short-ckt models)
ro  (output resistance) = ΔV_CE/ΔI_C  = V_A / I_C    (Early effect)
```
Relationships to memorize:
```
gm = I_C / V_T
rπ = β/gm  = β·V_T/I_C
re = V_T/I_E ≈ V_T/I_C         (I_E ≈ I_C)
rπ = (β+1)·re                  (≈ β·re)
I_C = 1 mA ⇒ gm = 40 mA/V (classic); rπ = 2.5 kΩ at β=100
```
**The "40" magic number:** `gm = 40·I_C` when `I_C` is in A (40 mA/V per mA).*
GATE loves `gm = 40·I_C[mA]` mA/V.

### Early effect (finite output resistance)
The collector current rises slightly with `V_CE`:
`I_C = I_C0·(1 + V_CE/V_A)`, `V_A` = Early voltage (tens of volts).
- `ro = V_A/I_C (≈ V_A/I_C(sat))`.
- With `V_A = 100 V` and `I_C = 1 mA`: `ro = 100 kΩ`.
- Small `I_C` → large `ro`. GATE asks: "output resistance ≈ ?" often `ro`.

---

## 8.2 The hybrid-π model (for midband/high-frequency analysis)

Connections: Base − collector − emitter.

```
        B ──┬─ rπ ──┬── E        (rπ from B to E)
           │       │
           │       ▼  (controlled)
           │       └──┐
           │   gm·v_be ▼ I source
           │          │
           │          │
           └─ ro ─────┘          (ro from C to E, in parallel with source)
         C
```
- `gm·v_be`: the collector current = transconductance × base-emitter voltage.
- `ro`: between collector and emitter, carrying the Early-effect current.
- `rπ`: the input resistance seen between base and emitter.
- Direction of source: for NPN, current flows **into the collector** (out of the
  emitter). Draw arrows accordingly; signs follow.

**Bypassing internals for GATE:** base-emitter behaves as `rπ`, the controlled
source `gm·v_be` drives the collector node, `ro` shunts it. Blindingly fast once
you draw it once.

---

## 8.3 The T-model (for some specific problems)

Base current enters at B; emitter has a small resistor `re` between emitter and
the internal node; collector is effectively a current source `α·I_E (≈I_C)`.

```
        B ──┐
            │
            │  (base drives through re to emitter; I_E = (β+1)I_B)
       C ◄──┴── α·I_E (= I_C) source
            │
        E ──re── internal-gnd
```

- `re` = `V_T/I_E`, often the handiest: *emitter resistance*.
- From the emitter, looking in: `re`. From the base: `(β+1)·re ≈ β·re = rπ`.
- Relationship: `rπ = (β+1)·re`.

When to use T-model: direct questions about emitter-follower input impedance,
or when the emitter is the signal node, or problems that give `re`.

---

## 8.4 Converting models and the golden relationships

| Want | Use |
|------|-----|
| gm | `I_C/V_T` |
| rπ | `β/gm` or `(β+1)re` |
| re | `V_T/I_E` |
| ro | `V_A/I_C` |
| IC given, β given | `I_B = I_C/β`, `I_E = I_C·(β+1)/β` |

**Common GATE mini-data set:** `I_C = 1 mA, β = 100, V_T = 25 mV, V_A = 100 V`
→ `gm = 40 mA/V`, `rπ = 2.5 kΩ`, `re = 25 Ω`, `ro = 100 kΩ`. Commit these.

---

## 8.5 AC analysis recipe (the heart of every BJT amplifier)

1. **DC analysis first:** find `I_C`, `V_CE` at Q (Chapter 07). This gives the
   parameters (`gm,rπ,ro`).
2. **Kill DC:** short all capacitors (coupling & bypass) in midband; short
   voltage supplies to ground (keep AC hosts).
3. Replace the BJT with a small-signal model.
4. Solve the linear circuit with KCL/KVL for `v_out/v_in`.

This recipe is Chapter 27 restated; keep it front-of-mind.

---

## Worked example — CE gain via the model

Circ: `V_CC=12`, `I_C=1 mA` at Q, `R_C=4 kΩ`, `R_L=4 kΩ`, `R_s=0`,
`β=100`, `R_E` bypassed, `ro` ignored.

- Mix small-signal: `v_out` appears across `R_C || R_L = 2 kΩ`.
- `v_be = v_in` (source directly at base).
- `i_c = gm·v_be = 40m·v_in` → `v_out = −i_c·(R_C||R_L) = −40m·2k·v_in = −80·v_in`.
- `A_v = −gm·(R_C||R_L) = −80`. **Negative** → phase inversion of CE stage.

---

## GATE traps (small-signal)

1. **Sign.** CE gives negative gain. Always write `A_v = −gm·(R_C||R_L)`; students
  drop the minus and half the problem.
2. Units: `gm` in A/V; `R` in Ω; gain dimensionless. `40 mA/V × 4 kΩ = 160`.
3. `rπ = β/gm`, `re = V_T/I_E` — do not mix base/emitter resistors.
4. If `ro` is NOT negligible (it's "∞" or "ignore") you can often shortcut;
  when given `V_A` nonzero, compute `ro` and include it in parallel with `R_C`.
5. `rπ` is only on the *base side* (hybrid-π); `re` only on the *emitter side*
  (T-model). Do not put both in one circuit.
6. ID of DC current is a Q-point; symbol "I_C" in small-signal problems means the
  **DC** value — do not confuse with AC amplitude.

---

## 5-question self-check

1. `I_C = 2 mA`. gm? → *80 mA/V.*
2. `β = 100`, `I_C = 1 mA`. rπ? → *2.5 kΩ.*
3. `V_T = 25 mV`, `I_E = 2 mA`. re? → *12.5 Ω.*
4. `V_A = 75 V`, `I_C = 0.5 mA`. ro? → *150 kΩ.*
5. `rπ = β·re` ⇒ `re` at `I_E=2mA =?` → *12.5 Ω, β=100 → rπ=1.25 kΩ.*

Next chapter: **`09-BJT-Amplifiers.md`**