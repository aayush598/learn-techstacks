# Antenna Fundamentals - Formulas

## Directivity
```
D = Umax / Uavg = 4*pi*Umax / Prad

U = radiation intensity (W/sr)
Prad = total radiated power (W)
```

## Gain
```
G = eta_ant * D

eta_ant = radiation efficiency = Prad/Pinput
G accounts for ohmic losses, D does not
```

## Effective Aperture
```
Ae = (lambda^2 * G) / (4*pi)

For aperture antenna: Ae = eta_a * A_physical
eta_a = aperture efficiency (typically 0.5-0.7)
```

## Friis Transmission Equation
```
Pr/Pt = Gt * Gr * (lambda / (4*pi*R))^2

Pr = received power
Pt = transmitted power
Gt = transmit antenna gain
Gr = receive antenna gain
R = distance between antennas
```

## EIRP (Effective Isotropic Radiated Power)
```
EIRP = Pt * Gt (in dB: EIRP_dB = Pt_dB + Gt_dB)
Equivalent power radiated by isotropic antenna for same field strength
```

## Radiation Resistance
```
For short dipole (l << lambda):
  Rr = 80*pi^2*(l/lambda)^2 = 20*(pi*l/lambda)^2

For half-wave dipole:
  Rr = 73 ohms

For monopole (quarter-wave over ground plane):
  Rr = 36.5 ohms (half of half-wave dipole)
```

## Beamwidth
```
HPBW = angle between half-power (-3dB) points
First null beamwidth (FNBW) = angle between first nulls

For uniform linear array of N elements:
  HPBW approximately 0.886*lambda/(N*d) (in radians)
```

## Antenna Noise Temperature
```
Ta = (Prad)/(kB) where k = Boltzmann constant = 1.38e-23 J/K
G/T ratio: figure of merit for receiving system
```

## Quick Reference
| Parameter | Formula | Unit |
|-----------|---------|------|
| Directivity | D = 4pi*Umax/Prad | dimensionless (dBi) |
| Gain | G = eta*D | dimensionless (dBi) |
| EIRP | Pt*Gt | Watts (dBW) |
| Friis | Pr = Pt*Gt*Gr*(lambda/4piR)^2 | Watts |
| Rr (half-wave) | 73 ohms | ohms |
| HPBW | 0.886*lambda/L | radians |
