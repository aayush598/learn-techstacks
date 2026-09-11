# Antenna Fundamentals - Concepts

## Role of Antenna
- Transducer between guided wave (line/waveguide) and free-space EM wave
- Radiates/receives power, matches to free-space impedance

## Basic Parameters
- **Directivity (D)**: ratio of max radiation intensity to average (isotropic)
- **Gain (G)**: directivity x efficiency
- **Efficiency**: eta = G/D (radiated power/input power)
- **Effective aperture (Ae)**: Ae = lambda^2 G / (4 pi)
- **Radiation resistance**: resistance representing radiated power

## Directivity/Gain
```
D = 4pi * U_max / P_rad   (U = radiation intensity W/steradian)
G = 4pi * U_max / P_in = eta * D
For isotropic: D = G = 1 (0 dBi)
```

## Effective Aperture & Friis
```
Ae = lambda^2 G/(4pi)
Friis: Pr = Pt Gt Gr (lambda/(4pi R))^2
  (power received in LOS, free space)
```

## Radiation Pattern
- Field pattern vs angle
- Main lobe (direction of max)
- Side lobes, back lobe
- HPBW (Half-Power Beam Width): 3-dB beamwidth
- FNBW (First Null Beamwidth)

## Directivity from Beamwidth (approx)
```
D ~ 4pi / (Theta_HPBW * Phi_HPBW)   (approx, radians)
For pencil beam
```

## Polarization
- Matches E-field orientation (linear/circular/elliptical)
- Max reception when polarizations match
- Mismatch gives polarization loss

## Antenna as Circuit
```
Input impedance ZA = RA + jXA
  RA = Rr (radiation) + Rloss
Match to feed line for max power
Impedance bandwidth: VSWR < 2 (say)
```

## Reciprocity
- Antenna parameters same for transmit and receive
- Pattern, gain identical both modes

## Bandwidth
- Frequency range where parameters stay within limits
- VSWR bandwidth, impedance bandwidth, gain bandwidth

## Radiation Mechanism
- Accelerating charge radiates
- Time-varying current distribution on structure
- Standing waves / traveling waves

---

## ISRO Key Points
- Gain = D * efficiency
- Ae = lambda^2 G/(4pi)
- Friis: Pr = Pt Gt Gr (lam/4piR)^2
- Directivity: 4pi U_max/P_rad
- HPBW vs directivity
- Reciprocity (same for Tx/Rx)
