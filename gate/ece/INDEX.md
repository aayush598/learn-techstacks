# GATE ECE — Complete Question Bank

> A question-only self-study resource. **No notes required.** Every question carries
> its own full solution, so reading top-to-bottom from Part 1 of any subject to its last
> file covers that subject completely.
>
> Format contract: see [`STYLE_GUIDE.md`](STYLE_GUIDE.md).

## How to use this

1. Pick a subject directory.
2. Read/attempt the questions **in file order, in sequence**. The files are ordered as a
   syllabus, and each file assumes the previous one.
3. Attempt before opening the `> **Answer:**` line. Cover it with your hand.
4. Finish a file, then drill only its `## Quick revision` bullets.
5. Do a final pass over every file's Quick revision the night before the exam.
6. For GATE-format practice, mark the questions typed `GATE-1` / `GATE-2` and answer
   them MCQ/NAT-style without writing full solutions.

## GATE ECE paper structure (context)

| Part | Content | Questions |
|---|---|---|
| Section A | General Aptitude | 10 |
| Section B | Engineering Mathematics | 10 |
| Section C | ECE core (choose 3 of 5) | 28 |

Subject weightage is not fixed — GATE ECE lets you pick **any 3** of the 5 offered
section-C papers. So you should be strong in at least 3, and ideally know which 3 you
attempt. Section C papers are usually drawn from clusters like
{Signals & Systems, DSP, Communication, Digital} / {Analog, Circuits, VLSI, Devices} /
{Machines, Power Electronics, Power Systems, Control, EM}.

---

## Subject directories

| # | Directory | Subject | Files | Target Qs |
|---|---|---|---|---|
| 1 | [`01_engineering_mathematics/`](01_engineering_mathematics/) | Engineering Mathematics | 5 | 1200+ |
| 2 | [`02_general_aptitude/`](02_general_aptitude/) | General Aptitude | 5 | 1000+ |
| 3 | [`03_circuit_theory/`](03_circuit_theory/) | Network / Circuit Theory | 5 | 1100+ |
| 4 | [`04_signals_and_systems/`](04_signals_and_systems/) | Signals & Systems (+ DSP) | 5 | 1200+ |
| 5 | [`05_analog_circuits/`](05_analog_circuits/) | Analog Circuits | 5 | 1100+ |
| 6 | [`06_digital_circuits/`](06_digital_circuits/) | Digital Circuits | 5 | 1100+ |
| 7 | [`07_computer_organization/`](07_computer_organization/) | Computer Organization & Architecture | 5 | 1000+ |
| 8 | [`08_electrical_machines/`](08_electrical_machines/) | Electrical Machines | 5 | 1100+ |
| 9 | [`09_power_electronics/`](09_power_electronics/) | Power Electronics | 5 | 1100+ |
| 10 | [`10_power_systems/`](10_power_systems/) | Power Systems | 5 | 1100+ |
| 11 | [`11_control_systems/`](11_control_systems/) | Control Systems | 5 | 1100+ |
| 12 | [`12_communication_systems/`](12_communication_systems/) | Communication Systems | 5 | 1200+ |
| 13 | [`13_electromagnetic_theory/`](13_electromagnetic_theory/) | Electromagnetic Theory | 5 | 1000+ |
| 14 | [`14_vlsi_microelectronics/`](14_vlsi_microelectronics/) | VLSI & Microelectronics | 5 | 1100+ |
| 15 | [`15_measurement_instrumentation/`](15_measurement_instrumentation/) | Measurement & Instrumentation | 5 | 1000+ |
| 16 | [`16_solid_state_physics/`](16_solid_state_physics/) | Solid State Physics & Materials | 5 | 1000+ |

Every subject directory contains a `README.md` that maps its own files and counts.

---

## How the file splits work

Each subject is 5 files, ordered so that a beginner can go straight through:

- **Part 1** — foundations / definitions / basic derivations
- **Part 2** — the core working machinery of the subject
- **Part 3** — advanced analysis and the part most often missed
- **Part 4** — GATE-favourite mixed problem sets (previous-year-style)
- **Part 5** — traps, numericals, previous-year pattern drills, Rapid-fire recall

Open any subject's `README.md` for the exact chapter list.

## Cross-subject links worth memorising

These connections are favourite GATE question themes, and they are already flagged with
inline pointers in the individual files:

- Fourier transform ↔ Poisson summation ↔ sampling theorem (Signals ↔ DSP ↔ Communication)
- Laplace transform ↔ transient response ↔ poles/zeros stability ↔ loop gain (Signals ↔ Circuit ↔ Control)
- RLC resonance ↔ impedance matching ↔ transmission lines ↔ EMI/EMC (Circuit ↔ EM ↔ Power Electronics)
- Modulation index ↔ noise figure ↔ Shannon limit (Communication ↔ Information theory)
- Sampling theorem ↔ ADC/DAC ↔ anti-aliasing filter ↔ DSP (Signals ↔ Digital ↔ Measurement)
- Device physics ↔ diode/MOS capacitance ↔ op-amp stability ↔ switching loss (Solid State ↔ Analog ↔ Power Electronics)
- Short-circuit admittance ↔ bus impedance matrix ↔ fault analysis (Power Systems ↔ Circuit theory)
- Machine equations ↔ Park's transformation ↔ vector control (Machines ↔ Control ↔ Power Electronics)
- Ray optics ↔ waveguide dispersion ↔ antenna gain (EM ↔ Communication)
- CMOS power/area/delay trade-off ↔ scaling laws (VLSI ↔ Device physics)
