# Successive Approximation Algorithm for Pacemaker ADC

## Overview

The Successive Approximation Algorithm (SAA) is the decision-making engine inside the SAR ADC that performs binary search to determine the digital representation of an analog input. In the iPACE-CHIP, this algorithm must execute reliably within strict timing constraints to support real-time cardiac sensing and pacing. Understanding the algorithm's implementation, timing, and error handling is essential for designing robust bio-potential digitization.

## Algorithm Fundamentals

### Binary Search Process

The SAA performs binary search by testing each bit from MSB to LSB:

```
Algorithm: Successive Approximation

Input:  Vin (sampled analog voltage)
Output: Dout[N-1:0] (digital code)

Initialize: SAR_reg = 0

For i = N-1 downto 0:
    1. Set bit i of SAR_reg to 1
    2. Generate DAC output: Vdac = DAC(SAR_reg)
    3. Compare: if Vin > Vdac then
                   keep bit i = 1
               else
                   set bit i = 0
    4. Store result in SAR_reg

Return: Dout = SAR_reg
```

### Concrete Example (8-bit)

```
Vin = 0.65V, Vref = 1.0V, N = 8 bits

Step 1: SAR = 10000000, Vdac = 0.500V
        Vin > Vdac (0.65 > 0.50) → Keep bit 7 = 1
        SAR = 10000000

Step 2: SAR = 11000000, Vdac = 0.750V
        Vin < Vdac (0.65 < 0.75) → Clear bit 6 = 0
        SAR = 10000000

Step 3: SAR = 10100000, Vdac = 0.625V
        Vin > Vdac (0.65 > 0.625) → Keep bit 5 = 1
        SAR = 10100000

Step 4: SAR = 10110000, Vdac = 0.6875V
        Vin < Vdac (0.65 < 0.6875) → Clear bit 4 = 0
        SAR = 10100000

Step 5: SAR = 10101000, Vdac = 0.65625V
        Vin < Vdac (0.65 < 0.65625) → Clear bit 3 = 0
        SAR = 10100000

Step 6: SAR = 10100100, Vdac = 0.640625V
        Vin > Vdac (0.65 > 0.640625) → Keep bit 2 = 1
        SAR = 10100100

Step 7: SAR = 10100110, Vdac = 0.6484375V
        Vin > Vdac (0.65 > 0.6484375) → Keep bit 1 = 1
        SAR = 10100110

Step 8: SAR = 10100111, Vdac = 0.65234375V
        Vin < Vdac (0.65 < 0.65234375) → Clear bit 0 = 0
        SAR = 10100110

Final: Dout = 10100110 = 0x0A6 = 166 decimal
Actual: 0.65 / 1.0 × 256 = 166.4 → 166 ✓
Error: 0.4 LSB (within ±0.5 LSB) ✓
```

## State Machine Implementation

### FSM States

```
┌──────────────────────────────────────────────────┐
│                                                  │
│  ┌──────┐   ┌──────┐   ┌──────┐   ┌──────┐     │
│  │ IDLE │──►│SAMPLE│──►│CONV  │──►│ DONE │     │
│  │      │   │      │   │      │   │      │     │
│  └──┬───┘   └──────┘   └──┬───┘   └──┬───┘     │
│     │                      │          │          │
│     │◄─────────────────────┴──────────┘          │
│     │                                            │
│     ▼                                            │
│  ┌──────┐                                        │
│  │ SLEEP│  (optional low-power state)            │
│  └──────┘                                        │
│                                                  │
└──────────────────────────────────────────────────┘
```

### State Descriptions

| State | Duration | Activity | Power Mode |
|-------|----------|----------|------------|
| IDLE | Variable | Wait for trigger | Low power |
| SAMPLE | 1 µs | S/H charges to Vin | Medium |
| CONV | 12 µs | Binary search (12 cycles) | Full |
| DONE | 0.5 µs | Output data, interrupt | Medium |
| SLEEP | Variable | Deep sleep between conv. | Ultra-low |

### Verilog RTL

```verilog
module successive_approximation (
    input  wire        clk,
    input  wire        rst_n,
    input  wire        start,
    input  wire        comp_out,
    output reg         conv_done,
    output reg  [11:0] sar_out,
    output reg         dac_enable,
    output reg  [11:0] dac_code
);

    // State encoding
    localparam IDLE   = 2'b00;
    localparam SAMPLE = 2'b01;
    localparam CONV   = 2'b10;
    localparam DONE   = 2'b11;
    
    reg [1:0]  state, next_state;
    reg [3:0]  bit_count;
    reg [11:0] sar_reg;
    
    // State register
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            state <= IDLE;
        else
            state <= next_state;
    end
    
    // Next state logic
    always @(*) begin
        next_state = state;
        case (state)
            IDLE:   if (start) next_state = SAMPLE;
            SAMPLE:           next_state = CONV;
            CONV:   if (bit_count == 4'd11) next_state = DONE;
            DONE:             next_state = IDLE;
        endcase
    end
    
    // Datapath
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            sar_reg   <= 12'd0;
            bit_count <= 4'd0;
            dac_code  <= 12'd0;
        end else begin
            case (state)
                IDLE: begin
                    sar_reg   <= 12'd0;
                    bit_count <= 4'd0;
                end
                CONV: begin
                    // Set current bit, compare, keep or clear
                    sar_reg[11 - bit_count] <= comp_out;
                    bit_count <= bit_count + 1;
                    dac_code  <= {sar_reg[11:1], comp_out};
                end
            endcase
        end
    end
    
    // Output assignments
    always @(*) begin
        dac_enable = (state == CONV);
        sar_out    = sar_reg;
        conv_done  = (state == DONE);
    end

endmodule
```

## Timing Analysis

### Conversion Timeline

```
Clock:     ──┐  ┌──┐  ┌──┐  ┌──┐  ┌──┐  ┌──┐  ┌──┐
             └──┘  └──┘  └──┘  └──┘  └──┘  └──┘  └──┘

State:     IDLE│SAMPLE│C11│C10│C9 │...│C1 │C0 │DONE│
             │  │      │   │   │   │   │   │   │  │

DAC:       ────│──────│MSB│   │   │   │   │LSB│────│
             │  │      │   │   │   │   │   │   │  │

Comp:      ────│──────│   │   │   │   │   │   │────│
             │  │      ▼   ▼   ▼   ▼   ▼   ▼   │  │

Data:      ────│──────│   │   │   │   │   │  Dout │
             │  │      │   │   │   │   │   │valid │

Total time: T_sample + N × T_clk + T_output
           = 1 µs + 12 × 1 µs + 0.5 µs = 13.5 µs
```

### Clock Period Derivation

```
Minimum clock period limited by:

1. DAC settling time:
   T_dac > 5 × τ_dac
   τ_dac = R_on × C_total = 10 kΩ × 100 pF = 1 ns
   T_dac > 5 ns

2. Comparator resolution:
   T_comp = t再生 + t锁存
   T_comp > 20 ns (for 12-bit accuracy)

3. SAR logic propagation:
   T_logic = t_setup + t_hold + t_prop
   T_logic > 5 ns

4. DAC settling to 0.5 LSB:
   Settling error = Vstep × exp(-T_settle/τ)
   For 0.5 LSB accuracy at 12-bit:
   exp(-T_settle/1ns) < 0.5/4096
   T_settle > 1ns × ln(8192) = 9.0 ns

Worst case: T_clk > max(5, 20, 5, 9) = 20 ns
Design choice: T_clk = 1 µs (relaxed for bio-signal timing)
```

## Error Sources and Mitigation

### Comparator Offset

```
Effect of comparator offset on conversion:

  Offset voltage: Vos
  
  Result: Digital code shifted by Vos/LSB codes
  
  For Vos = 1 mV, LSB = 2.44 µV (12-bit, 10 mV FSR):
    Code shift = 1 mV / 2.44 µV = 410 codes
    This is a gain error, not random noise
    
  Mitigation:
  1. Auto-zeroing comparator (shown in SAR ADC chapter)
  2. Digital calibration (store offset, subtract in digital)
  3. Chopper stabilization of comparator
```

### DAC Mismatch

```
Capacitor mismatch effects:

  For 12-bit SAR with binary-weighted caps:
  
  Worst case: MSB transition (512 × C_unit vs 512 × C_unit)
  
  If MSB cap has +0.1% error:
    ΔC = 0.1% × 512 = 0.512 unit caps
    INL error at MSB transition = 0.512 LSB
    
  DNL error at MSB transition:
    DNL = ΔC/C_unit = 0.512 LSB
    
  Requirement: INL < 0.5 LSB → matching < 0.1% needed
  
  Mitigation:
  - MIM capacitor matching: 0.05-0.2%
  - Common-centroid layout
  - Digital calibration of capacitor errors
```

### Kickback Noise

```
When comparator switches, charge injection disturbs input:

  Q_kickback = C_parasitic × ΔV_comparator
  
  For C_parasitic = 1 fF, ΔV = 1V:
    Q_kickback = 1 fC
    
  Voltage disturbance on DAC:
    ΔV_dac = Q_kickback / C_total = 1 fC / 100 pF = 10 µV
    
  This is 4 LSBs at 12-bit → must be mitigated
  
  Solutions:
  1. Pre-charge comparator before bit decision
  2. Use fully-differential architecture
  3. Add dummy switches for charge cancellation
  4. Allow extra settling time after comparator switch
```

### Clock Jitter

```
Effect of clock jitter on SAA:

  For SAR ADC, jitter during conversion causes:
  - Bit decision errors if jitter is large
  
  Requirement:
    σ_jitter < T_clk / (2 × SNR_linear)
    σ_jitter < 1 µs / (2 × 4096) = 122 ps
    
  On-chip oscillator jitter: typically 100-500 ps
  
  For bio-signal frequencies (250 Hz):
    Jitter effect is negligible (jitter << signal period)
    
  Jitter is critical for:
    - High-frequency input signals
    - Fast-changing signals during conversion
    
  Bio-signal slews slowly: < 5 V/s
  During 12 µs conversion, input changes by:
    ΔV = 5 × 12e-6 = 60 µV = 25 LSBs
    
  This is acceptable if S/H holds value accurately ✓
```

## Multi-Channel Implementation

### Time-Division Multiplexing

For iPACE-CHIP dual-channel (atrial + ventricular):

```
Multiplexed SAR ADC:

  Atrial PGA ──┐
               ├──► S/H ──► SAR ADC ──► Dout
  Vent. PGA ──┘     ▲
                     │
              ┌──────┴──────┐
              │ Channel MUX  │
              │ (sampled at  │
              │  different   │
              │  phases)     │
              └─────────────┘

Timing:
  T_cycle = 500 µs (2 kHz per channel)
  
  Phase 1: Sample Atrial (1 µs)
  Phase 2: Convert Atrial (12 µs)
  Phase 3: Sample Ventricular (1 µs)
  Phase 4: Convert Ventricular (12 µs)
  Phase 5: Idle/Sleep (474 µs)
  
  ADC utilization: (12 + 12) / 500 = 4.8%
  Power saving from duty cycling: 95.2%
```

### Simultaneous Sampling Option

```
Two separate S/H circuits, one ADC:

  Atrial PGA ──► S/H_A ──┐
                         ├──► MUX ──► SAR ADC
  Vent. PGA ──► S/H_V ──┘

  Both S/H sample simultaneously
  Conversions happen sequentially
  
  Advantage: No time skew between channels
  Disadvantage: 2× S/H area and power
  
  Required for:
  - Simultaneous atrial/ventricular timing analysis
  - Differential measurement between chambers
```

## Optimization Techniques

### Redundant Bit Trial

```
Standard SAA: Each bit decided once, no recovery
Redundant SAA: Allow bit re-trial for error correction

Redundant algorithm:
  - Use 1.5 bits per stage (3 comparisons: 0, 0.5, 1)
  - Allows ±1 LSB error correction per stage
  
  Extra clock cycles: N/2 additional (for 12-bit: 6 extra)
  Total cycles: 12 + 6 = 18 cycles
  
  Benefit: Relax comparator offset requirement by 2×
  Trade-off: 50% slower conversion
  
  Application: High-accuracy mode (when timing allows)
```

### Monotonic SAR

```
Modified SAR ensuring monotonic output:

  Property: Dout(i+1) ≥ Dout(i) for increasing Vin
  
  Modified algorithm:
  1. Set bit to 1
  2. If comparator says clear, DON'T clear (hold 1)
  3. This guarantees monotonically increasing codes
  
  Trade-off: Some INL/DNL degradation at code transitions
  
  Benefit:
  - Immune to comparator offset up to ±LSB
  - Simpler calibration
  
  Application: When monotonicity is more critical than linearity
```

### Bootstrapped Switch for S/H

```
Sampling switch with bootstrapped gate drive:

  Standard NMOS switch:
    Ron = 1/(µn × Cox × W/L × (Vgs - Vth))
    Ron varies with Vin → nonlinearity
    
  Bootstrapped switch:
    Vgs = Vboot (constant) regardless of Vin
    Ron = constant → linear sampling
    
  Implementation:
    Vboot capacitor (precharged to VDD)
    Switched to gate during sampling
    
  Required for:
  - Input range > VDD - Vth
  - Linearity > 12 bits
  
  For iPACE-CHIP (10 mV input range):
    Standard switch sufficient (input << VDD)
    Bootstrapping optional (area/power trade-off)
```

## Verification Strategy

### Behavioral Simulation

```
Test cases for SAA verification:

1. DC sweep: 0 to Vref in 1 LSB steps
   - Verify INL < 0.5 LSB
   - Verify DNL < 0.5 LSB
   
2. Sine wave test:
   - Input: 100 Hz sine, 80% FSR amplitude
   - Capture 1024 samples
   - Compute FFT, measure SINAD, SFDR
   
3. Transient test:
   - Step input (0 to FSR)
   - Measure conversion time
   - Verify monotonic response
   
4. Worst-case input:
   - Input at Vref/2 ± 0.5 LSB
   - Verify correct bit decisions at each stage
   
5. Noise test:
   - DC input at mid-scale
   - Measure code histogram
   - Verify Gaussian distribution
```

### Silicon Measurement

```
Post-silicon test procedure:

1. Functional test:
   - Apply known DC voltages
   - Verify digital output codes
   
2. Linearity test:
   - Histogram method with slow ramp
   - 1M+ samples for statistical accuracy
   
3. Dynamic test:
   - Apply clean sine wave from signal generator
   - Measure SINAD with spectrum analyzer
   
4. Power test:
   - Measure supply current during conversion
   - Verify duty cycling power savings
   
5. Temperature test:
   - -40°C, 25°C, 60°C
   - Verify performance across range
```

## Integration with iPACE-CHIP

### Data Flow

```
Electrode → LNA → PGA → Anti-Alias Filter → S/H → SAR ADC
                                                        │
                                                   ┌────┴────┐
                                                   │ SAA     │
                                                   │ Engine  │
                                                   └────┬────┘
                                                        │
                                              ┌─────────┴─────────┐
                                              │ Digital Processing │
                                              │                    │
                                              │ 1. Channel demux   │
                                              │ 2. Digital filter  │
                                              │ 3. Threshold det.  │
                                              │ 4. Pace logic      │
                                              └────────────────────┘
```

### Interrupt Generation

```
ADC completion interrupt:

  conv_done ──┐
              ├──► AND ──► ADC_IRQ to digital controller
  
  Response time:
    ADC_IRQ → Digital processing → Pace decision
    = 0 cycles (direct connection) + processing time
    
  Total sensing latency:
    S/H sample:     1 µs
    Conversion:     12 µs
    Digital detect: 5 µs
    ─────────────────────
    Total:         18 µs
    
  Well within 50 ms requirement for R-wave detection ✓
```

### Calibration Integration

```
Power-up calibration sequence:

  1. Assert cal_start signal
  2. SAR ADC performs self-test:
     a. Apply Vref/2 internally
     b. Run conversion, store result
     c. Compare with expected (0x800)
     d. Calculate offset correction
  3. Sweep DAC through known voltages
  4. Build lookup table for linearity correction
  5. Store calibration data in SRAM (144 bits)
  6. Assert cal_done signal
  
  Total calibration time: ~10 ms
  Power during calibration: Full ADC power (~2 µW)
```

## Summary

The successive approximation algorithm is the core conversion mechanism in the iPACE-CHIP SAR ADC:

| Parameter | Value |
|-----------|-------|
| Resolution | 12 bits |
| Conversion cycles | 12 (plus setup) |
| Clock frequency | 1 MHz |
| Conversion time | 12 µs |
| Clock period | 1 µs |
| FSM states | 4 (IDLE, SAMPLE, CONV, DONE) |
| Calibration storage | 144 bits |
| Multi-channel support | TDM (2 channels) |
| Power during conversion | 2 µW |
| Power during idle | < 10 nW |

The algorithm's simplicity, combined with calibration and careful analog design, provides reliable bio-potential digitization within the strict power and timing constraints of the iPACE-CHIP implantable pacemaker.
