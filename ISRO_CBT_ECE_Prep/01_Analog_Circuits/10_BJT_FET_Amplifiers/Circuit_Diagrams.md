# BJT and FET Amplifiers — Circuit Diagrams

Companion schematics for `Concepts.md`. The common-emitter stage dominates because a
bipolar transistor converts base current into collector current, while a FET stage is
voltage-controlled and needs only a bias network.

## 1. BJT Construction and Current Flow

The emitter-base junction is forward biased and the collector-base junction is reverse
biased, so almost all the emitter current becomes collector current.

```circuit
elm.Rect(corner1=(-9, 2.5), corner2=(-5, 5.5)).label('B-E junction\nforward biased:\nV_BE ~ 0.7 V', loc='center')
elm.Line(arrow='->').at((-5, 4)).right(1.5)
elm.Rect(corner1=(-3.5, 2.5), corner2=(0.5, 5.5)).label('B-C junction\nreverse biased:\ncollector sweeps\ncurrent', loc='center')
elm.Line(arrow='->').at((0.5, 4)).right(1.5)
elm.Rect(corner1=(2, 2.5), corner2=(6, 5.5)).label('alpha = Ic/Ie is\njust under 1;\nbeta = Ic/Ib is\n50 to 300', loc='center')
elm.Rect(corner1=(-9, -1.5), corner2=(-5, 1.5)).label('thin, heavily\ndoped emitter:\nsource of carriers', loc='center')
elm.Line(arrow='->').at((-5, 0)).right(1.5)
elm.Rect(corner1=(-3.5, -1.5), corner2=(0.5, 1.5)).label('lightly doped,\nwide collector:\nsinks the current\nand sets BVCEO', loc='center')
elm.Line(arrow='->').at((0.5, 0)).right(1.5)
elm.Rect(corner1=(2, -1.5), corner2=(6, 1.5)).label('base is thin:\nalpha close to 1\nmeans high beta', loc='center')
elm.Annotate().at((0, 6.2)).delta(0, 0.6).label('every amplifier question about a BJT reduces to two numbers: gm = Ic/Vt and ro = (VA + Vo)/Ic')
```

- `gm = Ic/Vt` is about 40 mS per milliamp, which is why a small bias current still gives
  a useful transconductance.
- The collector is deliberately lightly doped so that the reverse-biased base-collector
  junction sustains a large voltage.

## 2. Common Emitter with Voltage-Divider Bias

The classic stage: the divider sets the base, the emitter resistor sets the current, and the
collector resistor converts current swings into voltage swings.

```circuit
vcc = elm.SourceV().up().length(2).at((4, 2)).label('Vcc', loc='right')
elm.Ground().down().at((4, 2))
elm.Line().at((-2.5, 4)).right(6.5).to((4, 4))
elm.Annotate().at((-1, 4.4)).delta(0, 0.6).label('Vcc rail')
elm.Resistor().down().length(1.5).at((-1.5, 4)).label('R1', loc='right')
elm.Line().at((-1.5, 2.5)).down(1)
elm.Dot().at((-1.5, 1.5)).label('VB', loc='left')
elm.Resistor().down().length(1.5).at((-1.5, 1.5)).label('R2', loc='right')
elm.Ground().down().at((-1.5, 0))
elm.Line().at((-1.5, 1.5)).right(1.5)
q = elm.BjtNpn().at((0, 1.5))
elm.Dot().at((0, 1.5)).label('VB', loc='top')
elm.Line().at((0.75167, 2.19667)).up(0.30333)
elm.Line().at((0.75167, 2.5)).right(1.5)
elm.Resistor().up().length(1.5).at((0.75167, 2.5)).label('RC', loc='left')
elm.Dot().at((0.75167, 2.5)).label('VC', loc='left')
elm.Line().at((0.75167, 0.80333)).down(0.30333)
elm.Resistor().down().length(1.5).at((0.75167, 0.5)).label('RE', loc='right')
elm.Ground().down().at((0.75167, -1))
src = elm.SourceSin().right().length(2).at((-7, 1.5)).label('Vin', loc='left')
elm.Ground().down().at((-7, 1.5))
elm.Capacitor().right().length(1.5).at((-5, 1.5)).label('Cin', loc='bottom')
elm.Line().at((-3.5, 1.5)).right(3.5)
elm.Line().at((2.25167, 2.5)).right(1.5).to((3.75167, 2.5))
elm.Capacitor().right().length(1.5).at((3.75167, 2.5)).label('Cout', loc='top')
elm.Line().at((5.25167, 2.5)).right(2)
elm.Dot().at((6, 2.5)).label('Vout', loc='top')
elm.Annotate().at((7.5, 1.4)).delta(0, 0.6).label('gain = -gm*(RC || ro)\noutput inverted,\nhigh input and\nmoderate output impedance')
elm.Annotate().at((-7, 0.2)).delta(0, -0.6).label('make the divider current about ten times the base current so that VB is stiff')
```

- The Q point must satisfy both `VB = 0.7 + IE*RE` and the active-region requirement
  `VC > VB + 0.2`; design the divider first, then solve for `RC`.
- `RC` and `RE` set the gain and the swing limit; the transistor parameters only set the
  required bias.

## 3. Adding the Emitter Bypass Capacitor

Bypassing `RE` at signal frequencies restores the full `RC` gain; leaving it out trades gain
for linearity and a higher output impedance.

```circuit
vcc = elm.SourceV().up().length(2).at((4, 2)).label('Vcc', loc='right')
elm.Ground().down().at((4, 2))
elm.Line().at((-2.5, 4)).right(6.5).to((4, 4))
q = elm.BjtNpn().at((0, 1.5))
elm.Resistor().up().length(1.5).at((0.75167, 2.5)).label('RC', loc='left')
elm.Line().at((0.75167, 2.19667)).up(0.30333)
elm.Line().at((0.75167, 0.80333)).down(0.30333)
elm.Line().at((0.75167, 0.5)).right(1.5).to((2.25167, 0.5))
elm.Dot().at((0.75167, 0.5))
elm.Resistor().down().length(1.5).at((0.75167, 0.5)).label('RE', loc='left')
elm.Capacitor().down().length(1.5).at((2.25167, 0.5)).label('CE', loc='right')
elm.Ground().down().at((0.75167, -1))
elm.Ground().down().at((2.25167, -1))
src = elm.SourceSin().right().length(2).at((-7, 1.5)).label('Vin', loc='left')
elm.Ground().down().at((-7, 1.5))
elm.Capacitor().right().length(1.5).at((-5, 1.5)).label('Cin', loc='bottom')
elm.Line().at((-3.5, 1.5)).right(3.5)
elm.Line().at((0.75167, 2.5)).right(3.5).to((4.25167, 2.5))
elm.Capacitor().right().length(1.5).at((4.25167, 2.5)).label('Cout', loc='top')
elm.Line().at((5.75167, 2.5)).right(2)
elm.Dot().at((6.5, 2.5)).label('Vout', loc='top')
elm.Annotate().at((7.5, 0.6)).delta(0, 0.6).label('with CE shorted: Zin = beta*gm0 RE, gain = -gm*(RC || ro)')
elm.Annotate().at((7.5, -1)).delta(0, -0.6).label('with CE open: Zin = beta*(gm0 RE + re), gain = -gm RC RE/(RC+RE),\nwhich is far less sensitive to beta')
elm.Annotate().at((-7, 0.2)).delta(0, -0.6).label('1/(2*pi*CE*RE) is a low-frequency corner: choose it well below the signal band')
```

- Degeneration improves the linearity and makes the gain depend on resistor ratios instead of
  device parameters, which is why precision stages unbypass `RE`.
- A fully bypassed `RE` also removes the output-impedance stabilisation, so the gain now
  depends directly on `ro` and `beta`.

## 4. From re to Gain: The Small-Signal Picture

Three steps explain any BJT stage: `re` sets the input voltage, `gm` converts it to current,
and the load converts current to voltage.

```circuit
elm.Rect(corner1=(-9, 2.5), corner2=(-4, 5.5)).label('step 1: emitter-base\nis a diode\nre = 26 mV/IE ~ 1/gm0', loc='center')
elm.Line(arrow='->').at((-4, 4)).right(1.5)
elm.Rect(corner1=(-2.5, 2.5), corner2=(2.5, 5.5)).label('step 2: the base-emitter\nvoltage controls the\ncollector current: delta Ic = gm0*delta Vbe', loc='center')
elm.Line(arrow='->').at((2.5, 4)).right(1.5)
elm.Rect(corner1=(4, 2.5), corner2=(9, 5.5)).label('step 3: the collector\ncurrent flows into\nRC || ro || RL', loc='center')
elm.Line(arrow='->').at((6.5, 5.5)).up(1.5).to((6.5, 7))
elm.Rect(corner1=(4, 7), corner2=(9, 8.5)).label('Vout = -gm0*(RC || ro)*Vin', loc='center')
elm.Rect(corner1=(-9, -1.5), corner2=(-4, 1.5)).label('common emitter:\nvoltage gain = -gm RC\ncurrent gain = -beta', loc='center')
elm.Line(arrow='->').at((-4, 0)).right(1.5)
elm.Rect(corner1=(-2.5, -1.5), corner2=(2.5, 1.5)).label('common base:\nvoltage gain = +gm RC\ncurrent gain < 1', loc='center')
elm.Line(arrow='->').at((2.5, 0)).right(1.5)
elm.Rect(corner1=(4, -1.5), corner2=(9, 1.5)).label('common collector:\nvoltage gain ~ 1\ncurrent gain = +beta', loc='center')
elm.Annotate().at((0, -2.6)).delta(0, -0.6).label('the emitter is common to input and output in CE and CB, and the collector is common in CC;\nfor a FET, gate current is zero so the input resistance is set only by the bias network')
```

- Working in transconductance terms avoids the endless `alpha`, `beta`, `re`, `gm0` juggling
  that appears in textbook derivations.
- The product `gm*RC` is the figure of merit; raising it means more current, which costs
  headroom and power.

## 5. Common Base

The base is at AC ground, so the input impedance is very low and the output impedance is
high: a good broadband stage when a low input resistance is acceptable.

```circuit
vcc = elm.SourceV().up().length(2).at((4, 2)).label('Vcc', loc='right')
elm.Ground().down().at((4, 2))
elm.Line().at((-2.5, 4)).right(6.5).to((4, 4))
q = elm.BjtNpn().at((0, 1.5))
elm.Line().at((0, 1.5)).up(2.5).to((0, 4))
elm.Annotate().at((-1.5, 2.6)).delta(0, 0.6).label('base held at AC ground:\nno feedback around the input')
elm.Resistor().up().length(1.5).at((0.75167, 2.5)).label('RC', loc='left')
elm.Line().at((0.75167, 2.19667)).up(0.30333)
elm.Dot().at((0.75167, 2.5))
elm.Line().at((0.75167, 0.80333)).down(0.30333)
elm.Capacitor().down().length(1.5).at((0.75167, 0.5)).label('C', loc='right')
src = elm.SourceSin().right().length(2).at((-7, -1)).label('Vin', loc='left')
elm.Ground().down().at((-7, -1))
elm.Capacitor().right().length(1.5).at((-5, -1)).label('C', loc='bottom')
elm.Line().at((-3.5, -1)).right(4.25167).to((0.75167, -1))
elm.Line().at((0.75167, 2.5)).right(3.5).to((4.25167, 2.5))
elm.Capacitor().right().length(1.5).at((4.25167, 2.5)).label('C', loc='top')
elm.Line().at((5.75167, 2.5)).right(2)
elm.Dot().at((6.5, 2.5)).label('Vout', loc='top')
elm.Annotate().at((7.5, 0.6)).delta(0, 0.6).label('gain = +gm*RC (not inverted)')
elm.Annotate().at((7.5, -1)).delta(0, -0.6).label('Zin = 1/gm ~ 25 ohm at 1 mA, Zout ~ RC, current gain alpha < 1,\nso it is used for impedance matching, not for driving a high load')
```

- Common base stages are still used in tuned and cascode amplifiers because they avoid the
  Miller effect and stay fast.
- The DC bias is identical to a common emitter stage; only the AC grounding differs.

## 6. Emitter Follower (Common Collector)

Almost all of the input appears at the emitter, which is why it is the buffer of choice.

```circuit
vcc = elm.SourceV().up().length(2).at((4, 2)).label('Vcc', loc='right')
elm.Ground().down().at((4, 2))
elm.Line().at((-2.5, 4)).right(6.5).to((4, 4))
q = elm.BjtNpn().at((0, 1.5))
elm.Line().at((0.75167, 2.19667)).up(1.80333).to((0.75167, 4))
elm.Annotate().at((-1.5, 2.6)).delta(0, 0.6).label('collector at AC ground')
elm.Line().at((0.75167, 0.80333)).down(0.30333)
elm.Line().at((0.75167, 0.5)).right(1.5).to((2.25167, 0.5))
elm.Dot().at((0.75167, 0.5))
elm.Resistor().down().length(1.5).at((2.25167, 0.5)).label('RL', loc='right')
elm.Ground().down().at((2.25167, -1))
elm.Line().at((2.25167, 0.5)).right(2)
elm.Dot().at((3.25, 0.5)).label('Vout', loc='top')
src = elm.SourceSin().right().length(2).at((-7, 1.5)).label('Vin', loc='left')
elm.Ground().down().at((-7, 1.5))
elm.Capacitor().right().length(1.5).at((-5, 1.5)).label('Cin', loc='bottom')
elm.Line().at((-3.5, 1.5)).right(3.5)
elm.Resistor().down().length(1.5).at((0, 1.5)).label('RB', loc='left')
elm.Ground().down().at((0, 0))
elm.Line().at((2.25167, 0.5)).right(1.5).to((3.75167, 0.5))
elm.Annotate().at((5.5, 1.2)).delta(0, 0.6).label('Av = RL/(RL + re) is just under 1, so there is no phase inversion')
elm.Annotate().at((5.5, -0.8)).delta(0, -0.6).label('Zin = beta*(re + RL), Zout = re || (RL/beta) = RL/(1+beta):\nit supplies current and isolates the bias network')
```

- The DC level shifts down by `Vbe`, so a chain of followers needs level planning.
- Because the gain is close to unity, the stage cannot invert; use a common emitter for that.

## 7. Two Bias Circuits and Their Trade-Off

Fixed bias wastes base current and is beta-dependent; collector feedback removes `RB`
entirely but makes the Q point depend on beta and on `RC`.

```circuit
elm.SourceSin().right().length(2).at((-7, 1.5)).label('Vin', loc='left')
elm.Ground().down().at((-7, 1.5))
elm.Line().at((-5, 1.5)).right(2).to((-3, 1.5))
elm.Resistor().right().length(2).at((-3, 1.5)).label('RB', loc='top')
elm.Line().at((-1, 1.5)).right(1).to((0, 1.5))
q1 = elm.BjtNpn().at((0, 1.5))
elm.Dot().at((0, 1.5))
elm.Line().at((0.75167, 2.19667)).up(0.30333)
elm.Resistor().up().length(1.5).at((0.75167, 2.5)).label('RC', loc='left')
elm.Line().at((-3, 4)).right(8).to((5, 4))
elm.Line().at((0.75167, 2.5)).right(1.5).to((2.25167, 2.5))
elm.Line().at((0.75167, 0.80333)).down(0.80333)
elm.Ground().down().at((0.75167, 0))
elm.Annotate().at((-5, 3)).delta(0, 0.6).label('fixed bias:\nIB = (Vin - 0.7)/RB, IC = beta*IB\nsimple, but beta spreads the Q point\nover a wide range')
elm.SourceSin().right().length(2).at((3, 1)).label('Vin', loc='left')
elm.Ground().down().at((3, 1))
elm.Line().at((5, 1)).right(2).to((7, 1))
q2 = elm.BjtNpn().at((8, 1.5))
elm.Line().at((7, 1)).right(1)
elm.Dot().at((8, 1.5))
elm.Line().at((8.75167, 2.19667)).up(0.30333)
elm.Line().at((8.75167, 2.5)).right(1.5).to((10.25167, 2.5))
elm.Resistor().up().length(1.5).at((8.75167, 2.5)).label('RC', loc='right')
elm.Line().at((5, 4)).right(6).to((11, 4))
elm.Line().at((8.75167, 2.5)).left(3.25167).to((5.5, 2.5))
elm.Resistor().down().length(1.5).at((5.5, 2.5)).label('RB', loc='right')
elm.Line().at((5.5, 1)).right(2.5).to((8, 1))
elm.Line().at((8, 1)).up(0.5).to((8, 1.5))
elm.Dot().at((8, 1))
elm.Line().at((8.75167, 0.80333)).down(0.80333)
elm.Ground().down().at((8.75167, 0))
elm.Annotate().at((12.5, 2.4)).delta(0, 0.6).label('collector feedback:\nIB = (VC - 0.7)/RB and\nVC = Vcc - RC*beta*IB,\nso the loop pulls the Q point back')
elm.Annotate().at((12.5, 0.4)).delta(0, -0.6).label('negative feedback makes the stage\nself-biasing, but the gain also\nfalls as beta grows')
```

- Self-biasing matters when beta varies with temperature or with production spread; the
  collector-feedback resistor is the simplest such loop.
- The emitter resistor is the better stabiliser because it senses emitter current directly;
  collector feedback senses the dependent current instead.

## 8. Early Effect and Output Resistance

A finite `ro` sets the ceiling on stage gain and the slope of the output characteristic.

```circuit
elm.Rect(corner1=(-9, 2.5), corner2=(-4, 5.5)).label('physical cause:\nreverse-biased base-collector\ndepletion widens, so the\nneutral base narrows', loc='center')
elm.Line(arrow='->').at((-4, 4)).right(1.5)
elm.Rect(corner1=(-2.5, 2.5), corner2=(2.5, 5.5)).label('electrical effect:\nIc rises slightly as VCE rises,\nwith slope 1/ro', loc='center')
elm.Line(arrow='->').at((2.5, 4)).right(1.5)
elm.Rect(corner1=(4, 2.5), corner2=(9, 5.5)).label('ro = (VA + Vo)/Ic\nVA is the extrapolated\nintercept voltage, typically\n50 to 100 V', loc='center')
elm.Line().at((-3, -0.5)).right(7)
elm.Line().at((-3, -0.5)).up(1.5)
elm.Line().at((-3, 1)).right(1.25)
elm.Line().at((-1.75, 1)).down(0.5).to((-1.75, 0.5))
elm.Line().at((-1.75, 0.5)).right(1.25)
elm.Line().at((-0.5, 0.5)).up(0.5).to((-0.5, 1))
elm.Line().at((-0.5, 1)).right(4.5)
elm.Line().at((4, 0.5)).down(0.5).to((4, 0))
elm.Line().at((-0.5, 0.5)).to((4, 0.5))
elm.Dot().at((-0.5, 0.5))
elm.Annotate().at((1, 0.2)).delta(0, -0.6).label('slope 1/ro between the knee and breakdown')
elm.Annotate().at((0.25, -1.5)).delta(0, -0.6).label('VCE = VA is the extrapolated intercept: the point where the straight extension meets the Ic axis')
elm.Annotate().at((-3, -2.6)).delta(0, -0.6).label('consequences: gain is limited to gm*(RC || ro), Zout ~ RC || ro, and the Early effect\nadds a direct feed-forward from collector to emitter, which is the key\nparasitic capacitance in high-frequency analysis')
```

- For `gm*RC` to dominate, `RC` should be well below `ro`; when it is not, the stage is
  `ro`-limited and more current will not help.
- `Cmu` is a real junction capacitance, not a modelling artefact, and it produces the
  Miller effect that limits the high-frequency gain.

## 9. Common Source with Source Degeneration

The FET stage is a voltage amplifier from the gate: the gate current is essentially zero, so
only the bias network loads the source.

```circuit
vdd = elm.SourceV().up().length(2).at((-5, 2)).label('Vdd', loc='left')
elm.Ground().down().at((-5, 2))
elm.Line().at((-5, 4)).right(9).to((4, 4))
m = elm.NMos().at((2, 1.16667))
elm.Resistor().up().length(2.5).at((2, 1.5)).label('RD', loc='left')
elm.Line().at((2, 1.16667)).up(0.33333)
elm.Dot().at((2, 1.5))
elm.Line().at((2, 1.5)).right(2).to((4, 1.5))
elm.Capacitor().right().length(1.5).at((4, 1.5)).label('Cout', loc='top')
elm.Line().at((5.5, 1.5)).right(2)
elm.Dot().at((6.5, 1.5)).label('Vout', loc='top')
elm.Line().at((2, -0.5)).down(0.5)
elm.Resistor().down().length(1.5).at((2, -1)).label('RS', loc='right')
elm.Ground().down().at((2, -2.5))
src = elm.SourceSin().right().length(2).at((-8, 0)).label('Vin', loc='left')
elm.Ground().down().at((-8, 0))
elm.Capacitor().right().length(1.5).at((-6, 0)).label('Cin', loc='bottom')
elm.Line().at((-4.5, 0)).right(5.66667)
elm.Dot().at((1.16667, 0)).label('VG', loc='top')
elm.Resistor().up().length(1.5).at((1.16667, 0)).label('R1', loc='left')
elm.Resistor().down().length(1.5).at((1.16667, 0)).label('R2', loc='left')
elm.Ground().down().at((1.16667, -1.5))
elm.Line().at((1.16667, 1.5)).up(2.5).to((1.16667, 4))
elm.Annotate().at((8.5, 1.4)).delta(0, 0.6).label('gain = -gm*RD/(1 + gm*RS)\nand RS sets the linearity;\nwith RS bypassed the gain is -gm*RD')
elm.Annotate().at((-8, 1.4)).delta(0, 0.6).label('the gate draws no current, so the input impedance is\njust R1 || R2: often megaohms')
elm.Annotate().at((8.5, -1.2)).delta(0, -0.6).label('the source degeneration also raises the output impedance, which is what the\nsource follower uses as its gain mechanism')
```

- A JFET version of this circuit uses `gm = Id/2*Vt` at the drain current `Id/2`, so a JFET
  needs four times the drain current of a MOSFET for the same transconductance.
- The JFET gate-current zero and the reverse-biased gate junction are why JFETs tolerate a
  much larger input swing and are preferred for low-distortion audio.

## 10. Source Follower

The drain is at AC ground and the source follows the gate through `gm`; the gain approaches
one and the output impedance collapses.

```circuit
vdd = elm.SourceV().up().length(2).at((-5, 2)).label('Vdd', loc='left')
elm.Ground().down().at((-5, 2))
elm.Line().at((-5, 4)).right(9).to((4, 4))
m = elm.NMos().at((2, 1.16667))
elm.Line().at((2, 1.16667)).up(2.83333).to((2, 4))
elm.Annotate().at((-1, 2.6)).delta(0, 0.6).label('drain at AC ground')
elm.Line().at((2, -0.5)).down(0.5)
elm.Dot().at((2, -1))
elm.Resistor().down().length(1.5).at((2, -1)).label('RL', loc='right')
elm.Ground().down().at((2, -2.5))
elm.Line().at((2, -1)).right(2.5).to((4.5, -1))
elm.Dot().at((3.25, -1)).label('Vout', loc='top')
src = elm.SourceSin().right().length(2).at((-8, 0)).label('Vin', loc='left')
elm.Ground().down().at((-8, 0))
elm.Capacitor().right().length(1.5).at((-6, 0)).label('Cin', loc='bottom')
elm.Line().at((-4.5, 0)).right(5.66667)
elm.Dot().at((1.16667, 0))
elm.Resistor().up().length(1.5).at((1.16667, 0)).label('R1', loc='left')
elm.Resistor().down().length(1.5).at((1.16667, 0)).label('R2', loc='left')
elm.Ground().down().at((1.16667, -1.5))
elm.Line().at((1.16667, 1.5)).up(2.5).to((1.16667, 4))
elm.Annotate().at((7, -0.2)).delta(0, 0.6).label('Av = gm*RL/(1 + gm*RL) ~ 1, Zout = 1/gm ~ 100 ohm at 10 mA')
elm.Annotate().at((7, -1.8)).delta(0, -0.6).label('a CMOS source follower is weak (body effect, low gm), so a bipolar emitter\nfollower or a common-source stage is preferred wherever gain is needed')
```

- The source follower makes a good output stage because its `1/gm` output impedance lets it
  drive a low-resistance load without a large quiescent current.
- Its threshold shifts with the output swing in a CMOS process, so level shifters are
  inserted between logic stages that need true rail-to-rail swings.

## 11. Cascode

Stacking a second device above the first raises the output resistance to roughly
`gm*ro*ro`, multiplying the stage gain.

```circuit
vdd = elm.SourceV().up().length(2).at((-2, 3)).label('Vdd', loc='left')
elm.Ground().down().at((-2, 3))
elm.Line().at((-2, 5)).right(7).to((5, 5))
m1 = elm.NMos().at((2, 1.16667))
m2 = elm.NMos().at((2, 4.16667))
elm.Line().at((2, 1.16667)).up(1.33333).to((2, 2.5))
elm.Dot().at((2, 2.5)).label('casode node', loc='right')
elm.Line().at((2, 4.16667)).up(0.83333)
elm.Line().at((2, 5)).right(2).to((4, 5))
elm.Capacitor().right().length(1.5).at((4, 5)).label('Cout', loc='top')
elm.Line().at((5.5, 5)).right(2)
elm.Dot().at((6.5, 5)).label('Vout', loc='top')
elm.Line().at((2, -0.5)).down(0.5)
elm.Resistor().down().length(1.5).at((2, -1)).label('RS', loc='right')
elm.Ground().down().at((2, -2.5))
src = elm.SourceSin().right().length(2).at((-8, 0)).label('Vin', loc='left')
elm.Ground().down().at((-8, 0))
elm.Capacitor().right().length(1.5).at((-6, 0)).label('Cin', loc='bottom')
elm.Line().at((-4.5, 0)).right(5.66667)
elm.Dot().at((1.16667, 0)).label('gate M1', loc='top')
elm.Resistor().up().length(1.5).at((1.16667, 0)).label('R1', loc='left')
elm.Line().at((1.16667, 1.5)).up(3.5).to((1.16667, 5))
elm.Resistor().down().length(1.5).at((1.16667, 0)).label('R2', loc='left')
elm.Ground().down().at((1.16667, -1.5))
elm.Line().at((1.16667, 3)).right(1)
elm.Annotate().at((-1, 3)).delta(0, 0.6).label('gate M2 biased by a\nconstant: the cascode\nsenses the source\nvoltage and holds it')
elm.Annotate().at((8, 3.4)).delta(0, 0.6).label('Rout ~ gm*ro^2, so the gain is gm*RD*gm*ro,\nbut the headroom now spans two devices')
elm.Annotate().at((8, 1.4)).delta(0, -0.6).label('cascode stages dominate analog CMOS because output resistance,\nnot gm, limits the gain of a simple common-source stage')
```

- The cascode device must stay in saturation; a cascode bipolar transistor also improves
  isolation, at the cost of an extra `Vbe` of headroom and a possible `Vce,sat` limit.
- Cascoding two common-source stages does not improve noise; the cascode is a gain and
  impedance technique, not a noise technique.

## 12. Configuration Summary

| Configuration | Input | Output | Voltage gain | Current gain | Rin | Rout | Inverts |
|---|---|---|---|---|---|---|---|
| Common emitter | base | collector | `-gm*(RC || ro)` | `-beta` | `beta*re` | `RC || ro` | yes |
| Common base | emitter | collector | `+gm*(RC || ro)` | `alpha` | `re` | `RC || ro` | no |
| Emitter follower | base | emitter | `~1` | `+beta` | `beta*(re+RL)` | `RL/beta` | no |
| Common source | gate | drain | `-gm*RD` | huge | `R1 || R2` | `RD` | yes |
| Source follower | gate | source | `~1` | huge | `R1 || R2` | `1/gm` | no |
| Cascode | gate | drain | `-gm*RD*gm*ro` | huge | `R1 || R2` | `gm*ro^2` | yes |

- The common emitter and common source are the only configurations that provide both gain
  and inversion, which is what makes them the default first stage.
- A follower stage is chosen whenever the source or load resistance is the problem, not
  because a gain is wanted.
