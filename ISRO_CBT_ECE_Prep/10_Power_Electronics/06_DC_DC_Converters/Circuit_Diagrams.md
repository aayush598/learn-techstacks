# Circuit Diagrams

## 1. Buck Converter

The switch applies the input to the inductor during the on-time. The freewheel diode provides a current path during the off-time, while the output capacitor supports a nearly constant load voltage.

```circuit
elm.SourceV().up().at((-4, -2)).label("V_in", loc="left")
elm.Line().up(1).at((-4, 1))
elm.Switch().right().at((-4, 2)).label("Q1", loc="top")
elm.Dot().at((-2, 2)).label("switch node", loc="top")
elm.Inductor().right().at((-2, 2)).label("L", loc="top")
elm.Dot().at((1, 2)).label("V_out", loc="top")
elm.Capacitor().down().at((1, 2)).label("C", loc="right")
elm.Line().right(1).at((1, 2)).dot()
elm.Resistor().down().at((2, 2)).label("R_L", loc="right")
elm.Line().down(3).at((2, -1))
elm.Line().down(2).at((1, 0))
elm.Diode().down().at((-2, 1)).label("D freewheel", loc="right")
elm.Line().down(2).at((-2, 0))
elm.Line().left(6).at((2, -2)).to((-4, -2))
```

## 2. Boost Converter

The inductor stores energy while the switch is on. In the off interval the diode transfers that stored energy to the output, so the output can exceed the input voltage.

```circuit
elm.SourceV().up().at((-4, -2)).label("V_in", loc="left")
elm.Line().up(1).at((-4, 1))
elm.Inductor().right().at((-4, 2)).label("L", loc="top")
elm.Dot().at((-1, 2)).label("switch node", loc="top")
elm.Switch().down().at((-1, 2)).label("Q1", loc="right")
elm.Line().down(1).at((-1, -1))
elm.Line().right(2).at((-1, 2)).to((1, 2))
elm.Diode().up().at((1, 2)).label("D boost", loc="right")
elm.Line().up(1).at((1, 3))
elm.Line().up(1).at((1, 4)).label("V_out", loc="right")
elm.Capacitor().down().at((1, 4)).label("C", loc="right")
elm.Line().right(1).at((1, 4)).dot()
elm.Resistor().down().at((2, 4)).label("R_L", loc="right")
elm.Line().down(6).at((2, -2))
elm.Line().left(6).at((2, -2)).to((-4, -2))
```

## 3. Inverting Buck-Boost Converter

The inductor stores energy during switch on-state, and the coupling action transfers it to the output with reversed polarity during the off-state. The diode and output capacitor support the negative output.

```circuit
elm.SourceV().up().at((-5, -2)).label("V_in", loc="left")
elm.Line().up(1).at((-5, 1))
elm.Switch().right().at((-5, 2)).label("Q1", loc="top")
elm.Dot().at((-3, 2)).label("switch node", loc="top")
elm.Inductor().right().at((-3, 2)).label("L", loc="top")
elm.Dot().at((0, 2)).label("V_out", loc="right")
elm.Diode().down().at((0, 2)).label("D", loc="right")
elm.Line().down(2).at((0, 0))
elm.Capacitor().down().at((2, 2)).label("C", loc="right")
elm.Line().right(2).at((0, 2))
elm.Resistor().down().at((2, 2)).label("R_L", loc="right")
elm.Line().down(4).at((2, -2))
elm.Line().left(2).at((0, -2)).to((0, 0))
elm.Line().left(7).at((0, -2)).to((-5, -2))
```

## 4. Cuk Converter

The Cuk converter transfers energy through an intermediate capacitor while using two inductors. Its output polarity is inverted, and the series capacitor blocks a steady DC component.

```circuit
elm.SourceV().up().at((-6, -2)).label("V_in", loc="left")
elm.Line().up(1).at((-6, 1))
elm.Switch().right().at((-6, 2)).label("Q1", loc="top")
elm.Dot().at((-4, 2)).label("node A", loc="top")
elm.Inductor().right().at((-4, 2)).label("L1", loc="top")
elm.Dot().at((-1, 2)).label("series node", loc="top")
elm.Capacitor().right().at((-1, 2)).label("C_coupling", loc="top")
elm.Dot().at((2, 2)).label("node B", loc="top")
elm.Inductor().right().at((2, 2)).label("L2", loc="top")
elm.Dot().at((5, 2)).label("V_out", loc="right")
elm.Switch().down().at((-4, 2)).label("Q2", loc="right")
elm.Diode().up().reverse().at((2, 2)).label("D2", loc="right")
elm.Capacitor().down().at((5, 2)).label("C_out", loc="right")
elm.Line().right(1).at((5, 2)).dot()
elm.Resistor().down().at((6, 2)).label("R_L", loc="right")
elm.Line().down(4).at((6, -2))
elm.Line().left(12).at((5, -2)).to((-6, -2))
elm.Line().up(2).at((-4, -2)).to((-4, 0))
elm.Line().up(2).at((2, -2)).to((2, 0))
```

## 5. SEPIC Converter

The SEPIC converter combines a series coupling capacitor with two inductors. It can step up or down while keeping the output polarity inverted relative to the input.

```circuit
elm.SourceV().up().at((-6, -2)).label("V_in", loc="left")
elm.Line().up(1).at((-6, 1))
elm.Inductor().right().at((-6, 2)).label("L1", loc="top")
elm.Dot().at((-3, 2)).label("node A", loc="top")
elm.Capacitor().right().at((-3, 2)).label("C_sep", loc="top")
elm.Dot().at((0, 2)).label("node B", loc="top")
elm.Switch().down().at((-3, 2)).label("Q1", loc="right")
elm.Diode().up().at((0, 2)).label("D", loc="right")
elm.Inductor().right().at((0, 2)).label("L2", loc="top")
elm.Dot().at((3, 2)).label("V_out", loc="right")
elm.Capacitor().down().at((3, 2)).label("C_out", loc="right")
elm.Line().right(1).at((3, 2)).dot()
elm.Resistor().down().at((4, 2)).label("R_L", loc="right")
elm.Line().down(4).at((4, -2))
elm.Line().left(10).at((3, -2)).to((-6, -2))
elm.Line().up(2).at((-3, -2)).to((-3, 0))
elm.Line().up(2).at((0, -2)).to((0, 0))
```

## 6. Full-Bridge DC Converter

Two bridge legs apply opposite voltage polarities across the load. PWM and switching state selection determine the average output voltage and whether power flows into or out of the load.

```circuit
elm.SourceV().up().at((-6, -3)).label("V_dc", loc="left")
elm.Line().up(6).at((-6, 3))
elm.Line().right(9).at((-6, 3)).label("DC +", loc="top")
elm.Line().right(9).at((-6, -3)).label("DC -", loc="bottom")
elm.Switch().down().at((-3, 3)).label("Q1", loc="right")
elm.Switch().down().at((-3, 0)).label("Q2", loc="right")
elm.Dot().at((-3, 0)).label("out A", loc="left")
elm.Switch().down().at((3, 3)).label("Q3", loc="right")
elm.Switch().down().at((3, 0)).label("Q4", loc="right")
elm.Dot().at((3, 0)).label("out B", loc="right")
elm.Motor().right().at((-1, 0)).label("load", loc="bottom")
elm.Line().left(2).at((3, 0)).to((1, 0))
```

## 7. Push-Pull Converter

Two primary switches drive alternate half-cycles, and the center-tapped secondary rectifies both halves. The two secondary diodes prevent the two transistor voltages from being applied in series to the load.

```circuit
elm.SourceV().up().at((0, -2)).label("drive", loc="left")
elm.Line().up(1).at((0, -1)).dot()
elm.Switch().up().at((-1, -1)).label("Q1", loc="right")
elm.Switch().up().at((1, -1)).label("Q2", loc="left")
elm.Line().up(2).at((-1, 1))
elm.Line().up(2).at((1, 1))
elm.Line().left(1).at((-1, 3))
elm.Line().right(1).at((1, 3))
elm.Line().right(3).at((-1, 4)).label("coupled primary", loc="top")
elm.Diode().right().at((2, 4)).label("D1", loc="top")
elm.Diode().right().reverse().at((2, 2)).label("D2", loc="bottom")
elm.Line().right(2).at((5, 4))
elm.Line().down(2).at((5, 2))
elm.Line().right(1).at((5, 3)).label("V_out", loc="right")
elm.Line().down(3).at((0, -2)).to((0, 0))
```

## 8. Isolated Flyback Converter

The primary switch stores energy in the magnetizing inductance. During the off interval, the secondary diode rectifies the coupled flux into a DC output, while the transformer provides galvanic isolation.

```circuit
elm.SourceV().up().at((-5, -2)).label("V_dc", loc="left")
elm.Switch().right().at((-5, 1)).label("Q1 primary", loc="top")
elm.Inductor().right().at((-3, 1)).label("magnetizing L", loc="top")
elm.Line().right(1).at((0, 1))
elm.Line().right(1).at((0, 1)).label("magnetic core", loc="top")
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
