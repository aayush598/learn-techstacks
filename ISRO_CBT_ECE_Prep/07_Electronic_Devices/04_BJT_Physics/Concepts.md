# BJT Physics - Concepts

## BJT Structure

### NPN Transistor
```
Emitter (N+) ─── Base (P) ─── Collector (N)
   ← EB junction   ← CB junction
```
- Emitter: heavily doped (10¹⁹ cm⁻³)
- Base: thin, lightly doped (10¹⁷ cm⁻³)
- Collector: moderately doped (10¹⁵ cm⁻³)

### PNP Transistor
```
Emitter (P+) ─── Base (N) ─── Collector (P)
```
- Similar structure with opposite doping
- Current directions reversed

### Physical Dimensions
- Base width: WB ~ 0.1-1 μm
- Emitter width: ~1 μm
- Collector width: ~5 μm
- EB junction area < CB junction area

---

## Operating Modes

### 1. Active Mode (Forward Active)
- EB junction: forward biased
- CB junction: reverse biased
- Used for amplification
- IC = βIB

### 2. Saturation Mode
- EB junction: forward biased
- CB junction: forward biased
- Switch ON state
- VCE(sat) ≈ 0.2V

### 3. Cutoff Mode
- EB junction: reverse biased
- CB junction: reverse biased
- Switch OFF state
- IC ≈ 0

### 4. Reverse Active Mode
- EB junction: reverse biased
- CB junction: forward biased
- Poor performance (low β)
- Used in some logic families

---

## Current Components

### Emitter Current
$$I_E = I_B + I_C$$

### Collector Current
$$I_C = \alpha I_E + I_{CBO}$$

### Base Current
$$I_B = (1 - \alpha)I_E - I_{CBO}$$

### Current Components in NPN (Active Mode)
```
Emitter → Base: IE = IN + IPE
Base → Collector: IC = IN - IREC + IBC
Base → Emitter: IB = IPE + IREC - IBC
```

Where:
- IN = electron diffusion current
- IPE = hole injection from base to emitter
- IREC = recombination current in base
- IBC = base-collector reverse current

---

## Alpha (α) and Beta (β)

### Current Gain α (Common Base)
$$\alpha = \frac{I_C}{I_E}$$

Typical values: 0.95 - 0.999

### Current Gain β (Common Emitter)
$$\beta = \frac{I_C}{I_B}$$

Typical values: 20 - 1000

### Relationship
$$\beta = \frac{\alpha}{1 - \alpha}$$
$$\alpha = \frac{\beta}{1 + \beta}$$

### From Device Parameters
$$\alpha = \alpha_T \gamma$$

Where:
- αT = base transport factor = 1/(1 + WB²/2Ln²)
- γ = emitter injection efficiency = 1/(1 + NDpWB/(NBLEp))

---

## Ebers-Moll Model

### Injection Model
$$I_E = I_{ES}\left[\exp\left(\frac{V_{BE}}{V_T}\right) - 1\right] - \alpha_R I_{CS}\left[\exp\left(\frac{V_{BC}}{V_T}\right) - 1\right]$$

$$I_C = \alpha_F I_{ES}\left[\exp\left(\frac{V_{BE}}{V_T}\right) - 1\right] - I_{CS}\left[\exp\left(\frac{V_{BC}}{V_T}\right) - 1\right]$$

### Reciprocity Relation
$$\alpha_F I_{ES} = \alpha_R I_{CS}$$

### Ebers-Moll Parameters
| Parameter | Typical Value |
|-----------|---------------|
| IES | 10⁻¹⁴ - 10⁻¹² A |
| ICS | 10⁻¹⁴ - 10⁻¹² A |
| αF | 0.95 - 0.999 |
| αR | 0.1 - 0.5 |

---

## Early Effect (Base Width Modulation)

### Phenomenon
- Increase in VCB narrows effective base width
- Base width WB decreases
- Concentration gradient increases
- IC increases with VCB

### Early Voltage
$$V_A = \frac{I_C}{\frac{\partial I_C}{\partial V_{CE}}}$$

Typical values: 50-200V

### Output Resistance
$$r_o = \frac{V_A + V_{CE}}{I_C} \approx \frac{V_A}{I_C}$$

### Modified β
$$\beta_{eff} = \beta_0\left(1 + \frac{V_{CE}}{V_A}\right)$$

### Effects
1. IC increases slightly with VCE
2. Output resistance is finite
3. Increases bandwidth in CE configuration
4. Reduces voltage gain

---

## Gummel Plot

### Definition
Plot of ln(IC) and ln(IB) vs VBE

### Key Features
- IC vs VBE: exponential (linear on log scale)
- IB vs VBE: exponential
- β = IC/IB = slope ratio
- At high VBE: series resistance effects
- At low VBE: recombination current dominates

### Regions
1. Low VBE: IB dominated by recombination
2. Medium VBE: ideal region (β constant)
3. High VBE: series resistance effects

---

## Frequency Response

### Cutoff Frequency (fT)
$$f_T = \frac{1}{2\pi\tau_F}$$

Where τF = forward transit time

### Alpha Cutoff Frequency (fα)
$$f_\alpha = \frac{f_T}{\sqrt{1 - \alpha^2}} \approx f_T$$ (for α close to 1)

### Beta Cutoff Frequency (fβ)
$$f_\beta = \frac{f_T}{\beta_0}$$

### Transit Time Components
$$\tau_F = \tau_E + \tau_B + \tau_C + \tau_{CS}$$

Where:
- τE = emitter delay
- τB = base transit time = WB²/(2Dn)
- τC = collector depletion layer transit time
- τCS = collector substrate time

---

## Injection Efficiency

### Emitter Injection Efficiency
$$\gamma = \frac{I_{nE}}{I_{nE} + I_{pE}} = \frac{1}{1 + \frac{N_DBW}{N_ELE_P}}$$

Where:
- InE = electron current from emitter to base
- IpE = hole current from base to emitter
- ND = base doping
- NE = emitter doping
- BW = base width
- LE = emitter diffusion length

### For High γ
- NE >> ND (heavily doped emitter)
- BW << LE (thin emitter)

---

## Base Transport Factor

### Definition
$$\alpha_T = \frac{I_{nC}}{I_{nE}} = \frac{1}{1 + \frac{W_B^2}{2L_n^2}}$$

Where:
- InC = electron current reaching collector
- InE = electron current leaving emitter
- WB = base width
- Ln = electron diffusion length in base

### For High αT
- WB << Ln (thin base)
- Low recombination in base

---

## Current Components (Detailed)

### NPN in Active Mode
```
Emitter: IE = In + Ip (electrons + holes)
         ↓
Base:    In (electron diffusion) + Ip (hole recombination)
         ↓
Collector: IC ≈ In (electrons collected)
```

### Component Breakdown
1. **Electron diffusion** (dominant): In
2. **Hole injection**: Ip (base to emitter)
3. **Recombination**: Irec (in base)
4. **Reverse saturation**: ICBO

---

## Transistor Parameters

### Typical Values (2N2222A)
| Parameter | Value |
|-----------|-------|
| β (hFE) | 100-300 |
| α | 0.99-0.997 |
| VA | 100V |
| fT | 300 MHz |
| Cc | 8 pF |
| rbb' | 100 Ω |
| RE | 2 Ω |
| VCE(sat) | 0.3V |

### Temperature Coefficients
- β increases ~0.5-1%/°C
- VBE decreases ~2 mV/°C
- ICBO doubles per 10°C

---

## ISRO Key Points
- α = β/(1+β), β = α/(1-α)
- Early effect: IC increases with VCE
- fβ = fT/β
- VBE decreases 2 mV/°C
- β increases with temperature
- Ebers-Moll model valid in all regions
- Active mode: amplification
- Saturation: VCE(sat) ≈ 0.2V
