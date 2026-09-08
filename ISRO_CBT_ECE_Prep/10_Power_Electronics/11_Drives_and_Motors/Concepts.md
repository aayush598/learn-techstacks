# Drives and Motors - Concepts

## 1. DC Motor Speed Control

### DC Motor Basics
- Speed equation: n = (Va - IaRa)/(kΦ)
- Speed proportional to applied voltage (Va)
- Speed inversely proportional to field flux (Φ)
- Torque: T = kΦIa

### Speed Control Methods
1. **Armature voltage control**: Vary Va (constant Φ)
2. **Field flux control**: Vary Φ (constant Va)
3. **Armature resistance control**: Add series resistance (wasteful)
4. **Chopper control**: Vary average voltage via PWM

### Armature Voltage Control (Preferred)
- Most efficient method
- Constant torque operation below base speed
- Speed range: 1:10 typical
- Used in drives up to base speed

### Field Flux Control
- Constant power operation above base speed
- Speed increases as flux decreases
- Maximum speed limited by commutation and mechanical limits
- Used above base speed in field-weakening region

## 2. Chopper-Fed DC Motor Drives

### Basic Circuit
- Chopper (buck converter) feeds DC motor
- Motor back-EMF: E = kΦn
- Armature current: Ia = (Va - E)/Ra
- Speed control by varying duty cycle D

### Speed Equation
```
n = (D × Vin - IaRa)/(kΦ)

At no-load: Ia ≈ 0
n(no-load) ≈ D × Vin/(kΦ)
```

### Four-Quadrant Operation
- **Quadrant I**: Forward motoring (D > 0, Ia > 0)
- **Quadrant II**: Forward regeneration (D < 1, Ia < 0)
- **Quadrant III**: Reverse motoring (D < 0, Ia < 0)
- **Quadrant IV**: Reverse regeneration (D > 0, Ia > 0)

### Torque-Speed Characteristics
- Below base speed: constant torque (armature voltage control)
- Above base speed: constant power (field weakening)
- Base speed: speed at rated voltage and rated flux

### Regenerative Braking
- Motor acts as generator
- Energy returned to source
- Requires chopper in second quadrant (Type B)
- Limitation: source must accept regenerated energy

### Dynamic Braking
- Motor connected to braking resistor
- Energy dissipated as heat
- Simple but wasteful
- Used where regeneration not practical

## 3. Induction Motor V/f Control

### Induction Motor Basics
- Synchronous speed: ns = 120f/p
- Slip: s = (ns - n)/ns
- Torque: T ∝ V²/(f × (R2/s)² + (X2)²)

### V/f Control Principle
- Keep V/f ratio constant
- Maintains constant flux (Φ ∝ V/f)
- Constant torque below base speed
- Constant power above base speed (field weakening)

### Speed Control Methods
1. **V/f control**: Vary frequency and voltage proportionally
2. **Slip control**: Control slip frequency
3. **Vector control**: Independent control of flux and torque
4. **Direct torque control**: Direct control of torque and flux

### V/f Control Implementation
```
V = Vrated × (f/frated)   [for f < frated]
V = Vrated   [for f > frated, field weakening]

At low frequencies, voltage boost needed:
V = Vboost + Vrated × (f/frated)
```

### Torque-Speed Characteristics
- Maximum torque (breakdown torque) independent of frequency
- Starting torque ∝ V²/f² (at low frequency)
- Pull-out torque occurs at slip: sm = R2/X2

### Slip Calculations
```
s = (ns - n)/ns
ns = 120f/p (synchronous speed)
n = ns × (1-s) (rotor speed)

For 50 Hz, 4-pole motor:
ns = 1500 RPM
At s = 0.04: n = 1500 × 0.96 = 1440 RPM
```

## 4. Torque-Speed Characteristics

### DC Motor Characteristics
- **Shunt motor**: Nearly constant speed, moderate starting torque
- **Series motor**: High starting torque, speed varies widely
- **Compound motor**: Combination of shunt and series

### Induction Motor Characteristics
- **Low slip region**: Linear T-s curve
- **Breakdown torque**: Maximum torque point
- **Starting torque**: Torque at s = 1 (standstill)
- **Pull-up torque**: Minimum torque during acceleration

### Key Points
- Starting current: 5-7× rated current (direct-on-line)
- Starting torque: 1.5-2× rated torque (DOL)
- With V/f: starting current reduced, torque controlled
- Speed range: 10:1 typical with V/f, 100:1 with vector control

## 5. Inverter-Fed Motor Drives

### Voltage Source Inverter (VSI)
- DC bus with capacitor
- PWM output voltage
- Motor current determined by load
- Most common topology

### Current Source Inverter (CSI)
- DC bus with inductor
- Controlled output current
- Naturally commutated at load
- Used in high-power applications

### PWM Inverter for Motor Drive
- SPWM or SVM for voltage control
- V/f control for induction motors
- Vector control for high performance
- Speed range: 10:1 to 100:1

### Motor Insulation Stress
- dv/dt at motor terminals
- Voltage reflection on long cables
- Bearing currents
- Insulation stress increases with switching frequency

## 6. Torque Calculations

### DC Motor
```
T = k × Φ × Ia
T ∝ Ia (for constant flux)

Power: P = T × ω = E × Ia
ω = 2πn/60 (rad/s)
```

### Induction Motor
```
T = (3 × Vs² × R2/s) / (ωs × [(R1 + R2/s)² + (X1 + X2)²])

Simplified (near synchronous speed):
T ≈ (3 × Vs² × s) / (ωs × R2)

Maximum torque (breakdown):
Tmax = (3 × Vs²) / (2 × ωs × (R1 + √(R1² + (X1+X2)²)))
```

### Starting Torque
```
Tstart = (3 × Vs² × R2) / (ωs × [(R1 + R2)² + (X1 + X2)²])

Tstart/T rated ≈ 1.5-2 (for standard motors)
```

## 7. ISRO-Specific Focus

- DC motor drives for antenna positioning
- Induction motor drives for pump and fan applications
- V/f control for spacecraft mechanisms
- Efficiency requirements for power budget
- Radiation effects on motor insulation
- Redundancy in drive systems
