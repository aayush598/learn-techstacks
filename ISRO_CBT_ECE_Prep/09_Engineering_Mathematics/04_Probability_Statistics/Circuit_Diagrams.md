# Circuit Diagrams

## 1. Bayes Updating with Competing Hypotheses

Prior probabilities for two hypotheses feed a likelihood block. Normalizing the resulting weights produces the posterior probabilities; the drawing is a probability signal flow.

```circuit
elm.Line().right(1).at((-5, 1)).label("P(H1)")
elm.Line().right(1).at((-5, -1)).label("P(H2)")
elm.Dot().at((-2, 0)).label("evidence E", loc="top")
elm.Arrow().right().at((-4, 1)).to((-3, 1)).label("P(E|H1)", loc="top")
elm.Arrow().right().at((-4, -1)).to((-3, -1)).label("P(E|H2)", loc="top")
elm.Line().up(1).at((-3, -1)).to((-3, 1))
elm.Arrow().right().at((-2, 0)).to((1, 0)).label("unnormalized", loc="top")
elm.Arrow().right().at((1, 0)).to((4, 0)).label("posterior", loc="top")
elm.Dot().at((1, 0)).label("normalize", loc="bottom")
```

## 2. Central-Limit Summing Structure

The sum of many independent contributions tends toward a distribution described mainly by its mean and variance. The three branches illustrate the repeated addition; the diagram is a signal-flow model, not a physical claim about ordinary resistor noise alone.

```circuit
elm.SourceI().right().at((-5, 2)).label("X1")
elm.SourceI().right().at((-5, 0)).label("X2")
elm.SourceI().right().at((-5, -2)).label("X3")
elm.Dot().at((0, 0)).label("sum", loc="right")
elm.Arrow().right().at((-3, 2)).to((0, 2))
elm.Arrow().right().at((-3, 0)).to((0, 0))
elm.Arrow().right().at((-3, -2)).to((0, -2))
elm.Line().up(2).at((0, -2)).to((0, 2))
elm.Arrow().right().at((0, 0)).to((4, 0)).label("approximately normal", loc="top")
```

## 3. Three-State Markov Chain

Each state emits the next state with a labeled transition probability. The transition arrows form a directed graph, which is the natural representation of a discrete-time Markov process.

```circuit
elm.Dot().at((-3, 2)).label("S1", loc="left")
elm.Dot().at((2, 2)).label("S2", loc="right")
elm.Dot().at((0, -2)).label("S3", loc="right")
elm.Arrow().right().at((-3, 2)).to((2, 2)).label("P12", loc="top")
elm.Arrow().right().at((-3, 2)).to((0, -2)).label("P13", loc="top")
elm.Arrow().left().at((2, 2)).to((-3, 2)).label("P21", loc="bottom")
elm.Arrow().right().at((2, 2)).to((0, -2)).label("P23", loc="top")
elm.Arrow().left().at((0, -2)).to((-3, 2)).label("P31", loc="top")
elm.Arrow().left().at((0, -2)).to((2, 2)).label("P32", loc="bottom")
```

## 4. Series Reliability Chain

For independent components in a series chain, system success requires every element to succeed, so the reliabilities multiply.

```circuit
elm.SourceV().up().at((-3, 0)).label("supply", loc="left")
elm.Line().up(1).at((-3, 3))
elm.Switch().right().at((-3, 4)).label("A", loc="top")
elm.Switch().right().at((-1, 4)).label("B", loc="top")
elm.Switch().right().at((1, 4)).label("C", loc="top")
elm.Line().right(1).at((3, 4)).label("system works", loc="right")
elm.Line().down(6).at((4, 4))
elm.Line().left().at((4, -2))
elm.Line().left().at((3, -2))
elm.Line().left().at((2, -2))
elm.Line().left().at((1, -2))
elm.Line().left().at((0, -2))
elm.Line().up(2).at((-3, -2)).to((-3, 0))
```

## 5. Parallel Reliability Paths

Two independent branches are connected across the same supply. The system succeeds when at least one branch succeeds, so the failure probabilities multiply.

```circuit
elm.SourceV().up().at((-2, 0)).label("supply", loc="left")
elm.Line().up(1).at((-2, 3)).dot()
elm.Switch().right().at((-2, 4)).label("A")
elm.Line().right(1).at((0, 4)).dot()
elm.Line().down().at((1, 4))
elm.Switch().right().at((1, 3)).label("B")
elm.Line().right(1).at((3, 3)).dot()
elm.Line().right(1).at((4, 3))
elm.Line().down(5).at((5, 3))
elm.Line().left().at((5, -2))
elm.Line().up().at((-2, -2)).to((-2, 0))
elm.Line().right().at((-2, -2)).to((5, -2))
elm.Line().up(3).at((1, 3)).to((1, 0))
elm.Dot().at((-2, 0)).label("return", loc="left")
```
