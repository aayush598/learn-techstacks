# Circuit Diagrams

## 1. Step-Down Chopper

Closing the main switch applies the source to the load and stores energy in the inductor. Opening it transfers current to the freewheel path, maintaining a positive average output voltage.

```circuit
elm.SourceV().up().at((-4, -2)).label("V_dc", loc="left")
elm.Switch().right().at((-4, 1)).label("main switch", loc="top")
elm.Dot().at((-2, 1)).label("chopper node", loc="top")
elm.Inductor().right().at((-2, 1)).label("L", loc="top")
elm.Dot().at((1, 1)).label("V_o", loc="right")
elm.Capacitor().down().at((1, 1)).label("C", loc="right")
elm.Line().right(1).at((1, 1)).dot()
elm.Resistor().down().at((2, 1)).label("R_L", loc="right")
elm.Diode().down().at((-2, 0)).label("freewheel D", loc="right")
elm.Line().down(1).at((-2, 0))
elm.Line().left(4).at((-2, -2)).to((-4, -2))
elm.Line().down(3).at((2, -2))
elm.Line().left(6).at((2, -2)).to((-4, -2))
```

## 2. Step-Up Chopper

The switching inductor stores energy and then releases it through the diode and load. The output receives both the source energy and the inductor energy during the release interval.

```circuit
elm.SourceV().up().at((-4, -2)).label("V_dc", loc="left")
elm.Inductor().right().at((-4, 1)).label("L", loc="top")
elm.Dot().at((-1, 1)).label("switch node", loc="top")
elm.Switch().down().at((-1, 1)).label("main switch", loc="right")
elm.Diode().up().at((1, 1)).label("boost D", loc="right")
elm.Line().up(1).at((1, 2))
elm.Line().up(1).at((1, 3)).label("V_o", loc="right")
elm.Capacitor().down().at((1, 3)).label("C", loc="right")
elm.Line().right(1).at((1, 3)).dot()
elm.Resistor().down().at((2, 3)).label("R_L", loc="right")
elm.Line().left(6).at((2, -2))
elm.Line().up(3).at((-1, -2)).to((-1, 0))
elm.Line().up(2).at((-4, -2)).to((-4, 1))
elm.Line().up(1).at((-1, 1)).to((1, 1))
```

## 3. Reversible Step-Down/Step-Up Chopper

The second switch path returns stored energy to the source during braking intervals. One switch supports motoring, while the other supports regenerative current in the opposite direction.

```circuit
elm.SourceV().up().at((-3, -2)).label("V_dc", loc="left")
elm.Inductor().right().at((-3, 1)).label("L", loc="top")
elm.Dot().at((0, 1)).label("switch node", loc="top")
elm.Switch().right().at((0, 1)).label("motoring path", loc="top")
elm.Switch().left().at((0, 1)).label("regen path", loc="bottom")
elm.Diode().up().at((3, 1)).label("output D", loc="right")
elm.Line().up(2).at((3, 3)).label("load", loc="right")
elm.Resistor().down().at((3, 3)).label("R_L", loc="right")
elm.Line().down(5).at((3, -2))
elm.Line().left(6).at((3, -2)).to((-3, -2))
elm.Line().up(1).at((0, 0)).to((0, 1))
elm.Line().left(2).at((0, 0))
```

## 4. Current-Commutated Chopper

An auxiliary SCR and commutating elements force current through the main SCR to zero. This permits controlled turn-off even when the source current does not naturally reverse.

```circuit
elm.SourceV().up().at((-5, -2)).label("V_dc", loc="left")
elm.Inductor().right().at((-5, 1)).label("L", loc="top")
elm.Dot().at((-2, 1)).label("main path", loc="top")
elm.Switch().right().at((-2, 1)).label("main SCR", loc="top")
elm.Line().right(2).at((1, 1))
elm.Resistor().down().at((1, 1)).label("load", loc="right")
elm.Switch().down().at((-2, 1)).label("aux SCR", loc="right")
elm.Capacitor().right().at((-2, -1)).label("commutating C", loc="top")
elm.Inductor().down().at((0, -1)).label("commutating L", loc="right")
elm.Line().down(1).at((0, -2))
elm.Line().left(5).at((0, -2)).to((-5, -2))
elm.Line().down(3).at((1, -2))
elm.Line().left(6).at((1, -2)).to((-5, -2))
```

## 5. Voltage-Commutated Chopper

The auxiliary switch applies a reverse voltage across the main thyristor and removes its stored charge. The main device can then block after the commutation interval.

```circuit
elm.SourceV().up().at((-4, -2)).label("V_dc", loc="left")
elm.Switch().right().at((-4, 1)).label("main SCR", loc="top")
elm.Inductor().right().at((-1, 1)).label("L", loc="top")
elm.Dot().at((2, 1)).label("load node", loc="top")
elm.Switch().right().at((2, 1)).label("aux SCR", loc="top")
elm.Capacitor().down().at((2, 1)).label("commutating C", loc="right")
elm.Resistor().down().at((5, 1)).label("R_L", loc="right")
elm.Line().down(3).at((5, -2))
elm.Line().left(9).at((5, -2)).to((-4, -2))
elm.Line().left(2).at((2, 0))
elm.Line().down(1).at((2, -1))
elm.Line().left(2).at((2, -2)).to((0, -2))
```

## 6. Regenerative Braking Chopper

During braking, the machine's generated emf drives current back toward the DC source. The path is reverse in power-flow sense even though the same inductor, switch, and diode may be reused.

```circuit
elm.SourceV().up().at((-4, 0)).label("DC source", loc="left")
elm.Line().up(2).at((-4, 2))
elm.Inductor().right().at((-4, 3)).label("L", loc="top")
elm.Dot().at((-1, 3)).label("braking node", loc="top")
elm.Switch().right().at((-1, 3)).label("regen switch", loc="top")
elm.Diode().left().at((-4, 3)).label("D return", loc="bottom")
elm.Line().left(2).at((-4, 3))
elm.Line().up(1).at((-6, 3)).to((-4, 3))
elm.Line().right(4).at((-1, 3)).label("machine current", loc="top")
elm.Motor().right().at((3, 3)).label("M", loc="bottom")
elm.Line().right(1).at((6, 3))
elm.Line().down(3).at((6, 0))
elm.Line().left(10).at((6, 0)).to((-4, 0))
```

## 7. Four-Quadrant Chopper

Two bridge legs select the voltage polarity and the current direction. The four combinations cover forward motoring, reverse motoring, forward regeneration, and reverse regeneration.

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
elm.Motor().right().at((-1, 0)).label("drive motor", loc="bottom")
elm.Line().right(2).at((3, 0)).to((2, 0))
elm.Line().right(1).at((-5, -3))
```

## 8. Chopper Current and Voltage Paths

The inductor smooths current, while the capacitor smooths voltage at the load. The freewheel diode prevents a high inductive voltage when the main switch opens.

```circuit
elm.SourceV().up().at((-4, -2)).label("V_dc", loc="left")
elm.Switch().up().at((-4, 1)).label("Q", loc="right")
elm.Dot().at((-4, 4)).label("i_L", loc="left")
elm.Inductor().down().at((-4, 4)).label("L", loc="left")
elm.Line().down(2).at((-4, 1)).dot()
elm.Diode().down().at((-2, 1)).label("D", loc="right")
elm.Line().down(1).at((-2, 0))
elm.Line().left(2).at((-2, -2))
elm.Capacitor().down().at((0, 1)).label("C", loc="right")
elm.Resistor().down().at((2, 1)).label("load", loc="right")
elm.Line().right(2).at((0, 1)).to((2, 1))
elm.Line().down(3).at((2, -2))
elm.Line().left(6).at((2, -2)).to((-4, -2))
```
