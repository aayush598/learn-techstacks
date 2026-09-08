# MOSFET Models - Concepts

## Large Signal Model

### Purpose
- Represents DC and large AC behavior
- Used for bias point calculation
- Nonlinear model

### Components
1. Voltage-controlled current source (gmVgs)
2. Output resistance (ro)
3. Body effect (gmbVbs)
4. Capacitances (Cgs, Cgd, Cgb)

---

## Small-Signal Model

### Hybrid-π Model
```
Gate ──── Cgs ──── Source
          │
          gmVgs
          │
          ro
          │
        Drain
```

### Parameters
| Parameter | Formula | Description |
|-----------|---------|-------------|
| gm | μnCox(W/L)(VGS-VT) | Transconductance |
| ro | 1/(λID) | Output resistance |
| gmb | ηgm | Body transconductance |
| Cgs | (2/3)WLCox | Gate-source capacitance |
| Cgd | WLCov | Gate-drain capacitance |

---

## Transconductance (gm)

### Definition
Change in drain current per unit change in gate-source voltage

$$g_m = \frac{\partial I_D}{\partial V_{GS}} \bigg|_{V_{DS},V_{SB}}$$

### Formulas
$$g_m = \mu_n C_{ox} \frac{W}{L}(V_{GS} - V_T)$$

$$g_m = \sqrt{2\mu_n C_{ox} \frac{W}{L} I_D}$$

$$g_m = \frac{2I_D}{V_{GS} - V_T} = \frac{2I_D}{V_{OV}}$$

### Key Points
- gm ∝ √ID
- gm ∝ (W/L)
- gm independent of λ

---

## Output Resistance (ro)

### Definition
Change in drain voltage per unit change in drain current

$$r_o = \frac{\partial V_{DS}}{\partial I_D} \bigg|_{V_{GS}}$$

### Formula
$$r_o = \frac{1}{\lambda I_D} = \frac{V_A}{I_D}$$

### Key Points
- ro ∝ 1/ID
- ro ∝ L (longer channel → higher ro)
- ro independent of W

---

## Body Transconductance (gmb)

### Definition
Change in drain current per unit change in source-body voltage

$$g_{mb} = \frac{\partial I_D}{\partial V_{SB}} \bigg|_{V_{GS},V_{DS}}$$

### Formula
$$g_{mb} = \frac{\gamma g_m}{2\sqrt{2\phi_f + V_{SB}}} = \eta g_m$$

### Typical Values
- η = gmb/gm ≈ 0.1-0.3
- Depends on VSB and doping

---

## T-Model

### Equivalent Circuit
```
Source ──── gmVgs ──── Gate
              │
              │
              ro
              │
            Drain
```

### Usage
- Better for common-gate configurations
- Easier to analyze certain circuits
- Same parameters as hybrid-π

### Conversion
$$g_m = g_{mT}$$
$$r_o = r_{oT}$$

---

## Capacitance Model

### Gate-Source Capacitance
$$C_{gs} = \frac{2}{3}WLC_{ox} \text{ (saturation)}$$

### Gate-Drain Capacitance
$$C_{gd} = WLC_{ov} \text{ (overlap)}$$

### Gate-Body Capacitance
$$C_{gb} = \frac{WLC_{ox}}{1 + C_{ox}/C_{dep}}$$

### Total Gate Capacitance
$$C_{gg} = C_{gs} + C_{gd} + C_{gb}$$

---

## Channel Length Modulation

### Lambda (λ)
- Represents finite output resistance
- λ ∝ 1/L
- Typical: 0.01-0.1 V⁻¹

### Output Resistance
$$r_o = \frac{1}{\lambda I_D}$$

### Modified Current
$$I_D = I_{D,sat}(1 + \lambda V_{DS})$$

### Early Voltage
$$V_A = \frac{1}{\lambda}$$

---

## Velocity Saturation Effects

### Modified gm
$$g_m = W C_{ox} v_{sat}$$ (velocity saturated)

### Modified ID
$$I_D = W C_{ox} v_{sat}(V_{GS} - V_T)$$

### Impact
- Reduces gm compared to long-channel
- Important in sub-micron devices

---

## Noise Models

### Thermal Noise
$$i_{nd}^2 = \frac{4kT\gamma}{r_{ds0}} B$$

Where γ = 2/3 (saturation), rds0 = 1/gm

### Flicker Noise
$$i_{nf}^2 = \frac{K_f I_D^2}{f C_{ox} WL} B$$

### Shot Noise
$$i_{ng}^2 = 2qI_G B$$ (gate leakage)

---

## Large vs Small Signal

| Aspect | Large Signal | Small Signal |
|--------|--------------|--------------|
| Analysis | DC + large AC | Small AC perturbations |
| Model | Nonlinear | Linearized |
| Purpose | Bias point | Gain, impedance |
| Parameters | ID, VDS, VGS | gm, ro, C |

---

## Model Selection

### Common Source
- Hybrid-π preferred
- gmVgs at input, ro at output

### Common Gate
- T-model preferred
- Input at source, output at drain

### Common Drain (Source Follower)
- Hybrid-π with load at source
- High input, low output impedance

---

## ISRO Key Points
- gm = μnCox(W/L)(VGS-VT) = 2ID/Vov
- ro = 1/(λID) = VA/ID
- gmb = ηgm, η ≈ 0.1-0.3
- Cgs = (2/3)WLCox in saturation
- Hybrid-π: most common small-signal model
- T-model: useful for common-gate
- λ ∝ 1/L, gm ∝ √ID
