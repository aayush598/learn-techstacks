# Active Loads & CMOS Amplifiers — Circuit Diagrams

Companion schematics for `Concepts.md`. A resistor load wastes signal current and gives
only `RL` of load resistance; an **active load** (a current mirror) gives a resistance of
order `1/gds`, so the same current produces a much larger gain.

## 1. Resistive Load Versus Active Load

The same branch current through a resistor gives `V = I*RL`; through a mirror it gives
`V = I*ro`, and `ro` is typically 100 kΩ or more.

```circuit
elm.Rect(corner1=(-9, 1), corner2=(-4, 4)).label('resistive load\nVout = I*RL\nRL of 5 kOhm', loc='center')
elm.Line(arrow='->').at((-4, 2.5)).right(1.5)
elm.Rect(corner1=(-2.5, 1), corner2=(2.5, 4)).label('current-mirror load\nVout = I*ro\nro of 100 kOhm', loc='center')
elm.Line(arrow='->').at((2.5, 2.5)).right(1.5)
elm.Rect(corner1=(4, 1), corner2=(9, 4)).label('same stage, same current,\nmuch larger voltage gain', loc='center')
elm.Rect(corner1=(-9, -4), corner2=(-4, -1)).label('drain current sets\nthe operating point', loc='center')
elm.Line(arrow='->').at((-4, -2.5)).right(1.5)
elm.Rect(corner1=(-2.5, -4), corner2=(2.5, -1)).label('resistor needs Vds headroom\nand burns V^2/R', loc='center')
elm.Line(arrow='->').at((2.5, -2.5)).right(1.5)
elm.Rect(corner1=(4, -4), corner2=(9, -1)).label('mirror needs Vds,sat headroom\nand no power at zero signal', loc='center')
elm.Annotate().at((0, 4.8)).delta(0, 0.6).label('gain per stage rises by roughly the ratio ro/RL, which is often 20 to 100x')
elm.Annotate().at((0, -4.8)).delta(0, -0.6).label('the price: less output swing, tighter headroom and a poor output drive into a low load')
```

## 2. NMOS Current Mirror

The reference device is diode-connected, so its `Vgs` sets the gate voltage and the second
device copies the current exactly when `Vds` values match.

```circuit
q1 = elm.NMos().at((0, 1))
q2 = elm.NMos().at((2, 1))
elm.Line().at((0, 1)).up(0.75)
elm.Vdd().at((0, 1.75)).label('VDD')
elm.Line().at((0, 1)).down(1.16667).to((0, -0.16667))
elm.Dot().at((0, 1)).label('diode connected', loc='left')
elm.Dot().at((0, -0.16667)).label('gate node', loc='left')
elm.Line().at((-0.8333, -0.16667)).right(2)
elm.Dot().at((1.16667, -0.16667))
elm.Line().at((2, 1)).up(0.75)
elm.Dot().at((2, 1.75)).label('Iout mirror', loc='right')
elm.Line().at((2, 1.75)).right(2)
elm.Annotate().at((4, 1.75)).delta(0, 0.6).label('output current node\n(load or next stage)')
elm.Line().at((0, -0.66667)).down(0.83333)
elm.Vss().at((0, -1.5)).label('VSS')
elm.Line().at((2, -0.66667)).down(0.83333)
elm.Vss().at((2, -1.5)).label('VSS')
iref = elm.SourceI().down().length(1.5).at((-2, 1.33333))
elm.Line().at((-2, -0.16667)).down(1.5)
elm.Line().at((-2, 1.33333)).left(2).label('IREF', loc='left')
elm.Line().at((-0.8333, -0.16667)).left(1.1667)
elm.Annotate().at((-5.5, -0.8)).delta(0, -0.6).label('both devices share Vgs, so\nIout = IREF when the two Vds\nare equal (the reference branch)')
```

- `Iout = IREF * (W/L)_2 / (W/L)_1` for matched `Vds`.
- Output resistance is `ro`, so compliance only needs `Vds >= Vds,sat`.

## 3. PMOS Current Mirror

The same idea with the polarity reversed; the sources sit at the positive rail.

```circuit
m1 = elm.PMos().at((0, 2))
m2 = elm.PMos().at((2, 2))
elm.Line().at((0, 2)).up(0.75)
elm.Vdd().at((0, 2.75)).label('VDD')
elm.Line().at((0, 0.33333)).up(1.16667)
elm.Dot().at((0, 0.33333)).label('diode connected', loc='left')
elm.Dot().at((0, 1.5)).label('gate node', loc='left')
elm.Line().at((-0.8333, 1.5)).right(2)
elm.Dot().at((1.16667, 1.5))
elm.Line().at((2, 0.33333)).down(0.83333)
elm.Dot().at((2, -0.5)).label('Iout mirror', loc='right')
elm.Line().at((2, -0.5)).right(2)
elm.Annotate().at((4, -0.5)).delta(0, 0.6).label('output current node\n(load or next stage)')
elm.Line().at((0, 2)).right(2)
elm.Line().at((2, 2)).right(2)
elm.Line().at((2, 2.75)).right(0.5)
elm.Vdd().at((2.75, 2.75)).label('VDD')
iref = elm.SourceI().up().length(1.5).at((-2, -0.5))
elm.Line().at((-2, 1)).up(1.5)
elm.Line().at((-2, 1)).left(2).label('IREF', loc='left')
elm.Line().at((-0.8333, 1.5)).left(1.1667)
elm.Annotate().at((-5.5, 0.2)).delta(0, -0.6).label('the current is mirrored downward\nthrough the output device')
```

- A PMOS mirror has a lower `ro` than a matched NMOS mirror at the same current, because
  hole mobility is lower.
- A PMOS mirror also suffers body effect if its sources are not tied to the rail.

## 4. Cascode Current Mirror

Stacking a second device on top raises the output resistance to `gm*ro^2`, at the cost of
`2*Vds,sat` of compliance.

```circuit
q1 = elm.NMos().at((0, 1))
q2 = elm.NMos().at((0, 3))
q3 = elm.NMos().at((2, 1))
q4 = elm.NMos().at((2, 3))
elm.Line().at((0, 1)).up(0.33333)
elm.Dot().at((0, 1.33333)).label('stacked source node', loc='left')
elm.Line().at((2, 1)).up(0.33333)
elm.Dot().at((2, 1.33333))
elm.Line().at((0, 3)).up(0.75)
elm.Vdd().at((0, 3.75)).label('VDD')
elm.Line().at((2, 3)).up(0.75)
elm.Dot().at((2, 3.75)).label('Iout', loc='right')
elm.Line().at((2, 3.75)).right(2)
elm.Line().at((0, 1)).up(1.16667)
elm.Line().at((0, 0.16667)).right(2)
elm.Dot().at((0, 0.16667)).label('diode connection', loc='left')
elm.Dot().at((1.16667, 0.16667))
elm.Line().at((-0.8333, 0.16667)).left(1.1667)
elm.Line().at((-0.8333, 1.83333)).right(2)
elm.Dot().at((1.16667, 1.83333))
elm.Line().at((-0.8333, 1.83333)).left(1.5)
elm.Annotate().at((-5.5, 1.83333)).delta(0, 0.6).label('cascode bias')
elm.Line().at((0, -0.66667)).down(0.83333)
elm.Vss().at((0, -1.5)).label('VSS')
elm.Line().at((2, -0.66667)).down(0.83333)
elm.Vss().at((2, -1.5)).label('VSS')
elm.Annotate().at((5, 3.1)).delta(0, 0.6).label('Rout is now about gm*ro^2, so the mirror\nis a much better current source\nbut it needs twice the compliance')
elm.Annotate().at((5, -1.6)).delta(0, -0.6).label('cascode bias must track the supply: a\nself-biased cascode is preferred for\nsupply-independent behaviour')
```

- The cascode device must stay saturated, so the bias voltage is not arbitrary.
- With the cascode gate at a constant voltage the mirror becomes supply-independent, which
  is what analog design usually wants.

## 5. Common-Source Stage With an Active Load

This is the basic CMOS gain stage: the NMOS input device and the PMOS mirror load share the
drain node, so the full mirror current swing appears as output voltage.

```circuit
m_in = elm.NMos().at((0, 0))
m_load = elm.PMos().at((0, 2.5))
m_ref = elm.PMos().at((2, 2.5))
elm.Line().at((0, 2.5)).up(0.75)
elm.Vdd().at((0, 3.25)).label('VDD')
elm.Line().at((0, 0.83333)).down(0.83333)
elm.Dot().at((0, 0)).label('drain node / Vout', loc='top')
elm.Line().at((0, 0)).right(2.5)
elm.Annotate().at((2.5, 0)).delta(0, 0.6).label('output')
elm.Line().at((-0.8333, -1.16667)).left(2.1667)
elm.Dot().at((-3, -1.16667)).label('Vin', loc='left')
src = elm.SourceSin().right().length(1.5).at((-6, -1.16667)).label('input', loc='left')
elm.Ground().down().at((-6, -1.16667))
elm.Line().at((-4.5, -1.16667)).right(1.5)
elm.Line().at((0, -1.66667)).down(0.83333)
elm.Vss().at((0, -2.5)).label('VSS')
elm.Line().at((-0.8333, 2)).right(2)
elm.Dot().at((1.16667, 2))
elm.Line().at((2, 0.83333)).right(1)
elm.Line().at((3, 0.83333)).up(1.16667)
elm.Line().at((3, 2)).left(4.1667).to((-1.1667, 2))
elm.Dot().at((3, 2))
elm.Dot().at((2, 0.83333)).label('reference diode', loc='right')
elm.Line().at((2, 2.5)).up(0.75)
elm.Vdd().at((2, 3.25)).label('VDD')
iref = elm.SourceI().down().length(1.5).at((-3, 3.5))
elm.Line().at((-3, 2)).up(1.5)
elm.Line().at((-3, 2)).right(2.1667)
elm.Annotate().at((-3, 2)).label('IREF', loc='left')
elm.Annotate().at((-6, 1.2)).delta(0, 0.6).label('the mirror converts its own current\nvariation into a voltage swing at\nthe drain, so gain is gm*(ro_n||ro_p)')
elm.Annotate().at((4, 0.6)).delta(0, 0.6).label('single-ended output:\nthe common-source gain plus\nthe current-mirror gain')
```

- Voltage gain is `gm_n * (ro_n || ro_p)`, which is why a mirror load is worth its extra
  devices.
- The output is single-ended; a differential pair with a mirror load doubles the gain and
  cancels common-mode terms.

## 6. Gain and Output Swing of the Active-Loaded Stage

The gain rises with `gm` and with the output resistance, while the swing falls as the
headroom is spent.

```circuit
elm.Line().at((0, 0)).right(9)
elm.Line().at((0, 0)).up(4)
elm.Line().at((0.5, 3.5)).right(8)
elm.Line().at((0.5, 1.75)).right(8)
elm.Line().at((0.5, 0.5)).right(8)
elm.Annotate().at((4.5, 3.5)).delta(0, 0.6).label('ideal gain: gm*ro, limited in practice by the cascode')
elm.Annotate().at((4.5, 1.75)).delta(0, 0.6).label('realistic for a simple mirror load')
elm.Annotate().at((4.5, 0.5)).delta(0, 0.6).label('resistive load, for comparison')
elm.Annotate().at((0, -1)).delta(0, -0.6).label('larger ro means a smaller output current for the same swing,')
elm.Annotate().at((0, -1.6)).delta(0, -0.6).label('so the bias current goes down as the gain goes up')
elm.Rect(corner1=(-8, 1.5), corner2=(-5, 4)).label('headroom: one\nVds,sat for the\nNMOS, one for the\nPMOS plus its\nVds,sat', loc='center')
elm.Line().at((-5, 2.75)).right(5)
elm.Annotate().at((-6.5, 0.6)).delta(0, -0.6).label('the mirror costs the output\nrange that the resistors\nwould have used for bias')
```

## 7. CMOS Inverter as a Linear Amplifier

An inverter biased in the middle of its transfer curve is a voltage amplifier with a gain
near `-gm*R`, limited by both output devices.

```circuit
n = elm.NMos().at((0, 0))
p = elm.PMos().at((0, 3))
elm.Line().at((0, 3)).up(0.75)
elm.Vdd().at((0, 3.75)).label('VDD')
elm.Line().at((0, 1.33333)).down(1.33333)
elm.Dot().at((0, 0)).label('Vout', loc='top')
elm.Line().at((0, 0)).right(2.5)
elm.Annotate().at((2.5, 0)).delta(0, 0.6).label('output')
elm.Line().at((-0.8333, -1.16667)).left(2.1667)
elm.Dot().at((-3, -1.16667)).label('Vin', loc='left')
src = elm.SourceSin().right().length(1.5).at((-6, -1.16667)).label('input', loc='left')
elm.Ground().down().at((-6, -1.16667))
elm.Line().at((-4.5, -1.16667)).right(1.5)
elm.Line().at((-0.8333, 2.5)).left(2.1667)
elm.Dot().at((-3, 2.5)).label('Vbias: the trip point', loc='left')
vbs = elm.SourceV().up().length(2).at((-6, 0.5))
elm.Ground().down().at((-6, 0.5))
elm.Line().at((-6, 2.5)).up(2)
elm.Line().at((-4.5, 2.5)).right(1.5)
elm.Line().at((0, -1.66667)).down(0.83333)
elm.Vss().at((0, -2.5)).label('VSS')
elm.Annotate().at((4, 1.6)).delta(0, 0.6).label('gain is negative: the inverter adds 180 degrees,\nso a two-stage design is stable as an amplifier')
elm.Annotate().at((4, -1.6)).delta(0, -0.6).label('the PMOS contributes gain too,\nso Av is roughly -(gm_n + gm_p)*ro')
```

- Biasing at the trip point sets the quiescent current and therefore the gain.
- Common-mode range is tiny and the output swing is limited, so this is a teaching circuit
  rather than a practical one.

## 8. Source Follower (Common Drain)

The follower keeps the voltage gain near one but gives a low output impedance, which is
what a source or bias network needs.

```circuit
n = elm.NMos().at((0, 0))
elm.Line().at((-0.8333, -1.16667)).left(2.1667)
elm.Dot().at((-3, -1.16667)).label('Vin', loc='left')
src = elm.SourceSin().right().length(1.5).at((-6, -1.16667)).label('input', loc='left')
elm.Ground().down().at((-6, -1.16667))
elm.Line().at((-4.5, -1.16667)).right(1.5)
elm.Line().at((0, -1.66667)).down(0.83333)
elm.Vss().at((0, -2.5)).label('VSS')
elm.Line().at((0, 0)).right(3)
elm.Dot().at((1, 0)).label('bias tap', loc='top')
elm.Line().at((3, 0)).right(1.5)
rb = elm.Resistor().up().length(1.5).at((4.5, 0)).label('R to VDD', loc='right')
elm.Vdd().at((4.5, 1.5)).label('VDD')
elm.Line().at((1, 0)).up(0.75)
rl = elm.Capacitor().down().length(1.5).at((1, 0.75)).label('load', loc='right')
elm.Line().at((1, -0.75)).down(0.5)
elm.Ground().down().at((1, -1.25))
elm.Annotate().at((6.5, 0.2)).delta(0, 0.6).label('Rout = 1/(gm + gds)\nAv = gm*RL/(gm + gds)\ncurrent gain is large')
elm.Annotate().at((-4, 1.4)).delta(0, 0.6).label('the body effect lowers\nthe gain, because the\nsource moves away\nfrom the substrate')
```

- `Rout` is `1/gm` in parallel with `ro`, which is why a follower drives a low-resistance
  load easily.
- The follower costs one threshold of headroom and cannot swing to the negative rail.

## 9. Small-Signal Model (Block View)

The drain current of a MOS device is a voltage-controlled current source between drain and
source, with `ro` in parallel and the gate drawing no current.

```circuit
elm.Line().at((-6, 2)).right(2)
elm.Dot().at((-4, 2)).label('drain', loc='top')
elm.Line().at((2, 2)).right(2)
elm.Dot().at((4, 2)).label('source', loc='top')
elm.Rect(corner1=(-1.5, 1.5), corner2=(1.5, 2.5)).label('gm*Vgs', loc='center')
elm.Line(arrow='->').at((-4, 2)).right(2.5)
elm.Line().at((-4, 2)).up(1.5).to((-4, 3.5))
elm.Dot().at((-4, 3.5)).label('gate', loc='bottom')
elm.Line().at((-4, 2)).down(1.5)
elm.Resistor().down().length(1.5).at((-4, 2)).label('ro', loc='left')
elm.Line().at((-4, 0.5)).down(0.5)
elm.Ground().down().at((-4, 0))
elm.Line().at((2, 2)).down(1.5)
elm.Resistor().down().length(1.5).at((2, 2)).label('ro', loc='right')
elm.Line().at((2, 0.5)).down(0.5)
elm.Ground().down().at((2, 0))
elm.Annotate().at((-7, 1.2)).delta(0, -0.6).label('gate current is zero:\nthe device is voltage controlled,\nnot current controlled')
elm.Annotate().at((5, 1.2)).delta(0, -0.6).label('ro = 1/(lambda*I), so it grows with\ncurrent and falls with a short channel\nor a long channel design')
elm.Annotate().at((-1, 4.2)).delta(0, 0.6).label('the same model with a BJT: base current Ib and gm*Vbe')
```

## 10. Trade-Offs Summary

| Choice | Gain | Output swing | Output drive | Complexity |
|---|---|---|---|---|
| Resistive load | low | full | poor | lowest |
| NMOS mirror load | high | reduced | poor | two devices |
| PMOS mirror load | high | reduced | poor | two devices, worse `ro` |
| Cascode mirror load | very high | less | poor | four devices plus a bias |
| Source follower | unity | minus one threshold | good | one device plus a bias |
