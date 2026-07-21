# Loops and Iteration in Verilog

## 5.3.3 — Overview

Verilog provides several loop constructs for behavioral modeling. While loops
are primarily used in **testbenches** and `generate` blocks, certain loop
patterns synthesize to hardware. Understanding which loops synthesize and which
are simulation-only is critical for iPACE-CHIP RTL design.

---

## 5.3.4 — Loop Types Summary

| Loop | Synthesizable | Typical Use |
|------|---------------|-------------|
| `for` | Yes (generate) | Array iteration, module generation |
| `while` | No | Testbench stimulus |
| `repeat` | No (unless bounded) | Testbench delays |
| `forever` | No | Testbench clock generation |
| `do-while` | No | Testbench (SystemVerilog) |

---

## 5.3.5 — For Loop

### Testbench For Loop

```verilog
// NOT synthesizable — simulation only
integer i;
reg [7:0] test_data [0:255];

initial begin
    // Initialize memory
    for (i = 0; i < 256; i = i + 1) begin
        test_data[i] = i[7:0];
    end

    // Apply test vectors
    for (i = 0; i < 256; i = i + 1) begin
        @(posedge clk);
        data_in = test_data[i];
        @(posedge clk);
        if (data_out !== expected[i])
            $error("Mismatch at i=%0d", i);
    end
end
```

### Generate For Loop (Synthesizable)

```verilog
// Array of D flip-flops — synthesizes to 8 FFs
module register_8bit (
    input  wire       clk,
    input  wire       rst_n,
    input  wire [7:0] d,
    output wire [7:0] q
);
    genvar i;
    generate
        for (i = 0; i < 8; i = i + 1) begin : gen_ff
            dff_rst u_ff (
                .clk   (clk),
                .rst_n (rst_n),
                .d     (d[i]),
                .q     (q[i])
            );
        end
    endgenerate
endmodule
```

---

## 5.3.6 — While Loop (Testbench Only)

```verilog
// Testbench: wait for condition
integer timeout;
initial begin
    timeout = 0;
    while (!interrupt && timeout < 10000) begin
        @(posedge clk);
        timeout = timeout + 1;
    end

    if (timeout >= 10000)
        $error("Timeout waiting for interrupt");
    else
        $display("Interrupt received at time %0t", $time);
end
```

### Pacemaker Testbench: Wait for Sensing Event

```verilog
task wait_for_sense;
    input integer max_cycles;
    output integer actual_cycles;
    output reg     timed_out;
    integer count;
begin
    count = 0;
    timed_out = 0;
    while (!sense_event && count < max_cycles) begin
        @(posedge clk);
        count = count + 1;
    end
    actual_cycles = count;
    timed_out = (count >= max_cycles);
end
endtask
```

---

## 5.3.7 — Repeat Loop

```verilog
// Repeat: fixed number of iterations
// Not synthesizable (simulation only)

// Generate 16 clock cycles
repeat (16) begin
    @(posedge clk);
    spi_sclk = ~spi_sclk;
end

// SPI byte transfer
task spi_transfer;
    input [7:0] data;
    output [7:0] received;
    integer i;
begin
    received = 8'h00;
    cs_n = 1'b0;
    repeat (8) begin
        @(posedge clk);
        spi_mosi = data[7-i];
        spi_sclk = 1'b1;
        @(posedge clk);
        spi_sclk = 1'b0;
        received = {received[6:0], spi_miso};
    end
    cs_n = 1'b1;
end
endtask
```

---

## 5.3.8 — Forever Loop

```verilog
// Clock generation — simulation only
initial begin
    clk = 0;
    forever #500 clk = ~clk;  // 1 kHz clock
end

// Timeout watchdog
initial begin
    #10000000;  // 10 ms timeout
    $error("Simulation timeout!");
    $finish;
end
```

---

## 5.3.9 — Synthesizable Loop Patterns

### Generate-for: Memory Initialization

```verilog
// Synthesizable ROM with for-loop initialization
module config_rom (
    input  wire [3:0] addr,
    output wire [7:0] data
);
    reg [7:0] rom [0:15];
    integer i;

    always_comb begin
        // Initialize on first access
        rom[0]  = 8'hA0;  // pacing mode
        rom[1]  = 8'h3C;  // sensitivity
        rom[2]  = 8'h0F;  // pulse width
        rom[3]  = 8'h80;  // amplitude
        rom[4]  = 8'h64;  // refractory
        rom[5]  = 8'h00;  // reserved
        rom[6]  = 8'hFF;  // max rate
        rom[7]  = 8'h10;  // min rate
        // Remaining entries
        for (i = 8; i < 16; i = i + 1)
            rom[i] = 8'h00;
    end

    assign data = rom[addr];
endmodule
```

### Generate-for: Barrel Shifter

```verilog
module barrel_shifter #(
    parameter WIDTH = 16
)(
    input  wire [WIDTH-1:0]      data_in,
    input  wire [$clog2(WIDTH)-1:0] shift_amt,
    output wire [WIDTH-1:0]      data_out
);
    wire [WIDTH-1:0] stage [0:$clog2(WIDTH)];

    assign stage[0] = data_in;

    genvar i;
    generate
        for (i = 0; i < $clog2(WIDTH); i = i + 1) begin : gen_stage
            assign stage[i+1] = shift_amt[i] ?
                {stage[i][WIDTH-1-(2**i):0], {2**i{1'b0}}} :
                stage[i];
        end
    endgenerate

    assign data_out = stage[$clog2(WIDTH)];

endmodule
```

### Generate-for: Parallel Comparator Array

```verilog
module threshold_array #(
    parameter NUM_CHANNELS = 8,
    parameter DATA_WIDTH   = 12
)(
    input  wire [NUM_CHANNELS-1:0][DATA_WIDTH-1:0] adc_data,
    input  wire [NUM_CHANNELS-1:0][DATA_WIDTH-1:0] thresholds,
    output wire [NUM_CHANNELS-1:0]                  exceeded
);
    genvar ch;
    generate
        for (ch = 0; ch < NUM_CHANNELS; ch = ch + 1) begin : gen_cmp
            assign exceeded[ch] = (adc_data[ch] > thresholds[ch]);
        end
    endgenerate
endmodule
```

---

## 5.3.10 — Pacemaker: Multi-Channel Averaging with Generate

```verilog
module channel_averager #(
    parameter NUM_CHANNELS = 4,
    parameter SAMPLE_BITS  = 12,
    parameter AVG_BITS     = 4    // average 2^AVG_BITS samples
)(
    input  wire                                    clk,
    input  wire                                    rst_n,
    input  wire                                    sample_valid,
    input  wire [NUM_CHANNELS-1:0][SAMPLE_BITS-1:0] adc_data,
    output wire [NUM_CHANNELS-1:0][SAMPLE_BITS+AVG_BITS-1:0] average,
    output wire [NUM_CHANNELS-1:0] avg_valid
);

    reg [$clog2(2**AVG_BITS)-1:0] sample_count;
    reg [SAMPLE_BITS+AVG_BITS-1:0] accumulator [0:NUM_CHANNELS-1];
    reg [NUM_CHANNELS-1:0] valid_pipe;

    // Sample counter
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            sample_count <= '0;
        else if (sample_valid) begin
            if (sample_count == (2**AVG_BITS - 1))
                sample_count <= '0;
            else
                sample_count <= sample_count + 1'b1;
        end
    end

    // Per-channel accumulation using generate
    genvar ch;
    generate
        for (ch = 0; ch < NUM_CHANNELS; ch = ch + 1) begin : gen_avg
            always @(posedge clk or negedge rst_n) begin
                if (!rst_n) begin
                    accumulator[ch] <= '0;
                    valid_pipe[ch]  <= 1'b0;
                end else if (sample_valid) begin
                    if (sample_count == 0)
                        accumulator[ch] <= {{AVG_BITS{1'b0}}, adc_data[ch]};
                    else
                        accumulator[ch] <= accumulator[ch] + {{AVG_BITS{1'b0}}, adc_data[ch]};

                    valid_pipe[ch] <= (sample_count == (2**AVG_BITS - 1));
                end
            end
            assign average[ch] = accumulator[ch];
        end
    endgenerate

    assign avg_valid = valid_pipe;

endmodule
```

---

## 5.3.11 — Loop Synthesis Rules

### What Synthesizes

```verilog
// GENERATE FOR — creates multiple instances
genvar i;
generate
    for (i = 0; i < N; i = i + 1) begin : gen_inst
        module_name u_inst (...);
    end
endgenerate

// BEHAVIORAL FOR — unrolled by synthesis tool
reg [7:0] result;
integer i;
always_comb begin
    result = 8'h00;
    for (i = 0; i < 8; i = i + 1) begin
        if (data[i])
            result = result + 1'b1;
    end
end
// Synthesizes to: 8-bit popcount
```

### What Does NOT Synthesize

```verilog
// These are simulation-only:
while (condition) begin ... end  // unbounded
forever begin ... end            // infinite
repeat(N) begin ... end          // fixed delay (testbench)
#delay                          // time delay
@(event)                       // wait for event
$display, $monitor, $finish    // system tasks
```

---

## 5.3.12 — Best Practices

1. **Use `generate for`** for creating arrays of instances
2. **Use behavioral `for`** for combinational logic patterns (popcount, mux trees)
3. **Avoid `while`/`forever`** in synthesizable code — testbench only
4. **Bound all loops** — synthesis tools need static bounds
5. **Use `$clog2()`** for automatic width calculation
6. **Use `genvar`** for generate loop variables — scoped correctly
7. **Name generate blocks** — `gen_xxx` for better error messages
8. **Test loop-based logic** with assertions — ensure correct unrolling

---

## 5.3.13 — References

- IEEE Std 1364-2005, Section 4.5 — Looping Statements
- IEEE Std 1800-2017, Section 12.7 — Looping Statements
- iPACE-CHIP RTL Coding Guidelines, Section 3.6
