# Schmitt Triggers — Circuit Diagrams

Companion schematics for `Concepts.md`. A Schmitt trigger is a comparator with **positive
feedback**: the output itself decides the reference, so the trip point flips depending on
where the output already is. That gap between the two trip points is the hysteresis width.

## 1. Why a Plain Comparator Chatters

With no hysteresis, input noise of even a few microvolts near the reference swings the
output several times, which is unusable for a level detector or a relaxation oscillator.

```circuit
op = elm.Opamp(leads=True).right().at((0, 0))
src = elm.SourceSin().right().length(2).at((-6.5, -0.625)).label('Vin', loc='left')
elm.Ground().down().at((-6.5, -0.625))
elm.Line().at((-4.5, -0.625)).right(4.5)
elm.Dot().at((0, -0.625)).label('V- = Vin', loc='bottom')
elm.Dot().at((0, 0.625)).label('V+ = Vref', loc='top')
elm.Line().at((0, 0.625)).left(1.5).to((-1.5, 0.625))
elm.Ground().down().at((-1.5, 0.625))
elm.Line().at((3.4151, 3)).right(1.5).to((4.9151, 3)).label('Vout', loc='top')
elm.Line().at((3.4151, 0)).up(3)
elm.Dot().at((3.4151, 3)).label('output', loc='bottom')
elm.Annotate().at((5, -1.4)).delta(0, -0.6).label('noise of a few uV around Vref is enough\nto flip the output many times: the output\nfollows the noise, not the signal')
elm.Annotate().at((-3, 1.6)).delta(0, 0.6).label('no feedback: one trip point only')
```

- The gain near the trip point is `A_OL`, so microvolts of noise become rail-to-rail
  output swings.
- Adding positive feedback makes the trip point move away from the noise band.

## 2. Positive Feedback Sets Two Trip Points

A fraction `beta` of the output is added to the input side, so the trip point is
`Vref + beta*Vout`. When `Vout` is high the trip point is above `Vref`; when it is low the
trip point is below it.

```circuit
elm.Rect(corner1=(-9, -1.5), corner2=(-4, 1.5)).label('Vref', loc='center')
elm.Rect(corner1=(-9, 3), corner2=(-4, 6)).label('beta * Vout\n(from the last decision)', loc='center')
elm.Line().at((-6.5, 1.5)).up(1.5)
elm.Line().at((-6.5, 3)).down(1.5)
elm.Line().at((-6.5, 0)).right(1.5).to((-4.5, 0))
elm.Rect(corner1=(-4.5, -1.5), corner2=(-0.5, 1.5)).label('+', loc='center')
elm.Line().at((-0.5, 0)).right(1)
elm.Rect(corner1=(0.5, -1.5), corner2=(4.5, 1.5)).label('comparator\n(two decisions, not one)', loc='center')
elm.Line(arrow='->').at((4.5, 0)).right(1.5)
elm.Dot().at((6, 0))
elm.Rect(corner1=(6, -1.5), corner2=(10.5, 1.5)).label('Vout\n(one of the rails)', loc='center')
elm.Line().at((6, 0)).up(4.25).to((6, 4.25))
elm.Line().at((6, 4.25)).left(1.5).to((4.5, 4.25))
elm.Rect(corner1=(-4.5, 3), corner2=(-0.5, 6)).label('beta', loc='center')
elm.Line(arrow='->').at((-0.5, 4.5)).right(1.5).to((1, 4.5))
elm.Line().at((1, 4.5)).right(1.5).to((2.5, 4.5))
elm.Line().at((2.5, 4.5)).down(4.5)
elm.Line(arrow='->').at((2.5, 0)).left(2).to((0.5, 0))
elm.Annotate().at((10.5, 3.4)).delta(0, 0.6).label('the loop is positive: the output raises its own trip point')
elm.Annotate().at((-9, 6.6)).delta(0, 0.6).label('UTP = Vref + beta*Vsat,  LTP = Vref - beta*Vsat')
```

- Once the input reaches `UTP` the output snaps high, which moves the trip point to `UTP`.
- To come back it must fall past `LTP`, so the region between the two points is
  unambiguous.

## 3. Inverting Schmitt Trigger

The signal goes to the inverting input and the positive-feedback divider sets the trip
point.

```circuit
op = elm.Opamp(leads=True).right().at((0, 0))
src = elm.SourceSin().right().length(2).at((-6.5, -0.625)).label('Vin', loc='left')
elm.Ground().down().at((-6.5, -0.625))
elm.Line().at((-4.5, -0.625)).right(4.5)
elm.Dot().at((0, -0.625)).label('V- = Vin', loc='bottom')
elm.Line().at((0, 0.625)).up(1.25)
elm.Line().at((0, 1.875)).right(0.75).to((0.75, 1.875))
elm.Dot().at((0, 1.875)).label('V+ = beta*Vout', loc='left')
rf = elm.Resistor().right().length(1.5).at((0.75, 1.875)).label('R1  (to output)', loc='top')
elm.Line().at((2.25, 1.875)).right(1.1651).to((3.4151, 1.875)).label('Vout', loc='top')
elm.Line().at((3.4151, 1.875)).down(1.875)
elm.Dot().at((3.4151, 0)).label('output node', loc='bottom')
elm.Line().at((0, 1.875)).left(1.5)
elm.Resistor().down().length(1.25).at((-1.5, 1.875)).label('R2', loc='left')
elm.Ground().down().at((-1.5, 0.625))
elm.Annotate().at((5.5, 1.2)).delta(0.6, 0.6).label('output high while Vin is above UTP:\nthe loop flips the state and keeps it')
```

- `beta = R2/(R1+R2)`, so `UTP = +Vsat*R2/(R1+R2)` and `LTP = -Vsat*R2/(R1+R2)`.
- Hysteresis width `= 2*Vsat*R2/(R1+R2)`, independent of `R1` alone.

## 4. Non-Inverting Schmitt Trigger

Putting the signal on the non-inverting input makes the output follow the input polarity
while the hysteresis band is positioned by a reference.

```circuit
op = elm.Opamp(leads=True).right().at((0, 0))
src = elm.SourceSin().right().length(2).at((-6.5, 0.625)).label('Vin', loc='left')
elm.Ground().down().at((-6.5, 0.625))
elm.Line().at((-4.5, 0.625)).right(4.5)
elm.Dot().at((0, 0.625)).label('V+ = Vin', loc='top')
elm.Line().at((0, -0.625)).down(1.25)
elm.Line().at((0, -1.875)).right(0.75).to((0.75, -1.875))
elm.Dot().at((0, -1.875)).label('V- = reference node', loc='left')
rf = elm.Resistor().right().length(1.5).at((0.75, -1.875)).label('R1  (to output)', loc='bottom')
elm.Line().at((2.25, -1.875)).right(1.1651).to((3.4151, -1.875)).label('Vout', loc='bottom')
elm.Line().at((3.4151, -1.875)).up(1.875)
elm.Dot().at((3.4151, 0)).label('output node', loc='top')
elm.Line().at((0, -1.875)).left(1.5)
elm.Resistor().up().length(1.25).at((-1.5, -1.875)).label('R2', loc='left')
elm.Vdd().up().at((-1.5, -0.625)).label('+Vref')
elm.Annotate().at((5.5, -1.2)).delta(0.6, -0.6).label('output state follows the sign of Vin,\nso this is the useful form for\nlevel detection and waveform cleanup')
```

- `UTP = Vref + (Vsat - Vref)*R2/(R1+R2)`, `LTP = Vref - (Vsat - Vref)*R2/(R1+R2)`.
- With `R1 = R2` the band is symmetric about `Vref`, and the width is `Vsat - Vref`.

## 5. Hysteresis Width Against Input Noise

The only design rule that matters: the hysteresis width must exceed the peak-to-peak input
noise, with margin.

```circuit
op = elm.Opamp(leads=True).right().at((0, 0))
src = elm.SourceSin().right().length(2).at((-6.5, -0.625)).label('Vin', loc='left')
elm.Ground().down().at((-6.5, -0.625))
elm.Line().at((-4.5, -0.625)).right(4.5)
elm.Dot().at((0, -0.625))
elm.Line().at((0, 0.625)).up(1.25)
elm.Line().at((0, 1.875)).right(0.75).to((0.75, 1.875))
rf = elm.Resistor().right().length(1.5).at((0.75, 1.875)).label('R1', loc='top')
elm.Line().at((2.25, 1.875)).right(1.1651).to((3.4151, 1.875))
elm.Line().at((3.4151, 1.875)).down(1.875)
elm.Dot().at((3.4151, 0))
elm.Line().at((0, 1.875)).left(1.5)
elm.Resistor().down().length(1.25).at((-1.5, 1.875)).label('R2', loc='left')
elm.Ground().down().at((-1.5, 0.625))
elm.Line().at((-4.5, -0.625)).down(2.5).to((-4.5, -3.125))
elm.Line().at((-4.5, -3.125)).right(3)
elm.Annotate().at((-4.5, 1.2)).delta(0, 0.6).label('noise band on Vin')
elm.Annotate().at((5.2, 0.4)).delta(0, 0.6).label('choose R2/(R1+R2) so the\nhysteresis width is at least\n3x the input noise band')
elm.Annotate().at((5.2, -2.2)).delta(0, -0.6).label('for an op-amp, Vos drifts with\ntemperature, so the margin must\ncover drift as well')
elm.Annotate().at((-4.5, -3.9)).delta(0, -0.6).label('input moves inside the band: the\noutput simply holds its state')
```

- Add the offset and drift of the amplifier to the noise when sizing the margin.
- A small capacitor across `R2` speeds up the edges without reducing the DC hysteresis.

## 6. Transfer Characteristic (Block View)

The two thresholds and the direction of the transitions are the whole story; the vertical
jump is where the state actually changes.

```circuit
elm.Line().at((-3, 0)).right(7)
elm.Line().at((0, -2.5)).up(5)
elm.Line().at((-3, 0)).up(1.875)
elm.Line().at((-3, 1.875)).right(1.5)
elm.Line().at((-1.5, 1.875)).up(0.625).to((-1.5, 2.5))
elm.Line().at((1.5, 1.875)).up(0.625).to((1.5, 2.5))
elm.Line().at((-1.5, 2.5)).right(3)
elm.Dot().at((-1.5, 0)).label('LTP', loc='bottom')
elm.Dot().at((1.5, 0)).label('UTP', loc='bottom')
elm.Annotate().at((-2.2, 1.2)).delta(0, 0.5).label('-Vsat')
elm.Annotate().at((2.2, 1.2)).delta(0, 0.5).label('+Vsat')
elm.Annotate().at((-1.9, 0.7)).delta(0, 0.5).label('output stays low\nfor any Vin in the band')
elm.Annotate().at((-1, 3.2)).delta(0, 0.6).label('the steeper the jump, the faster the\nregenerative switch action')
elm.Annotate().at((4, -1.4)).delta(0, -0.6).label('the band is the memory of the circuit')
```

- A Schmitt trigger is a one-bit memory: the output stores which side of the band the input
  was last on.

## 7. Relaxation Oscillator

A Schmitt trigger plus an RC on the inverting input oscillates with a period set only by `R`,
`C` and the resistor ratio.

```circuit
op = elm.Opamp(leads=True).right().at((0, 0))
elm.Line().at((0, 0.625)).up(1.25)
elm.Line().at((0, 1.875)).right(0.75).to((0.75, 1.875))
rf = elm.Resistor().right().length(1.5).at((0.75, 1.875)).label('R1', loc='top')
elm.Line().at((2.25, 1.875)).right(1.1651).to((3.4151, 1.875))
elm.Line().at((3.4151, 1.875)).down(1.875)
elm.Dot().at((3.4151, 0)).label('square wave', loc='top')
elm.Line().at((0, 1.875)).left(1.5)
elm.Resistor().down().length(1.25).at((-1.5, 1.875)).label('R2', loc='left')
elm.Ground().down().at((-1.5, 0.625))
elm.Line().at((0, -0.625)).left(2)
elm.Dot().at((-2, -0.625)).label('timing node', loc='top')
r = elm.Resistor().left().length(2).at((-2, -0.625)).label('R', loc='bottom')
c = elm.Capacitor().down().length(2).at((-4, -0.625)).label('C', loc='left')
elm.Line().at((-4, -2.625)).down(0.5)
elm.Ground().down().at((-4, -3.125))
elm.Line().at((-6, -0.625)).right(2)
elm.Line().at((-6, -0.625)).up(0.75).to((-6, 0.125))
elm.Annotate().at((-6, 0.125)).delta(0, 0.6).label('C charges toward the\nopposite rail; the voltage\nat the timing node is a\ntriangle wave')
elm.Annotate().at((4.2, 1.2)).delta(0, 0.6).label('f = 1 / (2*RC*ln(1 + 2*R1/R2))\nfor R1 = R2:  f = 1/(1.386*R*C)')
```

- Duty cycle stays 50% as long as the thresholds are symmetric.
- Practical circuits add a diode across `R` to charge and discharge through different paths
  for an adjustable duty cycle.

## 8. Monostable One-Shot

A trigger pulse kicks the timing capacitor past the upper threshold; the output then stays
high for a fixed time set by `RC` and returns to the stable state by itself.

```circuit
op = elm.Opamp(leads=True).right().at((0, 0))
elm.Line().at((0, 0.625)).up(1.25)
elm.Line().at((0, 1.875)).right(0.75).to((0.75, 1.875))
rf = elm.Resistor().right().length(1.5).at((0.75, 1.875)).label('R1', loc='top')
elm.Line().at((2.25, 1.875)).right(1.1651).to((3.4151, 1.875)).label('Vout pulse', loc='top')
elm.Line().at((3.4151, 1.875)).down(1.875)
elm.Dot().at((3.4151, 0))
elm.Line().at((0, 1.875)).left(1.5)
elm.Resistor().down().length(1.25).at((-1.5, 1.875)).label('R2', loc='left')
elm.Ground().down().at((-1.5, 0.625))
elm.Line().at((0, -0.625)).left(2.5).to((-2.5, -0.625))
elm.Dot().at((-2.5, -0.625)).label('timing node', loc='top')
elm.Capacitor().down().length(2).at((-2.5, -0.625)).label('C', loc='right')
elm.Line().at((-2.5, -2.625)).down(0.5)
elm.Ground().down().at((-2.5, -3.125))
elm.Line().at((-2.5, -0.625)).left(2).to((-4.5, -0.625))
r = elm.Resistor().left().length(1.5).at((-4.5, -0.625)).label('R', loc='bottom')
elm.Line().at((-6, -0.625)).right(1.5).to((-4.5, -0.625))
src = elm.SourcePulse().right().length(1.5).at((-7.5, -0.625)).label('trigger', loc='left')
elm.Ground().down().at((-7.5, -0.625))
elm.Line().at((-6, -0.625)).up(0.875).to((-6, 0.25))
elm.Annotate().at((-6, 0.25)).delta(0, 0.6).label('a narrow trigger pulse\nis stretched to a\npulse of width ~RC*ln(...)')
elm.Annotate().at((3.4, 2.9)).delta(0, 0.6).label('one output pulse per trigger,\nthen the circuit resets itself')
```

- The output is stable with no trigger, so the circuit is a monostable, not an astable.
- The pulse width grows with `RC`, which is how the timing is set.

## 9. Schmitt Trigger as a Logic Interface

A slow, noisy or high-voltage input can drive a logic gate directly if a Schmitt trigger
first cleans it up and shifts the level.

```circuit
src = elm.SourceSin().right().length(2).at((-8, 0)).label('noisy input', loc='left')
elm.Ground().down().at((-8, 0))
elm.Line().at((-6, 0)).right(1.5).to((-4.5, 0))
elm.Rect(corner1=(-4.5, -1.25), corner2=(-0.5, 1.25)).label('Schmitt\ntrigger', loc='center')
elm.Line(arrow='->').at((-0.5, 0)).right(1.5)
elm.Rect(corner1=(1, -1.25), corner2=(5, 1.25)).label('logic gate\n(Schmitt input too,\nif available)', loc='center')
elm.Line(arrow='->').at((5, 0)).right(1.5).label('clean logic level', loc='top')
elm.Line().at((-2.5, 1.25)).up(1.25).to((-2.5, 2.5))
elm.Line().at((-2.5, 2.5)).right(5.5).to((3, 2.5))
elm.Line().at((3, 2.5)).down(1.25)
elm.Rect(corner1=(-8, 2.5), corner2=(-4.5, 5)).label('hysteresis', loc='center')
elm.Line().at((-6.25, 2.5)).down(0)
elm.Line(arrow='->').at((-4.5, 3.75)).right(1.5)
elm.Annotate().at((0, 4.4)).delta(0, 0.6).label('a Schmitt gate is specified with a\nnoise margin; an ordinary gate is not')
elm.Annotate().at((0, -2.6)).delta(0, -0.6).label('use one when the input changes slowly, is noisy, or crosses the threshold more than once')
```

- The Schmitt gate guarantees exactly one output transition per input crossing.
- A `74HC14` is the standard hex inverter with Schmitt inputs for exactly this job.

## 10. Choosing the Resistors

| Goal | Choose | Reason |
|---|---|---|
| Small hysteresis | large `R1/R2` ratio | width `= 2*Vsat*R2/(R1+R2)` |
| Low power | large `R1+R2` | the divider burns `Vsat^2/(R1+R2)` |
| Low offset error | small `R1`, small `R2` | input bias current flows through them |
| Fast oscillator | small `RC` | but keep `R` above the op-amp's bias limit |

- A real comparator IC (with true latch-based positive feedback) switches faster and its
  thresholds track the supply better than an op-amp used as a comparator.
- Add a small capacitor across `R1` to speed the output edge without changing the DC
  thresholds.
