# Small Signal Models - Concepts

## Purpose of Small-Signal Models

### Definition
- Linearized model valid for small perturbations around operating point
- Replace nonlinear device with linear equivalent circuit
- Used for AC analysis: gain, impedance, frequency response

### Validity
- Signal amplitudes small: v_AC << VT (~26 mV)
- Device operates at fixed Q-point
- Superposition applies

---

## BJT Hybrid-π Model

### Circuit Components
```
        IB       rπ ✓                    IC
   Base ●──┬─────┬───────────┬───────────● Drain
           │     │           │           │
           │    Cπ          gmVπ         ro
           │     │           │           │
           │     │           │           │
   Base ●──┴─────┴───────────┴───────────● Emitter
```

### Parameters
| Parameter | Formula | Description |
|-----------|---------|-------------|
| gm | IC/VT | Transconductance |
| rπ | β/gm = VT/IB | Input resistance |
| ro | VA/IC | Output resistance |
| Cπ | Cje + Cd | Base-emitter capacitance |
| Cμ | Ccb | Collector-base capacitance |

---

## BJT Small-Signal Parameters

### Transconductance
$$g_m = \frac{I_C}{V_T} = 40 I_C \quad \text{(S, if IC in A)}$$

### Input Resistance
$$r_\pi = \frac{V_T}{I_B} = \frac{\beta}{g_m}$$

### Emitter Resistance
$$r_e = \frac{V_T}{I_E} = \frac{\alpha}{g_m}$$

### Output Resistance
$$r_o = \frac{V_A}{I_C}$$

### Topologies
| Model | Uses |
|-------|------|
| Hybrid-π | CE amplifier (most common) |
| T-model (re) | CB, CC amplifiers |
| h-parameters | Manufacturer specs, low frequency |

---

## MOSFET Small-Signal Model

### Circuit Components
```
        Gate                          Drain
   G ●──┬──────────────────────┬────● D
        │                      │    │
       Cgd        gmVgs        │   ro
        │          │           │    │
   S ●──┴──────────┴───────────┴────● S
```

### Parameters
| Parameter | Formula | Description |
|-----------|---------|-------------|
| gm | 2ID/Vov | Transconductance |
| ro | 1/(λID) | Output resistance |
| gmb | ηgm | Body effect |
| Cgs | (2/3)WLCox | Gate-source cap |
| Cgd | Cgdo | Gate-drain cap |

---

## MOSFET Transconductance

### Formulas
$$g_m = \mu_n C_{ox} \frac{W}{L}(V_{GS} - V_T)$$

$$g_m = \sqrt{2\mu_n C_{ox} \frac{W}{L} I_D}$$

$$g_m = \frac{2I_D}{V_{GS} - V_T} = \frac{2I_D}{V_{OV}}$$

### gm/ID
$$\frac{g_m}{I_D} = \frac{2}{V_{OV}}$$

---

## MOSFET Output Resistance

### Definition
$$r_o = \frac{\partial V_{DS}}{\partial I_D} = \frac{1}{\lambda I_D} = \frac{V_A}{I_D}$$

### Key Points
- Finite due to channel length modulation
- Inversely proportional to ID
- Larger for longer channels

---

## Body Transconductance

### Definition
$$g_{mb} = \frac{\partial I_D}{\partial V_{SB}} = \eta g_m$$

### η Range
η = 0.1-0.3

### Effect
- Reduces gain
- Considered in back-gate analysis
- Important in bulk isolation

---

## T-Model (BJT)

### Circuit
```
    Base ──(rπ)──┬── Emitter
                 │
                 │
               αie
                 │
    Collect ─────┘
```

### Parameters
| Parameter | Relation |
|-----------|----------|
| re | VT/IE = α/gm |
| rb | base resistance |
| rc | collector resistance |

### Usage
- Common base analysis
- Common collector analysis
- Easier for some configurations

---

## h-Parameters (BJT)

### Two-Port Equations
$$v_{be} = h_{11} i_b + h_{12} v_{ce}$$
$$i_c = h_{21} i_b + h_{22} v_{ce}$$

### Parameters
| h-Parameter | Name | Definition |
|-------------|------|------------|
| h11 = hie | Input impedance | vbe/ib (vce=0) |
| h12 = hre | Reverse transfer | vbe/vce (ib=0) |
| h21 = hfe | Forward current gain | ic/ib (vce=0) |
| h22 = hoe | Output admittance | ic/vce (ib=0) |

### Relation to Hybrid-π
- hie = rπ
- hfe = β
- hoe = 1/ro
- hre ≈ 0 (usually negligible)

---

## Frequency Response

### Low-Frequency Cutoff
- Due to coupling/bypass capacitors
- Sets lower -3dB point

### High-Frequency Cutoff
- Due to internal capacitances (Cπ, Cμ)
- Miller effect on Cμ
- Sets upper -3dB point

### Gain-Bandwidth Product
$$GBW = \frac{g_m}{2\pi C_{in}}$$

---

## Comparison: BJT vs MOSFET Small Signal

| Parameter | BJT | MOSFET |
|-----------|-----|--------|
| gm | IC/VT (~40IC) | 2ID/Vov |
| Input R | rπ (finite) | ∞ (ideal) |
| Output R | ro = VA/IC | ro = 1/(λID) |
| Control | Current (IB) | Voltage (VGS) |
| Transconductance | Higher per mA | Lower per mA |

---

## ISRO Key Points
- gm(BJT) = IC/VT = 40IC
- gm(MOSFET) = 2ID/Vov
- rπ = β/gm, ro = VA/IC
- ro(MOSFET) = 1/(λID)
- Hybrid-π most common BJT model
- gmb = ηgm (body effect)
- Miller effect multiplies Cμ input
