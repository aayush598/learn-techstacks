# Choppers - Formulas

## 1. Type A Chopper (Step-Down/Buck) Formulas

### Output Voltage
```
Vo = D × Vin
D = ton/T = ton × fsw
Vo/Vin = D (0 ≤ D ≤ 1)
```

### Average Output Current
```
Io = Vo/RL = D × Vin/RL
```

### RMS Output Voltage
```
Vo(rms) = Vin × √D   [for rectangular pulse]
Vo(rms) = Vin × √(ton/T)
```

### Ripple Voltage
```
ΔVo = (Vin - Vo) × D × T / L   [peak-to-peak]
ΔVo = Vin × D × (1-D) / (Lfsw)
ΔVo(%) = D × (1-D) × Vin / (Lfsw × Vo) × 100%
```

### Ripple Current
```
ΔIL = Vin × D × (1-D) / (Lfsw)
IL(peak) = Io + ΔIL/2
IL(min) = Io - ΔIL/2
```

### Power Relationships
```
Pin = Vin × Is(avg)   [source current average]
Pout = Vo × Io
η = Pout/Pin = Vo/Vin = D (ideal)
```

### Source Current
```
Is(avg) = D × Io   [average source current]
Is(rms) = Io × √D   [RMS source current]
```

## 2. Type B Chopper (Step-Up/Boost) Formulas

### Output Voltage
```
Vo = Vin/(1-D)
Vo/Vin = 1/(1-D)
D = 1 - Vin/Vo
```

### Average Inductor Current
```
IL(avg) = Io/(1-D) = Io × Vo/Vin
```

### Output Current
```
Io = Vin × D / ((1-D)² × RL)   [for CCM]
```

### Ripple Voltage
```
ΔVo = Io × D / (C × fsw)
```

### Ripple Current
```
ΔIL = Vin × D / (Lfsw)
```

### Power Flow (Regenerative Braking)
```
P = Vin × IL(avg)   [power returned to source]
P = Vo × Io × (1-D)   [from load side]
```

## 3. Type C Chopper (Two-Quadrant) Formulas

### First Quadrant (Motoring)
```
Vo = D1 × Vin   [D1 = duty of Q1]
Io > 0
```

### Second Quadrant (Regeneration)
```
Vo = Vin/(1-D2)   [D2 = duty of Q2]
Io < 0
```

### Average Output Voltage
```
Vo = D1 × Vin   [for first quadrant]
Vo = Vin/(1-D2)   [for second quadrant]
```

### Mode Transition
```
At transition: Vo = Vin (at D1 = D2 = 0.5 approximately)
Smooth transition between modes
```

## 4. Type E Chopper (Four-Quadrant) Formulas

### Quadrant I (Forward Motoring)
```
Vo = D1 × Vin   [Q1, Q4 PWM]
Io > 0
```

### Quadrant II (Forward Regeneration)
```
Vo = D2 × Vin   [Q2, Q3 PWM]
Io < 0
```

### Quadrant III (Reverse Motoring)
```
Vo = -D3 × Vin   [Q2, Q3 PWM with different duty]
Io < 0
```

### Quadrant IV (Reverse Regeneration)
```
Vo = -D4 × Vin   [Q1, Q4 PWM]
Io > 0
```

### Output Voltage Range
```
-Vin ≤ Vo ≤ +Vin
-Io(max) ≤ Io ≤ +Io(max)
```

## 5. Step-Up Chopper Formulas

### Voltage Gain
```
M = Vo/Vin = 1/(1-D)

M = 1: Vo = Vin (D = 0)
M = 2: Vo = 2Vin (D = 0.5)
M = 5: Vo = 5Vin (D = 0.8)
M = 10: Vo = 10Vin (D = 0.9)
```

### Duty Cycle for Required Output
```
D = 1 - Vin/Vo = (Vo - Vin)/Vo

For Vo = 3Vin: D = 1 - 1/3 = 0.667
For Vo = 5Vin: D = 1 - 1/5 = 0.8
```

### Inductor Current
```
IL(avg) = Io/(1-D) = Io × M
IL(peak) = IL(avg) + ΔIL/2
ΔIL = Vin × D / (Lfsw)
```

### Output Capacitor
```
C = Io × D / (ΔVo × fsw)
```

## 6. Jones Chopper Formulas

### Output Voltage
```
Vo = Vin × (N2/N1) × D/(1-D)   [with auto-transformer]

Where:
N2/N1 = turns ratio of auto-transformer
D = effective duty cycle
```

### Turns Ratio Effect
```
Higher N2/N1 → higher voltage gain for same D
D = 0.5, N2/N1 = 1: Vo = Vin
D = 0.5, N2/N1 = 2: Vo = 2Vin
```

### Energy Transfer
```
Eper_cycle = 0.5 × Lm × IL²   [energy stored in transformer]
Pout = Eper_cycle × fsw
```

## 7. Morgan Chopper Formulas

### Output Voltage
```
Vo = D × Vin   [step-down operation]
Same as Type A chopper
```

### Commutation Capacitor
```
C = It × tc / Vc   [for forced commutation]

Where:
It = anode current at commutation
tc = commutation time
Vc = capacitor voltage (≈ Vin)
```

### Minimum Capacitor Value
```
Cmin = It × tc / Vin

Must be large enough to turn off SCR completely
```

### Commutation Energy
```
Ecomm = 0.5 × C × Vc²
Ecomm must be sufficient to turn off SCR
```

## 8. Efficiency Formulas

### Conduction Losses
```
Pcond = I² × Rds(on) × D   [MOSFET]
Pcond = I² × Rdc            [inductor DC resistance]
Pcond = Vf × I × (1-D)      [freewheeling diode]
```

### Switching Losses
```
Psw = 0.5 × Vin × Ipeak × (tON + tOFF) × fsw
```

### Total Efficiency
```
η = Po / (Po + Pcond + Psw + Pcore)

Typical values:
Buck: 90-95%
Boost: 90-95%
Four-quadrant: 85-92%
```

## 9. Ripple Formulas

### Output Voltage Ripple (Buck)
```
ΔVo = Vin × D × (1-D) / (Lfsw)
ΔVo(%) = ΔVo/Vo × 100% = (1-D)/(Lfsw × C) × 100%  [with LC filter]
```

### Input Current Ripple (Boost)
```
ΔIin = Vin × D / (Lfsw)
ΔIin(%) = ΔIin/Iin(avg) × 100%
```

### Critical Inductance
```
For CCM: L > (1-D) × R/(2fsw)   [Buck]
For CCM: L > D × (1-D)² × R/(2fsw)   [Boost]
```
