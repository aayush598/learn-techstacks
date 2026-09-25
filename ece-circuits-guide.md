# ECE Circuit Studio — authoring guide (md_book)

How to author schemdraw circuit snippets for the **ECE Circuit Studio**
(`/circuit` page, `/api/circuit` endpoint, Next.js app `md_book`).

Verified end-to-end against schemdraw 0.23 in md_book's isolated venv.
All coordinates below come from real renders of the exact pipeline the site
uses (`scripts/render_circuit.py` + the out-of-tree venv).

---

## 1. Gotchas that burn people first

These are the ones that each produced a real bug. Read them before anything.

1. **A circuit must be a CLOSED LOOP.** schemdraw draws elements one after
   another; it does **not** auto-connect the last element back to the first.
   If your bottom rail never returns into the source's **negative terminal**
   (its `start` anchor), the snippet renders a floating island — electrically
   an open circuit, even though it *looks* intentional.

   Symptom you'll see: the negative terminal of `V` sits at some `(x,y)` with
   nothing attached, and a `Ground`/wire dangles elsewhere. The SVG is real,
   the network is open.

   **Fix:** end the bottom rail with a wire that returns **up** into the
   source's negative terminal:
   ```python
   elm.Line().up().to(V.start)   # close the loop into V's negative terminal
   ```

2. **Snippets must be BARE element statements** — no `with schemdraw.Drawing() ...`:
   ```python
   # WRONG — creates a second, never-emitted drawing -> viewBox="inf inf"
   with schemdraw.Drawing() as d:
       d += elm.Resistor().right()

   # RIGHT — bare statements; the renderer already opens `with Drawing()`
   elm.Resistor().right().label('R1 10k', loc='bottom')
   ```
   A snippet that opens its own drawing shadows the renderer's, elements attach
   to a drawing that is never rendered, and you get an empty `viewBox="inf inf"`.

3. **The schemdraw venv must live OUTSIDE the Next.js project tree.**
   If the venv (`.circuit-venv`) is inside the project, Turbopack's build-time
   module walker crawls it computing "Compiling /circuit SSR pre-render", follows
   `bin/python` (a symlink **out of the filesystem root**), and deadlocks the
   build. The deadlock is Turbopack + the symlink, **not** the React code and
   **not** the Python renderer.

   Location used by md_book (see `scripts/setup_circuit_venv.sh`):
   ```
   ${HOME}/.cache/md_book/.circuit-venv
   ```
   Bootstrap a fresh clone with:
   ```bash
   bash scripts/setup_circuit_venv.sh
   ```

4. **No OS handoff.** The studio renders the schematic **inline in the page**
   (inline `<svg>`); the API returns `{svg: string}` JSON. Nothing is written
   to disk and nothing launches external viewers. If gwenview / a file viewer
   opens when you visit `/circuit`, a **stale dev server from an older build**
   is still serving the old "Download SVG" bundle (`kill` the old `next dev`/
   `next-server` PIDs), or your running server is a pre-fix build (re-run
   `npm run build`).

---

## 2. The panel setup (how md_book wires this up)

- `app/circuit/page.tsx` — the page (`○ /circuit`, static prerender; just renders
  `<CircuitStudio />`; no Python at build time).
- `app/api/circuit/route.ts` — `POST`, dynamic (`ƒ /api/circuit`); spawns the
  venv python + `scripts/render_circuit.py`, feeds the snippet on stdin, returns
  `{svg}` / `{error}`.
- `scripts/render_circuit.py` — reads snippet from stdin, runs it inside
  `with schemdraw.Drawing() as d:`, prints SVG to stdout.
- `scripts/setup_circuit_venv.sh` — creates the out-of-tree venv, installs
  schemdraw, verifies.
- `components/circuit-studio.tsx` — client editor: code textarea, EXAMPLES
  presets, **Copy SVG** button (clipboard only — no download button).
- `components/markdown-viewer.tsx` — must contain **zero** circuit/label code;
  circuits live only on `/circuit`, never in markdown.

Build/route table (verified, `next build` exit 0, `/circuit` static):
```
○ /circuit        static  (client shell; schemdraw never runs at build time)
ƒ /api/circuit    dynamic (spawns venv python only on POST)
```

---

## 3. Authoring language

Each snippet is a sequence of bare `schemdraw.elements` statements, run inside
one open drawing. Use these convenience aliases:

| Alias | Element | Example |
|-------|---------|---------|
| `elm.SourceV()` | voltage source | `elm.SourceV().up().label('V_in 10V')` |
| `elm.SourceI()` | current source | |
| `elm.Resistor()` | resistor | `elm.Resistor().right().label('R1 10k', loc='bottom')` |
| `elm.Capacitor()` | capacitor | |
| `elm.Inductor()` | inductor | |
| `elm.Diode()` / `elm.LED()` | diode / LED | |
| `elm.Line()` | wire | `elm.Line().right()` |
| `elm.Ground()` | ground | |
| `elm.Dot()` | junction dot | `elm.Dot().label('out', loc='right')` |

Key ideas:
- Elements chain: each starts where the previous one ended.
- `.up() .down() .right() .left()` set direction; `.label(text, loc=...)` adds
  labels.
- **Rails must return to the source's negative terminal** (see §1.1). 
  `SourceV().up()` puts the **negative** terminal at its `start` anchor (the
  bottom); `SourceV().down()` puts it at the top. Pick one and route the return
  rail to that exact anchor (use `.to(...)`).

---

## 4. Working examples

### 4.1 Closed voltage divider (corrrect loop)

```python
V = elm.SourceV().up().label('V_in 10V')
R1 = elm.Resistor().right().label('R1 10k', loc='bottom')
elm.Line().right()
R2 = elm.Resistor().down().label('R2 10k', loc='bottom')
elm.Line().down()
elm.Line().left()
elm.Line().up().to(V.start)   # ← returns the rail into V's negative terminal
elm.Ground()
```

Verified element trace (each start→end):
```
V         (0.0, 0.0)->(0.0, 3.0)   negative terminal at (0.0, 0.0)
R1        (0.0, 3.0)->(3.0, 3.0)
Line      (3.0, 3.0)->(6.0, 3.0)
R2        (6.0, 3.0)->(6.0, 0.0)
Line      (6.0, 0.0)->(6.0,-3.0)
Line      (6.0,-3.0)->(3.0,-3.0)
Line      (3.0,-3.0)->(3.0, 1.2)  .to(V.start) — climbs back to x≈3, then up
Ground    (3.0, 1.2)->(3.0, 1.2)
```
The loop node forms where the return rail meets the source's negative lease.

### 4.2 The SAME divider, but OPEN (the bug)

```python
V = elm.SourceV().up().label('V_in 10V')
R1 = elm.Resistor().right().label('R1 10k', loc='bottom')
elm.Line().right()
R2 = elm.Resistor().down().label('R2 10k', loc='bottom')
elm.Line().down()
elm.Line().left()          # rail returns left only to x=3.0
elm.Ground()               # dangles there — never reaches (0.0, 0.0)
```
Trace shows the difference: bottom rail ends at `(3.0,-3.0)`, Ground sits there,
and V's negative terminal `(0.0, 0.0)` is a floating island. **Open circuit.**
The only difference from §4.1 is the missing `elm.Line().up().to(V.start)`.

### 4.3 Diode / LED stack (also needs the return rail)

```python
V = elm.SourceV().up().label('V_in 5V')
elm.Resistor().right().label('R1 470', loc='bottom')
elm.LED().right().label('D1', loc='bottom')
elm.Line().right()
elm.Line().down()
elm.Line().left()
elm.Line().up().to(V.start)
elm.Ground()
```

### 4.4 Capacitive divider

```python
V = elm.SourceV().up().label('V_in 12V')
C1 = elm.Capacitor().right().label('C1 100n', loc='bottom')
elm.Line().right()
C2 = elm.Capacitor().down().label('C2 100n', loc='bottom')
elm.Line().down()
elm.Line().left()
elm.Line().up().to(V.start)
elm.Ground()
```

---

## 5. Rules of thumb (quick checklist)

- [ ] Every path is a **closed loop** (bottom rail `.to(V.start)`).
- [ ] Snippet uses **bare element statements** (no inner `with Drawing()`).
- [ ] Venv lives **outside** the project (`${HOME}/.cache/md_book/.circuit-venv`).
- [ ] No "Download" button anywhere — use **Copy SVG** (clipboard), so nothing
      leaves the website.
- [ ] `/circuit` stays a separate page; the markdown viewer has no circuit code.
- [ ] After editing, verify: `npx tsc --noEmit` (exit 0), `npm run build`
      (exit 0, `/circuit` static, `/api/circuit` dynamic).

---

## 6. What to do when it renders wrong

1. Check you're not on a **stale server** (open gwenview = old bundle):
   ```bash
   pgrep -af "next" | rg "dev|start"     # find strays
   kill -9 <PIDs>                          # kill only the old ones
   ```
2. **`viewBox="inf inf"`** → snippet opened its own drawing (gotcha §1.2).
3. **`500 render couldn't start`** → venv missing/relocated; run
   `bash scripts/setup_circuit_venv.sh`.
4. **Open circuit / floating ground** → missing return rail (gotcha §1.1).
5. Push Render, read the inline SVG in the page, confirm the source's negative
   terminal has an attached wire.

---
*Guide stored per request. Covers md_book's ECE Circuit Studio authoring —
preset form, closed-loop requirement, venv placement, and the gwenview/stale-
server source.*
