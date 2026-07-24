# E-Beam Probing

## 15.15.1 Overview

Electron beam (e-beam) probing is a non-contact technique for measuring voltage waveforms on integrated circuit interconnects without the need for physical probe contacts. By scanning a focused electron beam across the chip surface and analyzing the energy of backscattered and secondary electrons, e-beam probes can measure the voltage at any point on the metal interconnect layers with sub-micron spatial resolution and sub-nanosecond temporal resolution. For the iPACE-CHIP, e-beam probing is the technique of last resort when JTAG, scan chain, and boundary scan methods cannot provide sufficient visibility into the root cause of a silicon failure.

## 15.15.2 E-Beam Probe Physics

### Principle of Operation

```
E-Beam Probing Principle:

1. Electron gun generates a focused beam (5-25 keV)
2. Beam scans across the chip surface
3. When beam hits a metal interconnect:
   a. Primary electrons penetrate the passivation layer
   b. Secondary electrons are emitted from the metal surface
   c. Energy of secondary electrons depends on local voltage:
      - V = 0V: Reference energy (calibrated)
      - V > 0V: Secondary electrons have lower energy (positive potential repels)
      - V < 0V: Secondary electrons have higher energy (negative potential attracts)
   d. Energy analyzer measures secondary electron energy shift
   e. Voltage is calculated: V = delta_E / e (where e is electron charge)

4. By synchronizing beam scanning with chip clock:
   a. Voltage waveform at any point can be reconstructed
   b. Temporal resolution determined by beam blanking speed
   c. Spatial resolution determined by beam spot size
```

### Spatial and Temporal Resolution

```
iPACE-CHIP E-Beam Probing Capabilities:

Spatial Resolution:
  - Beam spot size: 50 nm (at 10 keV)
  - Minimum feature resolved: 180 nm (iPACE-CHIP process node)
  - Metal pitch on iPACE-CHIP: 400 nm (adequate for e-beam)
  - Via opening size: 200 nm (accessible to beam)

Temporal Resolution:
  - Beam blanking speed: 10 ps
  - Effective temporal resolution: 100 ps (with synchronization)
  - Maximum observable frequency: 10 GHz (well above iPACE-CHIP signals)
  - Timebase accuracy: 50 ps (with PLL synchronization)

Voltage Resolution:
  - Voltage sensitivity: 10 mV
  - Dynamic range: -5V to +5V
  - Measurement accuracy: 50 mV (with calibration)
```

## 15.15.3 Sample Preparation

### Decapsulation

```
E-Beam Sample Preparation for iPACE-CHIP:

Step 1: Package Decapsulation
  - Chemical decapsulation using fuming nitric acid
  - Remove mold compound to expose die surface
  - Temperature: 120C for 10-15 minutes
  - Rinse with acetone and IPA

  Alternative: Laser decapsulation (less chemical exposure)
  - Nd:YAG laser ablation of mold compound
  - Precision: 10 um lateral accuracy
  - Advantage: No chemical handling

Step 2: Die Cleaning
  - Remove residual mold compound with O2 plasma
  - Clean with dilute HF (100:1) to expose metal
  - Duration: 30 seconds (minimal oxide removal)

Step 3: Passivation Opening (if needed)
  - Focused Ion Beam (FIB) to cut passivation window
  - Window size: 1-2 um (exposes metal line)
  - Time: 5-10 minutes per window
  - Can open multiple windows for different observation points
```

### Backside Probing (Alternative)

```
Backside E-Beam Probing:
  - Thin the silicon substrate from the back
  - Use infrared e-beam to probe through silicon
  - Advantages: No need to remove passivation
  - Limitations: Lower resolution due to IR wavelength
  - Application: Probing on the silicon substrate side

  For iPACE-CHIP: Not typically needed (front-side access adequate)
```

## 15.15.4 E-Beam Probing System

### System Architecture

```
E-Beam Probing System Components:

1. Electron Column:
   - Field emission electron gun (Schottky emitter)
   - Accelerating voltage: 1-25 keV (adjustable)
   - Beam current: 1 pA - 100 nA (adjustable)
   - Spot size: 50 nm - 2 um (current-dependent)
   - Blanker: Electrostatic, 10 ps rise time

2. Scan System:
   - Electrostatic deflection plates
   - Scan field: 500 um x 500 um (at high magnification)
   - Scan speed: 100 MHz (for stroboscopic operation)
   - Pixel dwell time: 10 ns - 100 us (configurable)

3. Sample Stage:
   - Piezoelectric XYZ stage
   - Travel: 10 mm x 10 mm x 5 mm
   - Positioning accuracy: 10 nm
   - Tilt: +/- 45 degrees

4. Energy Analyzer:
   - Through-the-lens energy analyzer
   - Energy resolution: 50 meV
   - Energy range: -5V to +5V
   - Bandwidth: DC to 10 GHz (with lock-in amplifier)

5. Signal Processing:
   - Lock-in amplifier for voltage extraction
   - Timebase module for synchronized acquisition
   - External trigger input for chip synchronization
   - FPGA-based waveform reconstruction

6. Control System:
   - Workstation with measurement software
   - Beam alignment and focusing
   - Automated navigation (die map)
   - Waveform display and analysis
```

### Typical E-Beam System

```
Commercial E-Beam Probing Systems:

System                | Manufacturer     | Resolution | Bandwidth
----------------------|------------------|------------|----------
Measuring e-beam      | JEOL JEBX-2100   | 50 nm      | 100 GHz
E-beam probe station  | Raith eLINE Plus | 10 nm      | 10 GHz
Voltage contrast      | FEI Quanta 200   | 3 nm       | 1 GHz
Picosecond e-beam     | Hamamatsu HPD   | 100 nm     | 1 THz

The iPACE-CHIP validation uses the JEOL JEBX-2100 or equivalent,
which provides adequate spatial resolution for 180nm features and
sufficient temporal resolution for the chip's 4 MHz operation.
```

## 15.15.5 E-Beam Probing Applications

### Application 1: Clock Distribution Debug

```
Objective: Verify clock signal reaches all parts of the chip

Problem: Clock not reaching the telemetry block (intermittent failure)

E-Beam Procedure:
  1. Navigate to clock distribution network on die photo
  2. Place beam at clock buffer input (CLK_IN node)
  3. Measure clock waveform at input
  4. Place beam at clock buffer output (CLK_TELEM node)
  5. Measure clock waveform at output
  6. Compare input and output waveforms

Results:
  CLK_IN waveform: Clean 4 MHz square wave, 0-1.2V
  CLK_TELEM waveform: No oscillation (stuck at 0.6V)

  Root cause identified: Clock buffer transistor stuck at
  intermediate voltage (threshold voltage shift due to
  contamination during fabrication)

  Fix: Add redundant clock buffer in next spin
```

### Application 2: Signal Integrity Measurement

```
Objective: Measure high-frequency signal integrity on critical interconnect

Problem: SPI clock showing unexpected ringing at 8 MHz

E-Beam Procedure:
  1. Navigate to SPI clock distribution tree
  2. Place beam at SPI clock pad (output to external)
  3. Acquire waveform with 10 ps resolution
  4. Analyze rise time, overshoot, ringing

Results:
  SPI clock at pad:
  - Rise time: 2.1 ns (within specification)
  - Overshoot: 15% (marginal, specification < 20%)
  - Ringing: 2 cycles at 800 MHz (damped)
  - Ringing amplitude: 12% of swing

  Root cause: Impedance mismatch at pad driver output
  The 50-ohm driver drives a 35-ohm trace (minor mismatch)
  
  Fix: Adjust pad driver strength in next revision
```

### Application 3: State Machine Debug

```
Objective: Observe internal state machine transitions

Problem: Pacing state machine occasionally skips a state

E-Beam Procedure:
  1. Identify state register bits on die photo
  2. Place beam on state bit 0 (Q0)
  3. Acquire waveform synchronized to system clock
  4. Place beam on state bit 1 (Q1)
  5. Reconstruct state machine sequence

Results:
  Expected sequence: IDLE(00) -> SENSING(01) -> PACING(10) -> REFRAC(11) -> IDLE(00)
  Observed sequence: IDLE(00) -> SENSING(01) -> [skip] -> REFRAC(11) -> IDLE(00)
  
  The PACING(10) state was skipped in one instance.
  
  Root cause: Race condition between state register and output logic
  at high frequency (4 MHz). The state register updates on rising edge,
  but the combinational logic for state transition evaluates before the
  register output has settled.
  
  Fix: Add pipeline register on state transition logic output
```

### Application 4: Power Distribution Debug

```
Objective: Measure IR drop on power distribution network

Problem: Chip works at 1.2V nominal but fails at 1.0V

E-Beam Procedure:
  1. Navigate to VDD_DIG power grid on top metal layer
  2. Place beam at power pad (known voltage: 1.0V)
  3. Measure voltage at power pad
  4. Move beam along power grid to measure voltage at various points
  5. Create voltage map of power distribution

Results:
  Location              | Voltage at 1.2V in | Voltage at 1.0V in
  ----------------------|--------------------|--------------------
  Power pad (Pad 1)     | 1.200V             | 1.000V
  Near pad (50 um)      | 1.198V             | 0.998V
  Mid-grid (200 um)     | 1.192V             | 0.992V
  Far from pad (500 um) | 1.180V             | 0.980V
  Farthest point (800um)| 1.165V             | 0.965V
  
  IR drop: 35 mV from pad to farthest point (at 1.2V in)
  At 1.0V in: IR drop is the same (35 mV), but 0.965V is below
  the functional limit (0.95V) at the farthest point.

  Root cause: Power grid resistance too high in the corner of the die
  
  Fix: Widen power grid metal in the next revision, add additional
  power vias to reduce resistance
```

### Application 5: Leakage Path Identification

```
Objective: Locate the source of excess leakage current

Problem: VDD_DIG leakage is 2x expected (144 uA vs. 72 uA expected)

E-Beam Procedure:
  1. Power on chip with VDD_DIG at 1.2V
  2. Scan beam across die surface in voltage contrast mode
  3. Areas with unexpected voltage indicate leakage paths
  4. Zoom into anomalous area
  5. Identify the specific transistor or interconnect causing leakage

Results:
  Voltage contrast scan reveals a bright spot (unexpected conduction)
  in the SRAM array area.
  
  Zooming in reveals a via connecting VDD_DIG to GND through a
  partially open transistor (not fully turned off).
  
  Root cause: Gate oxide defect in one SRAM cell's access transistor,
  causing it to be partially on even when programmed off.
  
  Impact: Single SRAM cell drawing extra 72 uA. This is a single-die
  defect, not a systematic issue. Yield impact: minimal.
```

## 15.15.6 E-Beam Probing Procedure

### Standard Operating Procedure

```
E-Beam Probing Session - iPACE-CHIP:

Pre-Session:
  1. Review die photo and metal layer maps
  2. Identify target nodes for probing
  3. Prepare navigation coordinates
  4. Load sample into e-beam system
  5. Rough alignment using optical microscope

Beam Setup:
  1. Column alignment (beam centering)
  2. Stigmation correction (beam circularity)
  3. Focus at sample surface
  4. Set accelerating voltage (5 keV for voltage contrast)
  5. Set beam current (100 pA for high resolution)

Voltage Calibration:
  1. Find known voltage reference on chip (VDD pad)
  2. Measure secondary electron energy at reference
  3. Set calibration: energy shift = 0 at VDD voltage
  4. Verify calibration at GND pad

Measurement:
  1. Navigate to target node
  2. Align beam to metal line
  3. Select measurement mode (DC voltage or waveform)
  4. For waveform: set trigger and timebase
  5. Acquire measurement
  6. Save data (waveform, image, coordinates)

Post-Session:
  1. Return beam to park position
  2. Vent chamber and remove sample
  3. Backup measurement data
  4. Document findings in debug report
```

## 15.15.7 E-Beam Probing Limitations

### Limitations and Challenges

```
Challenge                        | Impact on iPACE-WebKit Debug
---------------------------------|-----------------------------------
Charging of passivation layer    | Distorts voltage measurement
                                 | Mitigation: Use low beam current
                                 | and charge neutralization gun

Limited access to buried layers  | Can only probe top 2 metal layers
                                 | Mitigation: Use FIB to create
                                 | access windows to lower layers

Non-invasive but not non-contact | Electron beam can induce charge
                                 | Mitigation: Use low energy (1 keV)
                                 | for voltage measurement

Sample destruction risk          | Decapsulation can damage die
                                 | Mitigation: Laser decapsulation
                                 | (less chemical exposure)

Time-consuming setup             | Each probing session takes 2-4 hours
                                 | for setup and navigation
                                 | Mitigation: Document coordinates
                                 | for reuse in subsequent sessions

Not suitable for high-speed signals > 10 GHz
                                 | iPACE-CHIP operates at 4 MHz
                                 | No limitation for this application

Requires specialized equipment and expertise
                                 | Not all validation labs have access
                                 | Mitigation: Partner with failure
                                 | analysis lab or university facility
```

## 15.15.8 Comparison with Other Debug Techniques

```
Technique         | Invasiveness | Resolution | Speed  | Cost    | When to Use
------------------|--------------|------------|--------|---------|------------------
JTAG/Debug        | None         | Register   | Fast   | Low     | First resort
Boundary Scan     | None         | Pin-level  | Fast   | Low     | Interconnect test
Scan Chain        | None         | Flip-flop  | Medium | Low     | Logic fault detection
Logic Analyzer    | Minimal      | Board-level| Fast   | Medium  | Digital timing
Micro-probing     | Physical     | Metal line | Fast   | High    | Package-level debug
E-beam probing    | Minimal      | Sub-micron | Slow   | Very High | Last resort
FIB modification  | Permanent    | Sub-micron | Slow   | Very High | Hypothesis testing
TEM analysis      | Destructive  | Atomic     | N/A    | Very High | Defect characterization
```

## 15.15.9 Summary

E-beam probing is a powerful technique for non-contact voltage measurement on the iPACE-CHIP die surface, providing sub-micron spatial resolution and sub-nanosecond temporal resolution. While it is the most expensive and time-consuming debug technique available, it provides unique capabilities that cannot be replicated by other methods. For the iPACE-CHIP, e-beam probing has been successfully used to debug clock distribution issues, measure power grid IR drop, identify leakage paths, and observe internal state machine behavior. The technique is reserved for cases where JTAG, scan chain, and boundary scan methods cannot provide sufficient visibility, and its use is always preceded by careful cost-benefit analysis given the specialized equipment and expertise required.
