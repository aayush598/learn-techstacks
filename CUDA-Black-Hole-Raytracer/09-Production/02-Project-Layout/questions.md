# Production — Project Layout Interview Questions and Answers

## Q1: What is the recommended source layout?
**A:** src/ (core lib: metric, geodesic, transfer, kernels), include/ (public headers), tools/ (cli: render, movie, validate), utils/ (grmhd converters), tests/ - a library-first structure.

## Q2: Why a library + CLI split?
**A:** The raytracer as a library lets tests, benchmarking, and alternate frontends link the same core; the CLI is a thin argument-parsing shell over it.

## Q3: Where do the CUDA kernels live?
**A:** src/gpu/*.cu for the device code and src/gpu/*.cuh headers; host wrappers in src/cpu/ - kernels compiled independently, host calls via a clean API.

## Q4: What is the role of the kernel CMake target?
**A:** Each .cu gets its own library target for correct arch flags; a single 'ray' top-level target aggregates - incremental compiles stay correct and fast.

## Q5: How do you separate data formats?
**A:** utils/ owns the GRMHD (HDF5/FITS) readers and the interpolated-field serialization - the core never depends on a simulation format directly.

## Q6: Where do tests live in relation to golden data?
**A:** tests/ holds the analytic golden files (shadow radius, deflection, doppler) PLUS a build-time downloader for the real GRMHD snapshot - both wired to ctest.

## Q7: What is the include-heirarchy discipline?
**A:** Internal-only headers under src/**/impl, public API headers in include/raytracer - prevents accidental cross-thread include tangles.

## Q8: How does the CLI stay consistent?
**A:** Options struct (clipp/argparse) in tools/cli parsed into a config struct consumed by the API - the CLI is data, the library is the logic.

## Q9: Where do configs/results go?
**A:** config/ holds the YAML/JSON run templates; out/ stores per-run frames + metadata - a fixed, documented out/ layout the pipeline scripts depend on.

## Q10: What is the 'scenes' directory?
**A:** data/scenes: the processed field volumes and their metadata (YAML/JSON), split by simulation and snapshot - the raytracer's consumable dataset home.

## Q11: How do you organize ongoing experiments?
**A:** A reproducible run directory per parameter set: out/<run-id>/ with the config, log, and outputs - every artifact traceable to one command.

## Q12: What is the summary?
**A:** A library-first layout: core kernels + host API as the engine, thin CLI, converters out of the core, and a fixed out/run-id hierarchy - maintenance is the product.

## Q13: Why does project layout matter for a research raytracer?
**A:** Because the tool must be reproducible, testable, and maintainable for months of tuning; project layout turns a script into a reliable product.

## Q14: What does project layout guarantee in a CI pipeline?
**A:** Every change builds, the golden images still match, and performance did not regress; project layout automation protects the project from careless commits.

## Q15: How does project layout structure code for tests?
**A:** Pure functions with injected parameters, golden-image comparisons, and analytic fixtures; project layout makes kernels unit-testable on the host.

## Q16: What is the role of project layout configuration?
**A:** Camera pose, metric, integrator, resolution, and data paths become CLI/JSON inputs so project layout runs are documented by their arguments.

## Q17: How does project layout handle environment variability?
**A:** CMake + containers pin compilers and CUDA versions; project layout reproducibility starts with a deterministic build environment.

## Q18: What does project layout add to the learning process?
**A:** Small milestones with acceptance criteria turn 'make an image' into 'make a trustworthy image'; project layout is how you actually finish.

## Q19: How is project layout validated numerically?
**A:** Against analytic Schwarzschild results and conserved-quantity drift checks before any visual tuning; project layout correctness precedes beauty.

## Q20: What is a reasonable project layout schedule?
**A:** Physics validation first, single frame next, movie pipeline last; project layout ordering prevents rework when physics changes.

## Q21: How does project layout manage data files?
**A:** Version registers, snapshot metadata, and hash checks before rendering so project layout always knows exactly which data made the image.

## Q22: What logging does project layout produce?
**A:** Progress per frame, step stats per region, and warnings for unphysical states; project layout logs are written to machine-parseable format.

## Q23: How does project layout make a movie?
**A:** Render each frame to an image file, then encode with ffmpeg using a fixed color pipeline; project layout encodes losslessly first, then to final.

## Q24: What does project layout do for performance budgeting?
**A:** Records time per frame phase (import, trace, post) and asserts budgets; project layout finds regressions before users notice them.

## Q25: How does project layout approach documentation?
**A:** A README per stage, a one-page architecture diagram, and a changelog; project layout documentation is updated with the code it explains.

## Q26: What is project layout quality-of-life?
**A:** Fast debug renders at low resolution, hot-reloaded config, and a progress bar - project layout makes iteration pleasant enough to be productive.

## Q27: How does project layout ensure portability?
**A:** Optional CUDA paths with CPU fallbacks and hardware queries; project layout runs on laptops and clusters with the same command line.

## Q28: What is the project layout acceptance test suite?
**A:** Verify build, run unit tests, render a small golden image, run a tiny movie, and check hashes - all automated in project layout CI.

## Q29: How does project layout select rendering parameters?
**A:** Defaults live in config files with ranges; project layout records effective parameters in the output metadata for every render.

## Q30: What is project layout two-tier testing?
**A:** Fast smoke tests on every commit plus full-scale golden renders nightly; project layout balances speed against coverage.

## Q31: How does project layout handle GPU-specific bugs?
**A:** Reproduce on the reference CPU path and bisect parameters; project layout isolates hardware issues from logic issues by identical interfaces.

## Q32: What does project layout require before a release?
**A:** Clean checkout builds, tests pass, golden images regenerated deliberately, and a versioned changelog; after that project layout is releasable.

## Q33: How does project layout inherit good practices from research code?
**A:** Every paper figure must be reproducible; project layout enforces the same discipline with stored parameters and hashed inputs.

## Q34: What is the role of project layout code review?
**A:** Catch numeric and architecture mistakes early; project layout review checklist includes dimension checks, tolerance choices, and unit conventions.

## Q35: How is project layout balanced against research freedom?
**A:** Experiments go in branches; the mainline stays green behind project layout gates so nothing is ever rendered from a broken tree.

## Q36: What is the final measure of project layout success?
**A:** A fresh checkout reproduces published images in a known time, letting anyone extend the work - that is production-grade project layout.

## Q37: What is the final measure of project layout success - justify your answer with a concrete production example.
**A:** A fresh checkout reproduces published images in a known time, letting anyone extend the work - that is production-grade project layout. A concrete example: consistently applying project layout in code review and regression tests keeps the whole pipeline trustworthy.

## Q38: How is project layout balanced against research freedom - justify your answer with a concrete production example.
**A:** Experiments go in branches; the mainline stays green behind project layout gates so nothing is ever rendered from a broken tree. A concrete example: consistently applying project layout in code review and regression tests keeps the whole pipeline trustworthy.

## Q39: What is the role of project layout code review - justify your answer with a concrete production example.
**A:** Catch numeric and architecture mistakes early; project layout review checklist includes dimension checks, tolerance choices, and unit conventions. A concrete example: consistently applying project layout in code review and regression tests keeps the whole pipeline trustworthy.

## Q40: How does project layout inherit good practices from research code - justify your answer with a concrete production example.
**A:** Every paper figure must be reproducible; project layout enforces the same discipline with stored parameters and hashed inputs. A concrete example: consistently applying project layout in code review and regression tests keeps the whole pipeline trustworthy.

## Q41: What does project layout require before a release - justify your answer with a concrete production example.
**A:** Clean checkout builds, tests pass, golden images regenerated deliberately, and a versioned changelog; after that project layout is releasable. A concrete example: consistently applying project layout in code review and regression tests keeps the whole pipeline trustworthy.

## Q42: How does project layout handle GPU-specific bugs - justify your answer with a concrete production example.
**A:** Reproduce on the reference CPU path and bisect parameters; project layout isolates hardware issues from logic issues by identical interfaces. A concrete example: consistently applying project layout in code review and regression tests keeps the whole pipeline trustworthy.

## Q43: What is project layout two-tier testing - justify your answer with a concrete production example.
**A:** Fast smoke tests on every commit plus full-scale golden renders nightly; project layout balances speed against coverage. A concrete example: consistently applying project layout in code review and regression tests keeps the whole pipeline trustworthy.

## Q44: How does project layout select rendering parameters - justify your answer with a concrete production example.
**A:** Defaults live in config files with ranges; project layout records effective parameters in the output metadata for every render. A concrete example: consistently applying project layout in code review and regression tests keeps the whole pipeline trustworthy.

## Q45: What is the project layout acceptance test suite - justify your answer with a concrete production example.
**A:** Verify build, run unit tests, render a small golden image, run a tiny movie, and check hashes - all automated in project layout CI. A concrete example: consistently applying project layout in code review and regression tests keeps the whole pipeline trustworthy.

## Q46: How does project layout ensure portability - justify your answer with a concrete production example.
**A:** Optional CUDA paths with CPU fallbacks and hardware queries; project layout runs on laptops and clusters with the same command line. A concrete example: consistently applying project layout in code review and regression tests keeps the whole pipeline trustworthy.

## Q47: What is project layout quality-of-life - justify your answer with a concrete production example.
**A:** Fast debug renders at low resolution, hot-reloaded config, and a progress bar - project layout makes iteration pleasant enough to be productive. A concrete example: consistently applying project layout in code review and regression tests keeps the whole pipeline trustworthy.

## Q48: How does project layout approach documentation - justify your answer with a concrete production example.
**A:** A README per stage, a one-page architecture diagram, and a changelog; project layout documentation is updated with the code it explains. A concrete example: consistently applying project layout in code review and regression tests keeps the whole pipeline trustworthy.

## Q49: What does project layout do for performance budgeting - justify your answer with a concrete production example.
**A:** Records time per frame phase (import, trace, post) and asserts budgets; project layout finds regressions before users notice them. A concrete example: consistently applying project layout in code review and regression tests keeps the whole pipeline trustworthy.

## Q50: How does project layout make a movie - justify your answer with a concrete production example.
**A:** Render each frame to an image file, then encode with ffmpeg using a fixed color pipeline; project layout encodes losslessly first, then to final. A concrete example: consistently applying project layout in code review and regression tests keeps the whole pipeline trustworthy.

## Q51: What logging does project layout produce - justify your answer with a concrete production example.
**A:** Progress per frame, step stats per region, and warnings for unphysical states; project layout logs are written to machine-parseable format. A concrete example: consistently applying project layout in code review and regression tests keeps the whole pipeline trustworthy.

## Q52: How does project layout manage data files - justify your answer with a concrete production example.
**A:** Version registers, snapshot metadata, and hash checks before rendering so project layout always knows exactly which data made the image. A concrete example: consistently applying project layout in code review and regression tests keeps the whole pipeline trustworthy.

## Q53: What is a reasonable project layout schedule - justify your answer with a concrete production example.
**A:** Physics validation first, single frame next, movie pipeline last; project layout ordering prevents rework when physics changes. A concrete example: consistently applying project layout in code review and regression tests keeps the whole pipeline trustworthy.

## Q54: How is project layout validated numerically - justify your answer with a concrete production example.
**A:** Against analytic Schwarzschild results and conserved-quantity drift checks before any visual tuning; project layout correctness precedes beauty. A concrete example: consistently applying project layout in code review and regression tests keeps the whole pipeline trustworthy.

## Q55: What does project layout add to the learning process - justify your answer with a concrete production example.
**A:** Small milestones with acceptance criteria turn 'make an image' into 'make a trustworthy image'; project layout is how you actually finish. A concrete example: consistently applying project layout in code review and regression tests keeps the whole pipeline trustworthy.

## Q56: How does project layout handle environment variability - justify your answer with a concrete production example.
**A:** CMake + containers pin compilers and CUDA versions; project layout reproducibility starts with a deterministic build environment. A concrete example: consistently applying project layout in code review and regression tests keeps the whole pipeline trustworthy.

## Q57: What is the role of project layout configuration - justify your answer with a concrete production example.
**A:** Camera pose, metric, integrator, resolution, and data paths become CLI/JSON inputs so project layout runs are documented by their arguments. A concrete example: consistently applying project layout in code review and regression tests keeps the whole pipeline trustworthy.

## Q58: How does project layout structure code for tests - justify your answer with a concrete production example.
**A:** Pure functions with injected parameters, golden-image comparisons, and analytic fixtures; project layout makes kernels unit-testable on the host. A concrete example: consistently applying project layout in code review and regression tests keeps the whole pipeline trustworthy.

## Q59: What does project layout guarantee in a CI pipeline - justify your answer with a concrete production example.
**A:** Every change builds, the golden images still match, and performance did not regress; project layout automation protects the project from careless commits. A concrete example: consistently applying project layout in code review and regression tests keeps the whole pipeline trustworthy.

## Q60: Why does project layout matter for a research raytracer - justify your answer with a concrete production example.
**A:** Because the tool must be reproducible, testable, and maintainable for months of tuning; project layout turns a script into a reliable product. A concrete example: consistently applying project layout in code review and regression tests keeps the whole pipeline trustworthy.

## Q61: Why does project layout matter for a research raytracer - justify your answer with a concrete production example.
**A:** Because the tool must be reproducible, testable, and maintainable for months of tuning; project layout turns a script into a reliable product. A concrete example: consistently applying project layout in code review and regression tests keeps the whole pipeline trustworthy.

## Q62: What does project layout guarantee in a CI pipeline - justify your answer with a concrete production example.
**A:** Every change builds, the golden images still match, and performance did not regress; project layout automation protects the project from careless commits. A concrete example: consistently applying project layout in code review and regression tests keeps the whole pipeline trustworthy.

## Q63: How does project layout structure code for tests - justify your answer with a concrete production example.
**A:** Pure functions with injected parameters, golden-image comparisons, and analytic fixtures; project layout makes kernels unit-testable on the host. A concrete example: consistently applying project layout in code review and regression tests keeps the whole pipeline trustworthy.

## Q64: What is the role of project layout configuration - justify your answer with a concrete production example.
**A:** Camera pose, metric, integrator, resolution, and data paths become CLI/JSON inputs so project layout runs are documented by their arguments. A concrete example: consistently applying project layout in code review and regression tests keeps the whole pipeline trustworthy.

## Q65: How does project layout handle environment variability - justify your answer with a concrete production example.
**A:** CMake + containers pin compilers and CUDA versions; project layout reproducibility starts with a deterministic build environment. A concrete example: consistently applying project layout in code review and regression tests keeps the whole pipeline trustworthy.

## Q66: What does project layout add to the learning process - justify your answer with a concrete production example.
**A:** Small milestones with acceptance criteria turn 'make an image' into 'make a trustworthy image'; project layout is how you actually finish. A concrete example: consistently applying project layout in code review and regression tests keeps the whole pipeline trustworthy.

## Q67: How is project layout validated numerically - justify your answer with a concrete production example.
**A:** Against analytic Schwarzschild results and conserved-quantity drift checks before any visual tuning; project layout correctness precedes beauty. A concrete example: consistently applying project layout in code review and regression tests keeps the whole pipeline trustworthy.

## Q68: What is a reasonable project layout schedule - justify your answer with a concrete production example.
**A:** Physics validation first, single frame next, movie pipeline last; project layout ordering prevents rework when physics changes. A concrete example: consistently applying project layout in code review and regression tests keeps the whole pipeline trustworthy.

## Q69: How does project layout manage data files - justify your answer with a concrete production example.
**A:** Version registers, snapshot metadata, and hash checks before rendering so project layout always knows exactly which data made the image. A concrete example: consistently applying project layout in code review and regression tests keeps the whole pipeline trustworthy.

## Q70: What logging does project layout produce - justify your answer with a concrete production example.
**A:** Progress per frame, step stats per region, and warnings for unphysical states; project layout logs are written to machine-parseable format. A concrete example: consistently applying project layout in code review and regression tests keeps the whole pipeline trustworthy.

## Q71: How does project layout make a movie - justify your answer with a concrete production example.
**A:** Render each frame to an image file, then encode with ffmpeg using a fixed color pipeline; project layout encodes losslessly first, then to final. A concrete example: consistently applying project layout in code review and regression tests keeps the whole pipeline trustworthy.

## Q72: What does project layout do for performance budgeting - justify your answer with a concrete production example.
**A:** Records time per frame phase (import, trace, post) and asserts budgets; project layout finds regressions before users notice them. A concrete example: consistently applying project layout in code review and regression tests keeps the whole pipeline trustworthy.

## Q73: How does project layout approach documentation - justify your answer with a concrete production example.
**A:** A README per stage, a one-page architecture diagram, and a changelog; project layout documentation is updated with the code it explains. A concrete example: consistently applying project layout in code review and regression tests keeps the whole pipeline trustworthy.

## Q74: What is project layout quality-of-life - justify your answer with a concrete production example.
**A:** Fast debug renders at low resolution, hot-reloaded config, and a progress bar - project layout makes iteration pleasant enough to be productive. A concrete example: consistently applying project layout in code review and regression tests keeps the whole pipeline trustworthy.

## Q75: How does project layout ensure portability - justify your answer with a concrete production example.
**A:** Optional CUDA paths with CPU fallbacks and hardware queries; project layout runs on laptops and clusters with the same command line. A concrete example: consistently applying project layout in code review and regression tests keeps the whole pipeline trustworthy.

## Q76: What is the project layout acceptance test suite - justify your answer with a concrete production example.
**A:** Verify build, run unit tests, render a small golden image, run a tiny movie, and check hashes - all automated in project layout CI. A concrete example: consistently applying project layout in code review and regression tests keeps the whole pipeline trustworthy.

## Q77: How does project layout select rendering parameters - justify your answer with a concrete production example.
**A:** Defaults live in config files with ranges; project layout records effective parameters in the output metadata for every render. A concrete example: consistently applying project layout in code review and regression tests keeps the whole pipeline trustworthy.

## Q78: What is project layout two-tier testing - justify your answer with a concrete production example.
**A:** Fast smoke tests on every commit plus full-scale golden renders nightly; project layout balances speed against coverage. A concrete example: consistently applying project layout in code review and regression tests keeps the whole pipeline trustworthy.

## Q79: How does project layout handle GPU-specific bugs - justify your answer with a concrete production example.
**A:** Reproduce on the reference CPU path and bisect parameters; project layout isolates hardware issues from logic issues by identical interfaces. A concrete example: consistently applying project layout in code review and regression tests keeps the whole pipeline trustworthy.

## Q80: What does project layout require before a release - justify your answer with a concrete production example.
**A:** Clean checkout builds, tests pass, golden images regenerated deliberately, and a versioned changelog; after that project layout is releasable. A concrete example: consistently applying project layout in code review and regression tests keeps the whole pipeline trustworthy.

## Q81: How does project layout inherit good practices from research code - justify your answer with a concrete production example.
**A:** Every paper figure must be reproducible; project layout enforces the same discipline with stored parameters and hashed inputs. A concrete example: consistently applying project layout in code review and regression tests keeps the whole pipeline trustworthy.

## Q82: What is the role of project layout code review - justify your answer with a concrete production example.
**A:** Catch numeric and architecture mistakes early; project layout review checklist includes dimension checks, tolerance choices, and unit conventions. A concrete example: consistently applying project layout in code review and regression tests keeps the whole pipeline trustworthy.

## Q83: How is project layout balanced against research freedom - justify your answer with a concrete production example.
**A:** Experiments go in branches; the mainline stays green behind project layout gates so nothing is ever rendered from a broken tree. A concrete example: consistently applying project layout in code review and regression tests keeps the whole pipeline trustworthy.

## Q84: What is the final measure of project layout success - justify your answer with a concrete production example.
**A:** A fresh checkout reproduces published images in a known time, letting anyone extend the work - that is production-grade project layout. A concrete example: consistently applying project layout in code review and regression tests keeps the whole pipeline trustworthy.

## Q85: What is the final measure of project layout success - justify your answer with a concrete production example.
**A:** A fresh checkout reproduces published images in a known time, letting anyone extend the work - that is production-grade project layout. A concrete example: consistently applying project layout in code review and regression tests keeps the whole pipeline trustworthy.

## Q86: How is project layout balanced against research freedom - justify your answer with a concrete production example.
**A:** Experiments go in branches; the mainline stays green behind project layout gates so nothing is ever rendered from a broken tree. A concrete example: consistently applying project layout in code review and regression tests keeps the whole pipeline trustworthy.

## Q87: What is the role of project layout code review - justify your answer with a concrete production example.
**A:** Catch numeric and architecture mistakes early; project layout review checklist includes dimension checks, tolerance choices, and unit conventions. A concrete example: consistently applying project layout in code review and regression tests keeps the whole pipeline trustworthy.

## Q88: How does project layout inherit good practices from research code - justify your answer with a concrete production example.
**A:** Every paper figure must be reproducible; project layout enforces the same discipline with stored parameters and hashed inputs. A concrete example: consistently applying project layout in code review and regression tests keeps the whole pipeline trustworthy.

## Q89: What does project layout require before a release - justify your answer with a concrete production example.
**A:** Clean checkout builds, tests pass, golden images regenerated deliberately, and a versioned changelog; after that project layout is releasable. A concrete example: consistently applying project layout in code review and regression tests keeps the whole pipeline trustworthy.

## Q90: How does project layout handle GPU-specific bugs - justify your answer with a concrete production example.
**A:** Reproduce on the reference CPU path and bisect parameters; project layout isolates hardware issues from logic issues by identical interfaces. A concrete example: consistently applying project layout in code review and regression tests keeps the whole pipeline trustworthy.

## Q91: What is project layout two-tier testing - justify your answer with a concrete production example.
**A:** Fast smoke tests on every commit plus full-scale golden renders nightly; project layout balances speed against coverage. A concrete example: consistently applying project layout in code review and regression tests keeps the whole pipeline trustworthy.

## Q92: How does project layout select rendering parameters - justify your answer with a concrete production example.
**A:** Defaults live in config files with ranges; project layout records effective parameters in the output metadata for every render. A concrete example: consistently applying project layout in code review and regression tests keeps the whole pipeline trustworthy.

## Q93: What is the project layout acceptance test suite - justify your answer with a concrete production example.
**A:** Verify build, run unit tests, render a small golden image, run a tiny movie, and check hashes - all automated in project layout CI. A concrete example: consistently applying project layout in code review and regression tests keeps the whole pipeline trustworthy.

## Q94: How does project layout ensure portability - justify your answer with a concrete production example.
**A:** Optional CUDA paths with CPU fallbacks and hardware queries; project layout runs on laptops and clusters with the same command line. A concrete example: consistently applying project layout in code review and regression tests keeps the whole pipeline trustworthy.

## Q95: What is project layout quality-of-life - justify your answer with a concrete production example.
**A:** Fast debug renders at low resolution, hot-reloaded config, and a progress bar - project layout makes iteration pleasant enough to be productive. A concrete example: consistently applying project layout in code review and regression tests keeps the whole pipeline trustworthy.

## Q96: How does project layout approach documentation - justify your answer with a concrete production example.
**A:** A README per stage, a one-page architecture diagram, and a changelog; project layout documentation is updated with the code it explains. A concrete example: consistently applying project layout in code review and regression tests keeps the whole pipeline trustworthy.

## Q97: What does project layout do for performance budgeting - justify your answer with a concrete production example.
**A:** Records time per frame phase (import, trace, post) and asserts budgets; project layout finds regressions before users notice them. A concrete example: consistently applying project layout in code review and regression tests keeps the whole pipeline trustworthy.

## Q98: How does project layout make a movie - justify your answer with a concrete production example.
**A:** Render each frame to an image file, then encode with ffmpeg using a fixed color pipeline; project layout encodes losslessly first, then to final. A concrete example: consistently applying project layout in code review and regression tests keeps the whole pipeline trustworthy.

## Q99: What logging does project layout produce - justify your answer with a concrete production example.
**A:** Progress per frame, step stats per region, and warnings for unphysical states; project layout logs are written to machine-parseable format. A concrete example: consistently applying project layout in code review and regression tests keeps the whole pipeline trustworthy.

## Q100: How does project layout manage data files - justify your answer with a concrete production example.
**A:** Version registers, snapshot metadata, and hash checks before rendering so project layout always knows exactly which data made the image. A concrete example: consistently applying project layout in code review and regression tests keeps the whole pipeline trustworthy.
