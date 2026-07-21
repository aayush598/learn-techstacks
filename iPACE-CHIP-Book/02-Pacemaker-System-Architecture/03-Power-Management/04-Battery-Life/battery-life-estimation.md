# Battery Life Estimation

## 2.3.4 Energy Budget, Duty Cycle Analysis, and Lifetime Prediction

Battery life estimation is the process of predicting how long the pacemaker
will operate before the battery is depleted. This chapter provides a
comprehensive methodology for estimating battery life, including current
consumption per mode, duty cycle analysis, worst-case scenarios,
temperature effects, and aging considerations.

---

## 2.12.1 Battery Life Estimation Methodology

### Fundamental Equation

The battery life is determined by the ratio of available battery capacity
to the average current consumption:

```
  Battery Life (years) = C_batt / (I_avg × 8766)

  where:
    C_batt = battery capacity (Ah)
    I_avg = average current consumption (A)
    8766 = hours per year (365.25 × 24)
```

### Estimation Flow

```
                    BATTERY LIFE ESTIMATION FLOW

  ┌──────────────────────────────────────────────────────────────┐
  │                                                              │
  │  Step 1: Define battery parameters                           │
  │  ┌──────────────────────────────────────────────────────┐   │
  │  │ Chemistry: Li/CFₓ                                    │   │
  │  │ Nominal capacity: 3.0 Ah                             │   │
  │  │ Nominal voltage: 2.8 V                               │   │
  │  │ Self-discharge: 1% per year                          │   │
  │  │ End-of-life voltage: 2.4 V                           │   │
  │  └──────────────────────────────────────────────────────┘   │
  │                                                              │
  │  Step 2: Define operating conditions                         │
  │  ┌──────────────────────────────────────────────────────┐   │
  │  │ Pacing mode: DDDR                                    │   │
  │  │ Pacing rate: 60-70 bpm (average 65 bpm)              │   │
  │  │ Sensing: Dual-chamber                                │   │
  │  │ Rate adaptation: Accelerometer-based                 │   │
  │  │ Telemetry: Occasional (monthly follow-up)            │   │
  │  └──────────────────────────────────────────────────────┘   │
  │                                                              │
  │  Step 3: Calculate current per mode                          │
  │  ┌──────────────────────────────────────────────────────┐   │
  │  │ Active mode: 10 µA                                   │   │
  │  │ Sleep mode: 2 µA                                     │   │
  │  │ Deep sleep mode: 0.5 µA                              │   │
  │  └──────────────────────────────────────────────────────┘   │
  │                                                              │
  │  Step 4: Estimate duty cycle                                 │
  │  ┌──────────────────────────────────────────────────────┐   │
  │  │ Active: 0.1% (2.4 seconds per day)                   │   │
  │  │ Sleep: 99.9% (8637.6 seconds per day)                │   │
  │  └──────────────────────────────────────────────────────┘   │
  │                                                              │
  │  Step 5: Calculate average current                           │
  │  ┌──────────────────────────────────────────────────────┐   │
  │  │ I_avg = I_active × D_active + I_sleep × D_sleep      │   │
  │  │ I_avg = 10 × 0.001 + 2 × 0.999 = 2.008 µA          │   │
  │  └──────────────────────────────────────────────────────┘   │
  │                                                              │
  │  Step 6: Calculate battery life                              │
  │  ┌──────────────────────────────────────────────────────┐   │
  │  │ Life = 3.0 / (2.008e-6 × 8766) = 170,600 hours      │   │
  │  │ Life = 170,600 / 8766 = 19.5 years                   │   │
  │  │ With self-discharge: 19.5 × 0.99 = 19.3 years        │   │
  │  └──────────────────────────────────────────────────────┘   │
  │                                                              │
  └──────────────────────────────────────────────────────────────┘
```

---

## 2.12.2 Current Consumption per Mode

### Detailed Current Breakdown

| Block | Active (µA) | Sleep (µA) | Deep Sleep (µA) | Hibernate (µA) |
|-------|------------|-----------|----------------|---------------|
| AFE (sensing) | 1.5 | 1.5 | 0 | 0 |
| AFE (filtering) | 0.5 | 0.5 | 0 | 0 |
| Digital controller | 2.0 | 0.5 | 0 | 0 |
| Timers | 0.5 | 0.5 | 0.3 | 0.05 |
| ADC (battery monitor) | 0.3 | 0.1 | 0 | 0 |
| DAC (threshold) | 0.2 | 0.1 | 0 | 0 |
| Bandgap reference | 0.5 | 0.5 | 0.3 | 0.1 |
| LDO regulators | 1.0 | 0.5 | 0.2 | 0.05 |
| Buck converter | 0.3 | 0.2 | 0.1 | 0 |
| Charge pump | 0.2 | 0.1 | 0 | 0 |
| RF transceiver | 0 | 0 | 0 | 0 |
| Watchdog timer | 0.1 | 0.1 | 0.1 | 0.05 |
| Brown-out detector | 0.1 | 0.1 | 0.1 | 0.05 |
| Temperature sensor | 0.05 | 0.05 | 0 | 0 |
| Clock oscillator | 0.3 | 0.3 | 0.2 | 0.1 |
| **TOTAL** | **7.6** | **4.1** | **1.3** | **0.4** |

### Current per Operation

| Operation | Current | Duration | Energy | Frequency | Daily Energy |
|-----------|---------|----------|--------|-----------|-------------|
| Pacing pulse | 5 mA | 0.4 ms | 5.6 µJ | 93,600/day | 524 mJ |
| Sense event processing | 10 µA | 100 µs | 0.003 µJ | 187,200/day | 0.56 mJ |
| Telemetry TX (1 event) | 5 mA | 100 ms | 1400 µJ | 30/day | 42 mJ |
| Telemetry RX (1 event) | 2 mA | 500 ms | 2800 µJ | 30/day | 84 mJ |
| Impedance measurement | 100 µA | 50 ms | 140 µJ | 3/day | 0.42 mJ |
| Battery voltage check | 50 µA | 10 ms | 1.4 µJ | 8640/day | 121 mJ |
| Self-test | 100 µA | 100 ms | 28 µJ | 1440/day | 40.3 mJ |

---

## 2.12.3 Duty Cycle Analysis

### Typical Duty Cycle

```
  Time Distribution (24-hour period):

  ┌─────────────────────────────────────────────────────────────────────┐
  │                                                                     │
  │  SLEEP MODE (99.9%)                                                │
  │  ████████████████████████████████████████████████████████████████   │
  │  86,376 seconds per day                                            │
  │                                                                     │
  │  ACTIVE MODE (0.1%)                                                │
  │  █                                                                  │
  │  86.4 seconds per day                                              │
  │                                                                     │
  │  Breakdown of Active Mode:                                          │
  │  ├── Sensing: 86.4 s (continuous during active)                    │
  │  ├── Pacing: 0.094 s (93,600 pulses × 1 µs processing)           │
  │  ├── Telemetry: 0.9 s (30 events × 30 ms each)                   │
  │  ├── Diagnostics: 1.44 s (1440 events × 1 ms each)               │
  │  ├── Self-test: 14.4 s (1440 events × 10 ms each)                │
  │  └── Other: 69.56 s (miscellaneous processing)                    │
  │                                                                     │
  └─────────────────────────────────────────────────────────────────────┘
```

### Duty Cycle by Mode

| Mode | Duty Cycle | Hours/Day | Seconds/Day |
|------|-----------|-----------|------------|
| Active (Full) | 0.001% | 0.0864 | 3.11 |
| Active (Normal) | 0.05% | 0.12 | 432 |
| Sleep | 99.9% | 23.976 | 86,314 |
| Deep Sleep | 0% | 0 | 0 |
| Hibernate | 0% | 0 | 0 |
| Telemetry | 0.003% | 0.00864 | 31.1 |

### Duty Cycle Variation with Patient Activity

```
  Duty Cycle
  (% Active)
    │
  0.5├──────────────────────────────────────
    │
  0.4├──────────────╱╲──────────────────────
    │              ╱  ╲
  0.3├─────────────╱────╲────────────────────
    │            ╱      ╲
  0.2├───────────╱────────╲─────────────────
    │          ╱          ╲
  0.1├─────────╱────────────╲───────────────
    │        ╱              ╲
  0.0├───────╱────────────────╲─────────────
    │      ╱                  ╲
    0├─────╱────────────────────╲───────────
    0   6am  12pm  6pm  12am  6am  12pm
              Time of Day

    Resting: 0.001% active
    Walking: 0.01% active
    Exercise: 0.1-0.5% active
    Sleep: 0.0001% active
```

---

## 2.12.4 Average Current Calculation

### Weighted Average

```
  I_avg = Σ (I_mode × D_mode) + Σ (I_event × N_event × t_event / T_day)

  where:
    I_mode = current in each mode (µA)
    D_mode = duty cycle of each mode (fraction)
    I_event = current during each event type (µA)
    N_event = number of events per day
    t_event = duration of each event (s)
    T_day = seconds per day (86,400)

  I_avg = I_sleep × D_sleep + I_active × D_active + I_events

  I_avg = (4.1 × 0.999) + (7.6 × 0.001) + I_events

  I_events:
    Pacing: 5000 × 93600 × 0.0004 / 86400 = 2.16 µA
    Telemetry TX: 5000 × 30 × 0.1 / 86400 = 0.017 µA
    Telemetry RX: 2000 × 30 × 0.5 / 86400 = 0.035 µA
    Impedance: 100 × 3 × 0.05 / 86400 = 0.00017 µA
    Battery check: 50 × 8640 × 0.01 / 86400 = 0.005 µA
    Self-test: 100 × 1440 × 0.1 / 86400 = 0.167 µA

  I_events_total = 2.16 + 0.017 + 0.035 + 0.00017 + 0.005 + 0.167
                 = 2.384 µA

  I_avg = (4.1 × 0.999) + (7.6 × 0.001) + 2.384
        = 4.096 + 0.0076 + 2.384
        = 6.488 µA
```

### Summary Current Budget

| Category | Current (µA) | % of Total |
|----------|-------------|-----------|
| Sleep mode (background) | 4.096 | 63.1% |
| Pacing events | 2.160 | 33.3% |
| Active mode (processing) | 0.008 | 0.1% |
| Telemetry events | 0.052 | 0.8% |
| Self-test events | 0.167 | 2.6% |
| Other events | 0.005 | 0.1% |
| **TOTAL** | **6.488** | **100%** |

---

## 2.12.5 Battery Life Calculation

### Nominal Case

```
  Battery capacity: 3.0 Ah (Li/CFₓ)
  Average current: 6.488 µA
  Self-discharge: 1% per year

  Nominal life = C_batt / (I_avg × 8766)
               = 3.0 / (6.488e-6 × 8766)
               = 3.0 / 0.05686
               = 52.8 years

  With self-discharge: 52.8 × 0.99 = 52.3 years

  This seems too long! Let's check with a smaller battery...
```

### Realistic Battery Size

For a typical pacemaker battery:
```
  Battery volume: 2.0 cm³
  Energy density: 500 Wh/kg (Li/CFₓ)
  Density: 3.0 g/cm³
  Battery mass: 2.0 × 3.0 = 6.0 g
  Energy: 6.0 × 500 = 3000 Wh = 3.0 Ah × 1000 V... 

  Wait, let me recalculate:
  Energy density: 500 Wh/kg = 0.5 Wh/g
  Battery mass: 6.0 g
  Energy: 6.0 × 0.5 = 3.0 Wh
  Voltage: 2.8 V
  Capacity: 3.0 / 2.8 = 1.07 Ah

  Battery capacity: 1.07 Ah (realistic for a 2 cm³ battery)
```

### Recalculated Battery Life

```
  Battery capacity: 1.07 Ah
  Average current: 6.488 µA
  Self-discharge: 1% per year

  Nominal life = 1.07 / (6.488e-6 × 8766)
               = 1.07 / 0.05686
               = 18.8 years

  With self-discharge: 18.8 × 0.99 = 18.6 years

  With safety margin (20%): 18.6 × 0.8 = 14.9 years

  Target: 10 years → PASS ✓
```

---

## 2.12.6 Worst-Case Analysis

### Worst-Case Current Consumption

| Parameter | Nominal | Worst Case | Unit |
|-----------|---------|-----------|------|
| Sleep current | 4.1 | 6.0 | µA |
| Active current | 7.6 | 12.0 | µA |
| Pacing current | 2.16 | 5.0 | µA |
| Telemetry current | 0.052 | 0.5 | µA |
| Self-test current | 0.167 | 0.5 | µA |
| **Total average** | **6.49** | **14.0** | **µA** |

### Worst-Case Battery Life

```
  Battery capacity: 1.07 Ah
  Worst-case average current: 14.0 µA
  Self-discharge: 2% per year (worst case)

  Worst-case life = 1.07 / (14.0e-6 × 8766)
                  = 1.07 / 0.12272
                  = 8.7 years

  With safety margin (10%): 8.7 × 0.9 = 7.8 years

  Target: 10 years → MARGINAL ⚠️

  Mitigation: Reduce worst-case current or increase battery capacity
```

### Worst-Case Scenarios

| Scenario | Impact | Current Increase | Mitigation |
|----------|--------|-----------------|------------|
| High pacing rate (120 bpm) | More pacing pulses | +2.86 µA | Rate limiting |
| Frequent telemetry (daily) | More TX/RX events | +0.5 µA | Reduce telemetry frequency |
| High temperature (42°C) | Increased leakage | +1.0 µA | Thermal management |
| Battery aging (5 yr) | Reduced capacity | -10% capacity | Conservative estimation |
| Manufacturing variation | Higher quiescent | +0.5 µA | Production screening |

---

## 2.12.7 Temperature Effects

### Temperature Dependence of Current

```
  I(T) = I_25 × e^(Ea/k × (1/T - 1/298))

  where:
    I_25 = current at 25°C
    Ea = activation energy (0.3-0.5 eV for CMOS leakage)
    k = Boltzmann constant (8.617e-5 eV/K)
    T = temperature (K)

  At 37°C (body temperature):
    I(37) = I_25 × e^(0.4/8.617e-5 × (1/310 - 1/298))
          = I_25 × e^(4643 × (-0.000129))
          = I_25 × e^(-0.599)
          = I_25 × 0.549

  Wait, that's a decrease! Let me recalculate...

  Actually, leakage increases with temperature:
    I(37) = I_25 × e^(Ea/k × (1/310 - 1/298))
          = I_25 × e^(0.4/8.617e-5 × (-0.000129))
          = I_25 × e^(-0.599)
          = I_25 × 0.549

  Hmm, the sign is wrong. Let me use the correct formula:
    I(T) = I_25 × e^(Ea/k × (1/298 - 1/T))

  At 37°C:
    I(37) = I_25 × e^(0.4/8.617e-5 × (1/298 - 1/310))
          = I_25 × e^(4643 × 0.000129)
          = I_25 × e^(0.599)
          = I_25 × 1.82

  So current increases by ~82% at 37°C vs 25°C.
```

### Temperature Impact on Battery Life

| Temperature | Current Multiplier | Battery Life | Change from 25°C |
|------------|-------------------|-------------|-----------------|
| 25°C | 1.00× | 18.8 years | — |
| 37°C | 1.82× | 10.3 years | -45% |
| 42°C | 2.50× | 7.5 years | -60% |
| 20°C | 0.70× | 26.9 years | +43% |
| 15°C | 0.50× | 37.6 years | +100% |

---

## 2.12.8 Battery Aging Effects

### Capacity Fade Model

```
  C(t) = C_0 × (1 - α × t^β)

  where:
    C_0 = initial capacity
    α = aging coefficient (0.01-0.05 per year^β)
    β = aging exponent (0.5-1.0)
    t = time (years)

  For Li/CFₓ: α = 0.02, β = 0.8
    C(10) = C_0 × (1 - 0.02 × 10^0.8)
          = C_0 × (1 - 0.02 × 6.31)
          = C_0 × (1 - 0.126)
          = C_0 × 0.874

  12.6% capacity loss after 10 years
```

### Internal Resistance Growth

```
  R(t) = R_0 × (1 + γ × t^δ)

  where:
    R_0 = initial internal resistance
    γ = growth coefficient (0.05-0.2 per year^δ)
    δ = growth exponent (0.5-1.0)

  For Li/CFₓ: γ = 0.1, δ = 0.7
    R(10) = R_0 × (1 + 0.1 × 10^0.7)
          = R_0 × (1 + 0.1 × 5.01)
          = R_0 × 1.501

  50% increase in internal resistance after 10 years
```

### Aging Impact on Battery Life

| Age | Capacity | Internal R | Effective Life | Change |
|-----|----------|-----------|---------------|--------|
| 0 years | 100% | 100% | 18.8 years | — |
| 5 years | 93% | 125% | 17.5 years | -7% |
| 10 years | 87% | 150% | 16.4 years | -13% |
| 15 years | 82% | 175% | 15.4 years | -18% |

---

## 2.12.9 Manufacturing Variation

### Process Variation Impact

| Parameter | Nominal | -3σ | +3σ | Unit |
|-----------|---------|-----|-----|------|
| Sleep current | 4.1 | 3.0 | 5.5 | µA |
| Active current | 7.6 | 6.0 | 9.5 | µA |
| Bandgap current | 0.5 | 0.3 | 0.8 | µA |
| LDO quiescent | 1.0 | 0.7 | 1.5 | µA |
| Clock oscillator | 0.3 | 0.2 | 0.5 | µA |

### Worst-Case Manufacturing

```
  Worst-case (+3σ) average current:
    I_avg_wc = 14.0 µA (from Section 2.12.6)

  Battery life with worst-case manufacturing:
    Life_wc = 1.07 / (14.0e-6 × 8766) = 8.7 years

  Battery life with nominal manufacturing:
    Life_nom = 1.07 / (6.49e-6 × 8766) = 18.8 years

  Battery life with -3σ manufacturing:
    Life_best = 1.07 / (4.5e-6 × 8766) = 27.1 years
```

---

## 2.12.10 Battery Life Projection Summary

### Combined Effects

```
  Battery Life Projection:

  Nominal conditions:           18.8 years
  Temperature (37°C):          × 0.55 = 10.3 years
  Aging (10 years):            × 0.87 = 9.0 years
  Manufacturing (+3σ):         × 0.62 = 5.6 years

  Worst-case combined:          5.6 years

  With safety margin (20%):     5.6 × 0.8 = 4.5 years

  This is below the 10-year target!
```

### Design Optimization

To meet the 10-year target under worst-case conditions:

1. **Reduce sleep current**: From 4.1 µA to 2.0 µA (power gating)
2. **Reduce active current**: From 7.6 µA to 5.0 µA (voltage scaling)
3. **Increase battery capacity**: From 1.07 Ah to 1.5 Ah (larger battery)
4. **Reduce self-discharge**: From 1% to 0.5% per year (better sealing)

### Optimized Projection

```
  Optimized current budget:
    Sleep: 2.0 µA × 0.999 = 1.998 µA
    Active: 5.0 µA × 0.001 = 0.005 µA
    Pacing: 1.5 µA
    Telemetry: 0.03 µA
    Self-test: 0.1 µA
    Total: 3.633 µA

  Optimized battery: 1.5 Ah

  Optimized life (nominal): 1.5 / (3.633e-6 × 8766) = 46.5 years
  Optimized life (37°C): 46.5 × 0.55 = 25.6 years
  Optimized life (+ aging): 25.6 × 0.87 = 22.3 years
  Optimized life (+3σ): 22.3 × 0.62 = 13.8 years

  With safety margin (20%): 13.8 × 0.8 = 11.0 years

  Target: 10 years → PASS ✓
```

---

## 2.12.11 Battery Life Estimation Tools

### Simulation-Based Estimation

```
  Battery life estimation tool inputs:

  1. Battery parameters:
     - Chemistry (Li/CFₓ)
     - Nominal capacity (1.5 Ah)
     - Nominal voltage (2.8 V)
     - Self-discharge rate (0.5%/year)
     - Internal resistance vs. SOC

  2. Operating conditions:
     - Pacing mode (DDDR)
     - Pacing rate profile (60-120 bpm, duty cycle)
     - Sensing activity (dual-chamber)
     - Rate adaptation (accelerometer)
     - Telemetry frequency (monthly)

  3. Environmental conditions:
     - Temperature profile (35-42°C)
     - Temperature cycling

  4. Manufacturing variation:
     - Process corners (fast/typical/slow)
     - Component tolerances

  Output:
     - Battery life (years) for each scenario
     - Confidence interval (95%)
     - Sensitivity analysis
```

### Monte Carlo Simulation

```
  Monte Carlo battery life estimation:

  1. Define probability distributions for all variables:
     - Battery capacity: Normal(1.5, 0.1) Ah
     - Sleep current: LogNormal(2.0, 0.3) µA
     - Active current: LogNormal(5.0, 0.5) µA
     - Temperature: Uniform(35, 42) °C
     - Self-discharge: Uniform(0.3, 0.7) %/year

  2. Run 10,000 simulations with random sampling

  3. Calculate battery life for each simulation

  4. Generate distribution of battery life:
     - Mean: 14.2 years
     - Standard deviation: 2.8 years
     - 5th percentile: 9.6 years
     - 95th percentile: 19.1 years

  5. 95% confidence that battery life > 9.6 years

  Target: 10 years → MARGINAL (need to optimize)
```

---

## 2.12.12 Summary

Battery life estimation is a complex process that must account for:

1. **Current consumption per mode**: Detailed breakdown of current in
   active, sleep, deep sleep, and hibernate modes.

2. **Duty cycle analysis**: The fraction of time spent in each mode,
   which varies with patient activity and pacing requirements.

3. **Event-based current**: Pacing pulses, telemetry transactions, and
   self-test operations contribute significantly to average current.

4. **Temperature effects**: Body temperature (37°C) increases leakage
   current by ~80% compared to room temperature.

5. **Battery aging**: Capacity fade and internal resistance growth reduce
   effective battery life over time.

6. **Manufacturing variation**: Process variation can increase average
   current by up to 100% in worst-case units.

The combined effect of these factors must be analyzed to ensure that the
10-year battery life target is met under worst-case conditions with
adequate safety margin. The estimation methodology presented in this
chapter provides the tools and framework for this analysis.
