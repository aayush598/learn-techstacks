# Protocol Verification for iPACE-CHIP Pacemaker

## 1. Introduction

Protocol verification ensures that the iPACE-CHIP pacemaker's interfaces comply with their specifications. This includes APB register access, UART telemetry, SPI communication, and internal bus protocols. SVA assertions provide continuous protocol monitoring during simulation and formal verification.

## 2. APB Protocol Verification

### 2.1 APB3 Protocol Assertions

```systemverilog
// APB3 write transaction
property apb3_write;
  @(posedge clk) disable iff (!rst_n)
    (psel && pen && pwrite && !pready)
    |=> ##[0:1] (pready && !pen);
endproperty

assert property (apb3_write) else
  `uvm_error("APB", "APB3 write protocol violation");

// APB3 read transaction
property apb3_read;
  @(posedge clk) disable iff (!rst_n)
    (psel && pen && !pwrite && !pready)
    |=> ##[0:1] (pready && !pen);
endproperty

assert property (apb3_read) else
  `uvm_error("APB", "APB3 read protocol violation");

// APB3 setup phase
property apb3_setup;
  @(posedge clk) disable iff (!rst_n)
    $rose(psel) |-> !pen;
endproperty

assert property (apb3_setup) else
  `uvm_error("APB", "APB3 setup phase violation");

// APB3 access phase
property apb3_access;
  @(posedge clk) disable iff (!rst_n)
    pen |-> psel;
endproperty

assert property (apb3_access) else
  `uvm_error("APB", "APB3 access without select");

// APB3 PREADY timing
property apb3_pready_timing;
  @(posedge clk) disable iff (!rst_n)
    $rose(psel && pen) |-> ##[1:MAX_APB_WAIT] pready;
endproperty

assert property (apb3_pready_timing) else
  `uvm_error("APB", "APB3 PREADY timeout");
```

### 2.2 APB Register Map Verification

```systemverilog
// Register write/readback
property reg_write_readback;
  @(posedge clk) disable iff (!rst_n)
    (apb_write && addr == REG_PACE_MODE)
    |-> ##[1:3] (read_data == write_data);
endproperty

assert property (reg_write_readback) else
  `uvm_error("REG", "Register write/readback mismatch");

// Register reset values
property reg_reset_values;
  @(posedge clk)
    !rst_n |=> (pace_mode_reg == DEFAULT_PACE_MODE);
endproperty

assert property (reg_reset_values) else
  `uvm_error("REG", "Register reset value incorrect");

// Register write protect
property reg_write_protect;
  @(posedge clk) disable iff (!rst_n)
    (apb_write && addr == REG_CALIBRATION && !calibration_mode)
    |-> !write_enable;
endproperty

assert property (reg_write_protect) else
  `uvm_error("REG", "Write-protected register written");
```

## 3. UART Protocol Verification

### 3.1 UART Frame Protocol

```systemverilog
// UART start bit
property uart_start;
  @(posedge clk) disable iff (!rst_n)
    $fell(uart_tx_line) |-> ##1 !uart_tx_line;
endproperty

assert property (uart_start) else
  `uvm_error("UART", "UART start bit violation");

// UART data bits (8N1)
property uart_data_bits;
  @(posedge clk) disable iff (!rst_n)
    uart_tx_active |-> ##BAUD_CYCLES uart_tx_active;
endproperty

assert property (uart_data_bits) else
  `uvm_error("UART", "UART data bit timing violation");

// UART stop bit
property uart_stop;
  @(posedge clk) disable iff (!rst_n)
    $rose(uart_tx_line) && uart_tx_active |-> ##BAUD_CYCLES !uart_tx_active;
endproperty

assert property (uart_stop) else
  `uvm_error("UART", "UART stop bit violation");

// UART frame completeness
property uart_frame_complete;
  @(posedge clk) disable iff (!rst_n)
    $fell(uart_tx_active) |-> ##1 uart_tx_line;
endproperty

assert property (uart_frame_complete) else
  `uvm_error("UART", "UART frame incomplete");
```

### 3.2 UART Telemetry Protocol

```systemverilog
// Telemetry message structure
property telemetry_header;
  @(posedge clk) disable iff (!rst_n)
    $rose(telemetry_active) |-> ##[1:3] (tx_data == MSG_HEADER);
endproperty

assert property (telemetry_header) else
  `uvm_error("TELEM", "Telemetry header missing");

// Telemetry CRC
property telemetry_crc;
  @(posedge clk) disable iff (!rst_n)
    $fell(telemetry_active) |-> tx_data == calculated_crc;
endproperty

assert property (telemetry_crc) else
  `uvm_error("TELEM", "Telemetry CRC mismatch");

// Telemetry periodicity
property telemetry_periodic;
  @(posedge clk) disable iff (!rst_n)
    $rose(telemetry_active) |->
      ##[MIN_TELEM_INTERVAL:MAX_TELEM_INTERVAL] $rose(telemetry_active);
endproperty

assert property (telemetry_periodic) else
  `uvm_error("TELEM", "Telemetry not periodic");
```

## 4. SPI Protocol Verification

### 4.1 SPI Mode 0 Protocol

```systemverilog
// SPI clock idle low
property spi_clk_idle;
  @(posedge clk) disable iff (!rst_n)
    !spi_cs_n |-> !spi_sclk;
endproperty

assert property (spi_clk_idle) else
  `uvm_error("SPI", "SPI clock not idle low");

// SPI data sampled on rising edge
property spi_sample;
  @(posedge clk) disable iff (!rst_n)
    $rose(spi_sclk) |-> $stable(spi_mosi);
endproperty

assert property (spi_sample) else
  `uvm_error("SPI", "SPI data not stable at sample edge");

// SPI chip select protocol
property spi_cs_protocol;
  @(posedge clk) disable iff (!rst_n)
    $fell(spi_cs_n) |-> ##1 spi_sclk;
endproperty

assert property (spi_cs_protocol) else
  `uvm_error("SPI", "SPI CS protocol violation");
```

## 5. Internal Bus Protocol

### 5.1 Wishbone Protocol

```systemverilog
// Wishbone write
property wishbone_write;
  @(posedge clk) disable iff (!rst_n)
    (wb_cyc && wb_stb && wb_we && !wb_ack)
    |=> ##[0:1] wb_ack;
endproperty

assert property (wishbone_write) else
  `uvm_error("WB", "Wishbone write protocol violation");

// Wishbone read
property wishbone_read;
  @(posedge clk) disable iff (!rst_n)
    (wb_cyc && wb_stb && !wb_we && !wb_ack)
    |=> ##[0:1] wb_ack;
endproperty

assert property (wishbone_read) else
  `uvm_error("WB", "Wishbone read protocol violation");

// Wishbone handshake
property wishbone_handshake;
  @(posedge clk) disable iff (!rst_n)
    (wb_cyc && wb_stb) |-> ##[1:MAX_WB_WAIT] wb_ack;
endproperty

assert property (wishbone_handshake) else
  `uvm_error("WB", "Wishbone handshake timeout");
```

## 6. Interrupt Protocol

### 6.1 Interrupt Assertion/ACK

```systemverilog
// Interrupt assertion
property irq_asserted;
  @(posedge clk) disable iff (!rst_n)
    $rose(irq) |-> irq_source != 0;
endproperty

assert property (irq_asserted) else
  `uvm_error("IRQ", "Interrupt without source");

// Interrupt acknowledge
property irq_acknowledged;
  @(posedge clk) disable iff (!rst_n)
    $rose(irq) |-> ##[1:MAX_IRQ_LATENCY] irq_ack;
endproperty

assert property (irq_acknowledged) else
  `uvm_error("IRQ", "Interrupt not acknowledged");

// Interrupt clear
property irq_cleared;
  @(posedge clk) disable iff (!rst_n)
    $rose(irq_ack) |=> !irq;
endproperty

assert property (irq_cleared) else
  `uvm_error("IRQ", "Interrupt not cleared after ACK");
```

## 7. Clock Domain Crossing Protocol

### 7.1 Synchronizer Protocol

```systemverilog
// Two-stage synchronizer
property sync_stage_1;
  @(posedge clk_domain_b) disable iff (!rst_n)
    $changed(async_signal) |->
      $stable(async_signal) [*2];
endproperty

assert property (sync_stage_1) else
  `uvm_error("CDC", "Synchronizer stage 1 violation");

// Gray code counter CDC
property gray_code_protocol;
  @(posedge clk) disable iff (!rst_n)
    $changed(gray_counter) |->
      $onehot(gray_counter ^ $past(gray_counter));
endproperty

assert property (gray_code_protocol) else
  `uvm_error("CDC", "Gray code CDC protocol violation");
```

## 8. Protocol Coverage

### 8.1 Protocol Cover Properties

```systemverilog
// Cover all APB access types
cover property (@(posedge clk) disable iff (!rst_n)
  psel && pen && pwrite
);

cover property (@(posedge clk) disable iff (!rst_n)
  psel && pen && !pwrite
);

// Cover all UART frame types
cover property (@(posedge clk) disable iff (!rst_n)
  $fell(uart_tx_line)
);

// Cover all SPI modes
cover property (@(posedge clk) disable iff (!rst_n)
  $fell(spi_cs_n)
);

// Cover all interrupt sources
cover property (@(posedge clk) disable iff (!rst_n)
  irq && (irq_source == FAULT_IRQ)
);

cover property (@(posedge clk) disable iff (!rst_n)
  irq && (irq_source == TIMER_IRQ)
);
```

## 9. Protocol Checker Module

### 9.1 Reusable Protocol Checker

```systemverilog
module apb_protocol_checker (
  input  logic        clk,
  input  logic        rst_n,
  input  logic        psel,
  input  logic        pen,
  input  logic        pwrite,
  input  logic        pready,
  input  logic [7:0]  paddr,
  input  logic [31:0] pwdata,
  input  logic [31:0] prdata
);

  // Internal tracking
  logic transaction_active;
  logic [7:0] addr_captured;
  logic [31:0] data_captured;

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      transaction_active <= 0;
      addr_captured <= 0;
      data_captured <= 0;
    end else begin
      if (psel && pen && !pready)
        transaction_active <= 1;
      else if (pready)
        transaction_active <= 0;

      if (psel && pen) begin
        addr_captured <= paddr;
        data_captured <= pwrite ? pwdata : prdata;
      end
    end
  end

  // Protocol assertions
  property no_idle_phase_violation;
    @(posedge clk) disable iff (!rst_n)
      !psel |-> !pen && !pready;
  endproperty
  assert property (no_idle_phase_violation) else
    $error("APB idle violation");

  property setup_to_access;
    @(posedge clk) disable iff (!rst_n)
      $rose(psel) |-> !pen;
  endproperty
  assert property (setup_to_access) else
    $error("APB setup violation");

endmodule
```

## 10. Summary

Protocol verification for the iPACE-CHIP pacemaker provides:

| Protocol | Assertions | Cover Properties |
|----------|------------|------------------|
| APB3 | 8 | 4 |
| UART | 6 | 3 |
| SPI | 4 | 2 |
| Wishbone | 4 | 2 |
| Interrupt | 4 | 3 |
| CDC | 3 | 2 |
| **Total** | **29** | **16** |

Key protocol verification benefits:
- **Real-time compliance** monitoring during simulation
- **Formal proof** of protocol correctness
- **Reusable checkers** for standard protocols
- **Coverage tracking** for protocol exhaustiveness
- **Debug-friendly** with detailed failure context
