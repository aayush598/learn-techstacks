# CRO and Oscilloscopes - Formulas

## 1. Bandwidth and Rise Time
```
t_r = 0.35 / BW

where:
t_r = rise time (seconds)
BW = bandwidth (Hz)
```

## 2. Lissajous Frequency Measurement
```
f_y / f_x = N_h / N_v

where:
N_h = number of horizontal tangencies (touching vertical line)
N_v = number of vertical tangencies (touching horizontal line)
```

## 3. Lissajous Phase Measurement
```
Phase angle phi = arcsin(a/b)

where:
a = distance from center to ellipse intersection with horizontal axis
b = horizontal span of ellipse at same Y-level

For circle: phi = 90 degrees
For line: phi = 0 or 180 degrees
```

## 4. Vertical Deflection
```
Y = (V_in × L × d) / (2 × d_v × V_a)

where:
L = length of deflection plates
d = distance between plates
d_v = distance from plates to screen
V_a = accelerating voltage
V_in = input signal voltage
```

## 5. Time Base
```
Sweep time = Time/div × number of divisions

For display of one complete cycle:
Sweep frequency = signal frequency / n
where n = number of cycles displayed
```

## 6. Deflection Sensitivity
```
Vertical: S_y = Y / V_in  (div/V or mm/V)
Horizontal: S_x = X / V_x  (div/V)

Gain = S × amplifier gain
```

## 7. Accelerating Voltage
```
eV_a = (1/2)mv^2
v = sqrt(2eV_a/m)

Higher V_a -> brighter spot, faster electron velocity
```

## 8. Sweep Speed
```
v_sweep = screen_width / sweep_time

For 10 divisions, 1 ms/div:
v_sweep = 10 div / 1 ms = 10,000 div/s
```

## 9. Bandwidth Requirement for Square Wave
```
BW_min = 0.35 / t_r( of square wave)

For good square wave display:
BW >= 3.5 × fundamental frequency
BW >= 5 × fundamental for excellent quality
```

## 10. Sampling Rate (DSO)
```
Nyquist: f_s >= 2 × f_max

For accurate waveform: f_s >= 10 × f_max (rule of thumb)
Sampling interval: T_s = 1/f_s
```

## 11. DSO Record Length
```
Record = Sampling_rate × Acquisition_time
Points = f_s × (Time/div × 10)
```

## 12. Probe Compensation
```
For 10x probe:
R_probe × C_probe = R_input × C_input

Compensation capacitor adjusted until square wave
appears flat (no overshoot or rounding)
```

## 13. Trigger Holdoff
```
Minimum time between triggers
Prevents retriggering during retrace
Holdoff >= retrace time
```

## 14. Storage Bandwidth (Sampling)
```
Equivalent-time sampling BW = 1/(2 × T_sample)

For real-time BW limited scope:
Equivalent BW can be much higher with sequential sampling
```

## Key Formulas for ISRO MCQs
| Quantity | Formula |
|----------|---------|
| Rise time | t_r = 0.35/BW |
| Freq (Lissajous) | fy/fx = Nh/Nv |
| Phase | phi = arcsin(a/b) |
| Nyquist | fs >= 2*fmax |
| BW for square wave | BW >= 3.5*f |
| Sweep time | Time/div x 10 div |
