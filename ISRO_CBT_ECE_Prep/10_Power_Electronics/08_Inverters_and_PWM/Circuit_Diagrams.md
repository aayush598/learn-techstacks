# Circuit Diagrams

## 1. Single-Phase Half-Bridge Inverter

The two switch positions connect the output midpoint alternately to the upper and lower DC rails. The output alternates between approximately positive and negative DC levels.

```circuit
elm.SourceV().up().at((-5, -3)).label("V_dc", loc="left")
elm.Line().up(6).at((-5, 3))
elm.Line().right(8).at((-5, 3)).label("DC +", loc="top")
elm.Line().right(8).at((-5, -3)).label("DC -", loc="bottom")
elm.Switch().down().at((-2, 3)).label("Q1", loc="right")
elm.Dot().at((-2, 0)).label("out A", loc="left")
elm.Switch().up().at((3, -3)).label("Q2", loc="right")
elm.Dot().at((3, 0)).label("out B", loc="right")
elm.SourceSin().up().at((0, -3)).label("v_ac", loc="left")
elm.Line().right(2).at((0, 0)).to((3, 0))
elm.Line().left(2).at((0, 0)).to((-2, 0))
```

## 2. Full-Bridge Square-Wave Inverter

Opposite diagonal switch pairs are turned on to apply either polarity across the load. The square-wave fundamental has a frequency set by the switching pattern.

```circuit
elm.SourceV().up().at((-5, 0)).label("V_dc", loc="left")
elm.Line().up(3).at((-5, 3))
elm.Line().right(8).at((-5, 3)).label("DC +", loc="top")
elm.Line().right(8).at((-5, -3)).label("DC -", loc="bottom")
elm.Switch().down().at((-2, 3)).label("Q1", loc="right")
elm.Switch().down().at((-2, 0)).label("Q2", loc="right")
elm.Dot().at((-2, 0)).label("A", loc="left")
elm.Switch().down().at((3, 3)).label("Q3", loc="right")
elm.Switch().down().at((3, 0)).label("Q4", loc="right")
elm.Dot().at((3, 0)).label("B", loc="right")
elm.Motor().right().at((-1, 0)).label("AC load", loc="bottom")
elm.Line().right(2).at((3, 0)).to((2, 0))
```

## 3. Modified Square-Wave Output

A stepped switching waveform uses multiple positive and negative levels to reduce the low-order harmonic content compared with a single-level square wave. The source symbols represent the available output levels.

```circuit
elm.SourceV().up().at((-4, -2)).label("-V", loc="left")
elm.SourceV().up().at((-4, 1)).label("0", loc="left")
elm.SourceV().up().at((-4, 4)).label("+V", loc="left")
elm.Line().right(3).at((-4, -2))
elm.Line().right(3).at((-4, 1))
elm.Line().right(3).at((-4, 4))
elm.Arrow().right().at((0, -2)).to((4, -2)).label("negative interval", loc="top")
elm.Arrow().right().at((0, 1)).to((4, 1)).label("zero interval", loc="top")
elm.Arrow().right().at((0, 4)).to((4, 4)).label("positive interval", loc="top")
```

## 4. Unipolar PWM

One bridge leg is held at a reference while the other is modulated between the two rails. The output therefore switches among two levels but has a controllable average value.

```circuit
elm.SourceSin().right().at((-5, 2)).label("reference", loc="left")
elm.SourceSin().right().at((-5, -2)).label("carrier", loc="left")
elm.Dot().at((0, 0)).label("comparator", loc="right")
elm.Line().right(2).at((-3, 2)).to((0, 2))
elm.Line().right(2).at((-3, -2)).to((0, -2))
elm.Line().up(2).at((0, -2)).to((0, 2))
elm.Arrow().right().at((0, 0)).to((4, 0)).label("PWM duty", loc="top")
elm.Arrow().right().at((4, 0)).to((7, 0)).label("one leg", loc="top")
elm.Line().down(2).at((4, 0))
elm.Line().left(9).at((4, -2))
elm.Line().up(2).at((-5, -2)).to((-5, 0))
```

## 5. Bipolar PWM

Both bridge legs are modulated together with opposite commands. The load voltage switches between the two rail polarities on every carrier transition.

```circuit
elm.SourceSin().right().at((-5, 2)).label("reference", loc="left")
elm.SourceSin().right().at((-5, -2)).label("triangle", loc="left")
elm.Dot().at((0, 0)).label("modulator", loc="right")
elm.Line().right(2).at((-3, 2)).to((0, 2))
elm.Line().right(2).at((-3, -2)).to((0, -2))
elm.Line().up(2).at((0, -2)).to((0, 2))
elm.Arrow().right().at((0, 0)).to((3, 0)).label("PWM A", loc="top")
elm.Arrow().right().at((3, -1)).to((6, -1)).label("PWM B complementary", loc="top")
elm.Line().down(1).at((0, 0)).to((0, -1))
elm.Line().right(3).at((0, -1)).to((3, -1))
```

## 6. Three-Phase Two-Level Voltage-Source Inverter

Three bridge legs create three phase voltages with 120-degree displaced references. The switching states synthesize a balanced voltage for a motor or other AC load.

```circuit
elm.SourceV().up().at((-6, 0)).label("V_dc", loc="left")
elm.Line().up(3).at((-6, 3))
elm.Line().right(12).at((-6, 3)).label("DC +", loc="top")
elm.Line().right(12).at((-6, -3)).label("DC -", loc="bottom")
elm.Switch().down().at((-3, 3)).label("Q1", loc="right")
elm.Switch().down().at((-3, 0)).label("Q2", loc="right")
elm.Dot().at((-3, 0)).label("phase A", loc="left")
elm.Switch().down().at((0, 3)).label("Q3", loc="right")
elm.Switch().down().at((0, 0)).label("Q4", loc="right")
elm.Dot().at((0, 0)).label("phase B", loc="left")
elm.Switch().down().at((3, 3)).label("Q5", loc="right")
elm.Switch().down().at((3, 0)).label("Q6", loc="right")
elm.Dot().at((3, 0)).label("phase C", loc="left")
elm.Motor().right().at((-2, 0)).label("three-phase load", loc="bottom")
elm.Line().right(2).at((3, 0)).to((1, 0))
```

## 7. Space-Vector PWM Reference

The reference vector is resolved into active switching vectors within the current sector. The dwell times are selected to match the sampled reference voltage.

```circuit
elm.Line().right(4).at((-4, 0)).label("V1", loc="left")
elm.Line().right(4).at((-4, 0)).to((0, 0))
elm.Line().right(4).at((0, 0)).label("V2", loc="top")
elm.Arrow().right().at((0, 0)).to((3, 3)).label("Vref", loc="top")
elm.Dot().at((0, 0)).label("sector", loc="left")
elm.Line().up(3).at((3, 0)).to((3, 3))
elm.Line().left(3).at((3, 3)).to((0, 3))
elm.Line().down(3).at((0, 3)).to((0, 0))
elm.Line().right(4).at((0, -2)).label("V0 and V7 dwell", loc="bottom")
```

## 8. Current-Source Inverter

A current-source inverter uses a large DC-link inductor to maintain current. Commutating switches reverse the current path through the AC-side bridge.

```circuit
elm.SourceV().up().at((-5, 0)).label("V_dc", loc="left")
elm.Inductor().right().at((-5, 3)).label("large L", loc="top")
elm.Dot().at((-2, 3)).label("I_dc", loc="right")
elm.Switch().right().at((-2, 3)).label("commutator", loc="top")
elm.Diode().right().at((1, 3)).label("D1", loc="top")
elm.Diode().up().reverse().at((4, 0)).label("D2", loc="right")
elm.Diode().down().at((4, 3)).label("D3", loc="right")
elm.SourceI().up().at((4, 0)).label("i_ac", loc="right")
elm.Line().down(3).at((4, -3))
elm.Line().left(9).at((4, -3)).to((-5, -3))
elm.Line().up(3).at((-5, -3)).to((-5, 0))
elm.Line().right(2).at((-2, 3)).to((1, 3))
```

