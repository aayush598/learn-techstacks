# Commutation - Formulas

## 1. Natural Commutation Formulas

### Current Zero-Crossing
```
i(t) = Im × sin(ωt + φ)

Current zero at: ωt = nπ - φ (for n = 1, 2, 3...)
```

### Turn-Off Time
```
tq = time from current zero to when SCR can block forward voltage
tq = trr + tgr   [reverse recovery + gate recovery]

Typical: tq = 50-200 μs for standard SCRs
```

### Commutation Angle (for controlled rectifiers)
```
μ = angle during which current transfers from one SCR to another
μ = cos⁻¹(cos α - (2ωLs × Io)/Vm)

Where:
α = firing angle
Ls = source inductance
Io = load current
Vm = peak supply voltage
```

## 2. Class A (Load Commutation) Formulas

### Series RLC Circuit
```
i(t) = (V/R) × e^(-αt) × sin(ωd × t)

Where:
α = R/(2L) = damping factor
ωd = √(ω₀² - α²) = damped frequency
ω₀ = 1/√(LC) = resonant frequency
```

### Commutation Condition
```
ζ = R/(2√(L/C)) < 1   [underdamped]

For commutation: current must cross zero
This requires: ωd > 0 → ω₀ > α → L > R²C/4
```

### Commutation Time
```
tc = π/ωd = π/√(1/(LC) - (R/(2L))²)   [half resonant period]
```

### Resonant Frequency
```
fres = 1/(2π√(LC))   [Hz]
ωres = 1/√(LC)       [rad/s]
```

## 3. Class B (Resonant Pulse Commutation) Formulas

### Tank Circuit
```
fres = 1/(2π√(LC))
ωres = 1/√(LC)
```

### Resonant Current
```
ires(t) = (Vc₀/√(L/C)) × sin(ωres × t)

Peak resonant current: Ires(peak) = Vc₀ × √(C/L)
```

### Commutation Condition
```
Ires(peak) > IL (load current)
Vc₀/√(L/C) > IL
Vc₀ > IL × √(L/C)
```

### Commutation Time
```
tc = π/(2fres) = π√(LC)/2   [quarter resonant period]

Or: tc = 1/(2fres) = π√(LC)   [half period]
```

### Component Sizing
```
C ≥ IL × tc / Vc₀   [minimum capacitance]
L = 1/(4π²fres² × C)   [inductance]
```

## 4. Class C (Complementary Commutation) Formulas

### Capacitor Voltage
```
Vc(final) = Vin   [steady state]

During commutation:
Vc(t) = Vin × (1 - e^(-t/(RC)))   [charging]
```

### Commutation Time
```
tc = RC × ln(Vin/(Vin - Vth))   [approximately]

For Vth << Vin:
tc ≈ RC × ln(1) ≈ 0 (instantaneous)
Practical: tc = few microseconds
```

## 5. Class D (Auxiliary Voltage Commutation) Formulas

### Capacitor Sizing
```
C ≥ IL × tc / Vc₀   [must supply load current during tc]

Vc₀ = Vin (charged to supply voltage)
```

### Reverse Voltage Duration
```
trev = C × Vc₀ / IL   [time capacitor maintains reverse voltage]

trev must be > tq (SCR turn-off time)
```

### Resistor for Charging
```
Rcharge = Vin / Icharge
Pcharge = Vin² / Rcharge   [charging power loss]
```

## 6. Class E (Auxiliary Current Commutation) Formulas

### Auxiliary Current
```
IA > IL (load current to divert)

When IA > IL:
Imain = IL - IA = 0 (if IA = IL)
```

### Commutation Time
```
tc = Ldiv × IL / Vdiv   [time to divert current]

Where:
Ldiv = inductance in diversion path
Vdiv = voltage driving diversion
```

## 7. Class F (GTO Commutation) Formulas

### Gate Turn-Off Requirements
```
IG(off) = IA / βoff   [negative gate current]
βoff = 3-5 (typical)

Power required:
PG = VG(off) × IG(off)   [instantaneous]
PG(avg) = PG × tOFF × fsw
```

### Turn-Off Time Components
```
tq = ts + tf + ttail

ts: stored time (1-2 μs) - charge extraction
tf: fall time (0.5-2 μs) - current decay
ttail: tail time (5-20 μs) - stored charge recombination
```

### Minimum Commutation Interval
```
Tmin = tq + margin (typically 20-30%)
fmax = 1/Tmin
```

## 8. Snubber Circuit Design Formulas

### RC Snubber (dv/dt Protection)
```
Cs ≥ Vpeak / (dv/dt)max   [capacitor]
Rs = √(Ls/Cs)   [for critical damping]
Rs ≥ Vpeak / (di/dt)max   [for current limiting]

Power loss:
Ps = 0.5 × Cs × Vpeak² × fsw
```

### RCD Snubber
```
Cs: dv/dt limiting capacitor
Rs: discharge resistor
D: fast recovery diode

Cs = Vpeak / (dv/dt)max
Rs = Vpeak² / (2 × Ps)   [for desired power dissipation]
```

### Turn-On Snubber (Series Inductor)
```
Ls = Vpeak / (di/dt)max

Ls limits di/dt during turn-on
Typical: Ls = 10-100 μH
```

## 9. Commutation Failure Conditions

### When Commutation Fails
```
1. tc < tq   [commutation time too short]
2. Vc < Vth   [capacitor voltage insufficient]
3. IL > Ires(peak)   [load current too high]
4. R too high   [capacitor cannot charge/discharge fast enough]
```

### Commutation Margin
```
Safety margin: tc = tq × (1.2 to 1.5)

Margin angle: γ = ω × tc × (1.2 to 1.5)
```

## 10. Useful Constants and Relationships

### SCR Parameters
```
VRRM: repetitive peak reverse voltage (600-4000V)
ITSM: surge current (100-5000A)
tq: turn-off time (50-200 μs)
IL: latching current (10-100 mA)
IH: holding current (5-50 mA)
```

### Component Derating
```
Vcap: 2× Vin minimum
Inductor: 1.5× IL peak minimum
Resistor: 2× Pcalc minimum
```

### Frequency Limits
```
Class A: limited by load resonance (kHz range)
Class B: limited by LC tank (10-100 kHz)
Class C: limited by capacitor discharge (1-10 kHz)
Class D: limited by capacitor charging (1-5 kHz)
Class E: limited by diversion time (1-10 kHz)
Class F: limited by GTO characteristics (1-5 kHz)
```
