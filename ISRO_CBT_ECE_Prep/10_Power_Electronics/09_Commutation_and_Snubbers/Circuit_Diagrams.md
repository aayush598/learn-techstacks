# Circuit Diagrams

## 1. Natural Commutation in a Thyristor

Natural commutation occurs when the AC current reaches zero and reverses polarity. The SCR can block the reversed voltage after the next current zero, so no forced commutation hardware is required.

```circuit
s = elm.SCR().right().at((-3, 0)).label("SCR", loc="top")
elm.SourceSin().up().at((-3, 0)).label("ac source", loc="left")
elm.Line().right(3).at((0, 0))
elm.Resistor().down().at((0, 0)).label("R load", loc="right")
elm.Line().down(2).at((0, -2))
elm.Line().left(3).at((0, -2))
elm.Line().up(2).at((-3, -2)).to((-3, 0))
elm.Dot().at((0, 0)).label("current zero", loc="right")
elm.SourceV().down().at(s.gate).label("gate", loc="bottom")
elm.Ground()
```

## 2. Class-D Forced Commutation

A charged auxiliary capacitor applies a reverse voltage to the main SCR and removes its stored charge. The main device then turns off even though the load current is not naturally zero.

```circuit
s = elm.SCR().right().at((-4, 2)).label("main SCR", loc="top")
elm.SourceV().up().at((-4, 0)).label("V_dc", loc="left")
elm.Line().up(2).at((-4, 2))
elm.Inductor().right().at((-1, 2)).label("load L", loc="top")
elm.Dot().at((2, 2)).label("load", loc="right")
elm.Resistor().down().at((2, 2)).label("R", loc="right")
elm.Capacitor().right().at((-4, 0)).label("commutating C", loc="bottom")
elm.Switch().right().at((-1, 0)).label("aux switch", loc="bottom")
elm.Diode().up().at((2, 0)).label("reverse-bias D", loc="right")
elm.Line().up(2).at((2, 2))
elm.Line().down(4).at((2, -2))
elm.Line().left(6).at((2, -2)).to((-4, 0))
elm.Line().left(3).at((2, 0))
elm.Line().down(2).at((2, -2))
```

## 3. Auxiliary-SCR Commutation

A second thyristor provides a low-impedance path for the main device's current. The main SCR is reverse-biased and can recover its blocking capability.

```circuit
main = elm.SCR().right().at((-4, 2)).label("main T1", loc="top")
aux = elm.SCR().right().at((-4, 0)).label("aux T2", loc="top")
elm.SourceV().up().at((-4, -2)).label("V_dc", loc="left")
elm.Line().up(2).at((-4, 0))
elm.Inductor().right().at((-1, 2)).label("load L", loc="top")
elm.Dot().at((2, 2)).label("load", loc="right")
elm.Resistor().down().at((2, 2)).label("R", loc="right")
elm.Capacitor().right().at((-1, 0)).label("C", loc="bottom")
elm.Diode().up().reverse().at((2, 0)).label("D", loc="right")
elm.Line().right(2).at((2, 0)).to((4, 0))
elm.Line().up(2).at((4, 0)).to((4, 2))
elm.Line().left(2).at((4, 2)).to((2, 2))
elm.Line().down(4).at((2, -2))
elm.Line().left(6).at((2, -2)).to((-4, -2))
elm.SourceV().down().at(main.gate).label("main gate", loc="bottom")
elm.Ground()
elm.SourceV().down().at(aux.gate).label("aux gate", loc="bottom")
elm.Ground()
```

## 4. Voltage Commutation Network

The auxiliary capacitor is charged before the main SCR is fired. Triggering the commutation switch places the charged voltage across the main device with reverse polarity.

```circuit
main = elm.SCR().right().at((-4, 2)).label("T1 main", loc="top")
elm.SourceV().up().at((-4, -2)).label("V_dc", loc="left")
elm.Line().up(2).at((-4, 0))
elm.Inductor().right().at((-1, 2)).label("load", loc="top")
elm.Dot().at((2, 2)).label("out", loc="right")
elm.Capacitor().down().at((2, 2)).label("C_comm", loc="right")
elm.Switch().right().at((-1, 0)).label("commutating switch", loc="bottom")
elm.Diode().up().at((2, 0)).label("D reverse", loc="right")
elm.Line().up(2).at((2, 0)).to((2, 2))
elm.Line().down(4).at((2, -2))
elm.Line().left(6).at((2, -2)).to((-4, -2))
elm.SourceV().down().at(main.gate).label("fire T1", loc="bottom")
elm.Ground()
```

## 5. Current-Commutation Network

The auxiliary inductor stores current and then applies a reverse current pulse to the main device. The resonant or forced current drives the main SCR below its holding current.

```circuit
s = elm.SCR().right().at((-4, 2)).label("main SCR", loc="top")
elm.SourceV().up().at((-4, -2)).label("V_dc", loc="left")
elm.Line().up(2).at((-4, 0))
elm.Inductor().right().at((-1, 2)).label("load L", loc="top")
elm.Dot().at((2, 2)).label("load", loc="right")
elm.Resistor().down().at((2, 2)).label("R", loc="right")
elm.Switch().right().at((-1, 0)).label("aux SCR", loc="bottom")
elm.Inductor().right().at((1, 0)).label("commutating L", loc="bottom")
elm.Capacitor().down().at((2, 0)).label("C", loc="right")
elm.Line().down(2).at((2, 0))
elm.Line().left(6).at((2, -2)).to((-4, -2))
elm.SourceV().down().at(s.gate).label("main gate", loc="bottom")
elm.Ground()
```

## 6. RC Snubber Across an SCR

The series resistor damps the switching transient and the capacitor absorbs high-frequency energy. The pair limits `dv/dt` and reduces turn-on stress.

```circuit
s = elm.SCR().right().at((-3, 0)).label("SCR", loc="top")
elm.SourceV().up().at((-3, 0)).label("V_A", loc="left")
elm.Line().right(3).at((0, 0))
elm.Line().up(2).at((0, 2))
elm.Capacitor().right().at((-3, 2)).label("C_snub", loc="top")
elm.Resistor().right().at((0, 2)).label("R_snub", loc="top")
elm.Line().right(3).at((3, 2))
elm.Line().down(2).at((3, 0))
elm.Line().right(3).at((3, 0))
elm.Line().down(2).at((6, 0))
elm.Line().left(6).at((6, -2))
elm.Line().up(2).at((-3, -2)).to((-3, 0))
```

## 7. RCD Clamp

The diode, capacitor, and resistor clamp the drain or switch-node voltage while dissipating the trapped energy in the resistor. This is common in MOSFET and IGBT converters.

```circuit
elm.SourceV().up().at((-4, 0)).label("V_in", loc="left")
elm.Switch().right().at((-4, 3)).label("Q1", loc="top")
elm.Dot().at((-1, 3)).label("switch node", loc="right")
elm.Diode().up().at((0, 2)).label("clamp D", loc="right")
elm.Capacitor().right().at((0, 3)).label("C_clamp", loc="top")
elm.Resistor().right().at((3, 3)).label("R_clamp", loc="top")
elm.Line().right(2).at((6, 3)).label("drain", loc="right")
elm.Line().left(6).at((6, -2)).to((-4, -2))
elm.Line().up(2).at((0, 0))
elm.Line().left(4).at((0, -2)).to((-4, -2))
```

## 8. Freewheeling Current Path

When the main switch opens, the diode provides a low-impedance loop through the load and smoothing inductor. This prevents an excessive inductive voltage spike.

```circuit
elm.SourceV().up().at((-4, -2)).label("V_dc", loc="left")
elm.Switch().right().at((-4, 1)).label("Q1", loc="top")
elm.Dot().at((-1, 1)).label("i_L", loc="top")
elm.Inductor().right().at((-1, 1)).label("L", loc="top")
elm.Dot().at((2, 1)).label("load node", loc="right")
elm.Resistor().down().at((2, 1)).label("R_L", loc="right")
elm.Diode().down().at((-1, 0)).label("freewheel D", loc="right")
elm.Line().down(1).at((-1, 0))
elm.Line().left(3).at((-1, -2)).to((-4, -2))
elm.Line().down(3).at((2, -2))
elm.Line().left(6).at((2, -2)).to((-4, -2))
```
