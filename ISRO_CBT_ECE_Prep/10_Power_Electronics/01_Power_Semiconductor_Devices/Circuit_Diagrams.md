# Circuit Diagrams

## 1. Diode Forward-Conduction Test

A forward-biased diode behaves approximately as a small resistance when its voltage exceeds the forward drop. The series resistor limits current and is therefore part of the safe test circuit.

```circuit
elm.SourceV().up().at((0, 0)).label("V_A", loc="left")
elm.Resistor().right().at((0, 3)).label("R limit", loc="top")
elm.Diode().right().at((3, 3)).label("D forward", loc="top")
elm.Line().down(3).at((6, 3))
elm.Line().left(6).at((6, -3))
elm.Line().up(3).at((0, -3)).to((0, 0))
elm.Dot().at((0, 0)).label("cathode return", loc="left")
```

## 2. Diode Reverse-Blocking Test

Reversing the diode polarity places the negative terminal at a higher potential than the positive terminal. Except for leakage, the current is blocked when the reverse voltage is below breakdown.

```circuit
elm.SourceV().up().at((0, 0)).label("V_A", loc="left")
elm.Resistor().right().at((0, 3)).label("R limit", loc="top")
elm.Diode().right().reverse().at((3, 3)).label("D reverse", loc="top")
elm.Line().down(3).at((6, 3))
elm.Line().left(6).at((6, -3))
elm.Line().up(3).at((0, -3)).to((0, 0))
elm.Dot().at((0, 0)).label("anode return", loc="left")
```

## 3. NPN BJT Common-Emitter Test

The base-source voltage controls collector current in the active region, while the collector resistor converts the controlled current into a voltage. The emitter is tied to the reference node.

```circuit
q = elm.BjtNpn().at((-1, 0)).label("Q1 NPN", loc="left")
elm.SourceV().down().at(q.base).label("V_B", loc="left")
elm.Ground()
elm.Line().up(1).at(q.collector).dot()
elm.Resistor().up().label("R_C", loc="right")
elm.Line().up().label("V_CC", loc="right")
elm.Line().down(1).at(q.emitter)
elm.Ground()
```

## 4. PNP BJT High-Side Test

The PNP emitter is connected toward the positive supply and its collector drives the load. A low base voltage relative to the emitter produces conduction in the ideal active-region model.

```circuit
q = elm.BjtPnp().at((-1, 0)).label("Q1 PNP", loc="left")
elm.SourceV().down().at(q.base).label("V_B", loc="left")
elm.Ground()
elm.SourceV().up().at(q.emitter).label("V_CC", loc="left")
elm.Line().down(1).at(q.collector).dot()
elm.Resistor().down().label("R_E", loc="right")
elm.Ground()
```

## 5. N-Channel Enhancement MOSFET

The gate is insulated from the drain-source path, so the steady-state gate current is ideally zero. The drain resistor limits current while the source is referenced to ground.

```circuit
q = elm.NMos(diode=True).at((-1, 0)).label("Q1 n-MOSFET", loc="left")
elm.SourceV().down().at(q.gate).label("V_G", loc="left")
elm.Ground()
elm.Line().up(1).at(q.drain).dot()
elm.Resistor().up().label("R_D", loc="right")
elm.Line().up().label("V_DD", loc="right")
elm.Line().down(1).at(q.source)
elm.Ground()
```

## 6. N-Channel IGBT

An IGBT combines a MOS-gated input with a high-voltage bipolar output stage. The emitter-side load path is shown with a collector resistor to make the controlled high-side current explicit.

```circuit
q = elm.IgbtN().at((-1, 0)).label("Q1 IGBT", loc="left")
elm.SourceV().down().at(q.base).label("V_G", loc="left")
elm.Ground()
elm.Line().up(1).at(q.collector).dot()
elm.Resistor().up().label("R_C", loc="right")
elm.Line().up().label("V_DC", loc="right")
elm.Line().down(1).at(q.emitter)
elm.Ground()
```

## 7. SCR in the Conductive State

A forward-biased SCR begins conducting when its gate receives a trigger pulse and remains latched while anode current exceeds its holding current. The load limits that current.

```circuit
s = elm.SCR().right().at((-3, 0)).label("T1 SCR", loc="top")
elm.Line().up(2).at(s.start)
elm.Resistor().up().label("R load", loc="left")
elm.Line().up().label("+V_A", loc="left")
elm.SourceV().down().at(s.gate).label("gate pulse", loc="bottom")
elm.Ground()
elm.Line().down(2).at(s.end)
elm.Line().left(3).at((0, -2))
elm.Line().up(2).at((-3, -2)).to((-3, 0))
```

## 8. TRIAC Bidirectional Conduction

A TRIAC can conduct in either direction when triggered, making it suitable for AC phase control. The series element represents the controlled load.

```circuit
t = elm.Triac().right().at((-3, 0)).label("T1 TRIAC", loc="top")
elm.Line().up(2).at((-3, 0))
elm.Resistor().up().label("AC load", loc="left")
elm.Line().up().label("AC", loc="left")
g = elm.Line().up(1).at(t.gate)
elm.SourceV().up().reverse().at(g.end).label("trigger", loc="right")
elm.Line().down(2).at(t.end)
elm.Line().left(3).at((0, -2))
elm.Line().up(2).at((-3, -2)).to((-3, 0))
```

## 9. GTO Symbol Convention

A gate-turn-off thyristor uses an SCR-family main terminal pair, but its gate accepts positive current for turn-on and negative current for turn-off. The label makes the bidirectional gate drive explicit.

```circuit
gto = elm.SCR().right().at((-3, 0)).label("T1 GTO", loc="top")
elm.Line().up(2).at(gto.start)
elm.Resistor().up().label("load", loc="left")
elm.Line().up().label("+V", loc="left")
elm.SourceV().down().at(gto.gate).label("-IG turn-off", loc="bottom")
elm.Ground()
elm.SourceV().up().at((-2, -1)).label("+IG turn-on", loc="right")
elm.Line().down().at((-2, 0)).to(gto.gate)
elm.Line().down(2).at(gto.end)
elm.Line().left(3).at((0, -2))
elm.Line().up(2).at((-3, -2)).to((-3, 0))
```
