# Circuit Diagrams

## 1. Half-Wave Uncontrolled Rectifier

One diode and one load form the simplest rectifier. The output repeats at the input frequency and contains a DC component plus ripple.

```circuit
elm.SourceSin().up().at((-3, 0)).label("v_s", loc="left")
elm.Diode().right().at((-3, 3)).label("D1", loc="top")
elm.Line().right(2).at((0, 3))
elm.Dot().at((2, 3)).label("v_o", loc="right")
elm.Resistor().down().at((2, 3)).label("R_L", loc="right")
elm.Line().down(3).at((2, 0))
elm.Line().left(5).at((2, -3))
elm.Line().up(3).at((-3, -3)).to((-3, 0))
```

## 2. Center-Tapped Full-Wave Rectifier

Each half of the secondary conducts on alternate half-cycles through one diode. Two diode drops appear in each output pulse when both devices are included in the current path.

```circuit
elm.SourceSin().up().at((0, 0)).label("upper secondary", loc="left")
elm.Diode().up().at((0, 3)).label("D1", loc="right")
elm.Line().up(1).at((0, 4))
elm.SourceSin().up().at((3, 0)).label("lower secondary", loc="left")
elm.Diode().up().reverse().at((3, 3)).label("D2", loc="right")
elm.Line().up(1).at((3, 4))
elm.Line().right(3).at((0, 5))
elm.Line().left(3).at((3, 5)).to((0, 5))
elm.Resistor().down().at((6, 5)).label("R_L", loc="right")
elm.Line().down(3).at((6, 2))
elm.Line().left(6).at((6, -1))
elm.Line().up(2).at((0, -1)).to((0, 0))
elm.Line().right(3).at((0, -1)).to((3, -1))
elm.Line().up(2).at((3, -1)).to((3, 0))
```

## 3. Single-Phase Bridge Rectifier

The bridge uses four diodes and provides a full-wave load voltage without a center-tapped secondary. The two conducting diodes produce two forward drops per half-cycle.

```circuit
elm.SourceSin().up().at((0, 0)).label("AC", loc="left")
elm.Diode().up().at((0, 3)).label("D1", loc="right")
elm.Line().up(1).at((0, 4))
elm.Line().right(7).at((0, 5)).label("positive", loc="top")
elm.Line().right(2).at((0, 0))
elm.Diode().up().at((2, 0)).label("D2", loc="right")
elm.Line().up(4).at((2, 1))
elm.Line().left(2).at((2, 5))
elm.Line().right(4).at((0, -2))
elm.Diode().up().at((4, -2)).label("D3", loc="right")
elm.Line().up(5).at((4, -1)).to((0, 3))
elm.Line().right(1).at((0, -2))
elm.Diode().up().at((1, -2)).label("D4", loc="right")
elm.Line().up(2).at((1, -1)).to((0, 0))
elm.Resistor().down().at((7, 5)).label("R_L", loc="right")
elm.Line().down(7).at((7, -2))
elm.Line().left(7).at((0, -2)).label("negative", loc="bottom")
```

## 4. Three-Phase Half-Wave Rectifier

At any instant, the phase with the highest instantaneous voltage supplies the positive output through its diode. The negative bus is the common neutral connection.

```circuit
elm.SourceSin().up().at((0, -2)).label("phase R", loc="left")
elm.Diode().up().at((0, 1)).label("D_R", loc="right")
elm.Line().up(2).at((0, 2))
elm.SourceSin().up().at((2, -2)).label("phase Y", loc="left")
elm.Diode().up().at((2, 1)).label("D_Y", loc="right")
elm.Line().up(2).at((2, 2))
elm.SourceSin().up().at((4, -2)).label("phase B", loc="left")
elm.Diode().up().at((4, 1)).label("D_B", loc="right")
elm.Line().up(2).at((4, 2))
elm.Line().right(3).at((0, 4)).to((6, 4)).label("positive DC", loc="top")
elm.Resistor().down().at((6, 4)).label("R_L", loc="right")
elm.Line().down(6).at((6, -2))
elm.Line().left(6).at((0, -2)).label("neutral return", loc="bottom")
```

## 5. Three-Phase Six-Pulse Bridge

A six-pulse bridge selects one upper diode and one lower diode for each 60-degree commutation interval. The resulting ripple frequency is six times the AC frequency.

```circuit
elm.SourceSin().up().at((-4, 0)).label("R", loc="left")
elm.SourceSin().up().at((0, 0)).label("Y", loc="left")
elm.SourceSin().up().at((4, 0)).label("B", loc="left")
elm.Diode().up().at((-4, 3)).label("upper R", loc="right")
elm.Diode().up().at((0, 3)).label("upper Y", loc="right")
elm.Diode().up().at((4, 3)).label("upper B", loc="right")
elm.Line().right(4).at((-4, 4)).label("DC +", loc="top")
elm.Diode().up().reverse().at((-4, -1)).label("lower R", loc="right")
elm.Diode().up().reverse().at((0, -1)).label("lower Y", loc="right")
elm.Diode().up().reverse().at((4, -1)).label("lower B", loc="right")
elm.Line().right(4).at((-4, -2)).label("DC -", loc="bottom")
elm.Resistor().down().at((8, 4)).label("load", loc="right")
elm.Line().right(2).at((-4, 4)).to((8, 4))
elm.Line().down(6).at((8, -2))
elm.Line().right(4).at((8, 4))
elm.Line().down(2).at((8, 2))
```

## 6. Capacitor-Smoothed DC Output

A reservoir capacitor supplies load current between rectifier charging peaks. The diode conducts in short intervals when the rectified source exceeds the capacitor voltage.

```circuit
elm.SourceSin().up().at((-4, -3)).label("v_s", loc="left")
elm.Diode().right().at((-4, 0)).label("D1", loc="top")
elm.Line().right(4).at((-1, 0))
elm.Dot().at((1, 0)).label("v_dc", loc="right")
elm.Capacitor().down().at((1, 0)).label("C reservoir", loc="right")
elm.Resistor().down().at((4, 0)).label("R_L", loc="right")
elm.Line().down(3).at((1, -3))
elm.Line().down(3).at((4, -3))
elm.Line().left(8).at((1, -3))
elm.Line().up(3).at((-4, -3))
```

## 7. Rectifier with Zener Regulation

The reservoir capacitor reduces ripple, while the Zener clamps the output near its rated voltage under the available load current. The series resistor limits Zener current.

```circuit
elm.SourceSin().up().at((-5, -3)).label("AC", loc="left")
elm.Diode().right().at((-5, 0)).label("D1", loc="top")
elm.Line().right(3).at((-2, 0))
elm.Dot().at((1, 0)).label("V_out", loc="right")
elm.Capacitor().down().at((1, 0)).label("C", loc="right")
elm.Resistor().right().at((1, 0)).label("R series", loc="top")
elm.Zener().down().at((4, 0)).label("Zener", loc="right")
elm.Line().down(3).at((1, -3))
elm.Line().down(3).at((4, -3))
elm.Line().left(9).at((1, -3))
elm.Line().up(3).at((-5, -3))
elm.Line().right(2).at((1, 0)).label("load", loc="right")
```
