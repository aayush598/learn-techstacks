# Diode Circuits - Concepts

## Ideal Diode
- Forward bias (V_anode > V_cathode): short circuit (ON)
- Reverse bias: open circuit (OFF)
- Instantaneous switching, no drop (ideal)

## Practical Diode
- Cutin/Threshold voltage V_gamma (~0.7V Si, ~0.3V Ge, ~0.2V Schottky)
- Forward conduction above threshold
- Reverse breakdown (Zener) at high reverse voltage
- Real: series resistance, reverse saturation current

## Diode Equation
```
I = Is (e^(V/(n VT)) - 1)
VT = kT/q ~ 25.85 mV at 300K (~26 mV)
n = ideality factor (1-2)
Is = reverse saturation current
```

## Rectifier Configurations

### Half-Wave Rectifier
```
V_dc = V_m/pi (ideal, ignoring drop)
Output: only positive half cycles
PIV = V_m (peak inverse voltage)
Frequency: same as input
Ripple heavily present
```

### Full-Wave (Center-Tap)
```
V_dc = 2 V_m/pi
Two diodes, center-tapped transformer
PIV = 2 V_m (per diode)
Output freq = 2x input
```

### Bridge Rectifier
```
V_dc = 2 V_m/pi
4 diodes, no center tap
PIV = V_m
Output freq = 2x input
Most common full-wave configuration
```

## Rectifier Parameters
```
Average output: V_dc
Ripple factor: r = V_rms_ac/V_dc
  Half-wave: 1.21
  Full-wave: 0.48
Form factor: V_rms/V_dc
Peak-to-peak ripple
```

## Filtering (Capacitor)
```
Capacitor holds peak, reduces ripple
Ripple voltage (approx): V_r = I/(f C)
   f = 2x line freq (full wave)
Ripple factor ~ 1/(4 sqrt(3) f R C) (full wave)
Larger C -> less ripple, larger peak current
```

## Clippers
- Clip (limit) portions of waveform
- Series/parallel diode configurations
- Zener clippers set clip levels
- Transfer characteristics piecewise

## Clampers
- Shift waveform DC level (not shape)
- Voltage level shifter
- Uses diode + capacitor
- Clamping to a reference level

## Voltage Doubler/Multiplier
- Capacitor + diode cascade
- Doubler: about 2 V_m
- Cascade to get higher multipliers
- Cockcroft-Walton for N-stage

## Zener Diode
- Operates in breakdown (reverse)
- Regulates voltage (constant V_z over wide current)
- Zener regulator: keeps V_out = V_z with series R
- Applications: voltage reference, regulator

## Applications
- Rectification (power supply front end)
- Detection/demodulation (envelope detection AM)
- Clipping/clamping (waveform shaping)
- Voltage regulation/reference
- Protection (flyback diodes, ESD clamps)

---

## ISRO Key Points
- Si cutin ~0.7V, Ge ~0.3V
- Bridge: PIV = Vm, center-tap: 2Vm
- Ripple factor: half 1.21, full 0.48
- Zener regulates in breakdown
- VT = 26 mV at 300K
- V_dc full-wave = 2Vm/pi
