# VHDL Advanced - Concepts

## Advanced VHDL Constructs
- Procedural/generic design, package bodies
- Records, arrays, functions, procedures
- Configurations, generics, generics for parameterization

## Generate Statements
- Create repeated structures (loops at elaboration time)
```vhdl
gen: for i in 0 to 7 generate
  dff: entity work.dff port map(d=>d(i), q=>q(i), clk=>clk);
end generate;
```
- FOR generate: repeat structure N times (arrays)
- IF generate: conditional inclusion

## Generics
- Parameterize module (widths, sizes) at instantiation
```vhdl
entity reg is
  generic (W : integer := 8);
  port (d: in std_logic_vector(W-1 downto 0); ...);
end reg;
```
- Reused with different parameters, improves design flexibility

## Functions & Procedures
```vhdl
function f(x: integer) return integer is
begin
  return x*2;
end function;

procedure p(signal x: out std_logic) is   -- procedure
begin
  x <= '1';
end procedure;
```
- Package: reuse across designs

## Types: Records, Arrays
```vhdl
type instr is record
  opcode : std_logic_vector(3 downto 0);
  data   : std_logic_vector(7 downto 0);
end record;

type matrix is array(0 to 3,0 to 3) of integer;
```

## FSMD / State machine modeling (sequential)
```vhdl
type state_type is (IDLE, RUN, DONE);
signal state, nstate : state_type;
-- 2-3 process FSM: reg + comb + output
```

## Signals vs Variables
| Feature | Signal | Variable |
|---------|--------|----------|
| Scope | whole architecture | process only |
| Assignment | <= | := |
| Update | end of process/delta | immediate |
| Synthesis | wires/registers | combinational |
- Signals: scheduled (delta), variables: immediate

## Multiple/Concurrent/Delay
- Delta cycle: signal updates delayed to end of process
- Important for correct simulation of sequential logic

## Configurations & Component binding
```vhdl
configuration cfg of top is
  for struct
    for u1 : gate use entity work.andg(behavioral);
    end for;
  end for;
end cfg;
```
- Select which architecture to use for a component

## Behavioral vs Synthesizable
- Simulation constructs (after, wait, file, delay) often NOT synthesizable
- Synthesis subset: processes, assignments, if/case, generate

## Testbench advanced
- Clock generation (process with wait)
- Stimulus generation
- Assertions / checking outputs

## Clocked vs combinational sensitivity
- Sequential: sensitivity list has clock (+ async reset)
- Combinational: all read inputs in sensitivity list

## Attributes
- 'EVENT, rising_edge, D'range, etc.
```vhdl
if clk'event and clk='1' then  -- equivalent to rising_edge
```

---

## ISRO Key Points
- Generate (for/if) -> repeated structure
- Generic -> parameterization
- Signal <= delayed, Variable := immediate
- Function/procedure, package
- State machine modeling
- Synthesizable subset vs simulation-only
