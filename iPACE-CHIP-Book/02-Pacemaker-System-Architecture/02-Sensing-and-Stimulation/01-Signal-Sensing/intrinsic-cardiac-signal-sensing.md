# Intrinsic Cardiac Signal Sensing

## 2.2.1 Intracardiac Electrogram Morphology and Sensing Circuit Design

The sensing subsystem is the most critical analog function in the pacemaker.
It must reliably detect cardiac depolarization signals (P-waves and R-waves)
that range from 0.1 mV to 30 mV in amplitude, while rejecting noise from
skeletal muscle myoelectrical activity (EMG), electrode polarization artifacts,
electromagnetic interference (EMI), far-field cardiac signals (T-waves), and
power-line interference. This chapter provides a comprehensive treatment of
intracardiac signal characteristics, sensing circuit design, and noise
rejection techniques.

---

## 2.5.1 Intracardiac Electrogram Characteristics

### Signal Sources

The intracardiac electrogram (EGM) is a recording of the electrical activity
of the heart as measured by electrodes in contact with the endocardial
surface. The EGM consists of three main components:

1. **P-wave**: Atrial depolarization signal, 0.2-3.0 mV amplitude,
   40-80 ms duration, frequency content 10-50 Hz.

2. **R-wave**: Ventricular depolarization signal, 0.5-30 mV amplitude,
   50-120 ms duration, frequency content 10-100 Hz.

3. **T-wave**: Ventricular repolarization signal, 0.1-5 mV amplitude,
   100-300 ms duration, frequency content 1-15 Hz.

### Typical Amplitude Ranges

| Signal | Atrial Channel | Ventricular Channel | Unit |
|--------|---------------|-------------------|------|
| P-wave amplitude | 0.2-3.0 | 0.1-1.0 | mV |
| R-wave amplitude | 0.5-5.0 (far-field) | 0.5-30 | mV |
| T-wave amplitude | 0.05-0.5 (far-field) | 0.1-5.0 | mV |
| Noise floor (EMG) | 0.01-0.1 | 0.01-0.1 | mV |
| Noise floor (EMI) | 0.001-0.05 | 0.001-0.05 | mV |
| Afterpotential (post-pace) | 10-100 | 10-100 | mV |

### Frequency Content

| Signal | Bandwidth | Dominant Frequency | Duration |
|--------|-----------|-------------------|----------|
| P-wave | 10-50 Hz | 20-30 Hz | 40-80 ms |
| R-wave | 10-100 Hz | 30-60 Hz | 50-120 ms |
| T-wave | 1-15 Hz | 3-8 Hz | 100-300 ms |
| EMG noise | 10-500 Hz | 50-200 Hz | Continuous |
| Power-line | 50/60 Hz | 50/60 Hz | Continuous |
| Afterpotential | 1-50 Hz | 5-20 Hz | 100-500 ms |

### Electrogram Morphology

The intracardiac EGM morphology depends on several factors:

1. **Electrode location**: Endocardial vs. epicardial, atrial vs.
   ventricular, septal vs. free wall.

2. **Electrode type**: Tip electrode (0.5-1.5 mm²), ring electrode
   (5-10 mm²), or coil electrode (50-100 mm²).

3. **Lead orientation**: The vector between tip and ring electrodes
   affects the signal amplitude and morphology.

4. **Cardiac pathology**: Ischemia, infarction, fibrosis, and
   hypertrophy alter the EGM morphology.

5. **Age and medications**: Beta-blockers, calcium channel blockers, and
   age-related changes affect heart rate and EGM morphology.

### Typical Ventricular EGM Waveform

```
        R-Wave
        ┌─┐
        │ │
   ─────┘ └────────────────────────────────── T-Wave
                                          ┌──────┐
                                          │      │
                                     ─────┘      └─────
   │←─── QRS Complex ───→│         │←── T-Wave ──→│
   │       50-120 ms     │         │   100-300 ms  │
   │                      │         │               │
   0.5-30 mV             │         0.1-5 mV        │
                          │                          │
                    Baseline Noise                   │
                    (EMG + EMI)                      │
                    0.01-0.1 mV                      │
                                                      │
   ◄──────────────── One Cardiac Cycle ──────────────►
                      600-1000 ms (60-100 bpm)
```

### Typical Atrial EGM Waveform

```
        P-Wave
        ┌─┐
        │ │
   ─────┘ └────────────────────────────────── Baseline
                                                    │
                                                    │
   │←── P-Wave ──→│                                 │
   │   40-80 ms   │                                 │
   │               │                                 │
   0.2-3.0 mV    │                                 │
                  │                                 │
            Far-field R-Wave (Atrial Channel)        │
            ┌─┐                                      │
            │ │                                      │
   ─────────┘ └─────────────────────────────────────┘
   │←─ 0.5-5 mV ─→│
   │    (rejected)  │
   │                │
   ◄──── One Atrial Cycle ────►
         600-1000 ms
```

---

## 2.5.2 Sensing Amplifier Design

### Low-Noise Amplifier (LNA) Topology

The sensing amplifier is the first stage in the signal chain and dominates
the overall noise performance. The design must achieve:

- Input-referred noise: < 5 µV RMS (10-100 Hz bandwidth)
- Input impedance: > 10 MΩ (to avoid loading the high-impedance electrode)
- CMRR: > 80 dB (to reject common-mode interference)
- PSRR: > 60 dB (to reject power supply noise)
- Gain: 20-800x (programmable)
- Bandwidth: 0.5-100 Hz (programmable)
- Power: < 1 µW

#### Chopper-Stabilized Amplifier

The chopper-stabilized amplifier is the preferred topology for pacemaker
sensing applications because it:

1. **Eliminates 1/f noise**: By modulating the input signal to a higher
   frequency before amplification, the 1/f noise of the input transistors
   is shifted out of the signal band.

2. **Reduces offset**: The chopping action modulates the offset voltage
   to the chopping frequency, where it can be filtered out.

3. **Provides high DC gain**: The chopper amplifier can achieve > 80 dB
   of DC gain with low offset and low noise.

```
                    CHOPPER-STABILIZED AMPLIFIER

  Input     ┌──────┐     ┌──────────┐     ┌──────┐     ┌──────────┐
  (Differential)    │     │          │     │      │     │          │
  ──────────┤ CHOP1 ├────▶│ GAIN     ├────▶│CHOP2 ├────▶│ LPF      ├──── Output
            │ (fCH) │     │ STAGE    │     │(fCH) │     │ (fc <<   │
  ──────────┤       │     │ (Av=20-  │     │      │     │  fCH)    │
            └──────┘     │  800x)   │     └──────┘     └──────────┘
                         └──────────┘

  fCH = Chopping frequency (1-10 kHz)
  fc  = Low-pass filter cutoff (100-500 Hz)
```

**Chopper frequency selection:**
- Must be >> signal bandwidth (100 Hz) to avoid aliasing
- Must be << switching speed limit of the amplifier
- Typically fCH = 1-10 kHz (10-100× signal bandwidth)
- Must be coprime with power-line frequency (50/60 Hz) to avoid
  intermodulation

**Chopper modulation/demodulation:**
- Input chopper modulates the differential input signal to fCH
- Amplifier amplifies the modulated signal
- Output chopper demodulates the amplified signal back to baseband
- Residual chopping artifacts are removed by the output LPF

**Noise performance:**
- Thermal noise: kT/C noise of the input sampling capacitors
- 1/f noise: Eliminated by chopping (reduced by > 40 dB)
- Chopper ripple: Residual offset at fCH, removed by LPF
- Total input-referred noise: < 5 µV RMS (10-100 Hz)

#### Fully Differential Amplifier

The fully differential topology provides:

- **Inherent common-mode rejection**: Differential signals are amplified,
  common-mode noise is rejected.
- **Reduced even-order distortion**: Differential operation cancels even-
  order harmonic distortion.
- **Better power supply rejection**: Differential signals are less
  susceptible to power supply noise.

### Gain Stage Design

The gain stage is implemented as a multi-stage amplifier with programmable
gain:

```
         ┌─────────────────────────────────────────────┐
         │              GAIN STAGE                      │
         │                                              │
  Input ─┤──▶ Pre-Amp ──▶ VGA ──▶ Post-Amp ──▶ Output │
  (Diff)  │   (Fixed)   (Variable)  (Fixed)           │
         │   (10x)      (2-80x)     (1-10x)           │
         │                                              │
         │   Total Gain: 20x to 8000x                  │
         │   (Programmable in 6 dB steps)              │
         │                                              │
         └─────────────────────────────────────────────┘
```

**Pre-amplifier:**
- Fixed gain of 10x (20 dB)
- Provides initial amplification to establish the noise floor
- Input-referred noise: < 3 µV RMS
- Bandwidth: > 1 kHz (to capture R-wave morphology)
- Power: < 0.5 µW

**Variable Gain Amplifier (VGA):**
- Gain range: 2x to 80x (6 dB to 38 dB)
- Gain step: 6 dB (2× per step, 8 discrete levels)
- Controlled by 3-bit gain register
- Power: < 0.5 µW

**Post-amplifier:**
- Fixed gain of 1x to 10x (0-20 dB)
- Provides final gain adjustment and drives the filter input
- Power: < 0.3 µW

### Input Impedance

The input impedance must be > 10 MΩ to avoid loading the electrode
(typically 300-1500 Ω for a chronic lead). The input impedance is
dominated by:

1. **Bias resistors**: The DC bias resistors set the input common-mode
   voltage. These must be > 100 MΩ to avoid loading.

2. **ESD protection diodes**: The reverse-biased ESD diodes contribute
   leakage current that limits the effective input impedance.

3. **Gate leakage**: At 130 nm and below, gate leakage through the input
   transistors can limit the input impedance. Use thick-oxide input
   transistors or cascode configurations to mitigate.

---

## 2.5.3 Bandpass Filter Design

### Filter Specifications

The bandpass filter shapes the frequency response to optimize detection of
the target cardiac signal while rejecting noise and interference.

| Parameter | Atrial Channel | Ventricular Channel | Unit |
|-----------|---------------|-------------------|------|
| High-pass corner (fHP) | 0.5-2.0 | 0.5-2.0 | Hz |
| Low-pass corner (fLP) | 30-80 | 50-100 | Hz |
| Passband ripple | < 0.5 | < 0.5 | dB |
| Stopband attenuation | > 40 | > 40 | dB @ 2× fLP |
| Filter order | 4-6 | 4-6 | — |
| Group delay variation | < 10 | < 10 | ms (0.5-0.8× fLP) |

### Filter Topology

The filter is implemented as an active-RC biquad cascade, with each biquad
stage providing a second-order transfer function:

```
Transfer Function (2nd-order BPF):

H(s) = (s × BW) / (s² + s × BW + ω₀²)

where:
  ω₀ = center frequency = 2π × √(fHP × fLP)
  BW = bandwidth = 2π × (fLP - fHP)
  Q = quality factor = ω₀ / BW
```

For a 4th-order bandpass filter, two biquad stages are cascaded:

```
H(s) = H1(s) × H2(s)

where:
  H1(s) = (s × BW1) / (s² + s × BW1 + ω₀₁²)
  H2(s) = (s × BW2) / (s² + s × BW2 + ω₀₂²)
```

### Programmable Corner Frequencies

The filter corner frequencies are programmed via switched capacitor arrays:

```
fHP = 1 / (2π × RHP × CHP)
fLP = 1 / (2π × RLP × CLP)

where:
  RHP, RLP = Programmable resistor arrays (switched)
  CHP, CLP = Programmable capacitor arrays (switched)
```

**Component values:**
- RHP: 10 MΩ to 100 MΩ (programmable in 16 steps)
- CHP: 10 pF to 100 pF (programmable in 8 steps)
- RLP: 1 MΩ to 10 MΩ (programmable in 16 steps)
- CLP: 100 pF to 1 nF (programmable in 8 steps)

### Notch Filter (50/60 Hz Rejection)

An optional notch filter can be included to reject power-line interference:

```
Notch Transfer Function:

H_notch(s) = (s² + ω₀²) / (s² + (ω₀/Q) × s + ω₀²)

where:
  ω₀ = 2π × 50 Hz or 2π × 60 Hz
  Q = 5-20 (adjustable)
```

The notch filter is implemented as a twin-T network with programmable Q:

```
                    ┌────────┐
                    │  Notch │
  Input ──────┬────┤  Filter├────┬──── Output
              │    │  (Twin-T)   │
              │    └────────┘    │
              │                  │
              └──── R ──── R ────┘
                     │
                     C
                     │
                    GND

  Notch frequency: f₀ = 1/(2π × R × C)
  Q factor: Adjusted via feedback network
```

### Filter Implementation Details

| Component | Type | Value Range | Control | Accuracy |
|-----------|------|------------|---------|----------|
| RHP | Poly resistor | 10-100 MΩ | 4-bit switch | ±5% |
| CHP | MIM capacitor | 10-100 pF | 3-bit switch | ±2% |
| RLP | Poly resistor | 1-10 MΩ | 4-bit switch | ±5% |
| CLP | MIM capacitor | 100p-1nF | 3-bit switch | ±2% |
| Op-amp | OTA | GBW > 10 kHz | Bias current | — |
| Switch | NMOS/PMOS | Ron < 10 kΩ | Digital control | — |

---

## 2.5.4 Threshold Detection and Auto-Adjustment

### Adaptive Threshold Algorithm

The adaptive threshold algorithm adjusts the detection threshold based on
the measured signal amplitude, providing optimal sensitivity across the
wide range of intracardiac signal amplitudes encountered in clinical
practice.

```
                    ADAPTIVE THRESHOLD ALGORITHM

  ┌──────────────────────────────────────────────────────────────┐
  │                                                              │
  │  1. Measure peak amplitude of detected event                 │
  │     Peak[n] = max(|V_filtered[t]|) for t in detection window│
  │                                                              │
  │  2. Update running average of peak amplitudes                │
  │     AvgPeak = (1/N) × Σ Peak[i], i = 1..N                   │
  │     N = averaging window (4-8 events, programmable)          │
  │                                                              │
  │  3. Set detection threshold                                  │
  │     Threshold = K × AvgPeak                                 │
  │     K = sensitivity factor (0.25-0.75, programmable)         │
  │                                                              │
  │  4. Apply minimum threshold                                  │
  │     Threshold = max(Threshold, Threshold_min)                │
  │     Threshold_min = 0.1 mV (programmable)                    │
  │                                                              │
  │  5. Apply maximum threshold                                  │
  │     Threshold = min(Threshold, Threshold_max)                │
  │     Threshold_max = 5.0 mV (programmable)                    │
  │                                                              │
  └──────────────────────────────────────────────────────────────┘
```

### Threshold Parameters

| Parameter | Symbol | Range | Default | Unit |
|-----------|--------|-------|---------|------|
| Sensitivity factor | K | 0.25-0.75 | 0.50 | — |
| Averaging window | N | 4-8 | 6 | events |
| Minimum threshold | Th_min | 0.1-1.0 | 0.1 | mV |
| Maximum threshold | Th_max | 1.0-5.0 | 5.0 | mV |
| Decay factor | D | 0.8-1.0 | 0.9 | — |
| Noise threshold | Th_noise | 0.01-0.1 | 0.05 | mV |

### Threshold Decay

When no events are detected for an extended period, the threshold decays
toward the minimum threshold to maintain sensitivity:

```
Threshold[n] = Threshold[n-1] × D

where:
  D = decay factor (0.8-1.0)
  Decay occurs when no event detected for > 3 × lower rate interval
```

---

## 2.5.5 Blank Periods and Refractory Periods

### Absolute Refractory Period (ARP)

During the absolute refractory period, the sensing amplifier is completely
blanked (input disconnected or threshold set to maximum). No events can be
detected during this period.

**Purpose:**
- Prevents oversensing of the pacing artifact (post-pace blanking)
- Prevents oversensing of the R-wave tail (post-sense blanking)
- Prevents cross-channel crosstalk

**Duration:**
- Post-pace ARP: 200-500 ms (programmable)
- Post-sense ARP: 200-350 ms (programmable)
- Cross-channel ARP: 10-50 ms (programmable)

### Relative Refractory Period (RRP)

During the relative refractory period, the sensing amplifier is active but
events are classified differently:

- Events during the RRP are marked as "refractory" events
- Refractory events do not reset the timing cycle
- Refractory events are used for diagnostic counting only
- Exception: High-amplitude events during RRP may be classified as
  premature beats (PVC detection)

**Duration:**
- Post-sense RRP: 300-500 ms (programmable)
- Post-pace RRP: 300-500 ms (programmable)

### Blanking Period Timing Diagram

```
  Pacing/Sensing Event
  │
  ▼
  ┌──────────────────────┬─────────────────────┬──────────────────────┐
  │  ABSOLUTE            │  RELATIVE            │  SENSING             │
  │  REFRACTORY          │  REFRACTORY          │  ACTIVE              │
  │  PERIOD (ARP)        │  PERIOD (RRP)        │  PERIOD              │
  │                      │                      │                      │
  │  • Amp blanked       │  • Amp active        │  • Amp active        │
  │  • Threshold = max   │  • Threshold = max   │  • Threshold = adapt │
  │  • No detection      │  • Events marked     │  • Full detection    │
  │  • Duration: 200ms   │  • Duration: 300ms   │  • Duration: until   │
  │                      │                      │    next event        │
  └──────────────────────┴─────────────────────┴──────────────────────┘
  │←───── ARP ─────→│←──── RRP ─────→│←──── Active Sensing ────→│
  │      200 ms      │     300 ms      │      until next event     │

  Total blanking = ARP + RRP = 500 ms (typical)
```

---

## 2.5.6 T-Wave Discrimination

T-wave oversensing is a common clinical problem that can lead to inappropriate
inhibition of pacing. Several techniques are used to discriminate T-waves
from R-waves:

### Technique 1: Frequency Discrimination

T-waves have lower frequency content (1-15 Hz) than R-waves (10-100 Hz).
By applying a high-pass filter with a corner frequency of 15-20 Hz, T-waves
can be significantly attenuated relative to R-waves.

```
  Filter Response:
  
  Gain (dB)
    0 ─────────────┐
                   │
  -10 ─────────────┤
                   │
  -20 ─────────────┘
                   │
  -40 ──────────────────────────
                   │
  -60 ──────────────────────────
         │← R-Wave →│← T-Wave →│
         10-100 Hz    1-15 Hz
```

### Technique 2: Duration Discrimination

T-waves have longer duration (100-300 ms) than R-waves (50-120 ms). By
measuring the duration of the detected event and rejecting events longer
than a programmable threshold, T-waves can be discriminated.

```
  Duration measurement:
  
  If (event_duration > Duration_threshold) then
      classify as T-wave (reject)
  else
      classify as R-wave (accept)
  
  Duration_threshold = 150-250 ms (programmable)
```

### Technique 3: Amplitude Discrimination

T-waves typically have lower amplitude than R-waves. By setting the
detection threshold above the expected T-wave amplitude, T-wave oversensing
can be prevented.

```
  Amplitude discrimination:
  
  R-wave amplitude: 0.5-30 mV
  T-wave amplitude: 0.1-5 mV
  
  If (Threshold > T-wave_amplitude) then T-wave rejected
```

### Technique 4: Timing Discrimination

T-waves occur after the R-wave with a consistent delay (the R-T interval,
typically 200-400 ms). By implementing a blanking period after each detected
R-wave that covers the expected T-wave timing, T-wave oversensing can be
prevented.

```
  Timing blanking:
  
  After R-wave detected:
      Start T-wave blanking timer (200-400 ms)
      During blanking: no events detected
      After blanking: normal sensing resumed
```

### Technique 5: Morphology Discrimination

Advanced pacemakers use template matching to discriminate R-waves from
T-waves based on their morphology:

```
  Morphology analysis:
  
  1. Capture detected event waveform
  2. Cross-correlate with stored R-wave template
  3. If correlation > threshold (e.g., 0.8) → classify as R-wave
  4. If correlation < threshold → classify as T-wave or noise
```

---

## 2.5.7 Far-Field R-Wave Rejection (Atrial Channel)

The atrial sensing channel must reject far-field R-waves (ventricular
depolarization signals that are conducted to the atrial electrodes). This
is particularly challenging because the far-field R-wave amplitude can be
0.5-5.0 mV, which is comparable to the P-wave amplitude.

### Rejection Techniques

1. **Amplitude discrimination**: Set the atrial threshold above the
   far-field R-wave amplitude (may reduce P-wave sensitivity).

2. **Timing blanking**: Blank the atrial channel during and after ventricular
   events (PVAB: post-ventricular atrial blanking).

3. **Morphology discrimination**: Use template matching to distinguish
   P-waves from far-field R-waves based on waveform shape.

4. **Dual sensing vectors**: Use two sensing vectors (tip-ring and
   tip-can) and select the vector with the best P-wave-to-R-wave ratio.

5. **Digital signal processing**: Apply adaptive filtering or wavelet
   transforms to separate P-waves from far-field R-waves.

### PVAB (Post-Ventricular Atrial Blanking)

PVAB is the primary mechanism for far-field R-wave rejection in dual-chamber
pacemakers:

```
  Ventricular Event (Sensed or Paced)
  │
  ▼
  ┌──────────────────────┬──────────────────────┐
  │  PVAB               │  Atrial Sensing      │
  │  (Atrial blanked)   │  Re-enabled          │
  │                      │                      │
  │  Duration: 50-400 ms │                      │
  │  (programmable)      │                      │
  └──────────────────────┴──────────────────────┘
  │←────── PVAB ───────→│←── Active Atrial ──→│
```

---

## 2.5.8 Noise Detection and Rejection

### EMG Noise

Skeletal muscle myoelectrical activity (EMG) produces broadband noise
(10-500 Hz) that can interfere with cardiac signal detection. Rejection
techniques include:

1. **Bandpass filtering**: The low-pass filter (fLP = 50-100 Hz) attenuates
   high-frequency EMG components.

2. **Auto-adjusting threshold**: The adaptive threshold algorithm raises
   the detection threshold in the presence of elevated noise levels.

3. **Noise detection algorithm**: Monitors the signal statistics (variance,
   zero-crossing rate) to detect the presence of EMG noise and adjusts
   sensing parameters accordingly.

### EMI Rejection

Electromagnetic interference from external sources (power lines, cellular
phones, MRI) can couple to the sensing electrodes. Rejection techniques
include:

1. **Common-mode rejection**: The differential input stage rejects
   common-mode EMI (> 80 dB CMRR).

2. **Notch filtering**: A 50/60 Hz notch filter rejects power-line
   interference.

3. **Input filtering**: The bandpass filter attenuates out-of-band EMI.

4. **Blanking**: During high-amplitude EMI events (e.g., electrocautery),
   the sensing amplifier is blanked to prevent inappropriate detection.

5. **WIEG (Wideband Interference Elimination Generator)**: Some pacemakers
   implement an active noise cancellation circuit that generates an
   anti-phase signal to cancel detected EMI.

### Afterpotential Rejection

After a pacing pulse, the electrode-tissue interface generates a large
voltage artifact (afterpotential) that can persist for 100-500 ms. This
artifact must be rejected to allow sensing of the evoked response.

**Rejection techniques:**
1. **Post-pace blanking**: Blank the sensing amplifier for 200-500 ms
   after each pacing pulse.
2. **High-pass filtering**: A high-pass filter with fHP = 10-20 Hz can
   attenuate the low-frequency afterpotential.
3. **Active discharge**: A low-impedance discharge circuit across the
   electrode rapidly dissipates the afterpotential.

---

## 2.5.9 Sensitivity Specifications Summary

| Parameter | Atrial Channel | Ventricular Channel | Unit |
|-----------|---------------|-------------------|------|
| Sensitivity range | 0.1-5.0 | 0.1-5.0 | mV |
| Sensitivity resolution | 0.1 | 0.1 | mV |
| Input-referred noise | ≤ 3 | ≤ 5 | µV RMS |
| Bandwidth (low-pass) | 30-80 | 50-100 | Hz |
| Bandwidth (high-pass) | 0.5-2.0 | 0.5-2.0 | Hz |
| CMRR | ≥ 80 | ≥ 80 | dB |
| PSRR | ≥ 60 | ≥ 60 | dB |
| Input impedance | ≥ 10 | ≥ 10 | MΩ |
| Overload recovery | ≤ 200 | ≤ 200 | µs |
| Sensing specificity | ≥ 99.5 | ≥ 99.5 | % |
| Sensitivity (detection) | ≥ 99.9 | ≥ 99.9 | % |
| T-wave rejection | ≥ 10:1 | ≥ 10:1 | (T/R) |
| Far-field R rejection | ≥ 5:1 | N/A | (P/Rff) |
| EMG rejection | ≥ 20 | ≥ 20 | dB |

---

## 2.5.10 Summary

Intrinsic cardiac signal sensing is a critical function in the pacemaker
that requires careful optimization of:

1. **Noise performance**: Input-referred noise < 5 µV RMS to detect small
   P-waves and R-waves.
2. **Selectivity**: Bandpass filtering and threshold adaptation to discriminate
   cardiac signals from noise and interference.
3. **Rejection**: Blank periods, refractory periods, and discrimination
   algorithms to reject T-waves, far-field signals, and artifacts.
4. **Adaptability**: Auto-adjusting sensitivity to handle the wide range of
   signal amplitudes encountered in clinical practice.
5. **Reliability**: > 99.9% detection sensitivity with > 99.5% specificity
   across all patient populations.

The chopper-stabilized amplifier topology provides the best combination of
low noise, low offset, and high CMRR for pacemaker sensing applications.
The adaptive threshold algorithm and blank period management ensure reliable
sensing across the full range of clinical conditions.
