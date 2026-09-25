# Circuit Diagrams

## 1. SCR DC Latching

After a gate pulse turns the SCR on, it remains on while anode current exceeds the holding current. Removing the gate signal alone does not turn it off.

```circuit
s = elm.SCR().right().at((-3, 0)).label("T1 SCR", loc="top")
elm.Line().up(2).at(s.start)
elm.Resistor().up().label("R load", loc="left")
elm.Line().up().label("+V_A", loc="left")
elm.SourceV().down().at(s.gate).label("one-shot gate pulse", loc="bottom")
elm.Ground()
elm.Line().down(2).at(s.end)
elm.Line().left(3).at((0, -2))
elm.Line().up(2).at((-3, -2)).to((-3, 0))
```

## 2. Gate Pulse below the SCR Trigger Threshold

A gate signal below the trigger threshold or below the breakover voltage does not start latching. The pulse is shown as a controlled input to the SCR gate.

```circuit
s = elm.SCR().right().at((-3, 0)).label("T1 off", loc="top")
elm.SourceSin().up().at((-3, -2)).label("small gate pulse", loc="left")
elm.Line().up(2).at((-3, 0))
elm.Line().down(2).at(s.end)
elm.Line().left(3).at((0, -2))
elm.Line().up(2).at((-3, -2)).to((-3, 0))
elm.Line().right(1).at((-1, -1)).to(s.gate)
elm.Dot().at((-1, -1)).label("below threshold", loc="bottom")
```

## 3. Half-Wave Controlled Rectifier

Firing at a delay angle alpha transfers the selected portion of each positive half-cycle to the load. The SCR blocks the negative half-cycle and must be commutated naturally by current reversal.

```circuit
s = elm.SCR().right().at((-3, 0)).label("T1", loc="top")
elm.SourceSin().up().at((-3, -3)).label("v_s", loc="left")
elm.Line().up(3).at((-3, 0))
elm.Dot().at((0, 0)).label("v_o", loc="right")
elm.Resistor().down().at((0, 0)).label("R_L", loc="right")
elm.Line().down(3).at((0, -3))
elm.Line().left(3).at((0, -3))
elm.Line().up(3).at((-3, -3))
elm.SourceV().down().at(s.gate).label("gate at alpha", loc="bottom")
elm.Ground()
```

## 4. Single-Phase Full-Wave Controlled Rectifier

One SCR and one diode form a controlled full-wave path for a resistive load. The SCR conducts on positive source half-cycles, while the diode provides the return current on negative half-cycles after the SCR is triggered.

```circuit
elm.SourceSin().up().at((0, 0)).label("v_s", loc="left")
s = elm.SCR().right().at((0, 3)).label("T1", loc="top")
elm.Line().right(3).at((3, 3))
elm.Diode().right().at((0, 0)).label("D1", loc="bottom")
elm.Line().right(3).at((3, 0))
elm.Line().up(3).at((3, 0)).to((3, 3))
elm.Dot().at((3, 3)).label("v_o", loc="right")
elm.Resistor().down().at((3, 3)).label("R_L", loc="right")
elm.Line().down(3).at((3, 0))
elm.Line().down(3).at((3, -3))
elm.Line().left(3).at((3, -3))
elm.Line().up(3).at((0, -3)).to((0, 0))
elm.SourceV().down().at(s.gate).label("trigger", loc="bottom")
elm.Ground()
```

## 5. Firing-Angle Control

The controller compares a timing ramp with a command level. The crossing determines alpha, and a narrow pulse is delivered to the selected thyristor gate.

```circuit
elm.SourceSin().right().at((-4, 2)).label("sine reference", loc="left")
elm.SourceV().up().at((-4, -2)).label("ramp", loc="left")
elm.Dot().at((0, 0)).label("comparator", loc="right")
elm.Line().right(2).at((-2, 2)).to((0, 2))
elm.Line().right(2).at((-2, -2)).to((0, -2))
elm.Line().up(2).at((0, -2)).to((0, 2))
elm.Line().right(2).at((0, 0)).label("alpha", loc="top")
elm.Line().right(2).at((2, 0)).label("gate pulse", loc="right")
elm.Arrow().right().at((4, 0)).to((6, 0)).label("to thyristor gate", loc="top")
```

## 6. dv/dt-Induced Turn-On

A rapidly rising anode voltage supplies displacement current through junction capacitance. If that current reaches the SCR's effective turn-on level, the device can conduct without a gate pulse.

```circuit
s = elm.SCR().right().at((-3, 0)).label("T1", loc="top")
elm.SourceV().up().at((-3, 0)).label("rapid dV/dt", loc="left")
elm.Capacitor().up().at((-3, 3)).label("C_j", loc="right")
elm.Line().up(1).at((-3, 4)).label("anode", loc="right")
elm.Line().down(2).at(s.end)
elm.Line().left(3).at((0, -2))
elm.Line().up(2).at((-3, -2)).to((-3, 0))
elm.Line().right(1).at((-1, -1)).to(s.gate)
elm.Dot().at((-1, -1)).label("no gate trigger", loc="bottom")
```

## 7. di/dt Limiting

Series inductance limits the rate at which anode current rises. Without sufficient inductance, the SCR can suffer excessive turn-on loss or local heating near the gate region.

```circuit
s = elm.SCR().right().at((-2, 0)).label("T1", loc="top")
elm.SourceV().up().at((-5, 0)).label("+V_A", loc="left")
elm.Line().right(1).at((-5, 3))
elm.Inductor().right().at((-4, 3)).label("L limit", loc="top")
elm.Line().right(1).at((-1, 3)).to(s.start)
elm.Line().down(2).at(s.end)
elm.Line().left(4).at((1, -2))
elm.Line().up(2).at((-5, -2)).to((-5, 0))
elm.SourceV().down().at(s.gate).label("gate", loc="bottom")
elm.Ground()
```

## 8. Holding-Current Interlock

The load current is monitored so the controller can issue a turn-off command before current falls below the SCR holding current. The sensing block is a control signal path.

```circuit
elm.Line().right(2).at((-5, 0)).label("SCR anode current", loc="left")
elm.Dot().at((-2, 0)).label("sense", loc="top")
elm.Arrow().right().at((-2, 0)).to((0, 0)).label("measure I_A", loc="top")
elm.Arrow().right().at((0, 0)).to((2, 0)).label("I_A > I_H", loc="top")
elm.Arrow().right().at((2, 0)).to((4, 0)).label("permit turn-off", loc="top")
elm.Line().down(2).at((4, 0))
elm.Line().left(9).at((4, -2))
elm.Line().up(2).at((-5, -2)).to((-5, 0))
```
