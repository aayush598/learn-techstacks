# Electromagnetics, Microwaves & Antennas - Complete Formula Sheet

## Vector Analysis
```
Gradient: grad(f) = df/dx * ax + df/dy * ay + df/dz * az
Divergence: div(A) = dAx/dx + dAy/dy + dAz/dz
Curl: curl(A) = |ax    ay    az  |
                |d/dx  d/dy  d/dz|
                |Ax    Ay    Az  |
Stokes theorem: closed(A.dl) = open(curl(A).dA)
Gauss divergence: closed(A.dA) = triple(div(A).dV)
```

## Maxwell's Equations
```
div(D) = rho_v
div(B) = 0
curl(E) = -dB/dt
curl(H) = J + dD/dt
```

## Plane Waves
```
Intrinsic impedance: eta = sqrt(mu/epsilon)
Free space: eta_0 = 377 ohms
Phase velocity: vp = 1/sqrt(mu*epsilon)
Wavelength: lambda = vp/f
Poynting vector: P = E x H (W/m^2)
Skin depth: delta = sqrt(2/(w*mu*sigma))
Brewster angle: theta_B = arctan(sqrt(e2/e1))
```

## Transmission Lines
```
Z0 = sqrt(L/C) [lossless]
Gamma = (ZL-Z0)/(ZL+Z0)
VSWR = (1+|Gamma|)/(1-|Gamma|)
Zin = Z0*(ZL+jZ0*tan(bl))/(Z0+jZL*tan(bl))
Quarter-wave: Zin = Z0^2/ZL
Half-wave: Zin = ZL
```

## Smith Chart
```
Center: matched point (Gamma = 0)
Right edge: open circuit (Gamma = 1)
Left edge: short circuit (Gamma = -1)
SWR circle: constant |Gamma| circle
Move toward generator: clockwise
Move toward load: counterclockwise
```

## Waveguides (Rectangular)
```
TE10 cutoff: fc = c/(2a)
Phase velocity: vp = f/sqrt(f^2-fc^2) = c/sqrt(1-(fc/f)^2)
Group velocity: vg = c*sqrt(1-(fc/f)^2)
vp * vg = c^2
Guide wavelength: lambda_g = lambda/sqrt(1-(fc/f)^2)
Dominant mode: TE10 (lowest cutoff)
```

## S-Parameters
```
b = S*a
S11: input reflection, S21: forward transmission
Reciprocal: S12 = S21
Lossless: S^H*S = I
3-port: cannot be reciprocal + lossless + matched
```

## Antennas
```
Directivity: D = 4*pi*Umax/Prad
Gain: G = eta*D
EIRP = Pt*Gt
Friis: Pr = Pt*Gt*Gr*(lambda/(4*pi*R))^2
Ae = lambda^2*G/(4*pi)
Half-wave dipole: Rr = 73 ohms
Quarter-wave monopole: Rr = 36.5 ohms
HPBW = 0.886*lambda/L (uniform linear array)
```

## Radar
```
Rmax = (Pt*Gt*Gr*lambda^2*sigma/((4*pi)^3*Smin))^(1/4)
Doppler shift: fd = 2*vr/lambda = 2*vr*f/c
Minimum detectable signal: Smin = kT0*B*F*SNR_min
```

## Microwave Devices
```
Gunn: f = 1/(2*pi*tau_d) (transit time frequency)
IMPATT: high power, high noise
TWT: broadband, medium power
Klystron: narrowband, high power
HEMT: low noise amplifier
```
