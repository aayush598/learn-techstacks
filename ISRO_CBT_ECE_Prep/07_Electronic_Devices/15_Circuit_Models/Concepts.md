# Circuit Models - Concepts

## DC vs AC Analysis

### DC (Bias) Analysis
- Capacitors open circuit
- Inductors short circuit
- Determine Q-point
- Large-signal models used

### AC (Small-Signal) Analysis
- DC sources grounded
- Capacitors short circuit (high freq)
- Inductors open circuit
- Small-signal models used

---

## DC Equivalent Circuit

### BJT DC Model
```
VCC
 │
 RB
 │
 Base ──── VBE(≈0.7V) ──── Emitter
                    │
                  RE
                    │
                  GND
```

### BJT DC Relations
$$V_{BE} \approx 0.7V \text{ (Si, ON)}$$
$$V_{CE(sat)} \approx 0.2V$$
$$I_C = \beta I_B$$

### MOSFET DC Model
```
Gate ──── open (ID = 0)
VGS = VG - VS (for enhancement, > VT)
ID = (1/2)kn(W/L)(VGS-VT)² (saturation)
```

---

## AC Equivalent Circuit

### Steps
1. Set DC sources to zero
2. Replace device with small-signal model
3. Capacitors short-circuited
4. Solve for AC quantities

### BJT AC Model
```
Base ─ rπ ─ gmVbe ─ ro ─ Collector
              │
            Emitter
```

### MOSFET AC Model
```
Gate ─ gmVgs ─ ro ─ Drain
              │
            Source
```

---

## Two-Port Networks

### Definition
- Any circuit with input and output ports
- Port = pair of terminals
- Described by relations between V1, I1, V2, I2

### Port Variables
- V1, I1: input port
- V2, I2: output port

---

## Parameter Sets (Two-Port)

### 1. z-parameters (Open-circuit impedance)
$$\begin{bmatrix} V_1 \\ V_2 \end{bmatrix} = \begin{bmatrix} z_{11} & z_{12} \\ z_{21} & z_{22} \end{bmatrix} \begin{bmatrix} I_1 \\ I_2 \end{bmatrix}$$

### 2. y-parameters (Short-circuit admittance)
$$\begin{bmatrix} I_1 \\ I_2 \end{bmatrix} = \begin{bmatrix} y_{11} & y_{12} \\ y_{21} & y_{22} \end{bmatrix} \begin{bmatrix} V_1 \\ V_2 \end{bmatrix}$$

### 3. h-parameters (Hybrid)
$$\begin{bmatrix} V_1 \\ I_2 \end{bmatrix} = \begin{bmatrix} h_{11} & h_{12} \\ h_{21} & h_{22} \end{bmatrix} \begin{bmatrix} I_1 \\ V_2 \end{bmatrix}$$

### 4. g-parameters (Inverse hybrid)
$$\begin{bmatrix} I_1 \\ V_2 \end{bmatrix} = \begin{bmatrix} g_{11} & g_{12} \\ g_{21} & g_{22} \end{bmatrix} \begin{bmatrix} V_1 \\ I_2 \end{bmatrix}$$

### 5. ABCD (Transmission) parameters
$$\begin{bmatrix} V_1 \\ I_1 \end{bmatrix} = \begin{bmatrix} A & B \\ C & D \end{bmatrix} \begin{bmatrix} V_2 \\ -I_2 \end{bmatrix}$$

---

## h-Parameters for BJT

### CE Configuration
| Symbol | Name | Typical Value |
|--------|------|---------------|
| hie | Input impedance | 1-10 kΩ |
| hre | Reverse transfer | 10⁻⁴-10⁻³ |
| hfe | Forward current gain | 20-1000 |
| hoe | Output admittance | 1-50 μS |

### CB Configuration
| Symbol | Value |
|--------|-------|
| hib | 10-100 Ω |
| hrb | ~10⁻³ |
| hfb = -α | ~-0.99 |
| hob | 0.1-5 μS |

### CC Configuration
- hic = hie
- hrc ≈ 1
- hfc = -(1+β)
- hoc = hoe

---

## Model Selection

### BJT
- **Low frequency**: h-parameters (from datasheet)
- **High frequency**: hybrid-π model
- **Large signal**: Ebers-Moll

### MOSFET
- **Low frequency**: gm, ro, gmb
- **High frequency**: add Cgs, Cgd, Cgb
- **Large signal**: square-law model

---

## Amplifier Configurations

### CE (Common Emitter)
- High gain, inverting
- Medium input impedance
- Medium output impedance

### CC (Common Collector)
- Gain ≈ 1, non-inverting
- High input impedance
- Low output impedance (buffer)

### CB (Common Base)
- High gain, non-inverting
- Low input impedance
- High output impedance

---

## Hybrid-π to h-parameter Conversion

$$h_{ie} = r_b + r_\pi$$
$$h_{fe} = \beta$$
$$h_{oe} = \frac{1}{r_o}$$
$$h_{re} \approx 0$$

---

## ISRO Key Points
- 5 parameter sets: z, y, h, g, ABCD
- h-parameters: most common for BJT
- hie = input impedance, hfe = β
- DC analysis: caps open
- AC analysis: caps short, DC grounded
- CE: inverting, high gain
- CC: buffer (Av≈1)
- CB: low input impedance
