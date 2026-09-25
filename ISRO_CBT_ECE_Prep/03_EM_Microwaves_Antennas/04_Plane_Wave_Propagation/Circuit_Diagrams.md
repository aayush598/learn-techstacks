# Circuit Diagrams

## 1. Uniform Plane-Wave Field Geometry

For a uniform plane wave, `E`, `H`, and the propagation direction are mutually perpendicular. The Poynting direction is `E × H`, while the intrinsic impedance relates the field magnitudes.

```circuit
elm.SourceSin().right().at((-5, 0)).label("plane wave", loc="left")
elm.Block().at((0, 2)).label("E\nelectric field", loc="top")
elm.Block().at((3, 0)).label("H\nmagnetic field", loc="right")
elm.Block().at((0, -2)).label("k\npropagation +z", loc="bottom")
elm.Arrow().at((0, 0)).to((0, 2)).label("E ⊥ H", loc="right")
elm.Arrow().at((0, 0)).to((3, 0)).label("E × H = S", loc="top")
elm.Block().at((6, 0)).label("|E|/|H| = η", loc="right")
```

## 2. Lossless and Lossy Propagation

In a lossless medium, amplitude is constant and only phase changes with distance. In a lossy conductor, the propagation constant has attenuation and phase parts, with skin depth measuring the `1/e` amplitude depth.

```circuit
elm.SourceSin().right().at((-5, 1)).label("E(z,t)", loc="left")
elm.Arrow().at((-2, 1)).to((0, 1)).label("propagate", loc="top")
elm.Block().at((1, 1)).label("lossless\nα = 0, γ = jβ", loc="top")
elm.SourceSin().right().at((-5, -1)).label("E(z,t)", loc="left")
elm.Arrow().at((-2, -1)).to((0, -1)).label("conductor", loc="top")
elm.Block().at((1, -1)).label("γ = α + jβ\nδ = 1/α", loc="bottom")
elm.Block().at((6, 0)).label("E(z) = E₀e^(-αz)e^(j(ωt-βz))", loc="right")
```

## 3. Polarization States

Linear polarization keeps the electric-field tip on one line. Circular polarization has constant magnitude and a rotating field, while elliptical polarization is the general unequal-axis case.

```circuit
elm.SourceSin().right().at((-5, 0)).label("E field", loc="left")
elm.Arrow().at((-2, 0)).to((0, 0)).label("polarization", loc="top")
elm.Block().at((1, 2)).label("linear\nE along a fixed line", loc="top")
elm.Block().at((1, 0)).label("circular\nconstant |E|, rotating tip", loc="top")
elm.Block().at((1, -2)).label("elliptical\ngeneral two-axis case", loc="bottom")
elm.Arrow().at((3, 2)).to((5, 2)).label("vertical or horizontal", loc="top")
elm.Arrow().at((3, 0)).to((5, 0)).label("RH or LH", loc="top")
elm.Arrow().at((3, -2)).to((5, -2)).label("axial ratio", loc="bottom")
```

## 4. Poynting Vector and Average Power

The instantaneous Poynting vector gives energy-flow direction. For a sinusoidal traveling wave, the time-average power density is related to the squared field amplitude and intrinsic impedance.

```circuit
elm.Block().at((-5, 0)).label("E(t)", loc="left")
elm.Block().at((-2, 2)).label("H(t)", loc="top")
elm.Block().at((1, 0)).label("S = E × H", loc="right")
elm.Arrow().at((-3, 1)).to((0, 1)).label("cross product", loc="top")
elm.Arrow().at((0, 0)).to((3, 0)).label("energy flow", loc="top")
elm.Block().at((4, 0)).label("Savg = ½ Re(E × H*)", loc="right")
elm.Block().at((4, -2)).label("Pavg = |E₀|²/(2η)", loc="right")
```

## 5. Normal Incidence at a Boundary

At a normal-incidence boundary, the electric field splits into a reflected and a transmitted wave. The reflection coefficient depends only on the two intrinsic impedances for a normal interface.

```circuit
elm.SourceSin().right().at((-6, 0)).label("incident Eᵢ", loc="left")
elm.Line().right(4).at((-2, 0)).label("medium 1", loc="top")
elm.Line().right(4).at((-2, -2)).label("medium 2", loc="bottom")
elm.Arrow().at((-5, 0)).to((0, 0)).label("ΓE reflected", loc="top")
elm.Arrow().at((1, 0)).to((5, 0)).label("TE transmitted", loc="top")
elm.Block().at((0, 2)).label("boundary", loc="bottom")
elm.Block().at((6, 0)).label("Γ = (η₂-η₁)/(η₂+η₁)\nT = 1+Γ", loc="right")
```
