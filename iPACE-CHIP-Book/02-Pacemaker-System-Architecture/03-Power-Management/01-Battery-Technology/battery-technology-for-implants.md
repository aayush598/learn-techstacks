# Battery Technology for Implantable Pacemakers

## 2.3.1 Primary Battery Chemistries and Characteristics

The battery is the sole energy source for the implantable pacemaker and must
reliably deliver power for 10-15 years without replacement. This chapter
covers the primary battery chemistries used in implantable medical devices,
their electrochemical characteristics, discharge behavior, and design
considerations for maximizing implant lifetime.

---

## 2.9.1 Battery Requirements for Implantable Pacemakers

### Key Requirements

| Parameter | Requirement | Justification |
|-----------|------------|---------------|
| Energy density | ≥ 500 Wh/kg | Minimize device size/weight |
| Calendar life | ≥ 12 years | Implant lifetime + margin |
| Self-discharge | ≤ 1% per year | Preserve capacity over life |
| Voltage stability | Flat discharge curve | Consistent pacing over life |
| Temperature range | 35-42°C (operating) | Body temperature |
| | -40 to +60°C (storage) | Sterilization, shipping |
| Hermeticity | ≤ 10⁻⁸ atm·cc/s He | Prevent electrolyte leakage |
| Biocompatibility | ISO 10993 | Implant in body |
| Safety | No thermal runaway | Patient safety |
| Voltage | 2.5-3.2 V nominal | Compatible with IC design |
| Current capability | 1-25 mA peaks | Pacing pulses |
| Pulse load capability | 25 mA for 1 ms | Pacing without voltage droop |
| Radiation tolerance | ≥ 100 krad(Si) | Radiation sterilization |

### Energy Budget

For a 10-year implant lifetime with typical pacing parameters:

```
Average current consumption: 10 µA
Pacing: 20 µA × 0.001% duty cycle = 0.2 µA average
Sensing: 1.5 µA continuous
Digital: 2.0 µA continuous
Telemetry: 5 mA × 0.01% duty cycle = 0.5 µA average
Power management: 3.5 µA continuous
Total average: ~10 µA

Battery capacity required:
C = I_avg × t = 10 µA × 10 years × 365.25 days/year × 24 hr/day
C = 10 × 10⁻⁶ × 10 × 365.25 × 24 × 3600
C = 10 × 10⁻⁶ × 3.156 × 10⁸
C = 3.156 Ah

With safety margin (20%): C_min = 3.156 × 1.2 = 3.787 Ah

Typical battery capacity: 1.0-3.0 Ah (single cell)
Multiple cells or higher energy density required for 10+ year life
```

---

## 2.9.2 Lithium-Iodine (Li/I₂) Batteries

### Chemistry

The lithium-iodine battery was the first widely used primary battery for
implantable pacemakers, introduced in the 1970s. The electrochemical
reaction is:

```
Anode:    2Li → 2Li⁺ + 2e⁻
Cathode:  I₂ + 2e⁻ → 2I⁻
Overall:  2Li + I₂ → 2LiI

Nominal voltage: 2.8 V
Theoretical energy density: 660 Wh/kg
Practical energy density: 200-300 Wh/kg
```

### Characteristics

| Parameter | Value | Unit |
|-----------|-------|------|
| Nominal voltage | 2.8 | V |
| Cutoff voltage | 2.0 | V |
| Energy density | 200-300 | Wh/kg |
| Self-discharge rate | 1-5% | per year |
| Internal resistance | 100-500 | Ω (increases with age) |
| Operating temperature | -40 to +70 | °C |
| Calendar life | 10-15 | years |
| Maximum continuous current | 1-5 | mA |
| Maximum pulse current | 10-20 | mA (1 ms) |
| Size (typical) | 20 × 20 × 6 | mm |
| Weight | 10-20 | g |
| Capacity (typical) | 1.0-2.5 | Ah |

### Discharge Curve

```
  Voltage
  (V)
    │
  3.0├──────────────────────────────────────────
    │
  2.8├──────┐
    │       │
  2.6├──────┤────────────────────────────────────
    │       │
  2.4├──────┤────────────────────────────────────
    │       │         Flat discharge region
  2.2├──────┤──────────────────────────────────╮
    │       │                                 │
  2.0├──────┤─────────────────────────────────┤── Cutoff
    │       │                                 │
  1.8├──────┤─────────────────────────────────┤
    │       │                                 │
  1.6├──────┤─────────────────────────────────┤
    │       │                                 │
  1.4├──────┤                                 │
    │       │                                 │
  1.2├──────┘                                 │
    │                                         │
    0├────┬────┬────┬────┬────┬────┬────┬────┤
    0   10%  20%  30%  40%  50%  60%  70%  80%
              Capacity Discharged (%)

    │←─────── Flat Region ───────→│←─ Knee ─→│
         (2.8V to 2.4V)           (2.4V to 2.0V)
         Duration: 70-80%          Duration: 20-30%
         of total life              of total life
```

### Advantages

1. **Proven track record**: Used in millions of pacemakers since the 1970s
2. **Simple construction**: No complex electrode structure required
3. **Good energy density**: 200-300 Wh/kg practical
4. **Low self-discharge**: 1-5% per year at body temperature
5. **Flat discharge curve**: Stable voltage over most of the discharge life
6. **Hermetic sealing**: Glass-to-metal or ceramic-to-metal seal

### Disadvantages

1. **Increasing internal resistance**: LiI is an ionic conductor with high
   resistivity. As the reaction proceeds, the internal resistance increases
   from ~100 Ω (fresh) to >1000 Ω (end of life), causing voltage droop
   under load.

2. **Voltage droop under load**: The high internal resistance causes
   significant voltage droop during high-current pulses (pacing):

```
  V_load = V_ocv - I_load × R_internal

  Example: I_load = 10 mA, R_internal = 500 Ω
  V_load = 2.8 - 0.01 × 500 = 2.8 - 5.0 = -2.2V (!)

  This means the battery cannot deliver 10 mA pulses directly.
  An output capacitor is required to buffer the pacing pulse.
```

3. **Iodine leakage risk**: If the hermetic seal is compromised, iodine
   can leak into the body, causing tissue damage.

4. **Limited pulse capability**: Cannot deliver high-current pulses
   directly; requires external capacitor for pacing.

---

## 2.9.3 Lithium-Silver Vanadium Oxide (Li/SVO) Batteries

### Chemistry

The lithium-silver vanadium oxide battery offers higher energy density and
lower internal resistance than Li/I₂:

```
Anode:    Li → Li⁺ + e⁻
Cathode:  Ag₂VO₄ + xLi⁺ + xe⁻ → Li_xAg₂VO₄
Overall:  2Li + Ag₂VO₄ → 2Ag + Li₂VO₄

Nominal voltage: 3.0 V
Theoretical energy density: 800 Wh/kg
Practical energy density: 300-500 Wh/kg
```

### Characteristics

| Parameter | Value | Unit |
|-----------|-------|------|
| Nominal voltage | 3.0 | V |
| Cutoff voltage | 2.5 | V |
| Energy density | 300-500 | Wh/kg |
| Self-discharge rate | 1-3% | per year |
| Internal resistance | 10-50 | Ω (low, stable) |
| Operating temperature | -40 to +70 | °C |
| Calendar life | 10-15 | years |
| Maximum continuous current | 5-20 | mA |
| Maximum pulse current | 50-100 | mA (1 ms) |
| Capacity (typical) | 1.5-3.0 | Ah |

### Advantages

1. **Lower internal resistance**: 10-50 Ω vs. 100-500 Ω for Li/I₂,
   enabling higher pulse currents without significant voltage droop.

2. **Higher energy density**: 300-500 Wh/kg vs. 200-300 Wh/kg for Li/I₂.

3. **Better pulse capability**: Can deliver 50-100 mA pulses directly,
   reducing the need for large output capacitors.

4. **Flatter voltage curve**: More stable voltage during discharge.

### Disadvantages

1. **Higher cost**: Silver (Ag) is an expensive material.

2. **Two-stage discharge**: The SVO cathode undergoes two reduction
   stages, creating a slight voltage step during discharge.

3. **Less proven**: Fewer years of clinical history than Li/I₂.

---

## 2.9.4 Lithium-Carbon Monofluoride (Li/CFₓ) Batteries

### Chemistry

The lithium-carbon monofluoride battery offers the highest energy density
of commonly used implantable battery chemistries:

```
Anode:    Li → Li⁺ + e⁻
Cathode:  (CFₓ)ₙ + nxLi⁺ + nxe⁻ → nC + nLiF
Overall:  xLi + CFₓ → xLiF + C

Nominal voltage: 2.8 V
Theoretical energy density: 2200 Wh/kg
Practical energy density: 500-800 Wh/kg
```

### Characteristics

| Parameter | Value | Unit |
|-----------|-------|------|
| Nominal voltage | 2.8 | V |
| Cutoff voltage | 2.0 | V |
| Energy density | 500-800 | Wh/kg |
| Self-discharge rate | 0.5-2% | per year |
| Internal resistance | 20-100 | Ω |
| Operating temperature | -40 to +70 | °C |
| Calendar life | 12-20 | years |
| Maximum continuous current | 5-15 | mA |
| Maximum pulse current | 30-80 | mA (1 ms) |
| Capacity (typical) | 2.0-4.0 | Ah |

### Discharge Curve

```
  Voltage
  (V)
    │
  3.0├──────────────────────────────────────────
    │
  2.8├──────┐
    │       │
  2.6├──────┤────────────────────────────────────
    │       │
  2.4├──────┤────────────────────────────────────
    │       │
  2.2├──────┤──────────────────────────────────╮
    │       │                                 │
  2.0├──────┤─────────────────────────────────┤── Cutoff
    │       │                                 │
  1.8├──────┤─────────────────────────────────┤
    │       │                                 │
    0├────┬────┬────┬────┬────┬────┬────┬────┤
    0   10%  20%  30%  40%  50%  60%  70%  80%
              Capacity Discharged (%)

    Very flat discharge curve over 80% of life
    Excellent voltage stability
```

### Advantages

1. **Highest energy density**: 500-800 Wh/kg, enabling the longest implant
   lifetime or smallest battery size.

2. **Excellent voltage stability**: Very flat discharge curve over 80% of
   the discharge life.

3. **Low self-discharge**: 0.5-2% per year, the lowest of the common
   implantable chemistries.

4. **Long calendar life**: 12-20 years, suitable for long-life implants.

5. **No iodine leakage risk**: Unlike Li/I₂, there is no hazardous iodine
   in the cathode.

### Disadvantages

1. **Lower pulse capability**: Cannot deliver as high pulse currents as
   Li/SVO; requires output capacitor for pacing.

2. **Voltage delay**: At low temperatures or after long storage, a voltage
   delay may occur when a load is first applied (due to passivation layer
   on the lithium anode).

3. **Cost**: Higher material and manufacturing cost than Li/I₂.

4. **CFₓ material variability**: The carbon monofluoride material can have
   variable stoichiometry, affecting performance consistency.

---

## 2.9.5 Hybrid Chemistries

### Li/SVO + CFₓ (Hybrid)

Some advanced pacemaker batteries use a hybrid cathode combining SVO and
CFₓ to optimize both energy density and pulse capability:

```
  Li/SVO + CFₓ Hybrid:

  SVO component: Provides high pulse current capability
  CFₓ component: Provides high energy density

  Combined benefits:
  - Energy density: 400-600 Wh/kg
  - Pulse capability: 50-100 mA
  - Self-discharge: 1-2% per year
  - Flat discharge curve
```

### Li/MnO₂ (Lithium Manganese Dioxide)

Used in some smaller pacemaker designs:

| Parameter | Value | Unit |
|-----------|-------|------|
| Nominal voltage | 3.0 | V |
| Energy density | 250-350 | Wh/kg |
| Self-discharge | 1-3% | per year |
| Internal resistance | 20-80 | Ω |

---

## 2.9.6 Battery Comparison Summary

| Parameter | Li/I₂ | Li/SVO | Li/CFₓ | Li/SVO+CFₓ | Unit |
|-----------|-------|--------|--------|-----------|------|
| Nominal voltage | 2.8 | 3.0 | 2.8 | 2.9 | V |
| Energy density | 200-300 | 300-500 | 500-800 | 400-600 | Wh/kg |
| Self-discharge | 1-5 | 1-3 | 0.5-2 | 1-2 | %/yr |
| Internal resistance | 100-500 | 10-50 | 20-100 | 15-60 | Ω |
| Max pulse current | 10-20 | 50-100 | 30-80 | 50-100 | mA |
| Calendar life | 10-15 | 10-15 | 12-20 | 12-18 | years |
| Cost | Low | High | Medium | High | — |
| Maturity | Very high | High | Medium | Medium | — |
| Typical capacity | 1.0-2.5 | 1.5-3.0 | 2.0-4.0 | 2.0-3.5 | Ah |

---

## 2.9.7 Battery Aging and End-of-Life

### Capacity Fade Mechanisms

1. **Active material consumption**: The electrochemical reaction consumes
   the active materials (lithium anode, cathode), reducing the available
   capacity.

2. **Internal resistance growth**: As the reaction products accumulate,
   the internal resistance increases, reducing the available voltage under
   load.

3. **Electrolyte depletion**: The electrolyte is consumed or degraded over
   time, reducing ionic conductivity.

4. **Passivation layer growth**: A passivation layer forms on the lithium
   anode, increasing impedance and reducing active surface area.

### End-of-Life Criteria

| Parameter | End-of-Life Threshold | Unit |
|-----------|----------------------|------|
| Open-circuit voltage | < 2.4 | V |
| Internal resistance | > 2000 | Ω |
| Capacity remaining | < 20% | of initial |
| Pulse voltage under load | < 2.0 | V at 10 mA |
| Low-battery indicator | Activated | — |

### Battery Depletion Timeline

```
  Battery Capacity
  (% of initial)
    │
  100├──────────────────────────────────────────
    │
   80├──────────────────────────────────────────
    │
   60├──────────────────────────────────────────
    │
   40├──────────────────────────────────────────
    │
   20├────────────────────────────────────────── ← EOL Threshold
    │
    0├────┬────┬────┬────┬────┬────┬────┬────
    0   1yr  2yr  4yr  6yr  8yr  10yr 12yr 14yr

    │←── Normal Operation ──→│←─ Low Battery ─→│
    │                        │   Indicator ON   │
    │                        │   Output reduced │
    │                        │                  │
    │                        │←─ EOL Margin ──→│
```

---

## 2.9.8 Battery Selection Guidelines

### Selection Criteria

1. **Implant lifetime requirement**: Longer lifetime → higher energy density
   chemistry (CFₓ or hybrid).

2. **Pacing output requirements**: Higher pacing current → lower internal
   resistance chemistry (SVO or hybrid).

3. **Device size constraints**: Smaller device → higher energy density
   chemistry.

4. **Cost constraints**: Lower cost → Li/I₂; higher budget → SVO or CFₓ.

5. **Regulatory history**: More clinical history → Li/I₂; newer chemistry
   → more clinical data required.

### Recommended Chemistry by Application

| Application | Recommended Chemistry | Rationale |
|------------|----------------------|-----------|
| Simple VVI (5-yr life) | Li/I₂ | Low cost, proven, sufficient energy |
| DDD (10-yr life) | Li/SVO or CFₓ | Higher energy, lower resistance |
| DDDR (10-yr life) | Li/CFₓ or hybrid | Highest energy for rate adaptation power |
| CRT-P (10-yr life) | Li/CFₓ or hybrid | Highest energy for 3-chamber pacing |
| CRT-D (8-yr life) | Li/SVO | High pulse capability for defibrillation |
| Next-gen CRM | Li/CFₓ or hybrid | Maximum energy density |

---

## 2.9.9 Battery Monitoring in Pacemaker IC

### Voltage Monitoring

The pacemaker IC includes a battery voltage monitoring circuit that
continuously monitors the battery voltage:

```
                    BATTERY VOLTAGE MONITORING

  Battery ────────┬────────────────────────────
                  │
                  ▼
            ┌──────────┐
            │  Voltage │
            │  Divider │ (R1, R2)
            └────┬─────┘
                 │
                 ▼
            ┌──────────┐
            │  ADC     │ (8-10 bit)
            │  Input   │
            └────┬─────┘
                 │
                 ▼
            ┌──────────────────────────────────┐
            │         DIGITAL PROCESSOR         │
            │                                   │
            │   V_batt = ADC_value × K_divider  │
            │                                   │
            │   If (V_batt < V_eol) then        │
            │       Set EOL flag                │
            │       Reduce pacing output        │
            │       Transmit low-battery alert  │
            │                                   │
            │   If (V_batt < V_critical) then   │
            │       Enter hibernate mode        │
            │       Minimum pacing only         │
            │                                   │
            └──────────────────────────────────┘
```

### Voltage Thresholds

| Threshold | Voltage | Action |
|-----------|---------|--------|
| Normal operation | > 2.6 V | Full function |
| Low battery warning | 2.4-2.6 V | Alert clinician, reduce output |
| Critical battery | 2.2-2.4 V | Minimum function, hibernate |
| End of life | < 2.2 V | Device shutdown |

---

## 2.9.10 Summary

The battery is the most critical component for implant lifetime:

1. **Li/I₂**: Proven, low cost, but high internal resistance limits pulse
   capability. Suitable for simple, lower-cost pacemakers.

2. **Li/SVO**: Lower internal resistance, higher pulse capability, moderate
   energy density. Good balance for dual-chamber pacemakers.

3. **Li/CFₓ**: Highest energy density, longest calendar life, excellent
   voltage stability. Best for long-life, high-function pacemakers.

4. **Li/SVO+CFₓ hybrid**: Combines the best of both chemistries. Highest
   performance but higher cost.

The choice of battery chemistry directly impacts the pacemaker's implant
lifetime, device size, pacing capability, and cost. The battery monitoring
circuit in the pacemaker IC provides continuous surveillance and automatic
response to battery depletion, ensuring patient safety throughout the
implant lifetime.
