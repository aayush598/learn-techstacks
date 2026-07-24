# 10.2.2 Error Detection and Correction (EDAC) for Pacemaker Memory Systems

## Chapter Overview

Error Detection and Correction (EDAC) codes provide a mathematically rigorous framework for protecting data against corruption. In the iPACE-CHIP, EDAC is the primary protection mechanism for all memory arrays and data paths where full TMR would be prohibitively expensive in terms of area and power. This chapter presents the complete EDAC implementation for the iPACE-CHIP, covering classical Hamming codes, advanced codes for multi-bit error protection, and the specific design considerations for life-critical implantable pacemaker applications.

The iPACE-CHIP's EDAC architecture must balance three requirements: (1) correct single-bit errors that occur at a rate of approximately 10^-10 per hour per bit, (2) detect double-bit errors that would otherwise corrupt patient data silently, and (3) do so with minimal area and power overhead to preserve the battery budget for a 10-year implant lifetime.

---

## 10.2.2.1 Fundamentals of Error Control Codes

### Code Parameters

An error control code is characterized by three parameters: (n, k, d)

- **n** = codeword length (total bits including check bits)
- **k** = data length (original data bits)
- **d** = minimum Hamming distance (minimum number of bit positions that differ between any two valid codewords)

The code can:
- Correct up to **t = floor((d-1)/2)** errors
- Detect up to **d-1** errors

For the iPACE-CHIP's requirements:
- **Single Error Correction (SEC):** d >= 3, t = 1
- **Double Error Detection (DED):** d >= 4, t = 1 (detect 2 errors, correct 1)
- **Double Error Correction (DEC):** d >= 5, t = 2

### Hamming Code Theory

The Hamming code is the foundational SEC-DED code used in the iPACE-CHIP. A binary Hamming code has parameters:

```
(n, k) = (2^m - 1, 2^m - 1 - m)

where m = number of check bits

Examples:
  m = 7:  (127, 120) Hamming code
  m = 6:  (63, 57) Hamming code
  m = 5:  (31, 26) Hamming code
  m = 4:  (15, 11) Hamming code
```

The iPACE-CHIP uses the (39, 32) shortened Hamming code with 7 check bits for 32 data bits, achieving SEC-DED with 21.9% overhead.

### Hamming Code Encoding

The encoding process generates check bits from the data bits using a generator matrix G:

```
Codeword = Data x G (mod 2)

For a (39, 32) code with 7 check bits:
  Data: D[31:0] (32 bits)
  Check bits: C[6:0] (7 bits)
  Codeword: C[6:0], D[31:0] = 39 bits total
```

The check bits are computed as parity sums over specific subsets of data bits. The exact parity equations are derived from the binary representation of the bit positions:

```
For bit position i (1-indexed):
  Bit i is included in check C[j] if and only if
  the j-th bit of i's binary representation is 1.

Example:
  Position 11 = 0b01011
  Bits set: positions 0, 1, 3
  So bit 11 contributes to C[0], C[1], and C[3]
```

### Hamming Code Decoding

The decoding process computes a syndrome vector from the received codeword:

```
Received: R[38:0] = C'[6:0], D'[31:0]

Syndrome S[6:0]:
  S[j] = sum(i where bit j of binary(i) is 1) R[i]  (mod 2)
```

The syndrome interpretation:
- S = 0: No error detected
- S = binary(k): Error at position k (single-bit error, correctable)
- S = non-zero, not power of 2: Multiple-bit error (uncorrectable)

### Extended Hamming Code for SEC-DED

The extended Hamming code adds one overall parity bit for guaranteed double error detection:

```
Overall parity P = D[0] XOR D[1] XOR ... XOR D[31] XOR C[0] XOR ... XOR C[6]

Decoding:
  If S = 0 AND P = 0: No error
  If S != 0 AND P = 1: Single error at position S (correctable)
  If S != 0 AND P = 0: Double error (detectable, not correctable)
  If S = 0 AND P = 1: Parity bit error (correctable)
```

The iPACE-CHIP's extended Hamming code has parameters (40, 32) with 8 check bits for 32 data bits and 25% overhead.

---

## 10.2.2.2 EDAC Implementation for iPACE-CHIP Memory

### Parameter Memory (8 Kbit)

The parameter memory stores all programmable pacemaker parameters. It must be highly reliable (Category A data), non-volatile, and modest in size.

**Memory Organization:**

```
Parameter Memory: 1024 bytes = 256 words x 32 bits/word

Each 32-bit word is protected by extended Hamming SEC-DED:
  Data bits: 32
  Check bits: 8 (7 Hamming + 1 overall parity)
  Codeword: 40 bits

Memory array size with ECC:
  256 words x 40 bits = 10,240 bits = 1280 bytes
Overhead: (10,240 - 8,192) / 8,192 = 25%
```

**ECC Encoder Implementation:**

The ECC encoder is a purely combinational circuit that computes 8 check bits from 32 data bits. The encoder is implemented using XOR gates organized in a tree structure for optimal delay:

```
Encoder delay: 4 gate levels (XOR tree depth for 32 inputs)
Encoder area:  ~200 transistors (8 parity generators x ~25 transistors each)
Encoder power: ~0.1 uW at 16 MHz
```

**ECC Decoder Implementation:**

The decoder computes the syndrome, determines the error location, and corrects the error:

```
Decoder stages:
  1. Syndrome computation: 4 gate levels (XOR tree)
  2. Error location decode: 2 gate levels (7-to-128 decoder)
  3. Error correction: 1 gate level (XOR with correction mask)
  4. Parity check: 1 gate level

Total decoder delay: 8 gate levels
Decoder area: ~800 transistors
Decoder power: ~0.3 uW at 16 MHz
```

### Data SRAM (16 Kbit)

The data SRAM stores intermediate computation results and is protected by the same ECC scheme:

```
Data SRAM: 512 words x 32 bits/word
With ECC: 512 words x 40 bits = 20,480 bits
Overhead: 25% (same as parameter memory)
```

### Instruction SRAM (32 Kbit)

The instruction SRAM stores the firmware code. ECC protection is critical because a corrupted instruction could cause the DSP to execute an incorrect operation:

```
Instruction SRAM: 1024 words x 32 bits/word
With ECC: 1024 words x 40 bits = 40,960 bits
Overhead: 25%
```

Additionally, the instruction SRAM has a CRC-32 checksum stored in a separate 32-bit register. This checksum is verified at power-up and periodically during operation.

### Flash Memory (64 Kbyte)

The flash memory stores the firmware image and parameter backups. Flash is inherently more resistant to SEUs than SRAM, but ECC is still applied:

```
Flash: 16384 words x 32 bits/word
With ECC: 16384 words x 40 bits = 655,360 bits
Overhead: 25%
```

---

## 10.2.2.3 Multi-Bit Error Protection

### The Multi-Bit Upset Problem

As technology scales, the probability of multi-bit upsets (MBUs) increases because physically adjacent memory cells become closer together. A single particle strike can corrupt 2-7 adjacent bits in the iPACE-CHIP's 180nm SRAM.

A standard SEC-DED Hamming code can correct only single-bit errors. If two bits in the same codeword are corrupted, the code detects the error (via the extended parity bit) but cannot correct it.

### Bit Interleaving

The iPACE-CHIP's primary defense against MBUs is bit interleaving. Adjacent physical memory cells are assigned to different codewords:

```
Physical memory layout (without interleaving):
Row 0: W0_bit0, W0_bit1, W0_bit2, ..., W0_bit31, W0_C0, W0_C1, ...
Row 1: W1_bit0, W1_bit1, W1_bit2, ..., W1_bit31, W1_C0, W1_C1, ...

With 4x interleaving:
Row 0: W0_bit0, W4_bit0, W8_bit0, ..., W124_bit0, W128_bit0, ...
Row 1: W0_bit1, W4_bit1, W8_bit1, ..., W124_bit1, W128_bit1, ...
```

The interleaving factor is chosen based on the maximum MBU size:

```
Max MBU at 180nm, LET < 40: 3 bits in the same physical row
Interleaving factor: 4

Result: worst case 3 bits in same row affects 3 different codewords
Each codeword has at most 1 error -> all correctable by SEC-DED
```

### BCH Codes for Enhanced Protection

For applications requiring correction of 2-bit errors within a single codeword, the iPACE-CHIP evaluates BCH (Bose-Chaudhuri-Hocquenghem) codes:

```
BCH(39, 32, 5) code:
  n = 39, k = 32, d = 5
  Can correct up to 2 errors
  Check bits: 7 (same as basic Hamming)
  Overhead: 21.9%

BCH(47, 32, 7) code:
  n = 47, k = 32, d = 7
  Can correct up to 3 errors
  Check bits: 15
  Overhead: 46.9%
```

The BCH(39, 32, 5) has the same overhead as the basic Hamming code but provides DEC (double error correction) capability. The trade-off is higher encoder/decoder complexity.

The iPACE-CHIP uses BCH(39, 32, 5) for the parameter memory (where the highest reliability is required) and standard Hamming SEC-DED for the data and instruction SRAMs.

### Reed-Solomon Codes

For the flash memory, which stores large blocks of data, the iPACE-CHIP evaluates Reed-Solomon codes:

```
RS(32, 24) code over GF(2^8):
  Symbol size: 8 bits
  Data symbols: 24 (192 bits)
  Check symbols: 8 (64 bits)
  Can correct up to 4 symbol errors (32 bits)
  Overhead: 33.3%
```

Reed-Solomon codes are particularly effective against burst errors (where multiple adjacent bits are corrupted), making them well-suited for flash memory where a single cell failure can corrupt an entire page.

---

## 10.2.2.4 EDAC for Data Paths

### Register File ECC

The iPACE-CHIP's register files include ECC on every read and write operation:

**Write Path:**
```
Data_In[31:0] ──► ECC_Encoder ──► Codeword[39:0] ──► Write to Register File
```

**Read Path:**
```
Codeword[39:0] from Register File ──► ECC_Decoder ──► Data_Out[31:0]
                                       │
                                       ├── Syndrome[6:0]
                                       ├── Error_Corrected (flag)
                                       └── Double_Error_Detected (flag)
```

**Error Handling on Read:**
```
If single error detected:
  1. Correct the error in the read data
  2. Rewrite the corrected codeword back to memory (scrubbing)
  3. Increment error counter
  4. Log the error address in diagnostic memory

If double error detected:
  1. Raise non-maskable interrupt
  2. Use last known-good value from redundant storage
  3. Log the error address in diagnostic memory
  4. If in Category A block, trigger safe-state transition
```

### Data Bus ECC

The iPACE-CHIP's internal data bus (32-bit) carries data between functional blocks. ECC protection on the data bus prevents corruption during transmission:

```
Source Block ──► ECC_Encoder ──► Data Bus (32 data + 8 ECC = 40 bits) ──► ECC_Decoder ──► Destination Block
```

The bus ECC uses the same (40, 32) extended Hamming code. The encoder is placed at the source block's output, and the decoder is placed at the destination block's input.

**Bus ECC Timing:**
The bus ECC adds 1 gate level of delay at the source (encoding) and 8 gate levels at the destination (decoding). At 180nm with a 16 MHz clock, this is approximately 0.5 ns encoding + 4 ns decoding = 4.5 ns total, which is well within the 62.5 ns clock period.

### UART/Telemetry Interface ECC

The telemetry data path uses a different ECC scheme due to the serial nature of the data:

```
Transmitter:
  Data[31:0] ──► ECC_Encoder ──► Shift_Register ──► UART_TX
                  (40 bits)       (serial shift)

Receiver:
  UART_RX ──► Shift_Register ──► ECC_Decoder ──► Data[31:0]
               (serial shift)      (40 bits)
```

The UART adds additional CRC-16 protection on top of the ECC:

```
UART Frame:
  [Start Bit][40 ECC bits][CRC-16][Stop Bit]
  
Total frame size: 1 + 40 + 16 + 1 = 58 bits
Effective data rate: 32/58 = 55.2% (vs. 32/32 = 100% without protection)
```

The combined ECC + CRC provides:
- ECC corrects single-bit errors in the data
- CRC detects burst errors in the transmission channel
- Together, they provide a residual error rate below 10^-12 per bit

---

## 10.2.2.5 EDAC Overhead Analysis

### Area Overhead

| Component | Without ECC | With ECC | Overhead |
|---|---|---|---|
| Parameter Memory (8 Kbit) | 8,192 bits | 10,240 bits | 25% |
| Data SRAM (16 Kbit) | 16,384 bits | 20,480 bits | 25% |
| Instruction SRAM (32 Kbit) | 32,768 bits | 40,960 bits | 25% |
| Flash (64 Kbyte) | 524,288 bits | 655,360 bits | 25% |
| Register files | 4,096 bits | 5,120 bits | 25% |
| Data bus (32-bit) | 32 bits | 40 bits | 25% |
| ECC encoder/decoder logic | 0 | ~5,000 transistors | N/A |
| **Total** | **585,728 bits** | **732,280 bits** | **25%** |

The total EDAC overhead is approximately 25% of the memory area plus the encoder/decoder logic. For the iPACE-CHIP, this translates to approximately 0.8 mm² of additional die area — well within the 25 mm² die budget.

### Power Overhead

The ECC encoder/decoder circuits consume dynamic power only when memory is accessed. The access frequency depends on the operational mode:

```
Active pacing mode: 100 memory accesses/second average
  Power: 5,000 transistors x 100 accesses/s x 0.5 transitions/access x C_gate x V^2
       = 5,000 x 100 x 0.5 x 1e-15 x 1.8^2
       = 0.81 uW

Sleep mode: 10 memory accesses/second average
  Power: 0.081 uW

Total EDAC power overhead: ~1 uW (active) to ~0.1 uW (sleep)
```

This is approximately 3% of the total digital power budget (12 uW) — a modest overhead for the significant reliability improvement.

### Reliability Improvement

The EDAC codes dramatically reduce the memory soft error rate:

```
Without ECC:
  SER_memory = 10^-10 per bit per hour
  Total SER = 10^-10 x 585,728 = 5.86 x 10^-5 per hour

With SEC-DED ECC:
  SER_corrected = (SER per bit)^2 x C(n,2) x N_words
               = (10^-10)^2 x 780 x 7,152
               = 5.58 x 10^-16 per hour

With bit interleaving (4x):
  SER_interleaved = (SER per bit)^2 x C(4,2) x N_words
                  = (10^-10)^2 x 6 x 7,152
                  = 4.29 x 10^-17 per hour

Improvement factor: 5.86 x 10^-5 / 4.29 x 10^-17 = 1.37 x 10^12
```

The ECC with interleaving provides a >10^12 improvement in memory reliability — from one error every ~17,000 hours (without ECC) to one error every ~2.3 x 10^12 years (with ECC and interleaving).

---

## 10.2.2.6 EDAC Scrubbing Strategy

### Proactive Scrubbing

Even with ECC correcting single-bit errors, the iPACE-CHIP proactively scrubs memory to prevent error accumulation:

**Hardware Scrub Engine:**

A dedicated hardware scrub engine operates independently of the DSP:

```
Scrub Engine:
  ┌────────────────────┐
  │ Address Generator   │──► Memory Address
  │ (auto-incrementing) │
  └────────┬───────────┘
           │
  ┌────────┴───────────┐
  │ ECC Check & Correct │──► Syndrome → Error Correction
  │ (pipeline stages)   │
  └────────┬───────────┘
           │
  ┌────────┴───────────┐
  │ Write-Back (if      │──► Write corrected data
  │ error detected)     │
  └────────┬───────────┘
           │
  ┌────────┴───────────┐
  │ Error Counter &     │──► Diagnostic Memory
  │ Logging             │
  └────────────────────┘
```

**Scrub Rate:**

The scrub rate is chosen to ensure that the probability of two uncorrectable errors accumulating between scrubs is negligible:

```
For SEC-DED, two errors in the same word between scrubs = uncorrectable
P(2 errors) = (R_SEU_per_word x T_scrub)^2 / 2

For R_SEU_per_word = 10^-14/hr, T_scrub = 10 ms:
P(2 errors) = (10^-14 x 2.78x10^-5)^2 / 2 = 3.86 x 10^-38

This is negligible.
```

**Scrub Priority:**

The scrub engine has three priority levels:
1. **Immediate scrub:** Triggered by ECC error detection (scrub the affected word immediately)
2. **Periodic scrub:** 10 ms interval for all memory (background operation)
3. **Power-on scrub:** Full memory scan at power-up before the device starts pacing

### Passive Scrubbing (Read-Modify-Write)

During normal operation, every memory read operation includes an implicit scrub cycle:

```
Read Operation:
  1. Read codeword from memory
  2. Decode and check ECC
  3. If single error: correct and write back (scrub)
  4. Return corrected data to the requestor
```

This passive scrubbing ensures that every memory location is scrubbed whenever it is accessed, providing additional protection beyond the periodic hardware scrub.

---

## 10.2.2.7 EDAC for Non-Volatile Memory

### Flash Memory ECC

The iPACE-CHIP's flash memory has different error characteristics than SRAM:

**Flash Error Model:**
- **Read disturb:** Repeated reads to a flash page can disturb adjacent cells
- **Program disturb:** Programming one page can disturb adjacent pages
- **Charge leakage:** Over time, stored charge can leak from floating gates (data retention)
- **Wear-out:** Each program/erase cycle degrades the oxide, increasing the error rate

**Flash ECC Requirements:**
Flash errors tend to be bursty (multiple adjacent bits fail together) rather than random (single bits flip independently). This makes burst-correcting codes more effective than random-error-correcting codes.

The iPACE-CHIP uses a concatenated code for flash:

```
Layer 1: BCH(39, 32, 5) for random error correction (corrects 2 random bit errors)
Layer 2: Reed-Solomon RS(32, 24) for burst error correction (corrects 4 symbol errors)

Combined: Corrects any combination of 2 random errors AND 4 burst symbol errors
Overhead: 25% (BCH) + 33.3% (RS) = 58.3% total for flash
```

### Flash ECC Implementation

The flash ECC is implemented in firmware rather than hardware, because:
1. Flash access is infrequent (only during power-up, parameter storage, and firmware updates)
2. The flash controller has sufficient processing time for software ECC
3. The firmware implementation allows flexibility in the ECC algorithm

```
Flash Read Operation (firmware ECC):
  1. Read 32-bit word from flash
  2. Compute BCH syndrome (software)
  3. If correctable error: correct and write back
  4. If uncorrectable: read from redundant flash copy
  5. Verify redundancy match
  6. If both copies uncorrectable: load from SRAM backup
```

### Flash Redundancy

The iPACE-CHIP maintains three copies of critical data in flash:

```
Copy 0 (Primary): Current firmware image and parameters
Copy 1 (Backup): Previous version (retained during firmware update)
Copy 2 (Golden): Factory-programmed original firmware (read-only)
```

If the primary copy is corrupted beyond ECC correction, the device loads from the backup copy. If the backup is also corrupted, the device loads the golden copy and enters a safe default configuration.

---

## 10.2.2.8 EDAC Verification and Testing

### Fault Model Coverage

The iPACE-CHIP's EDAC implementation is verified against the following fault models:

**Single Stuck-At Faults:** Every node in the encoder/decoder is forced to stuck-at-0 and stuck-at-1. The test verifies:
- Encoding produces correct check bits
- Decoding correctly identifies and corrects single-bit errors
- Decoding correctly detects double-bit errors
- No false corrections occur

**Multi-Node Faults:** Two-node stuck-at faults are simulated to verify that double errors are detected (not mis-corrected).

**Timing Faults:** The encoder and decoder are tested at the slowest process corner (slow NMOS, slow PMOS, high temperature, low voltage) to verify that the timing requirements are met.

**Transition Faults:** Every flip-flop in the ECC pipeline is tested for slow-to-rise and slow-to-fall faults.

### Production Test Patterns

The iPACE-CHIP's production test includes comprehensive EDAC verification:

**March Test:** A modified March-CW test is applied to all ECC-protected memories:

```
March-CW Algorithm:
  1. Write all 0s (with correct ECC)
  2. Read all (verify 0s, ECC correct)
  3. Write all 1s (with correct ECC)
  4. Read all (verify 1s, ECC correct)
  5. Write checkerboard pattern (with correct ECC)
  6. Read all (verify checkerboard, ECC correct)
  7. Write inverse checkerboard (with correct ECC)
  8. Read all (verify inverse, ECC correct)
  9. Write all 0s (with correct ECC)
  10. Read all (verify 0s, ECC correct)

Coverage: >99.9% of stuck-at faults in the memory array
```

**ECC Injection Test:**
The production test injects known errors into the ECC codewords and verifies that the encoder/decoder handles them correctly:

```
Test Cases:
  1. No error: verify syndrome = 0, no correction
  2. Single bit error (every position): verify correct correction
  3. Double bit error: verify detection (not correction)
  4. Triple bit error: verify detection (not correction)
  5. Parity bit error: verify correction
  6. All-zero codeword: verify no false error detection
  7. All-one codeword: verify no false error detection
```

---

## 10.2.2.9 EDAC Error Statistics and Diagnostics

### Error Rate Monitoring

The iPACE-CHIP continuously monitors the ECC error rate to detect:
1. Increasing error rates that may indicate aging-related degradation
2. Burst error events that may indicate a radiation event
3. Systematic errors that may indicate a manufacturing defect

**Error Counter Registers:**
```
ECC_Correctable_Errors: 16-bit counter (increments on each single-bit correction)
ECC_Uncorrectable_Errors: 8-bit counter (increments on each double-bit detection)
ECC_Last_Error_Address: 16-bit register (address of the last error)
ECC_Last_Error_Type: 2-bit register (00=none, 01=single, 10=double, 11=parity)
```

**Error Rate Calculation:**
```
Error_Rate = ECC_Correctable_Errors / (Time_Since_PowerOn x Memory_Size)

Normal range: < 10^-10 per bit per hour
Warning threshold: > 10^-8 per bit per hour
Critical threshold: > 10^-6 per bit per hour
```

### Adaptive Scrubbing Rate

The iPACE-CHIP adjusts its scrubbing rate based on the measured error rate:

```
If Error_Rate < 10^-9/hr:   scrub every 100 ms (normal)
If Error_Rate 10^-9 to 10^-7/hr: scrub every 10 ms (fast)
If Error_Rate 10^-7 to 10^-5/hr: scrub every 1 ms (aggressive)
If Error_Rate > 10^-5/hr:   scrub every 100 us + trigger diagnostic alert
```

This adaptive approach ensures that error accumulation is always controlled, regardless of the actual error rate.

---

## 10.2.2.10 Chapter Summary

EDAC codes provide efficient, low-overhead protection for the iPACE-CHIP's memory arrays and data paths. The combination of extended Hamming SEC-DED, bit interleaving, and proactive scrubbing achieves a memory reliability improvement of >10^12.

Key design decisions:

- **Extended Hamming (40, 32)** SEC-DED for all SRAM arrays (25% overhead)
- **BCH(39, 32, 5)** DEC for parameter memory (21.9% overhead, corrects 2 errors)
- **Bit interleaving (4x)** to convert MBUs into correctable single-bit errors
- **Hardware scrub engine** with 10 ms period for background error correction
- **Adaptive scrub rate** based on measured error rate
- **Triple flash redundancy** with concatenated BCH + RS codes
- **Comprehensive error diagnostics** for field monitoring

The total EDAC overhead is approximately 25% memory area and 3% power — a small price for the >10^12 improvement in memory reliability that is essential for a life-critical implantable pacemaker.

The next chapter (10.2.3) covers watchdog timers, which complement EDAC by monitoring the iPACE-CHIP's temporal behavior and detecting functional failures that EDAC cannot catch.

---

## References

1. Hamming, R.W., "Error Detecting and Error Correcting Codes," *Bell System Technical Journal*, Vol. 29, No. 2, 1950.
2. Hsiao, M.Y., "A Class of Optimal Minimum Odd-Weight-Column SEC-DED Codes," *IBM Journal of Research and Development*, Vol. 14, No. 4, 1970.
3. Lin, S., and Costello, D.J., *Error Control Coding*, 2nd Edition, Pearson, 2004.
4. Koob, R., and Laurie, B., "Building a Reliable Flash Storage System for Embedded Applications," *IEEE TC*, 2005.
5. IEC 60601-1:2005, "Medical Electrical Equipment — Part 1: General Requirements for Basic Safety and Essential Performance."
6. JEDEC JESD89A, "Measurement and Reporting of Alpha Particle and Terrestrial Cosmic Ray-Induced Soft Errors in Semiconductor Devices," 2006.
7. Mielke, N., et al., "Bit Error Rate in NAND Flash Memories," *IRPS Proceedings*, 2008.
8. Cui, X., et al., "Concatenated ECC Codes for Flash Memory Error Correction," *IEEE Transactions on Computers*, Vol. 64, No. 5, 2015.
