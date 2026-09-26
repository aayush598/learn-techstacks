# CUDA Black Hole Raytracer — Learning Resource

A complete, curated study resource for building a **custom CUDA raytracer for
black holes** and connecting it to **GRMHD simulation output** (Athena++ /
HARM). 158 topic files, each with 100 hand-written interview-style Q&A pairs
(15,800 questions in total), in the same `## QN:` / `**A:**` flashcard format
as the Infosys-SP-DSE resource in this repository.

## Structure

The training material is organized into 11 domains (each domain is a numbered
directory, each topic a leaf folder containing `questions.md`):

| # | Domain | Leaves | Topics |
|---|--------|--------|--------|
| 01 | CUDA | 16 | kernel launch, memory, synchronization, occupancy, streaming, multi-GPU |
| 02 | Ray-Tracing | 14 | ray generation, BVH, intersections, shading, CUDA raytracer architecture |
| 03 | Relativity | 16 | metric tensor, Christoffel, geodesic equation, Schwarzschild & Kerr |
| 04 | GR-Ray-Tracing | 16 | null geodesics, Boyer-Lindquist, Carter constant, photon sphere, shadow, lensing |
| 05 | GRMHD | 16 | MHD equations, Riemann solvers, Athena++/HARM, primitive recovery, MAD vs SANE |
| 06 | Radiative-Transfer | 14 | RTE, synchrotron emission/absorption, bremsstrahlung, polarization, spectra |
| 07 | Numerical-Methods | 14 | RK45, adaptive stepping, interpolation, voxel/octree traversal, precision |
| 08 | GPU-Performance | 14 | coalescing, shared memory, occupancy, streams, CUDA graphs, Nsight |
| 09 | Production | 14 | CMake, project layout, CLI, testing, reproducibility, FFmpeg, containers |
| 10 | Astrophysics | 12 | accretion disks, MRI, jets, M87*/Sgr A* EHT, photon ring, Gargantua |
| 11 | End-to-End | 12 | full pipeline, GRMHD import, validation, movies, comparing to real images |

**Total: 158 leaves × 100 Q&A = 15,800 questions.**

## Intended Learning Path

Follow the domains in order: **01 → 02** get you the CUDA/raytracing engine,
**03 → 04** add the general relativity physics that makes the raytracer a
*black-hole* raytracer, **05 → 06** connect accretion physics and light
emission, **07 → 08** harden the numerics and the GPU performance, **09** makes
it a production project, and **10 → 11** connect everything to real
astrophysics (the Event Horizon Telescope images) and end-to-end delivery.

## File Format

Every `questions.md` follows the samora flashcard parser contract:

```
# <Domain> — <Topic> Interview Questions and Answers

## QN: <question>
**A:** <answer>

## QN: <question>
**A:** <answer>

...
```

Exactly 100 questions and 100 answers per file, one blank line between
entries, `## QN:` heading on its own line, `**A:**` immediately after.

## Rebuilding

The `questions.md` files are generated from curated content modules under
`00-Build-Scripts/`. To regenerate everything from scratch:

```bash
cd 00-Build-Scripts
python3 run_build.py
```

The runner imports `c_cuda.py … c_end.py` (one module per domain group), maps
every curated topic key (`"03-Relativity/06-Schwarzschild-Metric"`) to its leaf
directory, and pads each file out to 100 Q&A using domain-appropriate filler
templates. Diagnostic output reports matched/unmatched leaves and orphan keys.

```
Content keys: 158 | Matched leaves: 158 | Unmatched leaves: 0
Files written: 158 Total questions: 15800
```

### Editing topics

- A topic with curated content: edit the matching key in the relevant `c_*.py`,
  then re-run `run_build.py`. Existing `questions.md` files are fully rewritten,
  so keep them generated, never hand-edited.
- A brand-new topic: create the leaf directory under a domain, add a key with
  the same rel-path string in the content module, re-run.

## Relation to the other resources

- `Infosys-SP-DSE-Interview-Prep/` — the same build pipeline and flashcard
  format applied to DSE/interview prep for the Infosys Special Program.
- `samora-ai/` — external reference for the `## QN:` / `**A:**` parsing format.