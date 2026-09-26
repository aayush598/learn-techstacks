# GATE Analog Circuits — The Single Complete Resource (ECE)

**Read once, trust forever.** This is a self-contained, chapter-by-chapter guide
to the entire GATE EC Analog Circuits syllabus. It is written so that a single
careful reading is enough to solve GATE-level problems. No other book, video, or
notes are required.

---

## What this resource covers

This resource follows the **official GATE (EC) Analog Circuits syllabus**:

> Diode circuits: clipping, clamping and rectifiers; BJT and MOSFET amplifiers:
> biasing, AC coupling, small-signal analysis, frequency response; current
> mirrors and differential amplifiers; op-amp circuits: amplifiers, summers,
> differentiators, integrators, active filters, Schmitt triggers and oscillators.

…expanded into every subtopic the exam actually asks. Every concept is built
with an **intuition first**, then the **formula**, then a **GATE-style example**,
then a **"traps to avoid"** box.

---

## Chapter map (read in this order)

| # | File | Covers |
|---|------|--------|
| 00 | `00-Start-Here.md` | This file. How to read, roadmap, marking strategy |
| 01 | `01-Prerequisites.md` | Ohm's law, KCL/KVL, Thevenin/Norton, phasors, complex impedance, dB, calculus |
| 02 | `02-Diodes-Basics-and-Models.md` | PN junction, I-V curve, Shockley eq, ideal / CVR / piecewise / small-signal models, Q-point |
| 03 | `03-Clipping-Circuits.md` | Series/shunt, biased, two-level clippers, waveform analysis |
| 04 | `04-Clamping-Circuits.md` | Positive/negative/biased clampers, cycle-by-cycle analysis, RC constant |
| 05 | `05-Rectifiers.md` | Half-wave, centre-tap, bridge, capacitor filter, ripple, PIV, efficiency |
| 06 | `06-BJT-Fundamentals.md` | NPN/PNP, α–β, regions, transistor as switch/amplifier |
| 07 | `07-BJT-Biasing.md` | Fixed, collector-to-base, emitter, voltage-divider bias, Q-point, stability |
| 08 | `08-BJT-Small-Signal-Models.md` | Hybrid-π, T-model, gm, rπ, re, ro, all relationships |
| 09 | `09-BJT-Amplifiers.md` | CE, CB, CC; gains, resistances, emitter degeneration, cascades |
| 10 | `10-AC-Coupling.md` | Coupling/bypass capacitors, DC blocking, low-frequency behaviour |
| 11 | `11-MOSFET-Fundamentals.md` | NMOS/PMOS, enhancement/depletion, regions, channel-length modulation, body effect |
| 12 | `12-MOSFET-Biasing.md` | Fixed-gate, drain-feedback, voltage-divider, current-source bias, Q-point |
| 13 | `13-MOSFET-Small-Signal-Model.md` | gm, ro, body effect, CS/CG/CD analysis prep |
| 14 | `14-MOSFET-Amplifiers.md` | CS, CG, CD; source degeneration; gains and resistances |
| 15 | `15-BJT-vs-MOSFET.md` | Direct comparison table + how to identify a circuit |
| 16 | `16-Frequency-Response.md` | Midband, lower/upper cutoffs, dominant pole, Miller effect, bandwidth |
| 17 | `17-Current-Mirrors.md` | BJT mirror, MOS mirror, ratio, output resistance, compliance, beta effect |
| 18 | `18-Differential-Amplifiers.md` | Differential pair, diff/common gain, CMRR, BJT and MOS |
| 19 | `19-Op-Amp-Fundamentals.md` | Ideal vs practical op-amp, virtual short, offset parameters, saturation |
| 20 | `20-Op-Amp-Amplifiers-Summers.md` | Inverting, non-inverting, follower, summers, scaling |
| 21 | `21-Op-Amp-Integrators-Differentiators.md` | Ideal/practical integrator and differentiator, waveforms, ramp, frequency limits |
| 22 | `22-Active-Filters.md` | LPF, HPF, BPF, notch, Sallen-Key, Butterworth, Q, order, cascading |
| 23 | `23-Schmitt-Trigger-Comparators.md` | Comparator, zero-crossing detector, hysteresis, thresholds, transfer curve |
| 24 | `24-Feedback.md` | Positive/negative feedback, loop gain, effects on gain/BW/resistances |
| 25 | `25-Oscillators.md` | Barkhausen, RC (phase-shift, Wien), LC (Colpitts, Hartley), relaxation, square/triangular |
| 26 | `26-Transistor-as-Switch.md` | BJT/MOSFET switching, cutoff/saturation, ON-OFF states |
| 27 | `27-DC-and-AC-Analysis-Method.md` | Step-by-step method for ANY transistor amplifier (the master method) |
| 28 | `28-Graphical-Interpretation.md` | I-V curves, load lines, Bode plots, hysteresis, waveforms — read any graph |
| 29 | `29-Formula-Sheet.md` | Every formula in the subject on one page |
| 30 | `30-Priority-Checklist.md` | Mark off chapters; "must know" vs "good to know" |

---

## Marking strategy / how much time

- **GATE EC 2027 pattern:** General Aptitude ~15 marks, Engineering
  Mathematics ~13 marks, Technical ~72 marks. Analog Circuits is one of the
  biggest single scoring blocks inside that 72.
- Typical GATE paper asks **8–12 questions** from analog circuits: 2–3 diode
  circuit waveform questions, 2–4 transistor amplifier numericals, 1–2 current
  mirror / differential pair, and 3–5 op-amp circuit questions.
- Strategy: master chapters **02 → 09, 19 → 25** first (they carry ~80% of the
  marks). Everything else supports those.

## How to read a chapter

1. Read the **"The idea in one line"** callout first.
2. Then the intuition + formulas.
3. Do the worked examples **by hand** on paper (do not skim them).
4. Read the **"GATE traps"** box last — this is where average students lose marks.

## Conventions used in this resource

- `R_in`, `V_CE`, `gm` — subscripts written inline for plain-text rendering.
- Greek: `β` (beta), `α` (alpha), `λ` (lambda), `ω` (omega).
- "Q-point" always means the DC operating point (`I_C`, `V_CE` for BJT;
  `I_D`, `V_DS` for MOSFET).
- All formulas are derived intuitively, so you can re-derive any of them in the
  exam hall instead of memorizing.

---

## Prerequisite check (5-minute self-test)

Before you start Chapter 01, be sure you can answer these instantly:

1. KCL says the sum of currents *into* a node = ? → *(sum of currents out)*
2. Thevenin equivalent = voltage source in series with resistor. Norton =
   current source in parallel with resistor.
3. Impedance of a capacitor = `1/(jωC)`; behaves open at DC, short at very high f.
4. `20·log10(100) = 40 dB`.
5. `d/dx (sin ωx) = ω·cos ωx`.

If any answer is slow, spend 20 minutes on Chapter 01 before anything else.

**Now go to `01-Prerequisites.md`.**