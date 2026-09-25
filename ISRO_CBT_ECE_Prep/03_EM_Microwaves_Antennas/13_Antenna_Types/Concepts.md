# Antenna Types - Concepts

## Wire Antennas

### Dipole
- Half-wave dipole: 2 lambda/4 arms
  - Length ~ lambda/2, Rr ~ 73 ohms, D ~ 1.64 (2.15 dBi)
- Full-wave: higher gain but impedance trickier
- Short dipole: low Rr, low efficiency unless matched

### Monopole (quarter-wave)
- lambda/4 over ground plane
- Rr ~ 36.5 ohms, D ~ 1.64 (2.15 dBi)
- Same ideal directivity as a half-wave dipole, but half the physical length above ground (image theory)

### Loop Antenna
- Small loop: electrically small, low Rr, used for receiving/direction finding
- Large loop (full-wave): higher gain
- Ferrite loop for AM radios

### Folded Dipole
- Two conductors joined at ends (folded)
- Impedance ~ 4x simple dipole (~300 ohms)
- Wider bandwidth

## Aperture Antennas

### Parabolic Dish
- High gain, beam from reflector
- Gain: G = eta (pi D/lambda)^2 (D = diameter)
- Feed at focus (horn). Uses: satellite, radar
- Beamwidth: theta ~ 70 lambda/D (degrees)

### Horn Antenna
- Flared waveguide aperture
- Medium gain, good for feeds, measurement (gain standard)
- E-plane / H-plane horns

## Array Antennas
- Multiple elements, phase-controlled beam
- **Phased array**: steer beam electronically (phase shifters)
- Array factor shapes pattern; elements shape element pattern
- Beam direction: theta (from array factor)
- Directivity: D ~ N (N elements) max (in ideal)

## Patch/Microstrip
- Low profile, flat, printed circuit antenna
- Low gain, narrow bandwidth, cheap
- Used in mobile, arrays, GPS

## Helical Antenna
- Helix radiates circular polarization
- Axial mode: endfire gain
- Used for satellite comm

## Yagi-Uda
- Driven element + director + reflector
- High gain (relative to dipole), narrow band, unidirectional
- Used for TV reception, amateur radio

## VHF/UHF others
- Log-periodic: broadband, frequency independent
- Discone: wideband
- Biconical, biconical dipole: broadband

## Comparison
| Type | Gain | BW | Use |
|------|------|----|-----|
| Dipole | 2.15 dBi | narrow-med | general |
| Dipole(1) | - | - | - |
| Monopole | ~5 dBi | med | mobile |
| Patch | 5-8 dBi | narrow | arrays |
| Horn | 10-25 dBi | wide | feeds |
| Dish | 30-60 dBi | narrow | satellite/radar |
| Yagi | 6-15 dBi | narrow | TV |
| Helical | 10 dBi | circ-pol | satellite |

---

## ISRO Key Points
- Half-wave dipole: 73 ohm, 2.15 dBi
- Monopole: 36.5 ohm, ideal directivity 1.64 (2.15 dBi)
- Parabolic: G = eta(piD/lambda)^2
- Folded dipole: 300 ohm, 4x
- Patch: low profile, narrowband
- Phased array: electronic steering
