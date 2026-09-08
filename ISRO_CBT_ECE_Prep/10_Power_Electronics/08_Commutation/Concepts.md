# Commutation - Concepts

## 1. What is Commutation?

### Definition
- Process of turning off a conducting thyristor/SCR
- Current must be reduced below holding current (IH)
- In AC circuits: natural zero-crossing
- In DC circuits: external circuit required

### Importance
- Enables controlled turn-off of SCRs
- Determines maximum switching frequency
- Affects circuit complexity and cost
- Critical for inverter and chopper operation

## 2. Natural Commutation (Line Commutation)

### Principle
- Current naturally falls to zero at AC line zero-crossing
- SCR turns off when current < IH
- No external circuit needed
- Simplest and most reliable

### Applications
- AC voltage controllers (light dimmers)
- Phase-controlled rectifiers
- AC regulators
- Simple, low-frequency applications

### Limitations
- Only works with AC supply
- Limited to line frequency (50/60 Hz)
- Cannot be used in DC circuits

## 3. Forced Commutation Classes

### Class A (Self-Commutation)
- Load commutation
- Series RLC circuit with underdamped response
- Current oscillates to zero naturally
- Used in resonant converters

### Class B (Resonant Pulse Commutation)
- LC tank circuit across SCR
- Resonant current pulse opposes load current
- Net current through SCR goes to zero
- Used in high-frequency inverters

### Class C (Complementary Commutation)
- Two SCRs share same load
- Turning on one SCR commutates the other
- Current transfers from one SCR to another
- Used in some inverter topologies

### Class D (Auxiliary Voltage Commutation)
- Auxiliary SCR and charged capacitor
- Capacitor voltage applied across main SCR (reverse bias)
- Forces current to zero
- Used in high-power applications

### Class E (Auxiliary Current Commutation)
- Auxiliary SCR diverts current from main SCR
- Current transfers to auxiliary path
- Main SCR turns off naturally
- Used in some chopper circuits

### Class F (External Pulse Commutation)
- External pulse circuit generates turn-off pulse
- Applied directly to SCR gate
- Limited to SCRs with gate turn-off capability (GTO)
- Simplest for GTOs

## 4. Load Commutation (Class A)

### Principle
- Load provides natural current zero-crossing
- Series RLC with damping ratio ζ < 1
- Current oscillates and goes to zero
- SCR turns off at current zero

### Conditions for Load Commutation
```
1. Load must be underdamped RLC
2. Resonant frequency must be appropriate
3. Current must fall below IH before next cycle
4. ζ = R/(2√(L/C)) < 1
```

### Applications
- Resonant converters
- High-frequency inverters
- Induction heating
- Some motor drives

## 5. Resonant Pulse Commutation (Class B)

### Principle
- LC tank connected across SCR
- When SCR turns on, LC resonates
- Current through SCR = load current - resonant current
- When resonant current > load current, SCR current = 0
- SCR turns off

### Commutation Time
```
tc = 1/(2fres) = π√(LC)   [half resonant period]

Where:
fres = 1/(2π√(LC))
```

### Condition for Successful Commutation
```
IL(max) < Ires(peak) = Vc/√(L/C)

Where:
Vc = initial capacitor voltage
L, C = tank circuit values
IL = load current to be commutated
```

### Design Formula
```
C ≥ IL × tc / Vc   [minimum capacitance]
L = 1/(4π²fres² × C)   [inductance for desired fres]
```

## 6. Complementary Commutation (Class C)

### Principle
- Two SCRs (T1, T2) share load
- T1 ON: load current through T1
- Turn on T2: capacitor voltage reverse biases T1
- T1 turns off (current transfers to T2)
- Next cycle: T2 turns off when T1 fires

### Applications
- Parallel inverters
- McMurray-Bedford inverter
- Some cycloconverter circuits

## 7. Auxiliary Voltage Commutation (Class D)

### Principle
- Auxiliary SCR (TA) and capacitor (C)
- C charged to supply voltage
- Fire TA: C applies reverse voltage across main SCR (T)
- T turns off (forced commutation)
- C discharges through load

### Circuit Operation
1. T conducts, load current flows
2. C charged to Vin through R
3. Fire TA: C voltage (-Vin) applied across T
4. T turns off
5. C discharges through TA and load
6. When C fully discharged, TA turns off (current zero)

### Commutation Time
```
tc = R × C × ln(Vc/Vth)   [approximately]

Where:
Vc = capacitor voltage at commutation
Vth = SCR forward threshold voltage (≈1-2V)
```

## 8. Auxiliary Current Commutation (Class E)

### Principle
- Auxiliary SCR diverts load current from main SCR
- When TA fires, current path changes
- Main SCR current → zero
- Main SCR turns off
- Load current continues through TA and freewheeling diode

### Applications
- Some chopper circuits
- Current-source inverters

## 9. External Pulse Commutation (Class F)

### Principle
- For GTO thyristors only
- Large negative gate pulse applied
- Extracts stored charge from P2 base
- GTO turns off (controlled turn-off)

### Gate Requirements
```
IG(off) = IA / βoff   [negative gate current]
βoff = turn-off gain (typically 3-5)
```

### Applications
- GTO inverters
- Medium voltage drives
- HVDC converters (legacy)

## 10. Commutation Circuit Design Considerations

### Key Parameters
1. **Turn-off time (tq)**: Time for SCR to recover blocking capability
2. **Commutation margin**: Safety margin added to tq
3. **Capacitor voltage rating**: Must handle peak reverse voltage
4. **Inductor current rating**: Must handle peak resonant current
5. **Resistor power rating**: Must handle commutation losses

### Design Steps
```
1. Determine load current to be commutated
2. Select commutation method (Class A-F)
3. Calculate L, C values for desired commutation time
4. Select SCR ratings (VRRM, ITSM)
5. Calculate component power ratings
6. Add safety margins (20-30%)
```

### Snubber Circuit Design
```
Cs = Vpeak / (dv/dt)max   [snubber capacitor]
Rs = Vpeak / (di/dt)max   [snubber resistor]
Psnubber = 0.5 × Cs × Vpeak² × fsw   [snubber loss]
```

## 11. ISRO-Specific Focus

- Commutation reliability for satellite power converters
- Radiation effects on SCR commutation characteristics
- Redundancy in commutation circuits
- Efficiency considerations for space applications
- EMI generated during commutation
- Thermal management of commutation components
