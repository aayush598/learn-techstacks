# Microwave Devices - Concepts

## Active Microwave Devices
- Generate/amplify signals at microwave frequencies (300 MHz - 300 GHz)
- Two classes: vacuum tubes and solid-state

## Vacuum Tube Devices
### Klystron (two-cavity)
- Uses velocity modulation and electron bunching
- Bunching -> current modulation -> power at output cavity
- Narrowband amplifier (typically)
- Reflex klystron: oscillator (single cavity + repeller)

### Magnetron
- Crossed E and B fields
- High power oscillator
- Used in radar transmitters (high power pulse)
- Rotation of electron cloud coupled to cavities

### TWT (Traveling Wave Tube)
- Slow-wave structure (helix) couples to electron beam
- Broadband amplification (frequency range wide)
- Moderate to high power
- Used in satellite & radar amplifiers
- Electron beam + RF signal amplify via interaction

### Crossed-field amplifier, Backward wave oscillator (BWO)
- Specialized high power devices

## Solid-State Devices
### Gunn Diode
- Made of GaAs
- Negative resistance (transferred electron/Gunn effect)
- Oscillator: simple, medium power, used in microwave sources
- No junction; bulk effect

### IMPATT Diode
- Impact Ionization Avalanche Transit Time
- Negative resistance from avalanche + transit time
- Higher power than Gunn, higher noise
- Used in oscillators

### Tunnel Diode
- Quantum tunneling negative resistance
- Very high frequency (sub-mm), low power

### Varactor Diode
- Voltage-variable capacitance
- Tuning, frequency multiplication, parametric amplification

### Schottky Diode
- Metal-semiconductor junction
- Fast switching (~THz), low forward drop
- Used in mixers, detectors, rectifiers at high freq

### HEMT (High Electron Mobility Transistor)
- Modulation-doped heterojunction
- Very high gain, low noise
- Used in LNAs (low-noise amplifiers)

### MESFET
- Metal-Semiconductor FET (GaAs)
- Microwave amplification, switching

## Power/Frequency Trade-off
```
Lower freq -> higher achievable power (vacuum tubes)
Higher freq -> lower power, solid state preferred
mm-wave: solid state emerging (GaN)
```

## Noise Performance
- Lowest noise: HEMT, BJT, then GaAs FET
- Vacuum tubes generally higher noise (except TWT moderate)

---

## ISRO Key Points
- Gunn: negative resistance bulk, oscillator
- IMPATT: avalanche + transit, higher power, noisy
- TWT: broadband amplifier (helix slow-wave)
- Klystron: narrowband, velocity modulation
- Magnetron: high power radar oscillator
- HEMT: low noise LNA
