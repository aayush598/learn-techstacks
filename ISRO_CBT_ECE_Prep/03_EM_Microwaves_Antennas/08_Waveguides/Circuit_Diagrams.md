# Circuit Diagrams

## 1. Hollow-Waveguide Mode Families

A single-conductor hollow guide cannot support a TEM mode. It supports TE and TM families, with mode indices describing transverse field variation along the guide dimensions.

```circuit
elm.SourceI().right().at((-6, 0)).label("microwave input", loc="left")
elm.Block().at((-2, 0)).label("hollow metal guide", loc="top")
elm.Arrow().at((0, 0)).to((2, 0)).label("fields", loc="top")
elm.Block().at((3, 2)).label("TEₘₙ\nEz = 0", loc="top")
elm.Block().at((3, 0)).label("TMₘₙ\nHz = 0", loc="top")
elm.Block().at((3, -2)).label("TEM\nnot supported\nwithout center conductor", loc="bottom")
elm.Block().at((7, 0)).label("m,n: half-wave\nvariations", loc="right")
```

## 2. Rectangular TE10 Cutoff and Single-Mode Range

For a rectangular guide of width `a`, the dominant TE10 mode has the lowest cutoff. Operating above `f_c10` but below `f_c20` avoids the next longitudinal mode.

```circuit
elm.Block().at((-5, 1)).label("guide width a")
elm.Arrow().at((-2, 1)).to((0, 1)).label("cutoff relation", loc="top")
elm.Block().at((1, 1)).label("fc10 = c/(2a)\nλc = 2a", loc="top")
elm.Block().at((-5, -1)).label("frequency")
elm.Arrow().at((-2, -1)).to((0, -1)).label("classify", loc="bottom")
elm.Block().at((1, -1)).label("f < fc: evanescent\nf > fc: propagating", loc="bottom")
elm.Block().at((6, 0)).label("TE10-only range\nfc10 < f < fc20 = c/a", loc="right")
```

## 3. Guide Dispersion and Velocities

The guide wavelength is longer than the free-space wavelength, so the phase velocity can exceed `c` while the group velocity remains below `c`. Their product remains `c²`.

```circuit
elm.SourceSin().right().at((-6, 0)).label("wave", loc="left")
elm.Block().at((-2, 0)).label("λ0 = c/f", loc="top")
elm.Arrow().at((0, 0)).to((2, 0)).label("guide", loc="top")
elm.Block().at((3, 0)).label("λg = λ0/√(1-(fc/f)²)", loc="right")
elm.Block().at((1, 2)).label("vp = c/√(1-(fc/f)²)\nvp > c", loc="top")
elm.Block().at((1, -2)).label("vg = c√(1-(fc/f)²)\nvg < c", loc="bottom")
elm.Block().at((7, 0)).label("vp·vg = c²", loc="right")
```

## 4. Conductor and Dielectric Losses

Wall currents create conductor loss, while dielectric loss depends on the loss tangent. Skin depth limits how far fields and current penetrate a good conductor.

```circuit
elm.SourceSin().right().at((-6, 0)).label("guided wave", loc="left")
elm.Block().at((-2, 2)).label("wall currents\nconductor loss αc", loc="top")
elm.Block().at((-2, -2)).label("dielectric\nαd = k tanδ / 2", loc="bottom")
elm.Arrow().at((0, 0)).to((2, 0)).label("attenuation", loc="top")
elm.Block().at((3, 0)).label("γ = α + jβ", loc="right")
elm.Block().at((6, 0)).label("good conductor\nδ = 1/α\nα = β", loc="right")
elm.Block().at((1, 0)).label("smaller guide\n→ more loss", loc="bottom")
```

## 5. Practical Waveguide Source-Load Setup

A source feeds a guided line through a launcher, and a matched load terminates it. A movable short or detector section provides an experimental reference for reflection and propagation measurements.

```circuit
elm.SourceV().up().at((-6, 0)).label("microwave source", loc="left")
elm.Line().right(2).at((-6, 3)).label("launcher", loc="top")
elm.Block().at((-3, 3)).label("TE10 guide", loc="top")
elm.Dot().at((0, 3)).label("measurement plane", loc="top")
elm.Line().right(3).at((0, 3))
elm.Block().at((3, 3)).label("movable short\nor detector", loc="top")
elm.Line().right(2).at((5, 3))
elm.Resistor().right().at((6, 3)).label("matched load", loc="bottom")
elm.Line().down(3).at((9, 3))
elm.Line().left(15).at((9, 0)).to((-6, 0))
elm.Ground().at((-6, 0))
elm.Block().at((0, 0)).label("source → guide → load", loc="bottom")
```

## 6. Circular Guide and Resonant Cavity

Circular waveguides use Bessel-root mode labels, with TE11 as the dominant mode. A shorted guide section behaves as a high-Q cavity used for filtering and oscillation.

```circuit
elm.SourceI().right().at((-6, 0)).label("microwave input", loc="left")
elm.Block().at((-2, 0)).label("circular guide", loc="top")
elm.Arrow().at((0, 0)).to((2, 0)).label("mode", loc="top")
elm.Block().at((3, 1)).label("TE11 dominant\nroot 1.841", loc="top")
elm.Block().at((3, -1)).label("TM01\nroot 2.405", loc="bottom")
elm.Line().right(2).at((5, 0))
elm.Line().right(2).at((5, 0)).label("shorted section", loc="top")
elm.Block().at((8, 0)).label("cavity resonator\nhigh Q", loc="right")
```
