# 10.2.3 Watchdog Timers for Implantable Pacemaker Supervision

## Chapter Overview

Watchdog timers are the iPACE-CHIP's last line of defense against functional failures that escape detection by redundancy, ECC, and other fault-tolerance mechanisms. A watchdog timer monitors the system's temporal behavior and triggers a recovery action if the expected behavior is not observed within a defined time window. In a life-critical implantable pacemaker, the watchdog system must be itself highly reliable -- a watchdog failure could leave the system unprotected, while a false watchdog trigger could interrupt essential pacing therapy.

This chapter presents the complete watchdog timer architecture for the iPACE-CHIP, covering the hierarchy of watchdogs, the feeding and refresh mechanisms, the recovery actions for different timeout conditions, and the design of the watchdog circuitry to ensure it remains functional even in the presence of faults.

---

## 10.2.3.1 Watchdog Timer Fundamentals

### Purpose and Function

A watchdog timer operates on a simple principle: the supervised system must periodically pet (refresh or kick) the watchdog by asserting a specific signal. If the watchdog is not pet within its timeout period, it assumes the supervised system has failed and initiates a recovery action.

Normal operation: the system periodically asserts the pet signal, resetting the watchdog counter before it reaches the timeout value. Failure scenario: the system becomes unresponsive, the pet signal is not asserted, the counter reaches the timeout value, and the watchdog triggers a recovery action.

### Watchdog Requirements for iPACE-CHIP

The iPACE-CHIP watchdog system must meet the following requirements:

1. Independence: The watchdog must operate independently of the system it supervises. A fault that disables the supervised system must not also disable the watchdog.
2. Reliability: The watchdog itself must have a failure rate below 10^-9 per hour (Category A requirement).
3. Determinism: The watchdog timeout must be precisely controlled within 5% tolerance.
4. Minimal False Positives: The watchdog must not trigger during normal operation, including during legitimate periods of inactivity such as sleep mode.
5. Appropriate Recovery: The recovery action must be proportional to the fault severity.

---

## 10.2.3.2 Watchdog Hierarchy

The iPACE-CHIP implements a three-tier watchdog hierarchy.

### Tier 1: Module Watchdogs

Each critical functional block has its own dedicated watchdog timer.

**Pacing Controller Watchdog:** Supervises the pacing state machine. The pet condition is that the FSM returns to IDLE state within one pacing cycle. The timeout is 2x the maximum pacing interval (e.g., 1200 ms for 60 bpm minimum). Recovery action is to reset the pacing controller FSM to IDLE state.

**Sensing Chain Watchdog:** Supervises the sensing amplifier and digital filter. The pet condition is a periodic self-test signal -- an injected noise pulse that must be detected. Timeout is 500 ms. Recovery action is to switch to backup sensing amplifier and recalibrate threshold.

**DSP Watchdog:** Supervises the digital signal processor. The pet condition is that the DSP must write a specific pattern to the watchdog register within the timeout. Timeout is 100 ms (10x the DSP worst-case interrupt latency). Recovery action is to reset the DSP and reload firmware from flash backup.

**Telemetry Watchdog:** Supervises the telemetry transceiver. The pet condition is a valid telemetry frame received or sent within timeout. Timeout is 5000 ms. Recovery action is to reset the telemetry interface and reinitialize communication.

### Tier 2: Domain Watchdogs

Domain watchdogs supervise groups of related modules.

**Pacing Domain Watchdog:** Supervises the pacing controller, output stage, and lead monitoring. All Tier 1 watchdogs in the pacing domain must be pet. Timeout is 2000 ms. Recovery action is to enter VOO safe mode at 60 bpm.

**Communication Domain Watchdog:** Supervises the telemetry, command parser, and parameter management blocks. Timeout is 10000 ms. Recovery action is to disable telemetry and continue pacing with current parameters.

### Tier 3: System Watchdog

The system watchdog is the top-level supervisor for the entire iPACE-CHIP. All Tier 2 watchdogs must be pet. Timeout is 5000 ms. Recovery action is a full system reset, loading golden firmware, and entering VOO safe mode.

### Watchdog Hierarchy Diagram

The system watchdog at Tier 3 monitors both the pacing domain and communication domain Tier 2 watchdogs, plus the DSP Tier 1 watchdog directly. Each Tier 2 watchdog in turn monitors its constituent Tier 1 module watchdogs. This hierarchical structure ensures that faults at any level are detected and appropriate recovery is triggered.

---

## 10.2.3.3 Watchdog Circuit Design

### Independent Oscillator

Each watchdog tier has its own independent RC oscillator to ensure timing independence from the main system clock.

The watchdog oscillator uses a current-starved ring oscillator with the following design values:

- Capacitance: 10 pF
- Reference voltage: 0.9 V
- Reference current: 100 nA
- Oscillation period: 2 x C x Vref / Iref = 180 ns
- Frequency: approximately 5.56 MHz

The RC oscillator is chosen over a crystal oscillator for the watchdog because:
1. RC oscillators have faster startup time (less than 1 microsecond versus greater than 100 ms for crystal)
2. RC oscillators are simpler and more reliable (no crystal to crack)
3. The absolute frequency accuracy of the RC oscillator (typically 20-30%) is acceptable for watchdog timing where the timeout is set with large margins

### Watchdog Timer Counter

The watchdog counter is a free-running counter that increments at the oscillator frequency. For Tier 1 (DSP watchdog, 100 ms timeout), a 16-bit counter with a divide-by-8 prescaler provides an adjusted timeout of approximately 94 ms. For Tier 2 (pacing domain, 2000 ms timeout), a prescaler of 128 gives approximately 1.5 seconds. For Tier 3 (system, 5000 ms timeout), a prescaler of 512 gives approximately 6 seconds.

### Pet (Refresh) Mechanism

The pet mechanism resets the watchdog counter to zero. It includes a debouncer that rejects glitches shorter than 1 microsecond, an edge detector that only responds to transitions (preventing a stuck-high pet signal from continuously refreshing the watchdog), and a unique pattern check for Tier 2 and Tier 3 watchdogs where the pet signal must contain a specific bit pattern changing each time.

### Redundant Watchdog Design

The iPACE-CHIP watchdog timers are themselves redundant to prevent common-mode failures. Two independent watchdog circuits (Watchdog A and Watchdog B) operate in parallel. If either watchdog times out, recovery is triggered. Both watchdogs must be pet independently.

The two watchdogs use different RC oscillator frequencies (nominal 5.56 MHz and 6.25 MHz), different counter widths (16-bit and 12-bit), different pet signal encoding (one uses edge, one uses pattern), and physical separation on the die (greater than 15 micrometers). This diversity prevents a single fault from affecting both watchdogs simultaneously.

---

## 10.2.3.4 Watchdog Feeding Strategy

### DSP Watchdog Pet

The DSP watchdog pet uses a challenge-response mechanism based on a hardware LFSR (Linear Feedback Shift Register). The hardware generates a deterministic but unpredictable sequence. The DSP must read the current LFSR state, compute the next value, and write it to the pet register. The watchdog verifies the written value matches the expected next value. A match resets the counter (pet successful); a mismatch or no write allows the counter to continue.

This design ensures:
- The DSP must be functioning correctly to pet the watchdog
- A hung DSP cannot pet the watchdog (no register write occurs)
- A corrupted DSP that writes incorrect values cannot pet the watchdog
- The watchdog itself is simple and reliable (just an LFSR and comparator)

### Pacing Controller Watchdog Pet

The pacing controller pet is generated by a hardware circuit that monitors the pacing state machine. A valid-state checker examines the FSM state register and asserts the pet signal only if the FSM is in one of the defined valid states (IDLE, A_SENSED, AV_DELAY, V_PACE, A_PACE). If the FSM enters an undefined state, the pet is not asserted and the watchdog times out.

### Sensing Chain Watchdog Pet

The sensing chain pet is generated by a self-test mechanism. Hardware injects a small test pulse into the sensing amplifier input. The sensing chain amplifies and digitizes the pulse. The digital output is compared against the expected value. If the result matches, the pet is asserted (sensing chain is functional). The test pulse is small enough to not be interpreted as a cardiac event by the sensing comparator.

---

## 10.2.3.5 Watchdog Recovery Actions

### Tier 1 Recovery

**Pacing Controller Recovery:** Assert reset to the pacing controller FSM for 100 microseconds, reload pacing parameters from backup registers, verify parameter integrity via ECC check, and resume pacing in IDLE state. Total recovery time is less than 1 ms.

**DSP Recovery:** Assert DSP reset for 100 microseconds, wait 10 ms for the clock to stabilize, load firmware from flash backup if the primary firmware is suspected corrupt, verify firmware CRC, and start the DSP from the reset vector. Total recovery time is less than 100 ms.

**Sensing Chain Recovery:** Switch to backup sensing amplifier (immediate, less than 1 microsecond), recalibrate sensing threshold (50 ms), and perform self-test on the backup amplifier. If the backup also fails, switch to fixed threshold mode. Total recovery time is less than 100 ms.

### Tier 2 Recovery

**Pacing Domain Recovery:** Reset all Tier 1 modules in the pacing domain, enter VOO (asynchronous) pacing mode at 60 bpm. This mode paces regardless of sensed activity, which is the safe default. Continue monitoring for sensing chain recovery. If sensing recovers, transition to VVI mode (demand pacing). Total recovery time to start VOO pacing is less than 10 ms.

**Communication Domain Recovery:** Reset all Tier 1 modules in the communication domain, disable the telemetry interface to prevent corrupted communication, and continue pacing with current parameters. Enable telemetry only after successful self-test.

### Tier 3 Recovery (System Level)

The system watchdog triggers the most comprehensive recovery: assert system reset to all modules for 200 microseconds, wait 50 ms for all clocks to stabilize, load golden firmware from the read-only flash copy, load default parameters from the read-only flash copy, perform a full self-test of all functional blocks, enter VOO safe mode at 60 bpm, enable telemetry for diagnostic reporting, and wait for the external programmer to reprogram parameters. Total recovery time is less than 500 ms to start VOO pacing.

---

## 10.2.3.6 Watchdog for Specific Failure Modes

### Detecting Firmware Corruption

Firmware corruption from flash bit-flips or radiation effects can cause the DSP to execute incorrect code. The watchdog detects this through program counter monitoring (a range checker verifies the PC stays within valid flash memory space) and stack pointer monitoring (verifies the SP stays within the valid SRAM stack area). If the PC or SP goes to an invalid address, a watchdog timeout is triggered.

### Detecting Clock Failures

If the watchdog RC oscillator is running but the system clock has stopped, the DSP cannot pet the watchdog and the timeout occurs naturally. For clock frequency deviations, the watchdog pet window is set to accommodate the full range of valid clock frequencies (16 MHz plus or minus 20%), so the watchdog does not trigger for frequency changes within the valid operating range.

### Detecting Power Supply Failures

A brown-out detector monitors VDD using a comparator against a threshold voltage. If VDD drops below 1.65 V (the minimum operating voltage), the brown-out detector asserts a brown-out reset to all digital logic, disables the pacing output to prevent incomplete pulses, and enters a low-power monitoring mode. When VDD recovers above 1.75 V (with hysteresis), normal operation resumes from the power-on state.

---

## 10.2.3.7 Watchdog Timing Analysis

### Timeout Budget

The watchdog timeout values are chosen to satisfy two competing requirements: (1) detect failures quickly enough to prevent patient harm, and (2) avoid false triggers during normal operation including worst-case legitimate delays.

For the pacing controller watchdog (1200 ms timeout):
- Normal pacing cycle: maximum 1000 ms (at 60 bpm lower rate limit)
- Timing margin: 200 ms (20% of the timeout)
- Failure detection latency: up to 1200 ms
- Patient safety margin: even if the watchdog takes 1200 ms to detect a pacing failure, the patient's intrinsic heart rhythm typically provides backup pacing support for up to 3000 ms (the escape interval)

For the DSP watchdog (100 ms timeout):
- Worst-case DSP interrupt latency: 10 ms
- Normal pet interval: 10 ms (the DSP pets every main loop iteration)
- Timing margin: 90 ms (90% of the timeout)
- The large margin accounts for legitimate DSP-intensive operations (e.g., telemetry transmission, parameter programming)

### Watchdog Overhead

The total area overhead of the watchdog system is approximately 0.3 mm2 (including both redundant watchdogs, oscillators, counters, and pet logic). The power overhead is approximately 0.5 microwatts (from the RC oscillators and counters), which is about 1.5% of the total digital power budget.

---

## 10.2.3.8 Windowed Watchdog

### Windowed Watchdog Concept

A standard watchdog detects only late pets (timeout). A windowed watchdog also detects early pets -- a pet that arrives before the minimum window time. This is important because a corrupted system might pet the watchdog too rapidly (e.g., a stuck loop that continuously asserts the pet signal), masking a hang condition.

### Windowed Watchdog Implementation

```
Windowed Watchdog Timing:

  |<--- Minimum Window --->|<--- Maximum Window --->|
  |      (no pet here)     |     (pet required here)  |
  
  Time 0 ────────────────── T_min ─────────────── T_max
  
  If pet before T_min: alarm (pet too early -- possible stuck pet)
  If pet between T_min and T_max: normal (counter reset)
  If pet after T_max: alarm (pet too late -- possible hang)
```

The iPACE-CHIP implements windowed watchdogs for the Tier 2 and Tier 3 watchdogs where the supervised system has a well-defined minimum execution time between pet operations:

```
DSP Windowed Watchdog:
  Minimum window: 1 ms (DSP cannot legitimately pet faster than this)
  Maximum window: 100 ms (DSP must pet within this time)
  
  Pet before 1 ms: the pet signal may be stuck high (corrupted DSP loop)
  Pet between 1 ms and 100 ms: normal operation
  Pet after 100 ms: DSP may be hung (timeout)

Pacing Domain Windowed Watchdog:
  Minimum window: 500 ms (pacing cycle cannot be shorter than this at URL)
  Maximum window: 2000 ms (pacing cycle must complete within this time)
```

### Benefits of Windowed Watchdog

1. **Stuck pet detection:** A corrupted system that continuously asserts the pet signal is detected by the minimum window violation.
2. **Speed monitoring:** The windowed watchdog indirectly monitors the system's execution speed. If the DSP runs too fast (possible clock glitch or firmware error), the early pet is detected.
3. **Code flow monitoring:** If the DSP skips a critical section of code and pets the watchdog earlier than expected, the minimum window violation detects this.

---

## 10.2.3.9 Watchdog Independence Verification

### Independence Requirements

The watchdog system must be independent of the systems it supervises. This independence is verified at three levels:

**Electrical Independence:**
```
Each watchdog has its own:
  - RC oscillator (separate from system crystal oscillator)
  - Power supply (from dedicated LDO or directly from battery)
  - Ground connection (separate substrate tap)
  - Reset signal path (separate from system reset tree)
  
Verification: Check that no shared nets connect the watchdog to the
supervised system except through the defined pet and timeout interfaces.
```

**Logical Independence:**
```
The watchdog logic is:
  - Not controllable by the DSP (no DSP-accessible registers in the watchdog)
  - Not dependent on the system clock (uses its own RC oscillator)
  - Not dependent on the system firmware (pure hardware implementation)
  
Verification: Verify that no DSP instruction can modify the watchdog's
internal state (oscillator, counter, pet logic) except through the
defined pet interface.
```

**Physical Independence:**
```
The watchdog circuits are physically separated from the supervised
circuits on the die:
  - Minimum 15 um separation between watchdog and DSP circuits
  - Separate power rail routing
  - Guard rings between watchdog and main logic
  
Verification: Layout extraction confirms the separation distances
and guard ring placement.
```

### Common Mode Failure Prevention

```
Common Mode Failure Scenarios and Prevention:

Scenario 1: Power supply glitch affects both watchdog and supervised system
  Prevention: Separate LDO regulators for watchdog and main system
  Detection: Watchdog monitors its own supply voltage
  
Scenario 2: Clock glitch affects both watchdog and supervised system
  Prevention: Independent RC oscillator for watchdog (not system clock)
  Detection: Watchdog monitors its own oscillator output
  
Scenario 3: Temperature extreme affects both watchdog and supervised system
  Prevention: Watchdog is designed to operate over a wider temperature
  range (-40C to +125C) than the main system (0C to 45C)
  Detection: Watchdog continues to function at temperature extremes
  
Scenario 4: Single-event latch-up in watchdog
  Prevention: Guard rings, triple-well isolation
  Detection: Latch-up current monitoring (watchdog current consumption)
```

---

## 10.2.3.10 Watchdog Design for Manufacturing

### Process Variation Tolerance

The watchdog's RC oscillator frequency varies with process:

```
Process Corners:
  Fast-Fast (FF): f_osc = 7.5 MHz (+35% from nominal)
  Typical-Typical (TT): f_osc = 5.56 MHz (nominal)
  Slow-Slow (SS): f_osc = 3.9 MHz (-30% from nominal)
  
  The timeout must be correct at all process corners:
    At FF: timeout is shortest (counter reaches limit fastest)
    At SS: timeout is longest (counter reaches limit slowest)
    
  Design margin: timeout is set using the worst-case (SS) corner
  with an additional 20% margin for component aging.
```

### Testability Features

The watchdog includes testability features for manufacturing test:

```
Test Mode 1: Oscillator Test
  Override the RC oscillator with an external test clock
  Measure the counter increment rate
  Verify the prescaler division ratio
  
Test Mode 2: Pet Override
  Force the pet signal (bypass the debouncer and edge detector)
  Verify the counter resets correctly
  
Test Mode 3: Timeout Override
  Force the counter to the timeout value
  Verify the timeout signal is generated
  Verify the recovery action is triggered
  
Test Mode 4: Watchdog Disable
  Disable the watchdog (for production testing of the main system)
  The disable signal is only available during production test
  (not accessible in the field)
```

---

## 10.2.3.11 Watchdog Timing Budget Analysis

### Detailed Timing Analysis

```
Pacing Controller Watchdog Timing Budget:

  Timeout: 1200 ms (nominal)
  
  Components of the timeout:
    RC oscillator period: 180 ns +/- 30% = 126 ns to 234 ns
    Prescaler: 64 (divide-by-64)
    Counter: 16-bit (65,536 counts max)
    
  Timeout calculation:
    T_timeout = prescaler * counter_max * T_osc
              = 64 * 65,536 * 180 ns
              = 754,974,720 ns
              = 755 ms
              
    With prescaler of 128: T_timeout = 1510 ms (closest to 1200 ms target)
    
  Process variation effect:
    At FF corner: T_timeout = 128 * 65536 * 126 ns = 1063 ms
    At SS corner: T_timeout = 128 * 65536 * 234 ns = 1965 ms
    
  The actual timeout ranges from 1063 ms to 1965 ms across process corners.
  This is within the acceptable range for the pacing controller watchdog
  (nominal 1200 ms, acceptable range 800 ms to 2000 ms).
```

### Temperature and Voltage Effects on Watchdog Timing

```
Temperature effect on RC oscillator:
  TC (temperature coefficient) of the RC oscillator: approximately +5000 ppm/C
  
  Over the operating range (0C to 45C):
    Delta_f / f = 5000e-6 * (45 - 25) = 10%
    
  At 45C: frequency increases by 10% (timeout decreases by ~10%)
  At 0C: frequency decreases by ~12% (timeout increases by ~12%)
  
  The timeout variation due to temperature is +/- 12%, which is
  within the acceptable range.

Voltage effect on RC oscillator:
  The current source in the RC oscillator depends on VDD:
    I_ref proportional to (VDD - V_th)^2 (for MOSFET current source)
    
  Over the operating range (1.65V to 2.1V):
    Delta_I / I = 2 * (2.1 - 1.8) / 1.8 = 33% (at 2.1V vs 1.8V)
    Delta_I / I = 2 * (1.65 - 1.8) / 1.8 = -17% (at 1.65V vs 1.8V)
    
  The timeout variation due to voltage is -17% to +33%, which is
  larger than the temperature effect. The timeout margin must
  accommodate this variation.
```

---

## 10.2.3.12 Chapter Summary

### Built-In Self-Test (BIST)

At every power-on, the watchdog performs a self-test that verifies: (1) the RC oscillator frequency is within 30% of nominal, (2) the counter increments correctly over 1000 counts, (3) the pet logic responds correctly by asserting pet and verifying counter reset, (4) the timeout detection works by letting the counter overflow and verifying the timeout signal, and (5) the recovery action is generated by asserting timeout and verifying the reset signal. Total BIST time is less than 1 ms.

### Production Testing

Production testing verifies: (1) the oscillator frequency across process corners (fast, typical, slow), (2) the timeout accuracy across voltage and temperature ranges, (3) the pet mechanism with all valid and invalid patterns, (4) the redundant watchdog independence (fault injection on one watchdog does not affect the other), and (5) the recovery action correctness (reset signal amplitude, duration, and timing).

### Fault Injection Testing

Fault injection testing verifies the watchdog system's resilience: (1) stuck-at faults on the pet input (verify timeout occurs), (2) stuck-at faults on the counter (verify timeout or no-timeout as appropriate), (3) stuck-at faults on the oscillator (verify timeout occurs), and (4) single-event upsets in the counter register (verify the majority of the time the counter either resets or continues correctly).

---

## 10.2.3.9 Field Monitoring and Diagnostics

### Watchdog Event Logging

Every watchdog timeout event is logged in non-volatile diagnostic memory with: (1) the watchdog tier and ID, (2) the timestamp (from the RTC), (3) the system state at the time of the timeout, (4) the recovery action taken, and (5) the post-recovery system status.

### Watchdog Statistics

The iPACE-CHIP maintains counters for: (1) total pet operations per watchdog, (2) total timeout events per watchdog, (3) total recovery actions per tier, and (4) current and maximum pet intervals. These statistics are available through telemetry for clinical review.

### Escalation Policy

If a Tier 1 watchdog timeout occurs: log the event, take the Tier 1 recovery action, and continue normal operation. If the same Tier 1 watchdog times out three times within 24 hours: escalate to Tier 2 recovery for that domain. If any Tier 2 watchdog times out: escalate to Tier 3 (system) recovery. After a Tier 3 recovery, the device operates in VOO safe mode until reprogrammed by the clinician.

---

## 10.2.3.10 Chapter Summary

The three-tier watchdog hierarchy provides comprehensive temporal supervision of the iPACE-CHIP's functional blocks. Key design principles include:

- **Independence:** Each watchdog has its own RC oscillator, separate from the system clock
- **Redundancy:** Dual watchdogs with diverse implementations prevent common-mode failures
- **Challenge-response pet mechanism:** Prevents corrupted systems from falsely petting the watchdog
- **Proportional recovery:** Tier 1 triggers module reset; Tier 2 triggers mode change; Tier 3 triggers full system reset
- **Comprehensive failure detection:** Covers firmware corruption, clock failures, power supply failures, and software hangs
- **Minimal overhead:** 0.3 mm2 area and 0.5 microwatts power for the complete watchdog system

The next chapter (10.2.4) covers graceful degradation, the strategy for maintaining essential pacing therapy even when multiple faults have reduced the system's capabilities.

---

## References

1. Guilhoto, J.J., "Watchdog Timer Applications for Microprocessor-Based Systems," *Embedded Systems Conference*, 2004.
2. IEC 60601-1:2005, "Medical Electrical Equipment -- Part 1: General Requirements for Basic Safety and Essential Performance."
3. IEC 62304:2006, "Medical Device Software -- Software Life Cycle Processes."
4. Kilsheimer, J., "Watchdog Timers -- A Vital Link in System Reliability," *EDN Magazine*, 2002.
5. Perry, R., "Designing Watchdog Timers for Automotive Applications," *Automotive Electronics Design*, 2006.
6. ANSI/AAMI EC11:1991/(R)2001/(R)2007, "Diagnostic Electrocardiographic Devices."
7. ISO 14708-3:2017, "Implants for Surgery -- Active Implantable Medical Devices -- Part 3."
8. Avizienis, A., "Fault-Tolerance and Fault-Avoidance in Digital Systems," *Proceedings of ISCAS*, 1986.
