# Op-Amp Basics — Circuit Diagrams

Companion schematics for `Concepts.md` and `Formulas.md`. Every diagram uses plain
`schemdraw` elements with explicit lengths, so the rendered geometry matches the
coordinates in the code and the signal flow can be followed without running anything.

Reading rule used throughout: **the upper op-amp input is `in1` (non-inverting, `+`) and
the lower input is `in2` (inverting, `-`)**.

## 1. Anatomy of an Ideal Op-Amp

The op-amp is a three-terminal differential block. The ideal model has infinite open-loop
gain, zero output impedance and no input current; the supply pins only set the output
voltage range in a real device.

```circuit
op = elm.Opamp(leads=True).right().at((0, 0)).label('U1', loc='center')
elm.Line().at((0, 0.625)).left(3).label('V+  non-inverting input', loc='left')
elm.Line().at((0, -0.625)).left(3).label('V-  inverting input', loc='left')
elm.Line().at((3.4151, 0)).right(2.5).label('Vout', loc='top')
elm.Line().at((1.3467, 0.84)).up(1.75).label('+V supply', loc='left')
elm.Line().at((1.3467, -0.84)).down(1.75).label('-V supply', loc='left')
elm.Annotate().at((5.9, 0.9)).delta(0, 0.9).label('Vout = A * (V+ - V-)\nA is huge, output saturates at the rails')
elm.Annotate().at((-3.0, 0.625)).delta(-1.4, 1.1).label('I+ = I- = 0\nno input current drawn')
```

- `V+` and `V-` are the only signal terminals; the supplies are not signal inputs.
- Output current is unlimited in the ideal model, so any load can be driven.

## 2. Virtual Short and Virtual Ground

Negative feedback forces `V+ = V-`. If `V+` is tied to ground, the `V-` node is at zero
volts but cannot sink current, which is what makes it a *virtual* ground.

```circuit
op = elm.Opamp(leads=True).right().at((0, 0))
src = elm.SourceSin().right().length(2).at((-6.5, -0.625)).label('Vin', loc='left')
elm.Ground().down().at((-6.5, -0.625))
rin = elm.Resistor().right().length(2).at((-4.5, -0.625)).label('Rin', loc='top')
elm.Line().at((-2.5, -0.625)).right(2.5)
elm.Dot().at((0, -0.625)).label('V- = 0 V\nvirtual ground', loc='bottom')
elm.Line().at((0, 0.625)).left(2)
elm.Ground().down().at((-2, 0.625))
rf = elm.Resistor().up().length(2).at((0, -0.625)).label('Rf', loc='left')
elm.Line().at((0, 1.375)).up(0.875)
elm.Line().at((0, 2.25)).right(3.4151)
elm.Line().at((3.4151, 2.25)).down(2.25)
elm.Line().at((3.4151, 0)).right(2).label('Vout', loc='top')
elm.Annotate().at((5.4, 1.6)).delta(1.2, 0.7).label('All of the input current\nmust flow through Rf:\nVout = -(Rf/Rin) * Vin')
```

- The virtual short holds **only while the feedback path is intact**.
- The virtual ground has `V- = 0` but `I- = 0`; it is not a current sink.

## 3. The Negative Feedback Loop, Abstract View

Feedback is what converts an open-loop amplifier with an unpredictable gain into a
circuit with an accurate, resistor-defined gain. `beta` samples the output.

```circuit
elm.Rect(corner1=(-2, -1), corner2=(2, 1)).label('Forward\namplifier\nA', loc='center')
elm.Line(arrow='->').at((2, 0)).right(2).label('Vo = A(Vi - beta*Vo)', loc='top')
elm.Rect(corner1=(4, -1), corner2=(8, 1)).label('Feedback\nnetwork\nbeta', loc='center')
elm.Line(arrow='<-').at((4, 0)).left(2)
elm.Rect(corner1=(-2, -5.5), corner2=(8, -3.5)).label('Error amplifier compares Vi with beta*Vo', loc='center')
elm.Line(arrow='->').at((-2, -4.5)).left(1.5).label('Vi', loc='left')
elm.Line(arrow='<-').at((8, -4.5)).right(1.5).label('beta*Vo', loc='right')
elm.Line().at((-3.5, -4.5)).up(4.5).to((-3.5, 0))
elm.Line(arrow='->').at((-3.5, 0)).right(1.5).label('error', loc='top')
elm.Annotate().at((0, 1.4)).delta(0, 0.9).label('A_cl = A / (1 + A*beta)  ->  1/beta   when   A*beta >> 1')
elm.Annotate().at((3, -7)).delta(0, -0.8).label('Open the loop and the gain is whatever the datasheet happens to say')
```

- The closed-loop gain is set by `beta`, i.e. by passive components, not by `A`.
- The same loop is what makes distortion, linearity and bandwidth predictable.

## 4. Non-Inverting Amplifier

`Vin` drives the non-inverting input and the `Rf`/`Rg` divider sets the gain. The
inverting input now sits at a *fraction* of the output rather than at zero volts.

```circuit
op = elm.Opamp(leads=True).right().at((0, 0))
src = elm.SourceSin().right().length(2).at((-6.5, 0.625)).label('Vin', loc='left')
elm.Line().at((-4.5, 0.625)).right(4.5)
elm.Dot().at((0, 0.625)).label('V+', loc='top')
elm.Line().at((0, -0.625)).left(2.5)
elm.Dot().at((-2.5, -0.625)).label('V- = Rg/(Rf+Rg) * Vout', loc='left')
rf = elm.Resistor().up().length(3).at((3.4151, 0)).label('Rf', loc='right')
elm.Line().at((3.4151, 3)).right(2).to((5.4151, 3)).label('Vout', loc='top')
elm.Dot().at((3.4151, 3)).label('Vout node', loc='bottom')
rg = elm.Resistor().down().length(3).at((4.4151, 3)).label('Rg', loc='right')
elm.Line().at((4.4151, 0)).down(1.875)
elm.Line().at((4.4151, -1.875)).left(6.915).to((-2.5, -1.875))
elm.Line().at((-2.5, -1.875)).up(1.25).to((-2.5, -0.625))
elm.Resistor().down().length(1.25).at((-2.5, -1.875)).label('Rg1', loc='left')
elm.Ground().down().at((-2.5, -3.125))
```

- `Vout = (1 + Rf/Rg) * Vin`, so gain can never be below unity and `Zin` stays very high.
- The divider current is small: `Rf + Rg` should be large enough to limit loading.

## 5. Voltage Follower (Unity Buffer)

Output tied straight back to the inverting input. Voltage gain is exactly one, but the
stage still gives current gain and impedance buffering.

```circuit
op = elm.Opamp(leads=True).right().at((0, 0))
src = elm.SourceSin().right().length(2).at((-6.5, 0.625)).label('Vin', loc='left')
elm.Line().at((-4.5, 0.625)).right(4.5)
elm.Dot().at((0, 0.625)).label('V+', loc='top')
elm.Line().at((0, -0.625)).left(1)
elm.Line().at((-1, -0.625)).down(2)
elm.Line().at((-1, -2.625)).right(6.9151).to((5.9151, -2.625))
elm.Line().at((5.9151, -2.625)).up(2.625).to((5.9151, 0))
elm.Dot().at((5.9151, 0)).label('output node', loc='top')
elm.Line().at((5.9151, 0)).right(1.5).to((7.4151, 0))
elm.Resistor().down().length(1.5).at((7.4151, 0)).label('load', loc='right')
elm.Ground().down().at((7.4151, -1.5))
elm.Annotate().at((-5.5, 1.6)).delta(0, 0.8).label('high input impedance:\nthe source sees almost no load')
elm.Annotate().at((1, 1.6)).delta(0, 0.8).label('gain = 1, but the low output\nimpedance drives the load')
```

- `A = 1`, no inversion, zero phase shift at DC.
- Ideal uses: impedance bridging between a high-impedance source and a low-impedance load.

## 6. Input Bias-Current Compensation

The two input bias currents are nominally equal, but unequal source impedances turn them
into a differential error. `Rb = Rf || Rsource` balances the two ends of the feedback
network.

```circuit
op = elm.Opamp(leads=True).right().at((0, 0))
src = elm.SourceV().right().length(2).at((-6.5, -0.625)).label('Vin', loc='left')
elm.Ground().down().at((-6.5, -0.625))
rb = elm.Resistor().right().length(2).at((-4.5, -0.625)).label('Rb = Rf || Rout', loc='top')
elm.Line().at((-2.5, -0.625)).right(2.5)
elm.Dot().at((0, -0.625))
rf = elm.Resistor().up().length(2).at((0, -0.625)).label('Rf', loc='left')
elm.Line().at((0, 1.375)).up(0.875)
elm.Line().at((0, 2.25)).right(3.4151)
elm.Line().at((3.4151, 2.25)).down(2.25)
elm.Line().at((3.4151, 0)).right(2).label('Vout', loc='top')
elm.Line().at((0, 0.625)).left(1.5)
elm.Ground().down().at((-1.5, 0.625))
elm.Line().at((-1.5, -1.75)).right(1.5).to((0, -1.75))
elm.Annotate().at((-4.5, -1.4)).delta(0, -0.8).label('Ib+ drops across Rb')
elm.Annotate().at((2.2, -1.2)).delta(1.2, -0.8).label('Ib- drops across the\nsame Rb seen from the\ninverting side')
elm.Annotate().at((4.6, 1.4)).delta(1.0, 0.7).label('Worst case without Rb:\noutput error = Ib * Rf')
```

- Compensated, the two bias-current drops are equal and cancel in the differential input.
- `Rb` must also be added to the noise-gain calculation, which it does automatically.

## 7. Offset Voltage, Slew Rate and Full-Power Bandwidth

Real op-amps have an input offset voltage and a finite maximum output slope. The offset
behaves like a small source in series with the differential input pair.

```circuit
op = elm.Opamp(leads=True).right().at((0, 0))
src = elm.SourceSin().right().length(2).at((-8, 0.625)).label('signal', loc='left')
elm.Line().at((-6, 0.625)).right(1.5)
vos = elm.SourceV().right().length(1.5).at((-4.5, 0.625)).label('Vos', loc='top')
elm.Line().at((-3, 0.625)).right(3)
elm.Line().at((0, 0.625)).left(1.25)
elm.Ground().down().at((-1.25, 0.625))
rf = elm.Resistor().up().length(2).at((0, -0.625)).label('Rf', loc='left')
rin = elm.Resistor().up().length(2).at((0, -0.625)).label('Rin', loc='right')
elm.Line().at((0, 1.375)).up(0.875)
elm.Line().at((0, 2.25)).right(3.4151)
elm.Line().at((3.4151, 2.25)).down(2.25)
elm.Line().at((3.4151, 0)).right(2).label('Vout', loc='top')
elm.Line().at((0, -2.625)).left(8).to((-8, -2.625))
elm.Line().at((-8, -2.625)).up(1.875)
elm.Line().at((1.3467, 0.84)).up(1.75).label('+V', loc='left')
elm.Line().at((1.3467, -0.84)).down(1.75).label('-V', loc='left')
elm.Annotate().at((5.4, 1.6)).delta(1.4, 0.7).label('Vout offset = Vos * (1 + Rf/Rin)\nSR = max dVout/dt\nFPB = SR / (2*pi*Vp)')
```

- Offset error and bias error are multiplied by the **noise gain** of the topology.
- At high frequency, `SR` (not the small-signal bandwidth) is usually the limit.

## 8. Common-Mode Rejection

A differential input pair amplifies the difference between the inputs and rejects what
they share. `Vcm` is the shared part, `Vd` the wanted part.

```circuit
op = elm.Opamp(leads=True).right().at((0, 0))
vcm = elm.SourceV().up().length(2).at((-6, -0.625)).label('Vcm', loc='left')
elm.Ground().down().at((-6, -0.625))
vd = elm.SourceV().up().length(2).at((-6, 0.625)).label('Vd', loc='left')
elm.Ground().down().at((-6, 0.625))
elm.Line().at((-6, 1.375)).right(6)
elm.Dot().at((0, 0.625)).label('V+ = Vcm + Vd/2', loc='top')
elm.Line().at((0, -0.625)).left(1.5)
elm.Ground().down().at((-1.5, -0.625))
rf = elm.Resistor().up().length(2).at((0, -0.625)).label('Rf', loc='left')
elm.Line().at((0, 1.375)).up(0.875)
elm.Line().at((0, 2.25)).right(3.4151)
elm.Line().at((3.4151, 2.25)).down(2.25)
elm.Line().at((3.4151, 0)).right(2).label('Vout = Ad * Vd', loc='top')
elm.Line().at((1.3467, 0.84)).up(1.75).label('+V', loc='left')
elm.Line().at((1.3467, -0.84)).down(1.75).label('-V', loc='left')
elm.Annotate().at((4.6, -1.4)).delta(1.4, -0.8).label('CMRR = 20*log10(Ad / Acm)\nICMR is a hard rail limit')
```

- An ideal op-amp has `Ad` enormous and `Acm = 0`.
- CMRR collapses with frequency because input mismatch is largely capacitive.

## 9. Gain-Bandwidth Trade-Off

For a single dominant pole, `A * f = GBW`. Ten times the closed-loop gain costs ten times
the bandwidth.

```circuit
for idx, (name, fbw) in enumerate([('A = 1', 'f = GBW'), ('A = 10', 'f = GBW/10'), ('A = 100', 'f = GBW/100')]):
    y = 4 - 4 * idx
    op = elm.Opamp(leads=True).right().at((0, y))
    src = elm.SourceSin().right().length(2).at((-5.5, y + 0.625))
    elm.Line().at((-3.5, y + 0.625)).right(3.5)
    elm.Line().at((0, y - 0.625)).left(1)
    elm.Ground().down().at((-1, y - 0.625))
    if idx == 0:
        elm.Line().at((0, y - 0.625)).down(1.5)
        elm.Line().at((0, y - 2.125)).right(3.4151)
        elm.Line().at((3.4151, y - 2.125)).up(2.125)
    else:
        rf = elm.Resistor().left().length(2).at((3.4151, y)).label('Rf', loc='top')
        rg = elm.Resistor().left().length(2).at((1.415, y)).label('Rg', loc='top')
        elm.Line().at((3.4151, y)).left(2)
        elm.Line().at((-0.585, y)).left(0.915).to((-1.5, y))
        elm.Ground().down().at((-1.5, y))
        elm.Line().at((-1.5, y)).up(1.375)
        elm.Line().at((-1.5, y + 1.375)).right(4.9151)
        elm.Line().at((3.4151, y + 1.375)).down(1.375)
    elm.Line().at((3.4151, y)).right(1.5).label(name + '   ' + fbw, loc='top')
elm.Annotate().at((-2.2, -4.2)).delta(0, -0.9).label('GBW is a constant of the device, so gain and bandwidth\ntrade one for one: only one of them can be large')
```

- Closed-loop pole: `f_cl = GBW / A_cl` for the non-inverting configuration.
- Stability is judged on the **noise gain**, so inverting stages can be the surprise.

## 10. Single-Supply Rail-to-Rail Design

With a `0 V` and `+5 V` supply, the signal and output can only swing between the rails, so
the bias point must sit at mid-supply for a symmetric excursion.

```circuit
op = elm.Opamp(leads=True).right().at((0, 0))
src = elm.SourceSin().right().length(1.5).at((-7.5, -0.625)).label('Vin ac', loc='left')
elm.Ground().down().at((-7.5, -0.625))
cin = elm.Capacitor().right().length(1.5).at((-6, -0.625)).label('Cin', loc='top')
rb1 = elm.Resistor().up().length(1.5).at((-4.5, -0.625)).label('Rb1', loc='left')
rb2 = elm.Resistor().down().length(1.5).at((-4.5, -0.625)).label('Rb2', loc='left')
elm.Line().at((-4.5, 0.875)).up(0.875)
elm.Vdd().at((-4.5, 1.75)).label('+5 V')
elm.Line().at((-4.5, -2.125)).down(0.875)
elm.Vss().at((-4.5, -3)).label('0 V')
elm.Dot().at((-4.5, -0.625)).label('Vref = Vcc/2', loc='right')
elm.Line().at((-4.5, -0.625)).right(4.5)
elm.Dot().at((0, -0.625)).label('V-', loc='bottom')
rf = elm.Resistor().up().length(2).at((0, -0.625)).label('Rf', loc='left')
elm.Line().at((0, 1.375)).up(0.875)
elm.Line().at((0, 2.25)).right(3.4151)
elm.Line().at((3.4151, 2.25)).down(2.25)
elm.Line().at((3.4151, 0)).right(2).label('Vout  0 to 5 V', loc='top')
elm.Line().at((1.3467, 0.84)).up(2.035)
elm.Vdd().at((1.3467, 2.875)).label('+5 V')
elm.Line().at((1.3467, -0.84)).down(1.16)
elm.Vss().at((1.3467, -2)).label('0 V')
elm.Annotate().at((4.6, -1.6)).delta(1.4, -0.8).label('The output cannot reach the rails:\nallow 1 to 2 V of headroom')
```

- `Rb1 = Rb2` gives a reference at `Vcc/2`, the centre of the usable output swing.
- `Cin` blocks the DC level so the op-amp does not fight the bias divider.

## 11. Chopper-Stabilized Amplifier (Block View)

Chopper modulation moves the offset and the 1/f noise above the signal band, where the
synchronous demodulator and the low-pass filter average it away. The wanted signal passes
unmodulated and is left untouched.

```circuit
elm.Rect(corner1=(-9, -1), corner2=(-6, 1)).label('Chopper\nmodulator\nf_chop', loc='center')
elm.Line(arrow='->').at((-6, 0)).right(1.5)
elm.Rect(corner1=(-4.5, -1), corner2=(-1, 1)).label('Instrumentation\namplifier', loc='center')
elm.Line(arrow='->').at((-1, 0)).right(1.5)
elm.Rect(corner1=(0.5, -1), corner2=(3.5, 1)).label('Synchronous\ndemodulator', loc='center')
elm.Line(arrow='->').at((3.5, 0)).right(1.5)
elm.Rect(corner1=(5, -1), corner2=(8, 1)).label('Low-pass\nfilter', loc='center')
elm.Line(arrow='->').at((8, 0)).right(1.5).label('Vout', loc='top')
elm.Rect(corner1=(-2, -4.75), corner2=(2, -2.75)).label('clock  f_chop >> signal band', loc='center')
elm.Line(arrow='->').at((-2, -3.75)).left(3.5)
elm.Line(arrow='<-').at((2, -3.75)).right(6.5)
elm.Line(arrow='->').at((5.5, -2.75)).up(1.75)
elm.Line().at((-9, -1.6)).down(4.15).to((-9, -5.75))
elm.Line().at((-9, -5.75)).right(17)
elm.Line(arrow='->').at((8, -5.75)).up(4.75)
elm.Annotate().at((-7.5, 1.4)).delta(0, 0.8).label('offset and 1/f noise are now\nmodulated to f_chop, then rejected')
elm.Annotate().at((0, 1.4)).delta(0, 0.8).label('residual: small ripple at f_chop')
```

- Result: very low offset drift with no periodic trimming capacitors.
- Cost: clock ripple at `f_chop` and a more demanding application circuit.

## 12. Which Op-Amp Parameter Dominates Which Requirement

Datasheet parameters are not independent, and the binding constraint changes with the
job. This map shows the trade the designer is actually making.

```circuit
elm.Rect(corner1=(-10, -2.5), corner2=(-6, 2.5)).label('Precision\nVos, Ib, drift\nhigh CMRR/PSRR', loc='center')
elm.Line(arrow='->').at((-6, 0)).right(2)
elm.Rect(corner1=(-4, -2.5), corner2=(0, 2.5)).label('High speed\nGBW, SR\nsettling time', loc='center')
elm.Line(arrow='->').at((0, 0)).right(2)
elm.Rect(corner1=(2, -2.5), corner2=(6, 2.5)).label('Low power\nquiescent current\nlow SR', loc='center')
elm.Line(arrow='->').at((6, 0)).right(2)
elm.Rect(corner1=(8, -2.5), corner2=(12, 2.5)).label('Rail-to-rail I/O\nworks at 0 V and\nat the top rail', loc='center')
elm.Rect(corner1=(-3, 4.5), corner2=(3, 7.5)).label('Always required too:\nnoise density, output drive,\nsupply rejection', loc='center')
elm.Line(arrow='<-').at((-3, 4.5)).down(2)
elm.Line(arrow='<-').at((3, 4.5)).down(2)
elm.Annotate().at((0, -3.6)).delta(0, -0.8).label('High GBW normally costs more quiescent current and more noise density')
```

## 13. Datasheet Checklist

- Is the input common-mode range inside the real supply, including at full output swing?
- Can the output reach the level the next stage needs, at the *minimum* supply?
- Is the loop stable for the **noise gain** of this topology, not just its signal gain?
- Are the resistor values small enough for bias-current error but large enough for bias?
- What does the noise gain do at high frequency, where stray capacitance raises it?
