# VHDL Advanced - Syntax Reference

## FOR-Generate
```vhdl
gen_label: for i in 0 to N-1 generate
  ins: entity work.mux generic map(...) port map(...);
end generate gen_label;
```

## IF-Generate
```vhdl
gen: if COND generate
  ... components ...
else generate
  ... other ...
end generate;
```

## Generic parameterized entity
```vhdl
entity shift is
  generic (N : positive := 8);
  port (din  : in  std_logic_vector(N-1 downto 0);
        q    : out std_logic_vector(N-1 downto 0);
        clk  : in  std_logic);
end shift;
-- instantiate with different N:
-- u1: shift generic map(N=>16) port map(...);
```

## Function
```vhdl
function to_3bit(v : integer) return std_logic_vector is
  variable r : std_logic_vector(2 downto 0);
begin
  r := conv_std_logic_vector(v,3);  -- or std_logic_vector(to_unsigned(...))
  return r;
end function;
```

## Signal vs Variable (behavior)
```vhdl
-- Signal (delta-delayed):
process
  signal s : std_logic;
begin
  s <= '1';   -- takes effect end of process; if read before, old value
  y <= s;
end process;

-- Variable (immediate):
process
  variable v : integer;
begin
  v := v + 1;   -- immediate update usable right away
  y <= v;
end process;
```

## Package declaration & body
```vhdl
package mypkg is
  function max2(a,b:integer) return integer;
  constant ZERO : std_logic := '0';
end package;

package body mypkg is
  function max2(a,b:integer) return integer is
  begin
    if a>b then return a; else return b; end if;
  end function;
end package body;
-- use: use work.mypkg.all;
```

## Moore-style FSM (2-process template)
```vhdl
type state_t is (S0, S1, S2);
signal state, nstate : state_t;

-- next state logic
process(state, input)
begin
  case state is
    when S0 => if input='1' then nstate<=S1; else nstate<=S0; end if;
    ...
  end case;
end process;

-- state register
process(clk, rst)
begin
  if rst='1' then state<=S0;
  elsif rising_edge(clk) then state<=nstate;
  end if;
end process;
```

## Attributes
```vhdl
clk'event          -- true on any edge
clk'event and clk='1' -- rising edge equivalent
D'ex'high, D'ex'left, D'ex'range -- array bounds
```

## Synthesizable vs not
| Synthesizable | Simulation only |
|---------------|-----------------|
| process, if, case | after (delay) |
| signal/variable | wait (unclocked) |
| generate, generic | file I/O |
| functions | transport delay |
| rising_edge | assert/report |

## Quick Reference
| Construct | Purpose |
|-----------|---------|
| generate for/if | replication/conditional structure |
| generic | parameterization |
| function/procedure | reusable logic |
| package | shared declarations |
| signal | scheduled (<=) |
| variable | immediate (:=) |
| record/array | composite types |
