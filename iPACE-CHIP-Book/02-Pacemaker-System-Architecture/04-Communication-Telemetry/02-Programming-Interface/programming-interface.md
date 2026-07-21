# Programming Interface

## 2.4.2 Magnet Activation, RF Programming Protocol, and Data Encoding

The programming interface provides the mechanism for clinicians to
non-invasively configure the pacemaker parameters, retrieve diagnostic
data, and monitor device status. This chapter covers magnet-triggered
activation, RF programming protocols, data encoding schemes, error
detection, and coil design.

---

## 2.14.1 Programming Interface Requirements

### Functional Requirements

| Parameter | Requirement | Unit |
|-----------|------------|------|
| Magnet activation range | ≥ 5 | cm |
| RF programming range | ≥ 2 | cm |
| Programming time | < 30 | s per parameter set |
| Data rate (programming) | 8-128 | kbps |
| Data rate (telemetry) | 8-128 | kbps |
| Bidirectional communication | Yes | — |
| Error detection | CRC-16 | — |
| Error correction | Optional (FEC) | — |
| Encryption | Optional (AES-128) | — |
| Power consumption | < 5 | mA (during programming) |
| Wake-up time | < 50 | ms |

### Safety Requirements

| Parameter | Requirement | Standard |
|-----------|------------|----------|
| No inadvertent programming | Dual verification | ISO 14708-3 |
| Programming timeout | 30 s inactivity → exit | ISO 14708-3 |
| Parameter validation | Range checking | IEC 60601-1 |
| Emergency stop | Magnet removal stops programming | ISO 14708-3 |
| Audit trail | All programming events logged | ISO 14708-3 |

---

## 2.14.2 Magnet Activation

### Magnet Function

The magnet is the primary mechanism for activating the telemetry link and
switching the pacemaker to a known state:

```
                    MAGNET ACTIVATION SEQUENCE

  Step 1: External magnet placed over implant site
    │
    ▼
  Step 2: Hall sensor detects magnetic field (B > 50 Gauss)
    │
    ▼
  Step 3: Wake-up interrupt generated
    │
    ▼
  Step 4: Pacemaker enters magnet mode:
    ├── Mode switch to asynchronous (DOO/VOO/AOO)
    ├── Rate = magnet rate (typically 80-100 bpm)
    ├── Telemetry link activated
    └── Programming interface enabled
    │
    ▼
  Step 5: External programmer establishes communication
    │
    ▼
  Step 6: Magnet removed → normal operation resumes
```

### Hall Sensor Specifications

| Parameter | Specification | Unit |
|-----------|--------------|------|
| Sensitivity | 10-100 | mV/Gauss |
| Operating range | 10-500 | Gauss |
| Hysteresis | 5-20 | Gauss |
| Supply current | < 100 | µA |
| Response time | < 1 | ms |
| Temperature range | -40 to +85 | °C |
| Package | SOT-23 or smaller | — |

### Magnet Mode Behavior

| Parameter | Magnet Mode | Normal Mode |
|-----------|------------|-------------|
| Pacing mode | DOO/VOO/AOO | DDD/VVI/AAI |
| Pacing rate | Magnet rate (80-100 bpm) | Programmed rate |
| Sensing | Disabled | Enabled |
| Rate adaptation | Disabled | Enabled |
| Telemetry | Enabled | Disabled (sleep) |
| Programming | Enabled | Disabled |

---

## 2.14.3 RF Programming Protocol

### Protocol Stack

```
                    RF PROGRAMMING PROTOCOL STACK

  ┌──────────────────────────────────────────────────────────────┐
  │                     APPLICATION LAYER                         │
  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
  │  │ Parameter│  │ Diag-    │  │ Firmware │  │ Event    │    │
  │  │ Read/Write│ │ nostics  │  │ Update   │  │ Log      │    │
  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘    │
  └──────────────────────────────────────────────────────────────┘
                              │
                              ▼
  ┌──────────────────────────────────────────────────────────────┐
  │                     TRANSPORT LAYER                           │
  │  ┌──────────┐  ┌──────────┐  ┌──────────┐                  │
  │  │ Packet   │  │ Flow     │  │ Error    │                  │
  │  │ Framing  │  │ Control  │  │ Detection│                  │
  │  └──────────┘  └──────────┘  └──────────┘                  │
  └──────────────────────────────────────────────────────────────┘
                              │
                              ▼
  ┌──────────────────────────────────────────────────────────────┐
  │                     DATA LINK LAYER                          │
  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
  │  │ Address- │  │ CRC-16   │  │ Retrans- │  │ Ack/     │    │
  │  │ ing      │  │          │  │ mission  │  │ Nack     │    │
  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘    │
  └──────────────────────────────────────────────────────────────┘
                              │
                              ▼
  ┌──────────────────────────────────────────────────────────────┐
  │                     PHYSICAL LAYER                            │
  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
  │  │ GFSK     │  │ Manchester│ │ Carrier  │  │ Power    │    │
  │  │ Modulation│ │ Encoding │  │ Detect   │  │ Control  │    │
  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘    │
  └──────────────────────────────────────────────────────────────┘
```

### Communication Sequence

```
                    PROGRAMMING SEQUENCE

  Programmer                          Pacemaker
      │                                    │
      │──── Magnet placed ────────────────▶│
      │                                    │
      │◀─── Wake-up acknowledge ───────────│
      │                                    │
      │──── Read device ID ───────────────▶│
      │                                    │
      │◀─── Device ID response ────────────│
      │                                    │
      │──── Read parameter set ───────────▶│
      │                                    │
      │◀─── Parameter set response ────────│
      │                                    │
      │──── Write new parameters ─────────▶│
      │                                    │
      │◀─── Write acknowledge ─────────────│
      │                                    │
      │──── Verify parameters ────────────▶│
      │                                    │
      │◀─── Verification response ─────────│
      │                                    │
      │──── Magnet removed ───────────────▶│
      │                                    │
      │◀─── Normal operation resumes ──────│
```

---

## 2.14.4 Data Encoding

### Manchester Encoding

Manchester encoding is used for clock recovery and DC balance:

```
  Manchester Encoding:

  Data:    1   0   1   1   0   0   1   0
           │   │   │   │   │   │   │   │
           ▼   ▼   ▼   ▼   ▼   ▼   ▼   ▼
  Manc.: ──┐   ┌───┐   └───┐       ┌───┐
           │   │   │       │       │   │
           │   │   │       │       │   │
           └───┘   └───────┘       └───┘

  Manchester: Transition in middle of bit period
  1 = Low→High transition
  0 = High→Low transition

  Advantages:
  - Self-clocking (no separate clock needed)
  - DC balance (equal number of 1s and 0s)
  - Simple implementation

  Disadvantages:
  - 2× bandwidth requirement
  - No error detection capability
```

### Bi-Phase Mark Code (BPMC)

BPMC is an alternative encoding used in some pacemaker telemetry systems:

```
  Bi-Phase Mark Code:

  Data:    1   0   1   1   0   0   1   0
           │   │   │   │   │   │   │   │
           ▼   ▼   ▼   ▼   ▼   ▼   ▼   ▼
  BPMC: ──┐   ┌───┐   └───┐       ┌───┐
          │   │   │       │       │   │
          │   │   │       │       │   │
          └───┘   └───────┘       └───┘

  BPMC: Transition at beginning of every bit period
  Additional transition in middle of bit period for 1
  No additional transition for 0

  Advantages:
  - Self-clocking
  - DC balance
  - Better spectral efficiency than Manchester
```

### Data Framing

```
                    DATA PACKET FORMAT

  ┌──────┬──────┬──────┬──────┬──────┬──────┬──────┐
  │ PREAM│ SYNC │ ADDR │ CMD  │ DATA │ CRC  │ POST │
  │ BLE  │ WORD │      │      │      │      │ AMBLE│
  │      │      │      │      │      │      │      │
  │ 8 bit│ 16bit│ 16bit│ 8 bit│ 0-256│ 16bit│ 8 bit│
  │      │      │      │      │ bytes│      │      │
  └──────┴──────┴──────┴──────┴──────┴──────┴──────┘

  Preamble: 0xAA or 0x55 (alternating bits for clock recovery)
  Sync word: 0xB42C (unique pattern for packet start)
  Address: Device address (16-bit unique ID)
  Command: Command type (read, write, ack, nack, etc.)
  Data: Payload data (0-256 bytes)
  CRC: CRC-16 for error detection
  Postamble: 0x00 (end-of-packet marker)
```

---

## 2.14.5 Parameter Read/Write Protocol

### Read Parameter

```
                    READ PARAMETER SEQUENCE

  Programmer                          Pacemaker
      │                                    │
      │──── Read Request ─────────────────▶│
      │     │                              │
      │     │ Command: 0x01 (Read)         │
      │     │ Parameter ID: 0xXX           │
      │     │                              │
      │◀─── Read Response ─────────────────│
      │     │                              │
      │     │ Status: 0x00 (Success)       │
      │     │ Parameter ID: 0xXX           │
      │     │ Value: [data bytes]          │
      │     │ CRC: [16-bit CRC]            │
```

### Write Parameter

```
                    WRITE PARAMETER SEQUENCE

  Programmer                          Pacemaker
      │                                    │
      │──── Write Request ────────────────▶│
      │     │                              │
      │     │ Command: 0x02 (Write)        │
      │     │ Parameter ID: 0xXX           │
      │     │ Value: [data bytes]          │
      │     │                              │
      │◀─── Write Acknowledge ─────────────│
      │     │                              │
      │     │ Status: 0x00 (Success)       │
      │     │ CRC: [16-bit CRC]            │
      │     │                              │
      │──── Verify Request ───────────────▶│
      │     │                              │
      │     │ Command: 0x03 (Verify)       │
      │     │ Parameter ID: 0xXX           │
      │     │                              │
      │◀─── Verify Response ───────────────│
      │     │                              │
      │     │ Status: 0x00 (Match)         │
      │     │ Value: [data bytes]          │
```

### Parameter Validation

```
  Parameter validation rules:

  1. Range checking:
     If (value < min_value) OR (value > max_value) then
         Reject with error code 0x01 (Out of Range)

  2. Step size checking:
     If ((value - min_value) % step_size) ≠ 0 then
         Reject with error code 0x02 (Invalid Step)

  3. Dependency checking:
     If (parameter A depends on parameter B) AND
        (B not set) then
         Reject with error code 0x03 (Dependency Error)

  4. Safety checking:
     If (value exceeds safety limit) then
         Reject with error code 0x04 (Safety Violation)

  5. Consistency checking:
     If (parameter set is inconsistent) then
         Reject with error code 0x05 (Inconsistency)
```

---

## 2.14.6 CRC-16 Error Detection

### CRC-16-CCITT Polynomial

```
  CRC-16-CCITT: x¹⁶ + x¹² + x⁵ + 1

  Polynomial: 0x1021
  Initial value: 0xFFFF
  Input reflection: No
  Output reflection: No
  Final XOR: 0x0000

  CRC Calculation (software implementation):

  uint16_t crc16(uint8_t *data, uint16_t length) {
      uint16_t crc = 0xFFFF;
      for (uint16_t i = 0; i < length; i++) {
          crc ^= (uint16_t)data[i] << 8;
          for (uint8_t j = 0; j < 8; j++) {
              if (crc & 0x8000)
                  crc = (crc << 1) ^ 0x1021;
              else
                  crc <<= 1;
          }
      }
      return crc;
  }
```

### CRC Performance

| Error Type | Detection Capability |
|-----------|---------------------|
| Single-bit errors | 100% |
| Double-bit errors | 100% |
| Odd number of errors | 100% |
| Burst errors ≤ 16 bits | 100% |
| Burst errors > 16 bits | 99.997% |

---

## 2.14.7 Coil Design for Programming

### Programming Coil Specifications

| Parameter | Specification | Unit |
|-----------|--------------|------|
| Inductance | 1-10 | µH |
| Turns | 10-50 | — |
| Wire gauge | 36-44 AWG | — |
| Core material | Air or ferrite | — |
| Diameter | 20-50 | mm |
| Resistance | < 10 | Ω |
| Q factor | > 10 | @ 400 MHz |
| Coupling coefficient | > 0.01 | — |

### Coil Matching

```
                    PROGRAMMING COIL MATCHING

  Coil ────────┬─────────────────────────────── To RF Transceiver
               │
               ▼
          ┌────────┐
          │  C1    │ (Series capacitor)
          └───┬────┘
              │
              ├─── L1 ────┐ (Shunt inductor)
              │           │
              ▼           │
          ┌────────┐      │
          │  C2    │      │
          └───┬────┘      │
              │           │
             GND          GND

  Matching network: Resonant at 402-405 MHz
  Bandwidth: > 3 MHz (for 10-channel MICS)
  Impedance transformation: 50 Ω → coil impedance
```

---

## 2.14.8 Security Features

### Authentication

```
                    CHALLENGE-RESPONSE AUTHENTICATION

  Programmer                          Pacemaker
      │                                    │
      │──── Challenge Request ────────────▶│
      │                                    │
      │◀─── Random Challenge (128-bit) ────│
      │                                    │
      │──── Encrypted Response ───────────▶│
      │     (AES-128 with shared key)      │
      │                                    │
      │◀─── Authentication Result ─────────│
      │     (Success/Failure)              │
```

### Encryption

| Algorithm | Key Size | Block Size | Use Case |
|-----------|---------|-----------|----------|
| AES-128 | 128 bit | 16 byte | Data encryption |
| AES-256 | 256 bit | 16 byte | High-security applications |
| HMAC-SHA256 | 256 bit | 64 byte | Message authentication |
| CRC-16 | — | — | Error detection (not security) |

---

## 2.14.9 Programming Coil Layout

```
                    PROGRAMMING COIL LAYOUT (Top View)

  ┌─────────────────────────────────────────────────────────────┐
  │                                                             │
  │    ┌─────────────────────────────────────────────────────┐  │
  │    │                                                     │  │
  │    │    ┌─────────────────────────────────────────────┐  │  │
  │    │    │                                             │  │  │
  │    │    │    ┌─────────────────────────────────────┐  │  │  │
  │    │    │    │                                     │  │  │  │
  │    │    │    │    ┌─────────────────────────────┐  │  │  │  │
  │    │    │    │    │                             │  │  │  │  │
  │    │    │    │    │         Coil Area           │  │  │  │  │
  │    │    │    │    │         (5 × 5 mm)          │  │  │  │  │
  │    │    │    │    │                             │  │  │  │  │
  │    │    │    │    └─────────────────────────────┘  │  │  │  │
  │    │    │    │                                     │  │  │  │
  │    │    │    └─────────────────────────────────────┘  │  │  │
  │    │    │                                             │  │  │
  │    │    └─────────────────────────────────────────────┘  │  │
  │    │                                                     │  │
  │    └─────────────────────────────────────────────────────┘  │
  │                                                             │
  │    Feed point ──┐                                           │
  │                │                                           │
  │    Matching network                                          │
  │                │                                           │
  │    To RF transceiver                                         │
  │                                                             │
  └─────────────────────────────────────────────────────────────┘

  Coil parameters:
    Turns: 5
    Trace width: 0.2 mm
    Trace spacing: 0.2 mm
    Outer dimension: 10 × 10 mm
    Inner dimension: 5 × 5 mm
    Substrate: FR-4 or ceramic
```

---

## 2.14.10 Summary

The programming interface provides a robust, safe, and secure mechanism
for non-invasive pacemaker configuration:

1. **Magnet activation**: Provides a simple, reliable mechanism for
   activating the telemetry link and switching to a known state.

2. **RF programming protocol**: Layered protocol stack with packet
   framing, error detection, and flow control ensures reliable data
   transfer.

3. **Data encoding**: Manchester encoding provides self-clocking and
   DC balance for reliable data transmission.

4. **Error detection**: CRC-16 provides 100% detection of single-bit
   and double-bit errors, and 99.997% detection of burst errors.

5. **Security**: Optional AES-128 encryption and challenge-response
   authentication protect against unauthorized programming.

6. **Coil design**: Small, efficient coils (5 × 5 mm) enable reliable
   communication at distances up to 5 cm through body tissue.

The programming interface is designed with patient safety as the primary
concern, with dual verification, parameter validation, timeout protection,
and comprehensive audit logging.
