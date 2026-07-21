# Tasks and Functions in Verilog

## 5.1.4 — Overview

Tasks and functions provide **procedural abstraction** within Verilog modules.
They encapsulate repeated logic, improving readability and reducing errors.
For iPACE-CHIP, tasks and functions are used in testbenches extensively and
can also model reusable combinational blocks in synthesizable RTL.

---

## 5.4.1 — Functions

### Declaration Syntax

```verilog
function [RETURN_WIDTH-1:0] function_name;
    input [WIDTH-1:0] arg1;
    input [WIDTH-1:0] arg2;
    // local variables
    begin
        function_name = expression;
    end
endfunction
```

### SystemVerilog Style

```verilog
function automatic logic [7:0] function_name(
    input logic [7:0] arg1,
    input logic [7:0] arg2
);
    logic [7:0] result;
    result = arg1 + arg2;
    return result;
endfunction
```

### Key Properties

| Property | Constraint |
|----------|-----------|
| Return value | Must assign to function name or use `return` |
| Time control | **No** `#`, `@`, or `wait` allowed |
| Calls | **Cannot** call tasks; can call other functions |
| Scope | Has own local variables |
| Recursion | Not supported (unless `automatic`) |
| Synthesis | Fully synthesizable for combinational logic |

### Basic Function Example

```verilog
// Absolute value function
function signed [7:0] abs_val;
    input signed [7:0] x;
    begin
        if (x < 0)
            abs_val = -x;
        else
            abs_val = x;
    end
endfunction

// Usage
wire signed [7:0] error_signal;
wire [7:0] magnitude = abs_val(error_signal);
```

### Pacemaker: ADC Value Clamping Function

```verilog
// Clamp ADC value to safe range [MIN, MAX]
function [11:0] clamp_adc;
    input [11:0] value;
    input [11:0] min_val;
    input [11:0] max_val;
    begin
        if (value < min_val)
            clamp_adc = min_val;
        else if (value > max_val)
            clamp_adc = max_val;
        else
            clamp_adc = value;
    end
endfunction

// Usage in module
wire [11:0] safe_adc = clamp_adc(adc_raw, 12'd100, 12'd3000);
```

### Pacemaker: CRC-8 Calculation Function

```verilog
function [7:0] crc8_calc;
    input [7:0]  data;
    input [7:0]  crc_in;
    reg   [7:0]  crc;
    integer      i;
    begin
        crc = crc_in ^ data;
        for (i = 0; i < 8; i = i + 1) begin
            if (crc[7])
                crc = (crc << 1) ^ 8'h07;  // polynomial x^8+x^2+x+1
            else
                crc = crc << 1;
        end
        crc8_calc = crc;
    end
endfunction

// Pipeline CRC over multiple bytes
function [7:0] crc8_block;
    input [63:0] block_data;  // 8 bytes
    reg   [7:0]  crc;
    integer      i;
    begin
        crc = 8'hFF;  // initial value
        for (i = 0; i < 8; i = i + 1)
            crc = crc8_calc(block_data[i*8 +: 8], crc);
        crc8_block = crc;
    end
endfunction
```

### Pacemaker: Priority Encoder Function

```verilog
function [2:0] priority_encode_8to3;
    input [7:0] requests;
    begin
        casez (requests)
            8'b1???????: priority_encode_8to3 = 3'd7;
            8'b01??????: priority_encode_8to3 = 3'd6;
            8'b001?????: priority_encode_8to3 = 3'd5;
            8'b0001????: priority_encode_8to3 = 3'd4;
            8'b00001???: priority_encode_8to3 = 3'd3;
            8'b000001??: priority_encode_8to3 = 3'd2;
            8'b0000001?: priority_encode_8to3 = 3'd1;
            8'b00000001: priority_encode_8to3 = 3'd0;
            default:     priority_encode_8to3 = 3'd0;
        endcase
    end
endfunction
```

### Automatic Functions (SystemVerilog)

```verilog
// Recursive function (requires `automatic`)
function automatic int factorial(input int n);
    if (n <= 1)
        return 1;
    else
        return n * factorial(n - 1);
endfunction
```

---

## 5.4.2 — Tasks

### Declaration Syntax

```verilog
task task_name;
    input  [WIDTH-1:0] arg1;
    output [WIDTH-1:0] arg2;
    inout  [WIDTH-1:0] arg3;
    // local variables
    begin
        // task body
    end
endtask
```

### SystemVerilog Style

```verilog
task automatic send_spi_byte(
    input  logic [7:0]  data,
    output logic        ack
);
    logic [7:0] shift_reg;
    int i;
    begin
        shift_reg = data;
        for (i = 0; i < 8; i = i + 1) begin
            @(posedge clk);
            spi_clk = shift_reg[7];
            spi_mosi = shift_reg[7];
            shift_reg = shift_reg << 1;
        end
        @(posedge clk);
        ack = 1'b1;
    end
endtask
```

### Key Properties

| Property | Constraint |
|----------|-----------|
| Return value | No return value; use output arguments |
| Time control | **Can** use `#`, `@`, `wait` |
| Calls | Can call other tasks and functions |
| Execution | Sequential within task body |
| Blocking | Executes completely before returning |
| Synthesis | Only synthesizable if no time controls |

### Task with Inout Arguments

```verilog
task swap_bytes;
    inout  [7:0] byte_a;
    inout  [7:0] byte_b;
    reg [7:0] temp;
    begin
        temp   = byte_a;
        byte_a = byte_b;
        byte_b = temp;
    end
endtask

// Usage
reg [7:0] reg_high, reg_low;
swap_bytes(reg_high, reg_low);  // swap in-place
```

### Pacemaker: SPI Transaction Task

```verilog
task spi_write_reg(
    input  [7:0]  addr,
    input  [7:0]  data,
    output        error
);
    reg [7:0] shift_out;
    reg [7:0] rx_data;
    integer   bit_idx;
    begin
        error = 1'b0;

        // Assert chip select
        @(posedge clk);
        spi_cs_n = 1'b0;

        // Send address byte (MSB first)
        shift_out = addr;
        for (bit_idx = 7; bit_idx >= 0; bit_idx = bit_idx - 1) begin
            @(posedge clk);
            spi_mosi = shift_out[bit_idx];
            spi_sclk = 1'b1;
            @(posedge clk);
            spi_sclk = 1'b0;
        end

        // Send data byte
        shift_out = data;
        for (bit_idx = 7; bit_idx >= 0; bit_idx = bit_idx - 1) begin
            @(posedge clk);
            spi_mosi = shift_out[bit_idx];
            spi_sclk = 1'b1;
            @(posedge clk);
            spi_sclk = 1'b0;
        end

        // Deassert chip select
        @(posedge clk);
        spi_cs_n = 1'b1;
    end
endtask

task spi_read_reg(
    input  [7:0]  addr,
    output [7:0]  data,
    output        error
);
    reg [7:0] shift_out;
    reg [7:0] rx_byte;
    integer   bit_idx;
    begin
        error = 1'b0;

        @(posedge clk);
        spi_cs_n = 1'b0;

        // Send address with read bit
        shift_out = {1'b1, addr[6:0]};  // MSB=1 for read
        for (bit_idx = 7; bit_idx >= 0; bit_idx = bit_idx - 1) begin
            @(posedge clk);
            spi_mosi = shift_out[bit_idx];
            spi_sclk = 1'b1;
            @(posedge clk);
            spi_sclk = 1'b0;
        end

        // Receive data byte
        for (bit_idx = 7; bit_idx >= 0; bit_idx = bit_idx - 1) begin
            @(posedge clk);
            spi_sclk = 1'b1;
            rx_byte[bit_idx] = spi_miso;
            @(posedge clk);
            spi_sclk = 1'b0;
        end

        @(posedge clk);
        spi_cs_n = 1'b1;
        data = rx_byte;
    end
endtask
```

### Pacemaker: Testbench Stimulus Task

```verilog
task apply_pacing_pulse;
    input [15:0] duration_us;
    input [7:0]  amplitude;
    begin
        @(posedge clk);
        pace_out_enable = 1'b1;
        dac_amplitude   = amplitude;
        #(duration_us * 1000);  // convert to ns at 1MHz sim clock
        pace_out_enable = 1'b0;
        dac_amplitude   = 8'd0;
        $display("[T=%0t] Pacing pulse: %0d us, amp=%0d",
                 $time, duration_us, amplitude);
    end
endtask
```

---

## 5.4.3 — Task vs Function Comparison

| Feature | Task | Function |
|---------|------|----------|
| Return value | No (use outputs) | Yes (via name or `return`) |
| Time controls | Allowed (`#`, `@`) | **Not** allowed |
| Calls tasks | Yes | **No** |
| Calls functions | Yes | Yes (functions only) |
| Simulation | Yes | Yes |
| Synthesis | Only if no timing | Yes (combinational) |
| Typical use | Testbench, sequential ops | Combinational math, encoding |

---

## 5.4.4 — Automatic vs Static Tasks/Functions

### Static (Default in Verilog)

```verilog
// All local variables shared across concurrent calls
task static_task;
    reg [7:0] local_var;  // shared! Problem in concurrent calls
    begin
        local_var = local_var + 1;
    end
endtask
```

### Automatic (SystemVerilog)

```verilog
// Each call gets its own copy of local variables
task automatic auto_task;
    input int value;
    output int result;
    int local_copy;  // private to each call
    begin
        local_copy = value;
        result = local_copy * 2;
    end
endtask
```

### When to Use Automatic

```verilog
// REQUIRED for re-entrant testbench tasks
task automatic drive_signal(
    input logic [7:0] data,
    input int         delay_cycles
);
    begin
        @(posedge clk);
        sig = data;
        repeat(delay_cycles) @(posedge clk);
        sig = 8'h00;
    end
endtask

// Can run in parallel in testbench
initial begin
    fork
        drive_signal(8'hAA, 10);
        drive_signal(8'hBB, 20);
    join
end
```

---

## 5.4.5 — Function and Task Arrays

### Function Returning Array (SystemVerilog)

```verilog
function automatic logic [7:0] [7:0] reverse_bytes(
    input logic [7:0] [7:0] input_array
);
    logic [7:0] [7:0] result;
    int i;
    begin
        for (i = 0; i < 8; i++)
            result[i] = input_array[7-i];
        return result;
    end
endfunction
```

### Task with Array Arguments

```verilog
task automatic compute_average(
    input  logic [11:0] samples [0:63],
    input  int          num_samples,
    output logic [11:0] average,
    output logic [15:0] sum
);
    int i;
    logic [15:0] accumulator;
    begin
        accumulator = 16'd0;
        for (i = 0; i < num_samples; i++)
            accumulator = accumulator + {4'b0, samples[i]};
        sum     = accumulator;
        average = accumulator[15:4];  // divide by 16 (use >> for power-of-2)
    end
endtask
```

---

## 5.4.6 — Pacemaker Module Using Tasks and Functions

```verilog
module telemetry_packet_builder (
    input  wire        clk,
    input  wire        rst_n,
    input  wire [7:0]  device_id,
    input  wire [7:0]  status_byte,
    input  wire [11:0] battery_voltage,
    input  wire [11:0] lead_impedance,
    input  wire [11:0] sensing_data,
    input  wire        send_trigger,
    output reg  [63:0] packet_out,
    output reg         packet_valid,
    output reg  [7:0]  packet_crc
);

    // CRC-8 function
    function [7:0] crc8;
        input [7:0] data_in;
        input [7:0] crc_in;
        reg [7:0] crc;
        integer i;
        begin
            crc = crc_in ^ data_in;
            for (i = 0; i < 8; i = i + 1)
                crc = crc[7] ? ((crc << 1) ^ 8'h07) : (crc << 1);
            crc8 = crc;
        end
    endfunction

    // Packet assembly task
    task assemble_packet;
        input [7:0]  dev_id;
        input [7:0]  status;
        input [11:0] battery;
        input [11:0] impedance;
        input [11:0] sensing;
        output [63:0] pkt;
        output [7:0]  crc_val;
        reg [7:0] crc_acc;
        begin
            // Header
            pkt[63:56] = 8'hA5;           // sync byte
            pkt[55:48] = dev_id;
            pkt[47:40] = status;

            // Battery (12 bits packed into 16 bits)
            pkt[39:24] = {4'b0, battery};

            // Lead impedance
            pkt[23:12] = impedance;

            // Sensing data
            pkt[11:0]  = sensing;

            // Calculate CRC
            crc_acc = 8'hFF;
            crc_acc = crc8(pkt[63:56], crc_acc);
            crc_acc = crc8(pkt[55:48], crc_acc);
            crc_acc = crc8(pkt[47:40], crc_acc);
            crc_acc = crc8(pkt[39:32], crc_acc);
            crc_acc = crc8(pkt[31:24], crc_acc);
            crc_acc = crc8(pkt[23:16], crc_acc);
            crc_acc = crc8(pkt[15:8],  crc_acc);
            crc_acc = crc8(pkt[7:0],   crc_acc);
            crc_val = crc_acc;
        end
    endtask

    // Main sequential logic
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            packet_out   <= 64'd0;
            packet_valid <= 1'b0;
            packet_crc   <= 8'd0;
        end else if (send_trigger) begin
            assemble_packet(
                device_id, status_byte, battery_voltage,
                lead_impedance, sensing_data,
                packet_out, packet_crc
            );
            packet_valid <= 1'b1;
        end else begin
            packet_valid <= 1'b0;
        end
    end

endmodule
```

---

## 5.4.7 — Synthesis Implications

### Synthesizable Function Patterns

```verilog
// Combinational logic — always synthesizable
function [15:0] multiply_16x16;
    input [15:0] a, b;
    begin
        multiply_16x16 = a * b;
    end
endfunction

// LUT-based mapping
function [3:0] one_hot_encode;
    input [2:0] binary;
    begin
        case (binary)
            3'd0: one_hot_encode = 4'b0001;
            3'd1: one_hot_encode = 4'b0010;
            3'd2: one_hot_encode = 4'b0100;
            3'd3: one_hot_encode = 4'b1000;
            default: one_hot_encode = 4'b0000;
        endcase
    end
endfunction
```

### Non-Synthesizable Patterns (Testbench Only)

```verilog
// These will NOT synthesize:
function void display_message;  // void return — simulation only
    input string msg;
    begin
        $display("[TB] %s", msg);
    end
endfunction

function real voltage_to_real;  // real type — simulation only
    input [15:0] raw;
    begin
        voltage_to_real = raw * 1.2 / 4096.0;
    end
endfunction
```

---

## 5.4.8 — Best Practices

1. **Use functions** for combinational math and encoding logic
2. **Use tasks** for sequential testbench operations with timing
3. **Always use `automatic`** in SystemVerilog for reentrant tasks/functions
4. **Avoid large functions** — synthesis tools may not optimize well beyond a
   certain complexity
5. **Keep functions pure** — no side effects, no global state
6. **Use tasks** when multiple output arguments are needed
7. **Document function latency** — critical for pipeline design
8. **Test tasks and functions independently** before integration

---

## 5.4.9 — References

- IEEE Std 1364-2005, Section 10.2 — Tasks and Functions
- IEEE Std 1800-2017, Section 13 — Procedural Programming
- iPACE-CHIP RTL Coding Guidelines, Section 3.5 — Procedural Abstraction
