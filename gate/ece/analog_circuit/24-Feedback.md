# Chapter 24 — Feedback

> **The idea in one line:** take a (usually small) sample of the output and feed
> it back to the input. Negative feedback *trades gain for stability*, *widens
> bandwidth*, and *fixes input/output impedance*; positive feedback *boosts
> gain (and causes oscillation)*. Every op-amp and oscillator is feedback.

---

## 24.1 The block-diagram vocabulary

```
               ┌──────────────┐
 x_in ──┬─────►│ amplifier A  │───► x_o
        │      └──────────────┘
        │   β  │
        └──────┴──── fetch (feedback network β)
```
- `A` = open-loop (base) gain.
- `β` = feedback fraction (what fraction of output is fed back).
- `Loop gain` = `A·β` (gain around the loop).
- `A_f` = closed-loop (feedback) gain.

### Negative feedback — sign convention
The feedback subtracts from the input:
`x_in' = x_in − β·x_o` (negative) or `+β` (positive).

---

## 24.2 The canonical gain formula (derive, don't memorize)

For feedback where the effective input is `x_in − β·x_o`:
```
x_o = A·(x_in − β·x_o)
x_o·(1 + A·β) = A·x_in
→  A_f = A/(1 + A·β)
```
- **Negative feedback:** `A_f = A/(1 + Aβ)` (gain reduced by `(1+Aβ)`).
- **Positive feedback:** `A_f = A/(1 − Aβ)` (gain *increased*).
- `(1 + A·β)` = **return difference / desensitivity factor**.

### Deep feedback approximation
When `A·β ≫ 1`:
```
A_f ≈ 1/β        (gain set by the feedback network, not the amplifier!)
```
This is why op-amp closed-loop gain `= 1/β` (e.g., non-inv `1+Rf/R1` from the
divider ∝ 1/β) is accurate even though `A` wobbles.

---

## 24.3 Effects of negative feedback (the six famous ones)

| Effect | What happens | Quantified |
|--------|--------------|------------|
| Gain | Decreases | `A/(1+Aβ)` |
| Gain stability | Increases (desensitized) | variation ÷ `(1+Aβ)` |
| Bandwidth | Increases | `BW_f = BW·(1+Aβ)` (gain-BW constant) |
| Distortion/noise | Decreases | distortion ÷ `(1+Aβ)` |
| Input resistance | increases (series) or decreases (shunt) | depends on topology |
| Output resistance | decreases (voltage) or increases (current) | depends on topology |

**Gain–bandwidth product stays constant** for a single-pole amplifier:
`A·BW = constant` → raising feedback (lowering A_f) raises BW proportionally.

---

## 24.4 The four feedback topologies (input/output sense)

Classification by *what is sampled at the output* and *how it's mixed at the
input*:

| Sample at output | Mix at input | Name | Effect on R_in | Effect on R_out |
|------------------|--------------|------|----------------|-----------------|
| Voltage | Series | Series–shunt (voltage–series) | ↑ R_in | ↓ R_out |
| Voltage | Shunt | Shunt–shunt (voltage–shunt) | ↓ R_in | ↓ R_out |
| Current | Series | Series–series (current–series) | ↑ R_in | ↑ R_out |
| Current | Shunt | Shunt–series (current–shunt) | ↓ R_in | ↑ R_out |

**How to recognize:**
- *Sampling:* if a resistor senses the output *voltage* → voltage sampling;
  if it sits in series with the load sensing *current* → current sampling.
- *Mixing:* if it connects to a point where it adds to the input in series
  (voltage addition) → series mixing; if it feeds a current node (virtual
  ground) → shunt mixing.

**Memorize diagonally:**
- Voltage sampling → lowers R_out. Current sampling → raises R_out.
- Series mixing → raises R_in. Shunt mixing → lowers R_in.

### The four basic topologies mapped to common amps
- Non-inverting op-amp: **voltage-series** → R_in ↑, R_out ↓. ✓ (Sallen-Key
  input buffers, emitter followers).
- Inverting op-amp: **voltage-shunt** → R_in ↓ (≈R1), R_out ↓. ✓
- Common-source/-emitter with degeneration R_E/R_S: **current-series** →
  R_in ↑, R_out ↑ (this is why unbypassed R_E raises input R!). ✓
- Collector feedback (R_B from C to B): **voltage-shunt** — the classic
  self-bias stabilizer.

---

## 24.5 The four gain formulas (each topology)

| Topology | Closed-loop gain | Unit |
|----------|------------------|------|
| Series-shunt (voltage-series) | A_f = A/(1+Aβ) | V/V |
| Shunt-shunt (voltage-shunt) | A_f = A/(1+Aβ) | V/V (input at a node) |
| Series-series (current-series) | A_f = A/(1+Aβ) | A/V (transconductance) |
| Shunt-series (current-shunt) | A_f = A/(1+Aβ) | — but treat with care |

Practically: for GATE problems the same `A/(1+Aβ)` relation holds; the
differences show up as *which* R_in/R_out changed.
**Shortcut:** after solving, check: negative feedback always has the
`(1+Aβ)` factor and the resistors-compliance R_in/R_out story.

---

## 24.6 Positive feedback — oscillation and the Barkhausen criterion

- Positive: `A_f = A/(1 − Aβ)`.
- When `Aβ = 1` → denom → 0 → **unbounded gain** → self-sustaining oscillation
  (Chapter 25).
- **Barkhausen:** `|Aβ| = 1` and `∠Aβ = 0°` (360° loop phase). Then the loop
  sustains a sinusoid of exactly that frequency.
- Positive feedback also resurfaces in Schmitt triggers (regenerative).

---

## 24.7 Stability concept

- Feedback reduces stability risk when loop gain `Aβ` is high (desensitizes),
  but too much phase lag around the loop (from internal poles) can turn
  negative feedback *positive* at high frequency → oscillation.
- Phase margin: margin between the loop's phase and −180° at unity gain.
  Positive margin → stable; ≈ 60° typical.
- GATE (EE flavour) may ask "why does an op-amp oscillate?" → loop gain with
  excessive phase shift at crossover.

---

## Worked examples

**Q1.** A = 10⁵, β = 0.01.
- `A_f = 10⁵/(1+1000) ≈ 100` (deep feedback ≈ 1/β = 100). ✓

**Q2.** Non-inv op-amp, R1 = 1k, Rf = 9k: `β = R1/(R1+Rf) = 0.1`.
`A_f = 1/β = 10 = 1+Rf/R1` ✓ matches Chapter 20.

**Q3.** CE amp with unbypassed R_E (current-series). R_in rises from `rπ` to
`rπ + (β+1)·R_E`. That's the "R_in ↑" of series mixing made visible.

---

## GATE traps (feedback)

1. `A_f = A/(1+Aβ)` vs `A/(1−Aβ)` — the SIGN decides stabilisation vs
   oscillation. Don't swap.
2. Deep feedback `A_f ≈ 1/β`: a *non-inverting* op-amp = β = R1/(R1+Rf) →
   `1+Rf/R1`. The 1/β shortcut fails for inverting.
3. R_in/R_out effects depend on *topology* — "total feedback reduces gain and
   widens BW" ✔ but input/output R needs the sampling/mixing identification.
4. GBW constant: raising closed-loop gain (less feedback) *narrows* bandwidth;
   a favourite inversion.
5. Feedback reduces *distortion* and *noise introduced after*, not all noise;
   don't over-believe.

---

## 5-question self-check

1. Negative feedback formula? → *A/(1+Aβ).*
2. Effect on bandwidth? → *× (1+Aβ).*
3. Non-inv op-amp β? → *R1/(R1+Rf).*
4. Which mixes (series→R_in: ↑ or ↓)? → *series mixing raises R_in.*
5. Oscillation when? → *Aβ positive with |Aβ|≥1 (Barkhausen).*

Next: **`25-Oscillators.md`**