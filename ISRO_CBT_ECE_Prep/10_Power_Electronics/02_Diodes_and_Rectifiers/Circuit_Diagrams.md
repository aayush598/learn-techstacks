# Circuit Diagrams

## 1. Half-Wave Rectifier

Only one half-cycle places forward bias on the diode, so the output is a positive half-wave. A smoothing capacitor is omitted here to expose the basic rectified waveform.

```circuit
elm.SourceSin().up().at((-3, 0)).label("v_ac", loc="left")
elm.Diode().right().at((-3, 3)).label("D1", loc="top")
elm.Line().right(2).at((0, 3))
elm.Dot().at((2, 3)).label("v_dc", loc="right")
elm.Resistor().down().at((2, 3)).label("R_L", loc="right")
elm.Line().down(3).at((2, 0))
elm.Line().left(5).at((2, -3))
elm.Line().up(3).at((-3, -3)).to((-3, 0))
```

## 2. Full-Wave Bridge Rectifier

Two diodes conduct on each AC half-cycle, so the load current always flows in the same direction. The bridge output is the positive difference between the two AC terminals.

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
elm.Line().down(3).at((7, 2))
elm.Line().down(4).at((7, -2))
elm.Line().left(7).at((0, -2))
elm.Dot().at((0, -2)).label("negative", loc="bottom")
```

## 3. Bridge Current Paths

The AC source is between the two bridge midpoints, and the load is between the positive and negative rails. Diode pairs D1-D4 and D2-D3 provide the two half-cycle current paths.

```circuit
elm.Line().right(2).at((-4, 2)).label("AC A", loc="left")
elm.Line().right(2).at((-4, -2)).label("AC B", loc="left")
elm.Diode().right().at((-2, 2)).label("D1", loc="top")
elm.Line().right(2).at((1, 2))
elm.Line().up(2).at((1, 2))
elm.Line().right(2).at((1, 4)).label("+", loc="right")
elm.Diode().right().reverse().at((-2, -2)).label("D4", loc="bottom")
elm.Line().right(2).at((1, -2))
elm.Line().up(2).at((1, -2))
elm.Line().right(2).at((1, 0)).label("-", loc="right")
elm.Diode().right().at((-2, 0)).label("D2", loc="top")
elm.Diode().right().reverse().at((1, 0)).label("D3", loc="bottom")
elm.Line().down(2).at((3, 4))
elm.Line().down(2).at((3, 0))
elm.Line().left().at((3, 2)).label("load", loc="bottom")
```

## 4. Capacitor-Input Filter

The diode conducts near each input peak and rapidly recharges the capacitor. The load then discharges the capacitor between peaks, reducing output ripple.

```circuit
elm.SourceSin().up().at((-4, -3)).label("v_ac", loc="left")
elm.Diode().right().at((-4, 0)).label("D1", loc="top")
elm.Line().right(5).at((-1, 0))
elm.Dot().at((1, 0)).label("v_dc", loc="right")
elm.Resistor().down().at((1, 0)).label("R_L", loc="right")
elm.Capacitor().down().at((3, 0)).label("C filter", loc="right")
elm.Line().down(3).at((1, -3))
elm.Line().down(3).at((3, -3))
elm.Line().left(7).at((1, -3))
elm.Line().up(3).at((-4, -3))
```

## 5. Zener Shunt Regulator

When the output reaches the Zener voltage, the diode conducts in reverse breakdown and diverts current. The series resistor sets the available regulator current.

```circuit
elm.SourceV().up().at((0, 0)).label("V_in", loc="left")
elm.Resistor().right().at((0, 3)).label("R series", loc="top")
elm.Dot().at((3, 3)).label("V_out", loc="right")
elm.Zener().down().at((3, 3)).label("Zener", loc="right")
elm.Line().down(3).at((3, 0))
elm.Line().left(3).at((3, 0)).to((0, 0))
elm.Line().right(2).at((3, 3)).label("regulated load", loc="right")
```

## 6. Full-Wave Voltage Doubler

The two diode-capacitor charge paths accumulate voltage so that the output is approximately twice the peak AC input under light load. The labels identify the AC source and the two stored charge nodes.

```circuit
elm.SourceSin().up().at((-3, -2)).label("v_ac", loc="left")
elm.Diode().up().at((-3, 1)).label("D1", loc="right")
elm.Line().up(1).at((-3, 2))
elm.Capacitor().down().at((-3, 2)).label("C1", loc="right")
elm.Line().down().at((-3, 0)).to((-3, 0))
elm.Line().right(3).at((-3, 3))
elm.Diode().up().at((0, 2)).label("D2", loc="right")
elm.Line().up(1).at((0, 3))
elm.Capacitor().down().at((0, 3)).label("C2", loc="right")
elm.Line().right(3).at((0, 4)).label("2 x peak", loc="right")
elm.Line().left(3).at((-3, 0))
elm.Line().down(2).at((-6, -2))
elm.Line().up().at((-6, 0)).to((-3, 0))
elm.Line().left(3).at((-6, -2)).to((-3, -2))
```

## 7. Diode Reverse-Recovery Path

When a forward-biased diode is opened, stored charge must be removed before blocking resumes. The switching loop highlights the parasitic path that produces reverse recovery current.

```circuit
elm.SourceV().up().at((0, 0)).label("forward drive", loc="left")
elm.Resistor().right().at((0, 3)).label("R", loc="top")
elm.Diode().right().at((3, 3)).label("D", loc="top")
elm.Line().down(3).at((6, 3))
elm.Line().left(6).at((6, -3))
elm.Line().up(3).at((0, -3)).to((0, 0))
elm.Switch().up().reverse().at((3, -3)).label("turn-off path", loc="right")
elm.Line().up().at((3, -3)).to((3, 0))
elm.Line().left(3).at((3, 0)).to((0, 0))
```
