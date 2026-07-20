# Pacemaker System Block Diagram

## 2.1.1 Complete System-Level Block Diagram

### 2.1.1.1 Top-Level Architecture Overview

The iPACE-CHIP implantable pacemaker is a mixed-signal System-on-Chip (SoC) integrating
analog front-end (AFE), digital controller, power management unit (PMU), telemetry
subsystem, and output stage onto a single die. The following block diagram illustrates
the complete system architecture with all major functional blocks and signal interconnects.

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                          iPACE-CHIP — Top-Level Block Diagram                   │
│                                                                                 │
│  ┌──────────────┐    ┌──────────────────────────────────────────────────────┐   │
│  │   EXTERNAL    │    │              iPACE-CHIP SoC                          │   │
│  │   INTERFACE   │    │                                                      │   │
│  │              │    │  ┌─────────────┐  ┌──────────────┐  ┌───────────┐  │   │
│  │  ┌────────┐  │    │  │  ANALOG     │  │   DIGITAL     │  │  POWER    │  │   │
│  │  │Program-│──┼────┼─▶│  FRONT-END  │─▶│   CONTROLLER  │─▶│  MANAGE-  │  │   │
│  │  │ming    │  │    │  │  (AFE)      │  │   (DSP + MCU) │  │  MENT     │  │   │
│  │  │Coil    │  │    │  └─────────────┘  └──────────────┘  │  (PMU)    │  │   │
│  │  └────────┘  │    │         │                │           └─────┬─────┘  │   │
│  │              │    │         │                │                 │        │   │
│  │  ┌────────┐  │    │  ┌─────▼─────┐  ┌──────▼──────┐  ┌──────▼──────┐  │   │
│  │  │Telemetry│──┼───┼─▶│  SENSING   │  │   PACING    │  │  BATTERY    │  │   │
│  │  │Antenna  │  │    │  │  CHANNELS  │  │   OUTPUT    │  │  INTERFACE  │  │   │
│  │  └────────┘  │    │  │            │  │   STAGE     │  │             │  │   │
│  │              │    │  └────────────┘  └──────┬──────┘  └─────────────┘  │   │
│  │  ┌────────┐  │    │                         │                          │   │
│  │  │Magnet  │──┼────┼─────────────────────────▶│                          │   │
│  │  │Sensor  │  │    │  ┌──────────────┐  ┌────▼───────┐                 │   │
│  │  └────────┘  │    │  │  TELEMETRY   │  │   LEAD     │                 │   │
│  │              │    │  │  SUBSYSTEM   │  │   INTERFACE │                 │   │
│  │  ┌────────┐  │    │  │  (RF TX/RX)  │  │   (LVN)    │                 │   │
│  │  │Acceler-│──┼────┼─▶│              │  │             │                 │   │
│  │  │ometer  │  │    │  └──────┬───────┘  └──────┬──────┘                 │   │
│  │  └────────┘  │    │         │                  │                        │   │
│  │              │    │  ┌──────▼───────┐  ┌──────▼──────┐                 │   │
│  │  ┌────────┐  │    │  │  WATCHDOG    │  │  HERMETIC   │                 │   │
│  │  │Battery │──┼────┼─▶│  TIMER (WDT) │  │  SEAL PAD   │                 │   │
│  │  │Cell    │  │    │  └──────────────┘  └─────────────┘                 │   │
│  │  └────────┘  │    │                                                      │   │
│  └──────────────┘    └──────────────────────────────────────────────────────┘   │
│                                                                                 │
│  ┌──────────────────────────────────────────────────────────────────────────┐   │
│  │                    TRANSDUCER / LEAD SYSTEM                              │   │
│  │   ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐              │   │
│  │   │ Atrial   │  │ Ventri-  │  │ Ventri-  │  │ Rate     │              │   │
│  │   │ Lead     │  │ cular    │  │ cular    │  │ Response │              │   │
│  │   │ (RA)     │  │ Lead     │  │ Lead     │  │ Sensor   │              │   │
│  │   │          │  │ (RV)     │  │ (LV)     │  │          │              │   │
│  │   └──────────┘  └──────────┘  └──────────┘  └──────────┘              │   │
│  └──────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 2.1.1.2 Analog Front-End (AFE) Detailed Block Diagram

The AFE is the critical interface between the cardiac tissue and the digital processing
subsystem. It must detect microvolt-level cardiac signals while rejecting interference
from muscle noise, electromagnetic interference (EMI), and electrode polarization.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    ANALOG FRONT-END (AFE) — Detailed View                │
│                                                                         │
│  RA Lead ──┐                                                           │
│            │   ┌────────────┐  ┌──────────┐  ┌──────────┐  ┌───────┐  │
│            ├──▶│ Multiplexer │─▶│ Variable │─▶│ Bandpass │─▶│ ADC   │  │
│  RV Lead ──┤   │ (MUX)      │  │ Gain LNA │  │ Filter   │  │ (SAR) │  │
│            │   │            │  │ 40-80dB  │  │ 0.5-100Hz│  │ 12-bit│  │
│  LV Lead ──┤   │ Ch: 4/8    │  │ Zin>1GΩ  │  │          │  │ 1kHz  │  │
│            │   └──────┬─────┘  └──────────┘  └──────────┘  └───┬───┘  │
│  Ext EGM ──┘         │                                         │      │
│                      │                                         │      │
│  ┌───────────────────▼─────────────────────────────────────────▼───┐  │
│  │                    DIGITAL SIGNAL PROCESSING                     │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────────────┐  │  │
│  │  │ Digital  │  │ Notch    │  │ Wavelet  │  │ Arrhythmia     │  │  │
│  │  │ Filter   │  │ Filter   │  │ Detect   │  │ Classifier     │  │  │
│  │  │ (IIR)    │  │ 50/60Hz  │  │ Engine   │  │ (AF/VT/VF)    │  │  │
│  │  └──────────┘  └──────────┘  └──────────┘  └────────────────┘  │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                                                                         │
│  Sensitivity: 0.25mV (P-wave) / 2.0mV (R-wave)                       │
│  Input Impedance: >1 GΩ  |  CMRR: >80dB  |  Noise: <5µVrms          │
│  Power: <3µW per channel  |  Dynamic Range: >60dB                    │
└─────────────────────────────────────────────────────────────────────────┘
```

### 2.1.1.3 Digital Controller Architecture

The digital controller is the brain of the pacemaker, implementing the pacing algorithm,
timing cycles, mode transitions, and safety monitoring logic.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                   DIGITAL CONTROLLER — Detailed View                     │
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                    PROCESSING CORE                                │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐   │   │
│  │  │ 16-bit   │  │ Hardware │  │ Timer    │  │ Interrupt    │   │   │
│  │  │ RISC MCU │  │ Multi-   │  │ Counter  │  │ Controller   │   │   │
│  │  │ (2MHz)   │  │ plier    │  │ Unit     │  │ (NVIC)       │   │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────────┘   │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                    MEMORY SUBSYSTEM                               │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐   │   │
│  │  │ 32KB     │  │ 8KB      │  │ 2KB      │  │ EEPROM       │   │   │
│  │  │ Flash    │  │ SRAM     │  │ Boot     │  │ 4KB          │   │   │
│  │  │ (Code)   │  │ (Data)   │  │ ROM      │  │ (Params)     │   │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────────┘   │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                    PACING ENGINE                                   │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐   │   │
│  │  │ Timing   │  │ Mode     │  │ Refract. │  │ Safety       │   │   │
│  │  │ Cycle    │  │ State    │  │ Period   │  │ Monitor      │   │   │
│  │  │ Generator│  │ Machine  │  │ Manager  │  │ (Escape      │   │   │
│  │  │          │  │          │  │          │  │  Interval)   │   │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────────┘   │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                    PERIPHERAL INTERFACES                          │   │
│  │  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌────────────┐  │   │
│  │  │ SPI  │ │ I2C  │ │ UART │ │ GPIO │ │ ADC  │ │ Telemetry  │  │   │
│  │  │      │ │      │ │      │ │      │ │ Ctrl │ │ Interface  │  │   │
│  │  └──────┘ └──────┘ └──────┘ └──────┘ └──────┘ └────────────┘  │   │
│  └──────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
```

### 2.1.1.4 Power Management Unit (PMU)

The PMU ensures reliable operation over the 10+ year implant lifetime while managing
power from the lithium battery through various operating modes.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                   POWER MANAGEMENT UNIT (PMU) — Detailed View            │
│                                                                         │
│  Li-I Battery ──┐                                                       │
│  (2.8-3.6V)     │                                                       │
│                 ▼                                                       │
│  ┌──────────────────────┐                                               │
│  │   Battery Monitor     │                                               │
│  │   ┌────────────────┐  │                                               │
│  │   │ Voltage Sense  │──┼──▶ Brown-out Reset (BOR)                    │
│  │   │ (10-bit ADC)   │  │                                               │
│  │   └────────────────┘  │                                               │
│  │   ┌────────────────┐  │                                               │
│  │   │ Current Sense  │──┼──▶ End-of-Life (EOL) Indicator             │
│  │   │ (Op-Amp)       │  │                                               │
│  │   └────────────────┘  │                                               │
│  └───────────┬────────────┘                                               │
│              │                                                           │
│              ▼                                                           │
│  ┌──────────────────────┐  ┌──────────────────────┐                     │
│  │   DC-DC Converter     │  │   Low-Dropout        │                     │
│  │   (Buck/Boost)        │  │   Regulator (LDO)    │                     │
│  │   η > 85%             │  │   Vout: 1.8V/1.2V    │                     │
│  │   Vout: 1.8V          │  │   PSRR > 60dB        │                     │
│  │   Iout: 500µA max     │  │   Iq: <500nA         │                     │
│  └───────────┬────────────┘  └──────────┬────────────┘                     │
│              │                          │                                 │
│              ▼                          ▼                                 │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                      POWER RAILS                                  │   │
│  │  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐  ┌──────────┐  │   │
│  │  │ VDD_A  │  │ VDD_D  │  │ VDD_IO │  │ VDD_RF │  │ VDD_PAD  │  │   │
│  │  │ 1.8V   │  │ 1.2V   │  │ 1.8V   │  │ 1.8V   │  │ 3.0V     │  │   │
│  │  │ Analog │  │ Digital│  │ I/O    │  │ RF     │  │ Output   │  │   │
│  │  └────────┘  └────────┘  └────────┘  └────────┘  └──────────┘  │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ┌──────────────────────┐  ┌──────────────────────┐                     │
│  │   Power-On Reset      │  │   Watchdog Timer      │                     │
│  │   (POR) Circuit       │  │   (External)          │                     │
│  │   Vth: 2.4V           │  │   Period: 8s          │                     │
│  └──────────────────────┘  └──────────────────────┘                     │
└─────────────────────────────────────────────────────────────────────────┘
```

### 2.1.1.5 Telemetry Subsystem

The telemetry subsystem enables non-invasive communication between the implanted
device and the external programmer for parameter configuration and data retrieval.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                   TELEMETRY SUBSYSTEM — Detailed View                    │
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                    RF TRANSCEIVER                                  │   │
│  │                                                                   │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐   │   │
│  │  │ MICS     │  │ ISM Band │  │ Wake-Up  │  │ Low-Power    │   │   │
│  │  │ TX/RX    │  │ TX/RX    │  │ Receiver │  │ Oscillator   │   │   │
│  │  │ 402-405  │  │ 2.4GHz   │  │ (-40dBm) │  │ (32kHz)      │   │   │
│  │  │ MHz      │  │          │  │          │  │              │   │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────────┘   │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                    MODULATION / DEMODULATION                      │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐   │   │
│  │  │ FSK      │  │ ASK/OOK  │  │ CRC-16   │  │ Manchester   │   │   │
│  │  │ Modulator│  │ Demod.   │  │ Generator│  │ Encoder/     │   │   │
│  │  │          │  │          │  │          │  │ Decoder      │   │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────────┘   │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                    TELEMETRY COIL / ANTENNA                       │   │
│  │                                                                   │   │
│  │       ┌─────────────────────────────────────┐                   │   │
│  │       │     Planar Spiral Coil              │                   │   │
│  │       │     Diameter: 20-30mm               │                   │   │
│  │       │     Turns: 10-20                    │                   │   │
│  │       │     L: 1-10µH                       │                   │   │
│  │       │     Q: 20-50                        │                   │   │
│  │       │     Matching Network: π-network     │                   │   │
│  │       └─────────────────────────────────────┘                   │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  Data Rate: 8-256 kbps  |  Range: 2-5cm (skin distance)                │
│  TX Power: <25µW  |  RX Sensitivity: -80dBm                           │
└─────────────────────────────────────────────────────────────────────────┘
```

### 2.1.1.6 Output Stage and Lead Interface

The output stage generates the pacing pulses and interfaces with the cardiac leads,
providing charge balancing and safety isolation.

```
┌─────────────────────────────────────────────────────────────────────────┐
│              OUTPUT STAGE & LEAD INTERFACE — Detailed View               │
│                                                                         │
│  From Digital Controller (pacing command)                               │
│              │                                                          │
│              ▼                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                 PACE OUTPUT GENERATOR                             │   │
│  │                                                                   │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐   │   │
│  │  │ Voltage  │  │ Current  │  │ Pulse    │  │ Charge       │   │   │
│  │  │ DAC      │  │ Source   │  │ Width    │  │ Balancer     │   │   │
│  │  │ 8-bit    │  │ Compliance│  │ Timer    │  │ (Auto-zero)  │   │   │
│  │  │ 0.5-10V  │  │ 25mA max │  │ 50µs-    │  │              │   │   │
│  │  │          │  │          │  │ 1.5ms    │  │              │   │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────────┘   │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                 SAFETY / PROTECTION CIRCUITS                      │   │
│  │                                                                   │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐   │   │
│  │  │ Output   │  │ Over-    │  │ Back-EMF │  │ DC Blocking  │   │   │
│  │  │ Filter   │  │ Voltage  │  │ Clamp    │  │ Capacitor    │   │   │
│  │  │ (RC)     │  │ Limiter  │  │ (TVS)    │  │ (if needed)  │   │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────────┘   │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                 LEAD CONNECTION INTERFACE                          │   │
│  │                                                                   │   │
│  │   Tip ────────┐    Ring ────────┐                                │   │
│  │   (Stimulus)  │    (Sensing)    │                                │   │
│  │               │                 │                                │   │
│  │   ┌───────────▼─────────────────▼───────────┐                   │   │
│  │   │          Switching Matrix                │                   │   │
│  │   │  (Pace/Sense Reconfiguration)           │                   │   │
│  │   │                                          │                   │   │
│  │   │  Mode: Unipolar / Bipolar               │                   │   │
│  │   │  Rds(on): <50Ω                          │                   │   │
│  │   │  Charge Injection: <10pC                 │                   │   │
│  │   └──────────────────────────────────────────┘                   │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  Lead Impedance: 200-2000Ω (nominal 500Ω)                              │
│  Polarization: <500mV afterpace                                        │
│  Shunt Protection: ESD >8kV HBM                                       │
└─────────────────────────────────────────────────────────────────────────┘
```

### 2.1.1.7 Complete Signal Flow Diagram

This diagram traces the complete signal path from cardiac sensing through pacing
output, including all intermediate processing stages.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     COMPLETE SIGNAL FLOW — End-to-End                        │
│                                                                             │
│  CARDIAC    ┌───────┐  ┌───────┐  ┌───────┐  ┌───────┐  ┌───────┐        │
│  TISSUE ───▶│ LEAD  │─▶│ AFE   │─▶│ ADC   │─▶│ DSP   │─▶│ PACING│        │
│             │       │  │       │  │       │  │       │  │ DECIDE│        │
│             │ Z:    │  │ LNA:  │  │ 12b   │  │ FIR/  │  │       │        │
│             │ 500Ω  │  │ 60dB  │  │ 1kHz  │  │ IIR   │  │ Timer │        │
│             │       │  │       │  │       │  │       │  │ Cntr  │        │
│             └───────┘  └───────┘  └───────┘  └───────┘  └───┬───┘        │
│                                                              │            │
│              ┌────────────────────────────────────────────────┘            │
│              │                                                             │
│              ▼                                                             │
│  ┌───────┐  ┌───────┐  ┌───────┐  ┌───────┐  ┌───────┐  ┌───────┐      │
│  │ DAC   │─▶│ PULSE │─▶│ OUTPUT│─▶│ LEAD  │─▶│CARDIAC│─▶│HEART  │      │
│  │ 8-bit │  │ GEN   │  │ STAGE │  │ NETWORK│  │TISSUE│  │BEAT   │      │
│  │       │  │       │  │       │  │       │  │       │  │       │      │
│  │ V:    │  │ W:    │  │ Zout: │  │ Zin:  │  │ R:    │  │       │      │
│  │ 0.5-  │  │ 50µs- │  │ <100Ω │  │ 500Ω  │  │ 1kΩ   │  │       │      │
│  │ 10V   │  │ 1.5ms │  │       │  │       │  │       │  │       │      │
│  └───────┘  └───────┘  └───────┘  └───────┘  └───────┘  └───────┘      │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    TELEMETRY PATH                                    │   │
│  │                                                                      │   │
│  │  ┌───────┐  ┌───────┐  ┌───────┐  ┌───────┐  ┌───────┐           │   │
│  │  │PROG-  │─▶│COIL   │─▶│RX     │─▶│DEMOD  │─▶│DIGITAL│           │   │
│  │  │RAMMER │  │MATCH  │  │LNA    │  │       │  │DECODE │           │   │
│  │  │       │  │NETWORK│  │       │  │FSK/   │  │       │           │   │
│  │  │       │  │       │  │NF:2dB│  │ASK    │  │CRC chk│           │   │
│  │  └───────┘  └───────┘  └───────┘  └───────┘  └───────┘           │   │
│  │                                                                      │   │
│  │  ┌───────┐  ┌───────┐  ┌───────┐  ┌───────┐  ┌───────┐           │   │
│  │  │DIGITAL│─▶│MOD    │─▶│TX     │─▶│COIL   │─▶│PROG-  │           │   │
│  │  │ENCODE │  │       │  │PA     │  │MATCH  │  │RAMMER │           │   │
│  │  │       │  │FSK/   │  │Pout:  │  │NETWORK│  │       │           │   │
│  │  │CRC add│  │ASK    │  │-10dBm │  │       │  │       │           │   │
│  │  └───────┘  └───────┘  └───────┘  └───────┘  └───────┘           │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    POWER PATH                                        │   │
│  │                                                                      │   │
│  │  ┌───────┐  ┌───────┐  ┌───────┐  ┌───────┐  ┌───────┐           │   │
│  │  │Li-    │─▶│PMU    │─▶│DC-DC  │─▶│LDO    │─▶│POWER  │           │   │
│  │  │Ion    │  │Monitor│  │Buck   │  │       │  │RAILS  │           │   │
│  │  │Cell   │  │       │  │η>85%  │  │1.8V   │  │       │           │   │
│  │  │3.0V   │  │BOR/   │  │       │  │1.2V   │  │A/D/I/O│           │   │
│  │  │nom    │  │EOL    │  │       │  │       │  │       │           │   │
│  │  └───────┘  └───────┘  └───────┘  └───────┘  └───────┘           │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.1.1.8 Interconnect and Bus Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                   ON-CHIP BUS ARCHITECTURE                               │
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                    AMBA AHB-LITE BUS (High-Speed)                │   │
│  │                                                                   │   │
│  │  Master: RISC MCU                                               │   │
│  │                                                                   │   │
│  │  Slaves:                                                         │   │
│  │  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────────┐   │   │
│  │  │ Flash  │ │ SRAM   │ │ AHB    │ │ DMA    │ │ Telemetry  │   │   │
│  │  │ 32KB   │ │ 8KB    │ │-APB    │ │Engine  │ │ Controller │   │   │
│  │  │        │ │        │ │ Bridge │ │        │ │            │   │   │
│  │  └────────┘ └────────┘ └────┬───┘ └────────┘ └────────────┘   │   │
│  └─────────────────────────────│───────────────────────────────────┘   │
│                                │                                       │
│  ┌─────────────────────────────▼───────────────────────────────────┐   │
│  │                    APB PERIPHERAL BUS (Low-Speed)                │   │
│  │                                                                   │   │
│  │  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────────┐   │   │
│  │  │ UART   │ │ Timer  │ │ GPIO   │ │ Watch- │ │ EEPROM     │   │   │
│  │  │        │ │ (4ch)  │ │ (8pin) │ │ dog    │ │ Ctrl       │   │   │
│  │  └────────┘ └────────┘ └────────┘ └────────┘ └────────────┘   │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  Bus Width: 16-bit AHB / 8-bit APB                                     │
│  Max Clock: 2MHz (AHB) / 1MHz (APB)                                    │
│  Arbiter: Fixed-priority (MCU only master)                             │
│  Wait States: 0 (flash with prefetch) / 0 (SRAM)                       │
└─────────────────────────────────────────────────────────────────────────┘
```

### 2.1.1.9 Clock and Reset Distribution

```
┌─────────────────────────────────────────────────────────────────────────┐
│                   CLOCK AND RESET DISTRIBUTION                          │
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                    CLOCK SOURCES                                  │   │
│  │                                                                   │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐                      │   │
│  │  │ 32.768kHz│  │ 2.048MHz │  │ 4.0MHz   │                      │   │
│  │  │ RC OSC   │  │ Crystal  │  │ Crystal  │                      │   │
│  │  │ (Low     │  │ (Main)   │  │ (RF)     │                      │   │
│  │  │ Power)   │  │          │  │          │                      │   │
│  │  │ ±2%     │  │ ±10ppm   │  │ ±10ppm   │                      │   │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘                      │   │
│  │       │             │             │                              │   │
│  │       ▼             ▼             ▼                              │   │
│  │  ┌──────────────────────────────────────┐                       │   │
│  │  │         CLOCK MANAGEMENT UNIT         │                       │   │
│  │  │  ┌──────────┐  ┌──────────┐          │                       │   │
│  │  │  │ PLL      │  │ Clock    │          │                       │   │
│  │  │  │ (optional│  │ Divider  │          │                       │   │
│  │  │  │  for     │  │ / Mux    │          │                       │   │
│  │  │  │  high-   │  │          │          │                       │   │
│  │  │  │  speed)  │  │          │          │                       │   │
│  │  │  └──────────┘  └──────────┘          │                       │   │
│  │  └──────────────────────────────────────┘                       │   │
│  │       │         │         │         │                           │   │
│  │       ▼         ▼         ▼         ▼                           │   │
│  │  ┌────────┐┌────────┐┌────────┐┌────────┐                      │   │
│  │  │ CPU    ││ Bus    ││ Timer  ││ RF     │                      │   │
│  │  │ Clock  ││ Clock  ││ Clock  ││ Clock  │                      │   │
│  │  │ 2MHz   ││ 1MHz   ││ 32kHz  ││ 4MHz   │                      │   │
│  │  └────────┘└────────┘└────────┘└────────┘                      │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                    RESET TREE                                     │   │
│  │                                                                   │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐   │   │
│  │  │ Power-On │  │ Brown-Out│  │ Watchdog │  │ Software     │   │   │
│  │  │ Reset    │  │ Reset    │  │ Reset    │  │ Reset        │   │   │
│  │  │ (POR)    │  │ (BOR)    │  │ (WDR)    │  │ (SWR)        │   │   │
│  │  │ Vth:2.4V │  │ Vth:2.6V │  │ T:8s     │  │              │   │   │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └──────┬───────┘   │   │
│  │       │             │             │               │             │   │
│  │       └──────┬──────┴──────┬──────┘               │             │   │
│  │              ▼             ▼                      │             │   │
│  │  ┌──────────────────────────────────────┐        │             │   │
│  │  │         RESET CONTROLLER             │◀───────┘             │   │
│  │  │  - Glitch filter: 100ns              │                      │   │
│  │  │  - Brown-out hysteresis: 100mV       │                      │   │
│  │  │  - Power-good delay: 1ms             │                      │   │
│  │  └──────────────────────────────────────┘                       │   │
│  └──────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
```

### 2.1.1.10 Package and Pin Assignment

```
┌─────────────────────────────────────────────────────────────────────────┐
│                   PACKAGE AND PIN ASSIGNMENT                              │
│                                                                         │
│  Package: Ceramic Titanium (Hermetic)                                   │
│  Dimensions: 38mm × 42mm × 6mm                                         │
│  Pin Count: 12 (hermetic feedthrough)                                  │
│  Seal: Laser-welded titanium case                                      │
│                                                                         │
│            ┌─────────────────────────────┐                              │
│           ╱│                             │╲                             │
│          ╱ │    iPACE-CHIP               │ ╲                            │
│         ╱  │    ┌───────────────────┐    │  ╲                           │
│        │   │    │                   │    │   │                          │
│        │   │    │     iPACE SoC     │    │   │                          │
│        │   │    │                   │    │   │                          │
│        │   │    └───────────────────┘    │   │                          │
│        │   │                             │   │                          │
│         ╲  │  ┌─┐ ┌─┐ ┌─┐ ┌─┐ ┌─┐ ┌─┐ │  ╱                           │
│          ╲ │  │1│ │2│ │3│ │4│ │5│ │6│ │ ╱                             │
│           ╲│  └─┘ └─┘ └─┘ └─┘ └─┘ └─┘ │╱                              │
│            │  ┌─┐ ┌─┐ ┌─┐ ┌─┐ ┌─┐ ┌─┐ │                               │
│            │  │7│ │8│ │9│ │10││11││12│ │                               │
│            │  └─┘ └─┘ └─┘ └──┘└──┘└──┘ │                               │
│            └─────────────────────────────┘                              │
│                                                                         │
│  Pin Assignment:                                                        │
│  ┌──────┬────────────────────┬───────────┬────────────────────────┐    │
│  │ Pin  │ Function           │ Direction │ Notes                  │    │
│  ├──────┼────────────────────┼───────────┼────────────────────────┤    │
│  │  1   │ RA Tip (Atrial)    │ I/O       │ Atrial pacing/sensing  │    │
│  │  2   │ RA Ring (Atrial)   │ I/O       │ Bipolar reference      │    │
│  │  3   │ RV Tip (Ventr.)    │ I/O       │ Ventricular pace/sense │    │
│  │  4   │ RV Ring (Ventr.)   │ I/O       │ Bipolar reference      │    │
│  │  5   │ LV Tip (CRT only)  │ I/O       │ Left ventricular       │    │
│  │  6   │ LV Ring (CRT only) │ I/O       │ Bipolar reference      │    │
│  │  7   │ Can (Case)         │ GND       │ Unipolar return        │    │
│  │  8   │ Telemetry Coil +   │ I/O       │ RF coil positive       │    │
│  │  9   │ Telemetry Coil -   │ I/O       │ RF coil negative       │    │
│  │ 10   │ Battery +          │ PWR       │ Li-I cell positive     │    │
│  │ 11   │ Battery -          │ GND       │ Li-I cell negative     │    │
│  │ 12   │ Magnet/Reed Switch │ INPUT     │ External magnet sense  │    │
│  └──────┴────────────────────┴───────────┴────────────────────────┘    │
│                                                                         │
│  Feedthrough Technology:                                                │
│  - Ceramic-to-metal seal (96% Al₂O₃)                                  │
│  - Platinum-iridium pins (Pt/Ir 90/10)                                │
│  - Hermeticity: <1×10⁻⁹ atm·cc/sec He leak rate                     │
│  - Corrosion-resistant sputtered platinum coating                      │
│                                                                         │
│  Total Current Drain (Nominal): ~10-20µA                               │
│  Battery Capacity: ~1.0 Ah (Li-SVO)                                   │
│  Target Lifetime: >10 years                                            │
└─────────────────────────────────────────────────────────────────────────┘
```

### 2.1.1.11 Critical Design Parameters Summary

| Parameter               | Value                    | Notes                           |
|--------------------------|--------------------------|----------------------------------|
| Supply Voltage           | 2.8–3.6V                | Li-ion/Li-SVO                    |
| Digital Core Voltage     | 1.2V                     | Low-power CMOS                   |
| Analog Supply            | 1.8V                     | Low-noise LDO                    |
| I/O Voltage              | 1.8V / 3.0V             | Telemetry + output stage         |
| Max Clock Frequency      | 2.048 MHz                | Main crystal                     |
| Low-Power Clock          | 32.768 kHz               | RC oscillator                    |
| RF Frequency             | 402–405 MHz (MICS)       | Medical implant comms            |
| ADC Resolution           | 12-bit                   | 1kHz sampling rate               |
| DAC Resolution           | 8-bit                    | Pacing amplitude control         |
| LNA Gain                 | 40–80 dB                 | Programmable                     |
| LNA Input Impedance      | >1 GΩ                    | CMOS gate input                  |
| CMRR                     | >80 dB                   | Differential sensing             |
| Noise Floor              | <5 µVrms                 | Input-referred                   |
| Output Voltage Range     | 0.5–10.0 V               | Programmable                     |
| Output Current           | 25 mA max                | Compliance voltage               |
| Pulse Width Range        | 0.05–1.5 ms              | Programmable                     |
| Lead Impedance Range     | 200–2000 Ω               | Measured in situ                 |
| Battery Capacity         | ~1.0 Ah                  | Li-SVO                           |
| Target Power             | <15 µW average           | 10-year lifetime                 |
| Die Size                 | ~25 mm²                  | 180nm CMOS                       |
| Package Size             | 38×42×6 mm               | Ti hermetic                      |
| Operating Temperature    | 35–41°C (body temp)      | Extended: 0–45°C                 |
| Implant Lifetime         | >10 years                | With battery replacement         |
| Biocompatibility         | ISO 10993 compliant      | USP Class VI                     |
| Safety Standard          | ISO 14708-1 / IEC 60601  | Active implantable               |

### 2.1.1.12 Design Trade-off Matrix

| Design Choice            | Option A           | Option B           | Selected    | Rationale           |
|---------------------------|--------------------|--------------------|-------------|---------------------|
| Process Node              | 180nm              | 65nm               | 180nm       | Reliability, cost   |
| Battery Chemistry         | Li-I               | Li-SVO             | Li-SVO      | Higher energy dens. |
| MCU Architecture          | 8-bit              | 16-bit RISC        | 16-bit      | Code efficiency     |
| ADC Type                  | SAR                | Delta-Sigma        | SAR         | Low power, speed    |
| Telemetry Frequency       | MICS 402MHz        | ISM 2.4GHz         | MICS        | Better tissue prop. |
| Pacing Mode               | VVI only           | DDDR               | DDDR        | Full clinical flex. |
| Lead Type                 | Unipolar           | Bipolar            | Bipolar     | Better noise imm.   |
| Crystal                   | External           | On-chip MEMS       | External    | Better accuracy     |
| Power Architecture        | LDO only           | Buck + LDO         | Buck + LDO  | Better efficiency   |
| Data Encoding             | Manchester         | Bi-phase-L         | Manchester  | Simpler, robust     |

---

*Section 2.1.1 — iPACE-CHIP System-Level Block Diagram*
*Next: Section 2.1.2 — System Requirements Specification*
