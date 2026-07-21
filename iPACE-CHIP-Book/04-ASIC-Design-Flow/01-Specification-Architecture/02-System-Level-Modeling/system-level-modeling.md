# System-Level Modeling for iPACE-CHIP ASIC

## 1. Introduction

System-level modeling bridges requirements capture and RTL design by creating executable
specifications of the iPACE-CHIP. These models serve as the golden reference for
functional verification, architecture exploration, and power-performance tradeoffs before
any RTL code is written.

For the iPACE-CHIP, system-level models must capture:

- **Behavioral algorithms** (pacing, sensing, timing)
- **Mixed-signal interactions** (analog front-end + digital processing)
- **Power-state transitions** (sleep, active, telemetry modes)
- **Safety mechanisms** (watchdog, redundancy switching)
- **Timing behavior** (real-time constraints, interrupt latency)

## 2. Modeling Languages and Tools

### 2.1 Language Selection Matrix

```
┌────────────┬──────────────┬────────────┬──────────────┬──────────────┐
│ Language   │ Abstraction  │ Speed      │ Accuracy     │ Use in iPACE │
├────────────┼──────────────┼────────────┼──────────────┼──────────────┤
│ SystemC    │ TLM / RTL    │ Very Fast  │ Medium       │ Top-level    │
│ MATLAB/    │ Algorithm    │ Fast       │ High (float) │ DSP algo     │
│  Simulink  │              │            │              │ exploration  │
│ C/C++      │ Functional   │ Very Fast  │ Low-Medium   │ SW models    │
│ Verilog-AMS│ Analog+Digital│ Medium   │ High         │ AFE modeling │
│ VHDL-AMS   │ Analog+Digital│ Medium   │ High         │ Alternative  │
│ SpecC      │ Architecture  │ Fast      │ Medium       │ Not used     │
│ SCADE      │ Safety-crit  │ Medium     │ High         │ Certifiable  │
└────────────┴──────────────┴────────────┴──────────────┴──────────────┘

  iPACE-CHIP Modeling Strategy:
    Algorithm Level:  MATLAB/Simulink → DSP algorithm validation
    Architecture:     SystemC TLM     → SoC integration & performance
    Mixed-Signal:     Verilog-AMS     → AFE + ADC + output driver
    Safety:           SCADE           → ISO 26262 / IEC 62304 compliance
    Verification:     UVM (SystemVerilog) → RTL vs. reference model
```

## 3. System Architecture Model

### 3.1 Top-Level SystemC Model

```cpp
// iPACE-CHIP Top-Level SystemC Model (simplified)
#include <systemc.h>
#include "analog_front_end.h"
#include "digital_controller.h"
#include "telemetry_unit.h"
#include "power_manager.h"
#include "output_driver.h"
#include "watchdog.h"

SC_MODULE(iPACE_CHIP) {
    // Ports
    sc_in<double>   atrial_input_p;    // Atrial sense +
    sc_in<double>   atrial_input_n;    // Atrial sense -
    sc_in<double>   vent_input_p;      // Ventricular sense +
    sc_in<double>   vent_input_n;      // Ventricular sense -
    sc_out<double>  atrial_output_p;   // Atrial pace +
    sc_out<double>  atrial_output_n;   // Atrial pace -
    sc_out<double>  vent_output_p;     // Ventricular pace +
    sc_out<double>  vent_output_n;     // Ventricular pace -
    sc_inout<float> tele_coil;         // Telemetry coil
    sc_in<bool>     reset_n;           // Active-low reset

    // Internal channels
    sc_fifo<sc_int<12>>  adc_atrial_out;
    sc_fifo<sc_int<12>>  adc_vent_out;
    sc_fifo<pace_cmd_t>  pace_commands;
    sc_signal<bool>      fault_detected;
    sc_signal<power_mode_t> power_mode;

    // Sub-modules
    AnalogFrontEnd      *afe;
    DigitalController   *dctrl;
    TelemetryUnit       *tele;
    PowerManager        *pwr;
    OutputDriver        *out_drv;
    Watchdog            *wdt;

    SC_CTOR(iPACE_CHIP) {
        afe      = new AnalogFrontEnd("afe");
        dctrl    = new DigitalController("dctrl");
        tele     = new TelemetryUnit("tele");
        pwr      = new PowerManager("pwr");
        out_drv  = new OutputDriver("out_drv");
        wdt      = new Watchdog("wdt");

        // AFE connections
        afe->atrial_in_p(atrial_input_p);
        afe->atrial_in_n(atrial_input_n);
        afe->vent_in_p(vent_input_p);
        afe->vent_in_n(vent_input_n);
        afe->adc_out_atrial(adc_atrial_out);
        afe->adc_out_vent(adc_vent_out);

        // Digital controller connections
        dctrl->sense_data_atrial(adc_atrial_out);
        dctrl->sense_data_vent(adc_vent_out);
        dctrl->pace_cmd(pace_commands);
        dctrl->fault_in(fault_detected);

        // Output driver
        out_drv->cmd(pace_commands);
        out_drv->out_p(vent_output_p);
        out_drv->out_n(vent_output_n);

        // Watchdog
        wdt->heartbeat(dctrl->heartbeat);
        wdt->fault_out(fault_detected);

        // Power manager
        pwr->mode(power_mode);
        pwr->subsystem_enable(afe->enable);
        pwr->subsystem_enable(dctrl->enable);
    }

    ~iPACE_CHIP() {
        delete afe;
        delete dctrl;
        delete tele;
        delete pwr;
        delete out_drv;
        delete wdt;
    }
};
```

### 3.2 SystemC TLM Architecture Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│                    iPACE-CHIP SystemC TLM Model                   │
│                                                                   │
│  ┌─────────────┐    sc_fifo<12>    ┌──────────────────────┐     │
│  │             │──────────────────►│                      │     │
│  │  AFE + ADC  │                   │  Digital Controller  │     │
│  │  (Verilog-  │    sc_fifo<12>    │  (SystemC/TLM)      │     │
│  │   AMS)      │──────────────────►│                      │     │
│  │             │                   │  • Pacing State Mch  │     │
│  └─────────────┘                   │  • Sensing Algorithm │     │
│        ▲                           │  • Timing Control    │     │
│        │                           │  • Parameter Store   │     │
│   Analog In                        └──────────┬───────────┘     │
│                                                │                  │
│                                    sc_fifo<cmd>│                  │
│                                                ▼                  │
│  ┌─────────────┐    tlm_socket    ┌──────────────────────┐     │
│  │  Telemetry  │◄────────────────►│  Output Driver       │     │
│  │  Unit       │                   │  (Behavioral)        │     │
│  │  (SystemC)  │                   │                      │     │
│  └─────────────┘                   └──────────────────────┘     │
│        ▲                                    │                     │
│        │                                    │                     │
│  ┌─────┴────────────────────────────────────┴──────────┐        │
│  │              Power Manager (SystemC)                 │        │
│  │  • Mode: SLEEP / ACTIVE / TELEMETRY                  │        │
│  │  • Clock gating, power gating                        │        │
│  │  • Current monitoring                                │        │
│  └─────────────────────────────────────────────────────┘        │
│                                                                   │
│  ┌─────────────────────────────────────────────────────┐        │
│  │              Watchdog (SystemC)                       │        │
│  • Window timer: 500ms ± 10ms                          │        │
│  • Safety state machine: NORMAL → WARN → SAFE → RESET  │        │
│  • Fault injection capability for verification          │        │
│  └─────────────────────────────────────────────────────┘        │
└──────────────────────────────────────────────────────────────────┘
```

## 4. Algorithm-Level Models (MATLAB/Simulink)

### 4.1 Cardiac Sensing Algorithm Model

```matlab
% iPACE-CHIP Sense Algorithm Model (MATLAB)
% Processes raw ADC data to detect cardiac events

classdef PaceSenseModel < handle
    properties
        % Filter coefficients (2nd-order Butterworth BPF)
        b_bpf = [0.0201, 0, -0.0402, 0, 0.0201];
        a_bpf = [1.0, -1.8669, 1.1829, -0.2764, 0.0244];

        % Threshold parameters (programmable)
        sense_threshold = 0.5e-3;  % 0.5 mV default
        auto_threshold_enable = true;
        threshold_decay = 0.99;    % 1% per beat

        % Refractory parameters
        blanking_period = 0.050;   % 50 ms
        refractory_period = 0.250; % 250 ms

        % State variables
        filtered_state = zeros(4, 1);
        last_event_time = -1.0;
        current_threshold = 0.5e-3;
        beat_count = 0;
        rr_intervals = zeros(10, 1);  % Last 10 RR intervals
        rr_index = 1;
    end

    methods
        function [detected, amplitude] = process_sample(obj, sample, timestamp)
            % Bandpass filter
            [obj.filtered_state] = filter(obj.b_bpf, obj.a_bpf, ...
                sample, obj.filtered_state);
            filtered = obj.filtered_state(end);

            % Apply refractory/blanking
            time_since_event = timestamp - obj.last_event_time;
            if time_since_event < obj.blanking_period
                detected = false;
                amplitude = 0;
                return;
            end

            % Adaptive threshold
            amplitude = abs(filtered);
            if obj.auto_threshold_enable && detected
                obj.current_threshold = obj.current_threshold * ...
                    obj.threshold_decay + amplitude * 0.1;
            end

            % Sensing decision
            if time_since_event >= obj.refractory_period && ...
               amplitude > obj.current_threshold
                detected = true;
                obj.last_event_time = timestamp;
                obj.beat_count = obj.beat_count + 1;

                % Update RR interval tracking
                if obj.last_event_time > 0
                    obj.rr_intervals(obj.rr_index) = time_since_event;
                    obj.rr_index = mod(obj.rr_index, 10) + 1;
                end
            else
                detected = false;
            end
        end

        function rate = get_heart_rate(obj)
            avg_rr = mean(obj.rr_intervals(obj.rr_intervals > 0));
            if avg_rr > 0
                rate = 60.0 / avg_rr;  % BPM
            else
                rate = 0;
            end
        end
    end
end
```

### 4.2 Sense Algorithm Signal Flow

```
Input Signal Processing Chain:
═══════════════════════════════════════════════════════════════════

  Electrode    ┌────────┐    ┌────────┐    ┌────────┐    ┌─────┐
  Signal ─────►│ Digital │───►│ BPF    │───►│ Auto   │───►│Comp-│──► Sense
  (from ADC)   │ Filter  │    │        │    │Thresh  │    │arator│    Output
               │ (DC)    │    │0.5-100 │    │ Calc   │    │      │
               └────────┘    │Hz 2nd  │    └────────┘    └──┬──┘
                             │ order   │                     │
                             └────────┘                      │
                                                             │
  Time-Domain View:                                          │
  ▲                                                          │
  │     ╱╲         ╱╲                                       │
  │    ╱  ╲       ╱  ╲      ╱╲                             │
  │───╱────╲─────╱────╲────╱──╲──── Threshold ────────────►│
  │  ╱      ╲   ╱      ╲  ╱    ╲                          │
  │ ╱        ╲ ╱        ╲╱      ╲___                      │
  ├──────────────────────────────────── t ──────────────────┘
  │   │         │         │         │
  │   ▼         ▼         ▼         ▼
  │  SENSE    SENSE    SENSE     SENSE
  │  Event    Event    Event     Event
  │
  │  Refractory Blanking
  │◄─────────────►│
  │    (50 ms)

  Threshold Adaptation:
  threshold[n] = 0.99 × threshold[n-1] + 0.1 × last_amplitude[n]
                 ─────────────────────────────────────────────────
  This provides slow adaptation to changing signal conditions
  while preventing threshold runaway after single large artifact.
```

## 5. Mixed-Signal Model (Verilog-AMS)

### 5.1 Analog Front-End Model

```verilog-ams
// iPACE-CHIP Analog Front-End (Verilog-AMS behavioral model)
`include "disciplines.vams"

module iPACE_AFE #(
    parameter GAIN_MIN    = 40,    // dB minimum gain
    parameter GAIN_MAX    = 80,    // dB maximum gain
    parameter BANDWIDTH   = 100,   // Hz upper cutoff
    parameter NOISE_FLOOR = 5e-6   // 5 µVrms input-referred noise
)(
    input  real   vin_p,      // Positive electrode input
    input  real   vin_n,      // Negative electrode input
    input  real   vref,       // Reference voltage (mid-supply)
    input  [7:0]  gain_ctrl,  // Gain control word
    input  [7:0]  bw_ctrl,    // Bandwidth control word
    output real   adc_data,   // ADC output (normalized ±1.0)
    input  clk,               // ADC clock
    input  enable             // Power enable
);

    real differential_in;
    real gain_linear;
    real bandwidth_hz;
    real filtered_out;
    real noise_gen;

    // Gain calculation
    initial begin
        gain_linear = 10.0 ** ((GAIN_MIN + gain_ctrl * (GAIN_MAX - GAIN_MIN) / 255.0) / 20.0);
        bandwidth_hz = 10.0 + bw_ctrl * (BANDWIDTH - 10.0) / 255.0;
    end

    // Differential input with common-mode rejection
    assign differential_in = (vin_p - vin_n) * gain_linear;

    // Simple RC filter model (1st order approximation)
    // Actual design uses 2nd order Sallen-Key topology
    analog begin
        // Bandwidth-dependent time constant
        @(initial_step) begin
            filtered_out = 0;
        end

        filtered_out = filtered_out + (differential_in - filtered_out) *
                       (1.0 / (bandwidth_hz * 2.0 * 3.14159));

        // Add noise contribution (thermal noise model)
        noise_gen = NOISE_FLOOR * `$random` / 32767.0;

        // ADC sampling (ideal quantizer behavioral model)
        @(posedge clk) begin
            if (enable) begin
                adc_data = (filtered_out + noise_gen) / (gain_linear * 2.5);
                // Clip to ±1.0
                if (adc_data > 1.0) adc_data = 1.0;
                if (adc_data < -1.0) adc_data = -1.0;
            end
        end
    end

endmodule
```

### 5.2 Output Driver Behavioral Model

```verilog-ams
// iPACE-CHIP Output Driver (Verilog-AMS behavioral model)
module iPACE_OUTPUT_DRIVER #(
    parameter VDD_PULSE    = 5.0,   // Pulse voltage (V)
    parameter R_LOAD       = 500.0, // Electrode impedance (Ω)
    parameter I_MAX        = 15e-3, // Maximum current limit (mA)
    parameter PW_MIN       = 0.05e-3, // Minimum pulse width (s)
    parameter PW_MAX       = 1.5e-3   // Maximum pulse width (s)
)(
    input  [2:0]  amplitude_ctrl,  // 0.5V to 7.5V in 1V steps
    input  [3:0]  pulse_width_ctrl, // 0.05ms to 1.5ms
    input         pace_trigger,
    input         enable,
    output real   i_out,           // Output current
    output real   v_out,           // Output voltage
    output reg    fault_flag       // Over-current fault
);

    real actual_voltage;
    real actual_width;
    real pulse_start_time;
    reg  pulse_active;

    // Decode control words to physical values
    always @(amplitude_ctrl) begin
        actual_voltage = 0.5 + amplitude_ctrl * 1.0; // 0.5V to 1.5V+
        if (actual_voltage > 7.5) actual_voltage = 7.5;
    end

    always @(pulse_width_ctrl) begin
        actual_width = 0.05e-3 + pulse_width_ctrl * 0.1e-3;
        if (actual_width > PW_MAX) actual_width = PW_MAX;
    end

    // Pulse generation with current limiting
    analog begin
        @(posedge pace_trigger) begin
            if (enable) begin
                pulse_active = 1;
                pulse_start_time = $abstime;
            end
        end

        // Monitor for end of pulse or fault
        if (pulse_active) begin
            v_out = actual_voltage;
            i_out = v_out / R_LOAD;

            // Over-current detection
            if (i_out > I_MAX) begin
                i_out = I_MAX;
                fault_flag = 1;
                v_out = i_out * R_LOAD;
            end

            // Check pulse width expiry
            if (($abstime - pulse_start_time) >= actual_width) begin
                pulse_active = 0;
                v_out = 0;
                i_out = 0;
                fault_flag = 0;
            end
        end else begin
            v_out = 0;
            i_out = 0;
        end
    end

endmodule
```

## 6. Power State Model

### 6.1 State Machine Definition

```
iPACE-CHIP Power State Machine:
═══════════════════════════════════════════════════════════════

  ┌─────────────────────────────────────────────────────────────┐
  │                    POWER STATES                              │
  │                                                              │
  │  ┌──────────┐   Pacing Event    ┌──────────────┐           │
  │  │          │──────────────────►│              │           │
  │  │  SLEEP   │◄──────────────────│   ACTIVE     │           │
  │  │          │   2ms timeout     │              │           │
  │  │ VDD: 0.5 │                   │ VDD: 50 µA  │           │
  │  │ µA       │                   │ peak         │           │
  │  │ Clk: OFF │                   │ Clk: ON      │           │
  │  │ AFE: OFF │                   │ AFE: ON      │           │
  │  │ DSP: OFF │                   │ DSP: ON      │           │
  │  └──────────┘                   └──────────────┘           │
  │       ▲                                │                    │
  │       │ Sleep Timer         Tele Rx Cmd │                   │
  │       │                                ▼                    │
  │  ┌──────────┐   Sleep Cmd     ┌──────────────┐            │
  │  │          │◄────────────────│              │            │
  │  │ TELEM    │                 │  TELE_TX     │            │
  │  │ RX       │                 │              │            │
  │  │          │                 │ VDD: 200 µA  │            │
  │  │ VDD: 200 │                 │ peak          │            │
  │  │ µA       │                 │ Carrier: ON   │            │
  │  │ PLL: ON  │                 │ PLL: ON       │            │
  │  └──────────┘                 └──────────────┘            │
  │       │                                │                    │
  │       └────────────────────────────────┘                    │
  │                  Sleep Command                              │
  └─────────────────────────────────────────────────────────────┘

  State Encoding (3-bit one-hot):
    SLEEP    = 3'b001
    ACTIVE   = 3'b010
    TELE_RX  = 3'b100
    TELE_TX  = 3'b101
    SAFE     = 3'b110  (fault state)
```

### 6.2 Power State Transition Table

```
┌────────────┬──────────────┬────────────────┬─────────────────────┐
│ Current    │ Next State   │ Trigger        │ Clock/Gate Changes  │
│ State      │              │                │                     │
├────────────┼──────────────┼────────────────┼─────────────────────┤
│ SLEEP      │ ACTIVE       │ Sleep timer    │ Un-gate AFE, DSP    │
│            │              │ expiry (33ms)  │ Enable BPF clock    │
├────────────┼──────────────┼────────────────┼─────────────────────┤
│ ACTIVE     │ SLEEP        │ 2ms no activity│ Gate AFE, DSP clock │
│            │              │                │ Retain SRAM state   │
├────────────┼──────────────┼────────────────┼─────────────────────┤
│ ACTIVE     │ TELE_RX      │ Tele carrier   │ Enable PLL          │
│            │              │ detected       │ Enable UART clock   │
├────────────┼──────────────┼────────────────┼─────────────────────┤
│ ACTIVE     │ SAFE         │ Watchdog fault │ Disable output drv  │
│            │              │                │ Enable safe pacing  │
├────────────┼──────────────┼────────────────┼─────────────────────┤
│ TELE_RX    │ ACTIVE       │ Tele session   │ Disable PLL         │
│            │              │ end / timeout  │ Gate UART clock     │
├────────────┼──────────────┼────────────────┼─────────────────────┤
│ TELE_RX    │ TELE_TX      │ Write command  │ Enable TX carrier   │
│            │              │ received       │                     │
├────────────┼──────────────┼────────────────┼─────────────────────┤
│ SAFE       │ SLEEP        │ Reset / power  │ Reset all logic     │
│            │              │ cycle          │                     │
└────────────┴──────────────┴────────────────┴─────────────────────┘
```

## 7. Timing Model

### 7.1 Real-Time Constraint Model

```
iPACE-CHIP Real-Time Timing Budget:
═══════════════════════════════════════════════════════════════

  Pacing Cycle Timeline (at 72 bpm = 833.33 ms):
  ┌────────────────────────────────────────────────────────────┐
  │ 0ms     100ms    200ms    300ms    400ms    500ms  833ms  │
  │  │        │        │        │        │        │      │     │
  │  │◄─ Atrial Sense ─►│◄─ AV Delay ──►│◄─ Vent Pace ─►│    │
  │  │   Window          │  (150ms typ)  │   Window        │    │
  │  │                   │               │                  │    │
  │  ├───────────────────┴───────────────┴──────────────────┤    │
  │  │              Refractory Periods                       │    │
  │  │  Atrial Refractory: |████| 250ms                     │    │
  │  │  Vent Refractory:           |████████| 300ms          │    │
  │  └──────────────────────────────────────────────────────┘    │
  └────────────────────────────────────────────────────────────┘

  Computation Timing Constraints:
    ┌─────────────────────────┬──────────────┬──────────────────┐
    │ Operation               │ Budget       │ Criticality      │
    ├─────────────────────────┼──────────────┼──────────────────┤
    │ ADC Sample → Sense Out  │ ≤ 5 ms      │ High             │
    │ Sense → Pace Decision   │ ≤ 10 ms     │ Critical         │
    │ Pace Cmd → Output Valid │ ≤ 100 µs    │ Critical         │
    │ Watchdog Window Check   │ ≤ 1 ms      │ Safety-critical  │
    │ Telemetry Command Exec  │ ≤ 50 ms     │ Medium           │
    │ Parameter Update        │ ≤ 10 ms     │ Medium           │
    │ Reset → Safe Pacing     │ ≤ 100 ms    │ Safety-critical  │
    └─────────────────────────┴──────────────┴──────────────────┘

  Clock Frequency Derivation:
    Core clock = max(operation_frequency) × safety_margin
               = 1 / 100µs × 1.5
               = 15,000 Hz = 15 kHz minimum

    Design choice: f_clk = 32.768 kHz (standard watch crystal)
    Period = 30.5 µs → satisfies all timing constraints ✓

    Alternative: f_clk = 1.024 MHz for telemetry
    Used only during telemetry mode (duty-cycled)
```

## 8. Safety Model

### 8.1 Safety State Machine (Formal Model)

```
Safety State Machine for Fault Handling:
═══════════════════════════════════════════════════════════════

  States: NORMAL, CAUTION, WARNING, SAFE_MODE, CRITICAL_SHUTDOWN

  ┌─────────────┐  All OK   ┌─────────────┐
  │   NORMAL     │◄─────────│  (initial)   │
  │  Normal      │          │              │
  │  Pacing      │          └─────────────┘
  └──────┬──────┘
         │ Non-critical fault
         ▼
  ┌─────────────┐  Resolved ┌─────────────┐
  │  CAUTION    │◄─────────►│  WARNING    │
  │  Log fault  │           │  Reduce     │
  │  Continue   │           │  Parameters │
  └─────────────┘           └──────┬──────┘
                                   │ Persistent fault
                                   ▼
  ┌─────────────┐  Timeout   ┌─────────────┐
  │  SAFE_MODE  │◄──────────│  CRITICAL   │
  │  Asynch     │            │  SHUTDOWN   │
  │  80ppm pace │            │  No output  │
  │  Max energy │            │  Require    │
  │  No sensing │            │  reset      │
  └─────────────┘            └─────────────┘

  Fault Conditions:
  ┌────────────────────────┬─────────────────────┬────────────┐
  │ Fault                  │ Detection Method     │ Response   │
  ├────────────────────────┼─────────────────────┼────────────┤
  │ Output over-current    │ Current sense        │ WARNING    │
  │ Clock frequency error  │ Redundant counter    │ CAUTION    │
  │ ADC saturation         │ Self-test            │ WARNING    │
  │ SRAM ECC error         │ ECC checker          │ CAUTION    │
  │ Watchdog timeout       │ HW watchdog          │ SAFE_MODE  │
  │ Double-bit ECC error   │ ECC checker          │ CRITICAL   │
  │ Power supply brownout  │ Brownout detect      │ SAFE_MODE  │
  │ Temperature excursion  │ On-chip sensor       │ WARNING    │
  │ Radiation event (SEU)  │ Redundancy check     │ CAUTION    │
  └────────────────────────┴─────────────────────┴────────────┘
```

## 9. Verification Model Integration

### 9.1 Verification Architecture

```
Reference Model Integration Flow:
═══════════════════════════════════════════════════════════════

  ┌─────────────────┐     ┌─────────────────┐
  │   MATLAB/       │     │   SystemC TLM   │
  │   Simulink      │     │   Model         │
  │   Algorithm     │     │   (Architecture)│
  └────────┬────────┘     └────────┬────────┘
           │                       │
           │  C-Code Gen           │  TLM-to-RTL
           │  (Embedded Coder)     │  Refinement
           ▼                       ▼
  ┌─────────────────┐     ┌─────────────────┐
  │   C Reference   │     │   RTL Design    │
  │   Model (CRC)   │     │   (Verilog)     │
  │                 │     │                  │
  └────────┬────────┘     └────────┬────────┘
           │                       │
           │   vsim                 │   synthesis
           │                       │
           ▼                       ▼
  ┌─────────────────┐     ┌─────────────────┐
  │   UVM Testbench │     │   Gate-Level    │
  │   (SystemVerilog)│     │   Netlist       │
  │                  │     │                  │
  │  ┌──────────────┐│     │  ┌──────────────┐│
  │  │DUT (RTL)     ││     │  │Gate-Level    ││
  │  │     vs       ││     │  │DUT           ││
  │  │CRC Model     ││     │  │     vs       ││
  │  │(reference)   ││     │  │CRC Model     ││
  │  └──────────────┘│     │  └──────────────┘│
  └─────────────────┘     └─────────────────┘

  Signoff Criteria:
  • RTL vs CRC:     100% instruction/functional coverage
  • Gate vs RTL:    0 failures in 10,000+ random seeds
  • Gate vs CRC:    0 failures at 3 corners (fast, typ, slow)
  • Assertion:      Zero vacuous passes on safety assertions
```

## 10. Model Parameter Summary

```
┌──────────────────────────┬──────────┬───────────┬──────────────┐
│ Parameter                │ Value    │ Unit      │ Source       │
├──────────────────────────┼──────────┼───────────┼──────────────┤
│ Core Clock Frequency     │ 32.768   │ kHz       │ Crystal      │
│ Telemetry Clock          │ 1.024    │ MHz       │ PLL-derived  │
│ ADC Resolution           │ 12       │ bits      │ Spec         │
│ ADC Sample Rate          │ 1000     │ SPS/ch    │ Spec         │
│ DSP Pipeline Depth       │ 5        │ stages    │ Architecture │
│ SRAM Size                │ 4        │ KB        │ Architecture │
│ Register File Size       │ 256      │ ×32-bit   │ Architecture │
│ FIFO Depth               │ 16       │ entries   │ Architecture │
│ Watchdog Timeout         │ 500      │ ms        │ Spec (AAMI)  │
│ Pacing Rate Range        │ 30-180   │ ppm       │ Spec         │
│ Pulse Voltage Range      │ 0.5-7.5  │ V         │ Spec         │
│ Pulse Width Range        │ 0.05-1.5 │ ms        │ Spec         │
│ Telemetry Bit Rate       │ 1-2      │ kbps      │ ISO 14708    │
│ Encryption Key Size      │ 128      │ bits      │ AES-128      │
│ ECC Width                │ 7        │ bits      │ SECDED       │
│ CRC Polynomial           │ 0x8005   │ —         │ CRC-16       │
└──────────────────────────┴──────────┴───────────┴──────────────┘
```

## 11. Model Validation

```
Model Validation Methodology:

  1. Algorithm Validation (MATLAB)
     • Input: Synthetic ECG waveforms (MIT-BIH database)
     • Output: Sensing event timestamps
     • Criteria: <1% false positive, <0.1% false negative

  2. Architecture Validation (SystemC)
     • Input: Annotated RTL traffic
     • Output: Throughput, latency, power estimates
     • Criteria: All real-time constraints met

  3. Mixed-Signal Validation (Verilog-AMS)
     • Input: SPICE netlist of AFE
     • Output: Transfer function, noise spectrum
     • Criteria: Meet analog specs within 10%

  4. Safety Validation (SCADE / Model Check)
     • Property: "No single fault causes uncontrolled pacing"
     • Method: Model checking + fault injection
     • Criteria: 100% property coverage

  Cross-Model Consistency Check:
  ┌─────────────────────┬──────────┬──────────┬────────────┐
  │ Property            │ MATLAB   │ SystemC  │ RTL        │
  ├─────────────────────┼──────────┼──────────┼────────────┤
  │ Sensitivity (V)     │ 2.0 mV   │ 2.0 mV   │ 2.0 mV     │
  │ Pace Rate (bpm)     │ 72       │ 72       │ 72         │
  │ AV Delay (ms)       │ 150      │ 150      │ 150        │
  │ Power (µA avg)      │ 8.5      │ 9.2      │ TBD        │
  │ Response Latency    │ <10ms   │ <10ms    │ TBD        │
  └─────────────────────┴──────────┴──────────┴────────────┘
```

## 12. Summary

System-level modeling for iPACE-CHIP provides:

1. **Executable specifications** that replace ambiguous natural language requirements
2. **Architecture exploration** before committing to RTL implementation
3. **Mixed-signal validation** bridging analog and digital domains
4. **Safety verification** through formal models and fault injection
5. **Reference models** for RTL and gate-level verification
6. **Power-state validation** ensuring compliance with battery lifetime targets

The multi-language approach (MATLAB for algorithms, SystemC for architecture, Verilog-AMS
for mixed-signal) provides the right abstraction level at each stage of the design flow,
while the unified verification strategy ensures consistency across all models.

---

*Previous: [Requirements Capture](../01-Requirements-Capture/requirements-capture.md) | Next: [Architecture Tradeoffs](../03-Architecture-Tradeoffs/architecture-tradeoffs.md)*
