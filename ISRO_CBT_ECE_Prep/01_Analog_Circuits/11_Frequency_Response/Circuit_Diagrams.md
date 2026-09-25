# Frequency Response of Amplifiers — Circuit Diagrams

Companion schematics for `Concepts.md`. Every capacitor in an amplifier is either a deliberate
high-pass corner or a parasitic low-pass corner, so the full response is just the sum of
their slopes on a log axis.

## 1. What the Magnitude Response Looks Like

A practical amplifier has a midband plateau, a low-frequency roll-off and a high-frequency
roll-off; the useful range sits between the two corners.

```circuit
elm.Line().at((0, 2)).to((3, 2))
elm.Line().at((3, 2)).to((5, 1.4))
elm.Line().at((5, 1.4)).to((7, 0.6))
elm.Line().at((7, 0.6)).to((9, 0))
elm.Line().at((9, 0)).to((11, -0.6))
elm.Line().at((11, -0.6)).to((13, -1.4))
elm.Line().at((13, -1.4)).to((15, -2.2))
elm.Line().at((0, 0)).up(3)
elm.Line().at((0, 0)).right(15.5)
elm.Dot().at((3, 2)).label('fL, 0.707*midband', loc='top')
elm.Dot().at((9, 0)).label('midband', loc='top')
elm.Dot().at((13, -1.4)).label('fH, 0.707*midband', loc='bottom')
elm.Annotate().at((1.5, 2.8)).delta(0, 0.6).label('40 dB midband')
elm.Annotate().at((1.5, 1.1)).delta(0, 0.6).label('-20 dB/dec')
elm.Annotate().at((14, 0.2)).delta(0, 0.6).label('-40 dB/dec:\none pole at each end')
elm.Annotate().at((7.5, -3.4)).delta(0, -0.6).label('bandwidth = fH - fL, and fL is usually so much smaller that BW ~ fH;\nwideband means fH far above the signal, not a flat response everywhere')
```

- The plateau is set by the resistors, the roll-off by the capacitors, so the two can be
  designed almost independently.
- For audio, `fL` of a few hertz and `fH` above 20 kHz leave four decades of usable
  response.

## 2. Coupling and Bypass Capacitors: The Low-Frequency Corners

Each capacitor forms a high-pass with the resistance it sees, and every one of them adds
`−20 dB/dec` below its own corner.

```circuit
elm.Rect(corner1=(-10, 2.5), corner2=(-5, 5.5)).label('input coupling Cin\nsees Rsig + Rin(base)\nfL1 = 1/(2*pi*Cin*(Rsig+Rin))', loc='center')
elm.Line(arrow='->').at((-5, 4)).right(1.5)
elm.Rect(corner1=(-3.5, 2.5), corner2=(1.5, 5.5)).label('emitter bypass CE\nsees RE (or RE || re)\nfL2 = 1/(2*pi*CE*RE)', loc='center')
elm.Line(arrow='->').at((1.5, 4)).right(1.5)
elm.Rect(corner1=(3, 2.5), corner2=(8, 5.5)).label('output coupling Cout\nsees RC || RL\nfL3 = 1/(2*pi*Cout*(RC||RL))', loc='center')
elm.Line().at((-10, 1.5)).right(18).to((8, 1.5))
elm.Rect(corner1=(-10, -1.5), corner2=(-5, 1.5)).label('below every corner:\ngain falls at\n-20 dB/dec per pole', loc='center')
elm.Line(arrow='->').at((-5, 0)).right(1.5)
elm.Rect(corner1=(-3.5, -1.5), corner2=(1.5, 1.5)).label('near the lowest\ncorner the response is\n-3 dB: that is fL', loc='center')
elm.Line(arrow='->').at((1.5, 0)).right(1.5)
elm.Rect(corner1=(3, -1.5), corner2=(8, 1.5)).label('above the highest\ncorner the gain is\nflat again', loc='center')
elm.Annotate().at((-1, -2.6)).delta(0, -0.6).label('the coupling capacitors exist to keep the DC bias out of the source and the load;\ntheir cost is fL, so the fix is simply a larger capacitor')
elm.Annotate().at((-1, 6.2)).delta(0, 0.6).label('the bypass capacitor trades midband gain for a corner: with CE open the gain is gm*RC*RE/(RC+RE),\nwith CE shorted it is gm*RC, and the transition happens near fL2')
```

- Shortening the source resistance raises the input corner, so a low `Rsig` hurts the low
  frequency even when the bias is generous.
- The bypass capacitor is the one corner that is *desirable*: it moves the transition to a
  frequency where it does not matter.

## 3. Parasitic Capacitance and the Miller Effect

The collector-base capacitance is multiplied by the stage gain, which is the dominant
high-frequency pole in a common-emitter stage.

```circuit
elm.Rect(corner1=(-9, 2.5), corner2=(-4, 5.5)).label('physical device:\nCbc (a few pF) bridges\nbase and collector\ninside the transistor', loc='center')
elm.Line(arrow='->').at((-4, 4)).right(1.5)
elm.Rect(corner1=(-2.5, 2.5), corner2=(2.5, 5.5)).label('the collector voltage swings\nopposite to the input, so the\ncapacitance sees a voltage\nmultiplied by (1 + Av)', loc='center')
elm.Line(arrow='->').at((2.5, 4)).right(1.5)
elm.Rect(corner1=(4, 2.5), corner2=(9, 5.5)).label('input Miller capacitance:\nCm,in = Cbc*(1 + |Av|)', loc='center')
elm.Line().at((-4, 1)).right(1.5)
elm.Rect(corner1=(-2.5, -1.5), corner2=(2.5, 1.5)).label('and the output sees the\ncomplement: Cm,out = Cbc*(1 + 1/|Av|),\nusually small', loc='center')
elm.Line(arrow='->').at((2.5, 0)).right(1.5)
elm.Rect(corner1=(4, -1.5), corner2=(9, 1.5)).label('fH ~ 1/(2*pi*Req*Cm,in)\nReq is the resistance seen\nby the base node', loc='center')
elm.Line().at((0, 0.9)).up(1.6)
elm.Line().at((0, 0.9)).right(8).to((8, 0.9))
elm.Rect(corner1=(-2.5, 3.5), corner2=(2.5, 6.5)).label('example: Av = 50 with Cbc = 4 pF\nlooks like 204 pF at the input,\nwhich is two orders more than\nany external compensation cap', loc='center')
elm.Annotate().at((0, -2.6)).delta(0, -0.6).label('a common-emitter gain of 100 with a few pF of Cbc gives a bandwidth in the low MHz,\nwhile a common-base stage has no voltage gain to multiply the capacitance:\nits Cbc carries almost no signal current')
```

- Miller multiplication is why a common-emitter stage has a much lower bandwidth than the
  same transistor used in common base or in a cascode.
- The cascode fixes it by holding the lower collector at a constant voltage, so `Cbc` sees
  almost no signal.

## 4. Gain-Bandwidth Product

For a one-pole amplifier, gain and bandwidth trade against each other exactly; boosting the
closed-loop gain narrows the useful band.

```circuit
elm.Line().at((0, 0)).to((12, 0)).to((15, -1))
elm.Line().at((0, 0.5)).to((9, 0.5)).to((12, 0))
elm.Line().at((0, 1)).to((6, 1)).to((12, 0))
elm.Line().at((0, 1.5)).to((3, 1.5)).to((12, 0))
elm.Line().at((0, -1)).up(3.5)
elm.Line().at((0, 0)).right(15.5)
elm.Annotate().at((1.2, 0.05)).delta(0, -0.6).label('gain 1 (follower)')
elm.Annotate().at((7.5, 0.55)).delta(0, 0.6).label('gain 10')
elm.Annotate().at((4.5, 1.05)).delta(0, 0.6).label('gain 100')
elm.Annotate().at((1.5, 1.55)).delta(0, 0.6).label('gain 1000')
elm.Line().at((12, 0)).up(2)
elm.Dot().at((12, 0)).label('GBW', loc='right')
elm.Annotate().at((0, 2.6)).delta(0, 0.6).label('vertical: gain in units of 20 dB;  horizontal: 3 units per decade of frequency')
elm.Annotate().at((0, -2.2)).delta(0, -0.6).label('all four lines cross 0 dB at the same frequency: that is why a 100x closed-loop amplifier\nwith a 1 MHz bandwidth and a 10x amplifier with a 10 MHz bandwidth are the same op-amp')
elm.Annotate().at((14, 1.4)).delta(0, 0.6).label('beyond GBW\nall curves follow\nthe open-loop roll-off')
```

- `GBW = gain * bandwidth` is why "the gain is 100" and "the bandwidth is 1 MHz" describe the
  same op-amp as "the gain is 10 and the bandwidth is 10 MHz".
- Real op-amps deviate above the unity-gain frequency because of the second pole, so the
  closed-loop bandwidth at high noise gains stops following the ideal line.

## 5. Op-Amp Frequency Response

The open-loop gain is a one-pole response; closing the loop divides it by the noise gain, so
the closed-loop pole moves but the product stays fixed.

```circuit
elm.Rect(corner1=(-9, 2.5), corner2=(-4, 5.5)).label('open-loop model:\nA(s) = GBW/s, a single pole\nnear 10 Hz for a 1 MHz part', loc='center')
elm.Line(arrow='->').at((-4, 4)).right(1.5)
elm.Rect(corner1=(-2.5, 2.5), corner2=(2.5, 5.5)).label('noise gain:\n1/beta evaluated at DC,\nincluding the resistors the feedback network actually presents', loc='center')
elm.Line(arrow='->').at((2.5, 4)).right(1.5)
elm.Rect(corner1=(4, 2.5), corner2=(9, 5.5)).label('closed-loop pole:\nfH = GBW / noise gain', loc='center')
elm.Rect(corner1=(-9, -1.5), corner2=(-4, 1.5)).label('phase margin check:\nlag = 45 deg at the crossing;\nneed about 60 deg for a comfortable step response', loc='center')
elm.Line(arrow='->').at((-4, 0)).right(1.5)
elm.Rect(corner1=(-2.5, -1.5), corner2=(2.5, 1.5)).label('the second pole is what makes the gain margin fall\nas the closed-loop gain rises, so stability must be checked\nat the highest gain the application selects', loc='center')
elm.Line(arrow='->').at((2.5, 0)).right(1.5)
elm.Rect(corner1=(4, -1.5), corner2=(9, 1.5)).label('add a dominant pole or a zero in the feedback network\nto buy phase margin when a capacitive load is present', loc='center')
elm.Annotate().at((0, -2.6)).delta(0, -0.6).label('slew rate, not bandwidth, limits large-signal behaviour: SR = 2*pi*Vpeak*fH for a full-power sine,\nand a 1 V step across a 1 MHz pole gives SR = 2*pi*1e6 rad/s')
```

- The noise gain is not the signal gain: an inverting stage with `Rf = Rg` has a signal gain
  of `-1` but a noise gain of `2`, so its bandwidth is `GBW/2`.
- Any capacitance in the feedback node or on the output adds poles that the datasheet
  specification may not cover.

## 6. Bode Plot Construction

Straight-line asymptotes and the phase approximation are enough for almost every exam and
design question.

```circuit
elm.Line().at((0, 0)).to((12, 0))
elm.Line().at((6, 0)).down(0.5).to((6, -0.5))
elm.Line().at((6, -0.5)).to((15, -2.5))
elm.Line().at((0, 0)).up(2.5)
elm.Line().at((0, 0)).right(15.5)
elm.Line().at((0, 2)).right(3).to((3, 2))
elm.Line().at((3, 2)).down(1).to((3, 1))
elm.Line().at((0, 1)).right(9).to((9, 1))
elm.Line().at((9, 1)).down(1.5).to((9, -0.5))
elm.Line().at((0, -0.5)).right(6).to((6, -0.5))
elm.Line().at((6, -0.5)).up(0.5).to((6, 0))
elm.Line().at((0, 1)).down(0.5).to((0, 0.5))
elm.Line().at((0, 0.5)).right(6).to((6, 0.5))
elm.Dot().at((6, 0.5)).label('break frequency', loc='bottom')
elm.Annotate().at((1.2, 1.05)).delta(0, 0.6).label('magnitude: start flat, subtract 20 dB for\nevery pole, add 20 dB for every zero')
elm.Annotate().at((0, 2.8)).delta(0, 0.6).label('phase: -45 deg per pole at the corner, -90 deg far away, +90 deg far from a zero')
elm.Annotate().at((1, -1.4)).delta(0, -0.6).label('a zero at 6 Hz cancels the pole there: the response is flat again above 6 Hz,\nwhich is the trick used to create a lead-compensated amplifier')
elm.Annotate().at((12, -3.4)).delta(0, -0.6).label('the exact curve is within about 3 dB of the asymptotes at each corner:\n0.707*midband at fL and fH')
```

- A pole lowers phase by 90 degrees and a zero raises it, which is how a feedback loop is
  checked for stability before it is built.
- When two poles sit within a decade of each other, the exact response sags more than 3 dB;
  place the dominant pole three decades below the next one.

## 7. Cascading Equal Stages

Cascading is not free: the overall bandwidth shrinks by a factor that is easy to quote for
equal stages.

```circuit
elm.Rect(corner1=(-10, 2.5), corner2=(-5, 5.5)).label('stage 1\nA1/(1 + s/w1)\nf1 = 1 MHz', loc='center')
elm.Line(arrow='->').at((-5, 4)).right(2)
elm.Rect(corner1=(-3, 2.5), corner2=(2, 5.5)).label('stage 2\nA2/(1 + s/w2)\nf2 = 1 MHz', loc='center')
elm.Line(arrow='->').at((2, 4)).right(2)
elm.Rect(corner1=(4, 2.5), corner2=(9, 5.5)).label('total gain is A1*A2\nbut the -3 dB point is\nlower than either stage', loc='center')
elm.Rect(corner1=(-10, -1.5), corner2=(-5, 1.5)).label('one pole: BW = f1', loc='center')
elm.Line(arrow='->').at((-5, 0)).right(2)
elm.Rect(corner1=(-3, -1.5), corner2=(2, 1.5)).label('two equal stages:\nf_total = 0.64*f1', loc='center')
elm.Line(arrow='->').at((2, 0)).right(2)
elm.Rect(corner1=(4, -1.5), corner2=(9, 1.5)).label('n equal stages:\nf = f1*sqrt(2^(1/n) - 1),\nwhich tends to f1 as n grows', loc='center')
elm.Annotate().at((0, -2.6)).delta(0, -0.6).label('alternatively push the gain into one stage and keep the rest as buffers:\nwideband amplifiers use a gain stage plus emitter followers, not a chain of gain stages')
elm.Annotate().at((0, 6.2)).delta(0, 0.6).label('the poles add in the product of the transfer functions, so slopes and phases add too')
```

- For two equal stages the 3 dB point is `0.64` of the single-stage value, and the asymptote
  at the meeting point is already `-6 dB`.
- Dominant-pole design keeps one pole three or more decades below the next so that the
  others contribute only phase, not a change in the dominant corner.

## 8. Bandwidth Improvement Techniques

Every technique either removes the Miller multiplication or spends gain to buy bandwidth.

```circuit
elm.Rect(corner1=(-10, 2.5), corner2=(-5, 5.5)).label('cascode: hold the lower\ncollector at constant voltage\nso Cbc sees no signal', loc='center')
elm.Line(arrow='->').at((-5, 4)).right(2)
elm.Rect(corner1=(-3, 2.5), corner2=(2, 5.5)).label('common base or cascode\non the input device:\nno Miller term, very fast', loc='center')
elm.Line(arrow='->').at((2, 4)).right(2)
elm.Rect(corner1=(4, 2.5), corner2=(9, 5.5)).label('neutralisation: feed a little\nof the output back to cancel\nthe Cbc current', loc='center')
elm.Rect(corner1=(-10, -1.5), corner2=(-5, 1.5)).label('choose a high-fT device:\nfT is the frequency where\nbeta falls to one', loc='center')
elm.Line(arrow='->').at((-5, 0)).right(2)
elm.Rect(corner1=(-3, -1.5), corner2=(2, 1.5)).label('trade gain for bandwidth:\nhalve the closed-loop gain,\ndouble the bandwidth', loc='center')
elm.Line(arrow='->').at((2, 0)).right(2)
elm.Rect(corner1=(4, -1.5), corner2=(9, 1.5)).label('accept the limit: a stage that is\ntoo slow can simply be replaced\nby a wider device', loc='center')
elm.Annotate().at((0, 6.2)).delta(0, 0.6).label('fT >> fH is required: a transistor with fT = 500 MHz can build an amplifier to only about 50 MHz')
elm.Annotate().at((0, -2.6)).delta(0, -0.6).label('bandwidth is set by the fastest parasitic path, so layout matters as much as\nthe schematic: short collector traces and a small collector island are worth\na great deal of bandwidth')
```

- The cascode and the common-base stage both defeat Miller multiplication, which is the
  single most effective change to a high-frequency design.
- A unity-gain buffer of a fast device often replaces several gain stages in wideband
  amplifiers.

## 9. Cutoff, Bandwidth, Rise Time and Settling Time

The same pole appears as a bandwidth, a rise time and a settling time, so one number answers
all three questions.

```circuit
elm.Line().at((0, 0)).to((3, 0)).to((6, -1))
elm.Line().at((0, -1)).up(1.5)
elm.Line().at((0, 0)).right(6.5)
elm.Dot().at((3, 0)).label('0.707', loc='top')
elm.Dot().at((0, 0)).label('1.0', loc='left')
elm.Line().at((0.6, 0)).up(0.423)
elm.Line().at((0.6, 0.423)).right(0.6).to((1.2, 0.423))
elm.Line().at((1.2, 0.423)).down(0.423)
elm.Line().at((1.2, 0)).up(0.214)
elm.Line().at((1.2, 0.214)).right(0.6).to((1.8, 0.214))
elm.Line().at((1.8, 0.214)).down(0.214)
elm.Line().at((1.8, 0)).up(0.107)
elm.Annotate().at((3.6, 0.25)).delta(0, 0.6).label('a first-order step reaches 63.2% of the final value\nat one time constant and 95% at about three')
elm.Annotate().at((-0.4, 0.55)).delta(0, 0.6).label('10 to 90% rise time\ntr = 0.35/fH')
elm.Annotate().at((-0.4, -0.55)).delta(0, -0.6).label('within 1% of final value:\nts ~ 4.6/fH, and with phase\nmargin the real number is larger')
elm.Annotate().at((3.6, -1.2)).delta(0, -0.6).label('in seconds, with fH in hertz: 1 MHz bandwidth gives 0.35 us rise time,\nwhich is why digital logic quoted at 100 MHz wants 3 ns or better')
elm.Annotate().at((0, -1.9)).delta(0, -0.6).label('octave = 2x in frequency = 6 dB;   decade = 10x in frequency = 20 dB')
```

- The `-3 dB` point is the `0.707` point; mixing up amplitude and power is the usual source
  of a 6 dB error.
- `tr = 0.35/fH` is the fastest way to check whether an amplifier is fast enough for a digital
  requirement.

## 10. Summary of the Useful Formulas

| Quantity | Formula | Note |
|---|---|---|
| Single-pole cutoff | `f = 1/(2*pi*R*C)` | `R` is what the capacitor sees |
| High-pass corner | `fL = 1/(2*pi*C_eq*R_eq)` | coupling and bypass caps |
| Miller capacitance | `Cm = Cbc*(1 + Av)` | dominates a CE stage |
| Dominant pole | `fH = GBW/noise gain` | one-pole op-amp |
| Gain-bandwidth product | `GBW = Av*BW` | constant for a one-pole part |
| Two equal stages | `f = 0.64*f_stage` | `sqrt(2^(1/n)-1)` in general |
| Rise time | `tr = 0.35/fH` | 10 to 90 percent |
| Slope | `-20 dB/dec` per pole | `+20 dB/dec` per zero |
| Phase | `-90 deg` per pole | `-45 deg` at the corner |
