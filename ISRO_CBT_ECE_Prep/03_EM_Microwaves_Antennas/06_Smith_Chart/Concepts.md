# Smith Chart - Concepts

## What it Is
- Graphical tool for transmission line / impedance matching calculations
- Plots normalized impedance/admittance on complex plane
- Polar: reflection coefficient Gamma (magnitude and angle)
- Developed by Phillip Smith (1939)

## Basics
```
Normalized impedance: z = Z/Z0
Normalized admittance: y = Y*Z0 = 1/z
Reflection coefficient: Gamma = (z-1)/(z+1)
The Smith chart maps z-plane (impedance) to unit circle in Gamma-plane
```

## Key Features
- Horizontal axis: real axis (R = 0 to infinity)
- Circles: constant resistance
- Arcs: constant reactance
- Circumference: |Gamma| = 1 (perfect reflection)
- Center: |Gamma| = 0 (matched, z=1)
- Top half: +jX (inductive)
- Bottom half: -jX (capacitive)

## Constant Value Curves
| Curve | Meaning |
|-------|---------|
| Constant R circle | moving along it: only reactance changes |
| Constant X arc | moving along it: only resistance changes |
| Constant |Gamma| circle | toward/away from load |
| Constant VSWR circle | same as |Gamma| circle |

## Motions on Chart
- Toward load: clockwise (counterclockwise rotation? - convention)
- Away from load / toward generator: one direction
- A full rotation = lambda/2 (half wavelength)
  Moving distance L (lambda) rotates angle 4*pi*L/lambda
- Quarter-wave (lambda/4) = 180 degree rotation (z -> 1/z)

## Reading Values
```
VSWR: read from |Gamma| circle intersection with real axis
Reflection: |Gamma| = (VSWR-1)/(VSWR+1)
z(d) from load: rotate clockwise by (2*beta*d)
Match: find z=1 point (center)
```

## Uses
1. Find input impedance from load at distance d
2. Determine VSWR
3. Design matching networks (single/double stub, quarter-wave)
4. Impedance & admittance conversion (rotate 180 = 1/z or read y)
5. Analyze transmission line transformations

## Admittance Point
- Impedance at a point -> admittance is diametrically opposite (180 deg, lambda/4)
- Same chart can be used as admittance chart (rotate reference)

---

## ISRO Key Points
- Smith chart = impedance + reflection coefficient combined
- Full rotation = lambda/2
- Quarter wave = 180 deg -> z becomes 1/z
- Match at center (z=1, Gamma=0)
- Top inductive, bottom capacitive
- VSWR from constant |Gamma| circle
