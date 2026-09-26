# Chapter 09 — BJT Amplifiers: CE, CB, CC

> **The idea in one line:** three ways to use a BJT amplifier. Each picks a
> different "ground" for the AC signal: **emitter** → Common-Emitter (inverting,
> high gain), **base** → Common-Base (non-inverting, low input impedance),
> **collector** → Common-Collector (buffer, gain ≈ 1). Learn the three gain and
> impedance signatures and everything else is recognition.

---

## 9.0 The three configurations — comparison first

| | Common-Emitter (CE) | Common-Base (CB) | Common-Collector (CC) |
|---|---|---|---|
| Input | Base | Emitter | Base |
| Output | Collector | Collector | Emitter |
| A_v | large, ~−gm·R_C (inverting) | large, +gm·R_C (non-inverting) | ≈ 1 (≤ 1) |
| A_i | ≈ β | ≈ α ≈ 1 | ≈ (β+1) large |
| R_in | ≈ rπ (mid) | ≈ re (very low) | ≈ (β+1)·(R_E∥R_L) huge |
| R_out | ≈ R_C (high) | ≈ R_C (high) | ≈ (R_s/β + re) low |
| Phase | 180° inversion | no inversion | no inversion |
| Typical use | voltage amplifier | high-frequency stage | buffer / impedance matching |

**How to recognize:** find which terminal is AC-grounded (capacitor to ground or
straight to supply). That terminal is the "common" one.

---

## 9.1 Common-Emitter amplifier

### Basic CE (no emitter resistor, bypassed `R_E`)
```
  +V_CC
   │
  R_C ───── C ───► v_out
   │        │
   │        B ───► v_in (through C1)
  R_E       │
  (bypassed)│ E ── C_E (bypass cap) ── GND
   │
  GND
```
- AC input at base, output from collector, emitter at AC ground.
- **Small-signal results (ro ignored):**
```
A_v = −gm·(R_C ∥ R_L)
R_in = R_B1 ∥ R_B2 ∥ rπ    (divider resistors; ignore if none: rπ)
R_out = R_C
```
- Phase inversion: output goes DOWN when input goes UP.

### CE with unbypassed emitter resistor `R_E` (source/emitter degeneration)
Only the *AC* presence of `R_E` matters — if no bypass cap, `R_E` appears in
series with the emitter in signal terms.
```
A_v = −gm·R_C/(1 + gm·R_E)            = −(R_C)/(R_E + 1/gm)
   ≈ −R_C/R_E                         (when gm·R_E ≫ 1)
R_in = R_B1∥R_B2∥(β+1)(re + R_E)      (huge!)
R_out = R_C
```
- Trade-off (GATE favourite): degeneration **reduces gain** but **improves
  linearity, increases input impedance, stabilizes the gain vs β/ro.**
- The ±: with R_E the gain becomes set by resistors (≈ R_C/R_E),
  not by gm (temperature sensitive). That's the whole point.

### Bypassed vs unbypassed
- **Bypass capacitor (C_E):** shorts R_E for AC at midband → R_E was removed
  from AC → full `−gm·R_C` gain.
- **Unbypassed:** R_E participates → moderate gain `−R_C/R_E` and high R_in.

GATE asks you to know what removing the bypass does: gain drops, input
resistance rises, bandwidth improves (less BLN?), the "CE with C_E removed" is
the standard midband question.

---

## 9.2 Common-Base amplifier
```
        V_out ─── C ─── (collector)
   v_in → E ── (via C1)         
        B ── C_B (bypass cap) ── GND
```
- Input at emitter, output at collector, base AC-grounded.

**Results:**
```
A_v = +gm·(R_C ∥ R_L)          (non-inverting!)
R_in = re || R_E_source ≈ re   (small, ~10–50 Ω)
R_out = R_C                    (high)
A_i ≈ α ≈ 1
```
- Non-inverting, high voltage gain, **low input impedance** — the signature.
- Great high-frequency behavior (no Miller effect, Chapter 16) → cascode.
- Current gain ≈ 1 (current buffer).

---

## 9.3 Common-Collector (emitter follower)
```
  +V_CC
   │
  (collector tied to supply)
  │
  B ──── v_in
  │
  E ──── R_E ─── GND
  │      └──► v_out
```
- Input at base, output at emitter, collector is AC ground (to V_CC is AC
  ground, since supplies are shorted).
- Output "follows" input minus a ~0 DC offset — unity gain buffer.

**Results:**
```
A_v = R_E/(R_E + re) ≈ 1         (but < 1; no inversion)
R_in = R_bias ∥ (β+1)·(R_E ∥ R_L)  (very high)
R_out = re + R_S/(β+1)             (very low)
A_i ≈ β+1
```
- **Summary: high R_in, low R_out, gain ≈ 1** — a level-shifting-unity buffer.
- Use it at the output stage to avoid loading a high-impedance source.

### Why R_out is low: intuitive
Emitter behaves like a voltage source following the base; the impedance looking
*into* the emitter node ≈ `re` plus anything in series at the base divided by
(β+1). Small.

---

## 9.4 Biasing generalization with R_E
Base-biased versions:
- DC Q-point: `I_B = (V_BB − V_BE)/(R_B + (β+1)R_E)`;
  `V_CE = V_CC − I_C(R_C + R_E)`.
- Signal: bypassed R_E vs not — the AC gain formula decides.
- For voltage-divider bias, `R_in` total includes `R1∥R2`.

---

## 9.5 Cascade (multistage) amplifiers

Two or more stages in series. Rules:
```
A_v(total) = A_v1 × A_v2 × ...     (multiply the *loaded* gains!)
```
- Each stage's load = next stage's R_in — this **loading** matters. Don't
  multiply *unloaded* gains.
- DC-blocking coupling caps between stages set each stage's DC independently.
- If gains are in dB: `A_tot[dB] = A1[dB] + A2[dB] + ...`
- Overall bandwidth narrows as you add stages (each pole adds).

**GATE example:** CE(Ampl) → CC(buffer). Stage 1 gain `−gm·(R_C∥R_in2)` — the
buffer's high R_in means it barely loads stage 1.

---

## 9.6 Extensive small-signal example (CE)

Given: `V_CC = 15 V`, `R1 = 100 kΩ`, `R2 = 25 kΩ`, `R_C = 4 kΩ`, `R_E = 1 kΩ`
(bypassed), `R_L = 4 kΩ`, `β = 200`, `V_BE = 0.7 V`, `V_T = 25 mV`.

1. DC: `V_B = 15·25/125 = 3 V`; `I_C ≈ (3−0.7)/1k = 2.3 mA`.
2. `gm = 2.3m/25m = 92 mA/V`; `rπ = β/gm = 200/92m ≈ 2.17 kΩ`.
3. `R_in = R1∥R2∥rπ`: `100k∥25k = 20 kΩ`; ∥ 2.17k ≈ 1.96 kΩ.
4. `A_v = −gm·(R_C∥R_L) = −92m·2k = −184`.
5. `R_out = R_C = 4 kΩ`.

If `R_E` were *unbypassed*: `A_v = −184/(1+92m·1k)?` careful:
`A_v = −gm·R_C/(1+gm·R_E) = −92m·4k/(1+92) = −368/93 ≈ −3.96 ≈ −R_C/R_E = −4`.

---

## GATE traps (BJT amplifiers)

1. CE **inverts**. If a problem says "same phase as input," it's CB or CC.
2. `A_v = −gm·(R_C∥R_L)`. Always the load `R_L` counts — students use bare R_C.
3. **Loading of cascades:** a later stage's input resistance divides the
   previous stage's gain. Multiply loaded gains only.
4. Emitter follower `A_v` is NOT "1 with gain." It's `R_E/(R_E+re) < 1`.
5. CB input impedance `≈ re`, ~tens of Ω — GATE asks "identify the circuit with
   input resistance = re" → CB.
6. R_in signatures: CE ~rπ; CB ~re; CC huge. When values are given, compare.
7. The bypass capacitor presence flips CE gain between `−gm·R_C` (bypassed)
   and `−R_C/R_E` (unbypassed); check whether `C_E` exists in the figure.

---

## 5-question self-check

1. Which config has voltage gain ≈ 1 and huge input R? → *CC (emitter follower).*
2. Name the inverting config. → *CE.*
3. CB typical R_in? → *≈ re.*
4. Two CE stages (each −50, loaded correctly): net? → *2500 positive (two
   inversions → non-inverting), |A|=2500.*
5. CE with unbypassed R_E: effect vs bypassed? → *lower gain, higher R_in.*

Next: **`10-AC-Coupling.md`**