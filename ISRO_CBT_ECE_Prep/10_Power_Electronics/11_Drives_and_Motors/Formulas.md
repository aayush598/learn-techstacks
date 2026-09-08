# Drives and Motors - Formulas

## 1. DC Motor Formulas

### Speed Equation
```
n = (Va - IaRa)/(kΦ)

Where:
Va = armature voltage
Ia = armature current
Ra = armature resistance
k = machine constant
Φ = field flux
```

### Back-EMF
```
E = kΦn = Va - IaRa
E ∝ nΦ
```

### Torque
```
T = kΦIa   [electromagnetic torque]
T ∝ Ia (for constant flux)
```

### Power
```
Pmech = T × ω = E × Ia
ω = 2πn/60   [rad/s]

Pinput = Va × Ia
Ploss = Ia² × Ra
Pmech = Pinput - Ploss
```

### Efficiency
```
η = Pout/Pin = Pmech/(Va × Ia)
η = (E × Ia)/(Va × Ia) = E/Va
```

## 2. Chopper-Fed DC Motor Formulas

### Armature Voltage
```
Va = D × Vin   [buck chopper]
D = duty cycle
```

### Speed
```
n = (D × Vin - IaRa)/(kΦ)

At no-load (Ia ≈ 0):
n(no-load) = D × Vin/(kΦ)

At full-load:
n(full-load) = (D × Vin - Ia(rated) × Ra)/(kΦ)
```

### Torque
```
T = kΦIa = kΦ × (D × Vin - kΦn)/Ra
```

### Power
```
Pmech = T × ω = (D × Vin × Ia) - (Ia² × Ra)
Pchopper = D × Vin × Is   [source power]
Is = D × Ia (average source current)
```

### Efficiency of Drive
```
η = Pmech/Pchopper = (E × Ia)/(D × Vin × Ia)
η = E/(D × Vin) = (D × Vin - IaRa)/(D × Vin)
```

## 3. Four-Quadrant Operation Formulas

### Quadrant I (Forward Motoring)
```
Va > 0, Ia > 0
Va = D1 × Vin
n = (D1 × Vin - IaRa)/(kΦ) > 0
T = kΦIa > 0
```

### Quadrant II (Forward Regeneration)
```
Va > 0, Ia < 0
Va = D2 × Vin (boost action)
n > 0 (same direction)
T < 0 (braking)
Power flows from motor to source
```

### Quadrant III (Reverse Motoring)
```
Va < 0, Ia < 0
Va = -D3 × Vin
n < 0 (reverse direction)
T < 0 (driving in reverse)
```

### Quadrant IV (Reverse Regeneration)
```
Va < 0, Ia > 0
Va = -D4 × Vin
n < 0, T > 0
Braking in reverse direction
```

## 4. Induction Motor Formulas

### Synchronous Speed
```
ns = 120f/p   [RPM]

Where:
f = supply frequency (Hz)
p = number of poles
```

### Slip
```
s = (ns - n)/ns = (ns - n)/ns

n = ns(1-s)   [rotor speed]
```

### Torque Equation
```
T = (3Vs²R2/s) / (ωs[(R1 + R2/s)² + (X1+X2)²])

Where:
Vs = stator voltage per phase
R1, R2 = stator, rotor resistance per phase
X1, X2 = stator, rotor reactance per phase
ωs = 2πns/60 = synchronous angular velocity
```

### Starting Torque (at s = 1)
```
Tstart = (3Vs²R2) / (ωs[(R1+R2)² + (X1+X2)²])

Tstart/T rated ≈ 1.5-2 (standard motors)
```

### Maximum Torque (Breakdown)
```
Tmax = (3Vs²) / (2ωs(R1 + √(R1² + (X1+X2)²)))

At slip: sm = R2/√(R1² + (X1+X2)²)

Tmax/T rated ≈ 2-3 (typical)
```

### Power Relationships
```
Pgap = T × ωs   [air gap power]
Pmech = (1-s) × Pgap   [mechanical power]
Pcu2 = s × Pgap   [rotor copper loss]

Pinput ≈ Pmech/η
```

## 5. V/f Control Formulas

### Constant V/f Ratio
```
V/f = Vrated/frated = constant   [for f < frated]

V = Vrated × (f/frated)
```

### Speed with V/f
```
n = ns(1-s) = (120f/p)(1-s)

At constant V/f:
Tmax independent of frequency (approximately)
```

### Low Frequency Boost
```
V = Vboost + Vrated × (f/frated)   [for f < 10 Hz]

Vboost compensates for stator resistance drop
Typical: Vboost = 5-15% of Vrated
```

### Constant Power Region (f > frated)
```
V = Vrated   [voltage limited]
Tmax ∝ 1/f² (decreases)
Pmax = constant
```

### Torque-Speed with V/f
```
At frequency f:
ns = 120f/p
Tmax ≈ constant (for V/f control)
n_base = 120frated/p   [base speed]

Below n_base: constant torque
Above n_base: constant power (field weakening)
```

## 6. Slip Calculation Examples

### Standard Calculations
```
For 50 Hz, 4-pole motor:
ns = 120 × 50/4 = 1500 RPM

At s = 0.04 (4% slip):
n = 1500 × (1-0.04) = 1440 RPM

At s = 0.02 (2% slip, near synchronous):
n = 1500 × 0.98 = 1470 RPM
```

### Frequency Change Effect
```
At 25 Hz (half frequency):
ns = 120 × 25/4 = 750 RPM
n (s=0.04) = 750 × 0.96 = 720 RPM

Speed proportional to frequency
```

### Starting Current
```
Istart = Vs / √((R1+R2)² + (X1+X2)²)   [at s=1]

Istart/Irated ≈ 5-7 (direct-on-line)
With V/f: Istart reduced proportionally
```

## 7. Drive Efficiency Formulas

### Overall Drive Efficiency
```
ηdrive = ηchopper × ηmotor × ηcontroller

Typical:
ηchopper = 90-95%
ηmotor = 85-95% (depends on load)
ηcontroller = 95-98%
ηtotal = 75-90%
```

### Energy Saving with V/f
```
Fan/pump load: P ∝ n³
At 80% speed: P = 0.8³ = 0.512 (51% power)
Energy saving = 49% at 80% speed!

Compared to throttle control (dissipate excess energy)
```

### Regenerative Braking Energy
```
Ebrake = ∫ T × ω dt   [during braking]

If regenerated to source:
Energy recovery = ηregen × Ebrake
ηregen ≈ 80-90%
```

## 8. Motor Starting Methods

### Direct-On-Line (DOL)
```
Istart = 5-7 × Irated
Tstart = 1.5-2 × Trated
Simple but high inrush current
```

### Star-Delta Starting
```
Istar = Idelta/√3 = Istart(DOL)/3
Tstar = Tdelta/3 = Tstart(DOL)/3
Reduced voltage starting
```

### Autotransformer Starting
```
Istart = (tap%)² × Istart(DOL)
Tstart = (tap%)² × Tstart(DOL)
Tap typically 65%, 80%
```

### Soft Starter (Thyristor)
```
Vary firing angle α to control starting voltage
Vo = Vm/π × (1 + cos α)
Smooth acceleration
Current limiting possible
```

### V/f Starting (Inverter)
```
Gradually increase f from 0 to rated
V/f = constant
Controlled current and torque
Best starting method
```

## 9. Useful Relationships

### DC Motor Constants
```
kΦ = E/n = (Va - IaRa)/n
Torque constant: kT = kΦ = T/Ia
Speed constant: kn = 1/kT (in SI units)
```

### Induction Motor Relationships
```
Pgap = T × ωs
Pmech = (1-s) × Pgap
Pcu2 = s × Pgap
η ≈ (1-s) (approximately, ignoring other losses)
```

### V/f Limitations
```
Maximum torque independent of frequency (ideal)
Practical: torque decreases at very low frequency
Voltage boost needed below 10 Hz
Field weakening above rated frequency
```
