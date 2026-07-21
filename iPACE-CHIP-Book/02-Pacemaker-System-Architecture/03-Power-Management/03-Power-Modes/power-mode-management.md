# Power Mode Management

## 2.3.3 Clock Gating, Power Gating, and Wake-Up Sequences

Power mode management is the primary mechanism for achieving the 10-year
battery life target in an implantable pacemaker. By dynamically scaling clock
frequencies, gating clocks to unused blocks, powering down inactive circuits,
and managing wake-up transitions, the pacemaker can reduce its average power
consumption from tens of milliwatts during active operation to less than
10 microwatts during normal sensing/pacing cycles.

---

## 2.11.1 Power Mode Definitions

### Mode Summary

| Mode | Description | Average Power | Wake-Up Time | Functions Active |
|------|------------|--------------|-------------|-----------------|
| Active (Full) | Pacing + Sensing + Telemetry | 10-25 µW | — | All |
| Active (Normal) | Pacing + Sensing | 5-15 µW | — | AFE, DFC, PMU |
| Sleep | Sensing only (no pacing needed) | 1-5 µW | < 1 ms | AFE, Timer, DFC |
| Deep Sleep | Timer only (asynchronous pacing) | 0.1-1 µW | < 5 ms | Timer, PMU |
| Hibernate | Watchdog timer only | 0.01-0.1 µW | < 50 ms | Watchdog, PMU |
| Off | Device powered down | 0 | N/A | None |

### Mode Transitions

```
                    POWER MODE STATE DIAGRAM

  ┌─────────────────────────────────────────────────────────────────────┐
  │                                                                     │
  │                                                                     │
  │  ┌──────────┐    Sensing    ┌──────────┐    Telemetry  ┌────────┐ │
  │  │          │    event      │          │    request    │        │ │
  │  │  SLEEP   │──────────────▶│  ACTIVE  │◀──────────────▶│ TELEM  │ │
  │  │  MODE    │◀──────────────│  MODE    │                │ MODE   │ │
  │  │          │    no events  │          │                │        │ │
  │  └────┬─────┘    for 8s     └────┬─────┘                └────────┘ │
  │       │                           │                                │
  │       │ timeout                   │ no pacing                      │
  │       │ (30s)                     │ for 60s                        │
  │       │                           │                                │
  │       ▼                           ▼                                │
  │  ┌──────────┐              ┌──────────┐                           │
  │  │          │              │          │                           │
  │  │  DEEP   │◀─────────────│  NORMAL  │                           │
  │  │  SLEEP   │              │  ACTIVE  │                           │
  │  │          │─────────────▶│          │                           │
  │  └────┬─────┘   pace       └──────────┘                           │
  │       │   needed                                              │
  │       │                                                          │
  │       │ timeout                                                  │
  │       │ (5min)                                                   │
  │       │                                                          │
  │       ▼                                                          │
  │  ┌──────────┐                                                    │
  │  │          │                                                    │
  │  │ HIBERNATE│◀─────── (battery critical)                         │
  │  │ MODE     │                                                    │
  │  └──────────┘                                                    │
  │                                                                     │
  └─────────────────────────────────────────────────────────────────────┘
```

---

## 2.11.2 Clock Gating

### Clock Gating Strategy

Clock gating is the most effective technique for reducing dynamic power
consumption. By disabling the clock to inactive circuit blocks, the
switching activity (and thus dynamic power) is eliminated.

```
  Dynamic power: P_dynamic = α × C × V² × f

  where:
    α = switching activity factor
    C = load capacitance
    V = supply voltage
    f = clock frequency

  Clock gating reduces f to 0 for gated blocks:
    P_gated = 0 (no switching)
```

### Clock Gating Implementation

```
                    CLOCK GATING ARCHITECTURE

  32.768 kHz ────┬──────────────────────────────────────
  Oscillator     │
                 ▼
            ┌─────────┐
            │  Clock  │
            │  Tree   │
            └────┬────┘
                 │
        ┌────────┼────────┬────────┬────────┬────────┐
        │        │        │        │        │        │
        ▼        ▼        ▼        ▼        ▼        ▼
   ┌────────┐┌────────┐┌────────┐┌────────┐┌────────┐┌────────┐
   │  ICG   ││  ICG   ││  ICG   ││  ICG   ││  ICG   ││  ICG   │
   │  AFE   ││  DFC   ││  Timer ││  RF    ││  PMU   ││  Diag  │
   └───┬────┘└───┬────┘└───┬────┘└───┬────┘└───┬────┘└───┬────┘
       │         │         │         │         │         │
       ▼         ▼         ▼         ▼         ▼         ▼
   ┌────────┐┌────────┐┌────────┐┌────────┐┌────────┐┌────────┐
   │  AFE   ││  DFC   ││  Timer ││  RF    ││  PMU   ││  Diag  │
   │  Block ││  Block ││  Block ││  Block ││  Block ││  Block │
   └────────┘└────────┘└────────┘└────────┘└────────┘└────────┘

  ICG = Integrated Clock Gating cell
  Each ICG has an enable signal from the power mode controller
```

### Clock Gating by Mode

| Mode | AFE Clock | DFC Clock | Timer Clock | RF Clock | PMU Clock |
|------|-----------|-----------|-------------|----------|-----------|
| Active (Full) | ON | ON | ON | ON | ON |
| Active (Normal) | ON | ON | ON | OFF | ON |
| Sleep | ON | OFF | ON | OFF | ON |
| Deep Sleep | OFF | OFF | ON | OFF | ON |
| Hibernate | OFF | OFF | OFF (slow) | OFF | ON |

### Clock Gating Controller

```
                    CLOCK GATING CONTROLLER

  Power Mode ────┬────────────────────────────────────
                 │
                 ▼
            ┌─────────┐
            │  Mode   │
            │  Decode │
            └────┬────┘
                 │
        ┌────────┼────────┬────────┬────────┬────────┐
        │        │        │        │        │        │
        ▼        ▼        ▼        ▼        ▼        ▼
   ┌────────┐┌────────┐┌────────┐┌────────┐┌────────┐
   │ AFE_EN ││ DFC_EN ││TMR_EN  ││ RF_EN  ││ PMU_EN │
   │        ││        ││        ││        ││        │
   └────────┘└────────┘└────────┘└────────┘└────────┘
        │        │        │        │        │
        ▼        ▼        ▼        ▼        ▼
   Clock to   Clock to  Clock to  Clock to  Clock to
   AFE block  DFC block Timer     RF block  PMU block
```

---

## 2.11.3 Power Gating

### Power Gating Strategy

Power gating eliminates both dynamic and static (leakage) power by
completely disconnecting the supply voltage from inactive circuit blocks.

```
  Total power: P_total = P_dynamic + P_static

  P_dynamic = α × C × V² × f (eliminated by clock gating)
  P_static = I_leak × V (eliminated by power gating)

  Power gating eliminates both components:
    P_gated = 0
```

### Power Gating Implementation

```
                    POWER GATING ARCHITECTURE

  V_ANA ────────┬────────────────────────────────────
                │
        ┌───────┼───────┬───────┬───────┬───────┐
        │       │       │       │       │       │
        ▼       ▼       ▼       ▼       ▼       ▼
   ┌────────┐┌────────┐┌────────┐┌────────┐┌────────┐
   │  PMOS  ││  PMOS  ││  PMOS  ││  PMOS  ││  PMOS  │
   │  Header││  Header││  Header││  Header││  Header│
   │  (AFE) ││  (ADC) ││  (DAC) ││  (RF)  ││  (SRAM)│
   └───┬────┘└───┬────┘└───┬────┘└───┬────┘└───┬────┘
       │         │         │         │         │
       ▼         ▼         ▼         ▼         ▼
   ┌────────┐┌────────┐┌────────┐┌────────┐┌────────┐
   │  AFE   ││  ADC   ││  DAC   ││  RF    ││  SRAM  │
   │  Block ││  Block ││  Block ││  Block ││  Block │
   └───┬────┘└───┬────┘└───┬────┘└───┬────┘└───┬────┘
       │         │         │         │         │
       ▼         ▼         ▼         ▼         ▼
   ┌────────┐┌────────┐┌────────┐┌────────┐┌────────┐
   │  NMOS  ││  NMOS  ││  NMOS  ││  NMOS  ││  NMOS  │
   │ Footer ││ Footer ││ Footer ││ Footer ││ Footer │
   └───┬────┘└───┬────┘└───┬────┘└───┬────┘└───┬────┘
       │         │         │         │         │
      GND       GND       GND       GND       GND

  PMOS Header: Connects/disconnects V_ANA to block
  NMOS Footer: Connects/disconnects block to GND
  Both must be ON for the block to operate
```

### Power Gating by Mode

| Block | Active | Sleep | Deep Sleep | Hibernate |
|-------|--------|-------|-----------|-----------|
| AFE | ON | ON | OFF | OFF |
| ADC | ON | OFF | OFF | OFF |
| DAC | ON | OFF | OFF | OFF |
| Digital Controller | ON | ON | OFF | OFF |
| Timers | ON | ON | ON | ON (slow) |
| RF Transceiver | ON | OFF | OFF | OFF |
| SRAM | ON | ON | OFF | OFF |
| Bandgap Reference | ON | ON | ON | ON |
| LDO Regulators | ON | ON | ON | ON (reduced) |
| Charge Pump | ON | ON | OFF | OFF |
| Watchdog | ON | ON | ON | ON |

### State Retention

When power-gating a block that needs to preserve its state (e.g., the
digital controller's register file), state retention techniques are used:

```
  State retention techniques:

  1. Retention flip-flops:
     - Separate retention supply (V_RET)
     - Hold state with reduced voltage
     - Power consumption: < 1 nW per flip-flop

  2. SRAM with retention:
     - Reduce SRAM supply voltage to retention level
     - Data maintained at reduced voltage
     - Power consumption: < 10 nW per KB

  3. Shadow registers:
     - Copy critical registers to low-power retention memory
     - Restore on wake-up
     - Power consumption: < 1 nW per register
```

---

## 2.11.4 Voltage Scaling

### Dynamic Voltage Scaling (DVS)

Dynamic voltage scaling adjusts the supply voltage based on the required
performance level:

```
  P_dynamic = α × C × V² × f

  If we reduce V by factor k:
    P_new = α × C × (kV)² × f = k² × P_original

  If we also reduce f by factor k (to maintain timing):
    P_new = α × C × (kV)² × (kf) = k³ × P_original

  Example: V reduced from 1.2V to 0.8V (k = 0.67)
    P_new = 0.67³ × P_original = 0.30 × P_original
    70% power reduction!
```

### Voltage Scaling by Mode

| Mode | V_DIG | V_ANA | V_RF | Performance |
|------|-------|-------|------|------------|
| Active (Full) | 1.2 V | 2.8 V | 1.8 V | Maximum |
| Active (Normal) | 1.2 V | 2.8 V | OFF | Normal |
| Sleep | 1.0 V | 2.8 V | OFF | Reduced |
| Deep Sleep | 0.8 V | 2.8 V | OFF | Minimum |
| Hibernate | 0.6 V (retention) | 2.8 V (OFF) | OFF | Retention only |

---

## 2.11.5 Wake-Up Sequences

### Wake-Up from Sleep

```
                    WAKE-UP FROM SLEEP SEQUENCE

  Event: Sensing event detected (comparator interrupt)
    │
    ▼
  Step 1: Enable DFC clock (< 1 µs)
    │
    ▼
  Step 2: Restore DFC state from retention registers (< 1 µs)
    │
    ▼
  Step 3: Process sense event (< 10 µs)
    │
    ▼
  Step 4: Make pacing decision (< 5 µs)
    │
    ▼
  Step 5: If pace needed → Enable output stage (< 5 µs)
    │
    ▼
  Step 6: Deliver pacing pulse (0.1-2 ms)
    │
    ▼
  Step 7: Disable DFC clock (return to sleep)
    │
    ▼
  Total wake-up time: < 1 ms
  Total active time per event: < 2 ms
```

### Wake-Up from Deep Sleep

```
                    WAKE-UP FROM DEEP SLEEP SEQUENCE

  Event: Timer expiry (lower rate interval elapsed)
    │
    ▼
  Step 1: Enable bandgap reference (< 100 µs)
    │
    ▼
  Step 2: Enable LDO regulators (< 500 µs)
    │
    ▼
  Step 3: Wait for regulators to settle (< 500 µs)
    │
    ▼
  Step 4: Enable DFC clock (< 1 µs)
    │
    ▼
  Step 5: Restore DFC state from retention (< 1 µs)
    │
    ▼
  Step 6: Execute pacing algorithm (< 10 µs)
    │
    ▼
  Step 7: Deliver pacing pulse (0.1-2 ms)
    │
    ▼
  Step 8: Disable DFC clock, LDOs (return to deep sleep)
    │
    ▼
  Total wake-up time: < 5 ms
  Total active time per event: < 5 ms
```

### Wake-Up from Hibernate

```
                    WAKE-UP FROM HIBERNATE SEQUENCE

  Event: Watchdog timeout or magnet detection
    │
    ▼
  Step 1: Enable bandgap reference (< 100 µs)
    │
    ▼
  Step 2: Enable all LDO regulators (< 1 ms)
    │
    ▼
  Step 3: Wait for regulators to settle (< 1 ms)
    │
    ▼
  Step 4: Enable system clock oscillator (< 1 ms)
    │
    ▼
  Step 5: Wait for oscillator to stabilize (< 1 ms)
    │
    ▼
  Step 6: Release digital reset (< 10 µs)
    │
    ▼
  Step 7: Execute POST (< 10 ms)
    │
    ▼
  Step 8: Load parameters from EEPROM (< 10 ms)
    │
    ▼
  Step 9: Enter normal operation
    │
    ▼
  Total wake-up time: < 50 ms
  Total active time: < 50 ms
```

---

## 2.11.6 Power Budget Analysis

### Active Mode Power Budget

| Block | Voltage | Current | Power | Duty Cycle | Average Power |
|-------|---------|---------|-------|-----------|---------------|
| AFE (sensing) | 2.8 V | 1.5 µA | 4.2 µW | 100% | 4.2 µW |
| Digital controller | 1.2 V | 2.0 µA | 2.4 µW | 100% | 2.4 µW |
| Timers | 1.2 V | 0.5 µA | 0.6 µW | 100% | 0.6 µW |
| Bandgap reference | 2.8 V | 0.5 µA | 1.4 µW | 100% | 1.4 µW |
| LDO regulators | 2.8 V | 1.0 µA | 2.8 µW | 100% | 2.8 µW |
| Buck converter | 2.8 V | 0.3 µA | 0.8 µW | 100% | 0.8 µW |
| **Total (normal)** | | **5.3 µA** | | | **12.2 µW** |

### Sleep Mode Power Budget

| Block | Voltage | Current | Power | Duty Cycle | Average Power |
|-------|---------|---------|-------|-----------|---------------|
| AFE (sensing) | 2.8 V | 1.5 µA | 4.2 µW | 100% | 4.2 µW |
| Timers | 1.2 V | 0.5 µA | 0.6 µW | 100% | 0.6 µW |
| Bandgap reference | 2.8 V | 0.5 µA | 1.4 µW | 100% | 1.4 µW |
| LDO regulators | 2.8 V | 0.5 µA | 1.4 µW | 100% | 1.4 µW |
| Buck converter | 2.8 V | 0.2 µA | 0.6 µW | 100% | 0.6 µW |
| **Total (sleep)** | | **3.2 µA** | | | **8.2 µW** |

### Deep Sleep Power Budget

| Block | Voltage | Current | Power | Duty Cycle | Average Power |
|-------|---------|---------|-------|-----------|---------------|
| Timers | 1.2 V | 0.3 µA | 0.4 µW | 100% | 0.4 µW |
| Bandgap reference | 2.8 V | 0.3 µA | 0.8 µW | 100% | 0.8 µW |
| LDO regulators | 2.8 V | 0.2 µA | 0.6 µW | 100% | 0.6 µW |
| Buck converter | 2.8 V | 0.1 µA | 0.3 µW | 100% | 0.3 µW |
| **Total (deep sleep)** | | **0.9 µA** | | | **2.1 µW** |

### Hibernate Power Budget

| Block | Voltage | Current | Power | Duty Cycle | Average Power |
|-------|---------|---------|-------|-----------|---------------|
| Watchdog timer | 1.2 V | 0.05 µA | 0.06 µW | 100% | 0.06 µW |
| Bandgap reference | 2.8 V | 0.1 µA | 0.3 µW | 100% | 0.3 µW |
| LDO (retention only) | 2.8 V | 0.05 µA | 0.14 µW | 100% | 0.14 µW |
| **Total (hibernate)** | | **0.2 µA** | | | **0.5 µW** |

---

## 2.11.7 Latency Analysis

### Wake-Up Latency Budget

| Transition | Target Latency | Breakdown |
|-----------|---------------|-----------|
| Sleep → Active | < 1 ms | Clock enable: 1 µs, State restore: 1 µs, Processing: 100 µs |
| Deep Sleep → Active | < 5 ms | LDO enable: 500 µs, Clock enable: 1 ms, State restore: 1 µs, Processing: 100 µs |
| Hibernate → Active | < 50 ms | LDO enable: 1 ms, Clock stabilize: 10 ms, POST: 10 ms, Parameter load: 10 ms |

### Impact on Pacing Accuracy

The wake-up latency must be less than the timing accuracy requirement:

```
  Timing accuracy requirement: ±1 ms
  Wake-up latency (Sleep → Active): < 1 ms
  Margin: 0 ms (tight!)

  Solution: Use timer interrupt to wake up BEFORE the pacing event
  Wake-up time = Timer interval - Wake-up latency
  Example: If pacing interval = 1000 ms, wake up at 999 ms
           → 1 ms before pacing event → sufficient margin
```

---

## 2.11.8 Power Mode Controller Implementation

### Hardware Power Mode Controller

The power mode controller is implemented as a dedicated hardware block
that operates independently of the firmware:

```
                    HARDWARE POWER MODE CONTROLLER

  ┌──────────────────────────────────────────────────────────────┐
  │                                                              │
  │  Inputs:                                                     │
  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
  │  │ Sense    │  │ Timer    │  │ Magnet   │  │ Battery  │   │
  │  │ Event    │  │ Expiry   │  │ Detect   │  │ Status   │   │
  │  │          │  │          │  │          │  │          │   │
  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘   │
  │       │             │             │             │            │
  │       ▼             ▼             ▼             ▼            │
  │  ┌──────────────────────────────────────────────────────┐   │
  │  │              MODE STATE MACHINE                      │   │
  │  │                                                      │   │
  │  │  Current Mode ──▶ Next Mode ──▶ Mode Transition      │   │
  │  │                                                      │   │
  │  └──────────────────────────────────────────────────────┘   │
  │       │                                                      │
  │       ▼                                                      │
  │  Outputs:                                                    │
  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
  │  │ Clock    │  │ Power    │  │ Voltage  │  │ State    │   │
  │  │ Gating   │  │ Gating   │  │ Scaling  │  │ Retention│   │
  │  │ Signals  │  │ Signals  │  │ Signals  │  │ Control  │   │
  │  │          │  │          │  │          │  │          │   │
  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
  │                                                              │
  └──────────────────────────────────────────────────────────────┘
```

### Firmware-Assisted Power Management

Some power mode transitions require firmware involvement:

| Transition | Hardware | Firmware | Reason |
|-----------|---------|---------|--------|
| Active → Sleep | Yes | Yes | Firmware saves state |
| Sleep → Active | Yes | Yes | Firmware restores state |
| Active → Deep Sleep | Yes | Yes | Firmware saves complex state |
| Deep Sleep → Active | Yes | Yes | Firmware restores complex state |
| Active → Hibernate | Yes | Yes | Firmware saves all state |
| Hibernate → Active | Yes | Yes | Firmware executes POST |

---

## 2.11.9 Clock Distribution

### Clock Tree Architecture

```
                    CLOCK TREE ARCHITECTURE

  32.768 kHz ────┬──────────────────────────────────────
  Crystal        │
  Oscillator     │
                 ▼
            ┌─────────┐
            │  Clock  │
            │  Buffer │
            └────┬────┘
                 │
        ┌────────┼────────┬────────┬────────┬────────┐
        │        │        │        │        │        │
        ▼        ▼        ▼        ▼        ▼        ▼
   ┌────────┐┌────────┐┌────────┐┌────────┐┌────────┐┌────────┐
   │  ÷1    ││  ÷2    ││  ÷4    ││  ÷8    ││  ÷16   ││  ÷32   │
   │(32.768k)│(16.384k)│(8.192k)│(4.096k)│(2.048k)│(1.024k)│
   └───┬────┘└───┬────┘└───┬────┘└───┬────┘└───┬────┘└───┬────┘
       │         │         │         │         │         │
       ▼         ▼         ▼         ▼         ▼         ▼
   ┌────────┐┌────────┐┌────────┐┌────────┐┌────────┐┌────────┐
   │  ICG   ││  ICG   ││  ICG   ││  ICG   ││  ICG   ││  ICG   │
   │  Fast  ││  Normal││  Medium││  Slow  ││  VSlow ││  XSlow │
   └───┬────┘└───┬────┘└───┬────┘└───┬────┘└───┬────┘└───┬────┘
       │         │         │         │         │         │
       ▼         ▼         ▼         ▼         ▼         ▼
   ┌────────┐┌────────┐┌────────┐┌────────┐┌────────┐┌────────┐
   │  AFE   ││  DFC   ││  Timer ││  Diag  ││  PMU   ││  Watch │
   │  Block ││  Block ││  Block ││  Block ││  Block ││  dog   │
   └────────┘└────────┘└────────┘└────────┘└────────┘└────────┘
```

### Clock Frequency Selection

| Clock | Frequency | Application | Power |
|-------|-----------|------------|-------|
| Fast | 32.768 kHz | AFE (high-speed sensing) | Highest |
| Normal | 16.384 kHz | Digital controller | High |
| Medium | 8.192 kHz | Timers | Medium |
| Slow | 4.096 kHz | Diagnostics | Low |
| Very Slow | 2.048 kHz | PMU | Very Low |
| Extremely Slow | 1.024 kHz | Watchdog | Lowest |

---

## 2.11.10 Summary

Power mode management is the primary mechanism for achieving the 10-year
battery life target:

1. **Clock gating**: Eliminates dynamic power by disabling clocks to
   inactive blocks. Reduces dynamic power by 50-90% depending on mode.

2. **Power gating**: Eliminates both dynamic and static power by
   disconnecting the supply voltage. Reduces total power by 90-99%
   in deep sleep and hibernate modes.

3. **Voltage scaling**: Reduces dynamic power quadratically with voltage.
   Scaling from 1.2V to 0.8V reduces dynamic power by 56%.

4. **Wake-up management**: Carefully sequenced wake-up transitions ensure
   that the pacemaker can resume normal operation within the timing
   accuracy requirements (< 1 ms for sleep, < 5 ms for deep sleep).

5. **Power budget**: The average power consumption of 10-15 µW in normal
   operation, with sleep mode at 1-5 µW and deep sleep at 0.1-1 µW,
   enables the 10-year battery life target.

The hardware power mode controller operates independently of the firmware,
ensuring that power mode transitions are deterministic and reliable even
under fault conditions. The firmware assists with complex state save/restore
operations during mode transitions.
