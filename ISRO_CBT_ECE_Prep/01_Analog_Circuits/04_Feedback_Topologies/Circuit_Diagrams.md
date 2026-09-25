# Feedback Topologies — Circuit Diagrams

Companion schematics for `Concepts.md`. A feedback amplifier is described by **how the
input is mixed** (series or shunt) and **how the output is sampled** (shunt or series).
Those two choices give the four basic topologies and fix the input and output
impedances.

## 1. Voltage-Series (Series-Shunt) Feedback — Non-Inverting Amp

The input is applied in series with the feedback at the `+` terminal, and the output voltage
is sampled with a divider. Gain is set by resistors, `Rin` is very high and `Rout` is low.

```circuit
op = elm.Opamp(leads=True).right().at((0, 0))
src = elm.SourceSin().right().length(2).at((-6.5, 0.625)).label('Vin', loc='left')
elm.Ground().down().at((-6.5, 0.625))
elm.Line().at((-4.5, 0.625)).right(4.5)
elm.Dot().at((0, 0.625)).label('series mixing at the input', loc='top')
elm.Line().at((0, -0.625)).left(2.5)
elm.Dot().at((-2.5, -0.625)).label('V- node', loc='left')
elm.Resistor().down().length(1.25).at((-2.5, -1.875)).label('R1', loc='left')
elm.Ground().down().at((-2.5, -3.125))
elm.Line().at((-2.5, -1.875)).up(1.25).to((-2.5, -0.625))
rf = elm.Resistor().up().length(3).at((3.4151, 0)).label('R2 (beta)', loc='right')
elm.Line().at((3.4151, 3)).right(2).to((5.4151, 3)).label('Vout', loc='top')
elm.Dot().at((3.4151, 3)).label('output node', loc='bottom')
rg = elm.Resistor().down().length(3).at((4.4151, 3)).label('Rg', loc='right')
elm.Line().at((4.4151, 0)).down(1.875)
elm.Line().at((4.4151, -1.875)).left(6.915).to((-2.5, -1.875))
elm.Annotate().at((7, 0.4)).delta(0, 0.6).label('Rin is raised and Rout is lowered:\nthe workhorse amplifier for\na voltage output')
```

- Closed-loop gain `1 + R2/R1`; the loop gain is `A*beta` with `beta = R1/(R1+R2)`.
- A differential input at the `+` terminal multiplies `Rin` by `1 + A*beta`.

## 2. Voltage-Shunt (Shunt-Shunt) Feedback — Transimpedance Amp

Input current enters the same node as the feedback current, and the output voltage is
sampled with a divider. `Rin` is low and `Rout` is low.

```circuit
op = elm.Opamp(leads=True).right().at((0, 0))
ip = elm.SourceI().up().length(2).at((-7, -2.625)).label('Iin', loc='left')
elm.Ground().down().at((-7, -2.625))
elm.Line().at((-7, -0.625)).right(7)
elm.Dot().at((-1.5, -0.625)).label('shunt summing node', loc='bottom')
elm.Line().at((-1.5, -0.625)).down(2).to((-1.5, -2.625))
elm.Line().at((-1.5, -2.625)).right(0.9151).to((-0.5849, -2.625))
rf = elm.Resistor().right().length(2).at((-0.5849, -2.625)).label('Rf', loc='bottom')
elm.Line().at((1.4151, -2.625)).right(3).to((4.4151, -2.625))
elm.Line().at((4.4151, -2.625)).up(2.625).to((4.4151, 0))
elm.Dot().at((4.4151, 0)).label('output node', loc='top')
elm.Line().at((4.4151, 0)).right(1.5).to((5.9151, 0)).label('Vout', loc='top')
elm.Line().at((0, 0.625)).left(1.5).to((-1.5, 0.625))
elm.Line().at((-1.5, 0.625)).up(1).to((-1.5, 1.625))
elm.Ground().up().at((-1.5, 1.625))
elm.Annotate().at((7, 0.4)).delta(0, 0.6).label('Vout = -Iin * Rf: low Rin and low Rout\nmean the next stage is well driven')
```

- `Zin` and `Zout` are both small, so this stage is safe to cascade.
- A photodiode or phototransistor front end is the classic use.

## 3. Current-Series (Series-Series) Feedback — Emitter Degeneration

The input is mixed in series (the `vbe` difference) and the output is sampled in series (the
collector current through the emitter resistor). Both `Rin` and `Rout` are high.

```circuit
q = elm.BjtNpn().at((0, 0))
src = elm.SourceV().up().length(2).at((-4, -4)).label('Vin', loc='left')
elm.Ground().down().at((-4, -4))
elm.Line().at((-4, -2)).up(2).to((-4, 0))
elm.Line().at((-4, 0)).right(1).to((-3, 0))
elm.Capacitor().right().length(1).at((-3, 0)).label('Cin (coupling)', loc='top')
elm.Line().at((-2, 0)).right(2).to((0, 0))
elm.Dot().at((-1.5, 0))
rb = elm.Resistor().up().length(1.5).at((-1.5, 0)).label('Rb', loc='left')
elm.Vdd().at((-1.5, 1.5)).label('VCC')
elm.Line().at((0.75167, 0.69667)).up(1.303).to((0.75167, 2))
elm.Dot().at((0.75167, 2)).label('output node', loc='left')
rl = elm.Resistor().up().length(1.5).at((0.75167, 2)).label('RL', loc='left')
elm.Vdd().at((0.75167, 3.5)).label('VCC')
elm.Line().at((0.75167, 2)).right(2.5).label('iout', loc='top')
elm.Line().at((0.75167, -0.69667)).down(0.303).to((0.75167, -1))
re = elm.Resistor().down().length(1.5).at((0.75167, -1)).label('Re', loc='right')
elm.Line().at((0.75167, -2.5)).down(0.5).to((0.75167, -3))
elm.Ground().down().at((0.75167, -3))
elm.Annotate().at((2.4, 1.2)).delta(0.6, 0.6).label('the emitter resistor is the\nseries sampling element')
elm.Annotate().at((-4.4, 0.8)).delta(0, 0.6).label('series mixing: vbe = vin - iout*Re')
elm.Annotate().at((3.2, 3.4)).delta(0.6, 0.6).label('both Rin and Rout\nare raised by the loop')
```

- Gain approaches `gm*Re`, which makes the stage linear and predictable.
- Series-series stages give current gain with high input and output impedance.

## 4. Current-Shunt (Shunt-Series) Feedback — Series Regulator

The input is mixed at a summing node and the output current is sensed in series, so `Rin`
is low while `Rout` stays high. This is the block picture of an LM317 or a constant-current
source.

```circuit
elm.Rect(corner1=(-9, -1), corner2=(-5, 1)).label('error amplifier', loc='center')
elm.Rect(corner1=(-3, -1), corner2=(0, 1)).label('pass\ntransistor', loc='center')
elm.Rect(corner1=(2, -1), corner2=(5, 1)).label('sense\nresistor', loc='center')
elm.Line(arrow='->').at((-5, 0)).right(2)
elm.Line(arrow='->').at((0, 0)).right(2)
elm.Line(arrow='->').at((5, 0)).right(2).to((7, 0)).label('regulated output', loc='top')
elm.Dot().at((7, 0))
r1 = elm.Resistor().down().length(1.5).at((7, 0)).label('R1', loc='right')
elm.Line().at((7, -1.5)).down(0.5).to((7, -2))
elm.Dot().at((7, -2))
r2 = elm.Resistor().down().length(1.5).at((7, -2)).label('R2', loc='right')
elm.Line().at((7, -3.5)).down(2).to((7, -5.5))
elm.Line().at((7, -5.5)).left(16).to((-9, -5.5))
elm.Line(arrow='->').at((-9, -5.5)).up(4.5).to((-9, -1))
elm.Rect(corner1=(-9, -4), corner2=(-5, -2)).label('bandgap\nreference', loc='center')
elm.Line(arrow='->').at((-7, -2)).up(1).to((-7, -1))
elm.Line(arrow='->').at((5, -2)).right(1.5).to((6.5, -2)).label('reference', loc='bottom')
elm.Annotate().at((9.5, 1.4)).delta(0.6, 0.6).label('the sense element is in series with the load,\nso Rout stays high')
elm.Annotate().at((-13, 1.4)).delta(0, 0.6).label('input injected at the\nsumming node (shunt)')
```

- The sense resistor turns output current into a feedback voltage.
- A feedback path *across* the output would instead give low `Rout`: that is voltage-shunt.

## 5. How the Input Is Mixed

Mixing sets the input impedance: a series difference multiplies it, a shunt summing node
reduces it.

```circuit
elm.Rect(corner1=(-8, 2), corner2=(-3, 4.5)).label('input port', loc='center')
elm.Rect(corner1=(1, 2), corner2=(6, 4.5)).label('amplifier', loc='center')
elm.Line(arrow='->').at((-3, 3.25)).right(4)
elm.Rect(corner1=(-8, -1.5), corner2=(-3, 1)).label('series mixing:\ndifference of\nvoltages', loc='center')
elm.Line(arrow='->').at((-5.5, 1)).up(1).to((-5.5, 2))
elm.Rect(corner1=(1, -1.5), corner2=(6, 1)).label('shunt mixing:\nsum of\ncurrents', loc='center')
elm.Line(arrow='->').at((-4, -1)).up(3).to((-4, 2))
elm.Annotate().at((-1.5, 5.2)).delta(0, 0.6).label('series mixing: Rin becomes (1 + A*b) * Rin_open')
elm.Annotate().at((-1.5, -2.4)).delta(0, -0.6).label('shunt mixing: Rin becomes Rin_open / (1 + A*b)')
```

## 6. How the Output Is Sampled

Sampling sets the output impedance: a shunt sample lowers it, a series sample keeps it high.

```circuit
elm.Rect(corner1=(-8, 2), corner2=(-3, 4.5)).label('amplifier', loc='center')
elm.Rect(corner1=(1, 2), corner2=(6, 4.5)).label('load', loc='center')
elm.Line(arrow='->').at((-3, 3.25)).right(4)
elm.Rect(corner1=(-8, -1.5), corner2=(-3, 1)).label('shunt sampling:\nvoltage across\nthe output', loc='center')
elm.Line(arrow='->').at((-5.5, 1)).up(1).to((-5.5, 2))
elm.Rect(corner1=(1, -1.5), corner2=(6, 1)).label('series sampling:\ncurrent through\nthe output', loc='center')
elm.Line(arrow='->').at((-4, -1)).up(3).to((-4, 2))
elm.Annotate().at((-1.5, 5.2)).delta(0, 0.6).label('shunt sampling: Rout falls to Rout_open / (1 + A*b)')
elm.Annotate().at((-1.5, -2.4)).delta(0, -0.6).label('series sampling: Rout rises to (1 + A*b) * Rout_open')
```

## 7. The Four Topologies at a Glance

| Topology | Input mixing | Output sampling | Rin | Rout | Example |
|---|---|---|---|---|---|
| Voltage-series | series | shunt | high | low | non-inverting op-amp |
| Voltage-shunt | shunt | shunt | low | low | inverting op-amp |
| Current-series | series | series | high | high | CE with emitter resistor |
| Current-shunt | shunt | series | low | high | series regulator, constant-current source |

## 8. Closed-Loop Gain and Desensitivity

Feedback divides the gain by `1/(1+T)` and divides the sensitivity to everything inside the
loop by the same factor.

```circuit
elm.Rect(corner1=(-8, -1), corner2=(-3, 1)).label('forward\ngain A', loc='center')
elm.Rect(corner1=(-8, -4.5), corner2=(-3, -2.5)).label('feedback\nnetwork b', loc='center')
elm.Line(arrow='->').at((-3, 0)).right(6)
elm.Dot().at((3, 0)).label('output', loc='top')
elm.Line().at((3, 0)).down(2.75).to((3, -2.75))
elm.Line(arrow='->').at((3, -2.75)).left(6).to((-3, -3.5))
elm.Line().at((-3, -3.5)).up(2.5)
elm.Line().at((-8, 0)).left(1.5).to((-9.5, 0))
elm.Line().at((-9.5, 0)).down(1).to((-9.5, -1))
elm.Dot().at((-9.5, -1)).label('error node', loc='left')
elm.Line().at((-9.5, -1)).right(6.5).to((-3, -1))
elm.Line().at((-9.5, -1)).down(3).to((-9.5, -4))
elm.Line(arrow='->').at((-9.5, -4)).right(6.5).to((-3, -4))
elm.Annotate().at((6, 0)).delta(0, 0.7).label('Af = A / (1 + A*b)')
elm.Annotate().at((6, -3.6)).delta(0, -0.6).label('sensitivity to A and to every\ndrift inside the loop is\nreduced by 1 + A*b')
```

- With a loop gain of `100`, the closed-loop gain and every tolerance inside the loop are
  `100x` better than without feedback.

## 9. Loop Gain Controls Accuracy and Bandwidth

The loop gain is the product of amplifier gain and feedback factor. It decides both how
accurate the closed-loop gain is and how fast the loop can settle.

```circuit
elm.Line().at((0, 0)).right(9)
elm.Line().at((0, 0)).up(4)
elm.Line().at((0.5, 0.5)).right(1.5)
elm.Line().at((2, 0.5)).to((2.75, 1.85))
elm.Line().at((2.75, 1.85)).to((3.5, 3.2))
elm.Line().at((3.5, 3.2)).to((4.25, 2.5))
elm.Line().at((4.25, 2.5)).to((5.75, 1.4))
elm.Line().at((5.75, 1.4)).to((7.5, 0.6))
elm.Line().at((0.5, 1.6)).right(6.5)
elm.Line().at((4, 1.6)).up(1.15).to((4, 2.75))
elm.Annotate().at((1.5, 3.6)).delta(0, 0.6).label('open-loop gain, rising then\nrolling off at its pole')
elm.Annotate().at((6.5, 1.6)).delta(0, 0.6).label('closed-loop gain')
elm.Annotate().at((4, 3.4)).delta(0, 0.6).label('loop gain T = A*b:\nthe vertical gap between\nthe two curves')
elm.Annotate().at((2.2, -0.9)).delta(0, -0.6).label('where T = 1 the closed-loop bandwidth is set')
```

- Stability needs phase margin at the frequency where the loop gain crosses 1 unit.
- Extra poles or pure delay inside the loop turn that crossing into ringing.

## 10. Identifying the Topology From a Schematic

Ask where the input enters, then where the feedback is taken.

```circuit
elm.Rect(corner1=(-9, 2), corner2=(-3, 4.5)).label('1. where does the input enter?\nto a + or - input, or to the same\nnode as the feedback?', loc='center')
elm.Rect(corner1=(-9, -1), corner2=(-3, 1.5)).label('2. where is the feedback taken?\nacross a divider (shunt), or in\nseries with the load (series)?', loc='center')
elm.Line(arrow='->').at((-6, 2)).down(1)
elm.Rect(corner1=(-1, 2), corner2=(3, 4.5)).label('input is series\n-> Rin is high', loc='center')
elm.Rect(corner1=(5, 2), corner2=(9, 4.5)).label('input is shunt\n-> Rin is low', loc='center')
elm.Line(arrow='->').at((-3, 3.25)).right(2)
elm.Line(arrow='->').at((3, 3.25)).right(2)
elm.Line(arrow='->').at((-6, -1)).up(2).to((-6, 2))
elm.Rect(corner1=(-1, -1.5), corner2=(4, 1.5)).label('only four combinations\nexist: the names follow', loc='center')
elm.Line(arrow='->').at((-3, 0)).right(2)
elm.Rect(corner1=(5.5, -1.5), corner2=(10, 1)).label('series + shunt = voltage-series\nseries + series = current-series\nshunt + shunt = voltage-shunt\nshunt + series = current-shunt', loc='center')
elm.Annotate().at((7.75, -2.3)).delta(0, -0.6).label('the answer set is closed')
```

## 11. Measuring Loop Gain in a Real Circuit

Breaking the loop and driving it converts the closed-loop amplifier into an open-loop test
bench, so `A*b` can be read directly with a meter.

```circuit
src = elm.SourceV().up().length(1.5).at((-7, -1.25)).label('inject 1 V', loc='left')
elm.Ground().down().at((-7, -1.25))
elm.Line().at((-7, 0.25)).right(1).to((-6, 0.25))
elm.Dot().at((-6, 0.25)).label('summing node', loc='top')
elm.Line().at((-6, 0.25)).right(1).to((-5, 0.25))
elm.Rect(corner1=(-5, -1), corner2=(-1, 1.5)).label('forward path A', loc='center')
elm.Line(arrow='->').at((-1, 0.25)).right(1).to((0, 0.25))
elm.Dot().at((0, 0.25)).label('A output', loc='bottom')
elm.Rect(corner1=(0, -0.75), corner2=(3.5, 1.25)).label('feedback network b', loc='center')
elm.Line().at((3.5, 0.25)).right(2).to((5.5, 0.25))
elm.Rect(corner1=(5.5, -0.5), corner2=(8, 1)).label('meter', loc='center')
elm.Dot().at((3.5, 0.25)).label('b output', loc='top')
elm.Line().at((3.5, 0.25)).down(2.5).to((3.5, -2.25))
elm.Line().at((3.5, -2.25)).left(9.5).to((-6, -2.25))
elm.Line(arrow='->').at((-6, -2.25)).up(2.5).to((-6, 0.25))
elm.Annotate().at((5.5, 1.4)).delta(0, 0.6).label('read b*Vout here')
elm.Annotate().at((-7, 1.4)).delta(0, 0.6).label('cut the loop, drive it,\nthen T = A*b is on the meter')
```

- A single frequency is not enough: repeat the measurement across the band to see where
  `T` falls through 1 unit.
- Network analysers do this automatically by injecting a signal into the loop.

## 12. Feedback in Discrete Circuits

The same four combinations appear in transistor stages; the sensing element is what changes.

```circuit
elm.Rect(corner1=(-9, 2), corner2=(-4, 4.5)).label('CE with emitter resistor\n(current-series, high in and out)', loc='center')
elm.Rect(corner1=(-2, 2), corner2=(3, 4.5)).label('CE with collector-to-base resistor\n(voltage-shunt, low in and out)', loc='center')
elm.Rect(corner1=(5, 2), corner2=(10, 4.5)).label('Emitter follower\n(series sample, low out)', loc='center')
elm.Rect(corner1=(-9, -1.5), corner2=(-4, 1)).label('Cascode with gate of the upper device\nfed from the lower node (current-shunt)', loc='center')
elm.Rect(corner1=(-2, -1.5), corner2=(3, 1)).label('Sense resistor in series with\nthe output (current-shunt)', loc='center')
elm.Rect(corner1=(5, -1.5), corner2=(10, 1)).label('Diode-connected or drain-to-gate\n(voltage-shunt, low in and out)', loc='center')
elm.Annotate().at((0.5, 5.2)).delta(0, 0.6).label('identify the sensing element first, then the mixing point')
```
