# LVDT - Concepts

## 1. LVDT Overview
Linear Variable Differential Transformer (LVDT) is an electromechanical transducer that converts linear displacement into an electrical signal.
Most widely used linear displacement transducer.

## 2. Construction

### 2.1 Primary Winding
- Single winding on central limb of bobbin
- Connected to AC excitation (typically 1-12V, 50-400 Hz)

### 2.2 Secondary Windings
- Two identical windings (S₁ and S₂) on either side of primary
- Connected in series-opposition (differential connection)

### 2.3 Core
- Movable soft iron/nickel-iron core
- Moves inside the bobbin with the displacement
- Provides low reluctance magnetic path

### 2.4 Bobbin
- Non-magnetic form that holds all windings
- Provides structural support

## 3. Working Principle

### 3.1 Mutual Inductance
- AC voltage applied to primary induces voltage in secondaries via mutual inductance
- Coupling depends on core position

### 3.2 Null Position
- Core at center → equal flux links both secondaries
- E₁ = E₂ → Output E_out = E₁ - E₂ = 0
- This is the zero displacement reference

### 3.3 Displacement from Null
- Move core toward S₁: E₁ > E₂ → E_out = E₁ - E₂ (in phase with primary)
- Move core toward S₂: E₂ > E₁ → E_out = E₂ - E₁ (180° out of phase)
- Phase reversal indicates direction of displacement

### 3.4 Differential Output
```
E_out = E₁ - E₂
At null: E_out = 0
Off-null: E_out ∝ displacement (for small displacements)
```

## 4. LVDT Characteristics

### 4.1 Sensitivity
```
Sensitivity = ΔE_out / Δx (mV/mm)
Typical: 40-100 mV/mm/V of excitation
Higher excitation → higher sensitivity
```

### 4.2 Linearity
- Excellent linearity over operating range (±0.25% FSD)
- Linear range typically ±2.5mm to ±250mm
- Beyond linear range, sensitivity drops

### 4.3 Resolution
- Theoretically infinite (analog output)
- Practically limited by signal conditioning electronics
- Typically better than 1 μm

### 4.4 Phase
- Output in phase with primary when core moves in one direction
- 180° out of phase when core moves in opposite direction
- Phase information determines direction

## 5. LVDT Signal Conditioning

### 5.1 Components
- AC excitation source
- Demodulator (phase-sensitive rectifier)
- Low-pass filter
- Amplifier

### 5.2 Demodulation
Converts AC output to DC proportional to displacement.
Phase-sensitive detection preserves direction information.

### 5.3 Output
- DC voltage: ±10V typical for full-scale displacement
- Current output: 4-20 mA for industrial applications

## 6. Advantages
- Infinite resolution (analog output)
- No electrical contact (no friction, long life)
- Robust construction
- High sensitivity
- Excellent linearity
- Rugged (can withstand vibration, shock)

## 7. Disadvantages
- Requires AC excitation
- Signal conditioning needed
- Limited dynamic response (core mass)
- Temperature sensitivity of windings
- Bulkier than some alternatives

## 8. Applications
- Precision dimensional measurement
- Hydraulic/pneumatic valve positioning
- Machine tool positioning
- Force/pressure measurement (with spring element)
- Material testing equipment
- Rocket/spacecraft component testing (ISRO relevant)

## 9. LVDT Parameters for ISRO
| Parameter | Typical Value |
|-----------|---------------|
| Sensitivity | 40-100 mV/mm/V |
| Linearity | ±0.25% FSD |
| Frequency range | DC to 500 Hz |
| Stroke length | ±0.5mm to ±750mm |
| Resolution | < 1 μm |
| Excitation | 1-12V AC, 50-400 Hz |

## 10. ISRO Focus Areas
- Sensitivity calculation (mV/mm)
- Null position concept
- Phase-sensitive demodulation for direction
- Linearity and resolution
- LVDT signal conditioning circuit
