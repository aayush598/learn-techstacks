# Chapter 10 — AC Coupling

> **The idea in one line:** coupling capacitors let the AC signal pass from
> stage to stage (or source to amplifier) while *blocking the DC*. Bypass
> capacitors let the AC signal avoid a resistor while keeping its DC bias.
> Together they decide the **low-frequency** behaviour of every amplifier.

---

## 10.1 What coupling and bypass capacitors do

Three typical capacitors in a transistor amplifier:

```
  input     C1 ──┤ base            (coupling: pass signal, block DC)
  supply V_B: (divider) → B
  emitter: ─ R_E ─ C_E ─ GND      (bypass: remove R_E from AC path)
  collector │ C2 ──► output        (coupling: pass signal to load, block DC)
```
- **Coupling capacitor (C1, C2):** in *series* with the signal path; blocks DC
  between stages/source/output; acts as a **high-pass filter**.
- **Bypass capacitor (C_E):** across (in *parallel* with) R_E; at midband it is
  a short, so the signal *bypasses* R_E; at low frequency it opens, so R_E
  comes back — this *also* creates a high-pass pole.

### The DC / AC split view
- **DC analysis:** capacitors are **open** — remove them; only DC paths matter.
- **Midband AC analysis:** capacitors are **short** — R_E bypassed, coupling
  passes everything.
- **Low-frequency AC:** capacitors add **poles** (high-pass behaviour) — gain
  rolls off below ~the cutoff frequency.
- **High-frequency AC:** transistor internal capacitors matter (Chapter 16).

---

## 10.2 DC blocking — why we couple AC

- Every stage wants its *own* Q-point; direct coupling would push DC into the
  next stage's base and ruin its bias.
- The coupling capacitor passes signal but blocks the DC offset; next stage sees
  only an AC waveform riding on its *own* bias.
- Sign squeeze: GATE asks "the DC component of the signal at the output
  terminal is?" — with capacitor coupling, answer: 0 (or the next stage's DC,
  not the source's DC).

### Voltage divider for DC bias but AC block
Remember in bias network `R1, R2`: in DC the base sees `V_th = V_CC·R2/(R1+R2)`;
for AC the base feeds into `R1∥R2` — these resistors ALSO load the AC input
(they appear in `R_in`). The coupling capacitor in front isolates the *source*
from that DC path.

---

## 10.3 Low-frequency response peaks (poles) of a CE stage

Each coupling/bypass capacitor forms an RC **high-pass** with an associated
frequency:

| Capacitor | Charging/discharge resistance | Cutoff (3-dB frequency) |
|-----------|------------------------------|---------------------------|
| Input coupling C1 | `R_s + R_in(stage)` | `f1 = 1/(2π·C1·(R_s+R_in))` |
| Output coupling C2 | `R_out + R_L` | `f2 = 1/(2π·C2·(R_out+R_L))` |
| Emitter bypass C_E | `R_E ∥ (re + (R_s+R_B)/(β+1))` | `fE = 1/(2π·C_E·R_eq)` |

Rules:
- Below each such frequency, gain falls at `20 dB/decade` (one pole).
- With several poles, each adds another 20 dB/decade of rolloff.
- **Dominant pole:** the largest of the cutoff frequencies dominates the
  overall -3 dB point (roughly max of f1, f2, fE).
- **Rule of thumb:** choose each coupling cap so its cutoff ≈ 1/10 of the
  lowest signal frequency → ~1 dB loss at that signal frequency.

---

## 10.4 The "emitter bypass" effect (revisited)

- Midband: `C_E` short → R_E gone → **maximum gain** `A_v = −gm·(R_C∥R_L)`.
- Low freq: `C_E` opens → R_E reappears → gain collapses toward
  `−R_C/R_E` (low).
- This *extra* gain collapse at low f is because of `C_E`’s high-pass action,
  even if C1, C2 were perfect — a subtle GATE favourite: **"which capacitor
  most limits low-frequency gain of the CE amplifier?"** → the *emitter
  bypass* (usually, if R_E is large).

Vary the problem:
- Removing `C_E` entirely (unbypassed) removes the extra pole and lower the
  midband gain (that high gain — R_E never bypassed at any frequency). The
  passband becomes flatter and wider but with smaller midband gain.

---

## 10.5 Cascade coupling networks

- **RC-coupled multistage:** each inter-stage cap + next-stage R_in = another
  high-pass pole. Total LF response = sum of all stages.
- **Direct coupling:** no caps → wider bandwidth at low end, but DC levels must
  be managed; used in ICs (op-amps), not in discrete discrete GATE problems
  unless so stated.
- The overall -3 dB frequency of `N` such cascaded equal poles:
  `f_total ≈ f_pole·√(2^(1/N) − 1)`⁻¹... i.e., lower than single pole. Prediction:
  more stages → lower low-cutoff (worse LF) and lower high-cutoff.

---

## Worked example — the bypass question

CE: `R_E = 1 kΩ`, `re = 25 Ω`, bypass `C_E = 10 µF`. Find freqs.

- `R_eq = re + (R1∥R2 ∥ ...)/ (β+1)` ≈ `re + R_B/(β+1)`.
  With `R_B = 20 kΩ`, β=200: `R_B/(β+1) ≈ 100 Ω`, so `R_eq ≈ 125 Ω`.
- `f_E = 1/(2π·C_E·R_eq) = 1/(2π·10µ·125) ≈ 127 Hz`.
- Above 127 Hz the bypass is effective.

Input coupling with `C1 = 0.1 µF`: `R_s + R_in ≈ 2 kΩ`:
- `f1 = 1/(2π·0.1µ·2k) ≈ 800 Hz` — this (not C_E) is the dominant LF pole.
- The amplifier's low-cutoff ≈ 800 Hz; high-cutoff set by transistor caps (Ch 16).

---

## 10.6 GATE traps (AC coupling)

1. **Capacitors: short (macro) in AC, open in DC.** Inverting these destroys
   every midband answer.
2. Each additional coupling/bypass cap = one more LF pole = a **high-pass**; it
   does NOT roll off the high end.
3. The emitter bypass affects a **specific** pole; a "low output" at bass
   frequencies usually points at C_E.
4. "Why does a guitar amp sound thin below 100 Hz?" — because low-cut moves up.
5. Do not count the *bypass* cap's `R_E` as just R_E — the equal impedance is
   ≈ `re + (R_B/(β+1))`, *much* smaller than R_E; using R_E itself is a classic
   error (f_E ten times too big).
6. Cascading more stages moves *both* cutoffs inward (bandwidth shrinks).

---

## 5-question self-check

1. Coupling capacitor is, in DC analysis? → *open circuit.*
2. In midband AC? → *short circuit.*
3. Removing the emitter bypass does what to midband gain? → *drops it
   (≈ −R_C/R_E set instead of −gm·R_C).*
4. 3-dB low-frequency point caused by coupling cap C1 with 2 kΩ total resistance?
   → *1/(2π·C1·2k).*
5. The big resistor R_E in bypass-cap cutoff is NOT R_E, it's? → *re +
   R_B/(β+1).*

Next: **`11-MOSFET-Fundamentals.md`**