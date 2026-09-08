# Bandgap Reference - Concepts

## Bandgap vs Temperature

### Energy Gap Temperature Dependence
$$E_g(T) = E_g(0) - \frac{\alpha T^2}{T + \beta}$$

| Material | Eg(0) (eV) | α (×10⁻⁴ eV/K) | β (K) | Eg(300K) |
|----------|------------|-----------------|-------|----------|
| Si | 1.17 | 4.73 | 636 | 1.12 |
| Ge | 0.74 | 4.77 | 235 | 0.67 |
| GaAs | 1.52 | 5.41 | 204 | 1.43 |
| InP | 1.42 | 4.9 | 327 | 1.35 |

### Key Properties
- Eg decreases with temperature
- Nearly linear near room temperature
- dEg/dT ≈ -0.27 meV/K for Si at 300K
- Bandgap determines device materials and wavelengths

---

## VBE Temperature Dependence

### BJT Base-Emitter Voltage
$$V_{BE}(T) = V_{BE}(T_0) - \frac{E_g - V_{BE}}{T}(T - T_0)$$

### Simplified
$$V_{BE}(T) = 1.2 - \left(\frac{1.2 - V_{BE0}}{T_0}\right)T - (n-1)V_T \ln\left(\frac{T}{T_0}\right)$$

### Practical Form
$$V_{BE}(T) \approx V_{G0} - \frac{T}{T_0}(V_{G0} - V_{BE0})$$

Where VG0 ≈ 1.2V (extrapolated to 0K)

### Temperature Coefficient
$$\frac{dV_{BE}}{dT} \approx -2 \text{ mV/°C}$$

---

## Why Negative TC of VBE?

### VBE Formula
$$V_{BE} = \frac{kT}{q} \ln\left(\frac{I_C}{I_S}\right)$$

### Is Temperature Dependence
$$I_S \propto T^3 \exp\left(-\frac{E_g}{kT}\right)$$

### Derivation
$$\frac{dV_{BE}}{dT} = \frac{V_{BE} - E_g/q - 3kT/q}{T} < 0$$

### Result
dVBE/dT ≈ -1.5 to -2.2 mV/°C

---

## PTAT Current (Proportional To Absolute Temperature)

### Concept
- Current proportional to absolute temperature
- Generated using ΔVBE

### ΔVBE Generation
$$\Delta V_{BE} = V_{BE1} - V_{BE2} = V_T \ln\left(\frac{I_1}{I_2}\right)$$

For two BJTs with different currents (or areas):
$$\Delta V_{BE} = V_T \ln(N)$$

Where N = current density ratio

### PTAT Current
$$I_{PTAT} = \frac{\Delta V_{BE}}{R} = \frac{V_T \ln(N)}{R}$$

### Temperature Coefficient
$$\frac{dI_{PTAT}}{dT} = \frac{k \ln(N)}{qR} > 0$$

---

## Bandgap Voltage Reference

### Principle
Sum a positive-TC voltage (proportional to VT) with negative-TC VBE to get temperature-independent output.

### Basic Circuit
```
VREF = VBE + K×VT
                          
            +---------------- VREF
            |
         ___|
        |   |
        |...|  VBE (negative TC)
        |   |
            |
         (K×VT added, positive TC)
```

### Output
$$V_{REF} = V_{BE} + K V_T$$

### Choose K such that:
$$\frac{dV_{BE}}{dT} + K \frac{dV_T}{dT} = 0$$

$$\frac{dV_T}{dT} = \frac{k}{q} = 86 \mu\text{V/K}$$

$$K = \frac{|dV_{BE}/dT|}{k/q} = \frac{2 \text{ mV/K}}{0.086 \text{ mV/K}} \approx 23$$

### Result
$$V_{REF} = V_{BE} + 23 \times V_T \approx 1.2 \text{ V}$$

---

## Brokaw Bandgap Reference

### Circuit Configuration
- Two BJTs with different emitter areas
- Current mirror
- Feedback amplifier

### Operation
- Currents forced in ratio N
- ΔVBE developed across R1
- PTAT current flows
- VREF = VBE + 2×R2/R1 × VT×ln(N)

### Advantages
- ~1.2V reference
- Temperature independent
- Low temperature drift

---

## Bandgap Reference Temperature Behavior

### First-Order Cancellation
- Cancels linear temperature dependence
- Higher order terms remain (curvature)

### Curvature
- VBE has nonlinear (ln(T)) terms
- Perfect cancellation impossible with simple circuit

### Curvature Compensation
- Second-order correction circuits
- Reduces drift to < 10 ppm/°C

---

## Sources of Error

### 1. Process Variations
- Resistor mismatch
- Transistor mismatch
- Oxide thickness variation

### 2. Temperature Effects
- Non-linear VBE
- Resistor temperature coefficient
- Op-amp offset

### 3. Packaging Effects
- Mechanical stress
- Thermal gradients

---

## ISRO Key Points
- VBE ≈ -2 mV/°C (negative TC)
- VT = +0.086 mV/°C (positive TC)
- Bandgap reference: VREF ≈ 1.2V
- K ≈ 23 (ratio to cancel TC)
- VG0 ≈ 1.2V (Si extrapolated to 0K)
- dEg/dT ≈ -0.27 meV/K (Si)
- Brokaw circuit: classic bandgap reference
