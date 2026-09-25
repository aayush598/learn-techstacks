# Circuit Diagrams

## 1. Differentiating RC High-Pass Network

A series capacitor with a resistive load emphasizes rapid changes in the input. With an ideal op-amp differentiator, the same transfer shape is obtained from a proportional path and an inverse-time feedback element.

```circuit
elm.SourceSin().up().at((-3, 0)).label("vin", loc="left")
elm.Capacitor().right().at((-3, 3)).label("C 1 uF", loc="top")
elm.Dot().at((-1.5, 3)).label("vout", loc="right")
elm.Resistor().down().at((-1.5, 3)).label("R 10k", loc="right")
elm.Line().down(3).at((-1.5, 0))
elm.Line().left().at((-1.5, -3))
elm.Line().up(3).at((-3, -3)).to((-3, 0))
```

## 2. Integrating RC Low-Pass Network

The capacitor voltage changes in proportion to the difference between input and output. At frequencies well below the corner frequency, the output is approximately the time integral of the input scaled by `RC`.

```circuit
elm.SourceSin().up().at((-4, 0)).label("vin", loc="left")
elm.Resistor().right().at((-4, 3)).label("R 10k", loc="top")
elm.Dot().at((-1, 3)).label("vout", loc="right")
elm.Capacitor().down().at((-1, 3)).label("C 1 uF", loc="right")
elm.Ground().at((-1, 0))
elm.Line().left().at((-1, 0)).to((-4, 0))
```

## 3. Op-Amp Integrator

The capacitor in the feedback path makes the closed-loop gain proportional to `1/(sRC)`. The inverting input is a virtual ground, so all input current flows through the feedback capacitor except for practical offset and bias effects.

```circuit
op = elm.Opamp(leads=True).label("U1", loc="center")
elm.Ground().at(op.in2)
rin = elm.Resistor().left().at(op.in1).idot().label("R 10k", loc="bottom")
elm.SourceV().up().reverse().at(rin.start).label("vin", loc="left")
elm.Capacitor().tox(op.out).label("C 1 uF", loc="top")
elm.Line().toy(op.out).dot()
elm.Line().right().at(op.out).label("vout = -(1/RC) integral(vin) dt", loc="right")
```

## 4. Laplace-Domain Series RLC Loop

Replacing derivatives by `s` factors gives the impedance relation `Z(s) = R + sL + 1/(sC)`. The diagram represents the physical series loop rather than drawing algebraic operators as components.

```circuit
elm.SourceV().up().at((0, 0)).label("V(s)", loc="left")
elm.Resistor().right().at((0, 3)).label("R", loc="top")
elm.Inductor().down().at((3, 3)).label("sL", loc="right")
elm.Capacitor().left().at((3, 0)).label("1/(sC)", loc="bottom")
elm.Dot().at((0, 0)).label("reference", loc="left")
elm.Ground().at((0, 0))
```

## 5. Newton Update as a Signal-Flow Loop

Newton's method repeatedly evaluates a function and its derivative, then moves the current estimate in the direction that reduces the error. The loop is a mathematical signal flow rather than a passive electrical circuit.

```circuit
elm.SourceI().right().at((-5, 0)).label("x(k)")
elm.Arrow().right().at((-3, 0)).to((-1, 0)).label("evaluate", loc="top")
elm.Dot().at((-1, 0)).label("f(xk), df/dx", loc="top")
elm.Arrow().right().at((-1, -1)).to((2, -1)).label("ratio", loc="top")
elm.Dot().at((2, 0)).label("update", loc="right")
elm.Arrow().right().at((2, 0)).to((5, 0)).label("x(k+1)", loc="right")
elm.Line().down().at((-1, -1)).to((-1, 0))
elm.Line().down(2).at((5, 0)).to((5, -2))
elm.Line().left().at((5, -2)).to((-5, -2))
elm.Line().up().at((-5, -2)).to((-5, 0))
```
