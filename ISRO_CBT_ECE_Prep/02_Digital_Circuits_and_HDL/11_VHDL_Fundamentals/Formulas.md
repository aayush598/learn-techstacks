# VHDL Fundamentals - Formulas & Syntax Reference

## Entity Template
```vhdl
entity <name> is
  port (
    <port_name> : <mode> <type>;
    ...
  );
end <name>;
```
Modes: in, out, inout, buffer

## Architecture styles
```vhdl
-- Dataflow (concurrent)
architecture dataflow of <n> is
begin
  y <= a and b;
end dataflow;

-- Behavioral (sequential, in process)
architecture behavioral of <n> is
begin
  process(a,b)
  begin
    y <= a and b;
  end process;
end behavioral;

-- Structural
architecture structural of <n> is
  component gate
    port (a,b: in std_logic; y: out std_logic);
  end component;
begin
  g1: gate port map(a=>a, b=>b, y=>y);
end structural;
```

## Operator precedence (high to low)
```
not
abs, unary -
* , /, mod, rem
+ , -
& (concat)
=, /=, <, <=, >, >=
and, or, nand, nor, xor, xnor  (note: <= is relational, low)
```

## Std_logic values (9-valued)
```
'U' uninit, 'X' unknown, '0' low, '1' high, 'Z' high-Z
'W' weak unknown, 'L' weak low, 'H' weak high, '-' don't care
```

## Conditional / selected signals
```vhdl
-- conditional (else-if like)
s <= a when rst='1' else b;

-- selected (case-like)
with sel select
  s <= a when "00",
       b when "01",
       c when others;
```

## Process forms
```vhdl
-- combinational (no clock)
process(all inputs)
begin ... end process;

-- sequential (clocked)
process(clk)
begin
  if rising_edge(clk) then
    ...
  end if;
end process;

-- register (D FF) template
process(clk)
begin
  if rising_edge(clk) then
    q <= d;
  end if;
end process;
```

## Declaring signals & variables
```vhdl
signal s : std_logic := '0';
signal vec : std_logic_vector(3 downto 0);
variable v : integer := 0;   -- in process only
constant K : integer := 5;
```

## IEEE packages
```vhdl
use ieee.std_logic_1164.all;   -- std_logic, std_logic_vector
use ieee.numeric_std.all;      -- unsigned, signed, + ,-
use ieee.std_logic_arith.all;  (legacy, avoid)
```

## Common idioms
```vhdl
y <= (others => '0');          -- fill with zeros
-- counter
if rising_edge(clk) then
  if rst='1' then cnt <= 0;
  elsif cnt = MAX then cnt <= 0;
  else cnt <= cnt + 1; end if;
end if;
```

## Quick Reference
| Concept | VHDL |
|---------|------|
| Interface | entity |
| Behavior | architecture |
| Signal assign | <= |
| Variable assign | := |
| Sequential | process |
| std_logic logic | std_logic_1164 |
| arithmetic | numeric_std |
| rising edge | rising_edge(clk) |
