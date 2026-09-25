# ECE Circuit snippet authoring (md_book `/circuit`)

What code you type, and how, for the ECE schematics that render on
md_book's `/circuit` studio page. Everything here is verified against the
actual render pipeline (`scripts/render_circuit.py` running under
`${HOME}/.cache/md_book/.circuit-venv`, schemdraw 0.23), with real element
anchor coordinates shown from real renders.

---

## 1. The ONE job of a snippet

Your snippet is a short **schemdraw** program. The renderer:
1. Starts a fresh `schemdraw.Drawing()`.
2. `exec`s your code **inside** `with Drawing():`.
3. Emits the drawing as inline SVG back to the page.

That's it. Your text → inline SVG in the website. Nothing is written to
diskley and nothing opens on your OS.

---

## 2. The syntax: a crash course

### 2.1 You get pre-made aliases — use them

Inside every snippet these names already exist:

| Name          | What it is                     | Typical use             |
|---------------|--------------------------------|-------------------------|
| `elm`         | `schemdraw.elements` module    | `elm.Resistor()...`     |
| `V`           | `elm.SourceV` (voltage src)    | `V = elm.SourceV()...`  |
| `R`           | `elm.Resistor`                 | `R = elm.Resistor()...` |
| `C`           | `elm.Capacitor`                | `elm.Capacitor()...`    |
| `L`           | `elm.Inductor`                 | `elm.Inductor()...`     |
| `D` / `LED`   | `elm.Diode` / `elm.LED`        | `elm.LED()...`          |
| `G`           | `elm.Ground`                   | `elm.Ground()`          |
| `W` / `WIRE`  | `elm.Line` (wire)              | `WIRE().right()`        |

You can also use `schemdraw` itself if you need something fancier.

### 2.2 Elements chain together

schemdraw is *relative*: each new element starts **where the previous one
ended**. You steer with `.up() .down() .right() .left()`, and each element
knows its own size (a resistor is 3 units, a line is 1 unit by default).

```python
V = elm.SourceV().up().label("V_in 10V")
R1 = elm.Resistor().right().label("R1 10k", loc="bottom")
elm.Line().right()
R2 = elm.Resistor().down().label("R2 10k", loc="bottom")
elm.Line().down()
elm.Line().left()
elm.Line().up().to(V.start)   # <-- close the loop into V's negative terminal
elm.Ground()
```

### 2.3 Labels

`.label("your text")` puts a label on an element. Use `loc` to position it:
- `loc="bottom"` — below the element (common for resistors).
- `loc="top"` — above.
- `loc="left"` / `loc="right"` — beside it.

```python
elm.Resistor().right().label("R1 10k", loc="bottom")
```

### 2.4 THE critical rule: your circuit MUST be a closed loop

**schemdraw does NOT auto-connect the last element back to the first.**
If your return rail never reaches the source's **negative terminal**, you draw
an open circuit: the source dangles, current can't flow, and any label/
junction next to it reads as a floating island.

Study this real render (your exact 7-element snippet):

```
0 SourceV     start=(0,0)   end=(0,3)    negative terminal is at (0,0)
1 Resistor    start=(0,3)   end=(3,3)
2 Line        start=(3,3)   end=(6,3)
3 Resistor    start=(6,3)   end=(6,0)
4 Line        start=(6,0)   end=(6,-3)
5 Line        start=(6,-3)  end=(3,-3)   <-- rail stops at x=3
6 Ground      start=(3,-3)  end=(3,-3)   <-- dangles here, node (0,0) floating
```

The bottom rail returns left **only to `x=3`**, then `Ground` sits there.
Negative terminal `(0,0)` is never tied in → **open circuit**.

**Same circuit, closed** — just add the return leg up to `V.start`:

```python
V = elm.SourceV().up().label("V_in 10V")
R1 = elm.Resistor().right().label("R1 10k", loc="bottom")
elm.Line().right()
R2 = elm.Resistor().down().label("R2 10k", loc="bottom")
elm.Line().down()
elm.Line().left()
elm.Line().up().to(V.start)   # return rail climbs to (0,0) = V's negative term
elm.Ground()
```
Verified trace of the closed version:
```
5 Line  start=(6,-3) end=(3,-3)
6 Line  start=(3,-3) end=(3,0)     <- up
7 Line  start=(3,0)  end=(0,0)     <- to(V.start) — reaches the negative terminal
8 Ground
```
Now the bottom rail ties into `(0,0)` and the loop is closed.

### 2.5 Bare statements — NOT a `with Drawing()` of your own

**Do not** write `with schemdraw.Drawing() as d:` inside your snippet.
The renderer already wraps your code in its own `Drawing()` context.
If you open a second drawing, elements attach to *that* drawing, the inner
one is never emitted, and you get an empty `viewBox="inf inf ..."` result.

WRONG:
```python
with schemdraw.Drawing() as d:
    d += elm.Resistor().right()
```

RIGHT (bare statements — the renderer's drawing is already open):
```python
V = elm.SourceV().up().label("V_in 10V")
elm.Resistor().right().label("R1 10k", loc="bottom")
# ... keep chaining bare statements ...
```

---

## 3. Pick-your-side convention (why it matters)

`schemdraw.Drawing` places the source with its **negative terminal at its
`start` anchor**. Common renderers do one of:

A. **Voltage source ONE way + ground at negative**:
```python
V = elm.SourceV().up().label("V_in 10V")
R1 = elm.Resistor().right().label("R1 10k", loc="bottom")
elm.Line().right()
R2 = elm.Resistor().down().label("R2 10k", loc="bottom")
elm.Line().down()
elm.Line().left()
elm.Line().down().to(elm.Ground)   # bottom rail to the ground node
# or, classic:
elm.Line().up().to(V.start)        # return to negative terminal
elm.Ground()
```
(Wire explicitly to the negative terminal, or to the ground node — both are
closed and correct.)

B. **Source going up, then drop rails to a ground plane** (sedan common in
tutorials). Whatever you choose, **pick one and be consistent** so no terminal
is left floating.

---

## 4. Label / value formatting

- Use plain text: `label("10k")`, `label("R1 10k", loc="bottom")`.
- Unit suffixes are just text — schemdraw doesn't parse them; write what you
  want to see: `0100n`, `10k`, `1uF` are all fine.
- Put a dot on shared nodes explicitly if you want junction emphasis:
  ```python
  elm.Dot().label("out", loc="right")
  ```

---

## 5. What the renderer returns & errors

- Success → `{ "svg": "<inline svg string>…" }`
- Any Python error → `{ "error": "<last traceback lines>" }` (HTTP 500).
- `viewBox="inf inf 5 5"` → empty drawing → your snippet opened its own
  `Drawing()` (see §2.5) or produced no elements.
- `500 "Render couldn't start"` → venv missing → run:
  ```bash
  bash scripts/setup_circuit_venv.sh
  ```

---

## 6. 30-second checklist before you hit Render

- [ ] Circuit is a **closed loop** (bottom rail reaches the source negative
      terminal, e.g. `.to(V.start)`; or the return rail lands on a ground
      node tied to it).
- [ ] **Bare statements only** — no `with schemdraw.Drawing()`.
- [ ] Using aliases from §2.1 (`elm.*`, `V`, `R`, `WIRE`, `G`, `LED`…).
- [ ] Labels say what you want to see, with `loc=` when needed.
- [ ] No stray element after the loop that dangles.

That's the whole language. Keep it a closed loop, keep it bare statements,
keep it consistent — and `/circuit` will draw exactly what you typed.
