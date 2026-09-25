# IC Voltage Regulators — Circuit Diagrams

Companion schematics for `Concepts.md`. A regulator holds one voltage constant while the
input, the load or the temperature moves; the only real choice is where the excess energy
goes, into a transistor or into an inductor.

## 1. What a Regulator Does

One feedback loop does the whole job: compare the output with a reference, drive the pass
element until they match, and the output stops moving.

```circuit
elm.Rect(corner1=(-9, 2.5), corner2=(-4, 5.5)).label('reference:\nbandgap or zener,\ntrimmed so the supply\nis temperature-stable', loc='center')
elm.Line(arrow='->').at((-4, 4)).right(1.5)
elm.Rect(corner1=(-2.5, 2.5), corner2=(2.5, 5.5)).label('error amplifier:\nmeasures the feedback\nagainst the reference and\namplifies the difference', loc='center')
elm.Line(arrow='->').at((2.5, 4)).right(1.5)
elm.Rect(corner1=(4, 2.5), corner2=(9, 5.5)).label('pass element:\ntransistor or switch in\nseries with the load;\nits drop is the variable', loc='center')
elm.Line(arrow='->').at((6.5, 5.5)).up(1.5).to((6.5, 7))
elm.Rect(corner1=(4, 7), corner2=(9, 8.5)).label('Vout, held constant', loc='center')
elm.Line().at((6.5, 8.5)).up(1.5).to((6.5, 10))
elm.Line().at((-9, 10)).right(15.5).to((6.5, 10))
elm.Line().at((-9, 10)).down(5.5).to((-9, 4.5))
elm.Rect(corner1=(-9, -1.5), corner2=(-4, 1.5)).label('what moves the output:\ninput line variation', loc='center')
elm.Line(arrow='->').at((-4, 0)).right(1.5)
elm.Rect(corner1=(-2.5, -1.5), corner2=(2.5, 1.5)).label('load current change', loc='center')
elm.Line(arrow='->').at((2.5, 0)).right(1.5)
elm.Rect(corner1=(4, -1.5), corner2=(9, 1.5)).label('temperature drift', loc='center')
elm.Annotate().at((0, 6.2)).delta(0, 0.6).label('the loop must be faster than any disturbance it is meant to reject')
elm.Annotate().at((0, -2.6)).delta(0, -0.6).label('the loop gain sets how much each disturbance is suppressed: a better reference lowers\nthe noise, a bigger loop gain lowers both line and load regulation')
```

- Negative feedback is the entire mechanism; the reference quality and the loop gain are the
  two things that separate a good regulator from a mediocre one.
- The pass element is the only part that dissipates power in a linear regulator, so its
  limit defines the package and the heat sink.

## 2. Performance Parameters

Every datasheet number is one of these four measurements, plus the limits that protect the
device.

```circuit
elm.Rect(corner1=(-9, 2.5), corner2=(-4, 5.5)).label('line regulation:\ndVout/dVin for a fixed load,\nquoted in uV/V or %/V', loc='center')
elm.Line(arrow='->').at((-4, 4)).right(1.5)
elm.Rect(corner1=(-2.5, 2.5), corner2=(2.5, 5.5)).label('load regulation:\ndVout/dI at fixed Vin,\nquoted in mV or uV/A', loc='center')
elm.Line(arrow='->').at((2.5, 4)).right(1.5)
elm.Rect(corner1=(4, 2.5), corner2=(9, 5.5)).label('ripple rejection:\ninput ripple divided by\noutput ripple, in dB\n(negative feedback helps)', loc='center')
elm.Rect(corner1=(-9, -1.5), corner2=(-4, 1.5)).label('dropout voltage:\nthe smallest Vin - Vout that\nstill regulates, and the\ninput capacitor that owns it', loc='center')
elm.Line(arrow='->').at((-4, 0)).right(1.5)
elm.Rect(corner1=(-2.5, -1.5), corner2=(2.5, 1.5)).label('quiescent current:\ndrawn with no load;\nlow value matters for\nbattery operation', loc='center')
elm.Line(arrow='->').at((2.5, 0)).right(1.5)
elm.Rect(corner1=(4, -1.5), corner2=(9, 1.5)).label('PSRR and noise:\nsame measurement as ripple\nrejection but reported\nin dB at a frequency', loc='center')
elm.Annotate().at((0, 6.2)).delta(0, 0.6).label('a rule of thumb: a fixed 78xx is good to a few tens of mV, a good LDO to a few mV,\nand a switched regulator to a few tens of mV before its own switching ripple is counted')
elm.Annotate().at((0, -2.6)).delta(0, -0.6).label('the datasheet conditions matter: line regulation is usually quoted at a fixed load,\nand load regulation at a fixed line, so compare like with like')
```

- Regulation percentage is relative to the output voltage, so a 5 V part looks worse in
  millivolts than a 12 V part with the same circuit.
- Dropout is the number that decides whether a battery is usable: the supply is dead once
  `Vin < Vout + dropout`.

## 3. Three-Terminal Fixed Regulator (7805)

The whole regulator is a rectangle to the designer: input capacitor in, output capacitor
out, and heat to remove.

```circuit
vin = elm.SourceV().up().length(2).at((-6, 0)).label('DC input\nsay 9 V', loc='left')
elm.Ground().down().at((-6, 0))
elm.Line().at((-6, 2)).up(0.5).to((-6, 2.5))
elm.Line().at((-4, 2.5)).right(0.5).to((-3.5, 2.5))
elm.Line().at((-4, 2.5)).down(1.5).to((-4, 1))
elm.Dot().at((-4, 2.5))
elm.Capacitor().down().length(1.5).at((-4, 1)).label('0.1 uF', loc='left')
elm.Ground().down().at((-4, -0.5))
elm.Rect(corner1=(-3.5, 0.5), corner2=(0.5, 3.5)).label('7805\nIN   OUT   GND', loc='center')
elm.Line().at((0.5, 2.5)).right(1.5).to((2, 2.5))
elm.Dot().at((2, 2.5))
elm.Capacitor().down().length(2).at((2, 2.5)).label('0.33 uF', loc='right')
elm.Ground().down().at((2, 0.5))
elm.Line().at((2, 2.5)).right(1.5).to((3.5, 2.5))
elm.Resistor().down().length(2).at((3.5, 2.5)).label('load', loc='right')
elm.Ground().down().at((3.5, 0.5))
elm.Dot().at((2.5, 2.5)).label('+5 V', loc='top')
elm.Line().at((-1.5, 0.5)).down(0.5).to((-1.5, 0))
elm.Ground().down().at((-1.5, 0))
elm.Annotate().at((5.5, 1.6)).delta(0, 0.6).label('heat: (9 - 5)*1 A = 4 W, so the tab must go to a\nheat sink; without one the device shuts down')
elm.Annotate().at((5.5, -0.4)).delta(0, -0.6).label('the input capacitor must sit within a few mm of the IN pin:\nit supplies the transient current and prevents oscillation')
elm.Annotate().at((-9, 1.4)).delta(0, 0.6).label('the 79xx family is the same part in a negative-supply\npinout: 7905 gives -5 V, 7912 gives -12 V')
```

- The ground pin of a 78xx is the reference: the output voltage is measured relative to it,
  so the layout of that trace sets the accuracy.
- The fixed part has no feedback pin, so the internal divider is trimmed during manufacture;
  the adjustable part exposes that divider instead.

## 4. Adjustable Regulator (LM317)

The 1.25 V reference is exposed through the adjust pin, so two resistors set the output.

```circuit
vin = elm.SourceV().up().length(2).at((-6, -0.5)).label('Vin', loc='left')
elm.Ground().down().at((-6, -0.5))
elm.Line().at((-6, 1.5)).right(4)
elm.Line().at((-4, 1.5)).down(0.5).to((-4, 1))
elm.Dot().at((-4, 1.5))
elm.Capacitor().down().length(1.5).at((-4, 1)).label('0.1 uF', loc='left')
elm.Ground().down().at((-4, -0.5))
elm.Rect(corner1=(-2, -0.5), corner2=(2.5, 2.5)).label('LM317\nIN   ADJ   OUT', loc='center')
elm.Line().at((2.5, 2)).right(1.5).to((4, 2))
elm.Dot().at((4, 2))
elm.Line().at((4, 2)).right(1.5).to((5.5, 2))
elm.Dot().at((5.5, 2))
elm.Capacitor().down().length(2).at((5.5, 2)).label('Cout', loc='right')
elm.Ground().down().at((5.5, 0))
elm.Line().at((5.5, 2)).right(1.5).to((7, 2))
elm.Resistor().down().length(2).at((7, 2)).label('load', loc='right')
elm.Ground().down().at((7, 0))
elm.Dot().at((4.75, 2)).label('Vout', loc='top')
elm.Resistor().down().length(1.5).at((4, 2)).label('R1', loc='left')
elm.Line().at((4, 0.5)).right(1.5).to((5.5, 0.5))
elm.Dot().at((4, 0.5))
elm.Resistor().down().length(1.5).at((5.5, 0.5)).label('R2', loc='right')
elm.Ground().down().at((5.5, -1))
elm.Annotate().at((9, 2.4)).delta(0, 0.6).label('Vout = 1.25 V * (1 + R2/R1): with R1 = 240 Ohm fixed\nand R2 adjustable, the range runs from 1.25 V to 37 V')
elm.Annotate().at((9, 0.4)).delta(0, -0.6).label('R1 must stay close to the ADJ pin: its drop creates the\n1.25 V, so a long trace adds error; a protection diode from\nOUT to IN keeps the output capacitor from discharging into the chip')
elm.Annotate().at((9, -1.8)).delta(0, -0.6).label('the 1.25 V reference is a current source into ADJ, so the divider current\nshould be well above the 50 uA reference current: 240 Ohm gives about 5 mA')
```

- The maximum output is `37 V` for the 317 regardless of the resistor ratio, because that is
  the reference charge limit.
- Minimum load current is a real requirement: below a few milliamps the part will not
  regulate, which is why a bleeder resistor is often added.

## 5. Negative Adjustable Regulator (LM337)

The negative mirror image: the same divider equation with the sign reversed, and the ground
reference at the opposite end.

```circuit
vin = elm.SourceV().down().length(2).at((-1.5, 4.5)).label('Vin', loc='left')
elm.Ground().down().at((-1.5, 4.5))
elm.Rect(corner1=(-2, -0.5), corner2=(2.5, 2.5)).label('LM337\nIN   ADJ   OUT', loc='center')
elm.Line().at((2.5, 0.5)).right(1.5).to((4, 0.5))
elm.Dot().at((4, 0.5))
elm.Line().at((4, 0.5)).right(1.5).to((5.5, 0.5))
elm.Dot().at((5.5, 0.5))
elm.Capacitor().down().length(2).at((5.5, 0.5)).label('Cout', loc='right')
elm.Ground().down().at((5.5, -1.5))
elm.Line().at((5.5, 0.5)).right(1.5).to((7, 0.5))
elm.Resistor().down().length(2).at((7, 0.5)).label('load', loc='right')
elm.Ground().down().at((7, -1.5))
elm.Dot().at((4.75, 0.5)).label('Vout', loc='top')
elm.Resistor().down().length(1.5).at((4, 0.5)).label('R1', loc='left')
elm.Line().at((4, -1)).right(1.5).to((5.5, -1))
elm.Dot().at((4, -1))
elm.Line().at((4, -1)).left(3.5).to((0.5, -1))
elm.Line().at((0.5, -1)).up(0.5).to((0.5, -0.5))
elm.Resistor().down().length(1.5).at((5.5, -1)).label('R2', loc='right')
elm.Ground().down().at((5.5, -2.5))
elm.Annotate().at((9, 1.6)).delta(0, 0.6).label('Vout = -1.25 V * (1 + R2/R1), same divider as the 317\nwith the polarity reversed')
elm.Annotate().at((9, -0.4)).delta(0, -0.6).label('the 337 needs the same output capacitor for stability and,\nlike the 317, draws a few milliamps of load current:\ndual supplies from one pair of chips are common')
elm.Annotate().at((9, -2.4)).delta(0, -0.6).label('pinouts differ between the positive and negative parts, which is a\nclassic wiring error: check the datasheet drawing, not the label')
```

- A tracking pair of 317 and 337 parts gives plus and minus rails from the same divider
  voltages.
- Dropout and maximum voltage match the positive part, so the same heat-sink rules apply with
  the same numbers.

## 6. Low-Dropout Regulator

An LDO keeps a PNP or PMOS pass device in its active region all the way down to a few
hundred millivolts, which is what makes it efficient from a battery.

```circuit
elm.Rect(corner1=(-9, 2.5), corner2=(-4, 5.5)).label('standard 7805:\npass NPN or PNP must keep\n0.7 V of Vbe plus saturation\nheadroom in the output stage', loc='center')
elm.Line(arrow='->').at((-4, 4)).right(1.5)
elm.Rect(corner1=(-2.5, 2.5), corner2=(2.5, 5.5)).label('LDO:\nPMOS pass device needs no\nVbe, so dropout can be a\nfew tens of millivolts', loc='center')
elm.Line(arrow='->').at((2.5, 4)).right(1.5)
elm.Rect(corner1=(4, 2.5), corner2=(9, 5.5)).label('cost: the pass element needs\na stable ESR range in the\noutput capacitor, or a\nzero added for stability', loc='center')
elm.Rect(corner1=(-9, -1.5), corner2=(-4, 1.5)).label('efficiency of a linear stage:\neta = Vout/Vin', loc='center')
elm.Line(arrow='->').at((-4, 0)).right(1.5)
elm.Rect(corner1=(-2.5, -1.5), corner2=(2.5, 1.5)).label('5 V from 5.5 V gives 91%;\n3.3 V from 3.7 V gives 89%;\n12 V from 12 V is impossible', loc='center')
elm.Line(arrow='->').at((2.5, 0)).right(1.5)
elm.Rect(corner1=(4, -1.5), corner2=(9, 1.5)).label('so an LDO belongs after a\nswitching stage: convert first,\nthen clean up the noise', loc='center')
elm.Annotate().at((0, 6.2)).delta(0, 0.6).label('a linear stage is also the cleanest regulator for a low-noise analog rail,\nbecause there is no switching frequency to filter')
elm.Annotate().at((0, -2.6)).delta(0, -0.6).label('an LDO cannot supply more current than the pass device and cannot survive a\nshort on its own: it still needs the current limit and thermal shutdown of a 78xx')
```

- The dropout number is the whole reason an LDO exists; everything else it does is the same
  feedback loop as a 78xx.
- Output-capacitor ESR lies in a window: too little and the loop oscillates, too much and the
  loop becomes sluggish, which is why datasheets specify a capacitor value and tolerance.

## 7. Buck (Step-Down) Converter

An inductor stores energy while the switch is on and releases it while the switch is off, so
the average output is less than the input with no linear loss.

```circuit
vin = elm.SourceV().up().length(2).at((-8, 0)).label('Vin', loc='left')
elm.Ground().down().at((-8, 0))
elm.Line().at((-8, 2)).up(0.5).to((-8, 2.5))
elm.Line().at((-8, 2.5)).right(8).to((0, 2.5))
sw = elm.NMos().at((0, 2.5))
elm.Line().at((-0.8333, 1.33333)).left(2.6667).to((-3.5, 1.33333))
elm.Rect(corner1=(-7, 0.5), corner2=(-3.5, 2.2)).label('PWM controller\nwith feedback and\ncurrent limit', loc='center')
elm.Line().at((0, 0.83333)).down(0.83333).to((0, 0))
elm.Inductor().right().length(2).at((0, 0)).label('L', loc='bottom')
elm.Line().at((2, 0)).right(3).to((5, 0))
elm.Dot().at((5, 0))
elm.Capacitor().down().length(2).at((5, 0)).label('C', loc='right')
elm.Ground().down().at((5, -2))
elm.Line().at((2, 0)).right(2).to((4, 0))
elm.Resistor().down().length(2).at((4, 0)).label('load', loc='right')
elm.Ground().down().at((4, -2))
elm.Resistor().up().length(1.5).at((5, 0)).label('R1', loc='right')
elm.Resistor().down().length(1.5).at((5, 0)).label('R2', loc='left')
elm.Ground().down().at((5, -3.5))
elm.Line().at((5, 0)).right(1).to((6, 0))
elm.Line().at((6, 0)).down(3).to((6, -3))
elm.Line().at((6, -3)).left(9.5).to((-3.5, -3))
elm.Line().at((-3.5, -3)).up(3.5).to((-3.5, 0.5))
elm.Annotate().at((-5.5, -3.6)).delta(0, -0.6).label('the controller sets the duty cycle D so that Vout = D*Vin;\nthe feedback divider tells it what Vout is doing')
elm.Annotate().at((8, 1.4)).delta(0, 0.6).label('switch on: current rises through L and the load\nswitch off: L forces current through C, so the output\nstays near Vout with ripple of about\nDeltaI*L/(Vin*C)')
elm.Annotate().at((8, -1.2)).delta(0, -0.6).label('efficiency of 85 to 95% because the loss is only I2R in L, the switch\nand the diode; the ripple current in the capacitor is\noften the real limit on how much load can be served')
```

- Duty cycle, not feedback accuracy, sets the ratio: the loop only corrects the error, so a
  fast loop with a slow reference is still an accurate supply.
- The output ripple is triangular at the switching frequency, so a second-stage LDO removes
  it at the cost of some efficiency.

## 8. Boost (Step-Up) Converter

The same inductor trick with the diode and switch interchanged: the inductor is charged from
the input and then discharged in series with it, so the output exceeds the input.

```circuit
vin = elm.SourceV().up().length(2).at((-7, -1)).label('Vin', loc='left')
elm.Ground().down().at((-7, -1))
elm.Line().at((-7, 1)).up(1).to((-7, 2))
elm.Inductor().right().length(2).at((-5, 2)).label('L', loc='bottom')
elm.Line().at((-3, 2)).right(1.5).to((-1.5, 2))
elm.Dot().at((-3, 2)).label('switching node', loc='bottom')
elm.Switch().down().length(1.5).at((-3, 2)).label('switch', loc='left')
elm.Line().at((-3, 0.5)).down(0.5).to((-3, 0))
elm.Ground().down().at((-3, 0))
elm.Line().at((-3, 2)).up(0.5).to((-3, 2.5))
elm.Diode().up().length(1.5).at((-3, 2.5)).label('D', loc='left')
elm.Line().at((-3, 4)).right(5).to((2, 4))
elm.Dot().at((2, 4))
elm.Capacitor().down().length(2).at((2, 4)).label('C', loc='right')
elm.Ground().down().at((2, 2))
elm.Line().at((2, 4)).right(2).to((4, 4))
elm.Resistor().down().length(2).at((4, 4)).label('load', loc='right')
elm.Ground().down().at((4, 2))
elm.Dot().at((3, 4)).label('Vout > Vin', loc='top')
elm.Annotate().at((6.5, 3.4)).delta(0, 0.6).label('switch on: the diode is reverse biased, the inductor\nstores energy and the load is fed from C alone')
elm.Annotate().at((6.5, 1.4)).delta(0, -0.6).label('switch off: the inductor discharges into C through D, adding its\nvoltage to Vin, so the output rises above the input')
elm.Annotate().at((-7, -2.4)).delta(0, -0.6).label('the output cannot fall below Vin in this simple form: once D conducts the\nswitch node is pinned at Vin + Vd, which is the limit when Vout approaches Vin')
```

- The same inductor, switch and feedback block serves every topology; only their connections
  change, which is why converter controllers are sold as general parts.
- A boost converter draws a larger input current than it delivers, so the input supply and
  its wiring must be sized for the output power.

## 9. Series, Shunt and Switching Compared

The topology decides where the unwanted energy goes, and that decides the efficiency.

```circuit
elm.Rect(corner1=(-10, 2.5), corner2=(-5, 5.5)).label('series (linear):\nexcess drops across the\npass transistor as heat\neta = Vout/Vin', loc='center')
elm.Line(arrow='->').at((-5, 4)).right(1.5)
elm.Rect(corner1=(-3.5, 2.5), corner2=(1.5, 5.5)).label('shunt (zener):\nthe resistor burns the\nexcess and the zener\nsets Vout', loc='center')
elm.Line(arrow='->').at((1.5, 4)).right(1.5)
elm.Rect(corner1=(3, 2.5), corner2=(8, 5.5)).label('switching:\nthe inductor takes the\nexcess and gives it\nback later', loc='center')
elm.Rect(corner1=(-10, -1.5), corner2=(-5, 1.5)).label('use a shunt for references,\nsense circuits and\nsmall currents only', loc='center')
elm.Line(arrow='->').at((-5, 0)).right(1.5)
elm.Rect(corner1=(-3.5, -1.5), corner2=(1.5, 1.5)).label('use a series pass for\nlow-noise rails where\nthe drop is small', loc='center')
elm.Line(arrow='->').at((1.5, 0)).right(1.5)
elm.Rect(corner1=(3, -1.5), corner2=(8, 1.5)).label('use switching whenever\nthe drop is more than\na volt or two, then\nadd an LDO if noise matters', loc='center')
elm.Annotate().at((-1, 6.2)).delta(0, 0.6).label('the conduction loss of a linear stage is P = (Vin - Vout)*I, which is why a 12 V input\nsupply for a 5 V rail wastes 60% of the power and needs a heat sink')
elm.Annotate().at((-1, -2.6)).delta(0, -0.6).label('switching converters add their own problems: ripple, radiated noise, and a loop that\nmust be compensated for stability, which is why a linear stage still has a place')
```

## 10. Inside a Three-Terminal Regulator

The same five blocks appear in a 7805, an LM317 and an LDO; only the pass device differs.

```circuit
elm.Rect(corner1=(-9, 3), corner2=(-5, 6)).label('bandgap reference:\n1.2 V from a current mirror\nplus a compensated pair;\n0.1% typical, TC < 100 ppm', loc='center')
elm.Line(arrow='->').at((-5, 4.5)).right(1.5)
elm.Rect(corner1=(-3.5, 3), corner2=(0.5, 6)).label('error amplifier:\nsets the pass device\ndrive until the feedback\nmatches the reference', loc='center')
elm.Line(arrow='->').at((0.5, 4.5)).right(1.5)
elm.Rect(corner1=(2, 3), corner2=(6, 6)).label('pass transistor:\nthe series element that\nabsorbs the excess', loc='center')
elm.Line(arrow='->').at((6, 4.5)).right(1.5)
elm.Rect(corner1=(7.5, 3), corner2=(11, 6)).label('output\npin', loc='center')
elm.Rect(corner1=(-9, -1), corner2=(-5, 2)).label('feedback divider:\ninternal and trimmed for a\nfixed part, external for\nthe adjustable one', loc='center')
elm.Line(arrow='->').at((-5, 0.5)).right(1.5)
elm.Rect(corner1=(-3.5, -1), corner2=(0.5, 2)).label('current limit and\nthermal shutdown:\nthe part protects itself\nand shuts down hot', loc='center')
elm.Line(arrow='->').at((0.5, 0.5)).right(1.5)
elm.Rect(corner1=(2, -1), corner2=(6, 2)).label('the adjustable part\nexposes the divider and\nthe 1.25 V reference\nthrough ADJ', loc='center')
elm.Line(arrow='->').at((6, 0.5)).right(1.5)
elm.Rect(corner1=(7.5, -1), corner2=(11, 2)).label('a 78xx is this\ndiagram with a fixed\ndivider and no\nadjust pin', loc='center')
elm.Annotate().at((1, 7)).delta(0, 0.6).label('all of this fits in one small die, so the external parts are only the capacitors and, for an adjustable part, two resistors')
```

- The reference is the accuracy limit; the error amplifier and the pass device set the
  regulation.
- Protection is inside the IC, but it is not a substitute for a correctly rated load or
  layout.

## 11. Protection and Safe Operating Area

The failure modes a regulator must survive are short circuits, hot dies and reverse voltage.

```circuit
elm.Rect(corner1=(-9, 2.5), corner2=(-4, 5.5)).label('current limit:\nfoldback or hiccup;\nprotects the pass device\nbut not the load', loc='center')
elm.Line(arrow='->').at((-4, 4)).right(1.5)
elm.Rect(corner1=(-2.5, 2.5), corner2=(2.5, 5.5)).label('thermal shutdown:\nshuts down near 150 C and\nrestarts when cool;\nno regulation while shut', loc='center')
elm.Line(arrow='->').at((2.5, 4)).right(1.5)
elm.Rect(corner1=(4, 2.5), corner2=(9, 5.5)).label('reverse protection:\na diode or a blocking\ncapability, because a\nreverse-biased pass device\ncan fail short', loc='center')
elm.Rect(corner1=(-9, -1.5), corner2=(-4, 1.5)).label('safe operating area:\nVce and Ic cannot both be\nlarge; the tab temperature\nand the package set the limit', loc='center')
elm.Line(arrow='->').at((-4, 0)).right(1.5)
elm.Rect(corner1=(-2.5, -1.5), corner2=(2.5, 1.5)).label('a heat sink cuts the\nthermal resistance from\nthe die to the case, so\nthe same die handles more watts', loc='center')
elm.Line(arrow='->').at((2.5, 0)).right(1.5)
elm.Rect(corner1=(4, -1.5), corner2=(9, 1.5)).label('calculate the worst case:\nlargest Vin, largest Iout\nand the highest ambient,\nwith no airflow', loc='center')
elm.Annotate().at((0, 6.2)).delta(0, 0.6).label('foldback current limit reduces the power as the voltage rises, so the device survives\na short without entering its secondary breakdown region')
elm.Annotate().at((0, -2.6)).delta(0, -0.6).label('thermal shutdown is a last resort, not a design tool: a regulator that cycles on and\noff is thermally limited and needs a bigger heat sink or less dissipation')
```

## 12. Applications and the Numbers to Remember

| Need | Part or topology | Remember |
|---|---|---|
| Fixed 5 V or 12 V rail | 7805, 7812, 7824 | about 2 V dropout, 1 A, heat sink if `P` is large |
| Fixed negative rail | 7905, 7912 | same part, mirrored pinout |
| Adjustable positive | LM317 | `Vout = 1.25*(1 + R2/R1)`, 1.25 to 37 V |
| Adjustable negative | LM337 | same, negative polarity |
| Battery to 3.3 V | LDO after a buck | efficiency `Vout/Vin` |
| High current, high ratio | buck or boost | 85 to 95% efficient |
| Precision reference | TL431 or a bandgap | better than a zener, needs its own bias |

```circuit
elm.Rect(corner1=(-9, 2.5), corner2=(-4, 5.5)).label('digital rail:\n5 V or 3.3 V from a bridge\nplus a 78xx for the lowest\neffort, or a buck when the\ncurrent is above a few amps', loc='center')
elm.Line(arrow='->').at((-4, 4)).right(1.5)
elm.Rect(corner1=(-2.5, 2.5), corner2=(2.5, 5.5)).label('analog rails:\nLDO after a buck, so the\nswitching ripple is removed\nand PSRR is high', loc='center')
elm.Line(arrow='->').at((2.5, 4)).right(1.5)
elm.Rect(corner1=(4, 2.5), corner2=(9, 5.5)).label('reference rails:\nTL431 or a bandgap with its\nown bias, buffered if more\nthan one load needs it', loc='center')
elm.Rect(corner1=(-9, -1.5), corner2=(-4, 1.5)).label('point-of-load:\nthe regulator belongs next\nto the load; trace\ninductance is part of the\nloop impedance', loc='center')
elm.Line(arrow='->').at((-4, 0)).right(1.5)
elm.Rect(corner1=(-2.5, -1.5), corner2=(2.5, 1.5)).label('decoupling:\none bulk capacitor at the\npin plus 100 nF at every\nIC, and the loop area kept\nsmall on the board', loc='center')
elm.Line(arrow='->').at((2.5, 0)).right(1.5)
elm.Rect(corner1=(4, -1.5), corner2=(9, 1.5)).label('reverse polarity and\ntransients need external\nprotection on long wires\nfrom a battery', loc='center')
elm.Annotate().at((0, 6.2)).delta(0, 0.6).label('the exam rule: know the part numbers, the divider equation, the dropout and the efficiency')
elm.Annotate().at((0, -2.6)).delta(0, -0.6).label('and remember that a linear regulator that is too hot is a design error, not\na part that is too weak: reduce the drop or the current before adding a bigger package')
```
