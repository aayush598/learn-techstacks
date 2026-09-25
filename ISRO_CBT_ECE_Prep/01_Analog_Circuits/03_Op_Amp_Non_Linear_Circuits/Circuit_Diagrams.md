# Op-Amp Non-Linear Circuits — Circuit Diagrams

Companion schematics for `Concepts.md` and `Formulas.md`. A comparator works the input
stage of an op-amp as a **one-bit decision maker** instead of a linear amplifier, which is
why these circuits are non-linear: the transfer function is a step, not a straight line.

## 1. Inverting Comparator

The reference sets the trip point and the output flips to a rail as soon as the input
crosses it. There is no feedback path, so the op-amp runs open loop with a gain of
hundreds of thousands.

```circuit
op = elm.Opamp(leads=True).right().at((0, 0)).label('U1  comparator', loc='center')
src = elm.SourceSin().right().length(2).at((-7, -0.625)).label('Vin', loc='left')
elm.Ground().down().at((-7, -0.625))
elm.Line().at((-5, -0.625)).right(5)
elm.Dot().at((0, -0.625)).label('V-', loc='bottom')
vref = elm.SourceV().up().length(2).at((-2, 0.625)).label('Vref', loc='left')
elm.Line().at((-2, 0.625)).down(0.5)
elm.Dot().at((0, 0.625)).label('V+', loc='top')
elm.Line().at((0, 1.625)).up(0.875)
elm.Vdd().at((0, 2.5)).label('+Vsat')
elm.Line().at((0, 0.625)).left(2)
elm.Line().at((3.4151, 0)).right(2).label('out: +Vsat when Vin < Vref', loc='top')
elm.Line().at((1.3467, 0.84)).up(1.66)
elm.Vdd().at((1.3467, 2.5)).label('+V')
elm.Line().at((1.3467, -0.84)).down(1.66)
elm.Vss().at((1.3467, -2.5)).label('-V')
elm.Annotate().at((5.4, 1.4)).delta(1.0, 0.7).label('Vout = +Vsat for Vin < Vref\nVout = -Vsat for Vin > Vref')
```

- The output is always at a rail, so average power is high and the response is fast.
- A real comparator IC (LM311, TLV3501) is used instead of a general op-amp.

## 2. Non-Inverting Comparator

Here the signal goes to the non-inverting input, so the output goes high when the input
*rises above* the reference.

```circuit
op = elm.Opamp(leads=True).right().at((0, 0)).label('U1  comparator', loc='center')
src = elm.SourceSin().right().length(2).at((-7, 0.625)).label('Vin', loc='left')
elm.Ground().down().at((-7, 0.625))
elm.Line().at((-5, 0.625)).right(5)
elm.Dot().at((0, 0.625)).label('V+', loc='top')
elm.Line().at((0, 0.625)).left(2)
vref = elm.SourceV().up().length(2).at((-2, -0.625)).label('Vref', loc='left')
elm.Line().at((-2, -0.625)).down(0.5)
elm.Dot().at((0, -0.625)).label('V-', loc='bottom')
elm.Line().at((0, -0.625)).down(0.875)
elm.Vss().at((0, -1.5)).label('-Vsat')
elm.Line().at((3.4151, 0)).right(2).label('out: +Vsat when Vin > Vref', loc='top')
elm.Annotate().at((5.4, 1.4)).delta(1.0, 0.7).label('Vout = +Vsat for Vin > Vref\nVout = -Vsat for Vin < Vref')
elm.Annotate().at((-6.4, -1.6)).delta(0, -0.7).label('swap the inputs to invert\nthe sense of the comparison')
```

## 3. Comparator Transfer Characteristic (Block View)

The open-loop gain is so large that any differential input above a few hundred
microvolts saturates the output. That threshold is the whole reason a comparator is
useful.

```circuit
elm.Line().at((-3, 0)).right(6).label('V+ - V-', loc='bottom')
elm.Line().at((0, -2.5)).up(5).label('Vout', loc='left')
elm.Line().at((-3, 0)).up(1.875)
elm.Line().at((-3, 1.875)).right(1.5)
elm.Line().at((-1.5, 1.875)).up(0.625).to((-1.5, 2.5))
elm.Line().at((1.5, 1.875)).up(0.625).to((1.5, 2.5))
elm.Line().at((-1.5, 2.5)).right(3)
elm.Dot().at((-1.5, 0))
elm.Annotate().at((-1.5, 0.6)).delta(0, 0.5).label('Vos')
elm.Annotate().at((-2.2, 1.2)).delta(0, 0.5).label('-Vsat')
elm.Annotate().at((2.2, 1.2)).delta(0, 0.5).label('+Vsat')
elm.Rect(corner1=(-6.5, -5.5), corner2=(-3.5, -3.5)).label('op-amp for\nlinear gain', loc='center')
elm.Rect(corner1=(-1.5, -5.5), corner2=(1.5, -3.5)).label('comparator:\nslew, not gain', loc='center')
elm.Rect(corner1=(3.5, -5.5), corner2=(6.5, -3.5)).label('logic gate:\nrail-to-rail\nin, one bit out', loc='center')
elm.Line(arrow='->').at((-3.5, -4.5)).right(2)
elm.Line(arrow='->').at((1.5, -4.5)).right(2)
elm.Annotate().at((0, -6.6)).delta(0, -0.6).label('open-loop gain A_OL is huge, so Vout = +/-Vsat for any Vd beyond Vos')
```

- The linear region is only a few hundred microvolts wide around zero.
- Propagation delay, not gain, is the figure of merit for a comparator.

## 4. Zero-Crossing Detector

Setting the reference to zero makes the output a square wave that marks each sign change
of the input, which is what a zero-crossing detector does.

```circuit
op = elm.Opamp(leads=True).right().at((0, 0))
src = elm.SourceSin().right().length(2).at((-7, -0.625)).label('Vin', loc='left')
elm.Ground().down().at((-7, -0.625))
elm.Line().at((-5, -0.625)).right(5)
elm.Dot().at((0, -0.625)).label('0 V reference', loc='bottom')
elm.Line().at((0, 0.625)).left(2)
elm.Ground().down().at((-2, 0.625))
elm.Line().at((3.4151, 0)).right(2).label('square wave: zero crossings\nof Vin become edges', loc='top')
elm.Annotate().at((5.4, -1.6)).delta(1.2, -0.8).label('used for frequency division,\nphase measurement and\nwaveform shaping')
elm.Annotate().at((-5.4, 1.4)).delta(0, 0.7).label('a small positive reference\nat V+ gives a clean\nzero-crossing pulse')
```

- Adding a small positive reference at `V+` avoids the slow, noisy crossing at exactly zero.
- A differentiator on the output gives narrow pulses of constant width.

## 5. Inverting Schmitt Trigger

Positive feedback sets two different trip points, so the output cannot chatter when the
input sits on the reference.

```circuit
op = elm.Opamp(leads=True).right().at((0, 0))
src = elm.SourceSin().right().length(2).at((-7, -0.625)).label('Vin', loc='left')
elm.Ground().down().at((-7, -0.625))
elm.Line().at((-5, -0.625)).right(5)
elm.Dot().at((0, -0.625)).label('V- = Vin', loc='bottom')
elm.Dot().at((0, 0.625)).label('V+ = beta*Vout', loc='top')
elm.Line().at((0, 0.625)).up(1.25)
elm.Line().at((0, 1.875)).right(0.75).to((0.75, 1.875))
elm.Dot().at((0, 1.875)).label('V+ node', loc='left')
rf = elm.Resistor().right().length(1.5).at((0.75, 1.875)).label('R1  (to output)', loc='top')
elm.Line().at((2.25, 1.875)).right(1.1651).to((3.4151, 1.875))
elm.Line().at((3.4151, 1.875)).down(1.875)
elm.Dot().at((3.4151, 0)).label('Vout node', loc='bottom')
elm.Line().at((0, 1.875)).left(1.5)
elm.Resistor().down().length(1.25).at((-1.5, 1.875)).label('R2', loc='left')
elm.Ground().down().at((-1.5, 0.625))
elm.Line().at((3.4151, 0)).right(2).label('Vout', loc='bottom')
elm.Annotate().at((4.4, 1.6)).delta(1.0, 0.7).label('UTP = +Vsat * R2/(R1+R2)\nLTP = -Vsat * R2/(R1+R2)\nhysteresis width = UTP - LTP')
```

- The input must swing past `UTP` to go high and past `LTP` to go low.
- `R2` pulls the `V+` node to ground, so the reference is a fraction of the *output*.

## 6. Non-Inverting Schmitt Trigger

Swapping the input and the feedback makes the output state follow the input polarity while
keeping the same hysteresis width.

```circuit
op = elm.Opamp(leads=True).right().at((0, 0))
src = elm.SourceSin().right().length(2).at((-7, 0.625)).label('Vin', loc='left')
elm.Ground().down().at((-7, 0.625))
elm.Line().at((-5, 0.625)).right(5)
elm.Dot().at((0, 0.625)).label('V+ = Vin', loc='top')
elm.Dot().at((0, -0.625)).label('V- = beta*Vout', loc='bottom')
elm.Line().at((0, -0.625)).down(1.25)
elm.Line().at((0, -1.875)).right(0.75).to((0.75, -1.875))
elm.Dot().at((0, -1.875)).label('V- node', loc='left')
rf = elm.Resistor().right().length(1.5).at((0.75, -1.875)).label('R1  (to output)', loc='bottom')
elm.Line().at((2.25, -1.875)).right(1.1651).to((3.4151, -1.875))
elm.Line().at((3.4151, -1.875)).up(1.875)
elm.Dot().at((3.4151, 0)).label('Vout node', loc='top')
elm.Line().at((0, -1.875)).left(1.5)
elm.Resistor().up().length(1.25).at((-1.5, -1.875)).label('R2', loc='left')
elm.Vdd().up().at((-1.5, -0.625)).label('+Vref')
elm.Line().at((3.4151, 0)).right(2).label('Vout', loc='top')
elm.Annotate().at((4.4, 1.6)).delta(1.0, 0.7).label('UTP = Vref + (Vsat - Vref)*R2/(R1+R2)\nLTP = Vref - (Vsat - Vref)*R2/(R1+R2)')
```

- `Vref` sets where the hysteresis band sits; the span is still `R2/(R1+R2)`.
- `R1 = R2` puts the band symmetrically around `Vref`.

## 7. Window Comparator

Two comparators watch the same input from above and below, so the output is active only
while the input lies inside a defined window.

```circuit
u1 = elm.Opamp(leads=True).right().at((0, 3)).label('U1', loc='center')
u2 = elm.Opamp(leads=True).right().at((0, -1)).label('U2', loc='center')
src = elm.SourceSin().right().length(2).at((-7, 1)).label('Vin', loc='left')
elm.Ground().down().at((-7, 1))
elm.Line().at((-5, 1)).right(2.5)
elm.Line().at((-2.5, 1)).up(1.625).to((-2.5, 2.375))
elm.Dot().at((-2.5, 2.375))
elm.Line().at((-2.5, 2.375)).right(2.5)
elm.Line().at((-2.5, 1)).down(1.375).to((-2.5, -0.375))
elm.Dot().at((-2.5, -0.375))
elm.Line().at((-2.5, -0.375)).right(2.5)
hi = elm.SourceV().up().length(1.5).at((-4.5, 0.625)).label('Vhi', loc='left')
elm.Line().at((-4.5, 2.125)).right(4.5)
elm.Dot().at((0, 3.625)).label('U1: +', loc='top')
lo = elm.SourceV().up().length(1.5).at((-4.5, -1.625)).label('Vlo', loc='left')
elm.Line().at((-4.5, -0.125)).right(4.5)
elm.Dot().at((0, -0.375)).label('U2: -', loc='top')
elm.Line().at((3.4151, 3)).right(1.5)
elm.Line().at((3.4151, -1)).right(1.5)
elm.Line().at((4.9151, 3)).down(2.25)
elm.Line().at((4.9151, -1)).down(1.25)
elm.Line().at((4.9151, 0.75)).right(1)
elm.Rect(corner1=(5.9151, -0.5), corner2=(9.4151, 2)).label('AND', loc='center')
elm.Line(arrow='->').at((9.4151, 0.75)).right(1.5).label('in window', loc='top')
elm.Annotate().at((-2.5, 4.4)).delta(0, 0.7).label('U1 output is high only when Vin < Vhi')
elm.Annotate().at((6.9, -1.6)).delta(0, -0.7).label('output high for\nVlo < Vin < Vhi\n(or the complement\nwith a NOR gate)')
```

- The window width is `Vhi - Vlo`; the centres are set by the two references.
- Adding hysteresis to each comparator stops chatter at the window edges.

## 8. Phase-Locked Loop (Block View)

A PLL locks a voltage-controlled oscillator to an external reference by comparing phases,
filtering the error, and feeding it back around the loop.

```circuit
elm.SourceSin().right().length(1.5).at((-8, 0)).label('reference in', loc='left')
elm.Line(arrow='->').at((-6.5, 0)).right(1)
elm.Rect(corner1=(-5.5, -1), corner2=(-1.5, 1)).label('Phase\ndetector', loc='center')
elm.Line(arrow='->').at((-1.5, 0)).right(1)
elm.Rect(corner1=(-0.5, -1), corner2=(2.5, 1)).label('Loop filter\n(low pass)', loc='center')
elm.Line(arrow='->').at((2.5, 0)).right(1).label('control voltage', loc='top')
elm.Rect(corner1=(3.5, -1), corner2=(6.5, 1)).label('VCO', loc='center')
elm.Line(arrow='->').at((6.5, 0)).right(1)
elm.Rect(corner1=(7.5, -1), corner2=(10.5, 1)).label('Divide by N', loc='center')
elm.Line(arrow='->').at((10.5, 0)).right(1.5).label('output', loc='top')
elm.Line().at((12, 0)).down(3)
elm.Line().at((12, -3)).left(19.5).to((-7.5, -3))
elm.Line(arrow='->').at((-7.5, -3)).up(2)
elm.Annotate().at((3, -4.4)).delta(0, -0.7).label('locked when the phase error settles to a constant and the loop filter holds a DC level')
elm.Annotate().at((-3.5, 1.4)).delta(0, 0.6).label('error = phase difference')
elm.Annotate().at((1, 1.4)).delta(0, 0.6).label('sets the average\nfrequency')
```

- Lock range and capture range differ; the loop filter bandwidth sets both.
- A divide-by-`N` in the feedback path multiplies the output frequency.

## 9. CMOS Transmission Gate

A complementary NMOS/PMOS pair passes the full input range with low on-resistance and very
high off isolation. The two gates need opposite drive phases.

```circuit
pm = elm.PMos().at((0, 2.5))
nm = elm.NMos().at((0, -0.5))
elm.Line().at((-3, -0.5)).right(3).to((0, -0.5))
elm.Line().at((-3, 0.833)).right(3).to((0, 0.833))
elm.Line().at((-3, -0.5)).up(1.333)
elm.Dot().at((-3, -0.5)).label('Vin', loc='left')
elm.Line().at((0, 2.5)).up(0.5)
elm.Line().at((0, 3)).right(3).to((3, 3))
elm.Line().at((3, 3)).down(6)
elm.Line().at((0, -2.167)).down(0.833)
elm.Line().at((0, -3)).right(3).to((3, -3))
elm.Dot().at((3, -3)).label('Vout', loc='bottom')
elm.Line().at((0, -2.167)).down(0.833).to((0, -3))
elm.Dot().at((0, -2.167))
elm.Line().at((-0.833, 2.0)).left(2.667).to((-3.5, 2.0)).label('phi_bar to PMOS gate', loc='left')
elm.Line().at((-0.833, -1.667)).left(2.667).to((-3.5, -1.667)).label('phi to NMOS gate', loc='left')
elm.Annotate().at((4.4, 1.4)).delta(0, 0.6).label('both devices are on when phi = 1\nand both are off when phi = 0')
elm.Annotate().at((4.4, -2.2)).delta(0, -0.6).label('Vin rides on both the NMOS drain\nand the PMOS drain, so the signal\npasses undiminished in both\ndirections')
```

- `Ron` is small only near mid-supply; the switch degrades toward the rails.
- Charge injection from the switch gates appears as a glitch on the held capacitor.

## 10. Sample-and-Hold

A switch charges a holding capacitor during the sample phase, and a buffer amplifier
delivers the stored voltage without loading it.

```circuit
sig = elm.SourceSin().right().length(2).at((-7, 0)).label('input', loc='left')
elm.Ground().down().at((-7, 0))
elm.Line().at((-5, 0)).right(1.5)
sw = elm.Switch().right().length(1.5).at((-3.5, 0)).label('S', loc='top')
elm.Dot().at((-2, 0)).label('sample', loc='top')
elm.Line().at((-2, 0)).right(1)
cap = elm.Capacitor().down().length(2).at((-1, 0)).label('Chold', loc='right')
elm.Line().at((-1, -2)).down(0.5)
elm.Ground().down().at((-1, -2.5))
elm.Line().at((-1, 0)).up(2.125)
op = elm.Opamp(leads=True).right().at((3, 1.5))
elm.Line().at((-1, 2.125)).right(4)
elm.Dot().at((0, 2.125)).label('buffer input', loc='top')
elm.Line().at((6.4151, 1.5)).right(2.5849).to((9, 1.5)).label('output follows the\nlast sampled value', loc='top')
elm.Dot().at((7.5, 1.5))
elm.Line().at((7.5, 1.5)).down(0.625)
elm.Line().at((7.5, 0.875)).left(4)
elm.Annotate().at((-4.6, 1.6)).delta(0, 0.6).label('switch open\n= hold')
elm.Annotate().at((-1, -3.4)).delta(0, -0.6).label('droop = I(leak) / Chold')
```

- The follower must draw negligible input current, or the capacitor droops.
- Practical ICs use a large hold capacitor and a leakage-free switch.

## 11. Relaxation Oscillator (Square-Wave Generator)

Cross-coupling a Schmitt trigger to an RC integrator gives a free-running square-wave
oscillator with no inductors.

```circuit
op = elm.Opamp(leads=True).right().at((0, 0))
elm.Line().at((0, 0.625)).up(1.25).to((0, 1.875))
elm.Line().at((0, 1.875)).right(3.4151)
elm.Line().at((3.4151, 1.875)).down(1.875)
elm.Dot().at((3.4151, 0))
elm.Resistor().right().length(1.5).at((0, 1.875)).label('R1', loc='top')
elm.Line().at((0, 1.875)).left(1.5)
elm.Resistor().down().length(1.25).at((-1.5, 1.875)).label('R2', loc='left')
elm.Ground().down().at((-1.5, 0.625))
elm.Line().at((0, -0.625)).left(2)
r = elm.Resistor().left().length(2).at((-2, -0.625)).label('R', loc='bottom')
c = elm.Capacitor().down().length(2).at((-4, -0.625)).label('C', loc='left')
elm.Line().at((-4, -2.625)).down(0.5)
elm.Ground().down().at((-4, -3.125))
elm.Line().at((-6, -0.625)).right(2)
elm.Line().at((-6, -0.625)).up(0.625).to((-6, 0))
elm.Annotate().at((-6, 0)).delta(0, 0.6).label('C charges toward\nthe opposite rail, then\nthe comparator flips')
elm.Line().at((3.4151, 0)).right(2).label('square wave', loc='top')
elm.Annotate().at((5.4, 1.4)).delta(1.0, 0.7).label('f = 1 / (2*RC*ln(1 + 2*R1/R2))\nfor R1 = R2:  f = 1/(1.386*R*C)')
```

- The capacitor charges exponentially toward the opposite rail, producing a triangular
  voltage at the inverting input and a square wave at the output.
- Frequency depends only on `R`, `C` and the ratio `R1/R2`.

## 12. Where a Comparator Breaks Down

Propagation delay plus feedback noise turns a fast crossing into ringing and false
triggers, which is the reason a real design adds hysteresis and filtering.

```circuit
elm.SourceSin().right().length(1.5).at((-8, 0)).label('slow ramp', loc='left')
elm.Line(arrow='->').at((-6.5, 0)).right(1)
elm.Rect(corner1=(-5.5, -1), corner2=(-2.5, 1)).label('input\nnoise', loc='center')
elm.Line(arrow='->').at((-2.5, 0)).right(1)
elm.Rect(corner1=(-1.5, -1), corner2=(1.5, 1)).label('comparator\nprop delay td', loc='center')
elm.Line(arrow='->').at((1.5, 0)).right(1)
elm.Rect(corner1=(2.5, -1), corner2=(5.5, 1)).label('output\nringing', loc='center')
elm.Line(arrow='->').at((5.5, 0)).right(1.5).label('unwanted\nedges', loc='top')
elm.Rect(corner1=(-4.5, -4.5), corner2=(-0.5, -2.5)).label('Schmitt\nhysteresis', loc='center')
elm.Rect(corner1=(0.5, -4.5), corner2=(4.5, -2.5)).label('input RC\nfilter', loc='center')
elm.Line(arrow='->').at((-0.5, -3.5)).right(1)
elm.Line(arrow='->').at((4.5, -3.5)).up(1.75).to((4.5, -1))
elm.Annotate().at((0, -5.6)).delta(0, -0.6).label('hysteresis must exceed the input noise; the filter must not slow the wanted edge')
elm.Annotate().at((7, 1.4)).delta(0, 0.6).label('each of these is a\nform of hysteresis')
```
