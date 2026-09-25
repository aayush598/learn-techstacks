# Circuit Diagrams

## 1. Series Pass Linear Regulator

A pass transistor places a controlled voltage drop between input and output. The feedback amplifier adjusts the pass element to keep the output near its reference despite input or load variation.

```circuit
elm.SourceV().up().at((-4, -2)).label("V_in", loc="left")
elm.Line().up(1).at((-4, 1))
elm.Switch().up().at((-4, 2)).label("pass element", loc="right")
elm.Line().up(1).at((-4, 4))
elm.Dot().at((-4, 4)).label("V_out", loc="right")
elm.Resistor().down().at((-4, 4)).label("R_L", loc="right")
elm.Line().down(6).at((-4, -2))
elm.Arrow().left().at((0, 4)).to((-3, 4)).label("feedback", loc="top")
elm.SourceV().up().at((0, 2)).label("V_ref", loc="right")
elm.Line().right(2).at((0, 3)).label("error amplifier controls pass drive", loc="right")
```

## 2. Shunt Linear Regulator

The series element limits current and the shunt element diverts excess current to maintain the output. Simple shunt regulation wastes input current, so it is mainly used for small loads and reference circuits.

```circuit
elm.SourceV().up().at((-3, -2)).label("V_in", loc="left")
elm.Resistor().up().at((-3, 1)).label("R series", loc="left")
elm.Dot().at((-3, 4)).label("V_out", loc="right")
elm.Resistor().down().at((-3, 4)).label("R_L", loc="right")
elm.Zener().down().at((-3, 4)).label("Zener", loc="right")
elm.Line().down(6).at((-3, -2))
elm.Line().left(3).at((-3, -2))
elm.Line().up(2).at((-6, -2)).to((-6, 0))
elm.Line().right(3).at((-6, 0)).to((-3, 0))
```

## 3. Fixed Three-Terminal Regulator

A series resistor limits input current, the regulator IC controls the output voltage, and capacitors provide stability and transient current. The labeled line is the IC's functional power path.

```circuit
elm.SourceV().up().at((-4, -3)).label("V_in", loc="left")
elm.Line().up(3).at((-4, 0))
elm.Resistor().right().at((-4, 0)).label("R_in", loc="top")
elm.Line().right(2).at((-1, 0))
elm.Dot().at((1, 0)).label("V_out", loc="right")
elm.Line().right(1).at((1, 0))
elm.Line().label("fixed regulator IC", loc="top")
elm.Line().right(1).at((2, 0)).dot()
elm.Capacitor().down().at((2, 0)).label("C_out", loc="right")
elm.Resistor().down().at((4, 0)).label("R_L", loc="right")
elm.Line().down(3).at((2, -3))
elm.Line().down(3).at((4, -3))
elm.Line().left(8).at((2, -3))
elm.Line().up(3).at((-4, -3))
elm.Line().right(1).at((1, 0))
```

## 4. Linear Dissipation versus Switched Transfer

A linear regulator reduces voltage by dissipating the difference as heat. A switching converter transfers energy through inductors, capacitors, and switches, reducing the power that must be dissipated as heat.

```circuit
elm.SourceV().up().at((-5, 0)).label("input", loc="left")
elm.Line().up(2).at((-5, 2)).label("linear series pass", loc="top")
elm.Resistor().right().at((-3, 2)).label("heat", loc="top")
elm.Line().right(3).at((0, 2)).label("regulated output", loc="right")
elm.SourceV().up().at((3, 0)).label("input", loc="left")
elm.Line().up(2).at((3, 2)).label("switched converter", loc="top")
elm.Inductor().right().at((1, 2)).label("L", loc="top")
elm.Diode().right().at((4, 2)).label("switch path", loc="top")
elm.Capacitor().down().at((7, 2)).label("C", loc="right")
elm.Line().right(2).at((5, 2)).to((7, 2))
elm.Line().down(2).at((7, 0))
elm.Line().left(12).at((7, 0)).to((-5, 0))
elm.Line().up().at((-5, 0)).to((-5, 2))
elm.Line().up().at((3, 0)).to((3, 2))
```

## 5. Buck-Derived SMPS

The switch and freewheel diode feed an LC output filter. Feedback changes the duty ratio so the regulated DC output remains above the switch-device drop margin.

```circuit
elm.SourceV().up().at((-4, -2)).label("V_in", loc="left")
elm.Line().up(1).at((-4, 1))
elm.Switch().right().at((-4, 2)).label("Q", loc="top")
elm.Dot().at((-2, 2)).label("pulse node", loc="top")
elm.Inductor().right().at((-2, 2)).label("L", loc="top")
elm.Dot().at((1, 2)).label("V_out", loc="right")
elm.Capacitor().down().at((1, 2)).label("C", loc="right")
elm.Line().right(1).at((1, 2)).dot()
elm.Resistor().down().at((2, 2)).label("R_L", loc="right")
elm.Diode().down().at((-2, 1)).label("D", loc="right")
elm.Line().down(2).at((-2, 0))
elm.Line().left(6).at((2, -2)).to((-4, -2))
elm.Line().down(4).at((2, -2))
elm.Arrow().left().at((1, 0)).to((-1, 0)).label("feedback controls duty", loc="bottom")
```

## 6. Boost-Derived SMPS

The switch charges the inductor and the diode transfers energy to the output capacitor. Feedback changes the duty ratio to regulate a higher output voltage.

```circuit
elm.SourceV().up().at((-4, -2)).label("V_in", loc="left")
elm.Inductor().right().at((-4, 1)).label("L", loc="top")
elm.Dot().at((-1, 1)).label("switch node", loc="top")
elm.Switch().down().at((-1, 1)).label("Q", loc="right")
elm.Diode().up().at((1, 1)).label("D", loc="right")
elm.Line().up(2).at((1, 3)).label("V_out", loc="right")
elm.Capacitor().down().at((1, 3)).label("C", loc="right")
elm.Line().right(1).at((1, 3)).dot()
elm.Resistor().down().at((2, 3)).label("R_L", loc="right")
elm.Line().left(6).at((2, -2)).to((-4, -2))
elm.Line().up(1).at((-1, 1)).to((1, 1))
elm.Line().up(1).at((-1, 0))
elm.Arrow().left().at((1, 0)).to((-1, 0)).label("feedback controls duty", loc="bottom")
```

## 7. Isolated Flyback SMPS

The primary switch stores energy in the magnetizing inductance during on-time. During off-time the secondary diode rectifies the coupled energy into a DC output across the load.

```circuit
elm.SourceV().up().at((-5, -2)).label("V_in", loc="left")
elm.Switch().right().at((-5, 1)).label("primary Q", loc="top")
elm.Inductor().right().at((-3, 1)).label("primary L", loc="top")
elm.Line().right(1).at((0, 1))
elm.Line().right(1).at((0, 1)).label("isolated magnetic core", loc="top")
elm.Inductor().right().at((1, 1)).label("secondary L", loc="top")
elm.Diode().right().at((4, 1)).label("secondary D", loc="top")
elm.Line().right(1).at((7, 1))
elm.Capacitor().down().at((7, 1)).label("C_out", loc="right")
elm.Line().right(1).at((7, 1)).dot()
elm.Resistor().down().at((8, 1)).label("R_L", loc="right")
elm.Line().down(3).at((8, -2))
elm.Line().left(4).at((5, -2))
elm.Line().up(3).at((5, -2)).to((5, 1))
elm.Line().left(10).at((-5, -2)).to((5, -2))
```

## 8. Isolated Forward Converter

A primary switch applies a reduced-amplitude pulse train to the magnetizing winding. The secondary diode rectifies the coupled pulse while the output inductor and capacitor smooth the load current.

```circuit
elm.SourceV().up().at((-5, -2)).label("V_in", loc="left")
elm.Switch().right().at((-5, 1)).label("Q primary", loc="top")
elm.Inductor().right().at((-3, 1)).label("primary winding", loc="top")
elm.Line().right(1).at((0, 1))
elm.Line().right(1).at((0, 1)).label("magnetic core", loc="top")
elm.Inductor().right().at((1, 1)).label("secondary winding", loc="top")
elm.Diode().right().at((4, 1)).label("D1", loc="top")
elm.Inductor().right().at((7, 1)).label("output L", loc="top")
elm.Dot().at((10, 1)).label("V_out", loc="right")
elm.Capacitor().down().at((10, 1)).label("C_out", loc="right")
elm.Line().right(1).at((10, 1)).dot()
elm.Resistor().down().at((11, 1)).label("R_L", loc="right")
elm.Line().down(3).at((11, -2))
elm.Line().left(16).at((11, -2)).to((-5, -2))
elm.Line().left(3).at((7, 1)).to((4, 1))
```

