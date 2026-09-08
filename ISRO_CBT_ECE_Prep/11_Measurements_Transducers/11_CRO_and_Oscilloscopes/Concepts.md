# CRO and Oscilloscopes - Concepts

## 1. CRO (Cathode Ray Oscilloscope)
Displays voltage waveforms as a function of time on a CRT screen.

## 2. CRT Construction
- Electron gun: Produces focused electron beam
- Deflection system: Y (vertical) and X (horizontal) plates
- Fluorescent screen: Converts electrons to visible light
- Vacuum envelope: Glass tube with phosphor coating

## 3. Vertical Deflection (Y-axis)
- Input signal applied to Y-deflection plates
- Vertical amplifier conditions the signal
- Sensitivity: V/div (volts per division)
- Controls: Volts/div, AC/DC/GND coupling

## 4. Horizontal Deflection (X-axis)
- Time base generator provides sawtooth/ramp waveform
- Sweep: Electron beam moves left to right at constant speed
- Retrace: Beam quickly returns to left
- Controls: Time/div, trigger

## 5. Time Base
- Sawtooth voltage drives X-deflection
- Frequency of sawtooth determines sweep rate
- Time/div setting controls how many divisions represent one time unit
- For display of periodic signals: sweep frequency = signal frequency / n

## 6. Triggering
Synchronizes sweep with input signal for stable display.
- Source: Line, external, or channel
- Slope: Positive or negative edge
- Level: Voltage threshold for trigger

## 7. Dual Trace (Dual Channel)
Two signals displayed simultaneously using two Y-channels.
- ALT (alternate): Switches between channels each sweep
- CHOP: Rapidly switches between channels during sweep
- Both channels share same time base

## 8. Sampling Oscilloscope
- For high-frequency signals beyond real-time bandwidth
- Takes samples from successive cycles of repetitive signal
- Reconstructs waveform from samples
- Equivalent-time sampling

## 9. Bandwidth
- Frequency range where amplitude response is within -3dB
- BW >= 3.5 × f_max for square wave display
- BW >= 3 × f_max for reasonable sine wave display
- Higher bandwidth = more expensive

## 10. Rise Time
```
t_r = 0.35 / BW
```
Ability to display fast-changing signals.

## 11. Lissajous Patterns
Formed when sinusoidal signals are applied to both X and Y plates.
Used for frequency and phase measurement.

### Frequency Measurement
```
f_y / f_x = (number of horizontal tangencies) / (number of vertical tangencies)
```

### Phase Measurement
- Line: 0 or 180 degrees
- Circle: 90 degrees
- Ellipse: intermediate phase
- Phase = arcsin(a/b) where a = minor axis, b = major axis intercept

## 12. CRO Specifications
| Parameter | Description |
|-----------|-------------|
| Bandwidth | -3dB frequency |
| Sensitivity | mV/div minimum |
| Time base | s/div to ns/div |
| Input impedance | 1 MOhm, 15-25 pF |
| Deflection factor | V/div |

## 13. Oscilloscope Types
- Analog CRO: Real-time display, limited bandwidth
- Digital Storage Oscilloscope (DSO): Digitizes and stores waveform
- Mixed Signal Oscilloscope (MSO): Analog + digital channels

## 14. ISRO Focus Areas
- Lissajous pattern frequency/phase measurement
- Bandwidth and rise time relationship
- Dual trace modes (ALT vs CHOP)
- Triggering principle
- Time base operation
