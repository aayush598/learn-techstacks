# PMMC Instruments - Concepts

## 1. PMMC (Permanent Magnet Moving Coil)
Also called D'Arsonval movement.
Most fundamental analog measuring instrument for DC measurements.

## 2. Construction
- **Permanent Magnet:** Provides strong, uniform radial magnetic field (Alnico or rare-earth)
- **Moving Coil:** Rectangular coil wound on soft iron former, free to rotate in air gap
- **Iron Core:** Soft iron cylinder inside coil → makes field radial and uniform
- **Control Springs:** Phosphor-bronze spiral springs (top and bottom) → provide restoring torque AND current path
- **Pointer:** Attached to coil, moves over calibrated scale
- **Damping:** Eddy current damping via aluminum former (or coil itself)

## 3. Three Torques

### 3.1 Deflecting Torque (T_d)
Caused by interaction of coil current with magnetic field.
```
T_d = BINA cos(θ)
For radial field: T_d = BINA (constant over scale)
where B = flux density, I = current, N = turns, A = area
```

### 3.2 Controlling (Restoring) Torque (T_c)
Provided by springs. Opposes deflection.
```
T_c = kθ
where k = spring constant, θ = deflection angle
```

### 3.3 Damping Torque (T_m)
Opposes motion, prevents oscillations.
PMMC uses **eddy current damping**: movement of aluminum former in magnetic field induces eddy currents → damping force.
Only applicable because field is confined to air gap (no damping outside).

## 4. Steady-State Deflection
At equilibrium: T_d = T_c
```
BINA = kθ
θ = BINA/k
θ ∝ I (linear scale for DC current measurement)
```

## 5. Why Radial Field?
With radial field, B is constant regardless of coil position.
This ensures T_d ∝ I → Linear scale.

## 6. Eddy Current Damping
- Aluminum former moves in permanent magnet field
- Induced eddy currents create opposing magnetic field
- Provides smooth, effective damping
- PMMC is the ONLY instrument using eddy current damping exclusively

## 7. PMMC Limitations
- Works only for DC (for AC, average torque = 0)
- Can measure AC with rectifier (moving iron for direct AC)
- Sensitive to external magnetic fields
- Temperature affects spring constant and magnetic field

## 8. Error Sources
- Spring fatigue (k changes with temperature)
- Magnet aging (B decreases over time)
- Temperature: both B and k change
  Net effect: errors partially cancel (both decrease with ↑T)
- Friction (minimal due to jewel bearings)
- Parallax error (pointer reading)
- Stray magnetic fields

## 9. Multi-Range Extension

### 9.1 Ammeter (Shunt)
Low resistance (shunt) in parallel with PMMC movement.
```
R_sh = R_m × I_m / (I - I_m)
where R_m = meter resistance, I_m = full-scale current, I = desired range
```
Universal shunt (Ayrton shunt) for multi-range ammeters.

### 9.2 Voltmeter (Multiplier)
High resistance (multiplier) in series with PMMC movement.
```
R_s = V/I_m - R_m = R_m(V/V_m - 1)
where V = desired range, V_m = meter full-scale voltage
```

## 10. Ayrton (Universal) Shunt
Single resistor network for multiple current ranges.
Advantage: shunt is always connected → no open-circuit risk during range switching.

## 11. PMMC vs Moving Iron
| Feature | PMMC | Moving Iron |
|---------|------|-------------|
| Field | Permanent magnet | Electromagnet |
| Scale | Linear | Non-linear (squared) |
| Damping | Eddy current | Air friction |
| Power consumption | Low | High |
| Accuracy | High (0.5-2%) | Low (2-5%) |
| AC/DC | DC only | Both |

## 12. Sensitivity of PMMC
```
Sensitivity = 1/I_fs = θ_max / (BINA × unit)
For voltmeter: S = R_v / V_range (Ω/V)
Higher sensitivity → lower loading
```

## 13..ISRO Focus Areas
- Torque equation: θ = BINA/k
- Shunt resistance: R_sh = R_m × I_m/(I-I_m)
- Multiplier: R_s = R_m(V/V_m - 1)
- Why PMMC gives linear scale (radial field)
- Eddy current damping mechanism
