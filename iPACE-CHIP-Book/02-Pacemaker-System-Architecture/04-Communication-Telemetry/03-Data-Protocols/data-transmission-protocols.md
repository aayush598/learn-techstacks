# Data Transmission Protocols

## 2.4.3 Packet Structure, Handshaking, Compression, and Electrogram Transmission

The data transmission protocols define how data is packaged, transmitted,
and verified between the implanted pacemaker and the external programmer.
This chapter covers packet structure, handshaking mechanisms, data
compression techniques, and the transmission of intracardiac electrograms.

---

## 2.15.1 Protocol Requirements

### Performance Requirements

| Parameter | Requirement | Unit |
|-----------|------------|------|
| Data rate | 8-128 | kbps |
| Packet error rate | < 10⁻⁵ | — |
| Latency (acknowledgment) | < 100 | ms |
| Maximum packet size | 256 | bytes |
| Handshaking | Stop-and-wait or sliding window | — |
| Flow control | Yes | — |
| Retransmission | Up to 3 | attempts |
| Timeout | 500 | ms |

### Data Types

| Data Type | Size | Frequency | Priority |
|-----------|------|-----------|----------|
| Parameter read/write | 4-32 bytes | On demand | High |
| Status update | 8-16 bytes | Every 100 ms | Medium |
| Diagnostic data | 64-256 bytes | Every 8-24 hr | Low |
| Electrogram data | 1-10 KB | On demand | Medium |
| Event log | 16-64 bytes | On demand | Medium |
| Firmware update | 1-64 KB | Rare | Low |

---

## 2.15.2 Packet Structure

### Standard Packet Format

```
                    STANDARD PACKET FORMAT

  ┌──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┐
  │ PREAM│ SYNC │ LEN  │ ADDR │ SEQ  │ DATA │ CRC  │ POST │
  │ BLE  │ WORD │      │      │ NUM  │      │      │ AMBLE│
  │      │      │      │      │      │      │      │      │
  │ 8 bit│ 16bit│ 8 bit│ 16bit│ 8 bit│ 0-N  │ 16bit│ 8 bit│
  │      │      │      │      │      │ bytes│      │      │
  └──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┘

  Preamble: 0xAA (alternating 10101010 for clock recovery)
  Sync word: 0xB42C (unique 16-bit pattern for packet start)
  Length: Number of data bytes (0-255)
  Address: Device address (16-bit unique ID)
  Sequence number: Packet sequence counter (0-255, wraps)
  Data: Payload data (0-255 bytes)
  CRC: CRC-16-CCITT over address + sequence + data
  Postamble: 0x00 (end-of-packet marker)
```

### Command Packet Format

```
                    COMMAND PACKET FORMAT

  ┌──────┬──────┬──────┬──────┬──────┬──────┬──────┐
  │ PREAM│ SYNC │ LEN  │ ADDR │ CMD  │ DATA │ CRC  │
  │ BLE  │ WORD │      │      │ CODE │      │      │
  │      │      │      │      │      │      │      │
  │ 8 bit│ 16bit│ 8 bit│ 16bit│ 8 bit│ 0-N  │ 16bit│
  │      │      │      │      │      │ bytes│      │
  └──────┴──────┴──────┴──────┴──────┴──────┴──────┘

  Command codes:
    0x01: Read parameter
    0x02: Write parameter
    0x03: Read status
    0x04: Read diagnostic
    0x05: Read electrogram
    0x06: Erase diagnostic
    0x07: Factory reset
    0x80: Acknowledge (ACK)
    0x81: Negative acknowledge (NACK)
    0x82: Ready (RDY)
    0x83: Not ready (NRDY)
```

### Response Packet Format

```
                    RESPONSE PACKET FORMAT

  ┌──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┐
  │ PREAM│ SYNC │ LEN  │ ADDR │ SEQ  │ STATUS│ DATA │ CRC  │
  │ BLE  │ WORD │      │      │ NUM  │      │      │      │
  │      │      │      │      │      │      │      │      │
  │ 8 bit│ 16bit│ 8 bit│ 16bit│ 8 bit│ 8 bit│ 0-N  │ 16bit│
  │      │      │      │      │      │      │ bytes│      │
  └──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┘

  Status codes:
    0x00: Success
    0x01: Out of range
    0x02: Invalid parameter
    0x03: Write protected
    0x04: CRC error
    0x05: Timeout
    0x06: Busy
    0xFF: Error
```

---

## 2.15.3 Handshaking Mechanisms

### Stop-and-Wait ARQ

The simplest handshaking mechanism, used for low-latency commands:

```
                    STOP-AND-WAIT ARQ

  Programmer                          Pacemaker
      │                                    │
      │──── Data Packet (seq=1) ──────────▶│
      │                                    │
      │◀─── ACK (seq=1) ──────────────────│
      │                                    │
      │──── Data Packet (seq=2) ──────────▶│
      │                                    │
      │◀─── ACK (seq=2) ──────────────────│
      │                                    │
      │──── Data Packet (seq=3) ──────────▶│
      │                                    │
      │    (packet lost)                   │
      │                                    │
      │    (timeout 500ms)                 │
      │                                    │
      │──── Retransmit (seq=3) ───────────▶│
      │                                    │
      │◀─── ACK (seq=3) ──────────────────│

  Properties:
  - Simple implementation
  - Low overhead (8 bytes per packet)
  - High latency (must wait for ACK)
  - Throughput: Limited by round-trip time
```

### Sliding Window ARQ

A more efficient mechanism for bulk data transfer:

```
                    SLIDING WINDOW ARQ (Window Size = 4)

  Programmer                          Pacemaker
      │                                    │
      │──── Data (seq=1) ────────────────▶│
      │──── Data (seq=2) ────────────────▶│
      │──── Data (seq=3) ────────────────▶│
      │──── Data (seq=4) ────────────────▶│
      │                                    │
      │◀─── ACK (seq=4, window=8) ────────│
      │                                    │
      │──── Data (seq=5) ────────────────▶│
      │──── Data (seq=6) ────────────────▶│
      │──── Data (seq=7) ────────────────▶│
      │──── Data (seq=8) ────────────────▶│
      │                                    │
      │◀─── ACK (seq=8, window=8) ────────│

  Properties:
  - Higher throughput (pipeline multiple packets)
  - More complex implementation
  - Requires buffer at both ends
  - Throughput: Window size × Packet size / RTT
```

### Handshaking State Machine

```
                    HANDSHAKING STATE MACHINE

  ┌─────────────────────────────────────────────────────────────┐
  │                                                             │
  │  ┌──────────┐    Send     ┌──────────┐    ACK    ┌────────┐│
  │  │          │──packet────▶│          │◀──────────│        ││
  │  │  IDLE    │             │  WAIT    │           │  DONE  ││
  │  │          │◀──timeout──│  ACK     │           │        ││
  │  └────┬─────┘             └────┬─────┘           └────────┘│
  │       │                        │                            │
  │       │                        │ NACK or                    │
  │       │                        │ timeout                    │
  │       │                        ▼                            │
  │       │                   ┌──────────┐                      │
  │       │◀──max retries────│  RETRY   │                      │
  │       │                   │          │                      │
  │       │                   └──────────┘                      │
  │       │                                                     │
  │       │◀─── error ──────────────────────────────────────── │
  │       │                                                     │
  │  ┌────┴─────┐                                              │
  │  │  ERROR   │                                              │
  │  │  HANDLER │                                              │
  │  └──────────┘                                              │
  │                                                             │
  └─────────────────────────────────────────────────────────────┘
```

---

## 2.15.4 Data Compression

### Electrogram Compression

Intracardiac electrograms are large data sets (1-10 KB per episode) that
must be compressed for efficient storage and transmission:

```
                    EGRAM COMPRESSION ALGORITHM

  1. Raw EGM data:
     - 12-bit ADC samples
     - Sample rate: 200-1000 Hz
     - Duration: 2-10 seconds
     - Raw size: 500-10,000 bytes

  2. Delta encoding:
     - Store differences between consecutive samples
     - Delta values are smaller than absolute values
     - Compression ratio: 2-4×

  3. Variable-length coding:
     - Small deltas: 4 bits
     - Medium deltas: 8 bits
     - Large deltas: 12 bits
     - Compression ratio: 1.5-2×

  4. Run-length encoding:
     - Encode runs of identical values
     - Useful for baseline segments
     - Compression ratio: 1.2-1.5×

  Total compression ratio: 3-10×
  Compressed size: 100-1000 bytes per episode
```

### Compression Performance

| Method | Ratio | Complexity | Quality | Use Case |
|--------|-------|-----------|---------|----------|
| Delta encoding | 2-4× | Low | Lossless | All EGM data |
| Delta + VLC | 3-6× | Medium | Lossless | Compressed EGM |
| Delta + RLE | 4-8× | Medium | Lossless | Compressed EGM |
| Wavelet compression | 5-10× | High | Lossy | High compression |
| DCT compression | 5-10× | High | Lossy | High compression |

---

## 2.15.5 Electrogram Transmission

### EGM Data Format

```
                    EGM DATA FORMAT

  ┌──────────────────────────────────────────────────────────────┐
  │  EGM Header (16 bytes)                                       │
  │  ┌──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┐  │
  │  │ Type │ Chan │ Samp │ Dur  │ Gain │ Offs │ Time │ CRC  │  │
  │  │      │      │ Rate │      │      │      │ stamp│      │  │
  │  │ 8 bit│ 8 bit│ 16bit│ 16bit│ 8 bit│ 8 bit│ 32bit│ 16bit│  │
  │  └──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┘  │
  │                                                              │
  │  EGM Data (variable length)                                  │
  │  ┌──────────────────────────────────────────────────────┐   │
  │  │  Compressed EGM samples                              │   │
  │  │  [delta-encoded, variable-length coded]              │   │
  │  └──────────────────────────────────────────────────────┘   │
  │                                                              │
  │  EGM Footer (4 bytes)                                        │
  │  ┌──────┬──────┐                                             │
  │  │ Markers│ CRC │                                             │
  │  │       │     │                                             │
  │  │ 16bit │ 16bit│                                             │
  │  └──────┴──────┘                                             │
  └──────────────────────────────────────────────────────────────┘

  Type: 0x01=Atrial, 0x02=Ventricular, 0x03=Marker
  Channel: 0x01=Near-field, 0x02=Far-field
  Sample rate: 200-1000 Hz
  Duration: 2-10 seconds
  Gain: mV per ADC count
  Offset: DC offset in ADC counts
  Timestamp: Seconds since implant
```

### EGM Transmission Sequence

```
                    EGM TRANSMISSION SEQUENCE

  Programmer                          Pacemaker
      │                                    │
      │──── Request EGM ──────────────────▶│
      │     │                              │
      │     │ Channel: Ventricular         │
      │     │ Duration: 5 seconds          │
      │     │                              │
      │◀─── EGM Header ───────────────────│
      │     │                              │
      │     │ Type: Ventricular            │
      │     │ Sample rate: 500 Hz          │
      │     │ Duration: 5 seconds          │
      │     │ Compressed size: 500 bytes   │
      │     │                              │
      │──── ACK ──────────────────────────▶│
      │                                    │
      │◀─── EGM Data (Part 1) ────────────│
      │     │ [128 bytes]                  │
      │                                    │
      │──── ACK ──────────────────────────▶│
      │                                    │
      │◀─── EGM Data (Part 2) ────────────│
      │     │ [128 bytes]                  │
      │                                    │
      │──── ACK ──────────────────────────▶│
      │                                    │
      │    ... (repeat for all parts)      │
      │                                    │
      │◀─── EGM Footer ───────────────────│
      │     │                              │
      │     │ Markers: [event markers]     │
      │     │ CRC: [16-bit CRC]            │
```

---

## 2.15.6 Flow Control

### Hardware Flow Control

```
                    HARDWARE FLOW CONTROL

  Programmer                          Pacemaker
      │                                    │
      │◀─── RTS (Ready to Send) ──────────│
      │                                    │
      │──── CTS (Clear to Send) ──────────▶│
      │                                    │
      │──── Data Packet ──────────────────▶│
      │                                    │
      │◀─── RTS ──────────────────────────│
      │                                    │
      │──── CTS ──────────────────────────▶│
      │                                    │
      │──── Data Packet ──────────────────▶│
```

### Software Flow Control (XON/XOFF)

```
                    SOFTWARE FLOW CONTROL

  Programmer                          Pacemaker
      │                                    │
      │──── Data Packet ──────────────────▶│
      │──── Data Packet ──────────────────▶│
      │──── Data Packet ──────────────────▶│
      │                                    │
      │◀─── XOFF (Pause) ─────────────────│
      │     (buffer 80% full)              │
      │                                    │
      │    (stop sending)                  │
      │                                    │
      │◀─── XON (Resume) ─────────────────│
      │     (buffer 20% full)              │
      │                                    │
      │──── Data Packet ──────────────────▶│
```

---

## 2.15.7 Multi-Channel Data Transmission

### Simultaneous Channel Transmission

For devices with multiple sensing channels (atrial + ventricular), EGM
data can be transmitted simultaneously:

```
                    MULTI-CHANNEL EGM FORMAT

  ┌──────────────────────────────────────────────────────────────┐
  │  Multi-Channel Header (24 bytes)                             │
  │  ┌──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┐  │
  │  │ Num  │ Ch1  │ Ch1  │ Ch2  │ Ch2  │ Samp │ Dur  │ CRC  │  │
  │  │ Chan │ Type │ Rate │ Type │ Rate │ Rate │      │      │  │
  │  │ 8 bit│ 8 bit│ 16bit│ 8 bit│ 16bit│ 16bit│ 16bit│ 16bit│  │
  │  └──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┘  │
  │                                                              │
  │  Channel 1 Data (Atrial EGM)                                 │
  │  ┌──────────────────────────────────────────────────────┐   │
  │  │  Compressed atrial samples                           │   │
  │  └──────────────────────────────────────────────────────┘   │
  │                                                              │
  │  Channel 2 Data (Ventricular EGM)                            │
  │  ┌──────────────────────────────────────────────────────┐   │
  │  │  Compressed ventricular samples                      │   │
  │  └──────────────────────────────────────────────────────┘   │
  │                                                              │
  │  Channel 3 Data (Marker Channel)                             │
  │  ┌──────────────────────────────────────────────────────┐   │
  │  │  Pacing/sensing markers                              │   │
  │  └──────────────────────────────────────────────────────┘   │
  │                                                              │
  │  Multi-Channel Footer (4 bytes)                              │
  │  ┌──────┬──────┐                                             │
  │  │ Markers│ CRC │                                             │
  │  └──────┴──────┘                                             │
  └──────────────────────────────────────────────────────────────┘
```

---

## 2.15.8 Error Recovery

### Retransmission Strategy

```
                    RETRANSMISSION STRATEGY

  Maximum retries: 3
  Timeout: 500 ms

  Retry 1: Retransmit same packet
  Retry 2: Retransmit with reduced data rate
  Retry 3: Retransmit with maximum error correction

  If all retries fail:
    - Log error in diagnostic memory
    - Notify programmer of transmission failure
    - Abort current operation
    - Return to idle state
```

### Error Recovery State Machine

```
                    ERROR RECOVERY STATE MACHINE

  ┌─────────────────────────────────────────────────────────────┐
  │                                                             │
  │  ┌──────────┐    Send     ┌──────────┐    ACK    ┌────────┐│
  │  │          │──packet────▶│          │◀──────────│        ││
  │  │  READY   │             │  WAIT    │           │  DONE  ││
  │  │          │◀──timeout──│  ACK     │           │        ││
  │  └────┬─────┘             └────┬─────┘           └────────┘│
  │       │                        │                            │
  │       │                        │ NACK or                    │
  │       │                        │ timeout                    │
  │       │                        ▼                            │
  │       │                   ┌──────────┐                      │
  │       │◀──retry 1────────│  RETRY 1 │                      │
  │       │                   │          │                      │
  │       │                   └────┬─────┘                      │
  │       │                        │                            │
  │       │                        │ NACK or                    │
  │       │                        │ timeout                    │
  │       │                        ▼                            │
  │       │                   ┌──────────┐                      │
  │       │◀──retry 2────────│  RETRY 2 │                      │
  │       │                   │          │                      │
  │       │                   └────┬─────┘                      │
  │       │                        │                            │
  │       │                        │ NACK or                    │
  │       │                        │ timeout                    │
  │       │                        ▼                            │
  │       │                   ┌──────────┐                      │
  │       │◀──retry 3────────│  RETRY 3 │                      │
  │       │                   │          │                      │
  │       │                   └────┬─────┘                      │
  │       │                        │                            │
  │       │                        │ failure                    │
  │       │                        ▼                            │
  │       │                   ┌──────────┐                      │
  │       │◀──abort──────────│  ABORT   │                      │
  │       │                   │          │                      │
  │       │                   └──────────┘                      │
  │                                                             │
  └─────────────────────────────────────────────────────────────┘
```

---

## 2.15.9 Real-Time Data Streaming

### Streaming Mode

For real-time monitoring, the pacemaker can stream EGM data continuously:

```
                    REAL-TIME STREAMING FORMAT

  ┌──────┬──────┬──────┬──────┬──────┬──────┐
  │ SYNC │ SEQ  │ CH   │ DATA │ CRC  │ SYNC │
  │      │ NUM  │ ID   │      │      │      │
  │ 8 bit│ 8 bit│ 8 bit│ 16bit│ 16bit│ 8 bit│
  └──────┴──────┴──────┴──────┴──────┴──────┘

  Stream parameters:
    Sample rate: 200-1000 Hz
    Resolution: 8-12 bits
    Channels: 1-3 (atrial, ventricular, marker)
    Data rate: 16-36 kbps per channel
    Latency: < 10 ms (for real-time display)
```

### Streaming vs. Stored EGM

| Feature | Real-Time Streaming | Stored EGM |
|---------|-------------------|-----------|
| Data rate | 16-36 kbps | 1-10 KB total |
| Latency | < 10 ms | > 100 ms |
| Power | Higher (continuous TX) | Lower (burst TX) |
| Range | Shorter (< 1 m) | Longer (> 2 m) |
| Use case | In-clinic monitoring | Remote follow-up |
| Storage | None (display only) | On-device memory |

---

## 2.15.10 Summary

The data transmission protocols provide reliable, efficient communication
between the pacemaker and external programmer:

1. **Packet structure**: Standardized packet format with preamble, sync,
   addressing, sequencing, and CRC ensures reliable data transfer.

2. **Handshaking**: Stop-and-wait ARQ for commands, sliding window ARQ
   for bulk data, with configurable timeout and retry parameters.

3. **Data compression**: Delta encoding with variable-length coding provides
   3-10× compression for electrogram data, enabling efficient storage and
   transmission.

4. **EGM transmission**: Multi-channel electrogram data with marker channels
   can be transmitted in stored or real-time streaming mode.

5. **Error recovery**: Comprehensive error detection (CRC-16) and recovery
   (3 retries with adaptive parameters) ensure reliable data transfer even
   in challenging RF conditions.

6. **Flow control**: Hardware (RTS/CTS) and software (XON/XOFF) flow
   control prevents buffer overflow and ensures smooth data transfer.

These protocols are designed to be robust, efficient, and power-conscious,
balancing the competing requirements of data throughput, reliability, and
battery life in an implantable medical device.
