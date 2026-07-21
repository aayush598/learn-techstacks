# Telemetry Controller RTL Design

## 5.5.3 — Overview

The **telemetry controller** manages wireless communication between the
iPACE-CHIP implant and the external programmer. It formats diagnostic data
into packets, transmits via SPI to the RF front-end, and receives configuration
commands from the external system. This chapter covers the complete RTL design
of the telemetry subsystem.

---

## 5.5.4 — Telemetry Requirements

| Parameter | Value | Unit |
|-----------|-------|------|
| Data Rate | 125 | kbps |
| Packet Size | 64 | bits |
| CRC Polynomial | x^8+x^2+x+1 | — |
| Sync Pattern | 0xA5 | — |
| SPI Clock | 1 | MHz |
| Encryption | XOR scramble | — |
| TX Power | -20 | dBm |
| Operating Range | 2-15 | cm |

---

## 5.5.5 — Telemetry Controller Top Module

```systemverilog
module telemetry_controller #(
    parameter DATA_WIDTH   = 8,
    parameter PACKET_WIDTH = 64,
    parameter SPI_CLK_DIV  = 4
)(
    input  logic                    clk,
    input  logic                    rst_n,

    // SPI interface to RF front-end
    input  logic                    spi_clk_in,
    output logic                    spi_miso,
    input  logic                    spi_mosi,
    input  logic                    spi_cs_n,

    // Data inputs
    input  logic [7:0]              device_id,
    input  logic [7:0]              status_byte,
    input  logic [11:0]             battery_voltage,
    input  logic [11:0]             lead_impedance,
    input  logic [11:0]             atrial_adc,
    input  logic [11:0]             vent_adc,

    // Control
    input  logic                    telemetry_enable,
    input  logic                    send_trigger,
    input  logic                    clear_faults,

    // Status
    output logic                    telemetry_active,
    output logic                    tx_busy,
    output logic                    rx_valid,
    output logic [7:0]              rx_data,
    output logic [7:0]              tx_data,
    output logic                    tx_valid,
    input  logic                    tx_ready,

    // Interrupts
    output logic                    irq_telemetry
);

    typedef enum logic [2:0] {
        TEL_IDLE    = 3'd0,
        TEL_COLLECT = 3'd1,
        TEL_BUILD   = 3'd2,
        TEL_CRC     = 3'd3,
        TEL_TX      = 3'd4,
        TEL_RX      = 3'd5,
        TEL_DONE    = 3'd6
    } telem_state_t;

    telem_state_t state;
    logic [PACKET_WIDTH-1:0] tx_packet;
    logic [PACKET_WIDTH-1:0] rx_packet;
    logic [$clog2(PACKET_WIDTH)-1:0] bit_count;
    logic [7:0] crc_reg;

    // CRC function
    function automatic logic [7:0] crc8(
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

    // Packet assembly
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state            <= TEL_IDLE;
            tx_packet        <= '0;
            crc_reg          <= 8'hFF;
            bit_count        <= '0;
            telemetry_active <= 1'b0;
            tx_busy          <= 1'b0;
            tx_data          <= '0;
            tx_valid         <= 1'b0;
        end else begin
            tx_valid <= 1'b0;  // default pulse

            case (state)
                TEL_IDLE: begin
                    telemetry_active <= 1'b0;
                    tx_busy          <= 1'b0;
                    if (send_trigger && telemetry_enable) begin
                        state <= TEL_COLLECT;
                        tx_busy <= 1'b1;
                    end
                end

                TEL_COLLECT: begin
                    // Assemble packet fields
                    tx_packet <= {
                        4'hA,                    // sync
                        4'h1,                    // packet type
                        device_id,               // 8 bits
                        status_byte,             // 8 bits
                        {4'b0, battery_voltage},  // 16 bits
                        {4'b0, lead_impedance},   // 16 bits
                        atrial_adc[11:0],         // 12 bits
                        vent_adc[11:0],           // 12 bits
                        8'h00                     // CRC placeholder
                    };
                    state <= TEL_BUILD;
                end

                TEL_BUILD: begin
                    // Calculate CRC
                    crc_reg <= 8'hFF;
                    crc_reg <= crc8(tx_packet[63:56], crc_reg);
                    crc_reg <= crc8(tx_packet[55:48], crc_reg);
                    crc_reg <= crc8(tx_packet[47:40], crc_reg);
                    crc_reg <= crc8(tx_packet[39:32], crc_reg);
                    crc_reg <= crc8(tx_packet[31:24], crc_reg);
                    crc_reg <= crc8(tx_packet[23:16], crc_reg);
                    crc_reg <= crc8(tx_packet[15:8],  crc_reg);
                    crc_reg <= crc8(tx_packet[7:0],   crc_reg);
                    tx_packet[7:0] <= crc_reg;
                    state <= TEL_TX;
                end

                TEL_TX: begin
                    telemetry_active <= 1'b1;
                    if (tx_ready && !tx_valid) begin
                        tx_data  <= tx_packet[bit_count +: 8];
                        tx_valid <= 1'b1;
                        bit_count <= bit_count + 8;
                        if (bit_count >= PACKET_WIDTH - 8) begin
                            state <= TEL_DONE;
                        end
                    end
                end

                TEL_DONE: begin
                    telemetry_active <= 1'b0;
                    tx_busy          <= 1'b0;
                    bit_count        <= '0;
                    state            <= TEL_IDLE;
                end

                default: state <= TEL_IDLE;
            endcase
        end
    end

    // RX handling
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            rx_packet <= '0;
            rx_valid  <= 1'b0;
            rx_data   <= '0;
        end else if (spi_cs_n && !spi_cs_n_prev) begin
            // CS assertion — start receiving
            rx_packet <= '0;
            rx_valid  <= 1'b0;
        end else if (!spi_cs_n && spi_mosi_valid) begin
            rx_packet <= {rx_packet[PACKET_WIDTH-2:0], spi_mosi};
        end else if (spi_cs_n && !spi_cs_n_prev) begin
            // CS deassertion — packet complete
            rx_valid <= 1'b1;
            rx_data  <= rx_packet[7:0];
        end
    end

    reg spi_cs_n_prev;
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            spi_cs_n_prev <= 1'b1;
        else
            spi_cs_n_prev <= spi_cs_n;
    end

    // Interrupt generation
    assign irq_telemetry = rx_valid;

endmodule
```

---

## 5.5.6 — Packet Builder with Scrambling

```systemverilog
module telemetry_packet_builder (
    input  logic        clk,
    input  logic        rst_n,
    input  logic [7:0]  device_id,
    input  logic [7:0]  status,
    input  logic [11:0] battery_mv,
    input  logic [11:0] impedance,
    input  logic [11:0] atrial_data,
    input  logic [11:0] vent_data,
    input  logic        send,
    output logic [63:0] packet_out,
    output logic        packet_ready
);

    typedef enum logic [1:0] {
        PB_IDLE   = 2'd0,
        PB_BUILD  = 2'd1,
        PB_CRC    = 2'd2,
        PB_SCRAMBLE = 2'd3
    } pb_state_t;

    pb_state_t state;
    logic [63:0] raw_packet;
    logic [7:0]  crc_val;

    // XOR scrambler key (fixed pattern for iPACE-CHIP)
    localparam logic [63:0] SCRAMBLE_KEY = 64'hA5A5_5A5A_C3C3_3C3C;

    function automatic logic [7:0] calc_crc(
        input logic [63:0] data
    );
        logic [7:0] crc;
        int i;
        begin
            crc = 8'hFF;
            for (i = 0; i < 8; i++)
                crc = calc_crc8(data[i*8 +: 8], crc);
            return crc;
        end
    endfunction

    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state         <= PB_IDLE;
            packet_out    <= '0;
            packet_ready  <= 1'b0;
        end else begin
            packet_ready <= 1'b0;

            case (state)
                PB_IDLE: begin
                    if (send) begin
                        raw_packet <= {
                            4'hA, 4'h1,
                            device_id, status,
                            {4'b0, battery_mv},
                            {4'b0, impedance},
                            atrial_data, vent_data,
                            8'h00
                        };
                        state <= PB_BUILD;
                    end
                end

                PB_BUILD: begin
                    crc_val <= calc_crc(raw_packet);
                    raw_packet[7:0] <= calc_crc(raw_packet);
                    state <= PB_SCRAMBLE;
                end

                PB_SCRAMBLE: begin
                    packet_out   <= raw_packet ^ SCRAMBLE_KEY;
                    packet_ready <= 1'b1;
                    state        <= PB_IDLE;
                end
            endcase
        end
    end

endmodule
```

---

## 5.5.7 — SPI Slave for Telemetry

```systemverilog
module telemetry_spi_slave (
    input  logic       clk,
    input  logic       rst_n,
    input  logic       spi_clk,
    input  logic       spi_mosi,
    output logic       spi_miso,
    input  logic       spi_cs_n,
    output logic [7:0] rx_byte,
    output logic       rx_valid,
    input  logic [7:0] tx_byte,
    input  logic       tx_load,
    output logic       tx_ready
);

    typedef enum logic [1:0] {
        SPI_IDLE  = 2'd0,
        SPI_XFER  = 2'd1,
        SPI_DONE  = 2'd2
    } spi_state_t;

    spi_state_t state;
    logic [2:0]  bit_idx;
    logic [7:0]  shift_reg;
    logic        spi_clk_prev;
    logic        spi_cs_n_prev;

    // Edge detection
    wire spi_clk_rising  = (spi_clk && !spi_clk_prev);
    wire spi_clk_falling = (!spi_clk && spi_clk_prev);
    wire cs_falling      = (!spi_cs_n && spi_cs_n_prev);
    wire cs_rising       = (spi_cs_n && !spi_cs_n_prev);

    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            spi_clk_prev <= 1'b0;
            spi_cs_n_prev <= 1'b1;
        end else begin
            spi_clk_prev <= spi_clk;
            spi_cs_n_prev <= spi_cs_n;
        end
    end

    // SPI Mode 0:0 — CPOL=0, CPHA=0
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state     <= SPI_IDLE;
            shift_reg <= 8'h00;
            bit_idx   <= 3'd0;
            rx_byte   <= 8'h00;
            rx_valid  <= 1'b0;
            spi_miso  <= 1'b0;
            tx_ready  <= 1'b1;
        end else begin
            rx_valid <= 1'b0;

            case (state)
                SPI_IDLE: begin
                    tx_ready <= 1'b1;
                    if (cs_falling) begin
                        state     <= SPI_XFER;
                        bit_idx   <= 3'd7;
                        shift_reg <= tx_byte;
                        spi_miso  <= tx_byte[7];
                    end
                end

                SPI_XFER: begin
                    if (spi_clk_rising) begin
                        // Sample MOSI on rising edge
                        shift_reg[bit_idx] <= spi_mosi;
                    end
                    if (spi_clk_falling) begin
                        // Shift out MISO on falling edge
                        if (bit_idx > 0) begin
                            bit_idx   <= bit_idx - 1;
                            spi_miso  <= shift_reg[bit_idx - 1];
                        end
                    end
                    if (cs_rising) begin
                        state    <= SPI_DONE;
                        rx_valid <= 1'b1;
                        rx_byte  <= shift_reg;
                    end
                end

                SPI_DONE: begin
                    state    <= SPI_IDLE;
                    tx_ready <= 1'b1;
                end
            endcase
        end
    end

endmodule
```

---

## 5.5.8 — UART Transmitter for Debug Telemetry

```systemverilog
module uart_transmitter #(
    parameter CLK_FREQ = 32768,
    parameter BAUD_RATE = 9600
)(
    input  logic       clk,
    input  logic       rst_n,
    input  logic [7:0] tx_data,
    input  logic       tx_start,
    output logic       tx_serial,
    output logic       tx_busy
);

    localparam BAUD_DIV = CLK_FREQ / BAUD_RATE;

    typedef enum logic [1:0] {
        UART_IDLE  = 2'd0,
        UART_START = 2'd1,
        UART_DATA  = 2'd2,
        UART_STOP  = 2'd3
    } uart_state_t;

    uart_state_t state;
    logic [$clog2(BAUD_DIV)-1:0] baud_count;
    logic [2:0] bit_idx;
    logic [7:0] shift_reg;

    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state      <= UART_IDLE;
            tx_serial  <= 1'b1;
            tx_busy    <= 1'b0;
            baud_count <= '0;
            bit_idx    <= '0;
        end else begin
            case (state)
                UART_IDLE: begin
                    tx_serial <= 1'b1;
                    tx_busy   <= 1'b0;
                    if (tx_start) begin
                        state     <= UART_START;
                        shift_reg <= tx_data;
                        baud_count <= '0;
                        tx_busy   <= 1'b1;
                    end
                end

                UART_START: begin
                    tx_serial <= 1'b0;  // start bit
                    if (baud_count == BAUD_DIV - 1) begin
                        state     <= UART_DATA;
                        baud_count <= '0;
                        bit_idx   <= 3'd0;
                    end else
                        baud_count <= baud_count + 1;
                end

                UART_DATA: begin
                    tx_serial <= shift_reg[bit_idx];
                    if (baud_count == BAUD_DIV - 1) begin
                        baud_count <= '0;
                        if (bit_idx == 3'd7)
                            state <= UART_STOP;
                        else
                            bit_idx <= bit_idx + 1;
                    end else
                        baud_count <= baud_count + 1;
                end

                UART_STOP: begin
                    tx_serial <= 1'b1;  // stop bit
                    if (baud_count == BAUD_DIV - 1) begin
                        state <= UART_IDLE;
                    end else
                        baud_count <= baud_count + 1;
                end
            endcase
        end
    end

endmodule
```

---

## 5.5.9 — Best Practices

1. **CRC on every packet** — detect transmission errors
2. **Scramble data** — prevent repeated pattern power issues
3. **Pipeline packet assembly** — don't block during TX
4. **Error detection** — check CRC on received packets
5. **Power management** — gate telemetry when not active
6. **Fault reporting** — include status byte in every packet
7. **Debug UART** — separate debug channel for lab testing
8. **Test with bit-error injection** — verify error handling

---

## 5.5.10 — References

- iPACE-CHIP Telemetry Specification, v2.0
- Bluetooth Low Energy Packet Format (reference)
- ISO 14708-1:2014 — Communication protocols
