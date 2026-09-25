# Circuit Diagrams

## 1. Discrete Diffusion by an RC Ladder

A diffusion equation is analogous to charge or heat spreading through neighboring cells. The shunt capacitors store the local state, while the series elements provide coupling between neighboring nodes.

```circuit
elm.SourceV().up().at((-6, 0)).label("boundary value", loc="left")
elm.Resistor().right().at((-6, 3)).label("R12", loc="top")
elm.Dot().at((-3, 3)).label("u1", loc="top")
elm.Resistor().right().at((-3, 3)).label("R23", loc="top")
elm.Dot().at((0, 3)).label("u2", loc="top")
elm.Resistor().right().at((0, 3)).label("R34", loc="top")
elm.Dot().at((3, 3)).label("u3", loc="top")
elm.Capacitor().down().at((-3, 3)).label("C1", loc="right")
elm.Capacitor().down().at((0, 3)).label("C2", loc="right")
elm.Capacitor().down().at((3, 3)).label("C3", loc="right")
elm.Line().right(2).at((3, 3)).label("diffusive boundary", loc="right")
elm.Line().down(3).at((5, 3))
elm.Line().left(11).at((5, 0))
elm.Line().up().at((-6, 0)).to((-6, 0))
```

## 2. One-Dimensional Laplace RC Network

Repeated series resistors and shunt capacitors form the electrical analogue of a one-dimensional diffusion operator. Increasing the number of sections improves spatial resolution.

```circuit
elm.SourceV().up().at((-6, 0)).label("V(x=0)", loc="left")
elm.Resistor().right().at((-6, 3)).label("R", loc="top")
elm.Dot().at((-3, 3)).label("V1", loc="top")
elm.Resistor().right().at((-3, 3)).label("R", loc="top")
elm.Dot().at((0, 3)).label("V2", loc="top")
elm.Resistor().right().at((0, 3)).label("R", loc="top")
elm.Dot().at((3, 3)).label("V3", loc="top")
elm.Capacitor().down().at((-3, 3)).label("C", loc="right")
elm.Capacitor().down().at((0, 3)).label("C", loc="right")
elm.Capacitor().down().at((3, 3)).label("C", loc="right")
elm.Line().right(2).at((3, 3)).label("x", loc="right")
elm.Line().down(3).at((5, 3))
elm.Line().left(11).at((5, 0))
elm.Line().up().at((-6, 0)).to((-6, 0))
```

## 3. Lossless Wave Line as an LC Ladder

A lossless transmission line is represented by repeated series inductors and shunt capacitors. The state variables alternate between magnetic energy in the inductors and electric energy in the capacitors.

```circuit
elm.SourceV().up().at((-6, 0)).label("input", loc="left")
elm.Inductor().right().at((-6, 3)).label("L", loc="top")
elm.Dot().at((-3, 3)).label("node 1", loc="top")
elm.Inductor().right().at((-3, 3)).label("L", loc="top")
elm.Dot().at((0, 3)).label("node 2", loc="top")
elm.Inductor().right().at((0, 3)).label("L", loc="top")
elm.Dot().at((3, 3)).label("node 3", loc="top")
elm.Capacitor().down().at((-3, 3)).label("C", loc="right")
elm.Capacitor().down().at((0, 3)).label("C", loc="right")
elm.Capacitor().down().at((3, 3)).label("C", loc="right")
elm.Line().right(2).at((3, 3)).label("load", loc="right")
elm.Line().down(3).at((5, 3))
elm.Line().left(11).at((5, 0))
elm.Line().up().at((-6, 0)).to((-6, 0))
```

## 4. Thermal Conduction as Resistance

For steady one-dimensional conduction, heat flow follows Ohm's law with thermal resistance `Rth = L/(kA)`. The electrical drawing is a direct physical analogue, not an electrical heater circuit.

```circuit
elm.SourceV().up().at((0, 0)).label("T_hot", loc="left")
elm.Resistor().right().at((0, 3)).label("Rth = L/(kA)", loc="top")
elm.Dot().at((3, 3)).label("interior node", loc="top")
elm.Resistor().right().at((3, 3)).label("Rth", loc="top")
elm.Line().right(2).at((6, 3)).label("T_cold", loc="right")
elm.Capacitor().down().at((3, 3)).label("thermal storage", loc="right")
elm.Line().down(3).at((3, 0))
elm.Line().left(3).at((3, 0)).to((0, 0))
```

## 5. Boundary Source and Terminating Load

A transmission-line model places a source at one boundary and a load at the other. Reflections occur when the line impedance does not match the terminating impedance.

```circuit
elm.SourceSin().up().at((-6, 0)).label("source", loc="left")
elm.Line().up(1).at((-6, 3)).label("Zin", loc="left")
elm.Inductor().right().at((-6, 4)).label("distributed L", loc="top")
elm.Capacitor().down().at((-3, 4)).label("distributed C", loc="right")
elm.Inductor().right().at((-3, 4)).label("distributed L", loc="top")
elm.Capacitor().down().at((0, 4)).label("distributed C", loc="right")
elm.Line().right(1).at((0, 4)).dot()
elm.Resistor().down().at((1, 4)).label("ZL", loc="right")
elm.Line().down(3).at((1, 1))
elm.Line().left(7).at((1, -2))
elm.Line().up(2).at((-6, -2)).to((-6, 0))
```
