# Enums and Structs in SystemVerilog

## 5.4.3 — Overview

SystemVerilog introduces `enum` and `struct` types for **richer data modeling**
in RTL and verification. Enums replace magic numbers with named states;
structs group related signals into coherent data types. For iPACE-CHIP, these
types improve FSM readability, configuration register modeling, and telemetry
packet construction.

---

## 5.4.4 — Enumeration Types

### Basic Enum Declaration

```systemverilog
// FSM states
typedef enum logic [2:0] {
    S_IDLE   = 3'b000,
    S_PACE   = 3'b001,
    S_SENSE  = 3'b010,
    S_REFRACT= 3'b011,
    S_TELEM  = 3'b100,
    S_SLEEP  = 3'b101,
    S_FAULT  = 3'b111
} state_t;

state_t state, next_state;
```

### Auto-Incrementing Values

```systemverilog
typedef enum logic [1:0] {
    MODE_OFF,       // 2'b00
    MODE_VVI,       // 2'b01
    MODE_AAI,       // 2'b10
    MODE_DDD        // 2'b11
} pacing_mode_t;
```

### Named Constants with Explicit Values

```systemverilog
typedef enum logic [3:0] {
    ALARM_NONE          = 4'h0,
    ALARM_BATT_LOW      = 4'h1,
    ALARM_LEAD_FAULT    = 4'h2,
    ALARM_SENSING       = 4'h3,
    ALARM_OVERTEMP      = 4'h4,
    ALARM_CRITICAL      = 4'hF
} alarm_code_t;
```

---

## 5.4.5 — Enum Methods

### Name and Value Queries

```systemverilog
state_t current_state = S_PACE;

// Get name as string
string name = current_state.name();  // "S_PACE"

// Get value
logic [2:0] val = current_state;  // 3'b001
```

### Enum Iteration

```systemverilog
// Iterate over all enum values (testbench)
for (state_t s = state_t.first(); s != state_t.last(); s = s.next()) begin
    $display("State: %s = %0d", s.name(), s);
end
```

---

## 5.4.6 — FSM with Enums

```systemverilog
module pacemaker_fsm (
    input  logic          clk,
    input  logic          rst_n,
    input  logic          timer_expired,
    input  logic          atrial_sense,
    input  logic          vent_sense,
    input  pacing_mode_t  mode,
    output logic          pace_out,
    output logic          timer_start,
    output logic          refractory_en
);

    // State type
    typedef enum logic [2:0] {
        IDLE       = 3'd0,
        PACE_A     = 3'd1,
        WAIT_V     = 3'd2,
        PACE_V     = 3'd3,
        REFRACT    = 3'd4,
        TELEM      = 3'd5,
        FAULT      = 3'd7
    } state_t;

    state_t state, next_state;

    // State register
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            state <= IDLE;
        else
            state <= next_state;
    end

    // Next state logic
    always_comb begin
        next_state = state;  // default: hold
        case (state)
            IDLE: begin
                if (mode == MODE_OFF)
                    next_state = IDLE;
                else if (timer_expired)
                    next_state = PACE_A;
                else if (atrial_sense)
                    next_state = WAIT_V;
            end

            PACE_A: begin
                next_state = REFRACT;
            end

            WAIT_V: begin
                if (vent_sense || timer_expired)
                    next_state = (vent_sense) ? REFRACT : PACE_V;
            end

            PACE_V: begin
                next_state = REFRACT;
            end

            REFRACT: begin
                if (timer_expired)
                    next_state = TELEM;
            end

            TELEM: begin
                next_state = IDLE;
            end

            FAULT: begin
                // Stay in fault until reset
                next_state = FAULT;
            end

            default: next_state = IDLE;
        endcase
    end

    // Output logic
    always_comb begin
        pace_out     = 1'b0;
        timer_start  = 1'b0;
        refractory_en = 1'b0;

        case (state)
            IDLE:    timer_start = 1'b1;
            PACE_A:  pace_out = 1'b1;
            PACE_V:  pace_out = 1'b1;
            REFRACT: refractory_en = 1'b1;
            TELEM:   timer_start = 1'b1;
        endcase
    end

endmodule
```

---

## 5.4.7 — Struct Types

### Packed Struct

```systemverilog
typedef struct packed {
    logic [7:0]  header;
    logic [7:0]  device_id;
    logic [15:0] payload;
    logic [7:0]  crc;
} telemetry_packet_t;

telemetry_packet_t packet;

// Access fields
packet.header   = 8'hA5;
packet.device_id = device_addr;
packet.payload  = {status_byte, alarm_code};
packet.crc      = calculated_crc;

// Concatenate as bit vector (packed)
logic [31:0] raw_packet;
assign raw_packet = packet;  // automatic pack
```

### Unpacked Struct

```systemverilog
typedef struct {
    logic [11:0] adc_atrial;
    logic [11:0] adc_ventricular;
    logic        valid;
    logic [1:0]  channel;
} adc_sample_t;

adc_sample_t current_sample;

// Access fields
current_sample.adc_atrial = 12'h800;
current_sample.valid      = 1'b1;
```

### Struct with Enum

```systemverilog
typedef struct packed {
    pacing_mode_t mode;
    logic [3:0]   sensitivity;
    logic [7:0]   pulse_width;
    logic [7:0]   pulse_amplitude;
    logic [7:0]   refractory_period;
} pacing_config_t;

pacing_config_t config_reg;

// Write all fields at once
config_reg = '{
    mode: MODE_VVI,
    sensitivity: 4'd8,
    pulse_width: 8'd20,
    pulse_amplitude: 8'h40,
    refractory_period: 8'd30
};
```

---

## 5.4.8 — Struct for Register Maps

```systemverilog
// Register file using struct
typedef struct packed {
    logic [7:0]  ctrl;          // 0x00
    logic [7:0]  status;        // 0x01
    logic [15:0] timer_count;   // 0x02-0x03
    logic [11:0] adc_atrial;    // 0x04-0x05
    logic [11:0] adc_ventricular; // 0x06-0x07
    logic [7:0]  pulse_width;   // 0x08
    logic [7:0]  pulse_amplitude; // 0x09
    logic [7:0]  sensitivity;   // 0x0A
    logic [7:0]  refractory;    // 0x0B
    logic [31:0] reserved;      // 0x0C-0x0F
} ipace_reg_map_t;

// Register write
ipace_reg_map_t regs;

always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        regs <= '0;
    end else if (write_en) begin
        case (addr)
            8'h00: regs.ctrl <= write_data;
            8'h02: regs.timer_count[15:0] <= write_data;
            8'h08: regs.pulse_width <= write_data;
            8'h09: regs.pulse_amplitude <= write_data;
        endcase
    end
end

// Register read
always_comb begin
    read_data = '0;
    case (addr)
        8'h00: read_data = regs.ctrl;
        8'h01: read_data = regs.status;
        8'h02: read_data = regs.timer_count[15:0];
        8'h04: read_data = regs.adc_atrial;
        8'h08: read_data = regs.pulse_width;
    endcase
end
```

---

## 5.4.9 — Union Types

```systemverilog
// Packed union — same memory, different interpretation
typedef union packed {
    logic [31:0]           raw;
    struct packed {
        logic [7:0]  byte0;
        logic [7:0]  byte1;
        logic [7:0]  byte2;
        logic [7:0]  byte3;
    } as_bytes;
    struct packed {
        logic [15:0] low_word;
        logic [15:0] high_word;
    } as_words;
} data_union_t;

data_union_t data;
data.raw = 32'hDEADBEEF;
// data.as_bytes.byte0 = 8'hEF
// data.as_words.low_word = 16'hBEEF
```

---

## 5.4.10 — Pacemaker Telemetry with Structs

```systemverilog
// Telemetry packet definition
typedef struct packed {
    logic [3:0]  sync;          // 4'hA
    logic [3:0]  packet_type;   // 0=status, 1=telemetry, 2=config
    logic [7:0]  device_id;
    logic [7:0]  status;
    logic [11:0] battery_mv;
    logic [11:0] lead_impedance;
    logic [11:0] atrial_adc;
    logic [11:0] vent_adc;
    logic [7:0]  crc8;
} ipace_telem_packet_t;

// CRC calculation function
function automatic logic [7:0] calc_crc8(
    input logic [7:0] data,
    input logic [7:0] crc_in
);
    logic [7:0] crc;
    int i;
    begin
        crc = crc_in ^ data;
        for (i = 0; i < 8; i++)
            crc = crc[7] ? ((crc << 1) ^ 8'h07) : (crc << 1);
        return crc;
    end
endfunction

// Packet builder
module telemetry_packetizer (
    input  logic                  clk,
    input  logic                  rst_n,
    input  logic [7:0]            device_id,
    input  logic [7:0]            status,
    input  logic [11:0]           battery_mv,
    input  logic [11:0]           lead_impedance,
    input  logic [11:0]           atrial_adc,
    input  logic [11:0]           vent_adc,
    input  logic                  send,
    output ipace_telem_packet_t   packet,
    output logic                  packet_valid
);
    logic [7:0] crc_acc;

    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            packet        <= '0;
            packet_valid  <= 1'b0;
        end else if (send) begin
            packet <= '{
                sync:           4'hA,
                packet_type:    4'd1,
                device_id:      device_id,
                status:         status,
                battery_mv:     battery_mv,
                lead_impedance: lead_impedance,
                atrial_adc:     atrial_adc,
                vent_adc:       vent_adc,
                crc8:           8'h00  // calculated below
            };

            // CRC over all fields except crc8
            crc_acc = 8'hFF;
            crc_acc = calc_crc8(packet[71:64], crc_acc);
            crc_acc = calc_crc8(packet[63:56], crc_acc);
            crc_acc = calc_crc8(packet[55:48], crc_acc);
            crc_acc = calc_crc8(packet[47:40], crc_acc);
            crc_acc = calc_crc8(packet[39:32], crc_acc);
            crc_acc = calc_crc8(packet[31:24], crc_acc);
            crc_acc = calc_crc8(packet[23:16], crc_acc);
            crc_acc = calc_crc8(packet[15:8],  crc_acc);

            packet.crc8 <= crc_acc;
            packet_valid <= 1'b1;
        end else begin
            packet_valid <= 1'b0;
        end
    end
endmodule
```

---

## 5.4.11 — Best Practices

1. **Use `typedef`** for all enums and structs — reusable across modules
2. **Pack structs** when bit-level access is needed — `packed`
3. **Use enums for FSMs** — self-documenting, tool-friendly
4. **Never use `casex`** with enums — use `case` or `unique case`
5. **Default enum values** — handle all cases in FSM
6. **Use struct for register maps** — maintain alignment and access
7. **Document struct layout** — comment bit fields
8. **Use `'{}` for struct literals** — explicit field assignment
9. **Check struct packing** — ensure no padding gaps
10. **Enumerate all enum values** — catch incomplete case statements

---

## 5.4.12 — References

- IEEE Std 1800-2017, Section 6.19 — Enumerations
- IEEE Std 1800-2017, Section 7.2 — Structures
- SystemVerilog for Verification, Chris Spear, Chapter 3
- iPACE-CHIP Data Types Package Specification
