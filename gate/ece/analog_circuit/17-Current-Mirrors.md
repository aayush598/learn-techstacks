# Chapter 17 — Current Mirrors

> **The idea in one line:** copy a known reference current to another branch
> *without* losing volts. Two matched transistors with connected bases make the
> mirrored device "clone" the reference current. This is the workhorse bias
> generator inside every op-amp and differential pair.

---

## 17.1 The basic BJT current mirror

```
         I_ref            I_out
          │                 │
   +V_CC  │                 │
          ▼                 ▼
     R ────┤  C(C1)     C(C2)┤
            │                 │
   B1 ──────┴──── B2 (tied)   │
            │                 │
           E1                 E2
            └────────┬────────┘
                     └── GND
```
- Q1 diode-connected (base–collector shorted). It sets `V_BE1`.
- Q2 sees the identical `V_BE` → identical `I_C` (matched transistors).
- `I_ref = (V_CC − V_BE)/R`.
- `I_out = I_C(Q2)`.

**Why classic:** because `I_C = I_S·e^(V_BE/V_T)`, equal `V_BE` (equal
`V_T`, matched `I_S`) with equal temperature ⇒ equal currents. The mirror
cancels process shifts since both transistors move together.

### DC equations (ideal, matching)
```
I_ref = (V_CC − V_BE)/R
I_out = I_ref            (perfect match)
```
**Real (β-finite) correction:**
```
I_out = I_ref · (1 + 2/β)⁻¹        ≈ I_ref   (β ≫ 1)
```
The *base currents* of Q1 and Q2 add to `I_ref`: `I_ref = I_C + 2·I_B`. So:
`I_out = (β/(β+2))·I_ref`. For β=100, that's 0.98 of I_ref → error 2%.

### Ratio (mirror ratio)
Add emitter resistors R_E1, R_E2 to set a ratio:
`I_out ≈ (R_E1/R_E2)·I_ref` (emitter-current form). Equal emitters → 1:1.

### BJT mirror output resistance
`R_out = ro2` (Early effect of Q2). With `V_A = 100 V`, `I_out = 1 mA`:
`R_out ≈ 100 kΩ`. GATE: "the current source's output resistance" = `ro`.

---

## 17.2 MOS current mirror

```
   I_ref        I_out
    │             │
   ┌┼────┐   ┌────┼┐
   │     │   │     │
   D1◄───┤   D2◄──┤
   G1─┬───┴───G2    │ (tied gates)
    S1│         S2  │
      └───GND───┘
```
- Q1 in saturation, diode-connected → sets `V_GS1`.
- Q2 sees same V_GS → same `I_D` (matched, no body effect, λ=0 ideal).

```
I_ref = (V_DD − V_GS)/R
I_out = I_ref          (matched)
```

### With channel-length modulation (λ)
```
I_out = I_ref · (1 + λ·V_DS2)/(1 + λ·V_DS1)
R_out = ro2 = 1/(λ·I_D)
```
- If `V_DS2 ≠ V_DS1`, the output *different* (λ tilts it).
- **Output resistance is `1/(λ·I_D)`** — a MOSFET current source in a
  differential amp gets its finite `ro` from exactly this.

### Ratio via W/L sizing
`I_out/I_ref = (W2/L2)/(W1/L1)` — trivially adjustable on chip. GATE may give
W/L values and ask the ratio.

### Compliance
The *compliance* (allowed voltage at the output node while still acting as a
source):
- MOS: `V_D2 must keep M2 in saturation` → `V_out ≥ V_GS2 − V_th` (or with the
  1-transistor source, above `V_GS`). Below it, current collapses/sourced slot.
- BJT: keep `V_CE2 ≥ V_CE(sat) ≈ 0.2 V` → compliance ≈ ~0.2 V (great for low
  headroom). MOS compliance usually a little higher (a V_GS or so).
- GATE: "which current source has lower minimum output voltage?" → BJT (≈0.2 V).

---

## 17.3 Current sink vs source

- **Sink:** current *into* the node (NPN/NMOS mirror on the low side).
- **Source:** current *out* to a load (PNP/PMOS mirror on the high side).
- The tail of a differential pair is usually an NMOS/NPN **sink**.

---

## 17.4 Improved mirrors (why they exist — GATE asks "purpose?")

| Mirror | Fix |
|--------|-----|
| Basic | reference current subject to β / λ / Vth mismatch |
| **Wilson** | boosts output R (vs beta-dependent miroir) — high R_out at the output |
| **Widlar** | creates a *small* output current from a larger reference; emitter resistor R_E in Q2; `I_out·R_E = V_T·ln(I_ref/I_out)` |
| **Cascode** | stacks transistors → very high output R (mini-Miller shields) |

Know: *Wilson* → very high output resistance. *Widlar* → small current from
large ref via R_E. *Cascode* → high R_out + better matching.

### Widlar formula (worth memorizing)
```
I_out = (V_T/R_E)·ln(I_ref/I_out)        (solved iteratively)
```
Used when you need a µA-level current source; a V_T·ln term = classic.

---

## 17.5 Bias current sources in practice

- Differential amplifier tail current (Chapter 18) is set by a mirror: the tail
  current is *stiff*, so common-mode gain → near 0, CMRR huge.
- Op-amp input-stage tail & active loads are mirrors.
- "Active load" (Q2 as a current source instead of resistor R_C) = the mirror
  output — gives high gain `gm·ro` from a single stage.

---

## Worked example — BJT mirror, finite β

`V_CC = 10 V`, `R = 9.3 kΩ` (so I_ref ≈ 1 mA with V_BE=0.7), β = 100.
- `I_ref = (10 − 0.7)/9.3k ≈ 1 mA`.
- Each base current = I_ref/(β+2) ≈ 9.8 µA.
- `I_C2 = I_ref·β/(β+2) ≈ 0.98 mA`.
- Error ≈ 2%. If Q2 has no collector load, output feeds mirror right.

## Worked example — MOS mirror, W/L ratio

`(W/L)1 = 5`, `(W/L)2 = 20`, I_ref = 2 mA, λ = 0, matched.
- `I_out = 2·(20/5) = 8 mA`.

---

## GATE traps (current mirrors)

1. The base/gate voltages are **tied**; matching is assumed. Don't re-solve
   V_BE per transistor.
2. Finite β: mirror `I_out = I_ref·β/(β+2)`. For BJT only (MOS no base current).
3. `R_out` of a mirror ≈ `ro` (1/(λI_D), V_A/I_C) — not zero.
4. λ tilts the mirror when V_DS differ: `λ≠0` → include the correction.
5. Widlar: output set by R_E and the V_T·ln ratio, NOT by resistor division.
6. Compliance: keep the output device in active/saturation; below 0.2 V (BJT)
   the mirror dies.

---

## 5-question self-check

1. Mirror makes I_out ≈ ? → *I_ref (matched).*
2. β=49, BJT mirror I_out/I_ref? → *49/51 ≈ 0.96.*
3. MOS mirror R_out? → *1/(λI_D).*
4. W/L ratio 3:1 for 1 mA I_ref → *3 mA.*
5. Widlar's special job? → *tiny I_out from big I_ref.*

Next: **`18-Differential-Amplifiers.md`**