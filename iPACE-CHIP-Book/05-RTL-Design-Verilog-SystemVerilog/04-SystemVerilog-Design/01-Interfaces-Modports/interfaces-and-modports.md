# Interfaces and Modports in SystemVerilog

## 5.4.1 — Overview

SystemVerilog **interfaces** encapsulate communication channels between modules,
replacing verbose port lists with a single connection point. **Modports**
(modular ports) define directional views of an interface, enforcing correct
signal directions at compile time. For iPACE-CHIP, interfaces dramatically
simplify SPI, ADC, and telemetry bus connections.

---

## 5.4.2 — Interface Declaration

### Basic Interface

```systemverilog
interface spi_bus;
    logic       clk;
    logic       mosi;
    logic       miso;
    logic       cs_n;
endinterface
```

### Interface with Functions/Tasks

```systemverilog
interface spi_bus_if;
    logic        clk;
    logic        mosi;
    logic        miso;
    logic        cs_n;
    logic [7:0]  tx_data;
    logic [7:0]  rx_data;
    logic        tx_valid;
    logic        tx_ready;

    // Monitor task — checks protocol
    task check_idle;
        if (!cs_n)
            $error("CS assertion while idle");
    endtask

    // Clock generation (testbench only)
    task start_clock;
        fork
            forever begin
                clk = 0; #5;
                clk = 1; #5;
            end
        join_none
    endtask
endinterface
```

---

## 5.4.3 — Modport Declarations

Modports define **directional views** of an interface:

```systemverilog
interface apb_bus;
    logic        pclk;
    logic        presetn;
    logic [31:0] paddr;
    logic        psel;
    logic        penable;
    logic        pwrite;
    logic [31:0] pwdata;
    logic [31:0] prdata;
    logic        pready;

    // Master view
    modport master (
        output pclk,
        output presetn,
        output paddr,
        output psel,
        output penable,
        output pwrite,
        output pwdata,
        input  prdata,
        input  pready
    );

    // Slave view
    modport slave (
        input  pclk,
        input  presetn,
        input  paddr,
        input  psel,
        input  penable,
        input  pwrite,
        input  pwdata,
        output prdata,
        output pready
    );

    // Monitor view (all inputs)
    modport monitor (
        input pclk, presetn, paddr, psel, penable,
        input pwrite, pwdata, prdata, pready
    );
endinterface
```

---

## 5.4.4 — Interface Instantiation

### Module with Interface Port

```systemverilog
module spi_master (
    input  logic       clk,
    input  logic       rst_n,
    spi_bus.master     spi     // interface port
);
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            spi.mosi   <= 1'b0;
            spi.cs_n   <= 1'b1;
        end else begin
            // Access signals through interface
            spi.mosi   <= shift_reg[7];
            spi.cs_n   <= ~active;
        end
    end
endmodule

module spi_slave (
    input  logic       clk,
    input  logic       rst_n,
    spi_bus.slave      spi     // interface port
);
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            spi.miso <= 1'b0;
        end else begin
            spi.miso <= shift_reg[7];
        end
    end
endmodule
```

### Connecting Instances

```systemverilog
module top;
    logic clk, rst_n;

    // Instantiate interface
    spi_bus u_spi_bus ();

    // Instantiate modules with interface
    spi_master u_master (
        .clk   (clk),
        .rst_n (rst_n),
        .spi   (u_spi_bus.master)  // modport connection
    );

    spi_slave u_slave (
        .clk   (clk),
        .rst_n (rst_n),
        .spi   (u_spi_bus.slave)
    );
endmodule
```

---

## 5.4.5 — Pacemaker SPI Interface

```systemverilog
interface ipace_spi_if;
    logic        sclk;
    logic        mosi;
    logic        miso;
    logic        cs_n;
    logic [7:0]  tx_byte;
    logic [7:0]  rx_byte;
    logic        tx_valid;
    logic        tx_ready;
    logic        rx_valid;

    // SPI Mode 0,0 configuration
    parameter CPOL = 0;
    parameter CPHA = 0;

    modport master_mp (
        output sclk,
        output mosi,
        input  miso,
        output cs_n,
        output tx_byte,
        output tx_valid,
        input  tx_ready,
        input  rx_byte,
        input  rx_valid
    );

    modport slave_mp (
        input  sclk,
        input  mosi,
        output miso,
        input  cs_n,
        input  tx_byte,
        input  tx_valid,
        output tx_ready,
        output rx_byte,
        output rx_valid
    );

    modport monitor_mp (
        input sclk, mosi, miso, cs_n,
        input tx_byte, tx_valid, tx_ready,
        input rx_byte, rx_valid
    );
endinterface
```

---

## 5.4.6 — Pacemaker ADC Interface

```systemverilog
interface ipace_adc_if #(
    parameter WIDTH = 12
)(
    input logic clk
);
    logic [WIDTH-1:0] data;
    logic             valid;
    logic             ready;
    logic [1:0]       channel;  // 0=atrial, 1=ventricular
    logic             start_conv;

    modport adc_master (
        output start_conv,
        output channel,
        input  data,
        input  valid,
        output ready
    );

    modport adc_slave (
        input  start_conv,
        input  channel,
        output data,
        output valid,
        input  ready
    );

    modport adc_monitor (
        input start_conv, channel, data, valid, ready
    );

    // Coverage group
    covergroup adc_cov @(posedge clk);
        channel_cp: coverpoint channel;
        valid_cp:   coverpoint valid;
        cross channel_cp, valid_cp;
    endgroup

    adc_cov cov_inst = new();
endinterface
```

---

## 5.4.7 — Interface with Clocking Blocks

```systemverilog
interface timing_if (input logic clk);
    logic [15:0] timer_count;
    logic        timer_done;
    logic        timer_enable;

    // Synchronous clocking block
    clocking driver_cb @(posedge clk);
        default input #1step output #1;
        output timer_enable;
        input  timer_count;
        input  timer_done;
    endclocking

    // Synchronous clocking block for monitor
    clocking monitor_cb @(posedge clk);
        default input #1step;
        input timer_count;
        input timer_done;
        input timer_enable;
    endclocking

    modport driver_mp (clocking driver_cb);
    modport monitor_mp (clocking monitor_cb);
endinterface
```

---

## 5.4.8 — Interface Arrays

```systemverilog
// Multiple ADC channels via interface array
module multi_channel_adc (
    input logic                  clk,
    input logic                  rst_n,
    ipace_adc_if adc_ch [4]     // array of 4 ADC interfaces
);
    genvar ch;
    generate
        for (ch = 0; ch < 4; ch = ch + 1) begin : gen_ch
            adc_channel_processor u_proc (
                .clk      (clk),
                .rst_n    (rst_n),
                .adc_if   (adc_ch[ch])
            );
        end
    endgenerate
endmodule
```

---

## 5.4.9 — Virtual Interfaces

```systemverilog
// Testbench uses virtual interfaces
class spi_test;
    virtual interface ipace_spi_if vif;

    task run();
        vif.cs_n = 1'b0;
        vif.tx_byte = 8'hA5;
        vif.tx_valid = 1'b1;
        @(posedge vif.tx_ready);
        vif.tx_valid = 1'b0;
    endtask
endclass

// Binding in testbench
module spi_tb;
    logic clk;
    ipace_spi_if u_spi (.clk(clk));

    spi_test test_h;

    initial begin
        test_h = new();
        test_h.vif = u_spi;  // bind virtual interface
        test_h.run();
    end
endmodule
```

---

## 5.4.10 — Best Practices

1. **Use interfaces** for all multi-signal buses — SPI, I²C, ADC, AXI
2. **Define modports** for every direction combination — master, slave, monitor
3. **Use `monitor_mp`** in testbenches — no signal direction issues
4. **Parameterize interfaces** — width, depth, protocol settings
5. **Add coverage** in interfaces — protocol and functional coverage
6. **Use clocking blocks** for testbench timing control
7. **Virtual interfaces** for class-based testbenches
8. **Name interfaces consistently** — `ipace_xxx_if` for iPACE signals
9. **Avoid interface arrays** when simple — use for multi-channel only
10. **Document interface protocols** — timing diagrams alongside code

---

## 5.4.11 — References

- IEEE Std 1800-2017, Section 22 — Interfaces
- SystemVerilog for Verification, Chris Spear, Chapter 4
- iPACE-CHIP Interface Specification, Appendix A
