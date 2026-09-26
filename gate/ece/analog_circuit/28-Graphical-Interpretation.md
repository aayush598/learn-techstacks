# Chapter 28 — Graphical Interpretation (Reading Curves & Waveforms)

> **The idea in one line:** GATE draws curves not circuits. Every exam has
> several questions of the form "which graph is correct?" or "what does this
> Bode plot tell you?" This chapter trains you to read each type instantly.

---

## 28.1 Diode I–V curves

```
   I  │        /  (exponential forward)
      │       /
      │      /
      │     /
  ────┴──/──┴───────── V
      │ /   V_γ (~0.7)
      │/__ tiny reverse current
    ──┴── breakdown at −V_z (vertical)
```
Read:
- **Knee / cut-in** = where forward conduction starts (0.7 V Si, 0.3 Ge).
- **Slope near a point** = 1/dynamic resistance: steeper → smaller r_d.
- **Vertical line at −Vz** = Zener breakdown (used in regulation).
- GATE: "at which point is diode's dynamic resistance smallest?" → farthest
  up the forward curve (steepest).

---

## 28.2 BJT input & output characteristic families

### Input: `I_B` vs `V_BE` (diode-like)
- Exponential, turn-on ≈ 0.5–0.6 V, "knee" 0.7 V. Straightly rises into the
  operating region.
- At a fixed `I_B`, `V_BE` changes little (−2 mV/°C — the temperature line).

### Output: `I_C` vs `V_CE`, family of `I_B`
```
   I_C
   │   (saturation-like region up to V_CE(sat)~0.2V, the "ankle")
   │          /  <- I_B = 80µ
   │      /  /   <- 60µ
   │   /‾‾/     <- 40µ  (flat active region! InC = β·I_B)
   │  / /       
   │ /          <- slope shows ro (Early effect)
   └────────────────────────── V_CE
```
- **Flat active region** → collector behaves as current source (`I_C` almost
  V_CE-independent). Slope = 1/ro (Early voltage).
- **Family spacing** = β: `ΔI_C/ΔI_B`.
- **The "ankle" (knee)** marks the boundary into saturation at small V_CE.
- Q-point = where DC load line crosses the family member for that I_B.

---

## 28.3 MOSFET output & transfer characteristics

### Output: `I_D` vs `V_DS`, family of `V_GS`
```
   I_D
   │      ╱  (saturation, flat; higher V_GS = higher line)
   │   ╱╱
   │╱╱ (triode, parabolic)
   └─────────────── V_DS
       └── back parabola boundary V_DS = V_GS − V_th
```
- Left region (before knee) = triode/linear — nearly proportional to V_DS →
  drain acts like a resistor.
- Right region (after knee) = saturation — flat: current source.
- Boundary line `V_GS − V_th` shifts right as V_GS increases.
- Slope of flat part = 1/ro (λ).

### Transfer: `I_D` vs `V_GS`
- Parabola starting at `V_th`. `I_D=½k(V_GS−V_th)²`.
- GATE: "the slope of the transfer curve at a point" = gm. Steeper = higher gm.

---

## 28.4 Load lines (DC and AC)

- **DC load line** in `(V_CE, I_C)` space: intercepts `V_CC` and
  `V_CC/R_total(DC)` — slope `−1/R_DC`.
- **AC load line:** steeper (uses R_AC = R_L∥R_C); passes *through Q*.
- Q + AC line → max swing: halve the distance to either clipping endpoint.
- Read-off questions:
  - "Maximum unclipped peak-to-peak output ≈ ?" → 2×min(Q distance to
    saturation, Q distance to cutoff) endpoints.
- Zero-signal / operating point: the Q marks the idle (signal = 0) point.

---

## 28.5 Bode magnitude plots (gain vs frequency, log scale)

```
 dB
  │
  │    ────── A_m (flat, 0 dB/dec) ───────
  │           │            ↖  -20 dB/dec (1 pole)
  │           │                 ↖ -40 dB/dec (2 poles)
  └───────────┴─────────────── f (log)
           f_L (high-pass knee)   f_H (low-pass knee)
```
- Flat midband = A_m. Slopes of 20/40 multiples of dB/dec tell total poles.
- Each *low* pole (f_L side): −20 dB/dec below corner: clearly marked as a
  *high-pass* roll (rising to flat).
- Each *high* pole: −20 dB/dec above f_H: low-pass roll.
- GATE: "how many poles does this have?" → count slope segments /20.
- Phase plots: −45° per pole at corner; −90° total far beyond (single pole).
  (Bode phase: start 0°, bend at f_c, asymptote −90° one pole.)

---

## 28.6 Op-amp transfer characteristic

```
  v_o
 +V_sat │  ┌─────────────  (flat at rail)
        │  │
        └──┼───────────────► v_id
           │ (vertical-ish transition across 0)
 −V_sat ───┴─
```
- Steep transition between rail-to-rail in the *side* = open-loop gain is the
  slope (very steep). 
- The flat rail = saturation (no more gain).
- **With feedback the op-amp's transfer looks different** (input→output
  straight through); the raw open-loop picture is this comparator-like one.

---

## 28.7 Schmitt hysteresis loop

```
  v_o
 +V_sat ─────┐
            │           ← rising input up to UT flips HIGH? no (refer
            │                    to transfer). Loop displays both paths:
            └───────► v_in
                  ↑ (travel direction = input history)
 −V_sat
```
- The loop's two vertical edges at `UT` and `LT`.
- Width = hysteresis `2·V_sat·R1/R_f`.
- A sine fed in produces a square with edges *only* at those two levels —
  that's the hysteresis snapshot GATE likes.

---

## 28.8 Clipper/clamper/rectifier waveforms (draw before answering)

Propagate **half by half**:
- **Clipper:** draw input; shave above (below) the clamp line; the flat equals
  the reference.
- **Clamper:** draw input; translate entire waveform up/down so one extreme
  touches the reference. Shapes preserved.
- **Rectifier:** only keep certain half-cycles. HWR keeps 1 half (DC Vm/π);
  FWR both (2Vm/π); capacitor adds ripple ripple sag.
- **Integrator/differentiator mapping** (Chapter 21): square→triangle;
  triangle→square; square→spikes; triangle→parabola. Direction & sign matter.

---

## 28.9 Oscillator output waveforms

- **Sinusoidal RC/LC:** clean sine at f_o, amplitude stabilized (soft limiting).
- **Relaxation:** square output of Schmitt + triangle from the integrator cap.
- **Phase-shift:** sine, gain ~settling, no nice square.
- Read: centers ±V_sat rails; frequency spacing on time axis ↔ period.

---

## GATE traps (graphical reading)

1. **Family spacing for MCQs:** In BJT output curve, line spacing *directly*
   reads β. Count and divide.
2. Boundaries: the *knee* = saturation/triode boundary; don't call the flat
   part "saturation."
3. Bode pole counting: slope /20 = order — a 40 dB/dec drop means 2 poles, not
   "bigger gain."
4. Hysteresis loop direction (CW/CCW) encodes inverting vs non-inverting
   Schmitt — trace it.
5. Load line: DC line uses R_DC alone; AC line is steeper and passes through Q.
6. Clamper changes DC level, NOT amplitude; clipper changes amplitude, NOT
   DC — the shape tells which.

---

## 5-question self-check

1. Slope of BJT active line? → *1/ro (Early effect).*
2. MOSFET triode region resembles? → *a resistor.*
3. Bode 40 dB/dec = how many poles? → *2.*
4. Op-amp open-loop transfer "vertical" region? → *huge gain.*
5. Square from a Schmitt fed by sine appears at? → *UT/LT edges only.*

Next: **`29-Formula-Sheet.md`**