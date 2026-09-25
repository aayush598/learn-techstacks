# Circuit Diagrams

## 1. Distributed Transmission-Line Equivalent

A transmission line is modeled by series resistance and inductance together with shunt conductance and capacitance per unit length. Repeating the section represents a distributed line rather than one lumped element.

```circuit
elm.SourceSin().up().at((-6, 0)).label("source", loc="left")
elm.Resistor().right().at((-6, 3)).label("R", loc="top")
elm.Inductor().right().at((-3, 3)).label("L", loc="top")
elm.Dot().at((0, 3)).label("line section", loc="top")
elm.Capacitor().down().at((0, 3)).label("C", loc="right")
elm.Resistor().down().at((3, 3)).label("G", loc="right")
elm.Line().right(2).at((0, 3)).to((3, 3))
elm.Block().at((0, 5)).label("distributed line", loc="top")
elm.Block().at((6, 3)).label("Z₀ = √((R+jωL)/(G+jωC))", loc="right")
```

## 2. Characteristic Impedance and Phase Velocity

For a lossless line, the characteristic impedance depends on the per-unit-length inductance and capacitance, not on the total line length. The phase velocity and wavelength follow from the same distributed parameters.

```circuit
elm.Block().at((-5, 1)).label("L per unit length")
elm.Block().at((-5, -1)).label("C per unit length")
elm.Arrow().at((-2, 1)).to((0, 1)).label("series magnetic energy", loc="top")
elm.Arrow().at((-2, -1)).to((0, -1)).label("shunt electric energy", loc="top")
elm.Block().at((1, 0)).label("Z₀ = √(L/C)", loc="right")
elm.Block().at((5, 1)).label("vₚ = 1/√(LC)", loc="right")
elm.Block().at((5, -1)).label("λ = vₚ/f\nβ = 2π/λ", loc="right")
```

## 3. Load Reflection and VSWR

A mismatch at the load launches a reflected wave. The magnitude of the reflection coefficient controls the standing-wave ratio and therefore the voltage maxima and minima along the line.

```circuit
elm.SourceSin().right().at((-6, 0)).label("V⁺ incident", loc="left")
elm.Line().right(5).at((-3, 0)).label("Z₀ line", loc="top")
elm.Arrow().at((-2, 0)).to((1, 0)).label("V⁺", loc="top")
elm.Arrow().at((1, 0)).to((-2, 0)).label("V⁻ reflected", loc="bottom")
elm.Dot().at((1, 0)).label("ZL", loc="top")
elm.Resistor().down().at((1, 0)).label("load", loc="right")
elm.Block().at((4, 2)).label("ΓL = (ZL-Z₀)/(ZL+Z₀)", loc="top")
elm.Block().at((4, -2)).label("VSWR = (1+|Γ|)/(1-|Γ|)", loc="bottom")
```

## 4. Input-Impedance Transformation

The load impedance is transformed as the electrical length changes. A quarter-wave line inverts the impedance, while a half-wave line repeats the load impedance.

```circuit
elm.Block().at((-5, 0)).label("ZL")
elm.Arrow().at((-2, 0)).to((0, 0)).label("length l", loc="top")
elm.Block().at((1, 0)).label("Zin(l)")
elm.Arrow().at((4, 0)).to((6, 0)).label("observe at input", loc="top")
elm.Block().at((1, 2)).label("l = λ/4\nZin = Z₀²/ZL", loc="top")
elm.Block().at((1, -2)).label("l = λ/2\nZin = ZL", loc="bottom")
elm.Block().at((7, 0)).label("Z₀ = √(L/C)", loc="right")
```

## 5. Standing-Wave Power Flow

The incident power splits into reflected and delivered power. The delivered power is reduced by the reflection factor, while the standing-wave voltage ratio is visible as alternating maxima and minima.

```circuit
elm.SourceSin().right().at((-6, 0)).label("V⁺", loc="left")
elm.Arrow().at((-3, 0)).to((1, 0)).label("incident power", loc="top")
elm.Arrow().at((1, 0)).to((-3, 0)).label("reflected power", loc="bottom")
elm.Dot().at((-1, 0)).label("voltage max", loc="top")
elm.Dot().at((2, 0)).label("voltage min", loc="bottom")
elm.Block().at((4, 1)).label("PL = |V⁺|²(1-|Γ|²)/(2Z₀)", loc="right")
elm.Block().at((4, -1)).label("PR = |V⁺|²|Γ|²/(2Z₀)", loc="right")
elm.Block().at((7, 0)).label("maxima repeat every λ/2", loc="right")
```
