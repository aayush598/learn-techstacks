# Op-Amp Linear Circuits — Circuit Diagrams

Companion schematics for `Concepts.md` and `Formulas.md`. All snippets use plain
`schemdraw` elements with explicit lengths, and every wire lands on a named node.

Reminder used throughout: for `Opamp(leads=True).at((x, y))` the anchors are
`in1 = (x, y + 0.625)` (non-inverting), `in2 = (x, y - 0.625)` (inverting) and
`out = (x + 3.4151, y)`.

## 1. Inverting Amplifier

The input drives the inverting input through `Rin`, so the inverting node is held at a
virtual ground and `Rf` converts the input current into an inverted output voltage.

```circuit
op = elm.Opamp(leads=True).right().at((0, 0))
src = elm.SourceSin().right().length(2).at((-7, -0.625)).label('Vin', loc='left')
elm.Ground().down().at((-7, -0.625))
rin = elm.Resistor().right().length(2).at((-5, -0.625)).label('Rin', loc='top')
elm.Line().at((-3, -0.625)).right(3)
elm.Dot().at((0, -0.625)).label('V- = 0 V', loc='bottom')
elm.Line().at((0, 0.625)).left(2)
elm.Ground().down().at((-2, 0.625))
rf = elm.Resistor().up().length(2).at((0, -0.625)).label('Rf', loc='left')
elm.Line().at((0, 1.375)).up(0.875)
elm.Line().at((0, 2.25)).right(3.4151)
elm.Line().at((3.4151, 2.25)).down(2.25)
elm.Line().at((3.4151, 0)).right(2).label('Vout', loc='top')
elm.Annotate().at((5.4, 1.4)).delta(1.2, 0.7).label('Vout = -(Rf/Rin) * Vin\nZin = Rin   (not high!)')
```

- `Zin` is only `Rin`, so a small `Rin` loads the source heavily.
- Gain accuracy comes from the resistor ratio, and input bias error is `Ib * Rf`.

## 2. Summing Amplifier (Weighted Inverting Summer)

Each input contributes `-Vin_i * (Rf/Rin_i)` to the output, so the circuit adds voltages
with independent weights.

```circuit
op = elm.Opamp(leads=True).right().at((0, 0))
legs = [('Vin1', 'Rin1', 1.5), ('Vin2', 'Rin2', 0.0), ('Vin3', 'Rin3', -1.5)]
for lbl, rlbl, y in legs:
    s = elm.SourceV().right().length(1.5).at((-9, y)).label(lbl, loc='left')
    elm.Ground().down().at((-9, y))
    elm.Resistor().right().length(1.5).at((-7.5, y)).label(rlbl, loc='top')
    elm.Line().at((-6, y)).right(4)
elm.Line().at((-2, 1.5)).down(2.125).to((-2, -0.625))
elm.Dot().at((-2, 0)).label('summing node', loc='left')
elm.Dot().at((-2, -0.625))
elm.Line().at((-2, -0.625)).right(2)
elm.Dot().at((0, -0.625)).label('virtual ground', loc='bottom')
elm.Line().at((0, 0.625)).left(1)
elm.Ground().down().at((-1, 0.625))
rf = elm.Resistor().up().length(2).at((0, -0.625)).label('Rf', loc='left')
elm.Line().at((0, 1.375)).up(0.875)
elm.Line().at((0, 2.25)).right(3.4151)
elm.Line().at((3.4151, 2.25)).down(2.25)
elm.Line().at((3.4151, 0)).right(2).label('Vout', loc='top')
elm.Annotate().at((5.4, 1.4)).delta(1.2, 0.7).label('Vout = -(Rf/Rin1)*Vin1\n       -(Rf/Rin2)*Vin2\n       -(Rf/Rin3)*Vin3')
```

- With all `Rin` equal, `Vout = -(Rf/Rin) * (Vin1 + Vin2 + Vin3)`.
- The summing node is a virtual ground, so each input sees an independent, fixed impedance.

## 3. Averaging Amplifier

Making every `Rin` equal and adding one extra input leg gives the arithmetic mean; `Rf`
then sets the overall scale.

```circuit
op = elm.Opamp(leads=True).right().at((0, 0))
ys = [1.5, 0.0, -1.5, -3.0]
for idx, y in enumerate(ys):
    s = elm.SourceV().right().length(1.5).at((-9, y)).label('Vin' + str(idx + 1), loc='left')
    elm.Ground().down().at((-9, y))
    elm.Resistor().right().length(1.5).at((-7.5, y)).label('Rin', loc='top')
    elm.Line().at((-6, y)).right(4)
elm.Line().at((-2, 1.5)).down(5.125).to((-2, -3.625))
elm.Dot().at((-2, 0.375))
elm.Line().at((-2, -3.625)).right(2)
elm.Dot().at((0, -0.625)).label('summing node', loc='bottom')
elm.Line().at((0, 0.625)).left(1)
elm.Ground().down().at((-1, 0.625))
rf = elm.Resistor().up().length(2).at((0, -0.625)).label('Rf = Rin/3', loc='left')
elm.Line().at((0, 1.375)).up(0.875)
elm.Line().at((0, 2.25)).right(3.4151)
elm.Line().at((3.4151, 2.25)).down(2.25)
elm.Line().at((3.4151, 0)).right(2).label('Vout = (V1+V2+V3+V4)/4', loc='top')
elm.Annotate().at((-6.5, -4.6)).delta(0, -0.8).label('Rf = Rin/3 divides the sum by four')
```

- Averaging is the simplest form of digital noise reduction by oversampling.
- The scale factor is set by `Rf/Rin`; with `n` equal inputs, `Rf = Rin/n` gives a mean.

## 4. Difference Amplifier (Subtractor)

With matched ratios `R2/R1 = R4/R3`, the output is a true difference and rejects the
common-mode part of the two inputs.

```circuit
op = elm.Opamp(leads=True).right().at((0, 0))
v1 = elm.SourceV().right().length(1.5).at((-9, 0.625)).label('V1', loc='left')
elm.Ground().down().at((-9, 0.625))
elm.Resistor().right().length(1.5).at((-7.5, 0.625)).label('R1', loc='top')
elm.Line().at((-6, 0.625)).right(6)
elm.Dot().at((0, 0.625)).label('V+', loc='top')
v2 = elm.SourceV().right().length(1.5).at((-9, -0.625)).label('V2', loc='left')
elm.Ground().down().at((-9, -0.625))
elm.Resistor().right().length(1.5).at((-7.5, -0.625)).label('R3', loc='top')
elm.Line().at((-6, -0.625)).right(6)
elm.Dot().at((0, -0.625)).label('V- = inverting node', loc='bottom')
r2 = elm.Resistor().up().length(1.5).at((0, -0.625)).label('R2', loc='left')
elm.Line().at((0, 0.875)).left(1.5)
elm.Resistor().down().length(1.5).at((-1.5, 0.875)).label('R4', loc='left')
elm.Line().at((-1.5, -0.625)).down(0.5)
elm.Ground().down().at((-1.5, -1.125))
elm.Line().at((0, 0.875)).up(1.375)
elm.Line().at((0, 2.25)).right(3.4151)
elm.Line().at((3.4151, 2.25)).down(2.25)
elm.Line().at((3.4151, 0)).right(2).label('Vout', loc='top')
elm.Annotate().at((5.4, 1.4)).delta(1.2, 0.7).label('Vout = (R2/R1) * (V2 - V1)\nonly if R2/R1 = R4/R3')
```

- Resistor-ratio mismatch directly becomes gain error and poor common-mode rejection.
- Resistor ratios must match to about 0.1% for a `0.1%` accurate difference amplifier.

## 5. Three-Op-Amp Instrumentation Amplifier

The first stage gives a high differential gain with very high input impedance, and the
second stage performs the subtraction. This is the standard front end for low-level
sensors.

```circuit
a1 = elm.Opamp(leads=True).right().at((0, 5)).label('A1', loc='center')
a2 = elm.Opamp(leads=True).right().at((0, 0)).label('A2', loc='center')
a3 = elm.Opamp(leads=True).right().at((7, 2)).label('A3', loc='center')
elm.Line().at((0, 5.625)).left(2.5).label('Vin+', loc='left')
elm.Line().at((0, 0.625)).left(2.5).label('Vin-', loc='left')
elm.Line().at((0, 4.375)).down(1.25)
elm.Dot().at((0, 3.125)).label('gain node', loc='left')
elm.Line().at((3.4151, 5)).down(1.875)
elm.Resistor().left().length(1.5).at((3.4151, 3.125)).label('Rf', loc='bottom')
elm.Resistor().down().length(1).at((0, 3.125)).label('Rg', loc='left')
elm.Line().at((0, 2.125)).down(0.5)
elm.Ground().down().at((0, 1.625))
elm.Line().at((0, -0.625)).down(1.25)
elm.Dot().at((0, -1.875)).label('gain node', loc='left')
elm.Line().at((3.4151, 0)).down(1.875)
elm.Resistor().left().length(1.5).at((3.4151, -1.875)).label('Rf', loc='bottom')
elm.Resistor().down().length(1).at((0, -1.875)).label('Rg', loc='left')
elm.Line().at((0, -2.875)).down(0.5)
elm.Ground().down().at((0, -3.375))
elm.Line().at((3.4151, 5)).right(1.0849)
elm.Line().at((4.5, 5)).down(2.375)
elm.Resistor().right().length(1).at((4.5, 2.625)).label('R3', loc='top')
elm.Line().at((5.5, 2.625)).right(1.5)
elm.Dot().at((7, 2.625)).label('A3 non-inverting', loc='top')
elm.Line().at((7, 2.625)).left(0.8)
elm.Line().at((6.2, 2.625)).down(1.125)
elm.Ground().down().at((6.2, 1.5))
elm.Resistor().down().length(0.75).at((6.2, 2.625)).label('R4', loc='right')
elm.Line().at((3.4151, 0)).right(1.0849)
elm.Line().at((4.5, 0)).up(1.375)
elm.Resistor().right().length(1).at((4.5, 1.375)).label('R1', loc='bottom')
elm.Line().at((5.5, 1.375)).right(1.5)
elm.Dot().at((6.5, 1.375)).label('A3 inverting node', loc='bottom')
elm.Line().at((6.5, 1.375)).right(0.5)
elm.Dot().at((7, 1.375))
elm.Line().at((6.5, 1.375)).down(2.375)
elm.Dot().at((6.5, -1))
elm.Resistor().right().length(2).at((6.5, -1)).label('Rf3', loc='bottom')
elm.Resistor().down().length(0.75).at((6.5, -1)).label('Rg3', loc='left')
elm.Ground().down().at((6.5, -1.75))
elm.Line().at((8.5, -1)).right(1.9151)
elm.Line().at((10.4151, -1)).up(3)
elm.Dot().at((10.4151, 2))
elm.Line().at((10.4151, 2)).right(2).label('Vout', loc='top')
elm.Annotate().at((2.2, 7)).delta(0, 0.7).label('Stage 1: two non-inverting amps, gain 1 + Rf/Rg each,')
elm.Annotate().at((2.2, 7)).delta(0, -0.1).label('so the input impedance is set by the op-amps, not by Rf/Rg')
elm.Annotate().at((11.4, 3.4)).delta(0.6, 0.7).label('Stage 2: unity-gain difference\namplifier, R1 = R3 and Rf3 = Rg3')
```

- Each first-stage amp has gain `1 + Rf/Rg`; the classic cross-coupled variant shares one
  `Rg` and gives a first-stage gain of `1 + 2Rf/Rg`.
- Gain accuracy comes from the resistor ratios, so `Rf/Rg` is usually trimmed.
- Only A3 rejects the common-mode part, which is why A3 needs tight resistor matching.

## 6. T-Network Amplifier

Splitting the feedback resistor into a T lets a very large closed-loop gain be built from
ordinary resistor values, at the cost of noise gain and bandwidth.

```circuit
op = elm.Opamp(leads=True).right().at((0, 0))
src = elm.SourceSin().right().length(2).at((-7, -0.625)).label('Vin', loc='left')
elm.Ground().down().at((-7, -0.625))
rin = elm.Resistor().right().length(2).at((-5, -0.625)).label('Rin', loc='top')
elm.Line().at((-3, -0.625)).right(3)
elm.Dot().at((0, -0.625)).label('virtual ground', loc='left')
ra = elm.Resistor().down().length(1.5).at((0, -0.625)).label('RA', loc='right')
elm.Dot().at((0, -2.125)).label('T junction', loc='left')
rb = elm.Resistor().right().length(2).at((0, -2.125)).label('RB', loc='bottom')
rc = elm.Resistor().down().length(1.5).at((2, -2.125)).label('RC', loc='right')
elm.Line().at((2, -3.625)).down(0.5)
elm.Ground().down().at((2, -4.125))
elm.Line().at((2, -2.125)).up(0.625).to((2, -1.5))
elm.Line().at((2, -1.5)).right(1.4151)
elm.Line().at((3.4151, -1.5)).up(1.5)
elm.Line().at((3.4151, 0)).right(2).label('Vout', loc='top')
elm.Line().at((0, 0.625)).left(2)
elm.Ground().down().at((-2, 0.625))
elm.Annotate().at((5.4, 1.4)).delta(1.2, 0.7).label('Gain = RA + RB + RA*RB/RC\nall divided by Rin, yet every\nresistor stays an ordinary value')
elm.Annotate().at((5.4, -2.2)).delta(1.2, -0.8).label('Cost: noise gain and offset\nare amplified too, so the\nusable bandwidth shrinks')
```

- Large gains are possible with small resistors, which keeps parasitic capacitance small.
- The trade is a higher noise gain, so the closed-loop bandwidth and settling suffer.

## 7. Practical Integrator

A capacitor in the feedback path gives integration. A resistor in parallel with it gives
the integrator a finite DC gain, which is what keeps a real op-amp from saturating on any
offset or bias current.

```circuit
op = elm.Opamp(leads=True).right().at((0, 0))
src = elm.SourceSin().right().length(2).at((-7, -0.625)).label('Vin', loc='left')
elm.Ground().down().at((-7, -0.625))
elm.Resistor().right().length(2).at((-5, -0.625)).label('Rin', loc='top')
elm.Line().at((-3, -0.625)).right(3)
elm.Dot().at((0, -0.625)).label('inverting node', loc='left')
elm.Line().at((0, 0.625)).left(2)
elm.Ground().down().at((-2, 0.625))
elm.Line().at((0, -0.625)).down(0.875)
elm.Dot().at((0, -1.5))
elm.Capacitor().right().length(1.5).at((0, -1.5)).label('Cf', loc='top')
elm.Line().at((1.5, -1.5)).right(1.9151)
elm.Line().at((3.4151, -1.5)).up(1.5)
elm.Line().at((0, -1.5)).down(1)
elm.Resistor().right().length(2).at((0, -2.5)).label('Rf  (DC path)', loc='bottom')
elm.Line().at((2, -2.5)).right(1.4151)
elm.Line().at((3.4151, -2.5)).up(2.5)
elm.Dot().at((3.4151, -1.5))
elm.Line().at((3.4151, 0)).right(2).label('Vout', loc='top')
elm.Annotate().at((5.4, 1.4)).delta(1.2, 0.7).label('Vout = -(1/Rin*Cf) * integral(Vin dt)\nDC gain = -Rf/Rin, so the op-amp\ncannot be driven to saturation')
```

- Gain falls as `1/(2*pi*f*Cf)`, so the stage is a low-pass with a pole at `1/(2*pi*Rf*Cf)`.
- The input must be offset-adjusted or reset, because any DC offset integrates without bound.

## 8. Practical Differentiator

Swapping the resistor and capacitor roles gives differentiation; the shunt resistor sets
the useful high-frequency gain limit.

```circuit
op = elm.Opamp(leads=True).right().at((0, 0))
src = elm.SourceSin().right().length(2).at((-7, -0.625)).label('Vin', loc='left')
elm.Ground().down().at((-7, -0.625))
cf = elm.Capacitor().right().length(1.5).at((-5, -0.625)).label('C', loc='top')
elm.Line().at((-3.5, -0.625)).right(3.5)
elm.Dot().at((0, -0.625)).label('inverting node', loc='left')
elm.Line().at((0, 0.625)).left(2)
elm.Ground().down().at((-2, 0.625))
rf = elm.Resistor().right().length(2).at((0, -0.625)).label('Rf', loc='top')
elm.Line().at((2, -0.625)).right(1.4151)
elm.Line().at((3.4151, -0.625)).up(0.625)
elm.Line().at((3.4151, 0)).right(2).label('Vout', loc='top')
elm.Line().at((-5, -0.625)).down(1.875)
elm.Resistor().right().length(1.5).at((-5, -2.5)).label('R1', loc='bottom')
elm.Line().at((-3.5, -2.5)).up(1.875)
elm.Dot().at((-3.5, -0.625))
elm.Annotate().at((5.4, 1.4)).delta(1.2, 0.7).label('Vout = -Rf*C * dVin/dt\nabove 1/(2*pi*R1*C) the gain\nflattens out at -Rf/R1')
```

- Unbounded HF gain is the classic differentiator problem: noise is amplified and the
  circuit oscillates. `R1` limits the gain and `Rf` keeps the loop stable.
- Average `R1*C << T` of the signal period, or the action is not differentiation.

## 9. Transimpedance Amplifier (Photodiode Amplifier)

A photodiode produces a small current, so the feedback impedance sets the transimpedance
gain. Holding the summing node at a virtual ground keeps the diode reverse biased.

```circuit
op = elm.Opamp(leads=True).right().at((0, 0))
pd = elm.Photodiode().up().length(1.5).at((-3, 0))
elm.Line().at(pd.end).right(3)
elm.Dot().at((0, -0.625)).label('virtual ground', loc='right')
elm.Line().at((0, 0.625)).left(2)
elm.Ground().down().at((-2, 0.625))
rf = elm.Resistor().up().length(2).at((0, -0.625)).label('Rf', loc='left')
elm.Line().at((0, 1.375)).up(0.875)
elm.Line().at((0, 2.25)).right(3.4151)
elm.Line().at((3.4151, 2.25)).down(2.25)
elm.Line().at((3.4151, 0)).right(2).label('Vout = -Id * Rf', loc='top')
elm.Line().at((0, -0.625)).down(1)
elm.Capacitor().right().length(1.5).at((0, -1.625)).label('Cf', loc='top')
elm.Line().at((1.5, -1.625)).right(1.9151)
elm.Line().at((3.4151, -1.625)).up(1.625)
elm.Line().at((0, -0.625)).left(3)
elm.Dot().at((-3, -0.625)).label('Id flows only through Rf and Cf', loc='bottom')
elm.Annotate().at((5.4, -1.6)).delta(1.2, -0.8).label('Cf adds a feedback pole to\ncancel the photodiode\ncapacitance and prevent peaking')
elm.Annotate().at((-5.6, 1.4)).delta(0, 0.7).label('light')
```

- `Zin` at the diode is just `1/(s*Cdiode)`: very small at high frequency.
- Stability, not gain, is the design problem; `Rf*Cf` is chosen from the diode and op-amp
  data sheets.

## 10. Transconductance Stage (Virtual-Sink Current Source)

Forcing `Vin` through a known resistor into a virtual ground makes the op-amp a
current source, and the current is set entirely by the resistor.

```circuit
op = elm.Opamp(leads=True).right().at((0, 0))
src = elm.SourceV().right().length(2).at((-7, -0.625)).label('Vin', loc='left')
elm.Ground().down().at((-7, -0.625))
rin = elm.Resistor().right().length(2).at((-5, -0.625)).label('Rsense', loc='top')
elm.Line().at((-3, -0.625)).right(3)
elm.Dot().at((0, -0.625)).label('0 V node', loc='bottom')
elm.Line().at((0, 0.625)).left(2)
elm.Ground().down().at((-2, 0.625))
load = elm.SourceI().up().length(2).at((2, -3.5)).label('floating load', loc='left')
elm.Line().at((2, -1.5)).up(1.5)
elm.Line().at((0, -0.625)).right(2)
elm.Line().at((2, -0.625)).up(1.5)
elm.Dot().at((2, -0.625)).label('I = Vin/Rsense', loc='right')
elm.Line().at((2, -0.625)).left(3.4151)
elm.Annotate().at((-4.6, 1.6)).delta(0, 0.8).label('the op-amp adjusts its output until the\nsense node sits at 0 V, so the current is\nfixed by the resistor')
elm.Annotate().at((4.6, -2.2)).delta(1.2, -0.8).label('output compliance limits the\nload voltage swing:\nVout stays between the rails')
```

- `Iout = Vin / Rsense` regardless of the load, within the output compliance range.
- Compliance headroom is the price: a high-side load cannot be driven this way.

## 11. Two-Stage Amplifier with AC Coupling

Staging multiplies gain, but each interstage coupling capacitor creates a high-pass
corner, so the stages must be budgeted together.

```circuit
a1 = elm.Opamp(leads=True).right().at((0, 0))
s1 = elm.SourceSin().right().length(1.5).at((-6, -0.625)).label('source', loc='left')
elm.Ground().down().at((-6, -0.625))
elm.Resistor().right().length(1.5).at((-4.5, -0.625)).label('Rin', loc='top')
elm.Line().at((-3, -0.625)).right(3)
elm.Dot().at((0, -0.625))
elm.Line().at((0, 0.625)).left(1)
elm.Ground().down().at((-1, 0.625))
rfa = elm.Resistor().up().length(2).at((0, -0.625)).label('Rf1', loc='left')
elm.Line().at((0, 1.375)).up(0.625)
elm.Line().at((0, 2)).right(3.4151)
elm.Line().at((3.4151, 2)).down(2)
rga = elm.Resistor().down().length(1.25).at((3.4151, 0)).label('Rg1', loc='right')
elm.Line().at((3.4151, -1.25)).down(0.5)
elm.Ground().down().at((3.4151, -1.75))
elm.Line().at((3.4151, 0)).right(1.5)
coup = elm.Capacitor().right().length(1.5).at((4.9151, 0)).label('Cc', loc='top')
elm.Dot().at((6.4151, 0)).label('stage 1 out', loc='top')
rload = elm.Resistor().down().length(1.25).at((6.4151, 0)).label('input of stage 2', loc='right')
elm.Line().at((6.4151, -1.25)).down(0.5)
elm.Ground().down().at((6.4151, -1.75))
elm.Annotate().at((5.4, 1.6)).delta(0, 0.7).label('corner f = 1/(2*pi*Cc*Rin2):\nstage 1 must be able to drive the\nwhole input impedance of stage 2')
elm.Annotate().at((-4.6, 1.6)).delta(0, 0.7).label('stage 1\nAv1 = 1 + Rf1/Rg1')
elm.Line().at((8.4151, -1.75)).right(2)
elm.Rect(corner1=(10.4151, -2.5), corner2=(13.4151, 0.5)).label('stage 2\nAv2', loc='center')
elm.Line(arrow='->').at((6.4151, -1.75)).right(3.4151)
elm.Line(arrow='->').at((13.4151, -1)).right(1.5).label('Vout', loc='top')
elm.Annotate().at((11.9, 1.4)).delta(0, 0.7).label('Av = Av1 * Av2\nand the offsets add, not multiply')
```

- Overall gain is the product, but offset, noise and distortion do not simply improve.
- Cascading costs one extra pole; the number of poles is what eventually limits bandwidth.

## 12. Choosing a Configuration (Block View)

The configuration decides the impedance seen by the source and by the load, which is
often the real reason for the choice.

```circuit
elm.Rect(corner1=(-9, -2.5), corner2=(-3, 2.5)).label('Inverting\nlow Zin, useful Zout\ngain Rf/Rin, any polarity', loc='center')
elm.Rect(corner1=(-1.5, -2.5), corner2=(4.5, 2.5)).label('Non-inverting\nhigh Zin, useful Zout\ngain 1 + Rf/Rg >= 1', loc='center')
elm.Rect(corner1=(6, -2.5), corner2=(12, 2.5)).label('Follower\nvery high Zin, lowest Zout\ngain exactly 1', loc='center')
elm.Rect(corner1=(-6, 4.5), corner2=(6, 7.5)).label('Rule of thumb: source impedance low -> inverting;\nsource impedance high -> non-inverting; heavy load -> follower', loc='center')
elm.Line(arrow='->').at((-3, 0)).right(1.5)
elm.Line(arrow='->').at((4.5, 0)).right(1.5)
elm.Line(arrow='<-').at((0, 4.5)).down(2)
elm.Annotate().at((0, -3.6)).delta(0, -0.8).label('Zout is low in all three cases: the op-amp output stage sets it, not the feedback network')
```
