# Data Acquisition - Concepts

## 1. Data Acquisition System (DAQ)
Process of collecting and converting real-world analog signals into digital data for processing, analysis, and storage.

## 2. System Components
Sensor/Transducer -> Signal Conditioning -> ADC -> Processor/Computer

## 3. Sample and Hold (S/H)
- Captures analog voltage at specific instant
- Holds it constant during ADC conversion
- Essential for signals that change during conversion
- Track mode: follows input; Hold mode: freezes value

### 3.1 Aperture Time
Time to switch from track to hold. Must be much smaller than signal period.

### 3.2 Hold Step
Voltage change during hold due to charge injection. Ideally zero.

### 3.3 Droop Rate
Rate at which held voltage decays due to capacitor leakage.

## 4. Multiplexed ADC Systems
- Multiple analog channels share single ADC
- Multiplexer (MUX) switches between channels sequentially
- Reduces cost (one ADC for many channels)
- Channel scanning rate = ADC rate / number of channels

## 5. Anti-Aliasing Filter
- Low-pass filter applied BEFORE sampling
- Removes frequencies above Nyquist frequency (fs/2)
- Prevents aliasing (false low-frequency components)
- Typically Butterworth or Bessel filter
- Order: Higher order = sharper cutoff

## 6. Sampling
### 6.1 Nyquist Theorem
```
fs >= 2 * fmax
```
Minimum sampling rate must be at least twice the highest signal frequency.

### 6.2 Aliasing
If fs < 2*fmax, high-frequency components appear as false low-frequency signals.
Cannot be removed after sampling.

### 6.3 Practical Sampling Rate
- Nyquist: fs = 2*fmax (theoretical minimum)
- Practical: fs = 5-10*fmax (for good reconstruction)
- Oversampling: fs >> 2*fmax (improves SNR)

## 7. Quantization
- Continuous amplitude mapped to discrete levels
- Number of levels = 2^n (n = ADC resolution)
- Quantization error = +/- 1/2 LSB
- Quantization noise decreases with more bits

### 7.1 Quantization Noise
```
SNR = 6.02n + 1.76 dB (for full-scale sinusoid)
```

## 8. DAQ Cards
- Complete data acquisition module
- Components: MUX, S/H, ADC, timing, digital I/O
- Interfaces: PCI, USB, Ethernet, PXI
- Specifications: resolution, sampling rate, number of channels

## 9. Sampling Rate Selection
```
For good reconstruction: fs >= 10 * fmax
For Nyquist compliance: fs >= 2 * fmax
With oversampling: SNR improvement = 3 dB per doubling of fs
```

## 10. Signal Conditioning
- Amplification: Boost weak signals to ADC range
- Filtering: Remove noise, anti-aliasing
- Isolation: Protect ADC from high voltages
- Excitation: For bridges, RTDs
- Linearization: Correct non-linear sensor output

## 11. ADC Selection for DAQ
| Type | Resolution | Speed | Application |
|------|-----------|-------|-------------|
| Dual Slope | 16-24 bit | Slow | Precision, DMM |
| SAR | 8-18 bit | Medium | General DAQ |
| Sigma-Delta | 16-24 bit | Slow-Medium | Audio, precision |
| Flash | 6-10 bit | Very fast | Oscilloscope |

## 12. ISRO Focus Areas
- Nyquist theorem application
- Anti-aliasing filter necessity
- Quantization noise formula
- Sample and hold operation
- DAQ system block diagram
