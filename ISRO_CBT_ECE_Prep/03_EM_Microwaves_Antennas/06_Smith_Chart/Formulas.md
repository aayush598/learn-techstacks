# Smith Chart - Formulas

## Normalization
```
z = Z/Z0
y = Y*Z0 = Y0/Y = 1/z  (inverse)
Also: y = 1/z rotates 180 deg on chart
```

## Reflection Coefficient
```
Gamma = (z-1)/(z+1) = (ZL-Z0)/(ZL+Z0)
|Gamma|, angle(Gamma) read polar
```

## VSWR from Chart
```
VSWR = (1+|Gamma|)/(1-|Gamma|)
Read from constant |Gamma| circle crossing real axis (max R value)
```

## Motion / Rotation
```
Input impedance at distance d from load:
  z_in = z_load rotated clockwise by angle:
    theta = 2 beta d = 4 pi d/lambda (electrical length)
Full circle: lambda/2 (180 electrical deg = 2*pi*... )
```
Important: A full revolution around the chart corresponds to a length of lambda/2.

## Quarter-Wave Transformer
```
At lambda/4 (180 deg), impedance inverts:
  Z_in = Z0^2 / Z_L
  For matching: Z_line = sqrt(Z_L * Z_source)
```

## Admittance Conversion
```
y = 1/z -> diametrically opposite point (180 deg / lambda/4)
```

## Match Condition
```
z = 1 (center), Gamma = 0, VSWR = 1
z = 1 +/- jX = reactance-only circle (for stub)
```

## Distance to stub
```
Find point on constant |Gamma| circle (from load) whose 
  real part (before stub) = 1 (unity conductance)
Rotate to locate stub position d
Stub length: rotate from open/short to cancel +jX reactance
```

## Quick Reference
| Operation | Chart Motion |
|-----------|--------------|
| z -> y | 180 deg (lambda/4) |
| toward load/generator | rotate |
| full rotation | lambda/2 |
| match | center z=1 |
| inductive | upper half |
| capacitive | lower half |
