# Circuit Diagrams

## 1. Point Charge and Electric Field

A point charge produces a radial electric field that decreases as `1/r²`. The potential is a scalar, while the field arrows point away from a positive charge and toward a negative charge.

```circuit
elm.Dot().at((0, 0)).label("+Q", loc="top")
elm.Arrow().at((0, 0)).to((3, 0)).label("E outward", loc="top")
elm.Arrow().at((0, 0)).to((-3, 0)).label("E outward", loc="top")
elm.Arrow().at((0, 0)).to((0, 3)).label("E", loc="right")
elm.Block().at((4, 0)).label("E = Q/(4πε₀r²) âr", loc="right")
elm.Block().at((4, -2)).label("V = Q/(4πε₀r)", loc="right")
```

## 2. Gauss Surface and Electric Flux

For a symmetric charge distribution, a closed Gaussian surface converts the total flux into the enclosed charge. Superposition allows multiple point charges to be handled as a vector sum.

```circuit
elm.Dot().at((0, 0)).label("Q_enc", loc="top")
elm.Line().right(3).at((-3, 3))
elm.Line().up(3).at((3, 3))
elm.Line().left(3).at((3, -3))
elm.Line().down(3).at((-3, -3)).to((-3, 3))
elm.Arrow().at((0, 0)).to((3, 0)).label("D·dA", loc="top")
elm.Block().at((5, 0)).label("∮S D·dA = Q_enc", loc="right")
elm.Block().at((5, -2)).label("∇·D = ρv", loc="right")
```

## 3. Capacitor Voltage and Stored Energy

The capacitor voltage is related to charge by `C = Q/V`; its electric energy is stored in the dielectric. The source and capacitor form a closed charging loop, with the return rail tied to the source negative terminal.

```circuit
elm.SourceV().up().at((0, 0)).label("V", loc="left")
elm.Line().right(2).at((0, 3))
elm.Capacitor().right().at((2, 3)).label("C", loc="bottom")
elm.Line().right(2).at((5, 3))
elm.Line().down(3).at((7, 3))
elm.Line().left(7).at((7, 0)).to((0, 0))
elm.Ground().at((0, 0))
elm.Block().at((3, -2)).label("W = ½CV² = ½QV", loc="bottom")
```

## 4. Current-Loop Magnetic Field

A current element creates a magnetic field by the Biot-Savart law. Around a straight conductor the field circles the wire, and the magnetic field strength for an ideal infinite wire falls as `1/ρ`.

```circuit
elm.SourceI().up().at((0, -3)).label("I", loc="left")
elm.Line().up(6).at((0, 3)).label("current wire", loc="right")
elm.Arrow().at((0, 0)).to((3, 0)).label("B circles wire", loc="top")
elm.Arrow().at((0, 0)).to((-3, 0)).label("B", loc="top")
elm.Arrow().at((0, 0)).to((0, 3)).label("B", loc="right")
elm.Block().at((5, 0)).label("B = μ₀I/(2πρ) âφ", loc="right")
elm.Block().at((5, -2)).label("dB ∝ I dl×âr/r²", loc="right")
```

## 5. Solenoid and Magnetic Energy

A solenoid converts current into an approximately uniform internal magnetic field. The same field links the turns to produce inductance and magnetic energy.

```circuit
elm.SourceI().up().at((-4, -3)).label("I", loc="left")
elm.Line().right(2).at((-4, 0))
elm.Block().at((-1, 0)).label("N turns\nsolenoid", loc="top")
elm.Line().right(2).at((2, 0))
elm.Resistor().right().at((2, 0)).label("coil L", loc="bottom")
elm.Line().down(3).at((5, 0))
elm.Line().left(9).at((5, -3)).to((-4, -3))
elm.Ground().at((-4, -3))
elm.Block().at((0, 2)).label("B = μ₀nI\ninside")
elm.Block().at((3, -2)).label("Wₘ = ½LI²", loc="bottom")
```
