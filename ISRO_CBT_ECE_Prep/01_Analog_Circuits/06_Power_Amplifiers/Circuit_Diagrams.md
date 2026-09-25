# Power Amplifiers — Circuit Diagrams

Companion schematics for `Concepts.md`. A power amplifier delivers volts and amps into a
low-impedance load, so the design question is not only gain but **efficiency**,
**distortion** and **heat**.

## 1. Class A: Conduction Angle 360 Degrees

The transistor conducts for the whole cycle, so the output follows the input everywhere.
Efficiency is capped by the resistor/quiescent current.

```circuit
q = elm.BjtNpn().at((0, 0))
src = elm.SourceSin().up().length(2).at((-4, -4)).label('input', loc='left')
elm.Ground().down().at((-4, -4))
elm.Line().at((-4, -2)).up(2).to((-4, 0))
elm.Line().at((-4, 0)).right(4)
elm.Dot().at((-1, 0)).label('base drive', loc='bottom')
rb = elm.Resistor().up().length(1.5).at((-1, 0)).label('Rb', loc='left')
elm.Vdd().at((-1, 1.5)).label('VCC')
elm.Line().at((0.75167, 0.69667)).up(1.30333)
elm.Dot().at((0.75167, 2)).label('output node', loc='left')
elm.Line().at((0.75167, 2)).up(1.5)
elm.Vdd().at((0.75167, 3.5)).label('VCC')
rl = elm.Resistor().down().length(1.5).at((4, 2)).label('RL', loc='right')
elm.Line().at((0.75167, 2)).right(3.24833).to((4, 2))
elm.Capacitor().right().length(1).at((4, 2)).label('coupling C', loc='top')
elm.Line().at((5, 2)).right(1.5)
elm.Line().at((6.5, 2)).down(1.5)
elm.Ground().down().at((6.5, 0.5))
elm.Annotate().at((6.5, 1.2)).delta(0, 0.6).label('AC load: the output\nfollows the base swing\nwith gain gm*RC')
elm.Annotate().at((-4, 1.6)).delta(0, 0.6).label('Q-point set so the transistor\nnever leaves its active region')
```

- Maximum theoretical efficiency is 25% for a resistor-loaded stage, 50% for a
  transformer-coupled one.
- Class A is linear and low distortion, but wastes current when the input is zero.

## 2. Class B and the Crossover Distortion

Two transistors take turns, one for each half cycle. The base-emitter threshold leaves a
dead zone around zero, which is the crossover distortion.

```circuit
q1 = elm.BjtNpn().at((0, 2.5))
q2 = elm.BjtNpn().at((0, -1.5))
src = elm.SourceSin().right().length(2).at((-7, 0.5)).label('input', loc='left')
elm.Ground().down().at((-7, 0.5))
elm.Line().at((-5, 0.5)).right(1.5)
elm.Dot().at((-3.5, 0.5)).label('input', loc='bottom')
rb = elm.Resistor().down().length(1.5).at((-3.5, 0.5)).label('Rb', loc='left')
elm.Line().at((-3.5, 0)).right(3.5)
elm.Dot().at((-1, 0)).label('bias', loc='top')
elm.Line().at((-1, 0)).up(1.80333).to((-1, 1.80333))
elm.Dot().at((-1, 1.80333)).label('Q1 base', loc='left')
elm.Line().at((-1, 1.80333)).right(1).to((0, 1.80333))
elm.Line().at((-1, 0)).down(1.80333)
elm.Dot().at((-1, -1.80333)).label('Q2 base', loc='left')
elm.Line().at((-1, -1.80333)).right(1).to((0, -1.80333))
elm.Annotate().at((-1, 0.6)).delta(-0.4, 0).label('no bias: each base needs\nabout 0.7 V before it conducts')
elm.Line().at((0.75167, 3.19667)).up(0.80333)
elm.Dot().at((0.75167, 4)).label('emitter follower pair', loc='left')
elm.Line().at((0.75167, -2.19667)).down(0.80333)
elm.Dot().at((0.75167, -3)).label('common node', loc='left')
elm.Line().at((0.75167, 4)).right(3.24833).to((4, 4))
rl = elm.Resistor().down().length(2).at((4, 4)).label('RL', loc='right')
elm.Line().at((4, 2)).right(1.5)
elm.Line().at((5.5, 2)).down(1.5)
elm.Ground().down().at((5.5, 0.5))
elm.Line().at((0.75167, -3)).down(0.5)
elm.Vss().at((0.75167, -3.5)).label('-VEE')
elm.Annotate().at((6.5, 3.4)).delta(0, 0.6).label('each device conducts for\nabout 180 degrees')
elm.Annotate().at((6.5, -2.2)).delta(0, -0.6).label('crossover notch appears when\nboth transistors are off near zero')
```

- With `Vcc = -Vee` symmetry, the peak efficiency is 78.5% and the maximum output swing is
  `Vcc - Vbe`.
- Distortion is mostly third-harmonic, so it is reduced by negative feedback or by biasing
  the pair slightly into conduction.

## 3. Class AB: The Practical Compromise

A small forward bias (from two diodes, or a `Vbe` multiplier) removes the dead zone while
keeping the quiescent current low.

```circuit
d1 = elm.Diode().up().length(1).at((-2, -1.25)).label('D1', loc='left')
d2 = elm.Diode().up().length(1).at((-2, -0.25)).label('D2', loc='left')
elm.Line().at((-2, 0.75)).up(0.75)
elm.Vdd().at((-2, 1.5)).label('VCC')
elm.Line().at((-2, -1.25)).down(0.75)
elm.Vss().at((-2, -2)).label('-VEE')
elm.Line().at((-2, -1.25)).right(2).to((0, -1.25))
elm.Line().at((-2, 0.75)).right(2).to((0, 0.75))
elm.Line().at((-2, -0.25)).right(1.5).to((-0.5, -0.25))
elm.Dot().at((-2, -0.25)).label('bias from the driver', loc='left')
src = elm.SourceSin().right().length(1.5).at((-4, -0.25)).label('input', loc='left')
elm.Ground().down().at((-4, -0.25))
elm.Line().at((-2.5, -0.25)).right(0.5)
q1 = elm.BjtNpn().at((0.75167, 0.75))
q2 = elm.BjtNpn().at((0.75167, -1.25))
elm.Dot().at((0, 0.75)).label('Q1 base', loc='left')
elm.Dot().at((0, -1.25)).label('Q2 base', loc='left')
elm.Line().at((1.50334, 1.44667)).up(0.55333)
elm.Dot().at((1.50334, 2)).label('output', loc='top')
elm.Line().at((1.50334, 2)).right(2.49666).to((4, 2))
rl = elm.Resistor().down().length(2).at((4, 2)).label('RL', loc='right')
elm.Line().at((4, 0)).right(1.5)
elm.Line().at((5.5, 0)).down(1.5)
elm.Ground().down().at((5.5, -1.5))
elm.Line().at((1.50334, 0.05333)).down(2.55333)
elm.Dot().at((1.50334, 0.05333))
elm.Line().at((1.50334, -0.55333)).down(1.94667)
elm.Line().at((1.50334, -1.94667)).down(0.55333)
elm.Dot().at((1.50334, -2.5)).label('common emitter node', loc='right')
elm.Annotate().at((-5.5, 1.4)).delta(0, 0.6).label('the diode string drops about 1.4 V, so\neach base sits 0.7 V above its emitter\nand both devices conduct a little at idle')
elm.Annotate().at((7, 1.2)).delta(0, 0.6).label('quiescent current is now non-zero,\nso efficiency sits between\nclass A and class B')
elm.Annotate().at((1, -3.6)).delta(0, -0.6).label('this is a Darlington-style drive: the diode bias is what keeps\nthe pair just inside conduction instead of fully off')
``````

- Typical quiescent bias is 2 to 10% of the peak output current.
- Thermal tracking matters: a `Vbe` multiplier with a transistor matched to the output pair
  follows temperature better than fixed diodes.

## 4. The Output Stage as a Feedback Loop

Real audio output stages wrap the whole thing in a feedback loop, so the crossover
distortion and the gain error are both corrected by the loop.

```circuit
op = elm.Opamp(leads=True).right().at((-6, 0)).label('driver', loc='center')
elm.Rect(corner1=(-1, 1), corner2=(4, 3.5)).label('complementary\noutput pair', loc='center')
elm.Line(arrow='->').at((-1, 2.25)).right(2)
elm.Line().at((4, 2.25)).right(2).to((6, 2.25))
elm.Dot().at((6, 2.25)).label('Vout', loc='top')
rl = elm.Resistor().down().length(2).at((6, 2.25)).label('RL', loc='right')
elm.Line().at((6, 0.25)).right(1)
elm.Ground().down().at((7, 0.25))
elm.Line().at((-6, 0.625)).right(1)
elm.SourceSin().right().length(1.5).at((-9.5, 0.625)).label('Vin', loc='left')
elm.Ground().down().at((-9.5, 0.625))
elm.Line().at((-6, -0.625)).left(1.5).to((-7.5, -0.625))
rf = elm.Resistor().right().length(2).at((-7.5, -0.625)).label('Rf', loc='bottom')
elm.Line().at((-5.5, -0.625)).up(2.875).to((-5.5, 2.25))
elm.Line().at((-5.5, 2.25)).right(2.5).to((-3, 2.25))
elm.Dot().at((-5.5, 2.25))
elm.Annotate().at((-5.5, 4.4)).delta(0, 0.6).label('the loop senses the real output, so gain error and\ncrossover distortion are both divided by 1 + A*b')
elm.Annotate().at((-1, -2.2)).delta(0, -0.6).label('the driver can be a low-power op-amp: the loop supplies\nthe current gain and the linearity')
```

- Closed-loop gain is `1 + Rf/Rin`, set by resistors rather than by transistor `gm`.
- The loop must stay stable at the load, so in-situ capacitance compensation is often used.

## 5. Class C: Conduction Angle Below 180 Degrees

The transistor conducts only around the peak of the cycle, so efficiency is high but the
output is a pulse train that must be filtered.

```circuit
q = elm.BjtNpn().at((0, 0))
src = elm.SourceSin().up().length(2).at((-4, -4)).label('input', loc='left')
elm.Ground().down().at((-4, -4))
elm.Line().at((-4, -2)).up(2).to((-4, 0))
elm.Line().at((-4, 0)).right(4)
rb = elm.Resistor().up().length(1.5).at((-1, 0)).label('Rb', loc='left')
elm.Vdd().at((-1, 1.5)).label('VCC')
elm.Line().at((0.75167, 0.69667)).up(1.30333)
elm.Line().at((0.75167, 2)).up(1.5)
elm.Vdd().at((0.75167, 3.5)).label('VCC')
elm.Line().at((0.75167, 2)).right(2.24833).to((3, 2))
l1 = elm.Inductor().right().length(1.5).at((3, 2)).label('tank L', loc='bottom')
c1 = elm.Capacitor().down().length(1.5).at((4.5, 2)).label('C', loc='right')
elm.Line().at((4.5, 0.5)).down(0.5)
elm.Ground().down().at((4.5, 0))
elm.Line().at((4.5, 2)).up(0.75).to((4.5, 2.75))
elm.Line().at((4.5, 2.75)).left(1.5).to((3, 2.75))
elm.Line().at((4.5, 2.75)).down(1.25).to((4.5, 1.5))
elm.Annotate().at((-4, 1.4)).delta(0, 0.6).label('bias below cutoff: current flows\nonly near the peak of the cycle')
elm.Annotate().at((6, 2.2)).delta(0, 0.6).label('the LC tank turns the pulse\ntrain back into a sine at\nthe resonant frequency')
```

- Efficiency can exceed 80%, but conduction angle below 180 degrees means strong harmonic
  content.
- Class C is used where a tuned load removes the harmonics: RF power stages, not audio.

## 6. Class D: Switching Amplifier

The transistor is driven fully on or fully off, so dissipation during switching is the only
loss. The switching waveform is reconstructed by the output filter.

```circuit
elm.Rect(corner1=(-9, -1.5), corner2=(-5, 1.5)).label('PWM\nmodulator', loc='center')
elm.Line(arrow='->').at((-5, 0)).right(2)
elm.Rect(corner1=(-3, -1.5), corner2=(1, 1.5)).label('H-bridge\nswitching stage', loc='center')
elm.Line(arrow='->').at((1, 0)).right(2)
elm.Dot().at((3, 0)).label('switched output', loc='top')
elm.Line().at((3, 0)).right(1.5).to((4.5, 0))
l1 = elm.Inductor().right().length(1.5).at((4.5, 0)).label('output filter L', loc='bottom')
c1 = elm.Capacitor().down().length(1.5).at((6, 0)).label('C', loc='right')
elm.Line().at((6, -1.5)).down(0.5)
elm.Ground().down().at((6, -2))
elm.Line().at((6, 0)).up(0.75)
elm.Line().at((6, 0.75)).left(1.5)
elm.Line().at((4.5, 0.75)).down(0.75)
elm.Line().at((4.5, 0.75)).right(1.5)
rl = elm.Resistor().down().length(1.5).at((6, 0.75)).label('RL', loc='right')
elm.Line().at((6, -0.75)).down(0.5)
elm.Ground().down().at((6, -1.25))
elm.Annotate().at((-7, 2.6)).delta(0, 0.6).label('three-level PWM: the switching frequency\nis a few times the highest audio frequency')
elm.Annotate().at((8.5, 0.6)).delta(0, 0.6).label('after the filter the\nload sees a sine,\nnot a square wave')
elm.Annotate().at((0, -3.4)).delta(0, -0.6).label('losses: switching, conduction and dead time only,\nso efficiency above 90% is routine')
```

- The switching transitions are the only lossy moments; conduction loss is nearly zero.
- Filter cutoff must be above the audio band and well below the switching carrier.

## 7. Class E and the Resonant Load

The device is driven into saturation only at the transition, and the load is a resonant
network, so the peak current is high but the average loss stays low.

```circuit
q = elm.BjtNpn().at((0, 0))
src = elm.SourceSin().up().length(2).at((-4, -4)).label('drive pulse', loc='left')
elm.Ground().down().at((-4, -4))
elm.Line().at((-4, -2)).up(2).to((-4, 0))
elm.Line().at((-4, 0)).right(4)
elm.Line().at((0.75167, 0.69667)).up(1.30333)
elm.Line().at((0.75167, 2)).up(1.5)
elm.Vdd().at((0.75167, 3.5)).label('VCC')
elm.Line().at((0.75167, 2)).right(2.24833).to((3, 2))
ser = elm.Inductor().right().length(1.5).at((3, 2)).label('series L', loc='bottom')
elm.Line().at((4.5, 2)).right(0.5)
sh = elm.Capacitor().down().length(1.5).at((5, 2)).label('shunt C', loc='right')
elm.Line().at((5, 0.5)).down(0.5)
elm.Ground().down().at((5, 0))
elm.Line().at((5, 2)).up(0.75)
elm.Line().at((5, 2.75)).left(2)
elm.Line().at((3, 2.75)).down(0.75)
elm.Line().at((3, 2.75)).right(2.5)
elm.Annotate().at((-4, 1.2)).delta(0, 0.6).label('the transistor is saturated only for a\nsmall part of the cycle')
elm.Annotate().at((6.5, 2.2)).delta(0, 0.6).label('the series L and shunt C form\nthe load, so voltage and\ncurrent peaks are out of phase')
elm.Annotate().at((0, -2.6)).delta(0, -0.6).label('efficiency above 90% is possible, but the circuit is narrowband:\nit only works at the design frequency')
```

- Class E is a narrowband design: the resonant load is part of the power conversion.
- Used in RF transmitters and in very high frequency switching converters.

## 8. Complementary-Symmetry Comparison (Block View)

The same four bias classes differ only in how long each device conducts, and that single
fact explains every efficiency number.

```circuit
elm.Rect(corner1=(-9, 2.5), corner2=(-4, 5)).label('class A: 360 deg\n25% (R load) / 50%\nlowest distortion', loc='center')
elm.Rect(corner1=(-2, 2.5), corner2=(3, 5)).label('class B: 180 deg\n78.5% max\ncrossover notch', loc='center')
elm.Rect(corner1=(5, 2.5), corner2=(10, 5)).label('class AB: 180 + idle\nup to 80%\nthe audio standard', loc='center')
elm.Rect(corner1=(-9, -1.5), corner2=(-4, 1)).label('class C: < 180 deg\n> 80%\nneeds a tuned load', loc='center')
elm.Rect(corner1=(-2, -1.5), corner2=(3, 1)).label('class D: switching\n> 90%\nneeds PWM and a filter', loc='center')
elm.Rect(corner1=(5, -1.5), corner2=(10, 1)).label('class E/F: resonant\n> 90%, narrowband\nRF and converters', loc='center')
elm.Annotate().at((0.5, 5.6)).delta(0, 0.6).label('efficiency rises as the conduction angle shrinks;')
elm.Annotate().at((0.5, 6.2)).delta(0, 0.6).label('linearity and simplicity fall as it shrinks')
elm.Annotate().at((0.5, -2.4)).delta(0, -0.6).label('choose the class from the load and the band, not from the efficiency alone')
```

## 9. Thermal and Safe-Area Limits

A power stage is limited by junction temperature and by safe operating area, not by gain.

```circuit
elm.Rect(corner1=(-9, -1.5), corner2=(-3, 1.5)).label('dissipation\nPd = Vce*Ic - Vout*Iout', loc='center')
elm.Line(arrow='->').at((-3, 0)).right(1.5)
elm.Rect(corner1=(-1.5, -1.5), corner2=(2, 1.5)).label('junction\ntemperature Tj', loc='center')
elm.Line(arrow='->').at((2, 0)).right(1.5)
elm.Rect(corner1=(3.5, -1.5), corner2=(8, 1.5)).label('heatsink and\ncase temperature', loc='center')
elm.Line().at((2, 3)).right(6)
elm.Line().at((8, 3)).down(1.5)
elm.Line(arrow='<-').at((2, 3)).left(3.5)
elm.Annotate().at((-1, 2.4)).delta(0, 0.6).label('thermal feedback: more heat, more bias current, less headroom')
elm.Rect(corner1=(-9, 3.5), corner2=(-3, 6)).label('safe operating area:\nIc vs Vce limit', loc='center')
elm.Rect(corner1=(-1.5, 3.5), corner2=(3, 6)).label('second breakdown:\na Vce rise can collapse Ic', loc='center')
elm.Rect(corner1=(4.5, 3.5), corner2=(9, 6)).label('fix: emitter ballast resistors\nor current sensing', loc='center')
elm.Line(arrow='->').at((-3, 4.75)).right(1.5)
elm.Line(arrow='->').at((3, 4.75)).right(1.5)
elm.Annotate().at((0, -2.6)).delta(0, -0.6).label('without thermal compensation the stage runs away as it heats up:\nit is the most common failure in a power amplifier')
```

- Derate the SOA curve for pulse duty cycle and for the ambient temperature.
- Emitter resistors of 0.1 to 1 ohm are the standard cure for thermal runaway and for
  current sharing.
