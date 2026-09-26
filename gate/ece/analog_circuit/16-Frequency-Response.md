# Chapter 16 — Frequency Response of Amplifiers

> **The idea in one line:** amplifiers do not have one fixed gain. Capacitors
> (coupling/bypass) kill the low end; internal transistor capacitances kill the
> high end. The flat middle band is the "midband gain." Learn the three regions,
> the two cutoffs, and the **Miller effect** — the single most-examined
> high-frequency concept in GATE analog.

---

## 16.1 The universal gain vs frequency picture

```
│A_v│  (dB)
  A_m ─────────────────────. midband (flat)
  40dB│    │               │
      │ 20dB/dec           │  -20dB/dec
      │   (low-freq roll)  │   (high-freq roll)
   ───┴───┬───────────┬────┴─── f
        f_L          f_H
```
- **Midband gain** `A_m`: the flat, "intended" gain.
- **Lower cutoff** `f_L`: gain drops 3 dB below at this frequency (amplifier
  useless below).
- **Upper cutoff** `f_H`: gain drops 3 dB at this frequency.
- **Bandwidth (BW)** `= f_H − f_L` (≈ f_H when dc-coupled, since f_L small).
- -3 dB point ⟺ gain = A_m/√2 ⟺ in dB, 3 dB down.

Poles vs zeros:
- Each **high-pass** pole (coupling/bypass cap) contributes `20 dB/dec` rolloff
  below its frequency and `+45°/decade` phase lead.
- Each **low-pass** pole (internal cap) contributes `20 dB/dec` rolloff above
  and `−45°` phase lag at the corner.

---

## 16.2 Low-frequency response — what sets f_L

Three capacitors (Ch 10) matter, each making a high-pass pole:

```
f = 1/(2π · C · R_effective)
```
| Cap | R_effective | Note |
|-----|-------------|------|
| Input coupling C1 | R_s + R_in | R_in includes bias resistors ∥ rπ (or R_G) |
| Output coupling C2 | R_out + R_L | typically dominant at output |
| Emitter/source bypass C_E/C_S | re + (R_B/(β+1)) [BJT]; 1/gm + R_S.. [MOS] | NOT R_E alone! |

**Dominant-pole rule:** the biggest f sets the overall low-cutoff:
`f_L ≈ max(f1, f2, fE)` (rough). The exact combination for multiple unequal
poles ≈ `√(f1² + f2² + ...)` (root-sum-square) if they're close.

### Why "sound gets thin" at low frequencies
Fewer bass signal components pass through the high-pass coupling caps — gain
drops. A bigger coupling C lowers f_L (extends bass).

---

## 16.3 High-frequency response — internal capacitances

Every transistor has internal (parasitic) capacitances:

**BJT (hybrid-π, high-frequency version):**
- `Cπ` between base and emitter (diffusion + junction cap).
- `Cμ` between base and collector (Miller-transformed, usually the villain).
- `ft` (transition frequency) ≈ `gm/(2π(Cπ + Cμ))`.

**MOSFET:**
- `Cgs`, `Cgd`, `Cdb`, `Csb` (overlap + junction caps).
- `ft ≈ gm/(2π(Cgs + Cgd))`.

Rules:
- The **input** node sees `Cgs` and the Miller-multiplied `Cgd`.
- The **output** node sees `Cds/Cdb`.
- Each forms an RC low-pass pole → `f_H`.

### Upper-cutoff derivations (the ones GATE actually asks)
For a CE/CS stage:
```
f_H ≈ 1/(2π·R_eff·C_tot)
```
where `R_eff` = source + input resistance seen into the device, `C_tot` = input
capacitance including Miller. Higher R_eff → lower f_H; higher C_tot → lower
f_H, so **adding source resistance lowers bandwidth**.

---

## 16.4 Miller effect (memorize the multiplication!)

**Miller theorem:** impedance `Z` between the inverting amplifier's input and
output (gain `−A`) appears, seen from the input, as `Z/(1+A)`, and from the
output as `Z/(1+1/A)`.

For a capacitor `C`, seen from the **input**:
```
C_Miller = C·(1 + A)      (amplified!)
```
And on the output side: `C_out ≈ C·(1 + 1/A) ≈ C` (usually negligible).

**Where it bites:**
- CE and CS amplifiers (inverting): `Cμ` or `Cgd` (small, 1–5 pF) multiplied by
  `(1 + gain)` — with gain 100 → 100×0.5pF = hundreds of pF → **slams f_H**
  down. This, not the device alone, limits bandwidth.
- `f_H ≈ 1/(2π · R_s(sig) · (C_in + (1+|A|)·Cμ))`.

### Why CB/CG avoids Miller
The base/gate is AC-grounded; the cap between input and output nodes is not
amplified because the input node voltage doesn't swing against the output. This
is **the** reason cascodes/current buffers exist.

---

## 16.5 Cascode / Widlar-style fixes (GATE questions)

- **Cascode** (CS/CB, common-gate output shield) removes the Miller blowup from
  the output side: the CG middle stage's input is at a *virtual-impedance-cut*
  node, so the Cgd path isn't multiplied. Result: f_H far higher, same gain.
- **Widlar / cascode with degeneration** — further linearity.

---

## 16.6 Bandwidth of cascaded identical stages

Each stage's f_H halves (roughly) with every identical stage:
- Single stage −3dB at f_H.
- Two identical stages: overall `f_H,total ≈ f_H·√(√2−1) ≈ 0.644·f_H`.
- N stages: `f_H = f_H_single·√(2^(1/N) − 1)`.
- Same story at low frequencies for the low-cutoff (pushes higher).
- **Gain-bandwidth product** (GBW): `A_m·BW ≈ constant` for a single dominant
  pole — raising gain lowers bandwidth (and vice-versa).

---

## Worked example — Miller

CE amp, gain `A_v = −50`, `Cμ = 2 pF`, `R_s = 1 kΩ`, `R_in = 2 kΩ`,
`Cπ = 20 pF` (included). Find f_H.

- `C_Miller = 2p·(1+50) = 102 pF`.
- `C_tot = Cπ + 102p = 122 pF`.
- `R_sig = R_s ∥ R_in? No — R_sig = R_s + (R1∥R2∥rπ)? ` For the source
  side: `R_source = 1 kΩ`, plus `R_in = 2 kΩ` — an input node at the base
  splits: total R to charge C_tot ≈ `R_s∥R_in ≈ 0.67 kΩ`, but more exactly for
  a *voltage* source: `R_char ≈ (R_s) ∥ (input R)`... Take `R_char ≈ 0.67 kΩ`:
- `f_H ≈ 1/(2π·670·122p) ≈ 1.94 MHz`.
- Without Miller (CB) the same cap at the base just Cπ, f_H ≈
  `1/(2π·670·20p) ≈ 11.9 MHz` — the 6× improvement says everything.

---

## GATE traps (frequency response)

1. Miller multiplies **`(1+|A|)`**, not `A`. Sign of gain irrelevant (use
   magnitude).
2. Miller is inverting stages only (CE/CS). CB/CG/CD/CC don't get it.
3. f_L is set by c**oupling/bypass** caps; f_H by **internal** caps. Never
   blame the external caps for HF.
4. R_E (the emitter resistor) is *not* the resistance in the bypass pole —
   it's `re + R_B/(β+1)`.
5. Bandwidth of N identical stages: f_H drops; don't pretend multiplication.
6. GBW constant only for single-pole — real multi-pole amps violate it; GATE
   expects the single-pole version.

---

## 5-question self-check

1. Which capacitor class sets f_L? → *coupling/bypass.*
2. Miller capacitance value for gain −100, C = 1 pF? → *101 pF.*
3. Which config avoids Miller? → *CB/CG.*
4. Two identical stages, single f_H = 1 MHz: overall f_H? → *≈ 0.644 MHz.*
5. Gain up 2× with a fixed dominant-pole BW product → BW? → *halved.*

Next: **`17-Current-Mirrors.md`**