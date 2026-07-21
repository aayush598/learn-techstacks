# Pacemaker Functional Architecture

## 2.1.3 Functional Decomposition and State Machine

The functional architecture of the implantable cardiac pacemaker defines the
hierarchical decomposition of system functions, the state machine governing
mode transitions, and the firmware architecture that orchestrates all
real-time operations. This chapter provides a complete specification of the
functional behavior, from the top-level system states down to the
interrupt-driven firmware service routines.

---

## 2.3.1 Functional Decomposition Tree

The pacemaker system can be decomposed into a hierarchy of functions, each
responsible for a specific aspect of device operation. The decomposition
follows a top-down approach, with the system function at the root and
leaf-level functions mapping to specific hardware blocks or firmware modules.

```
PACEMAKER SYSTEM
│
├── 1. SENSING SUBSYSTEM
│   ├── 1.1 Atrial Sensing
│   │   ├── 1.1.1 P-wave detection
│   │   ├── 1.1.2 Far-field R-wave rejection
│   │   ├── 1.1.3 Noise discrimination
│   │   └── 1.1.4 Auto-sensitivity adjustment
│   ├── 1.2 Ventricular Sensing
│   │   ├── 1.2.1 R-wave detection
│   │   ├── 1.2.2 T-wave discrimination
│   │   ├── 1.2.3 Noise discrimination
│   │   └── 1.2.4 Auto-sensitivity adjustment
│   └── 1.3 Sensor Input (Rate Adaptation)
│       ├── 1.3.1 Accelerometer signal processing
│       ├── 1.3.2 Minute ventilation sensing
│       ├── 1.3.3 QT interval measurement
│       └── 1.3.4 Sensor-indicated rate calculation
│
├── 2. PACING SUBSYSTEM
│   ├── 2.1 Atrial Pacing
│   │   ├── 2.1.1 Pulse amplitude control
│   │   ├── 2.1.2 Pulse width control
│   │   ├── 2.1.3 Polarity control
│   │   └── 2.1.4 Charge balancing
│   ├── 2.2 Ventricular Pacing
│   │   ├── 2.2.1 Pulse amplitude control
│   │   ├── 2.2.2 Pulse width control
│   │   ├── 2.2.3 Polarity control
│   │   └── 2.2.4 Charge balancing
│   ├── 2.3 Left Ventricular Pacing (CRT)
│   │   ├── 2.3.1 LV offset timing
│   │   ├── 2.3.2 V-V delay programming
│   │   └── 2.3.3 Multi-site pacing
│   └── 2.4 Output Safety
│       ├── 2.4.1 Maximum output limiting
│       ├── 2.4.2 Impedance monitoring
│       └── 2.4.3 Threshold search
│
├── 3. TIMING AND CONTROL SUBSYSTEM
│   ├── 3.1 Timing Cycle Management
│   │   ├── 3.1.1 Lower rate limit timing
│   │   ├── 3.1.2 Upper rate limit timing
│   │   ├── 3.1.3 AV interval timing
│   │   ├── 3.1.4 VA interval timing
│   │   ├── 3.1.5 Refractory period management
│   │   └── 3.1.6 Blanking period management
│   ├── 3.2 Mode Logic
│   │   ├── 3.2.1 Mode state machine
│   │   ├── 3.2.2 Mode switch detection
│   │   ├── 3.2.3 Mode switch back
│   │   └── 3.2.4 Mode override (magnet)
│   ├── 3.3 Rate Adaptation
│   │   ├── 3.3.1 Sensor-indicated rate calculation
│   │   ├── 3.3.2 Rate response slope
│   │   ├── 3.3.3 Rate acceleration/deceleration
│   │   └── 3.3.4 Rate smoothing
│   └── 3.4 Safety Monitor
│       ├── 3.4.1 Watchdog timer
│       ├── 3.4.2 Maximum rate enforcement
│       ├── 3.4.3 Minimum rate enforcement
│       ├── 3.4.4 Runaway pacing prevention
│       └── 3.4.5 Fault detection and recovery
│
├── 4. COMMUNICATION SUBSYSTEM
│   ├── 4.1 RF Telemetry
│   │   ├── 4.1.1 Data modulation/demodulation
│   │   ├── 4.1.2 Packet framing
│   │   ├── 4.1.3 Error detection/correction
│   │   └── 4.1.4 Encryption (optional)
│   ├── 4.2 Programming Interface
│   │   ├── 4.2.1 Parameter read/write
│   │   ├── 4.2.2 Firmware update (if supported)
│   │   ├── 4.2.3 Diagnostic data retrieval
│   │   └── 4.2.4 Event log download
│   └── 4.3 Magnet Interface
│       ├── 4.3.1 Magnet detection
│       ├── 4.3.2 Mode switch to async
│       ├── 4.3.3 Telemetry activation
│       └── 4.3.4 Rate response to magnet
│
├── 5. POWER MANAGEMENT SUBSYSTEM
│   ├── 5.1 Battery Management
│   │   ├── 5.1.1 Battery voltage monitoring
│   │   ├── 5.1.2 Battery current monitoring
│   │   ├── 5.1.3 End-of-life detection
│   │   └── 5.1.4 Low-battery alert
│   ├── 5.2 Power Mode Control
│   │   ├── 5.2.1 Active mode management
│   │   ├── 5.2.2 Sleep mode management
│   │   ├── 5.2.3 Deep sleep management
│   │   └── 5.2.4 Hibernate mode management
│   └── 5.3 Clock Management
│       ├── 5.3.1 System clock generation
│       ├── 5.3.2 Clock gating
│       ├── 5.3.3 Clock scaling
│       └── 5.3.4 Clock accuracy monitoring
│
├── 6. DIAGNOSTICS SUBSYSTEM
│   ├── 6.1 Data Collection
│   │   ├── 6.1.1 Electrogram recording
│   │   ├── 6.1.2 Event logging
│   │   ├── 6.1.3 Histogram collection
│   │   └── 6.1.4 Trend data collection
│   ├── 6.2 Data Storage
│   │   ├── 6.2.1 SRAM management
│   │   ├── 6.2.2 EEPROM management
│   │   ├── 6.2.3 Data compression
│   │   └── 6.2.4 Data integrity checking
│   └── 6.3 Data Retrieval
│       ├── 6.3.1 On-demand download
│       ├── 6.3.2 Streaming mode
│       └── 6.3.3 Summary statistics
│
└── 7. SELF-TEST AND CALIBRATION
    ├── 7.1 Power-On Self-Test (POST)
    │   ├── 7.1.1 Memory test (SRAM/EEPROM)
    │   ├── 7.1.2 ADC self-test
    │   ├── 7.1.3 DAC self-test
    │   ├── 7.1.4 Timer verification
    │   └── 7.1.5 Communication test
    ├── 7.2 Periodic Self-Test
    │   ├── 7.2.1 Impedance measurement
    │   ├── 7.2.2 Battery voltage check
    │   ├── 7.2.3 Lead integrity check
    │   └── 7.2.4 Memory integrity check
    └── 7.3 Calibration
        ├── 7.3.1 ADC calibration
        ├── 7.3.2 DAC calibration
        ├── 7.3.3 Reference voltage calibration
        └── 7.3.4 Oscillator frequency calibration
```

---

## 2.3.2 Top-Level State Machine

The pacemaker operates as a finite state machine (FSM) with the following
top-level states. The state transitions are driven by sensing events,
timer expirations, external commands (magnet, RF programming), and safety
conditions.

```
                    ┌──────────────────────┐
                    │                      │
        ┌──────────│   POWER-ON RESET     │
        │          │   (POR)              │
        │          │                      │
        │          └──────────┬───────────┘
        │                     │
        │                     ▼
        │          ┌──────────────────────┐
        │          │                      │
        │          │   POST               │
        │          │   (Power-On          │
        │          │    Self-Test)        │
        │          │                      │
        │          └──────────┬───────────┘
        │                     │ POST pass
        │                     ▼
        │          ┌──────────────────────┐
        │          │                      │
        │          │   INITIALIZATION     │
        │          │   (Load parameters   │
        │          │    from EEPROM)      │
        │          │                      │
        │          └──────────┬───────────┘
        │                     │
        │                     ▼
┌───────┴────────┐   ┌──────────────────────┐   ┌──────────────────────┐
│                │   │                      │   │                      │
│   SLEEP MODE   │◀──│   ACTIVE MODE        │──▶│   TELEM MODE         │
│                │   │   (Sensing/Pacing)   │   │   (Programming/      │
│   (Ultra-low   │   │                      │   │    Data Transfer)    │
│    power)      │   │   ┌──────────────┐   │   │                      │
│                │   │   │              │   │   │                      │
│                │   │   │  ┌────────┐  │   │   │                      │
│                │   │   │  │ SENSE  │  │   │   │                      │
│                │   │   │  │ SUB-   │  │   │   │                      │
│                │   │   │  │ STATE  │  │   │   │                      │
│                │   │   │  └────────┘  │   │   │                      │
│                │   │   │  ┌────────┐  │   │   │                      │
│                │   │   │  │ DECIDE │  │   │   │                      │
│                │   │   │  │ SUB-   │  │   │   │                      │
│                │   │   │  │ STATE  │  │   │   │                      │
│                │   │   │  └────────┘  │   │   │                      │
│                │   │   │  ┌────────┐  │   │   │                      │
│                │   │   │  │ PACE   │  │   │   │                      │
│                │   │   │  │ SUB-   │  │   │   │                      │
│                │   │   │  │ STATE  │  │   │   │                      │
│                │   │   │  └────────┘  │   │   │                      │
│                │   │   │              │   │   │                      │
│                │   │   └──────────────┘   │   │                      │
│                │   │                      │   │                      │
└───────┬────────┘   └──────────┬───────────┘   └──────────┬───────────┘
        │                       │                          │
        │                       ▼                          │
        │          ┌──────────────────────┐                │
        │          │                      │                │
        │          │   SAFE MODE          │◀───────────────┘
        │          │   (VOO/VVI at        │  (fault detected
        │          │    backup rate)      │   during telemetry)
        │          │                      │
        │          └──────────┬───────────┘
        │                     │
        │                     ▼
        │          ┌──────────────────────┐
        └────────▶│   HIBERNATE MODE     │
                  │   (Minimum power,    │
                  │    timer only)       │
                  │                      │
                  └──────────────────────┘
```

---

## 2.3.3 Detailed Active Mode State Machine

The active mode is the primary operating state of the pacemaker, where it
continuously senses cardiac signals and delivers pacing pulses as needed.
The active mode contains a nested state machine that implements the sense-decide-pace
cycle.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         ACTIVE MODE STATE MACHINE                           │
│                                                                             │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                     SENSE-DECIDE-PACE CYCLE                         │   │
│  │                                                                      │   │
│  │                                                                      │   │
│  │         ┌──────────┐    Event     ┌──────────┐    Decision          │   │
│  │         │          │   Detected   │          │   Made                │   │
│  │  ┌─────▶│  SENSE   │────────────▶│  DECIDE  │─────────────┐       │   │
│  │  │      │  (AFE     │             │  (Timer  │             │       │   │
│  │  │      │  Active)  │             │  Check)  │             │       │   │
│  │  │      │          │             │          │             │       │   │
│  │  │      └──────────┘             └──────────┘             │       │   │
│  │  │           │                         │                   │       │   │
│  │  │           │ No event                │ No pace needed   │       │   │
│  │  │           │ (timer expired)         │ (event sensed)   │       │   │
│  │  │           │                         │                   │       │   │
│  │  │           ▼                         ▼                   │       │   │
│  │  │      ┌──────────┐             ┌──────────┐             │       │   │
│  │  │      │  TIMER   │             │  INHIBIT │             │       │   │
│  │  │      │  EXPIRED │             │  (No     │             │       │   │
│  │  │      │          │             │   Pace)  │             │       │   │
│  │  │      └─────┬────┘             └─────┬────┘             │       │   │
│  │  │            │                         │                  │       │   │
│  │  │            │ Pace needed            │ Reset timer      │       │   │
│  │  │            │                        │                  │       │   │
│  │  │            │      ┌─────────────────┘                  │       │   │
│  │  │            │      │                                    │       │   │
│  │  │            │      ▼                                    │       │   │
│  │  │            │  ┌──────────┐                             │       │   │
│  │  │            │  │  RESET   │                             │       │   │
│  │  │            │  │  TIMER   │◀────────────────────────────┘       │   │
│  │  │            │  │          │                                     │   │
│  │  │            │  └──────────┘                                     │   │
│  │  │            │                                                    │   │
│  │  │            ▼                                                    │   │
│  │  │      ┌──────────┐                                              │   │
│  │  └──────│  PACE    │                                              │   │
│  │         │  (Output │                                              │   │
│  │         │  Stage)  │                                              │   │
│  │         │          │                                              │   │
│  │         └──────────┘                                              │   │
│  │                                                                    │   │
│  └────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Sense Sub-State

The sense sub-state is the default active state. In this state:

1. The AFE is powered on and actively monitoring the intracardiac signal.
2. The digital threshold comparator is continuously comparing the filtered
   signal against the adaptive threshold.
3. The refractory period timers are running, enforcing blanking intervals.
4. The auto-sensitivity algorithm is tracking peak amplitudes.

When a valid sensing event is detected (signal exceeds threshold AND not
in refractory period AND passes morphology check), the sense sub-state
transitions to the decide sub-state.

When the sensing timeout expires (lower rate interval elapsed without a
sense event), the sense sub-state transitions to the pace sub-state.

### Decide Sub-State

The decide sub-state evaluates the timing cycle state and determines whether
a pacing pulse is required. The decision logic considers:

1. **Lower rate limit**: If the lower rate timer has expired, a pacing pulse
   is mandatory (asynchronous backup).
2. **AV interval**: If an atrial event was sensed/paced and the AV interval
   has elapsed without a ventricular event, ventricular pacing is triggered.
3. **VA interval**: If a ventricular event was sensed/paced and the VA
   interval has elapsed without an atrial event, atrial pacing is triggered.
4. **Upper rate limit**: If pacing would exceed the upper rate limit, the
   pulse is deferred (post-ventricular atral refractory period extends).
5. **Sensor rate**: If rate adaptation is enabled, the sensor-indicated rate
   may modify the timing intervals.

If the decision is to pace, the state transitions to the pace sub-state.
If the decision is to inhibit (a valid event was sensed in time), the state
transitions to the reset sub-state, which resets the timing counters and
returns to the sense sub-state.

### Pace Sub-State

The pace sub-state activates the pacing output stage:

1. Loads the programmed amplitude and pulse width parameters.
2. Activates the charge pump to generate the pacing voltage.
3. Enables the output switch to deliver the pulse to the lead.
4. After the programmed pulse width, opens the output switch.
5. Activates the charge balancing circuit.
6. Starts the post-pace blanking timer.
7. Transitions back to the sense sub-state after blanking expires.

---

## 2.3.4 NBG Pacemaker Mode Definitions

The NBG (NASPE/BPEG Generic) code is a standardized notation for describing
pacemaker modes. The code consists of three letters: the first letter
indicates the chamber(s) paced, the second indicates the chamber(s) sensed,
and the third indicates the response to sensing.

### Mode Definitions

| Mode | Paced | Sensed | Response | Description |
|------|-------|--------|----------|-------------|
| OOO | None | None | None | Asynchronous, no pacing or sensing |
| AOO | Atrium | None | None | Asynchronous atrial pacing |
| VOO | Ventricle | None | None | Asynchronous ventricular pacing |
| DOO | Both | None | None | Asynchronous dual-chamber pacing |
| AAI | Atrium | Atrium | Inhibited | Atrial demand pacing |
| VVI | Ventricle | Ventricle | Inhibited | Ventricular demand pacing |
| DDD | Both | Both | Inhibited/Triggered | Dual-chamber demand pacing |
| AAIR | Atrium | Atrium | Inhibited + Rate | Atrial demand with rate adaptation |
| VVIR | Ventricle | Ventricle | Inhibited + Rate | Ventricular demand with rate adaptation |
| DDDR | Both | Both | Inhibited/Triggered + Rate | Dual-chamber with rate adaptation |
| DDI | Both | Both | Inhibited | Dual-chamber inhibited (no triggered) |
| DDIR | Both | Both | Inhibited + Rate | Dual-chamber inhibited with rate adaptation |
| VDD | None | Both | Inhibited/Triggered | Single-lead VDD pacing |

### Extended Mode Notation

The NBG code can be extended with additional modifiers:

| Suffix | Meaning | Example |
|--------|---------|---------|
| R | Rate-adaptive (sensor-driven) | DDDR |
| O | Open (asynchronous) | DOO |
| T | Triggered (atrial-synchronous) | DDT |
| I | Inhibited | DDI |

---

## 2.3.5 DDD Mode Timing Cycle — Complete State Diagram

The DDD mode is the most complex pacing mode, managing both atrial and
ventricular sensing and pacing with full timing cycle interaction. This
section presents the complete timing cycle state diagram.

```
                        DDD MODE TIMING CYCLE
                    (Dual-Chamber Sensing/Pacing)

    ┌─────────────────────────────────────────────────────────────────────┐
    │                                                                     │
    │  VENTRICULAR EVENT (Sensed or Paced)                               │
    │         │                                                           │
    │         ▼                                                           │
    │  ┌─────────────┐                                                   │
    │  │ START       │                                                   │
    │  │ VA INTERVAL │ ◄── VA Interval = 60000/LRL (ms)                  │
    │  │ TIMER       │     LRL = Lower Rate Limit (bpm)                  │
    │  └──────┬──────┘                                                   │
    │         │                                                           │
    │         │ VA Timer running                                         │
    │         │                                                           │
    │         ▼                                                           │
    │  ┌─────────────┐                                                   │
    │  │ SENSE       │                                                   │
    │  │ ATRIAL?     │──── YES ───▶ ATRIAL EVENT SENSED                 │
    │  │ (During VA) │              │                                     │
    │  └──────┬──────┘              │                                     │
    │         │ NO                   │                                     │
    │         │                      ▼                                     │
    │         ▼               ┌─────────────┐                            │
    │  ┌─────────────┐        │ START       │                            │
    │  │ VA TIMER    │        │ AV INTERVAL │ ◄── AV Delay (programmed) │
    │  │ EXPIRED?    │        │ TIMER       │                            │
    │  └──────┬──────┘        └──────┬──────┘                            │
    │         │ YES                   │                                    │
    │         │                      │ AV Timer running                   │
    │         ▼                      │                                    │
    │  ┌─────────────┐               ▼                                    │
    │  │ PACE        │        ┌─────────────┐                            │
    │  │ ATRIUM      │        │ SENSE       │                            │
    │  │ (Atrial     │        │ VENTRICLE?  │──── YES ───▶ VENTRICULAR   │
    │  │  Pacing)    │        │ (During AV) │              EVENT SENSED  │
    │  └──────┬──────┘        └──────┬──────┘              │             │
    │         │                      │ NO                   │             │
    │         │                      │                      │             │
    │         │                      ▼                      │             │
    │         │               ┌─────────────┐              │             │
    │         │               │ AV TIMER    │              │             │
    │         │               │ EXPIRED?    │              │             │
    │         │               └──────┬──────┘              │             │
    │         │                      │ YES                  │             │
    │         │                      │                      │             │
    │         │                      ▼                      │             │
    │         │               ┌─────────────┐              │             │
    │         │               │ PACE        │              │             │
    │         │               │ VENTRICLE   │              │             │
    │         │               │ (Ventricular│              │             │
    │         │               │  Pacing)    │              │             │
    │         │               └──────┬──────┘              │             │
    │         │                      │                      │             │
    │         │                      └──────────┬───────────┘             │
    │         │                                 │                         │
    │         │                                 ▼                         │
    │         │                          ┌─────────────┐                 │
    │         │                          │ START       │                 │
    │         └─────────────────────────▶│ PVARP       │                 │
    │                                    │ TIMER       │                 │
    │                                    │ (Post-Vent  │                 │
    │                                    │  Atrial     │                 │
    │                                    │  Refractory │                 │
    │                                    │  Period)    │                 │
    │                                    └──────┬──────┘                 │
    │                                           │                         │
    │                                           │ PVARP expires          │
    │                                           │                         │
    │                                           ▼                         │
    │                                    ┌─────────────┐                 │
    │                                    │ ATRIAL      │                 │
    │                                    │ CHANNEL     │                 │
    │                                    │ RE-ENABLED  │                 │
    │                                    │ (Sense      │                 │
    │                                    │  Ready)     │                 │
    │                                    └─────────────┘                 │
    │                                                                     │
    └─────────────────────────────────────────────────────────────────────┘
```

### DDD Timing Parameters

| Parameter | Symbol | Range | Default | Resolution |
|-----------|--------|-------|---------|-----------|
| Lower Rate Limit | LRL | 30-120 bpm | 60 bpm | 1 bpm |
| Upper Rate Limit | URL | 100-200 bpm | 120 bpm | 1 bpm |
| AV Delay | AVD | 30-350 ms | 200 ms | 10 ms |
| Rate-Adaptive AV | RA-AVD | 150-250 ms | 200 ms | 10 ms |
| PVARP | PVARP | 150-500 ms | 300 ms | 10 ms |
| Post-Ventricular Atrial Blanking | PVAB | 50-400 ms | 300 ms | 10 ms |
| Atrial Refractory | AREF | 150-500 ms | 300 ms | 10 ms |
| Ventricular Refractory | VREF | 200-400 ms | 250 ms | 10 ms |
| Atrial Sensitivity | ASENS | 0.1-5.0 mV | 0.5 mV | 0.1 mV |
| Ventricular Sensitivity | VSENS | 0.1-5.0 mV | 2.0 mV | 0.1 mV |
| Atrial Pulse Amplitude | APAMP | 0.5-7.5 V | 3.5 V | 0.5 V |
| Atrial Pulse Width | APW | 0.05-2.0 ms | 0.4 ms | 0.05 ms |
| Ventricular Pulse Amplitude | VPAMP | 0.5-7.5 V | 3.5 V | 0.5 V |
| Ventricular Pulse Width | VPW | 0.05-2.0 ms | 0.4 ms | 0.05 ms |
| Maximum Tracking Rate | MTR | URL+10 to 200 bpm | 120 bpm | 1 bpm |
| Maximum Sensor Rate | MSR | URL+10 to 200 bpm | 120 bpm | 1 bpm |

### DDD Timing Cycle Calculations

```
VA Interval (ms) = 60000 / LRL
Example: LRL = 60 bpm → VA Interval = 1000 ms

AV Delay (effective) = AVD × (1 - k × (Rate - LRL) / (URL - LRL))
where k = rate-adaptive AV shortening factor (0.5-1.0)

Lower Rate Interval = 60000 / LRL (ms)
Upper Rate Interval = 60000 / URL (ms)

PVARP = Post-Ventricular Atrial Refractory Period
PVAB = PVARP - VREF (atrial blanking after ventricular event)

Maximum Tracking Interval = 60000 / MTR (ms)
```

---

## 2.3.6 Mode Switch State Machine

Mode switching is a critical safety and therapeutic function that
automatically changes the pacing mode in response to atrial tachyarrhythmias.
The mode switch state machine is implemented independently for the atrial
and ventricular channels.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         MODE SWITCH STATE MACHINE                           │
│                                                                             │
│                                                                             │
│   ┌──────────────┐                                                         │
│   │              │                                                         │
│   │  DDD/DDDR    │◀────────────────────────────────────┐                 │
│   │  MODE        │                                      │                 │
│   │  (Tracking)  │                                      │                 │
│   │              │                                      │                 │
│   └──────┬───────┘                                      │                 │
│          │                                               │                 │
│          │ Atrial rate > MS Rate                         │                 │
│          │ for N consecutive beats                       │                 │
│          │                                               │                 │
│          ▼                                               │                 │
│   ┌──────────────┐                                      │                 │
│   │              │                                      │                 │
│   │  MODE        │                                      │                 │
│   │  SWITCH      │                                      │                 │
│   │  DETECTED    │                                      │                 │
│   │              │                                      │                 │
│   └──────┬───────┘                                      │                 │
│          │                                               │                 │
│          │ Transition to non-tracking mode               │                 │
│          │                                               │                 │
│          ▼                                               │                 │
│   ┌──────────────┐                                      │                 │
│   │              │                                      │                 │
│   │  VVI/VVIR    │                                      │                 │
│   │  MODE        │                                      │                 │
│   │  (Inhibited) │                                      │                 │
│   │              │                                      │                 │
│   └──────┬───────┘                                      │                 │
│          │                                               │                 │
│          │ Atrial rate < MS Rate                         │                 │
│          │ for M consecutive beats                       │                 │
│          │                                               │                 │
│          ▼                                               │                 │
│   ┌──────────────┐                                      │                 │
│   │              │                                      │                 │
│   │  MODE        │                                      │                 │
│   │  SWITCH      │──────────────────────────────────────┘                 │
│   │  BACK        │  Return to DDD/DDDR after                                │
│   │              │  stable sinus rhythm detected                           │
│   └──────────────┘                                                         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Mode Switch Parameters

| Parameter | Symbol | Range | Default | Unit |
|-----------|--------|-------|---------|------|
| Mode Switch Rate | MS Rate | 100-250 | 150 | bpm |
| Detection Count | N | 3-20 | 10 | beats |
| Switch-Back Rate | SB Rate | 80-200 | 120 | bpm |
| Switch-Back Count | M | 3-20 | 10 | beats |
| Mode Switch Duration | MSD | 1-300 | 60 | minutes |
| High Rate Duration | HRD | 3-30 | 10 | minutes |

### Detection Algorithm

```
Detection = (Atrial Rate > MS Rate) for N consecutive atrial events

Where:
  Atrial Rate = 60000 / Mean Atrial Interval (bpm)
  Mean Atrial Interval = (1/K) × Σ Atrial Interval[i], i = 1..K
  K = detection window size (typically 5-10 beats)

Switch-Back = (Atrial Rate < SB Rate) for M consecutive beats
```

---

## 2.3.7 Firmware Architecture

The pacemaker firmware is organized as a real-time operating system (RTOS)
with interrupt-driven task scheduling. The firmware architecture is designed
for:

1. **Deterministic timing**: All timing-critical operations are implemented
   in hardware timers with interrupt service routines (ISRs) that execute
   in bounded time.

2. **Power efficiency**: The firmware supports multiple power modes, with
   aggressive clock gating and peripheral shutdown during idle periods.

3. **Safety**: A hardware watchdog timer monitors firmware execution and
   triggers a safe mode reset if the firmware fails to service the watchdog
   within the timeout period.

4. **Testability**: All firmware modules support built-in self-test (BIST)
   and diagnostic modes for production testing and field troubleshooting.

### Firmware Layer Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         FIRMWARE ARCHITECTURE                               │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                     APPLICATION LAYER                                │   │
│  │                                                                      │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │   │
│  │  │ Pacing   │ │ Sensing  │ │ Mode     │ │ Rate     │ │ Safety   │  │   │
│  │  │ Algorithm│ │ Algorithm│ │ Logic    │ │ Adapt    │ │ Monitor  │  │   │
│  │  │          │ │          │ │          │ │          │ │          │  │   │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘  │   │
│  │                                                                      │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │   │
│  │  │ Telemetry│ │ Diag-    │ │ Power    │ │ Self-    │ │ Parameter│  │   │
│  │  │ Protocol │ │ nostics  │ │ Mgmt     │ │ Test     │ │ Manager  │  │   │
│  │  │          │ │          │ │          │ │          │ │          │  │   │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘  │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                          │                                 │
│                                          ▼                                 │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                     MIDDLEWARE LAYER                                 │   │
│  │                                                                      │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │   │
│  │  │ Timer    │ │ Event    │ │ Register │ │ Data     │ │ Clock    │  │   │
│  │  │ Manager  │ │ Queue    │ │ File     │ │ Storage  │ │ Manager  │  │   │
│  │  │          │ │          │ │ Manager  │ │ Manager  │ │          │  │   │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘  │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                          │                                 │
│                                          ▼                                 │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                     HARDWARE ABSTRACTION LAYER (HAL)                 │   │
│  │                                                                      │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │   │
│  │  │ GPIO     │ │ Timer    │ │ ADC/DAC  │ │ SPI/I2C  │ │ UART/    │  │   │
│  │  │ Driver   │ │ Driver   │ │ Driver   │ │ Driver   │ │ RF Driver│  │   │
│  │  │          │ │          │ │          │ │          │ │          │  │   │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘  │   │
│  │                                                                      │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐               │   │
│  │  │ Clock    │ │ Power    │ │ Interrupt│ │ Watchdog │               │   │
│  │  │ Driver   │ │ Mode     │ │ Manager  │ │ Driver   │               │   │
│  │  │          │ │ Driver   │ │          │ │          │               │   │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘               │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                          │                                 │
│                                          ▼                                 │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                     HARDWARE LAYER                                   │   │
│  │                                                                      │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │   │
│  │  │ AFE      │ │ Output   │ │ Timer    │ │ RF       │ │ PMU      │  │   │
│  │  │ (Analog  │ │ Stage    │ │ Counter  │ │ Trans-   │ │ (Power   │  │   │
│  │  │  Front   │ │ (Pacing) │ │ (Timer0) │ │ ceiver   │ │  Mgmt)   │  │   │
│  │  │  End)    │ │          │ │          │ │          │ │          │  │   │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘  │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Interrupt Structure

The firmware uses a priority-based interrupt structure. Higher-priority
interrupts can preempt lower-priority ISRs, ensuring that time-critical
operations (sensing, pacing) are never delayed by non-critical operations
(telemetry, diagnostics).

| Priority | ISR | Latency | Duration | Trigger |
|----------|-----|---------|----------|---------|
| 1 (Highest) | NMI (Safety) | < 1 µs | < 5 µs | Hardware fault |
| 2 | Timer0 (Pacing) | < 2 µs | < 10 µs | Timer match |
| 3 | Comparator (Sense) | < 5 µs | < 20 µs | Threshold crossing |
| 4 | Timer1 (Watchdog) | < 5 µs | < 5 µs | Watchdog timeout |
| 5 | SPI (Telemetry) | < 10 µs | < 50 µs | SPI transfer complete |
| 6 | ADC (Battery) | < 10 µs | < 100 µs | ADC conversion complete |
| 7 | GPIO (Magnet) | < 20 µs | < 10 µs | Hall sensor change |
| 8 (Lowest) | Timer2 (Diagnostics) | < 50 µs | < 500 µs | Diagnostic timer |

### Task Scheduling

The firmware uses a cooperative scheduling model with the following tasks:

| Task | Period | Priority | State | Description |
|------|--------|----------|-------|-------------|
| Sense Task | 1 ms | High | Running/Sleeping | Processes sense events |
| Pace Task | On-demand | High | Running/Sleeping | Executes pacing output |
| Timing Task | 1 ms | High | Running/Sleeping | Updates timing counters |
| Mode Task | On-demand | High | Running/Sleeping | Evaluates mode transitions |
| Sensor Task | 100 ms | Medium | Running/Sleeping | Processes sensor inputs |
| Telemetry Task | 10 ms | Medium | Running/Sleeping | Handles RF communication |
| Diagnostics Task | 1 s | Low | Running/Sleeping | Collects diagnostic data |
| Self-Test Task | 60 s | Low | Running/Sleeping | Periodic self-test |
| Power Task | 10 s | Low | Running/Sleeping | Manages power modes |
| Safety Task | 100 ms | High | Always running | Monitors safety parameters |

---

## 2.3.8 Data Flow Architecture

The data flow architecture defines how data moves between the various
subsystems of the pacemaker. Data flows are categorized as:

1. **Sensing data flow**: Intracardiac signals from electrodes to the
   digital controller for event detection.
2. **Pacing data flow**: Pacing parameters from the register file to the
   output stage for pulse delivery.
3. **Timing data flow**: Timer counter values exchanged between the timer
   block and the mode logic.
4. **Telemetry data flow**: Bidirectional data transfer between the digital
   controller and the RF transceiver.
5. **Diagnostic data flow**: Event data from all subsystems to the data
   storage block.
6. **Power data flow**: Battery status information from the PMU to the
   digital controller.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         DATA FLOW ARCHITECTURE                              │
│                                                                             │
│                                                                             │
│  ELECTRODE ───▶ AFE ───▶ SENSE DATA ───▶ DIGITAL ───▶ EVENT DATA          │
│  (Tip/Ring)    (Analog)   (Filtered)     CONTROLLER   (Timestamped)        │
│                                           (DFC)                            │
│                                             │                              │
│                                             │ PACE COMMAND                  │
│                                             ▼                              │
│  ELECTRODE ◀── OUTPUT ◀── PACE DATA ◀────── DFC                           │
│  (Tip/Ring)    STAGE      (Amplitude,      (Controller)                    │
│               (Analog)     Width)                                         │
│                                                                             │
│  TIMER ───────▶ DFC ───────▶ MODE LOGIC ───▶ DFC ───────▶ PACE/INHIBIT   │
│  BLOCK         (Counter)    (State Machine)  (Decision)                    │
│                                                                             │
│  RF TRANSCEIVER ◀──▶ DFC ◀──▶ EEPROM ◀──▶ SRAM                           │
│  (Telemetry)     (Protocol)  (Persistent)  (Working)                       │
│                                                                             │
│  PMU ────────▶ DFC ────────▶ TELEM ◀────── EXTERNAL                       │
│  (Battery)     (Monitor)    (Alert)        PROGRAMMER                      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2.3.9 Hierarchical Interrupt Model

The interrupt model ensures that all time-critical operations are handled
with deterministic latency. The model is organized in three tiers:

### Tier 1: Hardware Interrupts (Deterministic, < 10 µs)

These interrupts are handled directly by the hardware without firmware
intervention:

- **Comparator edge**: The AFE comparator generates a digital edge when a
  cardiac event is detected. This edge directly triggers the sense indicator
  output to the digital timer block.
- **Timer match**: Hardware timer match events generate pacing trigger signals
  directly to the output stage, bypassing firmware for minimum latency.
- **Watchdog timeout**: The hardware watchdog generates a non-maskable
  interrupt (NMI) that forces a system reset.

### Tier 2: Fast ISRs (Bounded, < 50 µs)

These interrupts are handled by short firmware ISRs:

- **Sense ISR**: Processes the sense indicator, updates the timing state,
  and generates a pace command if needed.
- **Timer ISR**: Updates the timing counters, checks for interval expiry,
  and schedules the next pacing event.
- **Telemetry ISR**: Handles the RF transceiver data transfer, buffering
  incoming and outgoing data.

### Tier 3: Deferred Tasks (Unbounded, < 10 ms)

These tasks are processed in the main firmware loop:

- **Diagnostics task**: Collects and stores diagnostic data.
- **Self-test task**: Runs periodic integrity checks.
- **Power management task**: Evaluates power mode transitions.
- **Parameter update task**: Applies parameter changes from the register file.

---

## 2.3.10 Safety Architecture

The safety architecture implements defense-in-depth principles, with
independent hardware and software safety monitors that can each independently
place the pacemaker into a safe mode.

### Hardware Safety Monitor

The hardware safety monitor is implemented as a dedicated digital block
that operates independently of the firmware. It monitors:

1. **Pacing rate**: If the pacing rate exceeds the programmed upper rate
   limit for more than 3 consecutive beats, the hardware monitor forces
   asynchronous pacing at the backup rate.

2. **Maximum pulse width**: If the pacing pulse width exceeds the maximum
   allowed value (programmable, typically 2.0 ms), the hardware monitor
   truncates the pulse and generates an alert.

3. **Maximum pulse amplitude**: If the pacing voltage exceeds the maximum
   allowed value (programmable, typically 7.5 V), the hardware monitor
   limits the output and generates an alert.

4. **Lead impedance**: If the measured lead impedance is outside the
   acceptable range (< 100 Ω or > 2000 Ω), the hardware monitor generates
   an alert and optionally disables pacing on the affected channel.

5. **Battery voltage**: If the battery voltage falls below the critical
   threshold (2.2 V), the hardware monitor disables telemetry and reduces
   pacing output to minimum to extend battery life.

### Firmware Safety Monitor

The firmware safety monitor runs as a high-priority task and monitors:

1. **Timing integrity**: Verifies that all timing counters are incrementing
   correctly and that the pacing intervals are within acceptable bounds.

2. **Memory integrity**: Periodically checks SRAM and EEPROM checksums to
   detect data corruption.

3. **Register file integrity**: Verifies that all programmable parameters
   have valid values and have not been corrupted.

4. **Sensor integrity**: Checks that sensor readings are within expected
   ranges and that the sensor data is consistent with expected physiological
   behavior.

5. **Communication integrity**: Verifies that all telemetry transactions
   complete successfully and that no data corruption has occurred.

### Safe Mode Behavior

When either safety monitor detects a fault, the pacemaker enters safe mode:

1. Mode is set to VVI (ventricular demand pacing).
2. Pacing rate is set to 60 bpm (asynchronous backup).
3. Pacing output is set to maximum amplitude and pulse width (to ensure
   capture despite unknown lead conditions).
4. Telemetry is disabled (to prevent interference with pacing).
5. Diagnostics are suspended (to minimize power and processing).
6. A fault code is stored in non-volatile memory for later retrieval.
7. The device remains in safe mode until a programmer re-enables normal
   operation or the fault condition is cleared.

---

## 2.3.11 Summary

The functional architecture of the implantable cardiac pacemaker is a
hierarchical, interrupt-driven system designed for:

1. **Real-time deterministic operation**: All timing-critical functions are
   implemented in hardware or fast ISRs with bounded execution times.

2. **Power efficiency**: The firmware supports multiple power modes with
   aggressive clock gating and peripheral shutdown.

3. **Safety**: Dual safety monitors (hardware and firmware) ensure that the
   pacemaker always operates in a safe state, even under fault conditions.

4. **Flexibility**: The firmware architecture supports multiple pacing modes,
   rate adaptation algorithms, and diagnostic features through a modular
   design.

5. **Testability**: Built-in self-test and diagnostic capabilities enable
   comprehensive production testing and field troubleshooting.

The state machine models presented in this chapter provide the complete
specification for the pacemaker's functional behavior, from the top-level
system states down to the interrupt-driven firmware service routines. These
models serve as the reference for firmware implementation and verification.
