# Circuit Diagrams

## 1. Source-Load Mismatch

A source impedance and a load impedance produce a reflection unless their real reference values are matched. Return loss and VSWR are useful indicators of the mismatch.

```circuit
elm.SourceV().up().at((-5, 0)).label("source", loc="left")
elm.Resistor().right().at((-5, 3)).label("Z₀", loc="top")
elm.Line().right(3).at((-2, 3)).label("transmission line", loc="top")
elm.Dot().at((1, 3)).label("load node", loc="top")
elm.Resistor().down().at((1, 3)).label("ZL", loc="right")
elm.Line().down(3).at((1, 3))
elm.Line().left(6).at((1, 0)).to((-5, 0))
elm.Ground().at((-5, 0))
elm.Block().at((4, 2)).label("Γ = (ZL-Z₀)/(ZL+Z₀)", loc="right")
elm.Block().at((4, -2)).label("VSWR = (1+|Γ|)/(1-|Γ|)", loc="right")
```

## 2. Quarter-Wave Transformer

A quarter-wave section uses `Z_q = √(Z₀Z_L)` for real impedances. At the design frequency, the transformer transforms the load to the source reference impedance.

```circuit
elm.SourceV().up().at((-5, 0)).label("Z₀ source", loc="left")
elm.Line().right(2).at((-5, 3))
elm.Block().at((-3, 3)).label("Zq section\nlength λ/4", loc="top")
elm.Line().right(2).at((0, 3))
elm.Resistor().right().at((0, 3)).label("ZL", loc="bottom")
elm.Line().down(3).at((3, 3))
elm.Line().left(8).at((3, 0)).to((-5, 0))
elm.Ground().at((-5, 0))
elm.Block().at((-3, 0)).label("Zq = √(Z₀ZL)", loc="bottom")
elm.Block().at((2, 0)).label("Zin = Zq²/ZL = Z₀", loc="right")
```

## 3. Single-Stub Reactive Match

The stub location is chosen from the normalized admittance and its length supplies only susceptance. This makes a general complex load matchable without changing the main-line impedance.

```circuit
elm.SourceV().up().at((-6, 0)).label("Z₀", loc="left")
elm.Line().right(3).at((-6, 3)).label("main line", loc="top")
elm.Dot().at((-3, 3)).label("d", loc="top")
elm.Line().down(2).at((-3, 3))
elm.Block().at((-3, 0)).label("stub length", loc="bottom")
elm.Line().right(4).at((-1, 3))
elm.Resistor().right().at((1, 3)).label("ZL", loc="bottom")
elm.Line().down(3).at((4, 3))
elm.Line().left(10).at((4, 0)).to((-6, 0))
elm.Ground().at((-6, 0))
elm.Block().at((6, 2)).label("Re(y)=1\nchoose d", loc="right")
elm.Block().at((6, -2)).label("Bstub = -Im(y)\nchoose stub length", loc="right")
```

## 4. Double-Stub Tuner

Two independently adjustable stubs provide more tuning freedom than one stub. The spacing is fixed, while each stub length is varied to cancel the residual reflection.

```circuit
elm.SourceV().up().at((-6, 0)).label("Z₀", loc="left")
elm.Line().right(3).at((-6, 3)).label("fixed spacing", loc="top")
elm.Dot().at((-3, 3)).label("stub 1", loc="top")
elm.Line().down(2).at((-3, 3))
elm.Block().at((-3, 0)).label("tune l1", loc="bottom")
elm.Line().right(3).at((-1, 3))
elm.Dot().at((2, 3)).label("stub 2", loc="top")
elm.Line().down(2).at((2, 3))
elm.Block().at((2, 0)).label("tune l2", loc="bottom")
elm.Line().right(3).at((4, 3))
elm.Resistor().right().at((4, 3)).label("ZL", loc="bottom")
elm.Line().down(3).at((7, 3))
elm.Line().left(13).at((7, 0)).to((-6, 0))
elm.Ground().at((-6, 0))
elm.Block().at((9, 2)).label("Γ=0 at matched load", loc="right")
```

## 5. Lumped L-Match

A series reactance followed by a shunt reactance forms a two-element L network. The quality factor controls the reactance magnitude and therefore the usable bandwidth.

```circuit
elm.SourceV().up().at((-5, 0)).label("Rs", loc="left")
elm.Line().right(2).at((-5, 3))
elm.Inductor().right().at((-3, 3)).label("Xs = QRs", loc="top")
elm.Dot().at((0, 3)).label("junction", loc="top")
elm.Capacitor().down().at((0, 3)).label("Xp = RL/Q", loc="right")
elm.Line().right(2).at((1, 3))
elm.Resistor().right().at((2, 3)).label("RL", loc="bottom")
elm.Line().down(3).at((5, 3))
elm.Line().left(10).at((5, 0)).to((-5, 0))
elm.Ground().at((-5, 0))
elm.Block().at((1, 0)).label("Q = √(RL/Rs - 1)\nbandwidth ∝ 1/Q", loc="bottom")
```

## 6. Tapered-Line Match

A tapered line changes characteristic impedance gradually instead of switching at one discontinuity. The gradual transition reduces reflections over a broader frequency range.

```circuit
elm.SourceV().up().at((-6, 0)).label("Z₀ source", loc="left")
elm.Block().right().at((-6, 3)).label("Z₀", loc="top")
elm.Arrow().at((-3, 3)).to((0, 3)).label("gradual Z(z)", loc="top")
elm.Block().at((1, 3)).label("tapered line\nexponential or Klopfenstein", loc="top")
elm.Arrow().at((4, 3)).to((6, 3)).label("impedance transition", loc="top")
elm.Resistor().right().at((6, 3)).label("ZL", loc="bottom")
elm.Line().down(3).at((9, 3))
elm.Line().left(15).at((9, 0)).to((-6, 0))
elm.Ground().at((-6, 0))
elm.Block().at((1, 0)).label("broadband match\nlow reflection", loc="bottom")
```
