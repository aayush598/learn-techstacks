# AI Question Generator — Prompt & Format Spec

> Paste the block below into any LLM to generate a new **solutions sheet** for the
> md_book visualizer/analyse section (line-by-line Python tracer). The sheet is
> parsed mechanically — deviations silently drop or break questions.
>
> `@mn1 <repo path>` … just paste this whole file's instructions.

---

## SOURCES (base the questions on these folders)

- `Infosys-SP-DSE-Interview-Prep` — DSA / CS fundamentals / Python / AI–ML / system design / DevOps / aptitude
- `ISRO_CBT_ECE_Prep` — analog & digital circuits / EM & antennas / communication / DSP / control / power / measurements / engineering math / aptitude

---

## PROMPT — copy from here

```
You are generating a "solutions sheet" in plain Markdown for a Python
step-by-step visualizer (a line-level tracer). Write N=100 questions as one
continuous Markdown document, based on the topics below. The sheet is parsed
mechanically — any deviation silently breaks or drops a question.

## SOURCE SCOPE

### A) Infosys-SP-DSE-Interview-Prep  (~60 questions)
- DSA: arrays (two-pointer, sliding window, sorting/searching, matrix,
  hashing/maps), strings (pattern matching, anagrams, substrings), linked
  lists, stacks/queues (monotonic stack, heaps), trees (BST, traversals,
  construction), graphs (BFS/DFS, shortest path, MST/union-find, topological
  sort), dynamic programming (1D/2D, knapsack, string, interval, state-machine),
  recursion/backtracking (permutations, combinations, subsets, mazes), greedy
  (activity selection, Huffman), segment trees / Fenwick, tries, bit manipulation
- CS fundamentals: OOP, DBMS (normalization, transactions), SQL (joins, window
  functions), OS (processes, memory, deadlocks, scheduling, synchronization),
  networks (TCP/IP, HTTP, IP addressing, security)
- Python: decorators, generators, exception handling, asyncio basics, FastAPI/Flask
- AI/ML: ML fundamentals, neural networks, CNN/RNN, RAG/LLM, agentic AI
- System design: load balancing, caching, REST API design, design patterns
- DevOps: Git, Docker, CI/CD, Linux basics
- Aptitude: number system, percentages, profit/loss, time & work,
  permutation/combination, probability, series, puzzles, syllogisms

### B) ISRO_CBT_ECE_Prep  (~40 questions)
- Analog circuits (op-amp gain, feedback, oscillators, filters, regulators)
- Digital & HDL (number systems, Boolean algebra & K-maps, combinational,
  multiplexers, adders, sequential, counters, FSMs, VHDL/Verilog, ADC/DAC)
- EM/microwaves/antennas (Maxwell, transmission lines, Smith chart,
  waveguides, antennas, radar)
- Communication (AM/FM, sampling, PCM, digital modulation, information theory,
  Huffman coding)
- Signals & DSP (Fourier, Laplace, Z-transform, filter design, FFT)
- Network theory (KCL/KVL, nodal/mesh, Thevenin/Norton, transients, resonance,
  two-port, coupled circuits)
- Electronic devices (PN junction, BJT, FET/MOSFET, small-signal models)
- Control systems (transfer functions, Routh-Hurwitz, root locus, Bode/Nyquist, PID)
- Engineering math (linear algebra, calculus, DEs, probability/statistics,
  numerical methods)
- Power electronics (rectifiers, SCR, inverters, choppers, PWM)
- Measurements & transducers (bridges, LVDT, strain gauges, CRO)
- Aptitude (visual/spatial reasoning, syllogisms, quantitative)

## RULE FOR THEORY-FIRST TOPICS (folder B + CS-funda + aptitude)
Most of folder B has prose only. Do NOT write prose questions. For each such
topic, write a small Python program that COMPUTES/VERIFIES the core concept and
prints a numeric/short example, e.g.:
- op-amp non-inverting gain = 1 + Rf/R1; RC low-pass cutoff = 1/(2*pi*R*C);
  LC oscillator frequency
- Thevenin/Norton: compute Vth and Rth of a resistive divider from component
  values; a tiny nodal/mesh solver for 2-3 loops
- transmission line: reflection coefficient, SWR, dB conversion
- Shannon capacity C = B*log2(1+S/N); Nyquist rate = 2B; Huffman coding (
  build the tree, print the code table — animates beautifully)
- naive DFT / FFT, moving-average filter, IIR step response
- control: Routh-Hurwitz tabular string count, closed-loop poles (cmath),
  error constants
- probability/statistics: expected value of a die, Bayes numerator, Poisson PMF,
  nCr
- aptitude: solve a logic puzzle (train meeting time, work-rate, age problem,
  series next term) in Python and print the answer
The traced function may take plain ints/lists/strings. Small inputs only.

## MARKDOWN STRUCTURE (strict)
1. Start each question with  `## N. Title`  (N running; optionally append
   Easy/Medium/Hard).
2. Below the heading: a concise statement in Markdown (<= ~2000 chars; UI
   truncates at 2400). For folder B topics, include the formula in one line.
3. Exactly ONE Python block per question, fenced exactly  ```python ... ``` .
4. One question per `##` heading; never two code blocks under one heading.

## PYTHON CODE REQUIREMENTS (critical)
- Define a `def` solution function (any name); helpers/classes are fine.
- End with a TOP-LEVEL  `print(solution_fn(arg1, arg2, ...))`  at module level —
  NOT inside `if __name__ == "__main__":`. This top-level print is how the
  tracer finds the function to animate and its default inputs.
- Standard library ONLY (browser runtime = Pyodide). `math`, `cmath`,
  `collections`, `heapq`, `bisect`, `functools`, `itertools`, `re`, `random`
  are fine. numpy/pandas/scipy/torch are FORBIDDEN. No network/file use.
- Code < 12,000 chars; no markdown fences or `~~~` inside code.
- Small inputs — the tracer records EVERY executed line (20,000 steps / 25 s
  limits). Keep lists/arrays < ~20 elements; keep recursion shallow.
- Write EXPLICIT, readable code (plain for/while loops, meaningful names,
  intermediate variables) — the visualizer animates line-by-line.
- Give the function a 1-sentence docstring (it becomes the animation headline).
- Print arguments must be Python literals so the UI's custom-input feature can
  reuse them.
- Code must run cleanly top-to-bottom (function, then print) — no uncaught
  errors.

## VERIFY each block mentally
-  ```python  open  ->  ```  close?
- contains  def ...( ?
- last executable line is an indentation-0  print(yourfn(...))?
- would it run and terminate fast in CPython?

## OUTPUT FORMAT
Output ONLY the raw Markdown sheet — no preamble, no explanations, no outer code
fence, no closing "verification" section. Number sequentially. Vary difficulty,
keep all questions distinct, cover every topic bucket above at least once.
```

---

## Why these rules exist (for your own review)

| Rule | Where it lives | Why |
|---|---|---|
| `## N. Title` heading | `solutions-index.ts` | A `#`/`##` line splits a new question; number (`N.`/`N)`) becomes the id; difficulty words are stripped |
| One fenced `python` block | `solutions-index.ts` | Only Python-tagged (or `looksLikePython`) fenced code is kept as the runnable `source` |
| Top-level `print(fn(...))` | `viz_tracer.py` | The tracer finds the animated function and default inputs from a top-level `print(...)`; an `if __name__ == "__main__"` guard is NOT found |
| Stdlib only | Pyodide 0.26.4 | numpy etc. are not installed in the browser runtime |
| `< 12_000` chars, has `def` + `print`/`dp` | `pyodide.ts` `looksLikePython` | Client-side acceptance gate |
| Small inputs / < 20k steps | `viz_tracer.py` | Per-line tracing hits step/time limits fast |