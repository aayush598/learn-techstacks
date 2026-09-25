# Circuit Diagrams

## 1. The Four Maxwell Relations

The four equations relate electric charge, magnetic flux, induced electric fields, and the conduction plus displacement currents. The arrows show the source quantity on the left and the resulting field relation on the right.

```circuit
elm.SourceI().right().at((-5, 3)).label("ρv", loc="left")
elm.Arrow().at((-2, 3)).to((0, 3)).label("electric source", loc="top")
elm.Block().at((1, 3)).label("∇·D = ρv")
elm.SourceI().right().at((-5, 1)).label("B", loc="left")
elm.Arrow().at((-2, 1)).to((0, 1)).label("no monopoles", loc="top")
elm.Block().at((1, 1)).label("∇·B = 0")
elm.SourceI().right().at((-5, -1)).label("∂B/∂t", loc="left")
elm.Arrow().at((-2, -1)).to((0, -1)).label("induction", loc="top")
elm.Block().at((1, -1)).label("∇×E = -∂B/∂t")
elm.SourceI().right().at((-5, -3)).label("J, ∂D/∂t", loc="left")
elm.Arrow().at((-2, -3)).to((0, -3)).label("magnetomotive source", loc="top")
elm.Block().at((1, -3)).label("∇×H = J + ∂D/∂t")
```

## 2. Faraday Induction Loop

A time-varying magnetic flux through a loop produces an electric-field circulation with the opposite sign. The loop and surface are generic representations of the integral law.

```circuit
elm.Line().right(4).at((-4, 0))
elm.Line().up(3).at((4, 0))
elm.Line().left(4).at((4, 3))
elm.Line().down(3).at((-4, 3)).to((-4, 0))
elm.Block().at((0, 1.5)).label("∂ΦB/∂t", loc="top")
elm.Arrow().at((0, 0)).to((0, -2)).label("changing B", loc="right")
elm.Block().at((0, -3)).label("∮C E·dl = -dΦB/dt", loc="bottom")
elm.Block().at((6, 0)).label("∇×E = -∂B/∂t", loc="right")
```

## 3. Ampere-Maxwell Current Balance

Ampere's law includes conduction current `J` and displacement current `∂D/∂t`. The displacement-current branch is what allows time-varying electric fields to support electromagnetic-wave propagation.

```circuit
elm.SourceI().right().at((-5, 2)).label("J", loc="left")
elm.Arrow().at((-2, 2)).to((0, 2)).label("conduction current", loc="top")
elm.SourceI().right().at((-5, 0)).label("∂D/∂t", loc="left")
elm.Arrow().at((-2, 0)).to((0, 0)).label("displacement current", loc="top")
elm.Dot().at((2, 1)).label("sum", loc="right")
elm.Block().at((3, 1)).label("∮H·dl = I_enc + dΦD/dt", loc="right")
elm.Block().at((3, -2)).label("enables EM waves", loc="right")
```

## 4. Boundary Conditions Between Two Media

At a dielectric interface, tangential electric field is continuous and normal electric displacement changes by surface charge. The corresponding magnetic conditions use normal `B` and tangential `H`.

```circuit
elm.Line().right(8).at((-4, 0)).label("medium 1", loc="top")
elm.Line().right(8).at((-4, -2)).label("medium 2", loc="bottom")
elm.Arrow().at((-2, 1)).to((0, 1)).label("E₁t = E₂t", loc="top")
elm.Arrow().at((1, 1)).to((3, 1)).label("B₁n = B₂n", loc="top")
elm.Block().at((0, -1)).label("D₁n - D₂n = ρs", loc="top")
elm.Block().at((3, -1)).label("H₁t - H₂t = Ks", loc="top")
elm.Dot().at((0, 0)).label("interface", loc="left")
```

## 5. Maxwell to Wave Equation

Taking the curl of Faraday's law and using the vector identity for the curl of a curl leads to the free-space wave equation. The same structure applies to the magnetic field.

```circuit
elm.Block().at((-5, 0)).label("Maxwell\ncurl laws")
elm.Arrow().at((-2, 0)).to((0, 0)).label("take curl", loc="top")
elm.Block().at((1, 0)).label("∇×(∇×E)")
elm.Arrow().at((4, 0)).to((6, 0)).label("identity + constitutive laws", loc="top")
elm.Block().at((7, 0)).label("∇²E = με ∂²E/∂t²", loc="right")
elm.Block().at((1, -2)).label("free space: J = 0\nv = 1/√(με)", loc="bottom")
elm.Block().at((7, -2)).label("∇²H = με ∂²H/∂t²", loc="right")
```
