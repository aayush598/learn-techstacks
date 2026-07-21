# Shutdown Power Management for Implantable Pacemaker ASICs

## 1. Introduction to Shutdown Power

Shutdown power management is a critical capability for implantable pacemaker ASICs, enabling the device to enter ultra-low-power states during periods of inactivity. In the iPACE-CHIP design, shutdown modes reduce power consumption from microwatts to nanowatts, extending battery life to meet the 10-year requirement. Shutdown power encompasses the residual power consumed when circuit blocks are selectively powered down while maintaining essential functions.

The effectiveness of shutdown power management depends on the depth of power-down achievable, the wake-up time required to resume operation, and the energy overhead of entering and exiting shutdown states. A well-designed shutdown strategy balances power savings against system responsiveness requirements.

## 2. Shutdown Power Components

### 2.1 Residual Leakage

Even in shutdown mode, some circuits remain powered and contribute leakage:

```
Always-On Circuit Leakage:

Circuit                  │ Leakage (nA) │ Why Always-On
─────────────────────────┼──────────────┼──────────────
Watchdog oscillator      │ 5            │ Safety requirement
Reset controller        │ 2            │ Startup supervision
Power-on detector       │ 1            │ Voltage monitoring
Backup oscillator       │ 3            │ Recovery timing
Configuration retention  │ 8            │ State preservation
I/O pad bias            │ 10           │ External pull-ups
─────────────────────────┼──────────────┼──────────────
TOTAL always-on          │ 29           │
```

### 2.2 Power Switch Leakage

Power switches themselves contribute leakage in the off state:

```
Power Switch Leakage Model:

PMOS Header Switch:
I_leak = I_D × exp(-V_th / (n × V_T))

For iPACE-CHIP power switch:
- W = 10 μm (sized for on-resistance)
- V_th = 400 mV (high-Vt switch)
- V_DS = 1.8V (full supply)
- I_leak ≈ 50 pA per switch

NMOS Footer Switch:
- Similar analysis
- Body effect increases V_th
- I_leak ≈ 30 pA per switch

Total power switch leakage (100 switches):
I_total ≈ 5 nA (negligible vs. always-on circuits)
```

### 2.3 Retention Power

Circuits retaining state during shutdown consume power:

```
Retention Power Sources:

1. Retention Flip-Flops:
   - Cross-coupled inverters maintain state
   - Leakage: 0.5-2 nA per flip-flop
   - Total for 1000 retention flops: 0.5-2 μA

2. SRAM Retention:
   - Reduced voltage operation (V_DD_ret = 0.5V)
   - Reduced leakage: 5× compared to full voltage
   - 2KB SRAM retention: ~20 nA

3. Configuration Registers:
   - Critical for startup configuration
   - Typically implemented with retention flops
   - Total: ~10 nA

4. Watchdog State:
   - Timer counter value
   - Interrupt pending flags
   - Total: ~5 nA
```

## 3. Shutdown State Taxonomy

### 3.1 Power State Hierarchy

```
iPACE-CHIP Power States:

┌─────────────────────────────────────────────────────────┐
│                    STATE 0: ACTIVE                      │
│                    Power: 50 μW                         │
│                    All blocks powered                    │
└─────────────────────────┬───────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────┐
│                   STATE 1: IDLE                         │
│                    Power: 5 μW                          │
│                    DSP clock gated                      │
└─────────────────────────┬───────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────┐
│                 STATE 2: MONITOR                        │
│                  Power: 500 nW                          │
│                  DSP powered off                        │
│                  Sensing remains active                 │
└─────────────────────────┬───────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────┐
│                 STATE 3: STANDBY                        │
│                   Power: 50 nW                          │
│                   Sensing powered off                   │
│                   Oscillator running                    │
└─────────────────────────┬───────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────┐
│                 STATE 4: SHUTDOWN                       │
│                   Power: 10 nW                          │
│                   All blocks off                        │
│                   Only retention + WDT                  │
└─────────────────────────┬───────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────┐
│                 STATE 5: DEEP SHUTDOWN                  │
│                   Power: 5 nW                           │
│                   Minimal retention                     │
│                   External wake-up only                 │
└─────────────────────────────────────────────────────────┘
```

### 3.2 State Transition Matrix

```
Transition Times and Energy Costs:

From\To      │ Active │ Idle  │ Monitor│ Standby│ Shutdown│Deep
─────────────┼────────┼───────┼────────┼────────┼─────────┼──────
Active       │   -    │ 1 μs  │ 10 μs  │ 100 μs │ 1 ms    │10 ms
Idle         │ 1 μs   │  -    │ 10 μs  │ 100 μs │ 1 ms    │10 ms
Monitor      │ 100 μs │ 10 μs │   -    │ 100 μs │ 1 ms    │10 ms
Standby      │ 500 μs │ 100 μs│ 200 μs │   -    │ 1 ms    │10 ms
Shutdown     │ 5 ms   │ 1 ms  │ 2 ms   │ 1 ms   │   -     │10 ms
Deep Shutdown│ 50 ms  │ 10 ms │ 20 ms  │ 10 ms  │ 10 ms   │  -

Energy to Enter (per transition):
- Active → Idle: 50 pJ
- Active → Monitor: 500 pJ
- Active → Standby: 5 nJ
- Active → Shutdown: 50 nJ
- Active → Deep Shutdown: 500 nJ

Energy to Exit (per transition):
- Idle → Active: 50 pJ
- Monitor → Active: 500 pJ
- Standby → Active: 5 nJ
- Shutdown → Active: 50 nJ
- Deep Shutdown → Active: 500 nJ
```

## 4. Shutdown Control Architecture

### 4.1 Power State Controller

```
Power State Controller (PSC):

┌──────────────────────────────────────────────────┐
│                Power State Controller             │
│                                                  │
│  ┌──────────────┐  ┌──────────────┐              │
│  │   State      │  │  Transition  │              │
│  │   Register   │──│  Logic       │              │
│  └──────┬───────┘  └──────┬───────┘              │
│         │                 │                      │
│  ┌──────▼───────┐  ┌──────▼───────┐              │
│  │   Power      │  │   Clock      │              │
│  │   Switch     │  │   Control    │              │
│  │   Manager    │  │   Unit       │              │
│  └──────┬───────┘  └──────┬───────┘              │
│         │                 │                      │
│  ┌──────▼───────┐  ┌──────▼───────┐              │
│  │   Wake-up    │  │   Reset      │              │
│  │   Detector   │  │   Sequencer  │              │
│  └──────────────┘  └──────────────┘              │
│                                                  │
│  Inputs:                                         │
│  - Software request (register write)             │
│  - Hardware event (low battery, etc.)            │
│  - External pin (programming interface)          │
│  - Watchdog timeout                             │
│                                                  │
│  Outputs:                                        │
│  - Power switch enable signals                   │
│  - Clock gate signals                           │
│  - Reset signals                                 │
│  - Wake-up acknowledgment                        │
└──────────────────────────────────────────────────┘
```

### 4.2 Shutdown Sequencing

```
Shutdown Sequence (State 0 → State 4):

Time    │ Action
────────┼───────────────────────────────────────────────
T0      │ Software initiates shutdown request
T0+1μs  │ Save critical registers to retention
T0+2μs  │ Disable all interrupts
T0+3μs  │ Complete pending memory operations
T0+4μs  │ Flush pipeline states
T0+5μs  │ Disable clock outputs to powered blocks
T0+10μs │ Assert reset to non-essential blocks
T0+50μs │ Begin power switch turn-off sequence
T0+100μs│ Power switches fully off (state-dependent)
T0+200μs│ Verify power-down status
T0+500μs│ Enter stable shutdown state

Total shutdown time: ~500 μs (State 0 → State 4)
Energy cost: ~50 nJ (dominated by power switch transitions)
```

### 4.3 Wake-Up Sequence

```
Wake-Up Sequence (State 4 → State 0):

Time     │ Action
─────────┼───────────────────────────────────────────────
T0       │ Wake-up event detected (alarm, external)
T0+1μs   │ PSC acknowledges wake-up request
T0+5μs   │ Begin power switch turn-on sequence
T0+50μs  │ Power switches fully on
T0+55μs  │ Start oscillator and wait for stability
T0+60μs  │ Release reset to blocks
T0+70μs  │ Load retention values to flip-flops
T0+100μs │ Verify clock stability
T0+150μs │ Restore configuration registers
T0+200μs │ Re-enable interrupts
T0+300μs │ Resume normal operation
T0+500μs │ Full functional restoration

Total wake-up time: ~500 μs (State 4 → State 0)
Energy cost: ~50 nJ (inrush current, oscillator startup)
```

## 5. Power Switch Implementation

### 5.1 Header Switch (PMOS)

```
PMOS Header Power Switch:

V_DD ─────────────────────┐
                          │
                    ┌─────┴─────┐
                    │   PMOS    │
                    │  Header   │
                    │  Switch   │
                    └─────┬─────┘
                          │
                    V_DD_switched
                          │
                    ┌─────┴─────┐
                    │  Power    │
                    │  Domain   │
                    │  Load     │
                    └─────┬─────┘
                          │
GND ──────────────────────┘

Design Parameters:
- W/L = 10μm / 0.18μm
- R_on ≈ 50 Ω (at V_GS = -1.8V)
- I_leak ≈ 50 pA (at V_GS = 0V)
- C_gate ≈ 20 fF

Gate Control:
- V_G = V_DD: Switch OFF (V_GS = 0)
- V_G = GND: Switch ON (V_GS = -V_DD)
- Transition time: ~10 ns (RC limited)
```

### 5.2 Footer Switch (NMOS)

```
NMOS Footer Power Switch:

V_DD ──────────────────────┐
                           │
                     ┌─────┴─────┐
                     │  Power    │
                     │  Domain   │
                     │  Load     │
                     └─────┬─────┘
                           │
                     V_DD_footer
                           │
                     ┌─────┴─────┐
                     │   NMOS    │
                     │  Footer   │
                     │  Switch   │
                     └─────┬─────┘
                           │
GND ───────────────────────┘

Design Parameters:
- W/L = 8μm / 0.18μm
- R_on ≈ 60 Ω (at V_GS = 1.8V)
- I_leak ≈ 30 pA (at V_GS = 0V)
- C_gate ≈ 16 fF

Note: NMOS footer has body effect that increases R_on
when V_DD is applied. Larger width needed vs. PMOS header.
```

### 5.3 Sleep Transistor Sizing

```
Sleep Transistor Sizing Methodology:

Step 1: Determine Maximum IR Drop
- Acceptable voltage droop: < 5% of V_DD = 90 mV
- Maximum current: I_max = 10 μA (active mode)
- R_on,max = 90 mV / 10 μA = 9 kΩ

Step 2: Calculate Transistor Width
For PMOS header:
- R_on ∝ 1/W (inversely proportional to width)
- Minimum W = 0.5 μm (process minimum)
- For R_on = 9 kΩ: W = 0.1 μm (very small)

For practical design (accounting for process variation):
- W = 2 μm (provides margin)
- R_on ≈ 2.5 kΩ (well below 9 kΩ limit)

Step 3: Verify Leakage
- I_leak at W = 2 μm: ~100 pA (acceptable)
- Multiple switches in parallel increase leakage
- Total leakage budget: 5 nA (50 switches × 100 pA)
```

### 5.4 Multi-Stage Power Switching

```
Cascaded Power Switch Architecture:

For deep shutdown modes, multi-stage switching reduces leakage:

Stage 1: Main Switch (always present)
┌─────────────────────────────────────────┐
│ V_DD ──┤ PMOS ├── V_DD_main            │
│        (W=5μm)  │                      │
│                 │                      │
│          ┌──────┴──────┐               │
│          │  Stage 2    │               │
│          │  Switch     │               │
│          │  (W=1μm)    │               │
│          └──────┬──────┘               │
│                 │                      │
│          ┌──────┴──────┐               │
│          │  Load       │               │
│          └─────────────┘               │
└─────────────────────────────────────────┘

Benefits:
- Main switch: Fast on/off for normal shutdown
- Stage 2: Ultra-low leakage for deep shutdown
- Combined leakage: ~5 pA (vs. 100 pA single switch)

Drawback:
- Additional voltage drop: 0.2V across stage 2
- Reduced noise margin
- More complex control
```

## 6. Shutdown Modes for iPACE-CHIP

### 6.1 Normal Operation Mode

```
Mode: NORMAL
Power: 50 μW
Duration: 95% of time (when heart is in normal rhythm)

Active Circuits:
- Cardiac sensing amplifier: ON
- Signal processing (DSP): ON (32 kHz)
- Pacing control logic: ON
- Stimulation output: OFF (until needed)
- Communication: OFF (until interrogation)
- All clocks: Running
- All power domains: ON

Power Breakdown:
┌─────────────────────┬──────────┐
│ Block               │ Power    │
├─────────────────────┼──────────┤
│ Sensing             │ 800 nW   │
│ DSP                 │ 1500 nW  │
│ Pacing logic        │ 500 nW   │
│ Clock distribution  │ 1000 nW  │
│ Other digital       │ 500 nW   │
│ Leakage             │ 100 nW   │
├─────────────────────┼──────────┤
│ TOTAL               │ 4.4 μW   │
└─────────────────────┴──────────┘
```

### 6.2 Monitoring Mode

```
Mode: MONITOR
Power: 500 nW
Duration: 4% of time (between cardiac events)

Active Circuits:
- Cardiac sensing amplifier: ON
- Signal processing: OFF (clock gated)
- Pacing control logic: ON (minimal)
- Stimulation output: OFF
- Communication: OFF
- Most clocks: GATED

Shutdown Actions:
1. Gate DSP clock (saves 1500 nW)
2. Gate non-essential clocks (saves 400 nW)
3. Reduce clock frequency to 8 kHz
4. Maintain sensing for R-wave detection

Power Breakdown:
┌─────────────────────┬──────────┐
│ Block               │ Power    │
├─────────────────────┼──────────┤
│ Sensing             │ 800 nW   │
│ Pacing logic        │ 100 nW   │
│ Clock distribution  │ 100 nW   │
│ Leakage             │ 100 nW   │
├─────────────────────┼──────────┤
│ TOTAL               │ 1100 nW  │
└─────────────────────┴──────────┘
```

### 6.3 Standby Mode

```
Mode: STANDBY
Power: 50 nW
Duration: < 1% of time (programming, maintenance)

Active Circuits:
- Cardiac sensing: OFF
- Signal processing: OFF
- Pacing logic: OFF
- Stimulation: OFF
- Communication: OFF
- Oscillator: RUNNING (low power)
- Watchdog: RUNNING

Shutdown Actions:
1. Power off sensing amplifier
2. Power off DSP block
3. Reduce oscillator to 1 Hz
4. Retain configuration in retention flops

Wake-Up Sources:
- External programming command
- Watchdog timeout
- Battery low alarm
- Manual reset

Power Breakdown:
┌─────────────────────┬──────────┐
│ Block               │ Power    │
├─────────────────────┼──────────┤
│ Oscillator          │ 20 nW    │
│ Watchdog            │ 10 nW    │
│ Retention           │ 15 nW    │
│ Leakage             │ 5 nW     │
├─────────────────────┼──────────┤
│ TOTAL               │ 50 nW    │
└─────────────────────┴──────────┘
```

### 6.4 Deep Shutdown Mode

```
Mode: DEEP_SHUTDOWN
Power: 10 nW
Duration: During implantation, non-use periods

Active Circuits:
- Oscillator: OFF
- Watchdog: OFF (except wake-up detector)
- Everything: OFF
- Only: Configuration retention + external wake-up

Shutdown Actions:
1. Power off all logic blocks
2. Stop oscillator
3. Disable watchdog
4. Retain minimal configuration (NVM)
5. External pin provides wake-up

Wake-Up Sources:
- External pin only (programming tool)
- No autonomous wake-up

Power Breakdown:
┌─────────────────────┬──────────┐
│ Block               │ Power    │
├─────────────────────┼──────────┤
│ Configuration NVM   │ 3 nW     │
│ I/O pad bias        │ 5 nW     │
│ Leakage             │ 2 nW     │
├─────────────────────┼──────────┤
│ TOTAL               │ 10 nW    │
└─────────────────────┴──────────┘
```

## 7. Shutdown Timing Analysis

### 7.1 Entry Timing Requirements

```
Shutdown Entry Timing Constraints:

Constraint 1: State Preservation
- Must complete state save before power-off
- Save time: 10 μs (retention flop write)
- Timeout: 50 μs (if save fails, force power-off)

Constraint 2: Analog Settling
- Amplifier bias currents must settle before measurement
- Settling time: 100 μs
- Cannot shutdown during active measurement

Constraint 3: Communication Completion
- Must complete any active UART transaction
- Maximum UART frame: 11 bits at 9.6 kbps = 1.15 ms
- Must wait for frame completion before shutdown

Constraint 4: Stimulation Safety
- Cannot shutdown during active stimulation pulse
- Maximum pulse width: 2 ms
- Must complete pulse before power domain shutdown

Total Entry Time Budget: 2 ms (worst case)
```

### 7.2 Exit Timing Requirements

```
Shutdown Exit Timing Constraints:

Constraint 1: Oscillator Startup
- Crystal oscillator startup: 100-500 μs
- RC oscillator startup: 10-50 μs
- Must wait for clock stability

Constraint 2: Power Supply Settling
- Decoupling capacitor charging: 50 μs
- Voltage regulator settling: 100 μs
- Must verify V_DD within specification

Constraint 3: Reset Assertion
- Minimum reset pulse width: 10 μs
- Clock monitoring before reset release: 50 μs
- Total reset sequence: 100 μs

Constraint 4: State Restoration
- Retention flop restore: 10 μs
- Register reload: 50 μs
- Configuration verification: 20 μs

Total Exit Time Budget: 1 ms (worst case)
```

### 7.3 Timing Diagram

```
Shutdown/Wake-Up Timing Diagram:

Signal         T0    T1    T2    T3    T4    T5    T6
              ─────┬─────┬─────┬─────┬─────┬─────┬─────
Power Request  ____|‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾|____
              (asserted at T0)

State Save     ____|‾‾‾‾‾‾‾|________________________
              (T0 to T1: 50 μs)

Power Switches ‾‾‾‾‾‾‾‾‾‾‾|____|____________________
              (off at T1)

V_DD_domain    ‾‾‾‾‾‾‾‾‾‾‾\______|‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
              (decays T1-T2, ramps T2-T3)

Oscillator     ‾‾‾‾‾‾‾|____|___________|‾‾‾‾‾‾‾‾‾‾‾
              (off T1, restarts T3)

Reset          ‾‾‾‾‾‾‾‾‾‾‾‾|____|____________________
              (asserted at T2, released T4)

Wake-Up Event  ______________________|‾‾‾‾‾‾‾‾‾‾‾‾‾
              (external event at T3)

Full Operation ______________________________|‾‾‾‾‾‾‾
              (restored at T5)

Time Scale:
T0: 0 μs (request)
T1: 50 μs (power off)
T2: 100 μs (oscillator stop)
T3: 200 μs (wake-up event)
T4: 300 μs (reset released)
T5: 500 μs (full operation)
T6: 1000 μs (monitoring)
```

## 8. Wake-Up Mechanisms

### 8.1 Wake-Up Source Architecture

```
Wake-Up Source Priority and Configuration:

Priority │ Source          │ Always-On │ Mode Required
─────────┼─────────────────┼───────────┼──────────────
1 (highest)│ External Pin  │ Yes       │ Any mode
2        │ Watchdog Timer  │ Yes       │ Standby+
3        │ Low Battery    │ Yes       │ Any mode
4        │ Cardiac Event  │ No        │ Monitor+
5        │ UART Reception │ No        │ Idle+
6        │ Timer Alarm    │ Partial   │ Standby+
7 (lowest) │ Software      │ No        │ Idle+

Wake-Up Controller Logic:

┌─────────────────────────────────────────┐
│ Wake-Up Controller                      │
│                                         │
│  ┌─────────────┐                        │
│  │ Priority    │                        │
│  │ Encoder     │◄─── Wake-up sources    │
│  └──────┬──────┘                        │
│         │                               │
│  ┌──────▼──────┐                        │
│  │ Arbitration │                        │
│  │ Logic       │                        │
│  └──────┬──────┘                        │
│         │                               │
│  ┌──────▼──────┐  ┌─────────────┐       │
│  │ State       │──│ Power State │       │
│  │ Machine     │  │ Controller  │       │
│  └──────┬──────┘  └─────────────┘       │
│         │                               │
│  ┌──────▼──────┐                        │
│  │ Interrupt   │                        │
│  │ Generator   │                        │
│  └─────────────┘                        │
└─────────────────────────────────────────┘
```

### 8.2 External Pin Wake-Up

```
External Wake-Up Implementation:

Pin Configuration:
┌──────────────────────────────────────┐
│ External Pin (WAKEUP_n)              │
│                                      │
│  V_DD ──────┤R├──── Pin              │
│             (100kΩ)                  │
│                                      │
│  Pin ──────────── To PSC             │
│                                      │
│  External Tool ──── Capacitor ── GND │
│                  (100nF)             │
└──────────────────────────────────────┘

Wake-Up Sequence:
1. External tool pulls pin low (capacitive coupling)
2. PSC detects falling edge
3. Debounce circuit (10 μs) confirms valid signal
4. PSC initiates wake-up sequence
5. Software reads wake-up source register

Edge Detection:
- Falling edge: Wake-up from any mode
- Rising edge: Optional (configurable)
- Level detection: For sustained wake-up requests
```

### 8.3 Internal Wake-Up Sources

```
Internal Wake-Up Implementation:

Watchdog Wake-Up:
┌──────────────────────────────────────┐
│ Watchdog Timer (always-on)           │
│                                      │
│  Oscillator ──── Counter ──── Compare│
│  (1 Hz)        (8-bit)     (config) │
│                                      │
│  Match ──── Wake-up Request         │
│                                      │
│  Purpose: Periodic system check      │
│  Interval: 1s to 255s (configurable)│
└──────────────────────────────────────┘

Cardiac Event Wake-Up:
┌──────────────────────────────────────┐
│ Sensing Amplifier + Comparator       │
│                                      │
│  Electrode ── Amplifier ── Comparator│
│                        (threshold)   │
│                                      │
│  Detection ──── Wake-up Request     │
│                                      │
│  Purpose: Detect R-wave for pacing  │
│  Sensitivity: 0.5 mV to 5 mV       │
└──────────────────────────────────────┘

Low Battery Wake-Up:
┌──────────────────────────────────────┐
│ Battery Monitor (always-on)          │
│                                      │
│  V_batt ── Divider ── Comparator    │
│           (1/3)      (1.0V ref)     │
│                                      │
│  V_batt < 2.4V ──── Wake-up        │
│  V_batt < 2.2V ──── Emergency      │
└──────────────────────────────────────┘
```

## 9. Energy Budget for Shutdown Operations

### 9.1 Energy Cost Analysis

```
Shutdown Energy Budget:

Operation             │ Energy    │ Notes
──────────────────────┼───────────┼──────────────
State save            │ 0.5 nJ    │ Retention flop write
Power switch off      │ 5 nJ      │ Capacitive discharge
Clock stop            │ 1 nJ      │ Clock tree discharge
Power switch on       │ 5 nJ      │ Capacitive charge
Oscillator startup    │ 10 nJ     │ Crystal warmup
Reset sequence        │ 2 nJ      │ Logic reset
State restore         │ 0.5 nJ    │ Retention flop read
Register reload       │ 1 nJ      │ Configuration load
Clock restart         │ 5 nJ      │ PLL/clock recovery
──────────────────────┼───────────┼──────────────
TOTAL per cycle       │ 30 nJ     │ Shutdown + wake-up

Break-Even Analysis:
- Power saved per shutdown: P_saved × t_shutdown
- Energy cost per cycle: 30 nJ
- Minimum beneficial shutdown duration: t_min = 30 nJ / P_saved

For P_saved = 4.5 μW:
- t_min = 30 nJ / 4.5 μW = 6.7 ms
- Any shutdown > 6.7 ms saves net energy

For P_saved = 500 nW:
- t_min = 30 nJ / 500 nW = 60 ms
- Need > 60 ms shutdown to save net energy
```

### 9.2 Optimal Shutdown Strategy

```
Optimal Shutdown Decision Matrix:

Shutdown Duration │ P_saved=4.5μW │ P_saved=500nW │ Decision
──────────────────┼────────────────┼───────────────┼─────────
< 1 ms            │ Net LOSS      │ Net LOSS      │ Don't shutdown
1-10 ms           │ Marginal      │ Net LOSS      │ Case by case
10-100 ms         │ Net GAIN      │ Marginal      │ Shutdown
100 ms - 1 s      │ Net GAIN      │ Net GAIN      │ Shutdown
> 1 s             │ Net GAIN      │ Net GAIN      │ Shutdown

iPACE-CHIP Application:
- Typical idle period: 200-500 ms (between heartbeats)
- P_saved: 4.5 μW (MONITOR mode savings)
- Net energy savings: 850-2250 nJ per cycle
- Annual energy savings: ~5 mJ (significant for battery life)
```

## 10. Shutdown Verification

### 10.1 Power Rail Monitoring

```
Power Rail Monitoring During Shutdown:

Measurement Points:
1. V_DD_main: Main supply rail
2. V_DD_domain: Powered domain voltage
3. V_DD_ret: Retention voltage

Monitoring Circuit:
┌─────────────────────────────────────────┐
│ Power Rail Monitor                       │
│                                         │
│  V_DD_main ──┬── Comparator ── Status  │
│              │     (V > 1.62V?)         │
│              │                          │
│  V_DD_domain ─┤── Comparator ── Status  │
│              │     (V > 0.1V?)          │
│              │                          │
│  V_DD_ret ───┤── Comparator ── Status   │
│              │     (V > 0.45V?)         │
│              │                          │
│  All Status ── AND gate ── PMSC        │
│  (all OK)                               │
└─────────────────────────────────────────┘

Verification Checks:
- V_DD_domain < 0.1V: Power domain fully off
- V_DD_ret > 0.45V: Retention state valid
- I_total < target: Leakage within budget
```

### 10.2 Current Measurement in Shutdown

```
Shutdown Current Measurement:

Setup:
- Precision ammeter in series with V_DD
- Shielded measurement environment
- Temperature control: 37°C ± 0.5°C
- Averaging: 10 second window

Expected Results:
Mode              │ I_total   │ V_DD   │ P_total
──────────────────┼───────────┼────────┼─────────
Normal (active)   │ 28 μA     │ 1.8V   │ 50 μW
Monitor           │ 0.6 μA    │ 1.8V   │ 1.1 μW
Standby           │ 28 nA     │ 1.8V   │ 50 nW
Shutdown          │ 5.5 nA    │ 1.8V   │ 10 nW
Deep Shutdown     │ 2.8 nA    │ 1.8V   │ 5 nW

Verification Criteria:
- I_total within ±20% of target at 37°C
- No unexpected current paths
- Stable reading over 10 second window
- Consistent across 10 consecutive measurements
```

## 11. Reliability Considerations

### 11.1 Power Cycling Stress

```
Power Cycling Impact on Reliability:

Power Cycle Effects:
1. Thermal stress from inrush current
2. Voltage overshoot/undershoot at power switches
3. Electromigration during high-current transitions
4. Oxide stress from voltage transients

iPACE-CHIP Power Cycling Budget:
- Cycles per day: ~100,000 (every heartbeat)
- Cycles per year: ~36.5 million
- Cycles per 10 years: ~365 million

Reliability Assessment:
- 180nm process: >10⁹ power cycles typical
- iPACE-CHIP target: 365 × 10⁶ cycles
- Safety margin: 2.7× (acceptable)

Mitigation Techniques:
1. Controlled ramp rates for power switches
2. Debounce circuits to prevent false switching
3. Current limiting during power-on
4. Redundant retention paths
```

### 11.2 State Corruption Prevention

```
State Corruption Scenarios and Prevention:

Scenario 1: Partial State Save
- Cause: Power-off during state save sequence
- Prevention: State save completed in single clock cycle
- Detection: Checksum verification after restore

Scenario 2: Retention Voltage Drop
- Cause: Leakage exceeds retention capability
- Prevention: Oversized retention capacitance
- Detection: Retention voltage monitor

Scenario 3: Clock Glitch During Shutdown
- Cause: Clock continues after shutdown requested
- Prevention: Clock gate before power-off
- Detection: Clock monitor in shutdown mode

Scenario 4: Race Condition in Wake-Up
- Cause: Multiple blocks starting simultaneously
- Prevention: Staggered startup sequence
- Detection: Timeout watchdog during startup
```

## 12. Summary

Shutdown power management in the iPACE-CHIP pacemaker ASIC enables a 5000× power reduction from active mode (50 μW) to deep shutdown (10 nW). The implementation employs a hierarchical power state machine with six operating states, each optimized for specific power-saving requirements. Multi-stage power switches with high-Vt transistors minimize leakage to picoamps per switch, while retention flip-flops preserve critical state during shutdown. Wake-up mechanisms range from external pin (always available) to internal cardiac event detection (requiring partial power). Energy budget analysis demonstrates that shutdown cycles longer than 6.7 ms provide net energy savings, which is easily achieved during the 200-500 ms idle periods between heartbeats. The comprehensive shutdown strategy contributes significantly to achieving the 10-year battery life target for the iPACE-CHIP implantable pacemaker.

## References

1. Benini, L., De Micheli, G., "Dynamic Power Management: Design Techniques and CAD Tools," Kluwer Academic, 1998.
2. Stergiou, A., et al., "Power Management in Implantable Medical Devices," Springer, 2015.
3. iPACE-CHIP Project Internal Documentation: Shutdown Mode Specification, Rev 2.1.
4. Silvestri, M., et al., "Ultra-Low Power Shutdown Techniques for Medical ASICs," IEEE BioCAS, 2018.
5. JEDEC Standard JESD21-C: Configuration and Timing for Low Power Modes.
