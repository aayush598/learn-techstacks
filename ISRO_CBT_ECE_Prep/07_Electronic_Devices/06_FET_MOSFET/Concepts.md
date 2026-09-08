# FET & MOSFET - Concepts

## Field Effect Transistor (FET)

### Basic Structure
- Voltage-controlled device
- Three terminals: Gate, Drain, Source
- Current controlled by electric field
- High input impedance (MΩ to GΩ)

### Types
1. **JFET**: Junction FET
2. **MOSFET**: Metal-Oxide-Semiconductor FET
3. **MESFET**: Metal-Semiconductor FET

---

## JFET

### Structure
- N-channel: N-type channel between P+ gates
- P-channel: P-type channel between N+ gates
- Symmetrical device (D and S interchangeable)

### Operating Principle
- Gate-source voltage controls channel width
- Reverse bias at gate-channel junction
- Depletion mode operation only

### Types
- **Depletion mode**: Normally ON (VGS = 0)
- **No enhancement mode** for JFET

### Channel Formation
- VGS = 0: maximum current (IDSS)
- VGS increases (reverse bias): channel narrows
- VGS = VP (pinch-off): channel closes

---

## JFET Characteristics

### Transfer Characteristic
$$I_D = I_{DSS}\left(1 - \frac{V_{GS}}{V_P}\right)^2$$

### Pinch-off Voltage (VP)
- VGS at which ID = 0
- Typical: -2V to -10V for N-channel
- Positive for P-channel

### Drain Current at VGS = 0
- IDSS: maximum drain current
- Typical: 1-20 mA

### Output Characteristics
- Linear region: VDS < VGS - VP
- Saturation region: VDS ≥ VGS - VP
- Ohmic region: small VDS

---

## JFET Parameters

### Transconductance
$$g_m = g_{m0}\left(1 - \frac{V_{GS}}{V_P}\right)$$

$$g_{m0} = \frac{2I_{DSS}}{|V_P|}$$

### Output Resistance
$$r_d = \frac{1}{\lambda I_D}$$

### Input Resistance
$$R_{in} = 10^9 - 10^{12} \text{ Ω}$$

---

## MOSFET Structure

### N-Channel Enhancement MOSFET
```
Source (N+) ──── Channel (P) ──── Drain (N+)
                    │
                    Gate (Metal)
                    │
                Oxide (SiO2)
```

### P-Channel Enhancement MOSFET
- Opposite doping
- Negative VGS for operation

### Four Terminals
1. Gate (G)
2. Drain (D)
3. Source (S)
4. Body/Bulk (B)

---

## MOSFET Types

### Enhancement Mode
- Normally OFF
- Requires VGS > VT to create channel
- Most common in digital circuits

### Depletion Mode
- Normally ON
- Channel exists at VGS = 0
- VGS controls current

### N-Channel vs P-Channel
| Parameter | N-Channel | P-Channel |
|-----------|-----------|-----------|
| Substrate | P-type | N-type |
| Carriers | Electrons | Holes |
| Mobility | Higher | Lower |
| VT | Positive | Negative |
| Speed | Faster | Slower |

---

## Threshold Voltage (VT)

### Definition
- Minimum gate voltage to create inversion layer
- VGS = VT: channel just forms
- Typical: 0.3-1V for modern MOSFETs

### Factors Affecting VT
1. Substrate doping (NA)
2. Oxide thickness (tox)
3. Gate material work function
4. Fixed oxide charge
5. Body effect

### Body Effect
$$V_T = V_{T0} + \gamma\left(\sqrt{2\phi_f + V_{SB}} - \sqrt{2\phi_f}\right)$$

Where:
- VT0 = threshold voltage at VSB = 0
- γ = body effect parameter
- φf = Fermi potential
- VSB = source-body voltage

---

## MOSFET Operating Regions

### 1. Cutoff Region
- VGS < VT
- ID = 0
- Switch OFF

### 2. Linear (Triode) Region
- VGS > VT and VDS < VGS - VT
- ID increases linearly with VDS
- Acts as voltage-controlled resistor

### 3. Saturation Region
- VGS > VT and VDS ≥ VGS - VT
- ID independent of VDS (ideal)
- Pinch-off at drain end
- Amplification region

### 4. Velocity Saturation
- High electric field
- ID saturates before VDS = VGS - VT
- Important in short-channel devices

---

## Drain Current Equations

### Linear Region
$$I_D = \mu_n C_{ox} \frac{W}{L}\left[(V_{GS} - V_T)V_{DS} - \frac{V_{DS}^2}{2}\right]$$

### Saturation Region
$$I_D = \frac{1}{2}\mu_n C_{ox} \frac{W}{L}(V_{GS} - V_T)^2$$

### With Channel Length Modulation
$$I_D = \frac{1}{2}\mu_n C_{ox} \frac{W}{L}(V_{GS} - V_T)^2(1 + \lambda V_{DS})$$

### Process Transconductance Parameter
$$k_n' = \mu_n C_{ox}$$

### MOSFET Transconductance Parameter
$$K_n = \frac{k_n' W}{2L} = \frac{\mu_n C_{ox} W}{2L}$$

---

## MOSFET Small-Signal Parameters

### Transconductance
$$g_m = \mu_n C_{ox} \frac{W}{L}(V_{GS} - V_T) = \sqrt{2\mu_n C_{ox} \frac{W}{L} I_D}$$

### Output Resistance
$$r_o = \frac{1}{\lambda I_D} = \frac{V_A}{I_D}$$

### Body Transconductance
$$g_{mb} = \eta g_m$$

Where η = gmb/gm typically 0.1-0.3

---

## Channel Length Modulation

### Phenomenon
- Increase in VDS narrows effective channel length
- Similar to Early effect in BJT
- Output resistance is finite

### Lambda (λ)
$$\lambda \propto \frac{1}{L}$$

Typical: 0.01-0.1 V⁻¹

### Output Resistance
$$r_o = \frac{1}{\lambda I_D}$$

---

## Velocity Saturation

### Phenomenon
- High electric field → carrier velocity saturates
- ID saturates before VDS = VGS - VT
- Important in short-channel devices

### Critical Field
$$E_{sat} \approx 10^4 \text{ V/cm (for Si)}$$

### Velocity Saturation Current
$$I_{D,sat} = W C_{ox} v_{sat}(V_{GS} - V_T)$$

---

## MOSFET Capacitances

### Gate-Source Capacitance
$$C_{gs} = \frac{2}{3}WLC_{ox} \text{ (saturation)}$$

### Gate-Drain Capacitance
$$C_{gd} = \frac{1}{3}WLC_{ox} \text{ (saturation)}$$

### Gate-Body Capacitance
$$C_{gb} = \frac{WLC_{ox}}{(1 + C_{ox}/C_{dep})}$$

---

## Power MOSFET

### Structure
- Vertical current flow
- DMOS (Double-diffused MOS)
- High current capability

### Applications
- Power switching
- Motor control
- DC-DC converters
- Audio amplifiers

---

## ISRO Key Points
- JFET: depletion mode only
- MOSFET: enhancement or depletion mode
- VT positive for N-channel enhancement
- IDSS = maximum drain current (JFET)
- gm = μnCox(W/L)(VGS-VT)
- Channel length modulation: λ
- Body effect: VT increases with VSB
