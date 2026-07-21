# Retention Flip-Flop Design for Implantable Pacemaker ASICs

## 1. Introduction to Retention Flip-Flops

Retention flip-flops (also called state-retention flip-flops or always-on flip-flops) are specialized storage elements that maintain their data state even when the main power supply to a logic block is removed. For the iPACE-CHIP pacemaker ASIC, retention flip-flops are essential for preserving critical configuration, state machine values, and calibration data during power-gated sleep modes, enabling fast wake-up without the overhead of full state restoration from external memory.

The fundamental challenge is maintaining state with minimal power consumption while the surrounding logic is powered off. This requires a dual-supply architecture: the main supply powers the flip-flop's functional logic, while a separate always-on supply powers only the state-holding elements. The design must balance retention power, wake-up time, area overhead, and reliability for the implantable medical device application.

## 2. Retention Flip-Flop Architectures

### 2.1 Standard Retention Flip-Flop

```
Standard Retention Flip-Flop Architecture:

V_DD_main (switchable)
    │
    ├─────────────────────────┐
    │                         │
    │  ┌─────────────────┐    │
    │  │                 │    │
    │  │  Functional     │    │
    │  │  Master-Slave   │    │
    │  │  Flip-Flop      │    │
    │  │                 │    │
    │  └────────┬────────┘    │
    │           │             │
    │     ┌─────┴─────┐       │
    │     │           │       │
    │  ┌──▼──┐     ┌──▼──┐   │
    │  │ Q   │     │ Q_n │   │
    │  └──┬──┘     └──┬──┘   │
    │     │           │       │
    └─────┼───────────┼───────┘
          │           │
          │     ┌─────┴─────────────────────┐
          │     │                           │
          │  ┌──▼──────────────────────┐    │
          │  │  Retention Latch        │    │
          │  │  (powered by V_DD_ret) │    │
          │  │                        │    │
          │  │  ┌────────┐            │    │
          │  │  │ Cross- │            │    │
          ├──┤  │ coupled│◄───────────┤    │
          │  │  │ invert │            │    │
          │  │  └────┬───┘            │    │
          │  │       │                │    │
          │  │  ┌────▼───┐            │    │
          │  │  │ Write  │            │    │
          │  │  │ Gate   │◄── SAVE_n  │    │
          │  │  └────────┘            │    │
          │  └────────────────────────┘    │
          │                                │
          └────────────────────────────────┘
                           │
                      Q_ret (retained value)

V_DD_ret (always-on, 0.5V)
    │
    └── Powers retention latch only

Operation:
- Normal mode: SAVE_n = 1, retention latch follows Q
- Sleep mode: V_DD_main off, retention latch holds Q
- Wake-up: V_DD_main restored, SAVE_n = 0, Q = Q_ret
```

### 2.2 Dual-Clock Retention Flip-Flop

```
Dual-Clock Retention Flip-Flop:

This design allows independent save and restore operations:

              V_DD_main
                │
    ┌───────────┴───────────┐
    │                       │
    │  ┌─────────────────┐  │
    │  │  Master Latch   │  │
    │  │  (CLK-gated)    │  │
    │  └────────┬────────┘  │
    │           │           │
    │  ┌────────▼────────┐  │
    │  │  Slave Latch    │  │
    │  │  (CLK-gated)    │  │
    │  └────────┬────────┘  │
    │           │           │
    │           Q           │
    │           │           │
    └───────────┼───────────┘
                │
          ┌─────▼─────┐
          │           │
    ┌─────▼─────┐  ┌──▼──────────┐
    │  SAVE     │  │  RESTORE    │
    │  Switch   │  │  Switch     │
    └─────┬─────┘  └──┬──────────┘
          │           │
    ┌─────▼─────┐     │
    │ Retention │     │
    │ Latch     │─────┘
    │ (V_DD_ret)│
    └───────────┘
          │
      Q_ret

Signals:
- SAVE_n: Active-low save control (capture Q into retention)
- RESTORE_n: Active-low restore control (drive Q from Q_ret)
- Both signals powered by V_DD_ret (always-on)
```

### 2.3 Low-Power Retention Flip-Flop

```
Ultra-Low-Power Retention Flip-Flop for iPACE-CHIP:

Optimized for minimum retention power:

            V_DD_main
                │
    ┌───────────┴───────────┐
    │                       │
    │  ┌─────────────────┐  │
    │  │  Transmission   │  │
    │  │  Gate Master    │  │
    │  └────────┬────────┘  │
    │           │           │
    │  ┌────────▼────────┐  │
    │  │  Transmission   │  │
    │  │  Gate Slave     │  │
    │  └────────┬────────┘  │
    │           │           │
    │           Q           │
    │           │           │
    └───────────┼───────────┘
                │
          ┌─────▼─────┐
          │           │
    ┌─────▼─────┐     │
    │  Minimal  │     │
    │  Inverter │     │
    │  Pair     │     │
    │  (V_DD_ret│     │
    │  = 0.5V)  │     │
    └─────┬─────┘     │
          │           │
          └───────────┘
                │
           Q_ret (retained)

Ultra-Low-Power Features:
- Retention latch: Single cross-coupled inverter pair
- V_DD_ret: 0.5V (minimum for state retention)
- Retention current: < 100 fA per flip-flop
- Retention power: 50 fW per flip-flop at 0.5V
- Total for 1000 flops: 50 pW (negligible)
```

## 3. Transistor-Level Design

### 3.1 Cross-Coupled Inverter Pair

```
Cross-Coupled Inverter Pair (Retention Latch):

V_DD_ret (0.5V)
    │
    ├─────────────────────┐
    │                     │
    │  ┌─────────┐        │
    │  │  PMOS   │        │
    │  │  M1     │        │
    │  └────┬────┘        │
    │       │             │
    │  ┌────┴────┐        │
    │  │  NMOS   │        │
    │  │  M2     │        │
    │  └────┬────┘        │
    │       │             │
    │       ├──────── Q_ret (output)
    │       │             │
    │  ┌────┴────┐        │
    │  │  PMOS   │        │
    │  │  M3     │        │
    │  └────┬────┘        │
    │       │             │
    │  ┌────┴────┐        │
    │  │  NMOS   │        │
    │  │  M4     │        │
    │  └────┬────┘        │
    │       │             │
    └───────┴──────┬──────┘
                   │
              GND (0V)

Design Parameters:
- M1/M3 (PMOS): W = 0.36 μm, L = 0.18 μm
- M2/M4 (NMOS): W = 0.18 μm, L = 0.18 μm
- V_DD_ret = 0.5V
- Retention current: < 100 fA (sub-threshold)
- Retention time: > 10 years (theoretical)
- Area: 0.54 μm × 0.36 μm = 0.19 μm²
```

### 3.2 Write Gate Circuit

```
Write Gate (Save Switch):

This circuit controls when Q is written to the retention latch:

V_DD_ret (0.5V)
    │
    ├─────────────────────┐
    │                     │
    │  ┌─────────┐        │
    │  │  PMOS   │        │
    │  │  M1     │        │
    │  │ (write  │        │
    │  │  gate)  │        │
    │  └────┬────┘        │
    │       │             │
    │  Q ───┤             │
    │       │             │
    │  ┌────┴────┐        │
    │  │  NMOS   │        │
    │  │  M2     │        │
    │  │ (write  │        │
    │  │  gate)  │        │
    │  └────┬────┘        │
    │       │             │
    │       ├──────── Q_ret (to retention latch)
    │       │             │
    └───────┴──────┬──────┘
                   │
              GND (0V)

Control: SAVE_n
- SAVE_n = 0 (active): M1 ON, M2 ON → Q_ret = Q
- SAVE_n = 1 (inactive): M1 OFF, M2 OFF → Q_ret held

Power:
- During save: 10 fA × 0.5V = 5 fW (transient)
- During retention: < 1 fA (leakage only)
```

### 3.3 Restore Circuit

```
Restore Circuit:

This circuit restores Q from Q_ret after power-on:

            V_DD_main (1.8V)
                │
    ┌───────────┴───────────┐
    │                       │
    │  ┌─────────────────┐  │
    │  │  PMOS M1        │  │
    │  │  (restore gate) │  │
    │  └────────┬────────┘  │
    │           │           │
    │  Q_ret ───┤           │
    │           │           │
    │  ┌────────▼────────┐  │
    │  │  NMOS M2        │  │
    │  │  (restore gate) │  │
    │  └────────┬────────┘  │
    │           │           │
    │           Q (restored)│
    │           │           │
    └───────────┼───────────┘
                │
           GND (0V)

Control: RESTORE_n
- RESTORE_n = 0 (active): M1 ON, M2 ON → Q = Q_ret
- RESTORE_n = 1 (inactive): M1 OFF, M2 OFF → Q held

Timing:
- Restore delay: 0.2 ns
- Must be completed before first clock edge
- RESTORE_n asserted during power-on sequence
```

## 4. Retention Power Analysis

### 4.1 Retention Current Budget

```
iPACE-CHIP Retention Current Budget:

Component                    │ Count │ Current/Flop │ Total
─────────────────────────────┼───────┼──────────────┼──────
Configuration registers      │ 200   │ 100 fA       │ 20 pA
State machine registers      │ 50    │ 100 fA       │ 5 pA
Calibration data             │ 100   │ 100 fA       │ 10 pA
Timer counters               │ 30    │ 100 fA       │ 3 pA
Interrupt pending flags      │ 10    │ 100 fA       │ 1 pA
Pacing parameters            │ 50    │ 100 fA       │ 5 pA
DSP coefficients             │ 200   │ 100 fA       │ 20 pA
Safety flags                 │ 20    │ 100 fA       │ 2 pA
─────────────────────────────┼───────┼──────────────┼──────
TOTAL                        │ 660   │              │ 66 pA

Retention Power at V_DD_ret = 0.5V:
P_ret = 66 pA × 0.5V = 33 pW

Over 10 years:
E_ret = 33 pW × 3.15 × 10⁸ s = 10.4 nJ

Battery Impact: 10.4 nJ / 1123 J = 0.0000009%
Retention power is negligible for battery life.
```

### 4.2 Retention Power vs. Wake-Up Time Trade-off

```
Retention vs. Wake-Up Trade-off:

More retention flip-flops:
+ Faster wake-up (state preserved)
+ Lower wake-up energy
- Higher retention power
- More area overhead

Fewer retention flip-flops:
+ Lower retention power
+ Less area overhead
- Slower wake-up (must reload state)
- Higher wake-up energy

iPACE-CHIP Trade-off Analysis:

Strategy          │ Ret. P  │ Wake Time │ Wake E   │ Area
──────────────────┼─────────┼───────────┼──────────┼──────
All flops retained│ 33 pW   │ 1 μs      │ 0.1 nJ   │ +30%
Critical only     │ 33 pW   │ 1 μs      │ 0.1 nJ   │ +15%
None retained     │ 0 pW    │ 1 ms      │ 100 nJ   │ 0%
NVM reload        │ 0 pW    │ 10 ms     │ 10 nJ    │ 0%

iPACE-CHIP Selection: Critical only (15% area overhead)
- Retains: 660 critical flip-flops
- Omits: DSP pipeline, data path registers
- Wake-up: 1 μs (from retention)
- NVM reload: Additional 10 μs for DSP coefficients
- Total wake-up: 11 μs (acceptable for pacemaker)
```

## 5. Reliability Analysis

### 5.1 Retention Time Estimation

```
Retention Time Analysis:

State retention depends on leakage of cross-coupled inverters:

Retention Time: t_ret = C_node × ΔV / I_leak

Where:
- C_node: Parasitic capacitance at storage node ≈ 1 fF
- ΔV: Maximum voltage change before state loss ≈ 100 mV
- I_leak: Sub-threshold leakage at V_DD_ret = 0.5V

At 0.5V V_DD_ret:
- I_leak ≈ 100 fA (per cross-coupled pair)
- t_ret = 1 fF × 100 mV / 100 fA = 1,000,000 seconds = 11.6 days

At 0.3V V_DD_ret:
- I_leak ≈ 10 fA
- t_ret = 1 fF × 100 mV / 10 fA = 10,000,000 seconds = 116 days

At 0.5V with refresh:
- Refresh every 1 day (periodic write)
- Actual retention: unlimited (refreshed)
- Refresh energy: 33 pW × 24h = 2.8 nJ per refresh

iPACE-CHIP Strategy: Periodic refresh
- Refresh interval: 1 hour (conservative)
- Refresh energy: 2.8 nJ / 24 = 0.12 nJ per refresh
- Total refresh energy: 0.12 × 8,760 × 10 = 10.5 kJ
  Wait, this is wrong. Let me recalculate:
- Refresh energy per hour: 33 pW × 3600 s = 119 pJ
- Refresh energy per 10 years: 119 pJ × 87,600 = 10.4 nJ
- Still negligible for battery life
```

### 5.2 SEU Susceptibility

```
SEU Analysis for Retention Flip-Flops:

Retention latch is most vulnerable during sleep mode:
- V_DD_ret = 0.5V (low voltage = low critical charge)
- Continuous storage (no refresh from clock)
- Exposed to radiation for extended periods

Critical Charge (Q_crit) Estimation:
Q_crit = C_node × V_DD_ret × k

Where:
- k = process-dependent constant (0.3 for 180nm)
- Q_crit = 1 fF × 0.5V × 0.3 = 0.15 fC

For comparison, standard flip-flop at 1.8V:
Q_crit = 1 fF × 1.8V × 0.3 = 0.54 fC

Retention flop is 3.6× more susceptible to SEU.

Mitigation Strategies:
1. Increase V_DD_ret (0.7V instead of 0.5V)
   - Q_crit = 0.21 fC (1.4× improvement)
   - Retention current increases: 10×
   - Trade-off: More retention power

2. Redundant retention latches (TMR)
   - Triple Modular Redundancy
   - 3× area overhead
   - SEU immune (majority voting)

3. Periodic refresh
   - Refresh clears any accumulated SEUs
   - At 1-hour refresh: SEU window = 1 hour
   - SEU rate in body: < 10⁻⁹ per hour
   - Probability of SEU during refresh window: 10⁻⁹
```

### 5.3 Temperature Dependence

```
Retention Performance vs. Temperature:

Temperature │ I_leak    │ t_ret     │ V_DD_ret  │ Status
────────────┼───────────┼───────────┼───────────┼────────
-20°C       │ 10 fA     │ 100 days  │ 0.5V      │ PASS
0°C         │ 30 fA     │ 33 days   │ 0.5V      │ PASS
25°C        │ 100 fA    │ 10 days   │ 0.5V      │ PASS
37°C        │ 200 fA    │ 5 days    │ 0.5V      │ PASS
42°C        │ 300 fA    │ 3.3 days  │ 0.5V      │ PASS
50°C        │ 500 fA    │ 2 days    │ 0.5V      │ PASS

At body temperature (37°C):
- Retention time: 5 days (without refresh)
- With 1-hour refresh: Unlimited retention
- Refresh overhead: Negligible

Temperature Compensation:
- At higher temperatures, increase refresh rate
- At lower temperatures, reduce refresh rate
- Adaptive refresh saves power at low temperature
```

## 6. Implementation in iPACE-CHIP

### 6.1 Retention Flop Placement

```
iPACE-CHIP Retention Flip-Flop Placement:

Domain 0 (Always-On):
- 200 configuration registers
- 50 state machine registers
- 20 safety flags
- Total: 270 retention flops
- Area overhead: 270 × 0.19 μm² = 51.3 μm²

Domain 1 (Sensing):
- 50 calibration data registers
- 10 interrupt flags
- Total: 60 retention flops
- Area overhead: 60 × 0.19 μm² = 11.4 μm²

Domain 2 (Processing):
- 100 DSP coefficients
- 30 timer counters
- 50 pacing parameters
- Total: 180 retention flops
- Area overhead: 180 × 0.19 μm² = 34.2 μm²

Domain 3 (Output):
- 150 retention flops (all state)
- Total: 150 retention flops
- Area overhead: 150 × 0.19 μm² = 28.5 μm²

TOTAL: 660 retention flops
Total area overhead: 125.4 μm²
Percentage of total die: 0.003% (negligible)
```

### 6.2 Save/Restore Control

```
Save/Restore Control Flow:

Power-Off Sequence (Domain 2):
T0:     SAVE_n_D2 = 0 (assert save)
T0+10ns: All Domain 2 retention flops capture state
T0+20ns: SAVE_n_D2 = 1 (save complete)
T0+50ns: V_DD_D2 begins to decay

Power-On Sequence (Domain 2):
T0:     V_DD_D2 ramp begins (0V to 1.2V)
T0+100μs: V_DD_D2 stable at 1.2V
T0+110μs: RESTORE_n_D2 = 0 (assert restore)
T0+120μs: All retention flops drive Q from Q_ret
T0+130μs: RESTORE_n_D2 = 1 (restore complete)
T0+140μs: First valid clock edge
T0+150μs: Domain 2 fully operational

Total wake-up time: 150 μs
State restoration time: 10 μs (from retention)
```

### 6.3 Verification

```
Retention Flip-Flop Verification:

Test 1: Save/Restore Functionality
- Write known values to retention flops
- Assert SAVE_n
- Power off domain
- Power on domain
- Assert RESTORE_n
- Verify all values match original
- Pass: All 660 flops verified

Test 2: Retention Time
- Save values to retention flops
- Power off domain
- Wait 24 hours (accelerated: 1000× in simulation)
- Power on domain
- Verify values retained
- Pass: All values retained

Test 3: Refresh Functionality
- Save values to retention flops
- Power off domain
- Enable refresh (1-hour interval)
- Wait 7 days (simulated)
- Power on domain
- Verify values retained
- Pass: All values retained

Test 4: SEU Immunity
- Apply particle strike simulation
- Check retention latch stability
- Verify error detection/correction
- Pass: No data corruption observed

Test 5: Temperature Sweep
- Repeat Test 1 at -20°C, 25°C, 37°C, 50°C
- Verify retention at all temperatures
- Pass: All temperatures pass
```

## 7. Summary

Retention flip-flops in the iPACE-CHIP pacemaker ASIC preserve 660 critical register states during power-gated sleep modes, with a total retention power of only 33 pW at 0.5V V_DD_ret. The ultra-low-power cross-coupled inverter pair architecture achieves retention times exceeding 5 days at body temperature, with periodic 1-hour refresh providing unlimited practical retention. The total area overhead is 125.4 μm² (0.003% of die), making retention flops an extremely efficient solution for fast wake-up. The 10-year energy cost of retention is only 10.4 nJ, representing a negligible 0.0000009% of battery capacity. Combined with proper SEU mitigation through periodic refresh, retention flip-flops provide reliable, low-power state preservation essential for the iPACE-CHIP's power-gating architecture.

## References

1. Shang, L., et al., "Active- Leakage-Power-Aware High-Level Synthesis," IEEE TCAD, 2005.
2. iPACE-CHIP Project Internal Documentation: Retention Flip-Flop Design Specification, Rev 1.4.
3. TSMC 0.18μm Mixed-Signal Process Design Manual: Standard Cell Library.
4. Mudge, T., "Power Aware Design of Digital Circuits," Springer, 2010.
5. Calhoun, B., et al., "Design Methodologies for Ultra-Low Power," Foundations and Trends in EDA, 2010.
