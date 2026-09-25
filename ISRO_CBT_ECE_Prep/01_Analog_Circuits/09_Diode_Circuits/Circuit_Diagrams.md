# Diode Circuits — Circuit Diagrams

Companion schematics for `Concepts.md`. A diode conducts from anode to cathode once the
forward voltage exceeds roughly 0.7 V for silicon, and that single property gives
rectification, clipping, clamping, voltage multiplication and regulation.

## 1. Half-Wave Rectifier

Only one half of the cycle reaches the load, so the average output is `Vpeak/pi` for a
resistive load.

```circuit
src = elm.SourceSin().right().length(2).at((-6, 0)).label('vac', loc='left')
elm.Ground().down().at((-6, 0))
elm.Line().at((-4, 0)).right(2)
d = elm.Diode().right().length(2).at((-2, 0)).label('D', loc='top')
elm.Line().at((0, 0)).right(2).to((2, 0))
elm.Dot().at((1, 0)).label('Vout', loc='top')
rl = elm.Resistor().down().length(2).at((2, 0)).label('RL', loc='right')
elm.Ground().down().at((2, -2))
elm.Annotate().at((-6, 1.6)).delta(0, 0.6).label('one diode: the load sees only the\npositive half cycles')
elm.Annotate().at((3.5, 0.4)).delta(0, 0.6).label('Vdc = Vpeak/pi = 0.318*Vpeak\nVrms = Vpeak/2 = 0.354*Vrms_in')
elm.Annotate().at((3.5, -1.4)).delta(0, -0.6).label('ripple at the input frequency,\nand one diode drop is lost')
```

- The output ripple is at the input frequency, which is the main drawback of a half-wave
  stage.
- The diode drop shifts the whole waveform down by `0.7 V`.

## 2. Full-Wave Centre-Tap Rectifier

Both half cycles drive the load, so the ripple is at twice the input frequency and the
average is twice as large. The transformer secondary is half the required output voltage.

```circuit
xf = elm.Transformer().at((0, 0.8))
src = elm.SourceSin().up().length(2).at((-1.5, -3.2)).label('vac', loc='left')
elm.Ground().down().at((-1.5, -3.2))
elm.Line().at((-1.5, -1.2)).up(1.2)
elm.Line().at((-1.5, 2.4)).right(1.5)
elm.Line().at((1, 2.4)).right(1.5).to((2.5, 2.4))
d1 = elm.Diode().down().length(1.5).at((2.5, 2.4)).label('D1', loc='left')
elm.Line().at((1, 0.8)).right(3).to((4, 0.8))
d2 = elm.Diode().down().length(1.5).at((4, 0.8)).label('D2', loc='left')
elm.Line().at((2.5, 0.9)).down(1.6).to((2.5, -0.7))
elm.Line().at((4, -0.7)).left(1.5).to((2.5, -0.7))
elm.Dot().at((2.5, -0.7)).label('output', loc='left')
elm.Line().at((1, 1.6)).right(0.5).to((1.5, 1.6))
elm.Annotate().at((1.5, 1.6)).delta(0, 0.6).label('centre tap\n(ground)')
rl = elm.Resistor().down().length(2).at((2.5, -0.7)).label('RL', loc='right')
elm.Ground().down().at((2.5, -2.7))
elm.Annotate().at((-4.5, 1.4)).delta(0, 0.6).label('each half of the secondary must\nsupply the full output swing,\nso Vsec,rms = 2*Vout/1.414')
elm.Annotate().at((6, 1.2)).delta(0, 0.6).label('Vdc = 2*Vpeak/pi\nripple at 2*fline')
```

- Only one diode conducts at a time, so two drops appear in the loop, not one.
- A centre tap halves the transformer utilisation, which is why bridges are preferred.

## 3. Bridge Rectifier

Four diodes give the full secondary voltage to the load and need no centre tap, at the cost
of two conducting drops.

```circuit
src = elm.SourceSin().right().length(2).at((-6, 0)).label('vac', loc='left')
elm.Ground().down().at((-6, 0))
elm.Line().at((-4, 0)).right(1.5).to((-2.5, 0))
elm.Dot().at((-2.5, 0)).label('AC1', loc='bottom')
elm.Diode().up().length(1.5).at((-2.5, 0)).label('D1', loc='left')
elm.Line().at((-2.5, 1.5)).right(2.5).to((0, 1.5))
elm.Diode().down().length(1.5).at((2.5, 1.5)).label('D2', loc='right')
elm.Line().at((0, 1.5)).right(2.5).to((2.5, 1.5))
elm.Diode().up().length(1.5).at((-2.5, -1.5)).label('D3', loc='left')
elm.Line().at((-2.5, 0)).down(1.5)
elm.Line().at((0, -1.5)).left(2.5).to((-2.5, -1.5))
elm.Diode().down().length(1.5).at((2.5, 0)).label('D4', loc='right')
elm.Line().at((2.5, 0)).up(1.5)
elm.Line().at((2.5, -1.5)).left(2.5).to((0, -1.5))
elm.Dot().at((0, 1.5)).label('+ output', loc='top')
elm.Dot().at((0, -1.5)).label('- output', loc='bottom')
elm.Line().at((4, 0)).right(1.5).to((5.5, 0))
elm.Line().at((5.5, 0)).down(3).to((5.5, -3))
elm.Line().at((5.5, -3)).left(9.5).to((-4, -3))
elm.Line().at((-4, -3)).up(3)
elm.Resistor().down().length(2).at((0, 1.5)).label('RL', loc='right')
elm.Line().at((0, -0.5)).down(1).to((0, -1.5))
elm.Annotate().at((-5, 3)).delta(0, 0.6).label('during one half cycle D1 and D4 conduct;\nduring the other, D2 and D3 conduct')
elm.Annotate().at((6, 1.2)).delta(0, 0.6).label('no centre tap needed, but the\noutput is 2*0.7 = 1.4 V below\nthe secondary peak')
```

- Two diodes conduct in series in every half cycle, so the loss is `2*0.7 V` plus twice the
  diode resistance.
- In a bridge, the negative output node is *not* ground; tie it to the chassis if leakage
  matters.

## 4. Capacitor-Input Filter

A large capacitor across the load holds the peak and supplies the load current between peaks,
which is why the ripple frequency and the regulation both improve.

```circuit
src = elm.SourceSin().right().length(2).at((-7, 0)).label('vac', loc='left')
elm.Ground().down().at((-7, 0))
elm.Line().at((-5, 0)).right(2).to((-3, 0))
d = elm.Diode().right().length(2).at((-3, 0)).label('D', loc='top')
elm.Line().at((-1, 0)).right(1).to((0, 0))
elm.Dot().at((0, 0)).label('Vout', loc='top')
c = elm.Capacitor().down().length(3).at((0, 0)).label('C', loc='left')
elm.Ground().down().at((0, -3))
elm.Line().at((0, 0)).right(2).to((2, 0))
rl = elm.Resistor().down().length(1.5).at((2, 0)).label('RL', loc='right')
elm.Line().at((2, -1.5)).down(1.5).to((2, -3))
elm.Ground().down().at((2, -3))
elm.Annotate().at((4, 1.4)).delta(0, 0.6).label('the capacitor charges to the peak\non the rising edge and then\ndischarges into RL between peaks')
elm.Annotate().at((4, -1.6)).delta(0, -0.6).label('Vripple(pp) ~ Iload/(f*C)\nC >= 10*1/(2*pi*f*RL) is\na common rule of thumb')
elm.Annotate().at((-7, 1.4)).delta(0, 0.6).label('the diode conducts in narrow pulses:\npeak diode current is many\ntimes the load current')
```

- Ripple is inversely proportional to both `C` and frequency, but the diode peak current
  grows as the ripple shrinks, which stresses the diode and the transformer.
- A capacitor-input filter needs a soft-start path in switch-mode supplies to limit that
  inrush.

## 5. Clippers

A series resistor sets the current; a diode to ground removes part of the waveform by
conducting on only one polarity.

```circuit
src = elm.SourceSin().right().length(2).at((-6, 1.5)).label('Vin', loc='left')
elm.Ground().down().at((-6, 1.5))
elm.Line().at((-4, 1.5)).right(2).to((-2, 1.5))
r1 = elm.Resistor().right().length(2).at((-2, 1.5)).label('R', loc='top')
elm.Line().at((0, 1.5)).right(2.5).to((2.5, 1.5))
elm.Dot().at((1, 1.5)).label('out', loc='top')
elm.Diode().down().length(1.5).at((2.5, 1.5)).label('D', loc='right')
elm.Ground().down().at((2.5, 0))
elm.Annotate().at((4, 1.2)).delta(0, 0.6).label('negative clipper: the diode conducts\nwhen the node tries to go below\n-0.7 V, so only the tops survive')
src2 = elm.SourceSin().right().length(2).at((-6, -3.5)).label('Vin', loc='left')
elm.Ground().down().at((-6, -3.5))
elm.Line().at((-4, -3.5)).right(2).to((-2, -3.5))
r2 = elm.Resistor().right().length(2).at((-2, -3.5)).label('R', loc='bottom')
elm.Line().at((0, -3.5)).right(2.5).to((2.5, -3.5))
elm.Dot().at((1, -3.5)).label('out', loc='bottom')
elm.Diode().up().length(1.5).at((2.5, -3.5)).label('D', loc='right')
elm.Ground().down().at((2.5, -5))
elm.Annotate().at((4, -3.8)).delta(0, -0.6).label('reverse the diode to clip the positive\nside instead; a string of\ndiodes in series shifts the\nclip level by n*0.7 V')
elm.Annotate().at((-6, -0.8)).delta(0, -0.6).label('R sets the clipping current: Iclip ~ (Vin - 0.7)/R')
```

- The clipped-off region still conducts through the diode, so the resistor must be sized for
  the peak current, not the average.
- Adding a DC reference in series with the diode sets the clip level precisely.

## 6. Clampers

A series capacitor removes the DC level, and a diode with a bias restores the peak to a
chosen reference, so a small AC signal rides on top of that reference.

```circuit
src = elm.SourceSin().right().length(2).at((-7, 0)).label('vac', loc='left')
elm.Ground().down().at((-7, 0))
elm.Line().at((-5, 0)).right(2).to((-3, 0))
c = elm.Capacitor().right().length(2).at((-3, 0)).label('C', loc='top')
elm.Line().at((-1, 0)).right(1).to((0, 0))
elm.Dot().at((0, 0)).label('out', loc='top')
elm.Diode().down().length(1.5).at((0, 1.5)).label('D', loc='right')
elm.Ground().up().at((0, 1.5))
elm.Line().at((0, 0)).right(2.5).to((2.5, 0))
rl = elm.Resistor().down().length(1.5).at((2.5, 0)).label('RL', loc='right')
elm.Ground().down().at((2.5, -1.5))
elm.Annotate().at((4.5, 0.8)).delta(0, 0.6).label('positive clamper: the diode pins the\nmost negative excursion at about\n0 V, so the whole waveform shifts up\nby its peak plus one diode drop')
elm.Annotate().at((-7, 1.4)).delta(0, 0.6).label('C blocks DC; the diode conducts only on the\nhalf cycle that would push the node below 0')
elm.Annotate().at((4.5, -1.6)).delta(0, -0.6).label('reverse D and the output is clamped negative;\ninsert a battery or Vref in series to set the\nresting level to any chosen value')
```

- The capacitor must be large compared with the load: a leaky load makes the DC level drift.
- This is the DC restorer used in stage-coupled amplifiers.

## 7. Voltage Doubler

A second diode and capacitor stack a second peak on top of the first, so the output is
roughly `2*Vpeak` from a `Vpeak` input.

```circuit
src = elm.SourceSin().right().length(2).at((-7, 1)).label('vac', loc='left')
elm.Ground().down().at((-7, 1))
elm.Line().at((-5, 1)).right(2).to((-3, 1))
d1 = elm.Diode().right().length(1.5).at((-3, 1)).label('D1', loc='top')
elm.Line().at((-1.5, 1)).right(0.5).to((-1, 1))
elm.Capacitor().down().length(2).at((-1, 1)).label('C1', loc='left')
elm.Ground().down().at((-1, -1))
elm.Line().at((-1, 1)).up(0.75)
elm.Line().at((-1, 1.75)).right(2).to((1, 1.75))
d2 = elm.Diode().right().length(1.5).at((1, 1.75)).label('D2', loc='top')
elm.Line().at((2.5, 1.75)).right(0.5).to((3, 1.75))
elm.Capacitor().down().length(2.5).at((3, 1.75)).label('C2', loc='right')
elm.Ground().down().at((3, -0.75))
elm.Line().at((3, 1.75)).right(2).to((5, 1.75)).label('Vout', loc='top')
elm.Dot().at((3, 1.75))
elm.Annotate().at((0, 3.2)).delta(0, 0.6).label('on alternate half cycles D1 and D2 charge C1 and C2,\nso the two capacitor voltages add in series')
elm.Annotate().at((0, -2)).delta(0, -0.6).label('a voltage doubler costs two diodes and two capacitors but no\ntransformer: the trade is a doubling of the output ripple frequency issue\nand a poor load capability, since only C2 supplies the load')
elm.Annotate().at((6, 1.2)).delta(0, 0.6).label('Vout ~ 2*Vpeak - 2*0.7 V')
```

- Add a third and fourth section to build a multiplier; each section costs two diodes and
  two capacitors.
- The load must be light: the capacitors recharge only near the peaks, so the ripple is
  large.

## 8. Zener Shunt Regulator

The zener holds a nearly constant voltage, and the series resistor takes the difference
between the input and the zener voltage.

```circuit
vin = elm.SourceV().up().length(2).at((-6, -3)).label('Vin', loc='left')
elm.Ground().down().at((-6, -3))
elm.Line().at((-6, -1)).up(1).to((-6, 0))
r = elm.Resistor().right().length(2).at((-6, 0)).label('R', loc='top')
elm.Line().at((-4, 0)).right(4).to((0, 0))
elm.Dot().at((0, 0)).label('Vout = Vz', loc='top')
z = elm.Zener().down().length(2).at((0, 0)).label('Zener', loc='right')
elm.Ground().down().at((0, -2))
elm.Line().at((0, 0)).right(2).to((2, 0))
rl = elm.Resistor().down().length(2).at((2, 0)).label('RL', loc='right')
elm.Ground().down().at((2, -2))
elm.Annotate().at((4.5, 0.8)).delta(0, 0.6).label('R = (Vin - Vz)/(Iz + IL)\nthe smallest valid R is the one\nthat still allows Iz(min) at Vin(min)')
elm.Annotate().at((4.5, -1.6)).delta(0, -0.6).label('a zener gives poor regulation and\nwastes current, but it is the\nsimplest shunt regulator and it\nis a fine reference for small loads')
```

- `Iz(min)` is usually 5 to 10 mA; keeping above it bounds the dynamic resistance.
- The load current bypasses the zener, so the output moves by roughly
  `IL*rs + deltaVz` when the load changes.

## 9. Diode Parameters and Where They Matter (Block View)

The small-signal resistance `rd = n*Vt/Id` explains why a diode is a poor linear element and
why a zener is a poor precision reference.

```circuit
elm.Rect(corner1=(-9, 2.5), corner2=(-4, 5.5)).label('forward drop:\n0.7 V silicon,\n0.3 V germanium,\n0.2 to 0.4 V Schottky', loc='center')
elm.Line(arrow='->').at((-4, 4)).right(1.5)
elm.Rect(corner1=(-2.5, 2.5), corner2=(2.5, 5.5)).label('reverse leakage:\ntiny for silicon,\nlarge for germanium\nand Schottky', loc='center')
elm.Line(arrow='->').at((2.5, 4)).right(1.5)
elm.Rect(corner1=(4, 2.5), corner2=(9, 5.5)).label('reverse breakdown:\nfixed by the\nzener voltage\n(for a zener)', loc='center')
elm.Rect(corner1=(-9, -1.5), corner2=(-4, 1.5)).label('dynamic resistance\nrd = n*Vt/Id\n26 mV per decade of current', loc='center')
elm.Line(arrow='->').at((-4, 0)).right(1.5)
elm.Rect(corner1=(-2.5, -1.5), corner2=(2.5, 1.5)).label('junction capacitance:\nsets the switching\nspeed and the\nreverse recovery loss', loc='center')
elm.Line(arrow='->').at((2.5, 0)).right(1.5)
elm.Rect(corner1=(4, -1.5), corner2=(9, 1.5)).label('power rating:\nP = V*F*I limits the\ncurrent a rectifier\nor a zener can take', loc='center')
elm.Annotate().at((0, 6.4)).delta(0, 0.6).label('the same exponential law I = Is*(exp(Vd/nVt) - 1) explains all three of the first row')
elm.Annotate().at((0, -2.6)).delta(0, -0.6).label('rectifier design uses the forward drop, the reverse rating and the surge current;\nfast switching design uses the junction capacitance and the recovery time')
```

- Reverse recovery charge is what limits the switching frequency of a diode bridge; a
  Schottky or a SiC diode removes it.
- A zener is a **shunt** reference; a bandgap is a series-fed reference with far better
  regulation, which is why precision supplies use one.

## 10. Diode Equation and the Three Regions

The equation gives forward conduction, the reverse-leakage floor and the breakdown knee, and
it is the fastest way to estimate a bias point.

```circuit
elm.Line().at((-3, 0)).right(7)
elm.Line().at((0, -2.5)).up(5)
elm.Line().at((-3, 0)).up(1.875)
elm.Line().at((-3, 1.875)).right(1.5)
elm.Line().at((-1.5, 1.875)).up(0.625).to((-1.5, 2.5))
elm.Line().at((1.5, 1.875)).up(0.625).to((1.5, 2.5))
elm.Line().at((-1.5, 2.5)).right(3)
elm.Line().at((0, 0)).right(3)
elm.Dot().at((0.5, 0)).label('knee', loc='bottom')
elm.Annotate().at((0, 1.2)).delta(0, 0.6).label('+Id  exponential rise, roughly 60 mV per decade')
elm.Annotate().at((-2.2, 0.6)).delta(0, 0.6).label('tiny leakage,\nthe reverse direction')
elm.Annotate().at((2.4, 0.6)).delta(0, 0.6).label('breakdown:\ncurrent rises\nsteeply')
elm.Annotate().at((0, 3.2)).delta(0, 0.6).label('I = Is*(exp(Vd/(n*Vt)) - 1):  n is 1 to 2, Vt is 26 mV at room temperature')
elm.Annotate().at((0, -3.4)).delta(0, -0.6).label('a forward-biased diode is a poor amplifier because rd is only tens of ohms\nat a few milliamps: that is why amplifiers use devices with a gm')
```

## 11. Summary of Diode Applications

| Application | Diodes | Key parameter |
|---|---|---|
| Half-wave rectifier | 1 | forward drop, reverse voltage rating |
| Centre-tap full wave | 2 | transformer ratio, two drops in series |
| Bridge rectifier | 4 | two drops, no centre tap |
| Clipper / limiter | 1 or a string | clip level `n*0.7 V`, series resistor |
| Clamper / DC restorer | 1 + 1 capacitor | capacitor size versus load |
| Voltage doubler | 2 + 2 capacitors | light load only |
| Zener shunt regulator | 1 + resistor | `Vz`, `Iz(min)`, zener current limit |
| Temperature sensing | 1 | forward drop falls about 2 mV per degree |
