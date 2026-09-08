# DC Bridges - Concepts

## 1. Bridge Circuits Overview
Bridge circuits compare an unknown impedance with a known standard. At balance, the detector reads zero (null condition).

## 2. Wheatstone Bridge

### 2.1 Basic Configuration
Four arms: R₁, R₂, R₃ (known), R₄ (unknown).
Source V_s connected across one diagonal, galvanometer across the other.

### 2.2 Balance Condition
At balance: V_g = 0 → No current through galvanometer.
```
R₁/R₂ = R₃/R₄
or R₁ × R₄ = R₂ × R₃ (product of opposite arms equal)
```

### 2.3 Bridge Sensitivity
```
S_B = ΔI_g / (ΔR₄/R₄)
```
Sensitivity depends on:
- Battery voltage (higher → more sensitive)
- Galvanometer sensitivity
- Ratio R₁/R₂ (optimal when all arms ≈ equal)

### 2.4 Thévenin Equivalent at Detector
When bridge is near balance:
```
V_th = V_s × [R₄/(R₃+R₄) - R₂/(R₁+R₂)]
R_th = (R₁||R₂) + (R₃||R₄)
```
Current through detector: I_g = V_th / (R_th + R_g)

## 3. Kelvin Double Bridge

### 3.1 Purpose
Measures very low resistances (below 1Ω) accurately.
Eliminates effect of lead and contact resistances.

### 3.2 Configuration
Has additional ratio arms (p, q) and connects the potential terminals directly to the unknown resistance terminals.

### 3.3 Balance Condition
```
R_x = R_s × (P/Q) when p/q = P/Q
```
P, Q: main ratio arms; p, q: auxiliary ratio arms.

## 4. Schering Bridge (DC Application)

### 4.1 General Impedance Bridge
Used for measuring capacitance and dissipation factor.
At balance: Real and imaginary parts separately equal zero.

## 5. Maxwell Bridge

### 5.1 Configuration
Measures unknown inductance using a standard capacitor.
One arm has inductance Lₓ in series with Rₓ.
Opposite arm has capacitor C in parallel with R.

### 5.2 Balance Condition
```
Lₓ = R₂ × R₃ × C₄
Rₓ = R₂ × R₃ / R₄
```

## 6. General Bridge Balance Principle
For any AC bridge at balance:
```
Z₁ × Z₄ = Z₂ × Z₃ (product of opposite arm impedances)
Separate into real and imaginary parts.
```

## 7. Thévenin Equivalent at Detector
Any bridge circuit can be reduced to:
- Open-circuit voltage V_th
- Thévenin resistance R_th
- Connected to galvanometer R_g

Detector current: I_d = V_th / (R_th + R_g)

## 8. Comparison: DC vs AC Bridges
| Feature | DC Bridge | AC Bridge |
|---------|-----------|-----------|
| Source | Battery | Oscillator |
| Arms | Resistive | R, L, C, combinations |
| Balance | Real only | Real + Imaginary |
| Examples | Wheatstone, Kelvin | Maxwell, Wien, Schering |

## 9. Unbalance Analysis
Small change ΔR in one arm produces detector current approximately:
```
I_d ≈ V_s × ΔR / [4R × (R_th + R_g)]
```
This linear approximation works for small unbalance.

## 10. Bridge Sensitivity Optimization
Maximum sensitivity when:
- All four resistances are approximately equal
- Battery voltage is maximum (within power dissipation limits)
- Galvanometer resistance matches R_th

## 11. Kelvin Bridge Details
- Four-terminal resistance measurement
- Current terminals and potential terminals are separate
- Eliminates contact resistance from measurement
- Used for: shunt resistors, bus bars, low-value precision resistors

## 12. ISRO Focus Areas
- Wheatstone bridge balance equation
- Bridge sensitivity calculation
- Thévenin equivalent at detector
- Kelvin bridge for low resistance
- Loading effect on bridge sensitivity
