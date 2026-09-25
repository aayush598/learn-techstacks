# Circuit Diagrams

## 1. DIAC Relaxation Oscillator

The timing capacitor charges through the resistor until the DIAC breakover voltage is reached. The DIAC then conducts and transfers charge, producing a repeating relaxation waveform.

```circuit
elm.SourceV().up().at((-3, 0)).label("V_supply", loc="left")
elm.Resistor().right().at((-3, 3)).label("R charge", loc="top")
elm.Dot().at((0, 3)).label("timing node", loc="right")
elm.Diac().right().at((0, 3)).label("DIAC", loc="top")
elm.Line().right(2).at((3, 3)).label("pulse", loc="right")
elm.Capacitor().down().at((0, 3)).label("C timing", loc="right")
elm.Line().down(3).at((0, 0))
elm.Line().left(3).at((0, 0)).to((-3, 0))
```

## 2. DIAC Triggering an SCR

The RC phase-shift network charges a capacitor until the DIAC fires and supplies a gate pulse. The pulse is removed after the SCR latches, limiting sustained gate drive.

```circuit
s = elm.SCR().right().at((0, 3)).label("T1 SCR", loc="top")
elm.SourceSin().up().at((0, 0)).label("v_ac", loc="left")
elm.Line().up(3).at((0, 3))
elm.Dot().at((3, 3)).label("RC node", loc="right")
elm.Resistor().right().at((3, 3)).label("R", loc="top")
elm.Capacitor().down().at((3, 3)).label("C", loc="right")
elm.Diac().right().at((5, 1)).label("DIAC", loc="top")
elm.Line().right(1).at((8, 1)).to((8, 3))
elm.Line().up(2).at((8, 3)).to((8, 5))
elm.Line().right(2).at((8, 5))
elm.Line().down(5).at((10, 0))
elm.Line().left(10).at((0, 0))
elm.Line().right(1).at((1, 2)).to(s.gate)
elm.Dot().at((1, 2)).label("gate trigger", loc="bottom")
```

## 3. TRIAC Bidirectional Characteristic

The TRIAC main terminals are symmetric, so the same device can conduct during either AC polarity. The gate trigger must be referenced to MT1 and synchronized to the selected half-cycle.

```circuit
t = elm.Triac().right().at((-3, 0)).label("T1 TRIAC", loc="top")
elm.SourceSin().up().at((-3, 0)).label("AC line", loc="left")
elm.Resistor().up().at((-3, 3)).label("load", loc="left")
elm.Line().up(2).at((-3, 5))
elm.Line().right(3).at((0, 0))
elm.Line().down(2).at((0, -2))
elm.Line().left(3).at((0, -2))
elm.Line().up(2).at((-3, -2)).to((-3, 0))
g = elm.Line().up(1).at(t.gate)
elm.SourceV().up().reverse().at(g.end).label("gate", loc="right")
```

## 4. TRIAC Phase-Controlled Load

The firing delay is varied in each permitted half-cycle. Earlier firing gives greater load power; delayed firing narrows the conduction interval.

```circuit
t = elm.Triac().right().at((-3, 0)).label("T1", loc="top")
elm.SourceSin().up().at((-3, 0)).label("v_s", loc="left")
elm.Resistor().up().at((-3, 3)).label("R_L", loc="left")
elm.Line().up(2).at((-3, 5))
elm.Line().right(3).at((0, 0))
elm.Dot().at((0, 0)).label("v_o", loc="right")
elm.Line().down(2).at((0, -2))
elm.Line().left(3).at((0, -2))
elm.Line().up(2).at((-3, -2)).to((-3, 0))
elm.SourceV().up().reverse().at(elm.Line().up(1).at(t.gate).end).label("delay alpha", loc="right")
```

## 5. DIAC Firing-Angle Reference

The timing capacitor charges from the AC line and reaches breakover at a selected angle. The resulting pulse is the trigger reference for the main TRIAC.

```circuit
elm.SourceSin().right().at((-4, 2)).label("v_ac", loc="left")
elm.Dot().at((0, 0)).label("RC timing", loc="top")
elm.Line().right(2).at((-2, 2)).to((0, 2))
elm.Line().right(2).at((-2, -2)).to((0, -2))
elm.Line().up(2).at((0, -2)).to((0, 2))
elm.Arrow().right().at((0, 0)).to((3, 0)).label("breakover pulse", loc="top")
elm.Arrow().right().at((3, 0)).to((6, 0)).label("TRIAC gate", loc="top")
elm.Line().right(2).at((0, -2)).label("ramp setting", loc="bottom")
```

## 6. GTO Turn-On and Turn-Off Drives

Positive gate current creates conduction, while a sufficiently negative gate pulse removes stored charge and interrupts anode current. The two drives are shown as separate controlled paths.

```circuit
gto = elm.SCR().right().at((-3, 0)).label("T1 GTO", loc="top")
elm.SourceV().down().at(gto.gate).label("-IG", loc="bottom")
elm.Ground()
elm.SourceV().up().at((-2, -1)).label("+IG", loc="right")
elm.Line().down().at((-2, 0)).to(gto.gate)
elm.Line().up(2).at((-3, 0))
elm.Resistor().up().label("load", loc="left")
elm.Line().up(2).at((-3, 4))
elm.Line().right(3).at((0, 0))
elm.Line().down(2).at((0, -2))
elm.Line().left(3).at((0, -2))
elm.Line().up(2).at((-3, -2)).to((-3, 0))
```

## 7. GTO Chopper Path

The GTO provides high-frequency switching and explicit turn-off, so it is useful in high-power choppers. The inductor smooths current and the freewheel diode carries inductive current while the main device is off.

```circuit
elm.SourceV().up().at((-4, -2)).label("V_dc", loc="left")
elm.Inductor().right().at((-4, 1)).label("L", loc="top")
elm.Dot().at((-1, 1)).label("switch node", loc="top")
elm.Switch().right().at((-1, 1)).label("GTO", loc="top")
elm.Line().right(1).at((1, 1))
elm.Diode().up().at((2, -1)).label("D_fw", loc="right")
elm.Line().up(1).at((2, 0)).to((2, 1))
elm.Line().right(2).at((2, 1))
elm.Resistor().down().at((4, 1)).label("load", loc="right")
elm.Line().down(3).at((4, -2))
elm.Line().left(8).at((4, -2)).to((-4, -2))
elm.Line().up(3).at((2, -2)).to((2, 0))
```

## 8. TRIAC Static dv/dt Limitation

A TRIAC can trigger accidentally if the rate of change of voltage across it produces sufficient internal displacement current. Snubbing and a controlled gate path reduce this risk.

```circuit
t = elm.Triac().right().at((-3, 0)).label("T1", loc="top")
elm.SourceV().up().at((-3, 0)).label("fast voltage edge", loc="left")
elm.Capacitor().up().at((-3, 3)).label("C_snub", loc="right")
elm.Resistor().up().at((-3, 4)).label("R_snub", loc="right")
elm.Line().up(1).at((-3, 5))
elm.Line().right(3).at((0, 0))
elm.Line().down(2).at((0, -2))
elm.Line().left(3).at((0, -2))
elm.Line().up(2).at((-3, -2)).to((-3, 0))
g = elm.Line().up(1).at(t.gate)
elm.SourceV().up().reverse().at(g.end).label("controlled gate", loc="right")
```
