# Circuit Diagrams

## 1. Series RLC Impedance

The source sees the sum of the resistive, inductive, and capacitive voltage drops. The net reactance is positive for inductive dominance and negative for capacitive dominance.

```circuit
elm.SourceSin().up().at((0, 0)).label("V phasor", loc="left")
elm.Resistor().right().at((0, 3)).label("R", loc="top")
elm.Inductor().down().at((3, 3)).label("j omega L", loc="right")
elm.Capacitor().left().at((3, 0)).label("-j/(omega C)", loc="bottom")
elm.Dot().at((0, 0)).label("reference", loc="left")
elm.Ground().at((0, 0))
```

## 2. Capacitive AC Divider

Two series capacitors divide an AC voltage. The output is taken across the lower capacitor, giving `Vout = Vin ZC2/(ZC1 + ZC2)` for the ideal unloaded case.

```circuit
elm.SourceSin().up().at((0, 0)).label("Vac", loc="left")
elm.Capacitor().up().at((0, 0)).label("C1", loc="right")
elm.Line().up().at((0, 2)).label("vout", loc="right")
elm.Capacitor().up().at((0, 2)).label("C2", loc="right")
elm.Line().up(1).at((0, 4))
elm.Line().right().at((0, 5))
elm.Line().down(5).at((2, 5))
elm.Line().left(2).at((2, 5)).to((0, 5))
elm.Line().down(3).at((2, 2))
elm.Line().left(2).at((2, -1)).to((0, -1))
elm.Line().up().at((0, -1)).to((0, 0))
```

## 3. Inductive AC Divider

The series inductors form an unloaded AC divider. The output across `L2` is proportional to `L2/(L1 + L2)` in magnitude and shifted in phase by the inductive divider relation.

```circuit
elm.SourceSin().up().at((0, 0)).label("Vac", loc="left")
elm.Inductor().up().at((0, 0)).label("L1", loc="right")
elm.Dot().at((0, 3)).label("vout", loc="right")
elm.Inductor().up().at((0, 3)).label("L2", loc="right")
elm.Line().up(1).at((0, 6))
elm.Line().right(2).at((0, 7))
elm.Line().down(7).at((2, 7))
elm.Line().left(2).at((2, 0)).to((0, 0))
```

## 4. Impedance Triangle

The impedance of a series RLC branch is the vector sum of the real resistance and the signed reactive component. The arrows are a phasor construction, not three physical components in series.

```circuit
elm.Line().right(4).at((-3, 0)).label("R")
elm.Arrow().up().at((1, 0)).to((1, 3)).label("XL - XC")
elm.Arrow().right().at((-3, 0)).to((1, 0))
elm.Arrow().right().at((-3, 0)).to((1, 3)).label("Z", loc="top")
elm.Dot().at((-3, 0)).label("0", loc="left")
elm.Dot().at((1, 0)).label("R", loc="bottom")
elm.Dot().at((1, 3)).label("R + jX", loc="right")
```

## 5. Real and Reactive Power Paths

A load can draw real power through a resistive path and exchange reactive energy through an inductive path. The arrows emphasize that these are different power components, not that the source supplies two independent physical voltages.

```circuit
elm.SourceSin().up().at((-3, 0)).label("supply")
elm.Line().up(1).at((-3, 3)).label("input current", loc="left")
elm.Dot().at((-3, 4)).label("load", loc="right")
elm.Arrow().right().at((-3, 4)).to((1, 4)).label("P", loc="top")
elm.Arrow().right().at((-3, 4)).to((1, 1)).label("Q", loc="top")
elm.Line().down(4).at((1, 0))
elm.Dot().at((-3, 0)).label("return", loc="left")
elm.Line().left(2).at((-3, 0)).to((-5, 0))
elm.Line().up().at((-5, 0)).to((-5, 3))
elm.Line().right().at((-5, 3)).to((-3, 3))
```
