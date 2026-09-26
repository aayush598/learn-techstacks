# Chapter 06 — BJT Fundamentals

> **The idea in one line:** A BJT is a *current-controlled* device. A small
> base current `I_B` controls a large collector current `I_C = β·I_B`. It has
> four terminals of interest (E, B, C, and the substrate which we ignore), and
> it "turns on" as an amplifier when both junctions are biased correctly.

---

## 6.1 The NPN and PNP transistor

Three layers: two junctions. Structure:

```
NPN:     n  |  p  |  n            PNP:     p  |  n  |  p
      Emitter Base Collector          Emitter Base Collector
```
- **Emitter** (E): heavily doped, supplies the charge carriers.
- **Base** (B): thin and lightly doped; the "control" layer.
- **Collector** (C): moderately doped, large area; gathers the carriers.

Symbols:
```
NPN:        C              PNP:        C
        ▲  ◄  ▲                    ▼ ◄  ▼
          |                           |
          B              B ◄──────────┘ emitter arrow points TO base
          |`__ ▔ emiter arrow points OUT
```
The **emitter arrow direction** is the giveaway in diagrams:
- NPN: arrow points **away** from the base (emitter current flows out).
- PNP: arrow points **toward** the base.

---

## 6.2 Transistor currents and the α–β relations

Conventions (NPN): conventional current flows into the collector, out the
emitter, and small current into the base.

```
I_E = I_C + I_B                     (KCL at node / charge conservation)
```

### Current gains
- `α` (alpha), common-base current gain:
  `α = I_C / I_E` (typically 0.95–0.99).
- `β` (beta), common-emitter current gain:
  `β = I_C / I_B` (typically 50–300).
- Relationship:
  `β = α/(1 − α)`
  `α = β/(β + 1)`
- Also: `I_C = α·I_E = β·I_B`, `I_E = (β+1)·I_B`.

**Derivation check:** `I_E = I_C + I_B` → divide by `I_C`:
`1/α = 1 + 1/β` → `β = α/(1−α)`. ✓

### Reverse saturation current
`I_C = β·I_B + (β+1)·I_CBO` — `I_CBO` is the small collector–base leakage
(µA–nA). For ideal problems: `I_C = β·I_B`.

---

## 6.3 Operating regions (memorize the bias conditions)

| Region | E-B junction | B-C junction | What it does |
|--------|--------------|--------------|--------------|
| **Cutoff** | Reverse | Reverse | `I_C ≈ 0` — switch OFF |
| **Active (forward-active)** | **Forward** | **Reverse** | Amplifier mode: `I_C = β·I_B` |
| **Saturation** | Forward | Forward | `I_C` no longer β·I_B; `V_CE ≈ 0.2 V`, switch fully ON |
| Reverse-active | Reverse | Forward | Only used in logic analysis, rarely in analog |

### The amplifier condition
For an NPN to amplify in active region:
- Forward bias E-B: **V_BE ≈ 0.7 V** (silicon).
- Reverse bias B-C: **V_CB > 0**, i.e., collector more positive than base.
- Equivalent check: **V_C > V_B > V_E** (NPN active region).

For PNP (mirror image): **V_E > V_B > V_C**, with `V_EB ≈ 0.7 V`.

---

## 6.4 The transistor as a switch

- **Cutoff** (OFF): Both junctions reverse → `I_C ≈ 0`, `V_CE ≈ V_CC`.
- **Saturation** (ON): Both forward → `I_C` saturates at `≈ V_CC/R_C`;
  `V_CE(sat) ≈ 0.2 V`.
- Rule to test saturation: compute `I_B` and `β·I_B`;
  if `β·I_B > V_CC/R_C` then the transistor is **saturated** (can't deliver).

**GATE check:** "Which region does the circuit keep the transistor in?"
Compute `V_C`, `V_B`, `V_E`, compare. Active iff `V_C > V_B`.

### The transistor as an amplifier
- Operated in **active region**.
- Small `ΔV_BE` (through the base) → large `ΔI_C = gm·ΔV_BE` → large `ΔV` across
  `R_C`. This is signal amplification. More in Chapter 08/09.

---

## 6.5 BJT characteristic curves (must be able to sketch)

### Output characteristics (I_C vs V_CE, family of Ib)

```
 I_C
  │    saturation region
  │       /   active region (flat lines, one per I_B)
  │      /   /   /   /
  │     /   /   /   /        ← I_C = β·I_B (flat ⇒ output resistance high)
  │    /__/
  │   cutoff (I_C ≈ 0)
  └──────────────────── V_CE
         0.2V
```
- In active region, `I_C` is essentially flat (independent of `V_CE`) → the
  transistor behaves like a (controlled) current source.
- Slight upward slope in active = **Early effect** (finite output resistance).

### Transfer characteristic (I_C vs V_BE)
- Exponential in forward active (like a diode): `I_C ∝ e^(V_BE/V_T)`.
- Turn-on threshold ≈ 0.5–0.6 V; full conduction ≈ 0.7 V.

### Input characteristic (I_B vs V_BE)
- Diode-like: negligible until ≈ 0.5 V, then exponential; operating point at
  0.7 V.

---

## 6.6 Important parameters you'll use all chapter

- `gm = I_C / V_T` (transconductance) — large signal relationship.
- `rπ = β/gm` (base resistance in hybrid-π) — details in Chapter 08.
- `r_e = V_T/I_E ≈ V_T/I_C` (emitter resistance).
- `β` is *the* headline datasheet number; make shot-calls with it.
- Naming: `V_CC` = collector supply; `V_BB` = base supply; `V_EE` = emitter supply.

---

## Worked example

**NPN, β = 100. `V_BE = 0.7 V`. V_BB = 2 V, R_B = 100 kΩ, R_C = 2 kΩ, V_CC = 10 V.**
Classify the region.

1. `I_B = (V_BB − V_BE)/R_B = (2 − 0.7)/100k = 13 µA`.
2. `β·I_B = 100·13µ = 1.3 mA`.
3. If active: `V_C = V_CC − I_C·R_C = 10 − 1.3·2 = 7.4 V`.
4. Since `V_C = 7.4 V > V_B = 2 V` and E-B forward → **active region**. ✓
   (Output would clip only if collector got pulled below base.)

**Same but V_BB = 5 V:** `I_B = 43 µA`, `βI_B = 4.3 mA` →
`V_C = 10 − 8.6 = 1.4 V < V_B` → cannot stay active → **saturated**.
Actual `V_CE(sat) ≈ 0.2 V`.

---

## GATE traps (BJT fundamentals)

1. **β defined as `I_C/I_B`.** Some books define `h_FE` (large-signal) vs
   `h_fe` (small-signal) — for ideal GATE problems they are equal.
2. Active-region condition for NPN: `V_C > V_B > V_E`; if a numerical states
   `V_C = V_B`, the transistor is about to leave active (or saturated).
3. `I_C = βI_B` holds ONLY in active regions. In saturation replace by fixing
   `V_CE(sat) ≈ 0` and solving with circuits.
4. PNP voltages are mirror images: don't mix up signs of `V_EB`, `V_EC`.
5. Emitter current = `(β+1)I_B`, not `β·I_B` — appears in emitter-bias loops.
6. Leakage `I_CBO` doubles with temperature; in old exam questions about
   "temperature stability", it matters.

---

## 5-question self-check

1. `β = 99`. `α`? → *99/100 = 0.99.*
2. NPN, `I_B = 20 µA`, `β = 150`. `I_E`? → *I_C = 3 mA, I_E = 3.02 mA.*
3. Saturation condition? → *both junctions forward; V_CE ≈ 0.2 V.*
4. In which region is `I_C = β·I_B` valid? → *forward active.*
5. NPN in active requires? → *V_C > V_B > V_E.* (curve check V_CB > 0)

Next chapter: **`07-BJT-Biasing.md`**