# Circuit Diagrams

## 1. Gradient of Potential to Electric Field

A scalar potential is differentiated to obtain a vector field. The negative gradient is the electric field, so the arrow direction represents the field direction while the magnitude represents the maximum rate of increase of potential.

```circuit
elm.SourceI().right().at((-5, 0)).label("V(x,y,z)", loc="left")
elm.Arrow().at((-2, 0)).to((0, 0)).label("gradient", loc="top")
elm.Block().at((0, -1)).label("∇V\nvector")
elm.Arrow().at((3, 0)).to((5, 0)).label("E = -∇V", loc="top")
elm.Block().at((5, -1)).label("electric field\nV/m")
```

## 2. Divergence as Source or Sink

A positive divergence represents net outward flux and a source; a negative value represents a sink. The radial arrows are the field-flow picture, while the block states the differential Gauss-law relation.

```circuit
elm.Dot().at((0, 0)).label("source or sink", loc="top")
elm.Arrow().at((0, 0)).to((3, 0)).label("D flux out", loc="top")
elm.Arrow().at((0, 0)).to((0, 3)).label("D flux", loc="right")
elm.Arrow().at((0, 0)).to((-3, 0)).label("D flux", loc="top")
elm.Arrow().at((0, 0)).to((0, -3)).label("D flux", loc="right")
elm.Block().at((4, 0)).label("∇·D = ρv\npositive: source\nnegative: sink")
```

## 3. Curl and Circulation

Curl measures the local rotation of a vector field. A closed circulation around a path is equivalent, through Stokes' theorem, to the surface integral of the curl.

```circuit
elm.SourceI().right().at((-5, 0)).label("vector field A", loc="left")
elm.Arrow().at((-2, 0)).to((0, 0)).label("apply ∇×", loc="top")
elm.Block().at((0, -1)).label("∇×A\nvector")
elm.Arrow().at((3, 0)).to((5, 0)).label("rotation", loc="top")
elm.Block().at((5, -1)).label("circulation\n∮ A·dl")
elm.Arrow().at((7, 1)).to((7, -1)).label("closed path C", loc="right")
```

## 4. Coordinate-System Mapping

The same point or field can be expressed in Cartesian, cylindrical, or spherical coordinates. The changing local basis in cylindrical and spherical coordinates is the reason their differential operators contain scale factors.

```circuit
elm.Block().at((-4, 0)).label("Cartesian\n(x,y,z)\nâx, ây, âz")
elm.Block().at((0, 2)).label("Cylindrical\n(ρ,φ,z)\nâρ, âφ, âz")
elm.Block().at((0, -2)).label("Spherical\n(r,θ,φ)\nâr, âθ, âφ")
elm.Arrow().at((-2, 0)).to((-1, 2)).label("transform", loc="top")
elm.Arrow().at((-2, 0)).to((-1, -2)).label("transform", loc="bottom")
elm.Arrow().at((1, 2)).to((3, 2)).label("dl and ∇", loc="top")
elm.Arrow().at((1, -2)).to((3, -2)).label("dV and ∇", loc="bottom")
```

## 5. Stokes and Gauss Integral Equivalences

Stokes' theorem converts a line integral around a loop to a surface integral of a curl. Gauss' divergence theorem converts flux through a closed surface to a volume integral of divergence.

```circuit
elm.Block().at((-4, 1)).label("∮C A·dl\nline integral")
elm.Arrow().at((-1, 1)).to((1, 1)).label("Stokes", loc="top")
elm.Block().at((2, 1)).label("∬S (∇×A)·dS\nsurface integral")
elm.Block().at((-4, -1)).label("∮S A·dS\nclosed flux")
elm.Arrow().at((-1, -1)).to((1, -1)).label("Gauss", loc="bottom")
elm.Block().at((2, -1)).label("∭V (∇·A)dV\nvolume integral")
elm.Block().at((6, 0)).label("integral Maxwell laws\n↔ differential form", loc="right")
```
