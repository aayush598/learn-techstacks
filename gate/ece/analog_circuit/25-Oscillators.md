# Chapter 25 — Oscillators

> **The idea in one line:** an oscillator is an amplifier with *positive
> feedback* that keeps itself ringing. The universal recipe: loop gain = 1 and
> loop phase = 0° at exactly one frequency. Learn the Barkhausen condition, then
> the four classic oscillators, then the op-amp waveform generators.

---

## 25.1 The Barkhausen criterion — the single idea

A feedback loop oscillates when the net loop gain times the phase condition is
met **at the oscillating frequency f_o**:

```
|Aβ| = 1          (gain condition)
∠Aβ = 0°          (phase condition: loop phase = 0° or 360°)
```
- **Start-up:** make `|Aβ| > 1` slightly so oscillations grow; amplitude
  limiting (saturation/nonlinearity) pulls it back to unity.
- **Sustain:** exactly 1 at steady state.
- If `|Aβ| < 1` at ALL frequencies → never oscillates (damped).
- Positive feedback path must add 0° (or net 360°) of phase around the loop.

GATE statements you'll be asked to judge:
- "Barkhausen gives the condition for sustained oscillation." ✓
- "Loop gain must be ≥1 at the frequency where phase = 0°. "
  ✓ (≥1 for start, =1 sustained).

---

## 25.2 The oscillator family tree

| Oscillator | Frequency set by | Feedback network | Band |
|------------|------------------|------------------|------|
| **Phase-shift** | RC network (3 stages) | 3× RC high-pass/lead | audio (low f) |
| **Wien bridge** | series RC + parallel RC | bridge | audio |
| **Colpitts** | LC tank | tapped capacitor + coil | RF |
| **Hartley** | LC tank | tapped inductor + cap | RF |
| **Crystal** | crystal resonance | piezoelectric | precise |
| **Relaxation (op-amp)** | RC timing | Schmitt + integrator | square/triangular |

---

## 25.3 RC oscillators — analysis facts you need

### Phase-shift oscillator (BJT or op-amp)

```
  ┌─────────────────────────────┐  (positive feedback path)
  │                             │
 [C─R] ─ [C─R] ─ [C─R] ─► amplifier (gain −29 or −A) ──► output
```
- Uses 3 RC ladder sections (180°) + inverting amplifier (–180°) = 360° total.
- **Frequency of oscillation** (equal R, C):
  `f_o = 1/(2π·R·C·√6)  ≈ 1/(2π·RC·2.449)`
- **Minimum gain required:** `|A| ≥ 29` ("–29 for inverter").
- GATE loves: "phase-shift oscillator oscillates at f = 1/(2πRC√6) and needs
  gain ≥ 29."

### Wien bridge oscillator

```
              ┌─── rf ───┐
  +──R──C──►+─┤        ─┼─► fo
      │ (series RC)      │
  R—┼──(parallel RC)     │
   output feeds both arms of the bridge
```
- Bridge: series RC (Z1) on top, parallel RC (Z2) on bottom; feedback path
  through them with gain arm.
- **Frequency:** `f_o = 1/(2π·R·C)` (when R,C equal).
- **Gain condition:** op-amp gain `1 + Rf/R1 ≥ 3` (balances the bridge). At
  exactly 3, sustained. Below 3: dies.
- Phase condition: at f_o the bridge contributes 0° (that's the defining
  property of the balanced bridge).
- "Gain of 3" and "f = 1/(2πRC)" — two classic MCQ targets.

Both RC types give **low frequency/audio** oscillators.

---

## 25.4 LC oscillators — resonance facts

Tank resonance:
`f_o = 1/(2π√(L·C_eff))`

### Colpitts
- Capacitor divider C1–C2 across the coil:
  `f_o = 1/(2π√(L·(C1·C2/(C1+C2))))`  (series caps!)
- Feedback tap: the capacitor divider taps the tank voltage down.

### Hartley
- Inductor divider L1–L2 (parallel to a single C):
  `f_o = 1/(2π√((L1+L2)·C))`   (series inductors!)
- Feedback tap: the inductor tap.

### Colpitts vs Hartley — one-liner for the exam
- **Colpitts:** center-tapped *capacitors*, L single. `1/√(L·Cseries)`.
- **Hartley:** center-tapped *inductors*, C single. `1/√((L1+L2)C)`.
- Frequency depends on the *resonating* combination; GATE gives the tank and
  asks f_o — just series-combine the right two elements.

### Crystal oscillator
- Piezoelectric resonance is extremely stable (Q 10⁴–10⁵).
- Replaces the LC in feedback: oscillator "locks" to crystal's f_o.
- GATE: "why crystals?" → stability/precision, small shift.

---

## 25.5 Relaxation / op-amp waveform oscillators

Basic square-wave generator (Schmitt + RC):

```
  ┌────────────────┐
  │                │
  │   op-amp (Schmitt, output ±V_sat)
  │                │
  │   v+ = v_o·R1/(R1+R2)     (hysteresis thresholds!)
  │   v− <── R ── C ──── C to GND
  │                │────────────► output
  └── R2 ─ R1 ─────┘ (positive feedback)
```
Operation:
- Output alternates ±V_sat; C charges/discharges through R toward the
  opposite threshold; flips on reaching hysteresis level.

**Frequency:**
```
T = 2·R·C·ln(1 + 2·R1/R2)
f = 1/T
```
- For symmetric rails, thresholds `±Vth = ±V_sat·R1/R2`... precisely
  `Vth = V_sat·R1/(R1+R2)`. GATE uses the ln formula most.
- **Square wave output** (from the Schmitt) + **triangle** from following C
  node/integrator.

### Triangular-wave generator (Schmitt + integrator)
```
  square (Schmitt out) ──R_int──► (integrator) ──► triangle
                 └── feedback to Schmitt input
```
- Integrator turns the square into a triangle.
- Triangle amplitude set by thresholds; frequency by
  `f = (V_th... )/(4·R_int·C·V_sat)·... ` typical. GATE wants the concept:
  - square from Schmitt
  - triangle from integrator
  - freq settable via R_int, C, and the Schmitt divider.

---

## 25.6 Worked examples

**Q1. Phase-shift: R = 10 kΩ, C = 1 nF.**
- `f_o = 1/(2π·10k·1n·√6) = 1/(2π·10k·1n·2.449) ≈ 6.5 kHz`.
- Minimum gain 29.

**Q2. Wien bridge R = 10 kΩ, C = 10 nF.**
- `f_o = 1/(2π·10k·10n) ≈ 1.59 kHz`. Gain arm needs 3.

**Q3. Relaxation: R=10 kΩ, C=10 nF, R1=10k, R2=20k.**
- `T = 2·10k·10n·ln(1 + 2·10k/20k) = 200µ·ln(2) ≈ 138.6 µs` → f ≈ 7.2 kHz.
- Thresholds `= ±V_sat·10k/30k = ±V_sat/3`.

---

## GATE traps (oscillators)

1. **Phase-shift needs gain ≥ 29, not 3.** 3 belongs to Wien.
2. Colpitts = caps in series (`C1C2/(C1+C2)`); Hartley = inductors in series
   (`L1+L2`). One swapped combo = instant wrong f_o.
3. Wien f_o = 1/(2πRC), the balanced condition sets gain to 3 — the *gain* term
   isn't 1/(2πRC).
4. Barkhausen: `|Aβ|=1 AND phase 0°` — one condition alone is insufficient.
5. "A·β slightly > 1 for start-up, = 1 at steady state" is the standard
   phrasing; "must equal 1 to start" is false.
6. Relaxation vs sinusoidal: relaxation = square/triangle (op-amp + RC);
   sinusoidal = phase-shift / Wien / LC. Don't cross.

---

## 5-question self-check

1. Barkhausen conditions? → *|Aβ|=1, ∠Aβ=0°.*
2. Phase-shift min gain? → *29.*
3. Wien f_o? → *1/(2πRC).*
4. Colpitts effective C? → *C1C2/(C1+C2).*
5. Relaxation waveform? → *square (+ triangle).*

Next: **`26-Transistor-as-Switch.md`**