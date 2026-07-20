# Functional Architecture

## 2.1.3 iPACE-CHIP Functional Architecture

### 2.1.3.1 Functional Decomposition Hierarchy

The iPACE-CHIP functional architecture is decomposed into five major subsystems,
each with clearly defined interfaces and responsibilities. The decomposition follows
a top-down approach from system level to leaf-level functions.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    iPACE-CHIP FUNCTIONAL DECOMPOSITION                       │
│                                                                             │
│                         ┌─────────────────────┐                             │
│                         │   iPACE-CHIP        │                             │
│                         │   SYSTEM            │                             │
│                         └──────────┬──────────┘                             │
│                                    │                                        │
│          ┌────────────┬────────────┼────────────┬────────────┐             │
│          │            │            │            │            │             │
│          ▼            ▼            ▼            ▼            ▼             │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│  │ F1:      │ │ F2:      │ │ F3:      │ │ F4:      │ │ F5:      │       │
│  │ SENSING  │ │ PACING   │ │ POWER    │ │ TELEMETRY│ │ CONTROL  │       │
│  │          │ │          │ │ MGMT     │ │          │ │ & TIMING │       │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘       │
│       │            │            │            │            │               │
│   ┌───┴───┐    ┌───┴───┐    ┌───┴───┐    ┌───┴───┐    ┌───┴───┐         │
│   │       │    │       │    │       │    │       │    │       │         │
│   ▼       ▼    ▼       ▼    ▼       ▼    ▼       ▼    ▼       ▼         │
│ ┌────┐ ┌────┐┌────┐ ┌────┐┌────┐ ┌────┐┌────┐ ┌────┐┌────┐ ┌────┐     │
│ │F1.1│ │F1.2││F2.1│ │F2.2││F3.1│ │F3.2││F4.1│ │F4.2││F5.1│ │F5.2│     │
│ │    │ │    ││    │ │    ││    │ │    ││    │ │    ││    │ │    │     │
│ └────┘ └────┘└────┘ └────┘└────┘ └────┘└────┘ └────┘└────┘ └────┘     │
│   │       │    │       │    │       │    │       │    │       │         │
│   ▼       ▼    ▼       ▼    ▼       ▼    ▼       ▼    ▼       ▼         │
│ ┌────┐ ┌────┐┌────┐ ┌────┐┌────┐ ┌────┐┌────┐ ┌────┐┌────┐ ┌────┐     │
│ │F1.1│ │F1.2││F2.1│ │F2.2││F3.1│ │F3.2││F4.1│ │F4.2││F5.1│ │F5.2│     │
│ │.1  │ │.1  ││.1  │ │.1  ││.1  │ │.1  ││.1  │ │.1  ││.1  │ │.1  │     │
│ └────┘ └────┘└────┘ └────┘└────┘ └────┘└────┘ └────┘└────┘ └────┘     │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### Detailed Function Tree

```
F1: SENSING SUBSYSTEM
├── F1.1: Intrinsic Signal Detection
│   ├── F1.1.1: P-wave detection (atrial)
│   │   ├── F1.1.1.1: Bandpass filtering (0.5–50 Hz)
│   │   ├── F1.1.1.2: Amplification (40–80 dB)
│   │   ├── F1.1.1.3: Threshold comparison
│   │   └── F1.1.1.4: Sensitivity auto-adjustment
│   ├── F1.1.2: R-wave detection (ventricular)
│   │   ├── F1.1.2.1: Bandpass filtering (10–100 Hz)
│   │   ├── F1.1.2.2: Amplification (40–80 dB)
│   │   ├── F1.1.2.3: Threshold comparison
│   │   └── F1.1.2.4: Dynamic threshold tracking
│   ├── F1.1.3: T-wave discrimination
│   │   ├── F1.1.3.1: T-wave morphology analysis
│   │   ├── F1.1.3.2: T-wave amplitude criterion
│   │   └── F1.1.3.3: T-wave timing criterion
│   └── F1.1.4: Far-field rejection
│       ├── F1.1.4.1: Common-mode rejection (CMRR)
│       ├── F1.1.4.2: Notch filtering (50/60 Hz)
│       └── F1.1.4.3: Morphology-based rejection
├── F1.2: Signal Conditioning
│   ├── F1.2.1: Impedance measurement
│   │   ├── F1.2.1.1: Lead impedance (DC pulse method)
│   │   ├── F1.2.1.2: Contact impedance monitoring
│   │   └── F1.2.1.3: Impedance trending
│   ├── F1.2.2: Electrogram (EGM) processing
│   │   ├── F1.2.2.1: Near-field EGM
│   │   ├── F1.2.2.2: Far-field EGM
│   │   └── F1.2.2.3: EGM storage/compression
│   └── F1.2.3: Noise detection
│       ├── F1.2.3.1: Muscle noise (EMG)
│       ├── F1.2.3.2: Lead noise (discontinuity)
│       ├── F1.2.3.3: Electromagnetic interference (EMI)
│       └── F1.2.3.4: Noise response algorithm

F2: PACING SUBSYSTEM
├── F2.1: Pulse Generation
│   ├── F2.1.1: Voltage-controlled current source
│   │   ├── F2.1.1.1: Output DAC (8-bit)
│   │   ├── F2.1.1.2: Compliance voltage limiter
│   │   └── F2.1.1.3: Output switch matrix
│   ├── F2.1.2: Pulse timing control
│   │   ├── F2.1.2.1: Pulse width control (50µs–1.5ms)
│   │   ├── F2.1.2.2: Pulse amplitude control (0.5–10V)
│   │   └── F2.1.2.3: Simultaneous/b sequential pacing
│   └── F2.1.3: Charge balancing
│       ├── F2.1.3.1: Automatic charge balance
│       ├── F2.1.3.2: Post-pace polarization removal
│       └── F2.1.3.3: Charge balance verification
├── F2.2: Output Safety
│   ├── F2.2.1: Overvoltage protection
│   │   ├── F2.2.1.1: Output voltage limiter
│   │   └── F2.2.1.2: Back-EMF clamp
│   ├── F2.2.2: Output energy limiting
│   │   ├── F2.2.2.1: Maximum energy per pulse
│   │   └── F2.2.2.2: Maximum average power
│   └── F2.2.3: Lead protection
│       ├── F2.2.3.1: DC current blocking
│       └── F2.2.3.2: ESD protection (8kV)

F3: POWER MANAGEMENT SUBSYSTEM
├── F3.1: Battery Management
│   ├── F3.1.1: Voltage monitoring
│   │   ├── F3.1.1.1: Real-time voltage sensing
│   │   ├── F3.1.1.2: End-of-life detection
│   │   └── F3.1.1.3: Low-battery warning
│   ├── F3.1.2: Current monitoring
│   │   ├── F3.1.2.1: Average current measurement
│   │   └── F3.1.2.2: Peak current detection
│   └── F3.1.3: Temperature monitoring
│       ├── F3.1.3.1: Die temperature sensing
│       └── F3.1.3.2: Thermal shutdown (>45°C)
├── F3.2: Voltage Regulation
│   ├── F3.2.1: DC-DC converter
│   │   ├── F3.2.1.1: Buck converter (3.0V → 1.8V)
│   │   ├── F3.2.1.2: Efficiency optimization
│   │   └── F3.2.1.3: Output filtering
│   ├── F3.2.2: LDO regulators
│   │   ├── F3.2.2.1: Analog supply (1.8V)
│   │   ├── F3.2.2.2: Digital core (1.2V)
│   │   ├── F3.2.2.3: I/O supply (1.8V/3.0V)
│   │   └── F3.2.2.4: RF supply (1.8V)
│   └── F3.2.3: Power sequencing
│       ├── F3.2.3.1: Start-up sequence
│       ├── F3.2.3.2: Power-on reset (POR)
│       └── F3.2.3.3: Brown-out detection (BOR)

F4: TELEMETRY SUBSYSTEM
├── F4.1: RF Communication
│   ├── F4.1.1: Transmitter
│   │   ├── F4.1.1.1: MICS band TX (402–405 MHz)
│   │   ├── F4.1.1.2: ISM band TX (2.4 GHz)
│   │   ├── F4.1.1.3: FSK/ASK modulation
│   │   └── F4.1.1.4: Power amplifier (PA)
│   ├── F4.1.2: Receiver
│   │   ├── F4.1.2.1: MICS band RX
│   │   ├── F4.1.2.2: ISM band RX
│   │   ├── F4.1.2.3: Low-noise amplifier (LNA)
│   │   └── F4.1.2.4: FSK/ASK demodulation
│   └── F4.1.3: Wake-up receiver
│       ├── F4.1.3.1: Low-power always-on detector
│       └── F4.1.3.2: Wake-up signal recognition
├── F4.2: Protocol Layer
│   ├── F4.2.1: Packet management
│   │   ├── F4.2.1.1: Packet framing
│   │   ├── F4.2.1.2: CRC-16 generation/check
│   │   └── F4.2.1.3: Retransmission logic
│   ├── F4.2.2: Data encoding
│   │   ├── F4.2.2.1: Manchester encoding
│   │   └── F4.2.2.2: Bi-phase encoding
│   └── F4.2.3: Command processing
│       ├── F4.2.3.1: Command decoder
│       ├── F4.2.3.2: Response formatter
│       └── F4.2.3.3: Error handling

F5: CONTROL & TIMING SUBSYSTEM
├── F5.1: Timing Engine
│   ├── F5.1.1: Interval counters
│   │   ├── F5.1.1.1: Lower rate interval (LRI)
│   │   ├── F5.1.1.2: AV delay timer
│   │   ├── F5.1.1.3: VA interval timer
│   │   ├── F5.1.1.4: PVARP timer
│   │   ├── F5.1.1.5: Refractory period timer
│   │   └── F5.1.1.6: Blanking period timer
│   ├── F5.1.2: Rate management
│   │   ├── F5.1.2.1: Lower rate limit (LRL)
│   │   ├── F5.1.2.2: Upper rate limit (URL)
│   │   ├── F5.1.2.3: Sensor-indicated rate (SIR)
│   │   └── F5.1.2.4: Rate smoothing algorithm
│   └── F5.1.3: Sensor processing
│       ├── F5.1.3.1: Activity sensor (accelerometer)
│       ├── F5.1.3.2: Sensor signal filtering
│       ├── F5.1.3.3: Sensor rate response curve
│       └── F5.1.3.4: Sensor rate blending
├── F5.2: Mode State Machine
│   ├── F5.2.1: Mode definition
│   │   ├── F5.2.1.1: ODO (monitoring only)
│   │   ├── F5.2.1.2: AAI (atrial demand)
│   │   ├── F5.2.1.3: VVI (ventricular demand)
│   │   ├── F5.2.1.4: DDD (dual demand)
│   │   ├── F5.2.1.5: DDDR (dual demand + rate response)
│   │   └── F5.2.1.6: VVIR (ventricular + rate response)
│   ├── F5.2.2: Mode transitions
│   │   ├── F5.2.2.1: Safe mode fallback
│   │   ├── F5.2.2.2: Mode switch (AF response)
│   │   └── F5.2.2.3: Magnet mode
│   └── F5.2.3: Safety monitoring
│       ├── F5.2.3.1: Watchdog timer
│       ├── F5.2.3.2: Escape interval monitoring
│       ├── F5.2.3.3: Fault detection
│       └── F5.2.3.4: Emergency reset
```

### 2.1.3.2 System State Machine

The iPACE-CHIP operates in five primary states with well-defined transitions
triggered by clinical events, timer expirations, or programmer commands.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SYSTEM STATE MACHINE — Top Level                          │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                                                                      │   │
│  │         ┌──────────────┐                                            │   │
│  │   ┌─────│   HIBERNATE   │◄──── Battery < 2.5V                      │   │
│  │   │     │   (SRAM off,  │◄──── Programmer command                   │   │
│  │   │     │    RTC on)    │◄──── Inactivity > 24h                     │   │
│  │   │     └──────┬────────┘                                            │   │
│  │   │            │ Magnet / RF wake-up / Timer                         │   │
│  │   │            ▼                                                      │   │
│  │   │     ┌──────────────┐                                            │   │
│  │   │     │    SLEEP      │◄──── No sensed/paced event                │   │
│  │   │     │   (Low-power  │◄──── Sensor rate < LRL                    │   │
│  │   │     │    mode)      │                                            │   │
│  │   │     └──────┬────────┘                                            │   │
│  │   │            │ Sensed event / Timer expiry / Wake-up               │   │
│  │   │            ▼                                                      │   │
│  │   │     ┌──────────────┐                                            │   │
│  │   │     │   ACTIVE      │◄──── Normal operation                     │   │
│  │   │     │  (Sensing +   │◄──── Intrinsic rhythm detected            │   │
│  │   │     │   Pacing)     │                                            │   │
│  │   │     └──┬───────┬────┘                                            │   │
│  │   │        │       │                                                  │   │
│  │   │        │       │ Arrhythmia detected                             │   │
│  │   │        │       ▼                                                  │   │
│  │   │        │  ┌──────────────┐                                       │   │
│  │   │        │  │  THERAPY     │                                       │   │
│  │   │        │  │  (Anti-tachy │                                       │   │
│  │   │        │  │   pacing /   │                                       │   │
│  │   │        │  │   shock)     │                                       │   │
│  │   │        │  └──────┬───────┘                                       │   │
│  │   │        │         │ Therapy complete / Abort                      │   │
│  │   │        │         ▼                                                │   │
│  │   │        │    ┌──────────────┐                                     │   │
│  │   │        └───▶│   RECOVERY    │                                     │   │
│  │   │             │  (Post-       │                                     │   │
│  │   │             │   therapy)    │                                     │   │
│  │   │             └──────┬────────┘                                     │   │
│  │   │                    │ Stable rhythm confirmed                      │   │
│  │   │                    └──────────┐                                   │   │
│  │   │                               │                                   │   │
│  │   └───────────────────────────────┘                                   │   │
│  │                                                                      │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  TRANSITIONS:                                                              │
│  ─────────────                                                             │
│  HIBERNATE → SLEEP:     Magnet event, RF wake-up signal, RTC alarm        │
│  SLEEP → ACTIVE:        Sensed cardiac event, escape interval timeout,    │
│                         sensor threshold crossed, RF command              │
│  ACTIVE → SLEEP:        No events for N cycles, sensor rate < LRL        │
│  ACTIVE → THERAPY:      VT/VF detected (3/8 or 4/8 criterion)           │
│  THERAPY → RECOVERY:    Therapy delivered (ATP/shock) or aborted          │
│  RECOVERY → ACTIVE:     Stable rhythm for M consecutive cycles           │
│  Any → HIBERNATE:       Battery < 2.5V, programmer command, fault        │
│  Any → FAULT:           Hardware/software fault detected                  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.1.3.3 Pacing Mode State Machine (DDD Mode)

The DDD mode state machine is the most complex operating mode, managing both
atrial and ventricular sensing/pacing with AV synchronization.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    DDD MODE STATE MACHINE                                    │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                                                                      │   │
│  │                    ┌────────────────────┐                            │   │
│  │    ┌──────────────▶│    IDLE            │◀──────────────────┐       │   │
│  │    │               │  (Waiting for VA   │                   │       │   │
│  │    │               │   interval)        │                   │       │   │
│  │    │               └───────┬────────────┘                   │       │   │
│  │    │                       │                                │       │   │
│  │    │              VA interval expires                       │       │   │
│  │    │              OR Atrial sensed                          │       │   │
│  │    │                       │                                │       │   │
│  │    │                       ▼                                │       │   │
│  │    │               ┌────────────────────┐                   │       │   │
│  │    │               │  ATRIAL            │                   │       │   │
│  │    │               │  PACING / SENSING  │                   │       │   │
│  │    │               │  (AV delay running)│                   │       │   │
│  │    │               └───────┬────────────┘                   │       │   │
│  │    │                       │                                │       │   │
│  │    │         ┌─────────────┼─────────────┐                  │       │   │
│  │    │         │             │             │                  │       │   │
│  │    │    AV delay      Ventricular   Atrial                 │       │   │
│  │    │    expires       sensed        sensed                 │       │   │
│  │    │         │        (intrinsic)  (during                 │       │   │
│  │    │         │             │        AV delay)              │       │   │
│  │    │         │             │             │                  │       │   │
│  │    │         ▼             ▼             ▼                  │       │   │
│  │    │  ┌────────────┐┌────────────┐┌────────────┐           │       │   │
│  │    │  │ VENTRICULAR││ VENTRICULAR││ VENTRICULAR│           │       │   │
│  │    │  │ PACING     ││ INHIBIT    ││ PACING     │           │       │   │
│  │    │  │ (No intrinsic││ (Sense    ││ (Non-      │           │       │   │
│  │    │  │  detected) ││  event)    ││  physiolog)│           │       │   │
│  │    │  └──────┬─────┘└──────┬─────┘└──────┬─────┘           │       │   │
│  │    │         │             │             │                  │       │   │
│  │    │         └─────────────┼─────────────┘                  │       │   │
│  │    │                       │                                │       │   │
│  │    │                       ▼                                │       │   │
│  │    │               ┌────────────────────┐                   │       │   │
│  │    │               │  VENTRICULAR       │                   │       │   │
│  │    │               │  EVENT             │                   │       │   │
│  │    │               │  (PVARP running)   │                   │       │   │
│  │    │               └───────┬────────────┘                   │       │   │
│  │    │                       │                                │       │   │
│  │    │              PVARP expires                             │       │   │
│  │    │              (then VA interval)                        │       │   │
│  │    │                       │                                │       │   │
│  │    └───────────────────────┘                                │       │   │
│  │                                                              │       │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  SPECIAL CONDITIONS:                                                       │
│  ──────────────────                                                        │
│  • If Atrial sensed during PVARP: Counted as far-field (not tracked)      │
│  • If Ventricular sensed during AV delay: AV delay reset, pace inhibited   │
│  • If Atrial sensed during AV delay (non-physiologic): Trigger VP         │
│  • Mode switching: If AF detected, switch to VVI/R at URL                 │
│  • Safety pacing: If no sensed event within LRI, deliver pace pulse       │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.1.3.4 Timing Cycle Diagram (DDD Mode)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    DDD MODE TIMING CYCLES                                    │
│                                                                             │
│  Intrinsic Atrial ────┐                                                    │
│  (P-wave)             │                                                    │
│                       ▼                                                    │
│  Atrial ────────┐    ┌──┐    ┌──┐    ┌──┐    ┌──┐    ┌──┐               │
│  Channel:       └────┤AS│────┤AP│────┤AP│────┤AS│────┤AP│────            │
│                      └──┘    └──┘    └──┘    └──┘    └──┘               │
│                       │     │     │     │     │                           │
│                       │  ┌──┴──┐  │  ┌──┴──┐  │                         │
│                       │  │AV   │  │  │AV   │  │                         │
│                       │  │Delay│  │  │Delay│  │                         │
│                       │  └──┬──┘  │  └──┬──┘  │                         │
│                       │     │     │     │     │                         │
│  Intrinsic Vent. ─────┼─────┼─┐   │  ┌──┼─────┼─┐                       │
│  (R-wave)             │     │ │   │  │  │     │ │                       │
│                       │     │ │   │  │  │     │ │                       │
│  Ventricular ────┐    │  ┌──┘ │   │  │  │  ┌──┘ │   ┌──┐               │
│  Channel:       └────┤  │VS  │   ├──┘  │  │VS  │   │VP│               │
│                      │  └──┬──┘   │     │  └──┬──┘   └──┘               │
│                       │     │     │     │     │                           │
│                       │  ┌──┴──┐  │  ┌──┴──┐  │                         │
│                       │  │PVARP│  │  │PVARP│  │                         │
│                       │  └──┬──┘  │  └──┬──┘  │                         │
│                       │     │     │     │     │                         │
│  Atrial ──────────────┼─────┼─────┼─────┼─────┼────────────             │
│  Refractory:         │     │     │     │     │                         │
│                      └─────┴─────┴─────┴─────┴────────────             │
│                                                                             │
│  LEGEND:                                                                   │
│  AS = Atrial Sense    AP = Atrial Pace    VS = Ventricular Sense         │
│  VP = Ventricular Pace                                                   │
│                                                                             │
│  CRITICAL TIMING INTERVALS:                                                │
│  ┌──────────────────────────────────────────────────────────────────┐     │
│  │  Lower Rate Interval (LRI):  860ms (70 ppm)                    │     │
│  │  AV Delay:                   200ms (programmable 30–350ms)      │     │
│  │  VA Interval:                LRI - AV Delay = 660ms            │     │
│  │  PVARP:                      300ms (programmable 150–500ms)    │     │
│  │  Post-Vent. Atrial Blanking: 100ms (programmable 50–400ms)     │     │
│  │  Upper Rate Limit:           120 bpm (500ms interval)          │     │
│  │  Sensor Indicated Rate:      60–120 bpm (sensor driven)        │     │
│  │  Total Cycle:                LRI = 860ms                        │     │
│  └──────────────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.1.3.5 Firmware Architecture

The firmware is organized into a layered architecture with real-time scheduling,
ensuring deterministic behavior for safety-critical pacing functions.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    FIRMWARE ARCHITECTURE — Layered Model                      │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │  LAYER 5: APPLICATION LOGIC                                         │   │
│  │  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐      │   │
│  │  │ Pacing     │ │ Sensing    │ │ Arrhythmia │ │ Diagnostics│      │   │
│  │  │ Algorithm  │ │ Algorithm  │ │ Detection  │ │ & Logging  │      │   │
│  │  │ (DDD/VVI/  │ │ (Auto-     │ │ (VT/VF/    │ │ (EGM store,│      │   │
│  │  │  AAI)      │ │  Sense)    │ │  AF)       │ │  counters) │      │   │
│  │  └────────────┘ └────────────┘ └────────────┘ └────────────┘      │   │
│  └───────────────────────────────┬──────────────────────────────────────┘   │
│                                  │                                          │
│  ┌───────────────────────────────▼──────────────────────────────────────┐   │
│  │  LAYER 4: MIDDLEWARE                                                 │   │
│  │  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐      │   │
│  │  │ Parameter  │ │ State      │ │ Timer      │ │ Safety     │      │   │
│  │  │ Manager    │ │ Manager    │ │ Service    │ │ Monitor    │      │   │
│  │  │ (EEPROM    │ │ (Mode      │ │ (Interval  │ │ (Watchdog, │      │   │
│  │  │  read/write)│ │ transitions│ │  counting) │ │  BOR)      │      │   │
│  │  └────────────┘ └────────────┘ └────────────┘ └────────────┘      │   │
│  └───────────────────────────────┬──────────────────────────────────────┘   │
│                                  │                                          │
│  ┌───────────────────────────────▼──────────────────────────────────────┐   │
│  │  LAYER 3: OS / SCHEDULER                                             │   │
│  │  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐      │   │
│  │  │ Task       │ │ Interrupt  │ │ Power      │ │ Clock      │      │   │
│  │  │ Scheduler  │ │ Controller │ │ Manager    │ │ Manager    │      │   │
│  │  │ (Priority  │ │ (NVIC)     │ │ (Sleep/    │ │ (Clock     │      │   │
│  │  │  based)    │ │            │ │  Hibernate)│ │  gating)   │      │   │
│  │  └────────────┘ └────────────┘ └────────────┘ └────────────┘      │   │
│  └───────────────────────────────┬──────────────────────────────────────┘   │
│                                  │                                          │
│  ┌───────────────────────────────▼──────────────────────────────────────┐   │
│  │  LAYER 2: HAL (Hardware Abstraction Layer)                           │   │
│  │  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐      │   │
│  │  │ AFE HAL    │ │ Output HAL │ │ Telemetry  │ │ Power HAL  │      │   │
│  │  │ (ADC, LNA, │ │ (DAC, PWM, │ │ HAL (RF,   │ │ (DC-DC,    │      │   │
│  │  │  Filter)   │ │  Switch)   │ │  Coil)     │ │  LDO, POR) │      │   │
│  │  └────────────┘ └────────────┘ └────────────┘ └────────────┘      │   │
│  └───────────────────────────────┬──────────────────────────────────────┘   │
│                                  │                                          │
│  ┌───────────────────────────────▼──────────────────────────────────────┐   │
│  │  LAYER 1: DRIVERS                                                    │   │
│  │  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐      │   │
│  │  │ SPI Driver │ │ I2C Driver │ │ UART Driver│ │ Timer Drv  │      │   │
│  │  │            │ │            │ │            │ │            │      │   │
│  │  └────────────┘ └────────────┘ └────────────┘ └────────────┘      │   │
│  │  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐      │   │
│  │  │ GPIO Driver│ │ ADC Driver │ │ Watchdog   │ │ Flash/     │      │   │
│  │  │            │ │            │ │ Driver     │ │ EEPROM Drv │      │   │
│  │  └────────────┘ └────────────┘ └────────────┘ └────────────┘      │   │
│  └───────────────────────────────┬──────────────────────────────────────┘   │
│                                  │                                          │
│  ┌───────────────────────────────▼──────────────────────────────────────┐   │
│  │  LAYER 0: BSP (Board Support Package)                                │   │
│  │  ┌──────────────────────────────────────────────────────────────┐   │   │
│  │  │  Register definitions, memory maps, interrupt vectors,      │   │   │
│  │  │  startup code, vector table, linker scripts                 │   │   │
│  │  └──────────────────────────────────────────────────────────────┘   │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  STACK SIZE: 256 bytes (main) / 128 bytes (interrupt)                      │
│  HEAP SIZE: 0 bytes (static allocation only)                               │
│  TOTAL CODE: <32 KB (Flash)                                                │
│  TOTAL RAM: <4 KB (SRAM)                                                   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.1.3.6 Task Scheduling and Priority

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    REAL-TIME TASK SCHEDULE                                   │
│                                                                             │
│  INTERRUPT PRIORITY LEVELS (NVIC — 4 bits, 0=highest)                     │
│  ┌──────┬────────────────────────┬──────────┬────────────────────┐        │
│  │ PRI  │ Source                 │ Latency  │ Handler            │        │
│  ├──────┼────────────────────────┼──────────┼────────────────────┤        │
│  │  0   │ Hardware Reset         │ 0 cycles │ Reset_Handler      │        │
│  │  1   │ NMI (Non-Maskable)     │ 2 cycles │ NMI_Handler        │        │
│  │  2   │ Hard Fault             │ 3 cycles │ HardFault_Handler  │        │
│  │  3   │ Timer (Pacing)         │ 4 cycles │ TIMER0_IRQHandler  │        │
│  │  4   │ ADC (Sensing)          │ 4 cycles │ ADC_IRQHandler     │        │
│  │  5   │ Telemetry RX           │ 6 cycles │ UART_IRQHandler    │        │
│  │  6   │ Telemetry TX           │ 6 cycles │ UART_IRQHandler    │        │
│  │  7   │ Watchdog                │ 8 cycles │ WDT_IRQHandler     │        │
│  │  8   │ Brown-out              │ 8 cycles │ BOR_IRQHandler     │        │
│  │  9   │ SPI (EEPROM)           │ 10 cycles│ SPI_IRQHandler     │        │
│  │ 10   │ GPIO (Magnet)          │ 10 cycles│ GPIO_IRQHandler    │        │
│  │ 11   │ Timer (General)        │ 12 cycles│ TIMER1_IRQHandler  │        │
│  │ 12   │ Sensor (Accel)         │ 12 cycles│ ADC1_IRQHandler    │        │
│  │ 13   │ Telemetry Wake-up      │ 14 cycles│ EXT_INT_IRQHandler │        │
│  │ 14   │ Software Trigger       │ 16 cycles│ SVC_Handler        │        │
│  │ 15   │ SysTick                │ 16 cycles│ SysTick_Handler    │        │
│  └──────┴────────────────────────┴──────────┴────────────────────┘        │
│                                                                             │
│  TASK EXECUTION TIMELINE (1ms time slice)                                  │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │ 0ms       1ms       2ms       3ms       4ms       5ms       6ms   │  │
│  │ │         │         │         │         │         │         │     │  │
│  │ ├─Sense──▶├─Sense──▶├─Sense──▶├─Sense──▶├─Sense──▶├─Sense──▶│     │  │
│  │ │         │         │         │         │         │         │     │  │
│  │ ├──Pace──▶├─────────├──Pace──▶├─────────├──Pace──▶├─────────│     │  │
│  │ │         │         │         │         │         │         │     │  │
│  │ ├──TLM──▶├─────────├─────────├──TLM──▶├─────────├─────────│     │  │
│  │ │         │         │         │         │         │         │     │  │
│  │ ├──Diag─▶├─────────├─────────├─────────├──Diag─▶├─────────│     │  │
│  │ │         │         │         │         │         │         │     │  │
│  │ ├──PM──▶ ├──────────├─────────├─────────├─────────├──PM────▶│     │  │
│  │ │         │         │         │         │         │         │     │  │
│  │ ├─Sleep──├─Sleep──▶├─Sleep──▶├─Sleep──▶├─Sleep──▶├─Sleep─▶│     │  │
│  │ │         │         │         │         │         │         │     │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  SENSE: ADC sampling + digital filtering + threshold comparison            │
│  PACE:  Output pulse generation (when required)                           │
│  TLM:   Telemetry packet processing (when active)                         │
│  DIAG:  Diagnostic data collection (periodic)                             │
│  PM:    Power mode management (periodic check)                            │
│  SLEEP: Low-power idle (clock gating active)                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.1.3.7 Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    DATA FLOW DIAGRAM — Level 0                              │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                                                                      │   │
│  │  ┌─────────┐    ┌─────────────────────────────────────────────┐     │   │
│  │  │EXTERNAL │    │              iPACE-CHIP                      │     │   │
│  │  │SOURCES  │    │                                              │     │   │
│  │  │         │    │  ┌──────────┐      ┌──────────────────┐    │     │   │
│  │  │Cardiac  │───▶│  │ SENSING  │─────▶│  DIGITAL         │    │     │   │
│  │  │Tissue   │    │  │ FRONT-END│      │  CONTROLLER      │    │     │   │
│  │  │         │    │  └──────────┘      └────────┬─────────┘    │     │   │
│  │  │         │    │       ▲                      │              │     │   │
│  │  │         │    │       │               ┌──────▼──────┐      │     │   │
│  │  │Program- │───▶│  ┌────┴────┐         │  PACING      │      │     │   │
│  │  │mer RF   │    │  │TELEMETRY│         │  OUTPUT      │      │     │   │
│  │  │         │    │  │SUBSYSTEM│         │  STAGE       │      │     │   │
│  │  │         │◀───│  └─────────┘         └──────┬───────┘      │     │   │
│  │  │         │    │                             │              │     │   │
│  │  │Magnet   │───▶│  ┌──────────┐      ┌───────▼──────┐      │     │   │
│  │  │         │    │  │ ACCELERO-│      │  LEAD        │      │     │   │
│  │  │         │    │  │ METER    │      │  INTERFACE   │      │     │   │
│  │  └─────────┘    │  └──────────┘      └───────┬──────┘      │     │   │
│  │                  │                           │              │     │   │
│  │                  │  ┌──────────┐      ┌───────▼──────┐      │     │   │
│  │                  │  │ BATTERY  │      │  CARDIAC     │      │     │   │
│  │                  │  │ & PMU    │─────▶│  TISSUE      │      │     │   │
│  │                  │  └──────────┘      └──────────────┘      │     │   │
│  │                  │                                           │     │   │
│  │                  └───────────────────────────────────────────┘     │   │
│  │                                                                      │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  DATA TYPES AND SIZES:                                                    │
│  ┌────────────────────┬──────────────┬──────────────┬──────────────┐      │
│  │ Data Flow          │ Width        │ Rate         │ Priority     │      │
│  ├────────────────────┼──────────────┼──────────────┼──────────────┤      │
│  │ EGM Raw (per ch)   │ 12-bit       │ 1024 sps     │ Real-time    │      │
│  │ EGM Processed      │ 8-bit        │ 128 sps      │ Real-time    │      │
│  │ Pace Command       │ 16-bit       │ <100 sps     │ Real-time    │      │
│  │ Pace Output        │ 8-bit DAC    │ <100 sps     │ Real-time    │      │
│  │ Sensor Data        │ 10-bit       │ 32 sps       │ Background   │      │
│  │ Telemetry TX       │ 8-bit        │ 8-256 kbps   │ Background   │      │
│  │ Telemetry RX       │ 8-bit        │ 8-256 kbps   │ Background   │      │
│  │ Parameters (EEPROM)│ 8/16-bit     │ On demand    │ Non-RT       │      │
│  │ Diagnostics        │ 16-bit       │ 1 sps        │ Background   │      │
│  │ Battery Voltage    │ 10-bit       │ 0.1 sps      │ Background   │      │
│  │ Lead Impedance     │ 16-bit       │ 1/8 Hz       │ Background   │      │
│  │ Temperature        │ 10-bit       │ 0.01 sps     │ Background   │      │
│  └────────────────────┴──────────────┴──────────────┴──────────────┘      │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.1.3.8 Error Handling Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    ERROR HANDLING ARCHITECTURE                               │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │  ERROR DETECTION LAYERS                                              │   │
│  │                                                                      │   │
│  │  LAYER 1: Hardware                                                   │   │
│  │  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐      │   │
│  │  │ Watchdog   │ │ Brown-out  │ │ Parity     │ │ CRC        │      │   │
│  │  │ Timer      │ │ Detector   │ │ Check      │ │ Generator  │      │   │
│  │  └──────┬─────┘ └──────┬─────┘ └──────┬─────┘ └──────┬─────┘      │   │
│  │         │              │              │              │              │   │
│  │  LAYER 2: Firmware                                                  │   │
│  │  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐      │   │
│  │  │ Stack      │ │ Timer      │ │ Range      │ │ Timing     │      │   │
│  │  │ Overflow   │ │ Overflow   │ │ Check      │ │ Monitor    │      │   │
│  │  └──────┬─────┘ └──────┬─────┘ └──────┬─────┘ └──────┬─────┘      │   │
│  │         │              │              │              │              │   │
│  │  LAYER 3: System                                                    │   │
│  │  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐      │   │
│  │  │ Lead       │ │ Battery    │ │ Memory     │ │ Clock      │      │   │
│  │  │ Integrity  │ │ EOL        │ │ Integrity  │ │ Integrity  │      │   │
│  │  └──────┬─────┘ └──────┬─────┘ └──────┬─────┘ └──────┬─────┘      │   │
│  └─────────│──────────────│──────────────│──────────────│──────────────┘   │
│            │              │              │              │                   │
│            └──────────────┴──────┬───────┴──────────────┘                   │
│                                  │                                          │
│                                  ▼                                          │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │  ERROR RESPONSE ACTIONS                                              │   │
│  │                                                                      │   │
│  │  ┌────────────────────────────────────────────────────────────────┐ │   │
│  │  │ SEVERITY: CRITICAL (Patient Safety)                           │ │   │
│  │  │ Actions:                                                      │ │   │
│  │  │  • Log error with timestamp                                   │ │   │
│  │  │  • Switch to safe pacing mode (VOO/AOO)                       │ │   │
│  │  │  • Set maximum output parameters                              │ │   │
│  │  │  • Store event in EEPROM                                      │ │   │
│  │  │  • Set ERI flag                                               │ │   │
│  │  │  • Attempt device reset (if software fault)                   │ │   │
│  │  └────────────────────────────────────────────────────────────────┘ │   │
│  │                                                                      │   │
│  │  ┌────────────────────────────────────────────────────────────────┐ │   │
│  │  │ SEVERITY: HIGH (Function Degradation)                         │ │   │
│  │  │ Actions:                                                      │ │   │
│  │  │  • Log error with timestamp                                   │ │   │
│  │  │  • Disable affected feature                                   │ │   │
│  │  │  • Continue operation in degraded mode                        │ │   │
│  │  │  • Store event in EEPROM                                      │ │   │
│  │  └────────────────────────────────────────────────────────────────┘ │   │
│  │                                                                      │   │
│  │  ┌────────────────────────────────────────────────────────────────┐ │   │
│  │  │ SEVERITY: MEDIUM (Performance Issue)                          │ │   │
│  │  │ Actions:                                                      │ │   │
│  │  │  • Log error with timestamp                                   │ │   │
│  │  │  • Adjust parameters (if possible)                            │ │   │
│  │  │  • Continue normal operation                                  │ │   │
│  │  └────────────────────────────────────────────────────────────────┘ │   │
│  │                                                                      │   │
│  │  ┌────────────────────────────────────────────────────────────────┐ │   │
│  │  │ SEVERITY: LOW (Informational)                                 │ │   │
│  │  │ Actions:                                                      │ │   │
│  │  │  • Log error with timestamp                                   │ │   │
│  │  │  • Continue normal operation                                  │ │   │
│  │  └────────────────────────────────────────────────────────────────┘ │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.1.3.9 Safety Monitoring State Machine

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SAFETY MONITORING STATE MACHINE                           │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                                                                      │   │
│  │           ┌──────────────────┐                                       │   │
│  │     ┌─────│   NORMAL         │◀──── All checks pass                 │   │
│  │     │     │   OPERATION      │                                       │   │
│  │     │     └────────┬─────────┘                                       │   │
│  │     │              │                                                  │   │
│  │     │         Anomaly detected                                       │   │
│  │     │              │                                                  │   │
│  │     │              ▼                                                  │   │
│  │     │     ┌──────────────────┐                                       │   │
│  │     │     │   VERIFICATION   │                                       │   │
│  │     │     │   (Confirm       │                                       │   │
│  │     │     │    anomaly)      │                                       │   │
│  │     │     └────────┬─────────┘                                       │   │
│  │     │              │                                                  │   │
│  │     │     ┌────────┴────────┐                                        │   │
│  │     │     │                 │                                         │   │
│  │     │  Confirmed        False alarm                                  │   │
│  │     │     │                 │                                         │   │
│  │     │     ▼                 └──────────┐                             │   │
│  │     │     ┌──────────────────┐         │                             │   │
│  │     │     │   ASSESSMENT     │         │                             │   │
│  │     │     │   (Classify      │         │                             │   │
│  │     │     │    severity)     │         │                             │   │
│  │     │     └────────┬─────────┘         │                             │   │
│  │     │              │                   │                             │   │
│  │     │     ┌────────┴────────┐          │                             │   │
│  │     │     │                 │          │                             │   │
│  │     │  CRITICAL        NON-CRITICAL    │                             │   │
│  │     │     │                 │          │                             │   │
│  │     │     ▼                 ▼          │                             │   │
│  │     │  ┌──────────────┐ ┌──────────┐  │                             │   │
│  │     │  │ SAFE MODE    │ │ DEGRADED │  │                             │   │
│  │     │  │ (VOO/AOO)    │ │ MODE     │  │                             │   │
│  │     │  └──────┬───────┘ └────┬─────┘  │                             │   │
│  │     │         │              │        │                             │   │
│  │     │         │         Resolved     │                             │   │
│  │     │         │              │        │                             │   │
│  │     │         │              └────────┘                             │   │
│  │     │         │                                                     │   │
│  │     │    ┌────┴────────────────────┐                               │   │
│  │     │    │                         │                                │   │
│  │     │  Resolved              Not resolved                           │   │
│  │     │    │                         │                                │   │
│  │     │    │                         ▼                                │   │
│  │     │    │                 ┌──────────────────┐                    │   │
│  │     │    │                 │   LOCKOUT         │                    │   │
│  │     │    │                 │   (Requires       │                    │   │
│  │     │    │                 │    programmer     │                    │   │
│  │     │    │                 │    reset)         │                    │   │
│  │     │    │                 └──────────────────┘                    │   │
│  │     │    │                                                          │   │
│  │     └────┘                                                          │   │
│  │                                                                      │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  MONITORED PARAMETERS:                                                     │
│  ┌────────────────────────────┬────────────────┬──────────────────────┐   │
│  │ Parameter                  │ Threshold      │ Response             │   │
│  ├────────────────────────────┼────────────────┼──────────────────────┤   │
│  │ Lead impedance             │ <200Ω or >2kΩ │ Alert, mode change   │   │
│  │ Battery voltage            │ <2.5V         │ ERI indication       │   │
│  │ Battery voltage            │ <2.2V         │ EOL, hibernate       │   │
│  │ Die temperature            │ >45°C         │ Thermal shutdown     │   │
│  │ Pacing capture threshold   │ >5.0V @ 0.5ms│ Alert, adjust output │   │
│  │ Sense amplitude            │ <0.5mV        │ Alert, check leads   │   │
│  │ Timer accuracy             │ >±5%          │ Safe mode            │   │
│  │ Memory integrity           │ CRC fail      │ Safe mode            │   │
│  │ Clock frequency            │ >±10%         │ Safe mode            │   │
│  │ Telemetry BER              │ >10⁻³        │ Retry, then disable  │   │
│  │ Watchdog timeout           │ 8 seconds     │ Hard reset           │   │
│  │ Stack pointer              │ Out of bounds │ Hard reset           │   │
│  └────────────────────────────┴────────────────┴──────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.1.3.10 Interface Specification Summary

| Interface                | Protocol    | Data Width | Clock      | Direction |
|---------------------------|-------------|------------|------------|-----------|
| AFE to Digital (EGM)     | SPI         | 12-bit     | 1 MHz      | AFE → MCU |
| MCU to Output Stage       | SPI         | 8-bit      | 1 MHz      | MCU → OUT |
| MCU to Telemetry          | UART        | 8-bit      | 115.2 kbps | Bidir     |
| MCU to EEPROM             | I2C         | 8-bit      | 400 kHz    | Bidir     |
| MCU to Accelometer        | SPI/I2C     | 16-bit     | 1 MHz      | ACCEL → MCU|
| MCU to PMU                | GPIO/SPI    | 8-bit      | 1 MHz      | Bidir     |
| MCU to Watchdog            | Dedicated   | 1-bit      | 32 kHz     | MCU → WDT |
| External to Coil          | Inductive   | Analog     | 402 MHz    | Bidir     |
| Magnet to MCU             | Reed switch | 1-bit      | N/A        | Mag → MCU |
| Battery to PMU            | Analog      | 2-wire     | DC         | BATT → PMU|

### 2.1.3.11 Memory Map

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    MEMORY MAP                                                │
│                                                                             │
│  ADDRESS RANGE        SIZE     ACCESS    DESCRIPTION                       │
│  ──────────────────────────────────────────────────────────────────────     │
│  0x00000000-0x00007FFF  32KB    R/X       Flash (Code)                     │
│  0x00000000-0x000000FF  256B    R/X       Interrupt Vector Table           │
│  0x00000100-0x00001FFF  ~8KB    R/X       Firmware Code                   │
│  0x00002000-0x00007FFF  ~24KB   R/X       Reserved / OTA Update           │
│                                          ─────────────────────────         │
│  0x20000000-0x20001FFF  8KB     R/W       SRAM (Data)                     │
│  0x20000000-0x200003FF  1KB     R/W       Stack (grows down)              │
│  0x20000400-0x20000BFF  2KB     R/W       Heap (if used, static alloc)    │
│  0x20000C00-0x200017FF  3KB     R/W       Global/Static Variables         │
│  0x20001800-0x20001BFF  1KB     R/W       EGM Buffer (circular)           │
│  0x20001C00-0x20001FFF  1KB     R/W       Diagnostic Buffer               │
│                                          ─────────────────────────         │
│  0x40000000-0x40000FFF  4KB     R/W       EEPROM (Parameters)             │
│  0x40000000-0x400003FF  1KB     R/W       Pacing Parameters               │
│  0x40000400-0x400007FF  1KB     R/W       Sensing Parameters              │
│  0x40000800-0x40000BFF  1KB     R/W       Telemetry Parameters            │
│  0x40000C00-0x40000FFF  1KB     R/W       Diagnostic Log                  │
│                                          ─────────────────────────         │
│  0x40010000-0x40010FFF  4KB     R/W       Peripheral Registers            │
│  0x40010000-0x400100FF  256B    R/W       AFE Registers                   │
│  0x40010100-0x400101FF  256B    R/W       Output Stage Registers          │
│  0x40010200-0x400102FF  256B    R/W       Telemetry Registers             │
│  0x40010300-0x400103FF  256B    R/W       Timer Registers                 │
│  0x40010400-0x400104FF  256B    R/W       PMU Registers                   │
│  0x40010500-0x400105FF  256B    R/W       GPIO Registers                  │
│  0x40010600-0x400106FF  256B    R/W       Watchdog Registers              │
│  0x40010700-0x400107FF  256B    R/W       Reserved                        │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

*Section 2.1.3 — Functional Architecture*
*Previous: Section 2.1.2 — Requirements Specification | Next: Section 2.1.4 — Technology Node Selection*
