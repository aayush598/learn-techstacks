# Oscillators — Circuit Diagrams

Companion schematics for `Concepts.md`. An oscillator is a feedback loop with no signal
input: the loop must satisfy the **Barkhausen criterion** `|A*beta| = 1` at a single
frequency, with the *right* phase, and the startup condition `|A*beta| > 1` at DC so the
oscillation grows until limiting sets in.

## 1. Barkhausen Criterion (Block View)

Two conditions, not one: the magnitude must be exactly one and the phase must be an
integer multiple of 360 degrees.

```circuit
elm.Rect(corner1=(-8, -1.5), corner2=(-4, 1.5)).label('amplifier\ngain A', loc='center')
elm.Rect(corner1=(-8, 3), corner2=(-4, 6)).label('frequency-selective\nnetwork, feedback\nfactor beta', loc='center')
elm.Line(arrow='->').at((-8, 0)).left(2)
elm.SourceSin().left().length(2).at((-10, 0)).label('sustain', loc='left')
elm.Line(arrow='->').at((-4, 0)).right(2)
elm.Dot().at((-2, 0))
elm.Line().at((-2, 0)).down(3).to((-2, -3))
elm.Line().at((-2, -3)).left(1.5)
elm.Line(arrow='->').at((-3.5, -3)).up(3.5).to((-3.5, 0.5))
elm.Annotate().at((-6, 7)).delta(0, 0.6).label('(1) magnitude: |A(jw0)*beta(jw0)| = 1')
elm.Annotate().at((-6, 6.4)).delta(0, 0.6).label('(2) phase: angle A + angle beta = 0 (mod 360)')
elm.Annotate().at((1, 0.4)).delta(0, 0.6).label('only one frequency satisfies both:\nthe oscillation frequency is f0')
elm.Annotate().at((1, -3.6)).delta(0, -0.6).label('any other frequency is not fed back in phase,\nso it is not sustained')
```

- The feedback network is always the frequency-selective part; without selectivity the loop
  amplifies noise across the whole band.
- `beta` sets the frequency, `A` sets the amplitude: the nonlinear limiting mechanism sets
  the output level.

## 2. Startup and Steady State

Real oscillators run the loop gain slightly above one at low frequency so that noise grows,
then let the nonlinearity pull it back to one.

```circuit
elm.Line().at((0, 0)).right(9)
elm.Line().at((0, 0)).up(4)
elm.Line().at((0.5, 0.5)).right(1.5)
elm.Line().at((2, 0.5)).to((4, 3.5))
elm.Line().at((4, 3.5)).to((6, 0.75))
elm.Line().at((6, 0.75)).to((8.5, 0.25))
elm.Line().at((0.5, 1.25)).right(8)
elm.Annotate().at((1.5, 3.9)).delta(0, 0.6).label('open-loop gain: rises, then falls at the poles')
elm.Annotate().at((5, 1.25)).delta(0, 0.6).label('loop gain T = A*b: > 1 at low frequency, exactly 1 at f0')
elm.Annotate().at((8.5, 0.25)).delta(0, 0.6).label('T < 1 at high frequency:\nall other noise is rejected')
elm.Rect(corner1=(-7, 1.5), corner2=(-3, 4)).label('startup:\nT(0) > 1, or the\noscillation never\nbegins', loc='center')
elm.Rect(corner1=(-7, -2.5), corner2=(-3, 0)).label('steady state:\nT(f0) = 1, limited by\nA saturation, a lamp,\nthermal drift or an\nAGC loop', loc='center')
elm.Annotate().at((0, -3.4)).delta(0, -0.6).label('A lamp or back-to-back diodes in the feedback path are the classic amplitude limiters')
```

- Failure to start is almost always a loop-gain or phase problem at low frequency, not a
  problem at `f0`.
- Amplitude limiting must be slow compared with `f0` and fast compared with the drift that
  would otherwise change the level.

## 3. Wien Bridge Oscillator

The positive-feedback network passes only a narrow band around `1/(2*pi*RC)` and returns
exactly one third of the output, so the amplifier gain must be 3.

```circuit
op = elm.Opamp(leads=True).right().at((0, 0))
elm.Line().at((0, -0.625)).left(2).to((-2, -0.625))
rg = elm.Resistor().down().length(1.25).at((-2, -0.625)).label('R', loc='left')
elm.Ground().down().at((-2, -1.875))
rf = elm.Resistor().up().length(3).at((3.4151, 0)).label('2R', loc='right')
elm.Line().at((3.4151, 3)).right(2).to((5.4151, 3)).label('Vout', loc='top')
elm.Line().at((5.4151, 3)).down(3)
elm.Line().at((5.4151, 0)).down(1.875)
elm.Line().at((5.4151, -1.875)).left(7.4151).to((-2, -1.875))
elm.Dot().at((-2, -1.875)).label('gain network node', loc='left')
elm.Line().at((0, 0.625)).left(2.5).to((-2.5, 0.625))
elm.Dot().at((0, 0.625)).label('bridge node', loc='top')
cp = elm.Capacitor().down().length(1.25).at((-2.5, 0.625)).label('C  (parallel)', loc='left')
elm.Ground().down().at((-2.5, -0.625))
rp = elm.Resistor().down().length(1.25).at((-1.5, 0.625)).label('R  (parallel)', loc='right')
elm.Ground().down().at((-1.5, -0.625))
elm.Line().at((0, 0.625)).up(0.875)
elm.Capacitor().right().length(1.5).at((0, 1.5)).label('C  (series)', loc='top')
elm.Resistor().right().length(1.5).at((1.5, 1.5)).label('R  (series)', loc='bottom')
elm.Line().at((3, 1.5)).right(2).to((5, 1.5))
elm.Line().at((5, 1.5)).down(1.5)
elm.Dot().at((5, 0))
elm.Annotate().at((-6, 2.4)).delta(0, 0.6).label('series R-C and parallel R||C:\nbeta(f0) = 1/3 with zero phase shift')
elm.Annotate().at((7, 1.2)).delta(0, 0.6).label('f0 = 1/(2*pi*R*C)\nA must be 3, so Rf = 2*Rg')
```

- The gain must be slightly **more** than 3 to start, and a lamp or AGC brings it back to
  exactly 3.
- Equal `R` and `C` in both arms is what makes the phase exactly zero at one frequency.

## 4. RC Phase-Shift Oscillator

Three identical RC sections contribute 60 degrees each, so the loop phase reaches 180
degrees and the amplifier provides the other 180.

```circuit
r1 = elm.Resistor().right().length(1.5).at((0, 0)).label('R', loc='bottom')
elm.Line().at((1.5, 0)).right(0.5).to((2, 0))
r2 = elm.Resistor().right().length(1.5).at((2, 0)).label('R', loc='bottom')
elm.Line().at((3.5, 0)).right(0.5).to((4, 0))
r3 = elm.Resistor().right().length(1.5).at((4, 0)).label('R', loc='bottom')
elm.Line().at((5.5, 0)).right(1.5).label('to the amplifier input', loc='right')
c1 = elm.Capacitor().down().length(1.5).at((1.5, 0)).label('C', loc='left')
elm.Ground().down().at((1.5, -1.5))
c2 = elm.Capacitor().down().length(1.5).at((3.5, 0)).label('C', loc='left')
elm.Ground().down().at((3.5, -1.5))
c3 = elm.Capacitor().down().length(1.5).at((5.5, 0)).label('C', loc='left')
elm.Ground().down().at((5.5, -1.5))
elm.Line().at((0, 0)).left(1.5)
elm.Dot().at((-1.5, 0)).label('from the amplifier output', loc='left')
elm.Annotate().at((2, 2.4)).delta(0, 0.6).label('each section shifts about 60 degrees at f0,\nso three sections give the 180 needed\nto cancel the amplifier inversion')
elm.Annotate().at((2, -2.6)).delta(0, -0.6).label('f0 = 1/(2*pi*R*C*sqrt(6)) for three equal sections,\nand the amplifier gain must exceed 29')
```

- The gain requirement of about 29 is high, and the sections load each other, so the
  amplitude is less stable than in a Wien bridge.
- A buffered version of each section gives a lower gain requirement and cleaner amplitude.

## 5. Colpitts Oscillator

A capacitive divider taps a fraction of the tank voltage back to the emitter, so the loop
gain exceeds one on every cycle.

```circuit
q = elm.BjtNpn().at((0, 0))
src = elm.SourceSin().right().length(1.5).at((-4, 0)).label('drive', loc='left')
elm.Ground().down().at((-4, 0))
elm.Line().at((-2.5, 0)).right(1.5).to((-1, 0))
cin = elm.Capacitor().right().length(1).at((-2.5, 0)).label('Cin', loc='top')
elm.Dot().at((-1, 0)).label('base', loc='bottom')
rb = elm.Resistor().down().length(1.25).at((-1, 0)).label('Rb', loc='left')
elm.Ground().down().at((-1, -1.25))
elm.Line().at((-1, 0)).right(1).to((0, 0))
elm.Line().at((0.75167, 0.69667)).up(0.80333)
elm.Dot().at((0.75167, 1.5)).label('collector node', loc='right')
elm.Line().at((0.75167, 1.5)).right(3.24833).to((4, 1.5))
c1 = elm.Capacitor().down().length(1.5).at((2, 1.5)).label('C1', loc='left')
elm.Ground().down().at((2, 0))
l1 = elm.Inductor().down().length(2.5).at((4, 1.5)).label('L', loc='right')
elm.Line().at((4, -1)).left(3.24833).to((0.75167, -1))
elm.Line().at((0.75167, -0.69667)).down(0.30333)
elm.Dot().at((0.75167, -1)).label('emitter node', loc='right')
c2 = elm.Capacitor().down().length(1.5).at((0.75167, -1)).label('C2', loc='left')
elm.Ground().down().at((0.75167, -2.5))
elm.Annotate().at((-6, 1.6)).delta(0, 0.6).label('the C1/C2 divider feeds a fraction of the tank\nvoltage to the emitter, so the stage repeats\nin phase with the tank voltage')
elm.Annotate().at((6, 1.2)).delta(0, 0.6).label('f0 = 1/(2*pi*sqrt(L*C1*C2))\nstartup needs gm*Rp > 1, where Rp is\nthe ac resistance seen at the emitter')
```

- The tap ratio sets the feedback fraction; it is a trade between startup margin and
  harmonic content.
- A Hartley oscillator is the same circuit with an inductive divider instead of `C1`/`C2`.

## 6. Hartley Oscillator

Replacing the capacitive divider with a tapped inductor gives higher impedance and better
energy storage at the same frequency.

```circuit
q = elm.BjtNpn().at((0, 0))
rb = elm.Resistor().down().length(1.25).at((-1, 0)).label('Rb', loc='left')
elm.Line().at((-1, 0)).right(1).to((0, 0))
elm.Dot().at((-1, 0)).label('base', loc='bottom')
elm.Ground().down().at((-1, -1.25))
src = elm.SourceSin().right().length(1.5).at((-4, 0)).label('drive', loc='left')
elm.Ground().down().at((-4, 0))
elm.Capacitor().right().length(1).at((-2.5, 0)).label('Cin', loc='top')
elm.Line().at((-1.5, 0)).right(0.5)
elm.Line().at((0.75167, 0.69667)).up(0.80333)
elm.Dot().at((0.75167, 1.5)).label('collector node', loc='right')
elm.Line().at((0.75167, 1.5)).right(3.24833).to((4, 1.5))
c1 = elm.Capacitor().down().length(1.5).at((2, 1.5)).label('C', loc='left')
elm.Ground().down().at((2, 0))
l1 = elm.Inductor().down().length(1.25).at((4, 1.5)).label('L1', loc='right')
l2 = elm.Inductor().down().length(1.25).at((4, 0.25)).label('L2', loc='right')
elm.Dot().at((4, 0.25)).label('tap to the base', loc='right')
elm.Line().at((4, -1)).left(3.24833).to((0.75167, -1))
elm.Line().at((0.75167, -0.69667)).down(0.30333)
elm.Dot().at((0.75167, -1)).label('emitter node', loc='right')
elm.Ground().down().at((0.75167, -1))
elm.Line().at((4, 0.25)).right(2).to((6, 0.25))
elm.Line().at((6, 0.25)).down(3.75).to((6, -3.5))
elm.Line().at((6, -3.5)).left(6).to((0, -3.5))
elm.Line(arrow='->').at((0, -3.5)).up(3.5)
elm.Annotate().at((7.5, -1.2)).delta(0, -0.6).label('the tap ratio sets the feedback fraction:\nf0 = 1/(2*pi*sqrt(Ltotal*C))')
```

- A tapped inductor gives a higher tank impedance than a capacitive divider, so it is easier
  to start and quieter.
- Mutual coupling between the two sections is unwanted; keep them apart physically or use a
  single tapped winding.

## 7. Clapp Oscillator

Adding a third capacitor in series with the inductor makes the frequency depend mainly on
`C3`, which is stable and easy to trim.

```circuit
elm.Line().at((-4, 0)).right(8)
elm.Dot().at((-4, 0)).label('collector node', loc='top')
c1 = elm.Capacitor().down().length(1.5).at((-2, 0)).label('C1', loc='left')
elm.Ground().down().at((-2, -1.5))
elm.Line().at((0, 0)).right(1.5)
c3 = elm.Capacitor().right().length(1.5).at((0, 0)).label('C3 (trim)', loc='top')
l1 = elm.Inductor().right().length(1.5).at((1.5, 0)).label('L', loc='bottom')
elm.Line().at((3, 0)).right(1).to((4, 0))
elm.Dot().at((4, 0)).label('emitter node', loc='top')
c2 = elm.Capacitor().down().length(1.5).at((4, 0)).label('C2', loc='right')
elm.Ground().down().at((4, -1.5))
elm.Annotate().at((0, 2.4)).delta(0, 0.6).label('C3 in series with L dominates the frequency:\nf0 = 1/(2*pi*sqrt(L*C3)) with only a small\nC1-C2 correction')
elm.Annotate().at((0, -2.8)).delta(0, -0.6).label('C3 is a low-value, high-stability part (often a trimmer or a\nsmall mica), so the frequency is stable against the\nlarger, more temperature-sensitive C1 and C2')
```

- The correction from `C1` and `C2` is second order in `1/C3`, which is what makes the Clapp
  frequency so stable.
- The added element also improves the loaded `Q` of the tank, giving a cleaner sine.

## 8. Crystal Equivalent Circuit

A crystal is a high-`Q` mechanical resonator: a motional branch in series with a parallel
shunt capacitance.

```circuit
r1 = elm.Resistor().right().length(1.5).at((0, 1)).label('R1 (ESR)', loc='bottom')
c0 = elm.Capacitor().right().length(1.5).at((1.5, 2)).label('C0', loc='top')
elm.Line().at((1.5, 1)).up(1)
elm.Dot().at((1.5, 1))
elm.Line().at((3, 2)).down(1)
elm.Dot().at((3, 1))
l1 = elm.Inductor().right().length(1.5).at((3, 1)).label('L1', loc='bottom')
c2 = elm.Capacitor().right().length(1.5).at((1.5, -1)).label('C2 (holder)', loc='bottom')
elm.Line().at((1.5, -1)).up(2)
elm.Dot().at((1.5, 1))
elm.Line().at((3, -1)).up(2)
elm.Dot().at((3, 1))
elm.Line().at((4.5, 1)).right(1.5).label('pin 2', loc='right')
elm.Line().at((0, 1)).left(1.5)
elm.Dot().at((-1.5, 1)).label('pin 1', loc='left')
elm.Annotate().at((1, 3.2)).delta(0, 0.6).label('motional branch: a very high Q resonator at fs,\nso only a narrow frequency range is reinforced')
elm.Annotate().at((1, -2.4)).delta(0, -0.6).label('C2 is the stray capacitance of the holder and leads;\nwith C1 it sets the load seen by the crystal')
```

- Near `fs` the motional impedance is small, so the network behaves like a low loss and the
  loop gain peaks sharply at `fs`.
- The high `Q` gives excellent frequency stability but a slow start-up, so the oscillator
  needs extra loop gain.

## 9. Crystal Oscillator (Pierce, Block View)

The crystal sits in the feedback path with a phase inversion, and bias resistors set the DC
operating point on the correct side of the negative-resistance curve.

```circuit
elm.Rect(corner1=(-9, -1.5), corner2=(-5, 1.5)).label('inverting\namplifier', loc='center')
elm.Line(arrow='->').at((-5, 0)).right(2)
elm.Rect(corner1=(-3, -1.5), corner2=(1, 1.5)).label('phase network\n(C1, C2)', loc='center')
elm.Line(arrow='->').at((1, 0)).right(2)
elm.Rect(corner1=(3, -1.5), corner2=(7, 1.5)).label('crystal\nbetween its\nanti-resonant\npoint and fs', loc='center')
elm.Line(arrow='->').at((7, 0)).right(1.5)
elm.Line().at((8.5, 0)).down(2.25).to((8.5, -2.25))
elm.Line(arrow='->').at((8.5, -2.25)).left(15.5).to((-7, -2.25))
elm.Line(arrow='->').at((-7, -2.25)).up(2.25)
elm.Rect(corner1=(-2, 3), corner2=(2, 5.5)).label('Rb1', loc='center')
elm.Rect(corner1=(4, 3), corner2=(8, 5.5)).label('Rb2 (sets dc\nbias level)', loc='center')
elm.Line().at((0, 3)).down(1.5)
elm.Line().at((6, 3)).down(1.5)
elm.Annotate().at((3, 6.4)).delta(0, 0.6).label('the crystal must see negative resistance to start;\nRb2 sets that level and also the drive amplitude')
elm.Annotate().at((3, -3.4)).delta(0, -0.6).label('total loop phase is 360 degrees only at the crystal frequency:\nthe amplifier and the network provide 180 plus 180')
```

- Excess drive heats the crystal and shifts its frequency; keep the drive current small.
- A series or parallel cut, a TCXO or an oven is the usual answer when the frequency must
  hold over temperature.

## 10. Choosing an Oscillator

| Type | Frequency range | Stability | Notes |
|---|---|---|---|
| Relaxation (Schmitt + RC) | audio to a few hundred kHz | poor with RC, good with a divider | easy, distorted square wave |
| Wien bridge | 1 Hz to about 100 kHz | medium | sine, needs amplitude control |
| RC phase shift | 1 kHz to 100 kHz | poor | high gain requirement, buffered version is better |
| Colpitts / Clapp | RF, MHz to GHz | poor with a discrete tank, good with a crystal | workhorse for RF |
| Crystal (Pierce) | 10 kHz to 100 MHz | very good | slow start, strong temperature dependence without ovening |
