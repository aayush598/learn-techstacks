# Circuit Diagrams

## 1. Normalized Impedance and Reflection Plane

The Smith chart maps a normalized load impedance `z = Z/Z₀` to the reflection coefficient `Γ = (z-1)/(z+1)`. The center represents a matched load, while the unit circle represents a perfect reflection.

```circuit
elm.Block().at((-5, 0)).label("Z load")
elm.Block().at((-2, 0)).label("Z₀ reference")
elm.Arrow().at((-1, 0)).to((1, 0)).label("normalize", loc="top")
elm.Block().at((2, 0)).label("z = Z/Z₀")
elm.Arrow().at((5, 0)).to((7, 0)).label("map", loc="top")
elm.Block().at((8, 0)).label("Γ = (z-1)/(z+1)", loc="right")
elm.Block().at((2, -2)).label("center: z=1, Γ=0", loc="bottom")
elm.Block().at((8, -2)).label("outer circle: |Γ|=1", loc="bottom")
```

## 2. Reading Constant-Value Curves

Constant-resistance circles, constant-reactance arcs, and constant-`|Γ|` circles answer different chart questions. The upper half represents positive reactance and the lower half negative reactance.

```circuit
elm.Dot().at((0, 0)).label("chart center\nz = 1", loc="top")
elm.Block().at((0, 3)).label("constant R\ncircles", loc="top")
elm.Block().at((3, 0)).label("constant X\narcs", loc="right")
elm.Block().at((0, -3)).label("constant |Γ|\nconstant VSWR", loc="bottom")
elm.Block().at((-3, 0)).label("top: +jX\nbottom: -jX", loc="left")
elm.Block().at((6, 0)).label("VSWR = (1+|Γ|)/(1-|Γ|)", loc="right")
```

## 3. Rotation Along a Transmission Line

Moving a fixed electrical length away from the load rotates the reflection coefficient on the chart. A half wavelength makes one complete revolution, while a quarter wavelength gives the diametrically opposite admittance point.

```circuit
elm.Block().at((-5, 0)).label("ΓL\nload point")
elm.Arrow().at((-2, 0)).to((0, 0)).label("move distance d", loc="top")
elm.Block().at((1, 0)).label("Γ(d)")
elm.Arrow().at((4, 0)).to((6, 0)).label("θ = 2βd", loc="top")
elm.Block().at((7, 0)).label("input point", loc="right")
elm.Block().at((1, 2)).label("d = λ/2\n360° rotation", loc="top")
elm.Block().at((1, -2)).label("d = λ/4\n180° rotation\nz → 1/z", loc="bottom")
```

## 4. Single-Stub Tuning Procedure

The load is moved along the constant-`|Γ|` circle to a point where normalized conductance is one. A short-circuited or open-circuited stub then supplies the susceptance needed to reach the center.

```circuit
elm.SourceSin().right().at((-6, 0)).label("source", loc="left")
elm.Line().right(3).at((-3, 0)).label("line", loc="top")
elm.Dot().at((-1, 0)).label("stub point d", loc="top")
elm.Line().down(2).at((-1, 0)).label("stub", loc="right")
elm.Block().at((-1, -3)).label("open or short", loc="bottom")
elm.Line().right(3).at((1, 0))
elm.Resistor().right().at((2, 0)).label("ZL", loc="bottom")
elm.Block().at((5, 2)).label("step 1: Re(y)=1", loc="right")
elm.Block().at((5, -2)).label("step 2: cancel Im(y)", loc="right")
```

## 5. Impedance, Admittance, and Match

Impedance and normalized admittance are reciprocal quantities, `y = 1/z`, and are read at diametrically opposite chart points. The final match is the center condition `z=1` and `Γ=0`.

```circuit
elm.Block().at((-4, 1)).label("z\nimpedance point")
elm.Arrow().at((-1, 1)).to((1, 1)).label("180°", loc="top")
elm.Block().at((2, 1)).label("y = 1/z\nadmittance point")
elm.Block().at((-4, -1)).label("VSWR read\nfrom |Γ| circle")
elm.Arrow().at((-1, -1)).to((1, -1)).label("normalize", loc="bottom")
elm.Block().at((2, -1)).label("match: z=1\nΓ=0, VSWR=1", loc="bottom")
elm.Block().at((6, 0)).label("same chart,\nimpedance or admittance view", loc="right")
```
