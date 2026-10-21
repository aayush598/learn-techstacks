# Infosys SP DSE — 100 OpenRTL Interview Q&A

> Based on the OpenRTL project by Aayush Gid — a 36-phase FPGA/IC product workflow with a fully open-source EDA toolchain, one-click flow driver, automated reporting, and agent-based lifecycle automation. All answers are grounded in the actual repo (`~/aayush/projects/personal/earning/openrtl`, `packages/openrtl/` + `.opencode/`).
> Candidate: Aayush Gid — B.Tech E&C | Agentic AI / AI Agent / Data Science Internships | MigratorGen, ScriptVector, OpenRTL.ai, Agno Open-Source PRs | IEEE Publication (2024)
> Scope: OpenRTL deep-dive only — vision, 36-phase workflow, subagents, EDA toolchain (Yosys/nextpnr/Verilator/SymbiYosys/cocotb), flow driver, report engine, scaffolding, testing, CI/CD, engineering decisions. DSA, SQL/tech-stack, and HR questions are in separate sheets.
> Interview pattern observed: panel deep-dives the most ambitious technical project on the resume — architecture, why each tool was chosen, what breaks, and how you'd take it to production.

---

## 1. Project Overview & Vision (Q1–Q15)

**Q1: What is OpenRTL?**
A: OpenRTL is my evolution of the OpenRTL.ai Verilog-generation tool into a full 36-phase FPGA/IC product workflow. It combines (1) an agent platform built on opencode — a primary "OpenRTL" agent plus ~35 domain engineer subagents (RTL, verification, synthesis, P&R, timing, power, clock, reset, formal, thermal, security, compliance, manufacturing, etc.) that drive a project from a one-line product description to manufacturing; (2) a fully open-source EDA toolchain (Yosys, nextpnr, icestorm, Icarus Verilog, Verilator, SymbiYosys, cocotb) that is cross-platform and installable via conda/pip/source; (3) a one-click flow driver `flow.sh`; (4) a dependency-free report engine that parses real tool output into Markdown + SVG infographics + a handoff zip; and (5) an automated test suite + CI. Everything is defined in `packages/openrtl/` and driven by `.opencode/` agents, commands, and skills.

**Q2: How did OpenRTL evolve from your earlier OpenRTL.ai project?**
A: The earlier OpenRTL.ai was a Streamlit app where you described a module in natural language, Gemini generated Verilog, Verilator linted it, Yosys synthesized it, and RTL metrics + netlistsvg rendered. It proved the "LLM + open-source EDA" idea but only covered the RTL-writing slice. OpenRTL generalizes that: instead of lint→synthesize→report, it covers every phase of a hardware product — market/requirements/architecture through compliance/release/field support — and moves the LLM from a single call into an orchestrated agent team, while keeping the deterministic open-source toolchain as the source of truth for correctness.

**Q3: Why build this on opencode instead of writing a bespoke coordinator?**
A: opencode already provides the hard parts of an agent platform: durable sessions, permission gates, tool execution, MCP, multi-agent orchestration, and a file-first context model. I create a repository `.opencode/agent` (markdown `mode: primary` / subagent definitions with model, color, description) and `.opencode/skills` (instructions loaded on demand), plus `.opencode/command` slash-commands for the workflow. Reusing the platform meant I could spend my effort on hardware-domain logic — the toolchain, flow, report engine, gates — rather than rebuilding an agent runtime. My commits are exactly that: "feat: add OpenRTL agents and skills" and "feat(toolchain): Add OpenRTL toolchain with conda environment and provisioning scripts".

**Q4: What's the single-source-of-truth design, and why does it matter here?**
A: The lifecycle is defined once in `scaffold/scaffold.ts` as a `PHASES` array (36 phases with id, title, group, deps, gate, ctx) and mirrored in `docs/workflow/workflow.json`, while `toolchain/manifest.yaml` is the machine-readable inventory of every EDA tool keyed to the phase that consumes it — and provision.sh (install), doctor.sh (verify), flow.sh (drive) and the report engine (versions in headers) all read the same manifest. One definition drives install, verification, execution and reporting, so the tool → phase mapping can't drift.

**Q5: What are the 36 phases, grouped how?**
A: Numbered 00–35 and grouped into six lifecycle groups. Define: 00 Project, 01 Ideation, 02 Market, 03 Requirements, 04 Feasibility, 05 System Architecture, 06 Interface Definition, 07 FPGA Selection, 08 Component Selection, 09 Hardware Architecture, 10 PCB Architecture, 11 Power, 12 Clock, 13 Reset, 14 Security, 15 Thermal, 16 Software, 17 Firmware, 18 RTL Architecture, 19 Verification Plan. Implement: 20 Implementation, 21 Testbench, 24 Synthesis, 27 Optimization. Verify: 22 Simulation, 23 Formal, 25 P&R, 26 Timing Closure, 28 Debug, 29 System Validation. Produce: 30 Manufacturing, 31 Production Testing, 32 Compliance. Sustain: 33 Documentation, 34 Release, 35 Field Support. Every phase has dependencies, a review gate, and context files.

**Q6: How do quality gates work?**
A: Each phase declares a gate type — `architecture` (define/design), `implementation` (RTL/netlist work), `timing` (verify), or `ops` (produce/sustain). The primary agent's operating principle is "never skip a phase or advance past an open gate; resolve or waive blocking findings first." The `/openrtl-gate` command evaluates gate status and the workflow engine (`flow.sh`/`/openrtl-workflow advance`) refuses to move to the next runnable phase until dependencies are satisfied, the gate passes, and reviews are done. This is the IC equivalent of "definition of done."

**Q7: What does the primary agent actually do?**
A: `openrtl.md` is a `mode: primary` agent with `color: "#22d3ee"` and `model: nvidia/deepseek-r1`. It orchestrates the whole lifecycle: loads skills (`openrtl-init`, `openrtl-workflow`), stores the product description to `docs/00-project/project-description.md`, then for each phase loads the phase skill + task manager, executes tasks, records decisions in `docs/`, runs reviews, closes the gate, and stops at user approval gates (ideation, requirements, architecture) to present files before continuing. It delegates technical work to the right `openrtl-*` subagent.

**Q8: Why a team of ~35 specialized engineer subagents instead of one general agent?**
A: Hardware is deeply specialized — the correctness criteria for a power-domain design, a clock/reset scheme, formal properties, and a compliance checklist are unrelated. A dedicated subagent per role (rtl-engineer, verification-engineer, synthesis-engineer, pnr-engineer, timing-engineer, power-engineer, clock-engineer, reset-engineer, formal-engineer, thermal-engineer, security-engineer, manufacturing-engineer, compliance-engineer, firmware-engineer, embedded-engineer, field-support-engineer, release-manager, requirements-engineer, market-analyst, system-architect, and more) gives each one a narrow, expert system prompt and lets the orchestrator compose them like a real cross-functional IC team. It also mirrors how enterprise design flow is actually staffed.

**Q9: What's the file-first context principle, and why is it core?**
A: Every phase writes to files under `docs/` — status.md, gates.md, `ctx/*.md`, decisions. Decisions must never live only in the conversation. This matters for two reasons: (1) the opencode session can be resumed (`/openrtl resume`) and the agent rebuilds full context from disk, and (2) it's auditable — a reviewer can diff what the agent "decided." It turns ephemeral chat into a durable design record, which is how you ship hardware (everything in docs, traceable).

**Q10: Where do deterministic tools sit vs the LLM?**
A: The LLM (agents) plans, writes RTL, and fills context files; the deterministic open-source EDA tools are ground truth for correctness — Verilator for lint, Yosys for synthesis/formal, nextpnr for P&R, icetime/nextpnr STA for timing, cocotb/iverilog for simulation, pytest for regression. `flow.sh` is the forcing function: the agent runs tools through it, artifacts land where the workflow and report engine expect, and reports are parsed from real output (never hallucinated numbers). This hybrid — LLM for authorship, tools for verification — is the same philosophy I used in MigratorGen.

**Q11: What are the key artifacts of a completed OpenRTL project?**
A: Under `docs/<phase>/`: publishable Markdown reports per section (synth, pnr, timing, power, coverage, formal, sim, quality), dependency-free SVG infographics, and under `docs/34-release/handoff/` a zip of netlist + bitstream + reports. Build artifacts under `build/`: lint.log, sim.log, formal logs, `<top>_netlist.v`, `<top>_synth.json`, `<top>_synth.stat`, `<top>.asc`, `<top>.bin` bitstream, timing.rpt, coverage.dat. Plus `openrtl-project.json` metadata and `docs/workflow/workflow.json` state. The manifest lists every artifact's canonical path.

**Q12: What does `openrtl-project.json` contain and how is it used?**
A: It's the project marker that identifies a folder as an OpenRTL project and carries metadata: `top` module, `device` (e.g. `ice40up5k-sg48`), arch, description, lifecycle state. `flow.sh` walks up from the current directory until it finds this file to auto-resolve the project root; the report engine reads `top`/`device` from it (resolve_t op/resolve_device logic); the scaffold writes it for every generated project. It's the anchor that makes all tools context-aware.

**Q13: Which FPGA architectures are supported?**
A: `flow.sh --arch` accepts `ice40` (iCE40 via `synth_ice40`/`nextpnr-ice40`/`icepack`), `ecp5` (via `synth_ecp5`/`nextpnr-ecp5` with device like `25k`), `nexus` (via `synth_nexus`/`nextpnr-nexus`), and `generic` (plain `synth`). The report engine holds device budgets (LUT/FF/BRAM/DSP/PLL/IO) per arch and device — e.g. ice40up5k, ice40hx8k, ecp5 lfe5u-25f/45f/85f, nexus lfcp5-85f. Default is ice40.

**Q14: What languages/targets are supported?**
A: Verilog and SystemVerilog are fully supported (packages read before modules automatically). VHDL is opt-in via the Yosys GHDL plugin, and Chisel is explicitly out of scope for now (would require a FIRRTL front-end). The manifest declares this explicitly so expectations are set in the machine-readable source of truth.

**Q15: What's the distribution story — how does someone consume OpenRTL?**
A: `packages/openrtl/` is itself a workspace package (`openrtl-toolchain`, renamed to avoid a turbo name conflict) exposing npm scripts for every flow command (`doctor`, `provision`, `lint`, `sim`, `synth`, `pnr`, `reports`, `handoff`, `all`, `scaffold`, `test`, `ci`). A project can `cd` and `make all` via the scaffolded Makefile wired to `flow.sh`. Agents get the `openrtl-toolchain` skill that documents every command, artifact, and rule. So there are three surfaces: package scripts, generated Makefile, and the agent skill — all pointing at the same flow driver.

---

## 2. 36-Phase Workflow & Agents (Q16–Q30)

**Q16: Walk me through the define group (phases 00–04).**
A: 00 Project captures the product description (`project-description.md`); 01 Ideation explores the idea and alignment; 02 Market does market analysis and positioning (market-analyst agent); 03 Requirements writes the formal requirements doc; 04 Feasibility studies feasibility and records decisions. Each depends on the previous (03 depends on 01+02, 04 depends on 02+03), all gated on `architecture`. This is deliberately front-loaded so the design group has solid requirements to build against.

**Q17: How do the design phases connect to RTL?**
A: Design spans 05 System Architecture → 06 Interface Definition → 07 FPGA Selection → 08 Component Selection → 09 Hardware Architecture → 10 PCB → 11 Power → 12 Clock → 13 Reset → 14 Security → 15 Thermal → 16 Software → 17 Firmware → 18 RTL Architecture → 19 Verification Plan. Notably 12 Clock and 13 Reset are first-class architecture phases (clock-engineer, reset-engineer agents) because they're where most timing and boot failures come from; 18 RTL Architecture has a `decisions` context file (e.g. DECISION-070 for FPGA arch choices); 19 Verification Plan drives everything in the verify group.

**Q18: How does the implement group's dependency structure work?**
A: 20 Implementation depends on 18 only (gate: implementation). 21 Testbench depends on 19 + 20. 24 Synthesis depends on 20 (you can't synthesize before RTL exists) — build artifacts like the netlist flow out of it. 27 Optimization depends on 20 + 24 and uses pyverilog for RTL analysis. The DAG in the scaffold mirrors the real design flow: no synthesis before implementation, no P&R before synthesis.

**Q19: Describe the verify group and its unique constraint — "gate: timing".**
A: 22 Simulation (cocotb/iverilog + pytest), 23 Formal (SymbiYosys/SMT), 25 Place & Route, 26 Timing Closure, 28 Debug, 29 System Validation. Except 22/23/28 (mixed), the gate for P&R and timing is literally `timing`. 29 System Validation depends on 26 Timing Closure + 28 Debug + 23 Formal — i.e., you can't claim system-level validation until timing closed AND formal passed AND bugs closed. That dependency chain is the "don't claim integration complete on a design that fails timing" rule.

**Q20: What happens in produce and sustain?**
A: Produce: 30 Manufacturing (BOM, assembly, foundry), 31 Production Testing (test plan, fixtures), 32 Compliance/Certification. Sustain: 33 Documentation (user + API docs, release notes), 34 Release (handoff zip), 35 Field Support (support, obsolescence). These mirror mechanical/electrical product development — most AI agents would stop at "RTL works," OpenRTL goes to what it takes to actually ship hardware. Compliance depends on 29 + 30; Release depends on 29 + 33.

**Q21: What are openrtl commands and give me examples?**
A: `.opencode/command/*.md` defines slash-commands: `/openrtl` (start/resume), `/openrtl-workflow` (status/advance/resume/rollback using workflow.json), `/openrtl-gate` (evaluate gate status), `/openrtl-review` (run review), `/openrtl-scaffold`, `/openrtl-flow` (drive flow.sh), `/openrtl-phase`, `/openrtl-project`, `/openrtl-release`, `/openrtl-tasks`, `/openrtl-vis`, `/openrtl-analytics`, `/openrtl-approve`, `/openrtl-decision`. E.g. `/openrtl-workflow rollback <phase>` re-opens a closed phase for rework — the state machine version of "go back to the drawing board."

**Q22: What skills does the agent load, and how are they organized?**
A: Skills are numbered per phase (`openrtl-00-project` … `openrtl-24-synthesis`, `openrtl-market`, `openrtl-ideation`, `openrtl-visualization`) plus cross-cutting `openrtl-toolchain` and `openrtl-flow`. Each is a `SKILL.md` with a description (so opencode auto-loads it when relevant) and the step-by-step for that phase — e.g. the `openrtl-toolchain` skill documents every `flow.sh` command, its tool, and its artifacts, plus the rule "prefer the flow driver — run `flow.sh <cmd>` rather than invoking tools by hand, so artifacts land where the workflow and report engine expect them."

**Q23: Why is the toolchain skill so prescriptive about running tools via flow.sh?**
A: Because the report engine parses artifacts at canonical paths (`build/synth/<top>_netlist.v`, `docs/<phase>/reports/<section>.md`). If an agent or user runs yosys manually, output lands somewhere arbitrary and the pipeline degenerates to drifting, unreliable reports. The skill encodes the invariant: flow.sh owns artifact placement; doctor after provisioning; run `flow.sh test` after any tool/parser change and leave it green; record tool versions in the phase toolchain context.

**Q24: How are decisions recorded and how does the workflow stay resumable?**
A: Decisions go to `docs/00-project/decisions/` (e.g. `DECISION-070-fpga-arch.md`), and both `flow.sh` and the report engine read this file to resolve arch/top. `docs/workflow/workflow.json` stores current phase, deps, gate, blockers. `/openrtl-workflow status` reports phase/deps/gate/blockers, `advance` moves only when satisfied, `resume` continues the current phase, `rollback` re-opens for rework. This gives the whole thing a checkpoint-restart model — kill the session, come back, agent rebuilds state from disk.

**Q25: Which subagents are closest to "RTL correctness", and how do they split work?**
A: rtl-engineer writes synthesizable modules; verification-engineer plans and writes cocotb tests; formal-engineer writes `.sby` properties; simulation-engineer runs regression; synthesis-engineer owns the netlist/resource/inference quality; pnr-engineer owns placement/routing/congestion/bitstream; timing-engineer owns slack/WNS/TNS/fmax; power-engineer owns static+toggle power; debug-engineer owns root-cause analysis. The orchestrator calls the right one per phase, and reviewer/validator/risk agents sit across all phases as quality functions.

**Q26: How do the reviewer/validator/risk agents fit the process?**
A: `openrtl-reviewer` reviews phase deliverables, `openrtl-validator` validates claims against tool output, and `openrtl-risk` scores risk. The workflow only advances a gate when reviews are done (`/openrtl-gate` checks review completion). This is the agent-platform equivalent of design reviews and sign-offs — an independent check so the writing agent can't self-approve its own work.

**Q27: What's the purpose of the researcher and market-analyst agents in a *hardware* project?**
A: 02 Market generates market analysis and positioning before requirements are frozen; the researcher keeps up with chip/EDA landscape to inform FPGA selection (07). For a product to actually ship, the right FPGA and the right requirements must be chosen before a single line of RTL is written — these agents operationalize "start from the market, not from the code." It's what separates a hardware startup flow from a coding exercise.

**Q28: How did you choose the primary agent's model?**
A: `openrtl.md` sets `model: nvidia/deepseek-r1` — chosen for long-context reasoning (the workflow demands holding a 36-phase plan) and strong agentic/tool-use behavior at efficient cost. Individual subagents can override models too, so expensive reasoning can be reserved for tools like formal or timing analysis. This is a lesson I carry: pick the model per workload, not one model for everything.

**Q29: How does the workflow avoid "AI spaghetti" on a 36-phase project?**
A: Three mechanisms: (1) numbered phases with explicit deps — the scaffold generates the full DAG, so nothing runs before its inputs; (2) gates — advance requires gate pass + reviews; (3) file-first — every phase writes to its own `docs/<NN>-<phase>/` namespace with status/gates/ctx. The state machine (`workflow.json`) is process-global, durable, and resumable. There's no free-form loop, which is exactly what you don't want when each phase's output feeds the next design decision.

**Q30: What failed or is still hardest, and how would you fix it?**
A: (1) Keeping 36 phases genuinely enforced — a single agent will happily skip "boring" phases; I made gates hard dependencies and added reviewer/validator agents. (2) Tool availability — not every machine has nextpnr; `flow.sh all` degrades gracefully by skipping missing-tool steps and still producing reports. (3) Long sessions/context — mitigated with file-first + resume. (4) Next step: a progress dashboard and a CI job that re-runs `flow.sh test` per PR to the workflow so agents can't regress the tooling.

---

## 3. Toolchain & Installation (Q31–Q45)

**Q31: What tools are in the open-source EDA toolchain?**
A: Yosys (synthesis + formal SAT/BMC engine), nextpnr (place & route + open STA, per-arch binaries), icestorm (icepack/iceunpack/icebox / icetime for bitstream + timing), Icarus Verilog (simulation + VCD), Verilator (lint, 2-state sim, statement/toggle coverage), cocotb (coroutine-based testbench), pytest (regression runner), SymbiYosys + yosys-smtbmc (formal property checking, SMT-based BMC), pyverilog (optional RTL analysis), Python 3.9+, z3-solver, PyYAML. All Apache-2.0/MIT/BSD or conda/pip.

**Q37: What does the toolchain manifest encode?**
A: `manifest.yaml` declares the tool name, command, package, source (conda/pip), minimum version, the check command (e.g. `yosys --version`), which flows it serves, which phases consume it, and a note. It's the single source of truth read by provision.sh (install), doctor.sh (verify), flow.sh (drivers, e.g. `NEEDS` map), and the report engine (versions in headers). If we add a tool, we add one manifest entry and everything else follows.

**Q33: How does provision.sh install tools?**
A: Modes: `--conda` (conda-forge env `openrtl` from `conda-env.yml` — yosys, iverilog, verilator, python, pip), `--pip` (Python-side: cocotb, pytest, pyverilog, PyYAML, z3), `--source` (builds icestorm, nextpnr-ice40, iverilog and SymbiYosys from source into `~/.local/openrtl`, since conda-forge doesn't ship them), and `--check` (report only). Default `auto` detects conda/apt/brew/pip and does the full install. It's one command for Linux/macOS/Windows-WSL2, no root needed.

**Q34: Why do icestorm/nextpnr/SymbiYosys need a source build?**
A: conda-forge ships Yosys, Icarus Verilog and Verilator, but the FPGA place-and-route stack (icestorm, nextpnr-ice40) and SymbiYosys aren't packaged there. `provision.sh --source` builds them from source into `~/.local/openrtl`. The README is explicit: the recommended full install is conda (+pip) followed by `--source`, or `--source` alone if yosys/verilator already exist via the OS package manager.

**Q35: How does provision.sh handle modern Python/pip quirks?**
A: `pip_user()` adds `--user`, auto-adds `--break-system-packages` when it detects PEP 668 (`EXTERNALLY-MANAGED` marker in the stdlib path) so `--pip`/`--source` work on externally-managed distros without a venv, and sets `COCOTB_IGNORE_PYTHON_REQUIRES=1` so cocotb can build its sdist on Python versions (e.g. 3.14) that its setup.py guards against, falling back to a wheel when available. These are the real-world install-landmines the agent would otherwise hit months later.

**Q36: How does doctor.sh verify the toolchain?**
A: `doctor.sh` checks each tool's presence + version and prints `PASS`/`FAIL`/`SKIP`: required tools (yosys, nextpnr-ice40, iverilog, verilator, icepack, icetime, python3) FAIL when missing; optional tools (sby, pytest, zip, cocotb) SKIP. It ends with `toolchain summary: PASS=N FAIL=N SKIP=N` and a non-zero exit code if any required tool is missing — so it's usable directly as a CI gate. `flow.sh doctor` delegates to it.

**Q37: What's in `conda-env.yml`?**
A: Named env `openrtl` from conda-forge: `python>=3.9`, `pip`, `yosys>=0.33`, `iverilog>=11`, `verilator>=5.0`, plus a pip block (cocotb>=1.8, pytest, pyverilog, PyYAML, z3-solver). Comments document OS quirks (Linux: works out of the box; macOS: same env; Windows: use WSL2 for nextpnr/iverilog interop). Version floors are chosen because older yosys/verilator mis-handle current SystemVerilog.

**Q38: Why are version floors pinned at all?**
A: yosys>=0.33 and verilator>=5.0 represent real capability thresholds — newer SystemVerilog constructs (packages, interfaces, `always_comb`) and formal features only round-trip correctly on recent releases. Unext pinned tools make the flow silently wrong: lint passes on old Verilator but the code doesn't synthesize on current Yosys. The manifest records `version_ge` per tool and doctor catches violations.

**Q39: How is the environment cross-platform without root?**
A: conda/micromamba/miniforge install to user space; source builds go to `~/.local/openrtl`; pip installs `--user`. Linux: nothing extra; macOS: conda ships binaries; Windows: WSL2 is documented as the supported route for nextpnr/iverilog interoperability. No sudo, no global package manager tinkering — reproducibility without admin rights.

**Q40: What does the doctor exit code mean for automation?**
A: `[[ $FAIL -eq 0 ]]` is the final line of doctor.sh — exit 0 iff no required tool is missing. In CI (`cicd/ci.sh`) and `flow.sh all` this is what decides whether to proceed. It's a health gate, not an opinion: optional-but-absent tools (SymbiYosys, cocotb) are SKIP not FAIL, so a laptop without formal tools still gets a green doctor plus a report telling you exactly what would be skipped.

**Q41: How does the flow handle a machine with only some tools?**
A: `flow.sh all` has a `NEEDS` table — formal needs `sby`, sim needs `iverilog`, pnr needs `nextpnr-$ARCH`, timing needs `nextpnr-$ARCH`. Before each step it checks the required tool; missing → `skip <step> (missing: <tool>)` and continues. Any step that runs and fails sets rc=1 but the pipeline keeps going, so the run still produces whatever reports are possible and the exit code tells CI whether to fail.

**Q42: What's the thinking behind open-source-only as the default?**
A: Cost, reproducibility, licensing, and auditability: the whole flow is free, version-stable, and inspectable — you can read the tool source to debug. Vendor tools (Vivado, Quartus, Libero) remain available as optional adapters gated behind `OPENRTL_VENDOR_TOOLS=1` so teams on real vendor flows aren't locked out, but the default posture is open-source. This maps beautifully to enterprise philosophy where license management and reproducibility are governance concerns.

**Q43: Why cocotb + iverilog as the default simulation stack?**
A: cocotb lets testbenches be written in Python (coroutines with `async def` / `await` — I already use pytest and Python everywhere) instead of pure HDL, and iverilog provides the free Verilog simulator that emits VCD for analysis. Verilator covers the fast 2-state simulation + coverage lane. Together: Python-native verification, free, cross-platform, and the exact artifacts (sim.log, .vcd, coverage.dat) the report engine parses.

**Q44: How does the flow keep deterministic across machines?**
A: The doctor checks versions and the manifest sets floors; the scaffold records arch/top/device in `openrtl-project.json`; `flow.sh` pins seeds (`--seed 1` for nextpnr-ice40) so P&R is reproducible; artifacts always land at canonical paths. If a tool version drifts, doctor flags it — a gate, not a hope.

**Q45: What did you choose NOT to include, and why?**
A: VHDL by default (needs the ghdl plugin — documented as opt-in), Chisel (FIRRTL out of scope), paid EDA (vendor adapters optional), a cloud IDE (flow is CLI-first so it runs anywhere, including CI). Cutting scope on the tool side kept the install, tests, and docs honest — every claim in the README is something the automated test suite actually exercises.

---

## 4. Flow Driver & EDA Automation (Q46–Q60)

**Q46: What exactly does `flow.sh <command>` run?**
A: It's the unified driver with commands: `doctor`, `lint`, `sim`, `formal`, `synth`, `pnr`, `timing`, `power`, `coverage`, `verify`, `reports`, `handoff`, `test`, and `all`. Options: `--top`, `--arch` (ice40|ecp5|nexus|generic), `--project`, `--threads`, plus test flags (`--only`, `--verbose`, `--tap`, `--list`). The head of the file doubles as its own `--help` (prints lines 2–38). It exports `OPENRTL_TOP/ARCH/PROJECT` so downstream tools read the same context.

**Q47: How does flow.sh resolve the project, top module, and arch automatically?**
A: It walks up from CWD to the nearest `openrtl-project.json`; reads `top` from the JSON (fallback). If `--top` isn't given, `detect_top()` cascades: (1) grep `DECISION-070-fpga-arch.md` for a `"name"`/`"top"`/`module` token; (2) grep the Makefile for `--top-module` or `TOPLEVEL`; (3) take the first `module` declaration in `rtl/*.sv`/`rtl/*.v` (skipping `*_pkg`/`*.svh`). Arch falls back to grep of the DECISION file, default ice40. So `flow.sh synth` works in any project directory with zero flags.

**Q58: How does `cmd_lint` build the source list correctly?**
A: It collects `*_pkg.sv`, `*_pkg.v`, `*.svh` first (SystemVerilog packages must be read before the modules that import them) then module files, excluding packages/svh from the module list. Runs `verilator --lint-only --sv -Wall -Wno-DECLFILENAME --top-module <top>` into `build/lint/lint.log`; on pass it appends `LINT PASS`; on any issue it exits 1 with a pointer to the log — lint is a hard gate in this flow.

**Q49: How does simulation handle project-specific testbenches?**
A: `cmd_sim` prefers the project's own `Makefile` if it has a `sim`/`test`/`run` target (`make sim`, tee'd to `build/sim/sim.log` and returning the real exit via `PIPESTATUS`), else falls back to `pytest tb/ -q` when a `tb/` directory exists, else warns. This respects cocotb's `make`-driven model while still normalizing output location.

**Q50: How does formal verification run?**
A: If `sby` exists and `formal/*.sby` files exist, it loops `sby -f` per file into `build/formal/<file>.log` and greps the `SUMMARY|PASS|FAIL` lines. If sby is absent but yosys exists, it falls back to a basic `yosys` SAT check (`read_verilog -sv ...; hierarchy -top <top>; sat`). If neither exists, it warns. So formal is best-effort with three tiers — full SymbiYosys BMC, basic SAT, or explicit skip.

**Q51: Walk me through the Yosys synthesis script it emits.**
A: `cmd_synth` writes a `.ys` script: `read_verilog -sv <packages+modules>` (packages first), `hierarchy -check -top <top>`, `proc; flatten`, then the arch-specific pass (`synth_ice40`/`synth_ecp5`/`synth_nexus`/generic `synth`), then `tee -o build/synth/<top>_synth.stat stat -top <top>`, `write_verilog <top>_netlist.v`, and `write_json <top>_synth.json`. It also prints the Warning count from the log. Missing Yosys → die with "run provision.sh".

**Q52: What does `cmd_pnr` produce for ice40 vs ecp5?**
A: ice40: `nextpnr-ice40 --json <synth.json> --pcf <constraints> --asc <top>.asc --seed 1 --freq <clock_mhz>`; ecp5: `nextpnr-ecp5 --json --lpf --textcfg <top>.config --<device>` (device from `OPENRTL_DEVICE`, default 25k); generic: `nextpnr-generic`. After P&R it runs `icepack` to produce the `<top>.bin` bitstream and extracts the "Max frequency" block from pnr.log into `build/timing/timing.rpt`.

**Q53: How does flow.sh know the target clock frequency?**
A: `clock_mhz()` parses the first `-period <ns>` in `constraints/*.sdc`, converting it to MHz (`1000 / period`), else uses `OPENRTL_FREQ_MHZ` (default 100). That feeds `nextpnr --freq`, so P&R is constraint-driven rather than guessing — the SDC, not a magic constant, sets the timing target.

**Q54: How does the power estimate work?**
A: `cmd_power` calls the report engine's `power` section: a toggle-based estimate using a netlist cell model (counts cell types from the synth JSON/stat, applies assumed toggle activity), writing `build/power/power.md` and printing the first 30 lines. It's a scouting estimate, not sign-off-grade — the README is honest that this is "toggle-based power estimate per resource," which is the right fidelity for architecture decisions.

**Q55: How does coverage work with Verilator?**
A: `cmd_coverage` requires Verilator + an `OPENRTL_COVERAGE_WORKSPACE`. It compiles RTL with `verilator --cc --coverage --sv ... -CFLAGS "-std=c++11" --Mdir <workspace>`; after you run simulation in that workspace it merges the `.dat` files with `verilator_coverage --annotate` and `--write build/coverage/coverage.dat`. Statement and toggle coverage land in a single mergeable dat for the report.

**Q56: What is the `verify` step and why does it exist?**
A: It re-reads the *synthesized netlist* with Yosys together with the arch cell sim-models (`cells_sim.v` from the yosys datdir), runs `hierarchy -check` and `check`, and appends `NETLIST LINT PASS (0 problems)` on success. This is a netlist lint-clean re-check: it proves the synthesized structural netlist re-elaborates cleanly against the target's cell-library sim models — catching gate-level issues that RTL lint can't.

**Q57: How do reports and handoff work end-to-end?**
A: `cmd_reports` runs `report.py all --project --top --arch`, copies `docs/*/reports` into `build/reports` for artifact capture, and lists every generated `.md`. `cmd_handoff` runs `report.py handoff` which packages reports + netlist + bitstream into `docs/34-release/handoff/<project>-handoff-<date>.zip` — the actual deliverable for a manufacturing/release handoff.

**Q58: How does `flow.sh all` orchestrate the entire pipeline?**
A: It iterates `doctor lint sim formal synth pnr timing power coverage verify reports handoff`. Per step it checks the `NEEDS` map (formal:sby, sim:iverilog, pnr/timing:nextpnr-$ARCH); missing tools cause a graceful skip with a warning; any step that runs and fails is recorded (rc=1) but execution continues; doctor's own findings are informational (it can't proceed without yosys). It finishes with `=== pipeline finished (rc=N) ===`.

**Q59: Why does the pipeline continue-on-failure instead of stopping dead?**
A: A broken P&R shouldn't erase the synthesis report a designer still needs; and on a partially-provisioned machine the pipeline should produce whatever it can rather than nothing. `all` reports rc so CI can still fail the job — it's "collect as much signal as possible, then gate," the same philosophy as structured log collection in my FastAPI services.

**Q60: How is `flow.sh test` wired?**
A: It forwards `--only <suite>`, `--verbose`, `--tap`, `--list` straight to `tests/run_tests.sh`, so the same test suite is available as a flow command, a Makefile target (`make test`), an npm script (`bun run test`), and a CI step — one suite, four entry points, zero duplication.

---

## 5. Report Engine & Visualization (Q61–Q72)

**Q61: What does the report engine do, at a high level?**
A: `report/report.py` parses *real tool output* — yosys logs/stat files, nextpnr logs, SDC constraints, pytest results, netlist JSON — and renders every deliverable into `docs/<phase>/reports/<section>.md` plus dependency-free SVG infographics, and can package a handoff zip. Sections: `synth`, `pnr`, `timing`, `power`, `coverage`, `formal`, `sim`, `quality`, `all`, `handoff`. It's pure Python 3.8+, zero third-party dependencies, and degrades gracefully to "pending" when artifacts are missing.

**Q62: Why "dependency-free" for the report engine?**
A: It must run in CI containers, on bare-metal machines mid-provisioning, and inside constrained agent sandboxes; the only required runtime is Python 3.8+. Charts come from `report/svg.py` — a small hand-rolled SVG library (`bar_chart`, `donut_chart`, `gauge_chart`, `histogram`, `hbar_chart`, `line_chart`, `PALETTE`). No matplotlib, no pandas, no node — which means the report step can never be the thing that fails to install.

**Q63: How does the synth report avoid hallucinating numbers?**
A: It parses the yosys log: `parse_yosys_stat` handles both stat orientations (`<count> <cellname>` from the `tee -o` stat file and the `Number of cells:` block `<cellname> <count>`), `parse_resource_summary` reads wires/bits/ports/memories/processes (both formats), `parse_inference` maps pass names (`proc`, `opt_expr`, `alumacc`, `sharing`, `abc9`, `memory_collect`, `fsm`, `dfflegalize`, `ice40_opt`…) to human notes, and `parse_warnings` dedupes up to 30 warnings. `device_utilization` divides actual cell counts (matched by cell-type prefixes via `BUDGET_CELLS`: `SB_LUT4`→lut, `SB_DFF`→ff, `SB_RAM40_4K`→bram, `SB_DSP`→dsp, `SB_PLL40_CORE`→pll, `SB_IO`→io) by the device budget from `DEVICE_BUDGET`. All numbers come from the tools, never generated.

**Q64: What are the device budgets and how are they used?**
A: `DEVICE_BUDGET` is a lookup per arch/device — ice40up5k (5280 LUT/FF, 30 BRAM, 1 PLL, 48 IO), ice40hx8k, ecp5 lfe5u-25f/45f/85f, nexus lfcp5-85f, etc. "approx figures from vendor datasheets." The util function returns `(RESOURCE, used, available, %)` per budget resource, which is exactly what the "device budget" and utilization infographics plot — the engineer sees at a glance whether the design fits the chosen device.

**Q65: Walk me through the cascade that resolves top/device/arch in report.py.**
A: `resolve_top` checks CLI flag → `openrtl-project.json` `top` → DECISION-070 regex → Makefile `--top-module`/`TOPLEVEL` → first `module` in sorted `rtl/*.sv`/`rtl/*.v` → default "top". `resolve_arch` checks CLI → DECISION regex (ice40|ecp5|nexus|generic) → default ice40. `resolve_device` reads `device` from the JSON. Every consumer (flow.sh and report.py) uses the same resolution rules, so they can never disagree.

**Q66: How does the timing report work?**
A: It reads `build/timing/timing.rpt` (produced by `flow.sh pnr` from the nextpnr "Max frequency" block) and renders fmax/slack/WNS/TNS-oriented Markdown + charts. If P&R hasn't run, the section degrades to "pending" with a pointer to run `flow.sh pnr` first rather than crashing with a KeyError — same graceful-degradation pattern across every section.

**Q67: How does the handoff packaging work?**
A: `cmd_handoff`/`report.py handoff` collects the reports (docs/*/reports), the netlist (`build/synth/<top>_netlist.v`), the bitstream (`build/pnr/<top>.bin`) and zips them to `docs/34-release/handoff/<project>-handoff-<date>.zip`. That single zip is the contractual "this is what you ship" artifact. Artifact locations come from `manifest.yaml`.

**Q68: How are SDC constraints represented in reports?**
A: `parse_sdc` reads every `constraints/*.sdc`, strips comments/blanks, and returns (directive, statement) tuples which the constraints section renders — so the timing targets actually used by P&R are visible in the published report, closing the loop between "what we told nextpnr" and "what timing we got."

**Q69: What's the quality section?**
A: `quality` aggregates the synth/pnr/timing/power/coverage/sim/formal sections into a single assessment document — the executive summary of the flow. It's the one place a reviewer (human or the openrtl-reviewer agent) goes to decide "is this design ready to move from verify to produce?" The dependency-free aggregation pulls the already-rendered per-section output together.

**Q70: Why SVG infographics? What do they show?**
A: Self-contained SVGs render anywhere (browsers, git diffs, docs, Markdown preview) without a charting runtime. Examples: utilization donut (used vs available per resource), resource histograms from the stat file, timing gauges, power hbar charts, regression trendlines. Dependency-free + embeddable was the requirement; hand-rolling SVG kept it zero-dep.

**Q71: How does the report engine stay robust to missing artifacts?**
A: Every section is written to "degrade gracefully to pending instead of crashing" (the module docstring states it as a promise). `read()` returns "" on OSError; `parse_*` functions return empty dicts/lists; `find_build` walks multiple candidate locations. So a half-run pipeline still produces a truthful, labeled report set — "pending" is honest, and the flow tells you which step to run to fill it.

**Q72: How is the report engine tested?**
A: `tests/test_report_engine.py` (394 lines) unit-tests the parsers — feeding it fixture yosys logs in both stat orientations, resource summaries, inference notes, warning lists — plus end-to-end runs against a generated fixture project. Combined with `tests/run_tests.sh` (633 lines) which generates a minimal RTL counter+add/sub into a temp sandbox and drives the full pipeline, missing tools produce SKIP while real parser regressions fail loudly.

---

## 6. Scaffolding & Project Structure (Q73–Q82)

**Q73: What does `scaffold.ts` generate?**
A: `bun scaffold/scaffold.ts --name alu4 --desc "4-bit ALU..." --top alu4 --arch ice40` creates `<dir>/alu4/` with `openrtl-project.json` (metadata + lifecycle), `docs/workflow/workflow.json`, `docs/00-project/` context, all 36 `docs/<NN>-<phase>/status.md + gates.md + ctx/*.md`, and the working tree: `rtl/`, `tb/`, `formal/`, `constraints/`, a `Makefile` wired to `flow.sh` (with `--top-module`/`TOPLEVEL` that `detect_top` can read), and a `.opencode/` agent+skills bundle so the project is immediately agent-ready. The whole tree is a stable skeleton the autopilot agent fills in.

**Q74: Why do phases carry a `ctx` list?**
A: Each phase's `ctx` defines its context files — status trackers like `project-description`, `toolchain`, `requirements`, `decisions`, `simulation`, `synthesis`, `timing-slack`, `wnS-tns`, `fmax`, `bom`, `assembly`, `compliance`, `release`. The scaffold creates those placeholders, and agents write into them. This is the file-first contract: the structure tells the agent what evidence a phase must produce, and the report engine knows where to write its section into.

**Q75: How does the scaffold encode dependencies as a DAG?**
A: Each `PhaseDef` lists `deps` (phase ids). The workflow engine advances a phase only when all deps are satisfied (status closed) — e.g. 23-formal requires 19 + 20; 29-system-validation requires 26 + 28 + 23; 34-release requires 29 + 33. The scaffold guarantees the DAG exists from day one; the workflow guarantees no jumping ahead. Cycles are impossible by construction because ids are numbered and deps point backward.

**Q76: Why gate types mapped to whole groups?**
A: `architecture` gates close the define/design phases (approvals happen before RTL is written), `implementation` gates close actual artifact production (20, 21, 24, 27), `timing` gates close verify (25/26/29 — the hidden snag of any FPGA project), `ops` gates close produce/sustain. The gate type is a categorical "what kind of sign-off does this need," letting the review process adapt per phase rather than one-size-fits-all.

**Q77: What does the generated Makefile do?**
A: It's wired to `flow.sh` (`make all`, `make lint`, `make sim`, etc.) so engineers get a familiar entry point, and its `--top-module`/`TOPLEVEL` serves as a fallback for top-module auto-detection when the DECISION file or project JSON isn't matched. The scaffold README's canonical commands — `make all`, `flow.sh all` — are interchangeable by design (package.json scripts wrap the same flow.sh).

**Q78: How does a project get a `.opencode/` bundle?**
A: The scaffold emits `.opencode/` with the agent + skills bundle so the *generated project* is self-contained — you can open it in opencode and the OpenRTL agents, commands, and skills are there without cloning the whole toolchain repo. This is distribution: the workflow travels with the project, not the other way around.

**Q79: How is `workflow.json` consumed?**
A: `/openrtl-workflow status|advance|resume|rollback` reads `docs/workflow/workflow.json` for current phase, deps, gate, blockers; `advance` moves to the next runnable phase only when deps satisfied + gate passed + reviews done; `rollback <phase>` re-opens for rework. It's the durable state machine of the project — the file-first equivalent of "where are we?".

**Q80: How do you keep the scaffold's PHASES list in sync with the workflow JSON and the manifest?**
A: `scaffold.ts` is the single source of truth for the lifecycle (it either writes `workflow.json` from the same `PHASES` array or the JSON mirrors it), and `manifest.yaml` separately but consistently maps tools→phases. The constraint I enforce: phase ids in scaffold, workflow.json, and manifests must match; the tests (`test_report_engine.py`, flow tests) assert the generated tree has all 36 phase dirs and correct deps.

**Q81: What edge cases did you handle in scaffolding?**
A: (1) Naming — package renamed to `openrtl-toolchain` to avoid a turbo workspace-name conflict (my third commit was literally that fix). (2) `--dir` vs current dir output paths. (3) Dotted/top-module identifiers validated before writing. (4) Re-scaffolding an existing dir must not clobber user work (idempotent creation of missing pieces). (5) Makefile + DECISION + project.json must all agree on top by construction.

**Q82: How would you extend scaffolding?**
A: (1) A `--template` gallery (counter, ALU, UART, AXI-lite…). (2) `--vendor flow` adapters (Vivado/Quartus) generating vendor project files. (3) Auto-seeding `tb/` with a cocotb harness per top module. (4) `--device` validation against `DEVICE_BUDGET`. (5) A `--git` flag that initializes the repo with the CI workflow pre-installed.

---

## 7. Testing & CI/CD (Q83–Q90)

**Q83: What is the automated test strategy?**
A: `tests/run_tests.sh` (633 lines) generates a minimal RTL fixture (counter + add/sub) into a temp sandbox *at test time* — no design files ship in the repo — and drives it through every tool the monster pipeline touches: yosys, verilator, iverilog, nextpnr, icetime, cocotb, SymbiYosys, the report engine, the flow pipeline, and the scaffold. Missing tools report `SKIP`; any real failure is a non-zero exit. Plus `test_report_engine.py` unit-tests the parsers with real fixture logs.

**Q83b: Why generate fixtures at test time?**
A: Shipping design files in the repo would (a) imply they're example deliverables, (b) bloat the repo, and (c) go stale. Generating a minimal counter+add/sub fixture in a temp sandbox means the test always exercises the actual toolchain against known-good minimal design and never depends on checked-in artifacts that can rot. It also mirrors real usage: the flow is tested the way a user drives it.

**Q85: How is the suite organized per tool?**
A: `run_tests.sh` iterates over suites keyed by the manifest's tools; each suite runs its tool's test and reports `PASS`/`FAIL`/`SKIP`. `flow.sh test --only yosys` runs just one suite; `--verbose`/`--tap` forward more detail. Tools not installed → SKIP (so a laptop without sby still exercises everything else), and CI is configured to treat SKIP legitimately but FAIL strictly.

**Q86: What does the CI entry point do?**
A: `cicd/ci.sh --skip-install` runs doctor (gating) + the full suite; `cicd/openrtl-ci.yml` is a GitHub Actions workflow template that provisions the toolchain in CI (conda/pip/source) and runs the suite on push/PR. Provisioning in CI is the same one-shot `provision.sh`, so the CI environment matches a developer laptop — no hidden drift between "works on my machine" and "works in CI."

**Q87: Why treat doctor as a CI gate?**
A: A flow test that silently SKIPPs 5 tools is worthless — it looks green but validated nothing. doctor's non-zero exit on missing required tools forces provisioning to happen or the job to fail, making coverage truthful. `--skip-install` assumes a pre-provisioned runner; without it, ci.sh provisions first. Either way the gate is: required tools present AND suite green.

**Q88: What's the risk of test flakiness given real EDA tools?**
A: Real tools are slow and version-sensitive; I mitigated by (1) version floors in the manifest + doctor checks, (2) fixture design minimized to counter+add/sub so runs are seconds not minutes, (3) `--seed 1` for reproducible P&R, (4) SKIP not FAIL for genuinely-missing optional tools, (5) temp-sandbox isolation so failures can't pollute a repo. The one flakiness class left — version-imposed behavior drift — is caught by doctor before tests run.

**Q89: How does the agent workflow get tested?**
A: The repo itself is the test harness: `opencode` runs are exercised against generated projects. Constraints like "re-run `flow.sh test` after changing any tool integration or parser and leave the suite green" are encoded in the `openrtl-toolchain` skill, so agents are instructed to verify their own changes — and CI re-runs the suite on every PR merging into the toolchain, giving the agent work an independent backstop.

**Q90: How does OpenRTL's testing compare to enterprise EDA sign-off?**
A: We don't claim sign-off-grade verification — this is a *workflow-automation* suite proving the pipeline, tools, and parsers work end to end. Real sign-off (coverage goals, formal completeness, timing margin sign-off, ECO) remains the design engineer's job with the tools OpenRTL drives. The suite's job is to guarantee the *infrastructure* is correct so a designer can trust the reports those tools feed.

---

## 8. Engineering Decisions & Scaling (Q91–Q100)

**Q91: What's the relationship between the agent platform and deterministic EDA tooling?**
A: Complementary, never one replacing the other: agents (LLM) are used where semantics live — interpreting a product description, writing RTL intent, generating testbenches, reading tool output and explaining it; deterministic tools (Verilator/Yosys/nextpnr/SymbiYosys) are the ground truth for "did it actually work." The agents plan and write; the flow verifies; the report engine parses; the reviewer agent gates. This is the same hybrid-decision I defend for MigratorGen: use the LLM only where the answer is ambiguous, keep everything measurable deterministic.

**Q92: What is the biggest correctness risk in an agent-driven hardware flow, and how do you mitigate it?**
A: Silent fabrication — the agent "reports" a design as passing lint/synthesis when it never ran the tool. Mitigations: (1) `flow.sh` is the only sanctioned execution path and artifacts land at canonical paths; (2) the report engine parses real logs, so numbers trace to actual tool output; (3) `verify` re-lints the netlist; (4) reviewer/validator agents and gates prevent self-approval; (5) CI runs the suite independently. The invariant is: every number in every report must be projector from a tool artifact.

**Q93: How is this different from OpenRTL.ai v1, concretely?**
A: v1 = single Streamlit page: natural-language → Gemini Verilog → Verilator lint loop (≤5 auto-fix iterations) → Yosys synth → metrics/schematic. OpenRTL = multi-agent lifecycle: 36 phases, ~35 domain subagents, quality gates, decision records, workflow state machine, whole open-source FPGA P&R toolchain, reports+infographics, tests, CI, and scaffold-generated projects. v1 proved the LLM can write RTL; OpenRTL is the product-development infrastructure around that idea.

**Q94: Where does firmware sit in a flow that's about RTL?**
A: Phase 17 Firmware Architecture and a `firmware-engineer` agent: a real SoC/FPGA product ships with software — boot bring-up, register drivers, HPS/soft-core code (and the `embedded-engineer` plus `field-support-engineer` agents cover the board + in-the-field lifecycle). Including firmware as a first-class phase is part of what makes this a *product* workflow, not a Verilog scratchpad.

**Q95: How would you scale this to a team of many engineers?**
A: (1) The file-first docs are already the shared design record any engineer can diff. (2) Per-project workflow.json + gates give PR-style approval semantics. (3) The openrtl-* subagents can be reassigned per discipline like a staffing model. (4) CI on PRs to the toolchain keeps infra green for everyone. (5) Next: per-role permission scopes and a review bot that blocks merges until the reviewer validator signs off — mirroring required-CI-checks from my Krip AI internship.

**Q96: What open-source EDA gaps remain, and what did you do about them?**
A: The big gaps are static timing sign-off depth and vendor-arch fidelity: I use nextpnr/icetime for STA and unpack P&R reports, which is scrouting-grade, not tape-out-grade; formal is SymbiYosys (SMT-based BMC — solid but not full equivalence-checking at scale). I document this honestly in the flow docs ("toggle-based power estimate", "scouting, not sign-off") and keep vendor adapters optional, so teams that need Vivado/Quartus can plug in without forking the flow.

**Q97: How does this project reflect your AI-engineering skills specifically?**
A: Prompt/system-engineering at scale (37 agents, phase skills, commands — a real "swarm" orchestration design), file-first state design (the agent's memory is the repo), tool-calling discipline (flow.sh + doctor + tests as guardrails), hybrid LLM/deterministic architecture, and CI/CD hygiene — the same themes as MigratorGen (structured rules + deterministic rewrite engine) and my internships (FastAPI + Docker + GitHub Actions). It's a resume line that demonstrates "I can build agent infrastructure, not just call an API."

**Q98: How would you make OpenRTL production-ready for a company?**
A: (1) A managed runner for agents + flow in CI with results artifacted. (2) Secrets handling for vendor tool licenses and API keys. (3) Version-pinning the whole manifest + reproducible environments via the conda/nix integration the repo already has (`flake.nix`, `nix` dir). (4) A reporting service exposing the SVGs/Markdown as a web dashboard. (5) Template catalog + plugin registry for tool adapters. (6) Formal docs for the review/approval workflow so it can be audited.

**Q99: What would you do differently if starting over?**
A: (1) Define the manifest as JSON schema-validated from day one (YAML is readable but schemaless). (2) Encode the 36-phase DAG in a single serialized format the scaffold, workflow engine, and report engine all consume directly, eliminating mirror/duplication. (3) Build the CI workflow template before the toolchain (tests would have caught tool gaps sooner). (4) Add a golden-project end-to-end test earlier. (5) Keep the agent definitions generating from a data model, so adding phase skills doesn't mean 37 hand-edited files.

**Q100: Where does OpenRTL go next — what's the roadmap?**
A: (1) Golden end-to-end integration test in CI with the full P&R toolchain provisioned. (2) Vivado/Quartus adapter reference implementations. (3) A project dashboard (web) rendering the existing SVG/Markdown reports. (4) Multi-user workflow state with approvals. (5) A "power-tool" manifest with openSTA for real STA. (6) Publish it as a reusable open-source "agentic semiconductor workflow" template — the goal is that describing a chip gets you not just RTL, but a reviewed, verified, synthesis-and-P&R-closed hardware project.

---

*Revision checklist: all answers verified against the OpenRTL repo — `packages/openrtl/` (README, package.json `openrtl-toolchain`, toolchain/flow.sh 376 lines, toolchain/manifest.yaml 150 lines, toolchain/provision.sh, toolchain/doctor.sh, toolchain/conda-env.yml, scaffold/scaffold.ts 296 lines, report/report.py 995 lines, report/svg.py, tests/run_tests.sh, tests/test_report_engine.py, cicd/) and `.opencode/` (37 agent files incl. openrtl.md primary agent on nvidia/deepseek-r1, 18 commands, numbered phase skills + openrtl-toolchain/openrtl-flow skills, opencode.jsonc) — agents, commands, flow commands, artifact paths, phase list, and manifest fields all match the code.*