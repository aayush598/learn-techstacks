# Chapter 15 — BJT vs MOSFET: Comparison and Circuit Identification

> **The idea in one line:** one current-controlled (BJT), one voltage-controlled
> (MOSFET), with mirror-image amplifier topologies. If you can *name the other
> family's equivalent* whenever you see a transistor amplifier, you can answer
> any "identify the circuit" or "compare" GATE question.

---

## 15.1 Head-to-head control philosophy

| | BJT | MOSFET |
|---|---|---|
| Control signal | base current `I_B` | gate voltage `V_GS` |
| Input impedance | finite (`rπ`) | infinite (gate open) |
| Output current | `I_C = βI_B` | `I_D = ½k(V_GS−V_th)²` |
| Law | exponential (transport) | square law |
| gm at 1 mA | 40 mA/V | typically 2–10 mA/V |
| Gate/base current | negligible in small-signal (but not zero) | **zero** in steady state |
| Thermal behavior | `V_BE`~−2 mV/°C | `V_th` drifts, gm roughly half-order |
| Speed | slightly lower tailing | faster (small RC, no minority storage) |
| Noise | shot-dominated | better at low freq in some FOM |
| Power | base current wastes a bit | mostly gate-charging current |
| Body effect | (n/a) | yes, if body not tied to source |

**Where it shows up in GATE:**
- "Which device has virtually infinite input impedance?" → **MOSFET**.
- "Which needs ~0.7 V between B-E to conduct?" → BJT.
- "Why is the MOSFET better for battery/low-power?" → input impedance + high
  R_in → less source loading.

---

## 15.2 Amplifier topology mirror — memorize as pairs

| BJT | MOSFET | Notes |
|-----|--------|-------|
| Common-Emitter (CE) | Common-Source (CS) | inverting, high gain, `A_v = −gm·(R_C∥R_L)` / `−gm(R_D∥R_L)` |
| Common-Base (CB) | Common-Gate (CG) | non-inverting, R_in ≈ re / 1/gm, current buffer |
| Common-Collector (CC) | Common-Drain (CD) | source/emitter follower, ≈1 gain buffer |
| `rπ = β/gm` | ∞ input R at gate | input side difference |
| `re = V_T/I_E` | `1/gm` | the "low input R" terminal family |
| `ro = V_A/I_C` | `ro = 1/(λI_D)` | both are the transistor output impedance |

So a CE-vs-CS problem is a 1:1 translation. Once you've mastered Ch 09, Ch 14
is free.

---

## 15.3 Gain, resistance, and degeneration — parallel table

| | CE | CS |
|---|---|---|
| A_v basic | −gm·(R_C∥R_L) | −gm·(R_D∥R_L) |
| A_v degenerated | −gm·R_C/(1+gm·R_E) ≈ −R_C/R_E | −gm·R_D/(1+gm·R_S) ≈ −R_D/R_S |
| R_in | R1∥R2∥rπ | R_G (large) |
| R_out | R_C | R_D |

The formulas are *identical in structure*. "Degeneration resistor" = R_E in BJT,
R_S in MOS. Both:
- reduce gain, increase linearity, increase input R, widen bandwidth,
- make gain set by resistors → β/process-stable.

---

## 15.4 Identify-the-circuit questions (the GATE payoff)

Given a schematic, follow this checklist:

1. **Device type:** symbol shows NPN/PNP (arrow) or NMOS/PMOS (broken/solid
   channel). 
2. **Find the AC-grounded terminal:** any terminal connected to ground
   *through* a capacitor (or straight to a supply) = the common terminal.
   - Emitter/source at AC ground → **CE / CS**.
   - Base/gate at AC ground → **CB / CG**.
   - Collector/drain at AC ground → **CC / CD**.
3. Read the gain/phase to confirm:
   - CE/CS: inverting, gain ~gm·R_load, R_in moderate.
   - CB/CG: non-inverting, R_in small (re / 1/gm).
   - CC/CD: gain ≈ 1, R_in huge, R_out small.

**Common trap:** a capacitor whose other side connects to the *supply* in AC is
also an AC ground (supplies are midband shorts). Count it.

---

## 15.5 Frequency/response differences worth two marks

- MOSFET internal caps are smaller → higher `ft` and wider bandwidth.
- BJT `gm/I_C = 1/V_T` (high for its current); MOSFET `gm/I_D` falls as 1/√I_D —
  BJT wins *gain-per-mA* at low current.
- Miller effect (Ch 16) applies to CE and CS (both inverting, C between
  cap-in/out cap), not to CB/CG/CD/CC.

---

## Worked identification example

```
  +V_CC
   │
  R_C ─────────────► v_out
   │                    │
  C1 ─ v_in ────────────┤ (base)
   │                    │
  R_E ─ C_E ─ GND       │ (emitter bypass)
```
- Emitter: connected to the supply via nothing; but C_E → GND so **emitter
  AC-grounded** ⇒ Common-Emitter. Phase inverted, so for v_in going up
  v_out goes down.

---

## GATE traps (BJT vs MOSFET)

1. Infinite R_in belongs to MOSFETs; never apply `rπ` to a MOS gate.
2. Same topology names across families — translating saves time; don't re-derive.
3. Inverting family signs: CE/CS invert, CB/CG/CD/CC don't. Half a mark for
  phase mistakes.
4. Degeneration: R_E and R_S both *reduce* gain; R_E never stands alone in
  formulas (gm·R_E matters).
5. A capacitor to supply = AC ground; don't call that terminal "not the
  common."

---

## 5-question self-check

1. Device with infinite input R? → *MOSFET.*
2. CE ↔ ? → *CS.*
3. Which config has R_in ≈ re/1gm both families? → *CB/CG.*
4. Degeneration resistor purpose in both? → *stabilize gain/linearity at the
   cost of gain.*
5. Phase of CS? → *inverting (180°).*

Next: **`16-Frequency-Response.md`**