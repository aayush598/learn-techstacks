# EM/Microwaves/Antennas - Memory Tricks

## Intrinsic Impedance
- **Free space = 377 ohms** - "**3, 7, 7**" (remember the double 7)
- eta = sqrt(mu/epsilon) in any medium

## Transmission Line Formulas
- **Z0 = sqrt(L/C)** - "**Square root of L over C**"
- **VSWR = (1+|Gamma|)/(1-|Gamma|)** - "**One plus over one minus**"
- For matched: VSWR = 1, for open/short: VSWR = infinity

## Waveguide
- **TE10 cutoff: fc = c/(2a)** - "**Speed of light over twice the width**"
- **vp > c, vg < c** - "**Phase Pranks (is fast), Group Grazes (is slow)**"
- **vp * vg = c^2** - "**Product always c squared**"

## S-Parameters Memory
- **S11 = reflection** (input side, "1-1" = same port interaction)
- **S21 = transmission** (from port 1 to 2, "1-2")
- **Reciprocal: S12 = S21** - "**Symmetry of good components**"
- **Lossless: sum of column powers = 1** - "**Everything in, nothing lost**"

## Antenna Formulas
- **Half-wave dipole = 73 ohms** - "**Radius roughly 73 nm in the UV**"
- **Quarter-wave monopole = 36.5 ohms** - "**Half of 73**"

## Microwave Devices
- **Gunn = Negative Resistance** (transferred electron effect)
- **IMPATT = Impact Ionization Avalanch** (Transit Time)
- **TWT = Traveling Wave Tube** (broadband)
- **HEMT = High Electron Mobility** (low noise)

## Friis Equation Memory
- **Pr = Pt*Gt*Gr*(lambda/4piR)^2**
- "**Power received = Power sent * Gt * Gr * (lambda over 4 pi R) squared**"
- The (lambda/4piR) term is the "space loss"

## Material Properties
- **Free space: eta = 377 ohms, c = 3e8 m/s**
- **Copper: sigma = 5.8e7 S/m** (good conductor)
- **Silicon: epsilon_r = 11.7** (semiconductor)
