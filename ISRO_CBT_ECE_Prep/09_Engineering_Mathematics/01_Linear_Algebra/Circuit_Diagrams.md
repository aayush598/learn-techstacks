# Circuit Diagrams

## 1. Vector Addition as a Signal-Flow Operation

Two input signals meet at a summing node. The output is the component-wise sum, with the physical interpretation determined by the signals carried on the branches.

```circuit
elm.SourceI().right().at((-4, 1)).label("x(t)", loc="left")
elm.SourceI().right().at((-4, -1)).label("y(t)", loc="left")
elm.Dot().at((0, 0)).label("sum", loc="right")
elm.Arrow().right().at((-3, 1)).to((0, 1)).label("x")
elm.Arrow().right().at((-3, -1)).to((0, -1)).label("y")
elm.Line().up(1).at((0, -1)).to((0, 1))
elm.Arrow().right().at((0, 0)).to((3, 0)).label("x + y")
```

## 2. Matrix-Vector Multiplication as a Weighted Merge

Each input component is scaled by the corresponding matrix coefficient before the contributions are summed. This is a signal-flow equivalent, not a claim that ordinary resistors implement matrix arithmetic by themselves.

```circuit
elm.Line().right(2).at((-4, 2)).label("x1")
elm.Line().right(2).at((-4, 0)).label("x2")
elm.Line().right(2).at((-4, -2)).label("x3")
elm.Dot().at((0, 0)).label("sum", loc="right")
elm.Arrow().right().at((-2, 2)).to((0, 2)).label("a11 x1", loc="top")
elm.Arrow().right().at((-2, 0)).to((0, 0)).label("a21 x2", loc="top")
elm.Arrow().right().at((-2, -2)).to((0, -2)).label("a31 x3", loc="bottom")
elm.Line().up(2).at((0, -2)).to((0, 2))
elm.Arrow().right().at((0, 0)).to((4, 0)).label("Ax")
```

## 3. Basis Decomposition

A vector is expressed as a weighted sum of basis vectors. The coefficients select how much of each basis component is present.

```circuit
elm.SourceI().right().at((-5, 0)).label("v")
elm.Arrow().right().at((-3, 0)).to((-1, 0))
elm.Dot().at((-1, 0)).label("split", loc="top")
elm.Arrow().right().at((-1, 0)).to((1, 2)).label("c1")
elm.Arrow().right().at((-1, 0)).to((1, 0)).label("c2")
elm.Arrow().right().at((-1, 0)).to((1, -2)).label("c3")
elm.Line().right(1).at((1, 2)).label("b1")
elm.Line().right(1).at((1, 0)).label("b2")
elm.Line().right(1).at((1, -2)).label("b3")
```

## 4. Eigenvector Mode

An eigenvector is unchanged in direction by a linear transformation; only its scale changes. The loop represents the relation `Ax = lambda x`.

```circuit
elm.SourceI().right().at((-4, 0)).label("x")
elm.Arrow().right().at((-2, 0)).to((0, 0)).label("A", loc="top")
elm.Dot().at((0, 0)).label("Ax", loc="top")
elm.Arrow().right().at((0, -1)).to((2, -1)).label("scale by lambda", loc="top")
elm.Arrow().up().at((2, -1)).to((2, 0))
elm.Line().down(2).at((-4, 0)).to((-4, -2))
elm.Line().right().at((-4, -2)).to((2, -2))
elm.Line().up().at((2, -2)).to((2, -1))
elm.Line().label("same direction", loc="bottom")
```
