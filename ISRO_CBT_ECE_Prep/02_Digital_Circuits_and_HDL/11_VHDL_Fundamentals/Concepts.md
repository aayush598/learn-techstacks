# VHDL Fundamentals - Concepts

## What is VHDL
- VHSIC Hardware Description Language (VHSIC = Very High Speed Integrated Circuit)
- IEEE standard 1076
- Used to describe/simulate/synthesize digital hardware
- Behavioral, dataflow, structural modeling styles

## VHDL Design Units
```
Entity: interface (inputs/outputs/ports)
Architecture: implementation (behavior)
Configuration: binding entity-architecture
Package: shared declarations
Testbench: external stimulus
```

## Entity Declaration
```vhdl
entity and_gate is
  port (
    a, b : in  std_logic;
    y    : out std_logic
  );
end and_gate;
```
- Describes inputs/outputs (black-box interface)

## Architecture
```vhdl
architecture behavioral of and_gate is
begin
  y <= a and b;
end behavioral;
```
- Describes BEHAVIOR (what it does)

## Modeling Styles
| Style | Description |
|-------|-------------|
| Behavioral | High-level, processes, sequential |
| Dataflow | Concurrent signal assignments (<=) |
| Structural | Component instantiation (gates) |

## Concurrent vs Sequential
- Concurrent (dataflow): statements execute in parallel, order-independent
- Sequential (process): statements inside process execute in order (like software)

## Data Types
```
std_logic: 9-valued logic (U,X,0,1,Z,W,L,H,-)
std_logic_vector: array of std_logic
boolean, integer, bit
signed/unsigned (numeric_std)
```

## Std_logic values
```
U - uninitialized, X - unknown, 0, 1
Z - high impedance, W - weak
L - weak low, H - weak high, - don't care
```

## Common Operators
```
Logic: and, or, not, nand, nor, xor, xnor
Relational: =, /=, <, >, <=, >=
Arithmetic: +, - (signed/unsigned)
Concatenation: &
```

## Conditional Assignments
```vhdl
y <= a when sel='0' else b;     -- conditional
with sel select                     
  y <= a when "00",               -- selected
       b when "01",
       c when others;
```

## Process Statement (Sequential)
```vhdl
process (a, b)  -- sensitivity list
begin
  if a='1' then
    y <= b;
  else
    y <= '0';
  end if;
end process;
```

## Libraries/Packages
```vhdl
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;  -- for unsigned/signed
```
- std_logic_1164: std_logic/std_logic_vector
- numeric_std: arithmetic on signed/unsigned

## Testbench
- Entity with no ports, instantiates DUT, applies stimulus
- Used for simulation verification (not synthesizable)

---

## ISRO Key Points
- Entity = interface, Architecture = behavior
- Behavioral (process) vs dataflow (concurrent) vs structural
- std_logic 9-valued, std_logic_vector
- ieee.std_logic_1164, ieee.numeric_std
- Concurrent <= vs sequential process
