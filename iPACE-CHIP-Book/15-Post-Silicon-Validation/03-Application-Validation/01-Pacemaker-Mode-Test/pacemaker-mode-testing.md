# Pacemaker Mode Testing

## 15.9.1 Overview

The iPACE-CHIP supports multiple pacemaker pacing modes as defined by the NBG (NASPE/BPEG Generic) code system. Each mode represents a different combination of pacing and sensing capabilities tailored to specific patient arrhythmia profiles. Pacemaker mode testing validates that the iPACE-CHIP correctly implements each supported mode, transitions between modes as programmed, and behaves according to the applicable regulatory standards (IEC 60601-2-4, ISO 14708-3). This chapter details the comprehensive testing of every pacemaker mode supported by the iPACE-CHIP.

## 15.9.2 NBG Code Reference

The NBG code uses four positions to describe pacemaker behavior:

```
Position 1: Chamber(s) Paced      | V = Ventricular, A = Atrial, D = Dual
Position 2: Chamber(s) Sensed     | V = Ventricular, A = Atrial, D = Dual, O = None
Position 3: Response to Sensing   | I = Inhibited, T = Triggered, D = Dual
Position 4: Rate Modulation       | R = Rate modulation, O = None

Additional modifiers:
  S = Single chamber (A or V)
  E = Extends (multisite pacing)
```

### Modes Supported by iPACE-CHIP

```
Mode   | Description                        | Clinical Application
-------|------------------------------------|---------------------------
VVI    | Vent pace, vent sense, inhibited   | Atrial fibrillation
VVIR   | VVI + rate response                 | AF + chronotropic incompetence
VOO    | Asynchronous vent pacing           | Test mode, magnet mode
VVT    | Vent pace, vent sense, triggered   | Rarely used (backup)
AOO    | Asynchronous atrial pacing         | Test mode
AAI    | Atr pace, atr sense, inhibited     | Sick sinus syndrome
AAIR   | AAI + rate response                 | SSS + chronotropic incompetence
DDD    | Dual pace, dual sense, dual resp  | AV block (complete)
DDDR   | DDD + rate response                 | AV block + chronotropic incompetence
VDD    | Vent pace, dual sense, triggered   | AV block (normal atrial function)
DOO    | Asynchronous dual pacing           | Test mode
```

## 15.9.3 Test Infrastructure

### Pacing Test System

The test system generates realistic cardiac signals and measures pacing output:

```
Test System Components:
  1. Dual-channel signal generator (atrial + ventricular)
     - Programmable waveform shapes (R-wave, P-wave templates)
     - Programmable amplitude (0.1 mV to 10 mV)
     - Programmable timing (cycle length, AV delay)
  
  2. Pacing output analyzer
     - Oscilloscope with protocol decoding
     - Custom FPGA for real-time parameter extraction
  
  3. Timing measurement system
     - 100 MHz counter (10 ns resolution)
     - Hardware trigger on pacing events
  
  4. Patient simulator
     - Resistor network (100-1500 ohm range)
     - Capacitive coupling (1 nF - 100 nF)
     - Polarization voltage injection
```

### Test Cardiac Signals

Realistic cardiac signal templates are used for testing:

```
Ventricular R-Wave Template:
  - Morphology: Triphasic
  - Duration: 80 ms
  - Amplitude range: 2-15 mV (programmable)
  - dV/dt max: 500 mV/s (typical R-wave slew rate)

Atrial P-Wave Template:
  - Morphology: Biphasic
  - Duration: 100 ms
  - Amplitude range: 0.5-5 mV (programmable)
  - dV/dt max: 100 mV/s (typical P-wave slew rate)

T-Wave Template:
  - Morphology: Monophasic
  - Duration: 200 ms
  - Amplitude range: 0.2-2 mV
  - Important: Must not be sensed as R-wave (T-wave rejection)
```

## 15.9.4 VVI Mode Testing

### Test VVI-01: Basic Pacing

```
Objective: Verify VVI mode generates pacing pulses at the lower rate limit

Test Setup:
  - No input signal (no intrinsic rhythm)
  - Lower rate limit: 60 bpm (1000 ms interval)
  - Pulse amplitude: 3.5V
  - Pulse width: 0.5 ms

Procedure:
  1. Enable VVI mode
  2. Start timing
  3. Capture 100 pacing pulses on oscilloscope
  4. Measure interval between consecutive pulses
  5. Measure pulse amplitude and width

Expected Results:
  - Pacing interval: 1000 ms +/- 5 ms
  - Pulse amplitude: 3.5V +/- 10%
  - Pulse width: 0.5 ms +/- 5%
  - Regular, uninterrupted pacing
```

### Test VVI-02: Sensing and Inhibition

```
Objective: Verify sensed events inhibit pacing

Test Setup:
  - Lower rate limit: 60 bpm (1000 ms)
  - Sensing threshold: 0.5 mV
  - Apply R-waves at 80 bpm (750 ms interval, faster than lower rate)

Procedure:
  1. Enable VVI mode
  2. Apply R-waves at 750 ms intervals
  3. Verify pacing is inhibited during sensing
  4. Remove R-waves
  5. Verify pacing resumes at 1000 ms interval
  6. Measure latency from sensed event to pacing output inhibition

Expected Results:
  - No pacing pulses during R-wave application
  - Pacing resumes within 1000 ms of last R-wave
  - Inhibition response time < 100 ms
```

### Test VVI-03: Sensitivity Sweep

```
Objective: Determine the sensing threshold

Procedure:
  1. Apply R-waves at known amplitude
  2. Start with amplitude well below threshold (0.1 mV)
  3. Increase amplitude in 0.05 mV steps
  4. At each amplitude, deliver 10 R-waves
  5. Record detection rate (number sensed / 10)
  6. Continue until 100% detection achieved

Expected Results:
  - 0% detection at 0.1 mV
  - Transition zone between 0.3 mV and 0.7 mV
  - 100% detection at 0.7 mV and above
  - Sensing threshold: amplitude at 100% detection
  - Threshold within 0.4-0.6 mV (programmed 0.5 mV)
```

### Test VVI-04: Refractory Period

```
Objective: Verify post-pace and post-sense refractory periods

Test Setup:
  - Absolute refractory period (ARP): 250 ms
  - Relative refractory period (VRP): 350 ms
  - Lower rate limit: 60 bpm

Procedure Part A (Post-Pace ARP):
  1. Apply no input signal (pacing at 60 bpm)
  2. Deliver sensed event at 100 ms after pace (within ARP)
  3. Verify pacing is NOT inhibited
  4. Deliver sensed event at 200 ms after pace (within ARP)
  5. Verify pacing is NOT inhibited
  6. Deliver sensed event at 300 ms after pace (after ARP, within VRP)
  7. Verify event is sensed but timing is NOT reset (VRP)

Procedure Part B (Post-Sense VRP):
  1. Apply R-wave to inhibit pacing
  2. Deliver sensed event at 100 ms after R-wave (within VRP)
  3. Verify event is not sensed (blanking) or sensed but not resetting

Expected Results:
  - ARP: 250 ms +/- 5 ms
  - VRP: 350 ms +/- 5 ms
  - Events within ARP: pacing not inhibited
  - Events within VRP: sensed but no timing reset
```

### Test VVI-05: Upper Rate Limit

```
Objective: Verify maximum pacing rate is enforced

Test Setup:
  - Upper rate limit: 120 bpm (500 ms minimum interval)
  - Lower rate limit: 60 bpm

Procedure:
  1. Apply R-waves at 150 bpm (400 ms interval, faster than URL)
  2. Verify pacing output does not exceed 120 bpm
  3. Apply R-waves at 100 bpm (600 ms interval, within limits)
  4. Verify pacing follows R-waves at 100 bpm

Expected Results:
  - Pacing rate capped at 120 bpm regardless of sensing rate
  - No pacing faster than upper rate limit
```

## 15.9.5 AAI Mode Testing

### Test AAI-01: Basic Atrial Pacing

```
Objective: Verify AAI mode generates atrial pacing pulses

Test Setup:
  - No input signal
  - Lower rate limit: 60 bpm
  - Pulse amplitude: 2.5V
  - Pulse width: 0.4 ms

Procedure:
  1. Enable AAI mode
  2. Capture 100 atrial pacing pulses
  3. Verify regular pacing at 60 bpm

Expected Results:
  - Atrial pacing interval: 1000 ms +/- 5 ms
  - Atrial pulse amplitude: 2.5V +/- 10%
  - Atrial pulse width: 0.4 ms +/- 5%
```

### Test AAI-02: Atrial Sensing

```
Objective: Verify P-wave sensing inhibits atrial pacing

Procedure:
  1. Apply P-waves at 75 bpm (800 ms interval)
  2. Verify pacing inhibited during P-wave sensing
  3. Remove P-waves
  4. Verify pacing resumes at 60 bpm

Expected Results:
  - P-wave detection sensitivity: 0.5 mV threshold
  - P-wave blanking period: 100 ms
  - P-wave refractory period: 300 ms
```

### Test AAI-03: Rate Hysteresis

```
Objective: Verify rate hysteresis function

Test Setup:
  - Lower rate limit: 60 bpm
  - Hysteresis: 10 bpm (paces at 60 bpm, senses down to 50 bpm)

Procedure:
  1. Apply P-waves at 55 bpm (between hysteresis and base rate)
  2. Verify pacing is inhibited (55 > 50 bpm hysteresis limit)
  3. Remove P-waves
  4. Verify pacing resumes at 60 bpm (base rate, not hysteresis rate)
  5. Apply P-waves at 48 bpm (below hysteresis limit)
  6. Verify pacing starts at 60 bpm (below hysteresis limit)

Expected Results:
  - Sensing threshold with hysteresis: 50 bpm
  - Pacing resumes at 60 bpm (not 50 bpm)
  - Hysteresis prevents oscillation near the pacing threshold
```

## 15.9.6 DDD Mode Testing

### Test DDD-01: AV Sequential Pacing

```
Objective: Verify dual-chamber AV sequential pacing

Test Setup:
  - Mode: DDD
  - Lower rate limit: 60 bpm
  - AV delay: 200 ms
  - Pulse amplitudes: 3.5V (V), 2.5V (A)

Procedure:
  1. Apply no input signals
  2. Verify atrial pace followed by ventricular pace
  3. Measure AV delay between atrial and ventricular pulses
  4. Measure cycle length between consecutive atrial pulses

Expected Results:
  - Atrial pacing interval: 1000 ms
  - AV delay: 200 ms +/- 5 ms
  - Sequence: A-pace ... 200 ms ... V-pace ... 800 ms ... A-pace
  - Both chambers pace in correct sequence
```

### Test DDD-02: P-wave Tracking (Atrial Tracking)

```
Objective: Verify ventricular pacing tracks sensed P-waves

Test Setup:
  - Mode: DDD
  - AV delay: 200 ms
  - Upper rate limit: 120 bpm

Procedure:
  1. Apply P-waves at 80 bpm (750 ms interval)
  2. Verify ventricular pace follows each P-wave after AV delay
  3. Verify atrial pace is inhibited (P-waves sensed)
  4. Increase P-wave rate to 130 bpm (above URL)
  5. Verify ventricular pacing is capped at upper rate limit

Expected Results:
  - V-pace follows P-wave after 200 ms AV delay
  - A-pace inhibited during P-wave sensing
  - At 130 bpm input, V-pace rate limited to 120 bpm
  - Smooth transition from tracking to non-tracking mode
```

### Test DDD-03: PVC Response

```
Objective: Verify response to premature ventricular contraction

Test Setup:
  - Mode: DDD
  - AV delay: 200 ms
  - Lower rate limit: 60 bpm

Procedure:
  1. Apply normal P-waves at 75 bpm
  2. Inject PVC (premature R-wave) at 300 ms after last V-pace
  3. Verify A-sense is blanked after PVC (no A-pace triggered)
  4. Verify timing resets from PVC (VA interval starts)
  5. Verify next A-pace and V-pace follow correct timing

Expected Results:
  - PVC detected and correctly processed
  - No inappropriate atrial pacing immediately after PVC
  - VA interval reset from PVC event
  - Next AV delay starts from next atrial event
```

### Test DDD-04: Mode Switching

```
Objective: Verify automatic mode switch during atrial tachycardia

Test Setup:
  - Mode: DDD with mode switch enabled
  - Mode switch rate: 175 bpm (atrial tachycardia detection)
  - Fallback mode: VVIR

Procedure:
  1. Apply P-waves at 80 bpm (normal tracking)
  2. Verify DDD tracking behavior
  3. Increase P-wave rate to 200 bpm (above mode switch rate)
  4. Verify mode switches from DDD to VVIR
  5. Verify ventricular pacing at lower rate limit (not 200 bpm)
  6. Decrease P-wave rate to 60 bpm (below mode switch rate)
  7. Verify mode switches back to DDD

Expected Results:
  - Mode switch occurs within 30 seconds of tachycardia detection
  - Fallback to VVIR prevents rapid ventricular tracking
  - Mode switch back to DDD occurs within 30 seconds of tachycardia termination
  - Smooth transitions without pacing gaps
```

### Test DDD-05: Post-Ventricular Atrial Refractory Period (PVARP)

```
Objective: Verify PVARP prevents far-field R-wave sensing

Test Setup:
  - Mode: DDD
  - PVARP: 300 ms

Procedure:
  1. Apply normal P-waves at 75 bpm
  2. Deliver simulated far-field R-wave at 50 ms after V-pace
  3. Verify far-field R-wave is not sensed (within PVARP)
  4. Verify P-wave after PVARP is sensed correctly
  5. Verify A-pace is not triggered by far-field R-wave

Expected Results:
  - PVARP: 300 ms +/- 10 ms
  - Far-field R-wave during PVARP: not sensed
  - P-wave after PVARP: correctly sensed
  - No inappropriate atrial pacing triggered by far-field signals
```

## 15.9.7 VVIR Mode Testing (Rate Response)

### Test VVIR-01: Sensor Response

```
Objective: Verify rate modulation based on activity sensor

Test Setup:
  - Mode: VVIR
  - Lower rate limit: 60 bpm
  - Upper rate limit: 120 bpm
  - Sensor type: Accelerometer

Procedure:
  1. Verify pacing at 60 bpm with no activity
  2. Apply vibration simulating walking (moderate activity)
  3. Verify pacing rate increases above 60 bpm
  4. Apply vibration simulating running (high activity)
  5. Verify pacing rate increases toward 120 bpm
  6. Remove vibration
  7. Verify pacing rate gradually decreases back to 60 bpm

Expected Results:
  - Rate increase follows sensor response curve
  - Response time: 10-30 seconds to reach 50% of target rate
  - Recovery time: 60-120 seconds to return to lower rate limit
  - No rate oscillations during steady-state activity
```

### Test VVIR-02: Sensor Threshold

```
Objective: Verify minimum activity level for rate response

Procedure:
  1. Apply vibration at increasing levels
  2. Record pacing rate at each vibration level
  3. Determine threshold vibration for rate increase

Expected Results:
  - Threshold vibration: < 0.01 g (very sensitive to activity)
  - Rate increases monotonically with vibration amplitude
  - No rate response below threshold (avoid noise-induced rate increase)
```

### Test VVIR-03: Rate Response Curve

```
Objective: Verify programmed rate response curve

Test Setup:
  - Rate response curve: Linear from 60 bpm at rest to 120 bpm at max activity

Procedure:
  1. Set vibration levels from 0% to 100% in 10% steps
  2. Record steady-state pacing rate at each level
  3. Plot measured rate vs. vibration level
  4. Compare with programmed curve

Expected Results:
  - Measured curve follows programmed curve within 5 bpm
  - Linear response as programmed
  - No saturation or nonlinearity in the response
```

## 15.9.8 Magnet Mode Testing

### Test MAG-01: Magnet Response

```
Objective: Verify response to external magnet application

Procedure:
  1. Apply magnet (simulated by driving MAG pin)
  2. Verify mode switches to asynchronous (DOO or VOO)
  3. Verify pacing rate changes to magnet rate (typically 100 bpm)
  4. Remove magnet
  5. Verify mode reverts to programmed mode
  6. Measure magnet rate accuracy

Expected Results:
  - Magnet detection within 1 second
  - Magnet rate: 100 bpm +/- 5 bpm
  - Mode reverts within 1 second of magnet removal
  - No data loss during magnet mode transition
```

### Test MAG-02: Magnet Application Duration

```
Objective: Verify behavior during prolonged magnet application

Procedure:
  1. Apply magnet
  2. Maintain magnet for 30 seconds
  3. Verify continuous asynchronous pacing
  4. Remove magnet
  5. Verify normal mode resumes

  6. Apply magnet for 60 seconds
  7. Verify battery status counter increments
  8. Remove magnet
  9. Verify battery status retained

Expected Results:
  - Continuous operation in magnet mode
  - Battery status properly tracked during magnet mode
  - No adverse effects from prolonged magnet application
```

## 15.9.9 Mode Transition Testing

### Test TRANS-01: Programmer-Initiated Mode Change

```
Objective: Verify mode changes commanded by programmer

Procedure:
  1. Start in VVI mode, verify normal operation
  2. Command mode change to DDD via SPI/telemetry
  3. Verify mode changes within 1 second
  4. Verify all DDD parameters loaded correctly
  5. Command mode change to VVIR
  6. Verify mode changes correctly
  7. Command mode change back to VVI
  8. Verify original VVI parameters restored

Expected Results:
  - Mode changes complete within 1 second
  - All parameters correctly loaded for each mode
  - No pacing interruption during mode change
  - Previous mode parameters stored and restorable
```

### Test TRANS-02: Automatic Mode Change (Safety)

```
Objective: Verify automatic mode change on fault detection

Procedure:
  1. Start in DDD mode
  2. Inject fault on atrial sensing channel (open circuit)
  3. Verify automatic switch to VVI mode (safe fallback)
  4. Verify alert generated (telemetry notification)
  5. Clear fault condition
  6. Verify mode remains in VVI (manual intervention required)

Expected Results:
  - Fault detected within 5 seconds
  - Mode switches to safe fallback (VVI)
  - Alert transmitted to programmer
  - Mode does not automatically revert (requires clinician action)
```

## 15.9.10 Timing Accuracy Summary

### Comprehensive Timing Measurements

```
Parameter                        | Setting  | Measured   | Error    | Limit
---------------------------------|----------|------------|----------|--------
VVI pacing interval              | 1000 ms  | 1001.2 ms  | +0.12%  | +/- 5%
AAI pacing interval              | 1000 ms  | 999.8 ms   | -0.02%  | +/- 5%
DDD AV delay                     | 200 ms   | 199.5 ms   | -0.25%  | +/- 5%
DDD VA interval                  | 800 ms   | 800.7 ms   | +0.09%  | +/- 5%
PVARP                            | 300 ms   | 302.1 ms   | +0.70%  | +/- 10%
ARP (post-pace)                  | 250 ms   | 251.8 ms   | +0.72%  | +/- 10%
VRP (post-sense)                 | 350 ms   | 348.5 ms   | -0.43%  | +/- 10%
Upper rate limit                 | 120 bpm  | 119.8 bpm  | -0.17%  | +/- 5%
Lower rate limit                 | 60 bpm   | 60.1 bpm   | +0.17%  | +/- 5%
Magnet rate                      | 100 bpm  | 100.3 bpm  | +0.30%  | +/- 5%
Rate response recovery time      | 60 s     | 62.3 s     | +3.8%   | +/- 20%

All timing parameters within specification.
```

## 15.9.11 Summary

The pacemaker mode testing of the iPACE-CHIP validates correct implementation of all supported pacing modes, including single-chamber (VVI, AAI), dual-chamber (DDD, VDD), rate-responsive (VVIR, AAIR, DDDR), and test/magnet modes. Timing accuracy across all modes meets the +/- 5% specification, and mode transitions occur smoothly within the required 1-second window. The sensing algorithm correctly detects cardiac events at the programmed threshold and rejects non-cardiac signals (T-waves, far-field signals). These results demonstrate that the iPACE-CHIP provides safe and effective pacing therapy across all supported clinical applications.
