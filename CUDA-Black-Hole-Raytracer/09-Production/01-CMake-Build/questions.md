# Production — Cmake Build Interview Questions and Answers

## Q1: What is the CMake build structure for the project?
**A:** A modern CMake project: SBMA root, target(s) for the CUDA raytracer library and CLI, plus optional bindings and tests - with CUDA/NVIDIA flags isolated in one settings file.

## Q2: How do you configure CUDA support in CMake?
**A:** enable_language(CUDA), find_package(CUDAToolkit), set CMAKE_CUDA_STANDARD=17, and per-target CUDA_ARCHITECTURES - the proper way to target GPUs without hard-coded -arch.

## Q3: What is the release build layout?
**A:** Single CMake (not recursed) with subdirectories: src/ (raytracer lib), tools/ (cli), utils/ (converters), tests/, plus examples/ - each a small add_library target.

## Q4: What are the compiler flags for the kernels?
**A:** CMAKE_CUDA_FLAGS_RELEASE with -O3 and -use_fast_math for the render paths, but a fat default flag set that stays deterministic (no aggressive FP contraction surprises).

## Q5: How do you enforce a consistent FP contract?
**A:** Pass -ffp-contract=off (or override with explicit fma) so floating point is bit-exact across runs and compilers - the reproducibility contract at compile time.

## Q6: What is a 'relocatable device code' need?
**A:** Unless you use separately-compiled device kernels, keep them in the same translation unit (relocatable device code off); for multi-object device linkage set CUDA_SEPARABLE_COMPILATION as needed to keep the binary coherent.

## Q7: How do you keep GPU architectures portable?
**A:** CMAKE_CUDA_ARCHITECTURES lists e.g, 86;89;90;: set via a cache variable and only compile-for-the-host's GPU in local dev ('native').

## Q8: What does find_package(CUDAToolkit) enable?
**A:** Detection of the toolkit's nvcc/ptxas versions and headers/libraries - a single canonical place for the CUDA dependency, including the host-side libs.

## Q9: What are the ctest hooks?
**A:** add_test() over the golden tests (analytic validation, convergence, determinism) wired to ctest - `ctest` becomes the project's entrance test command.

## Q10: How do you version and package?
**A:** project(VERSION) + CPack or a simple install(TARGETS) rule; the version string flows into the CLI --version and into every log/render's metadata.

## Q11: What is the developer loop?
**A:** cmake --build build -j --target ray-cli && ctest --test-dir build -R validation - the two-command loop that keeps engineering productive.

## Q12: What are the pitfalls of stale binary caches?
**A:** GC cache and CUDA_ARCHITECTURES changes need a fresh configure; document 'delete build when changing arch' in the README.

## Q13: What is the summary?
**A:** A modern CMake build = CUDA-as-first-class language, arch-cached targets, deterministic FP flags, ctest golden suite, and a two-command dev loop.

## Q14: Why does cmake build matter for a research raytracer?
**A:** Because the tool must be reproducible, testable, and maintainable for months of tuning; cmake build turns a script into a reliable product.

## Q15: What does cmake build guarantee in a CI pipeline?
**A:** Every change builds, the golden images still match, and performance did not regress; cmake build automation protects the project from careless commits.

## Q16: How does cmake build structure code for tests?
**A:** Pure functions with injected parameters, golden-image comparisons, and analytic fixtures; cmake build makes kernels unit-testable on the host.

## Q17: What is the role of cmake build configuration?
**A:** Camera pose, metric, integrator, resolution, and data paths become CLI/JSON inputs so cmake build runs are documented by their arguments.

## Q18: How does cmake build handle environment variability?
**A:** CMake + containers pin compilers and CUDA versions; cmake build reproducibility starts with a deterministic build environment.

## Q19: What does cmake build add to the learning process?
**A:** Small milestones with acceptance criteria turn 'make an image' into 'make a trustworthy image'; cmake build is how you actually finish.

## Q20: How is cmake build validated numerically?
**A:** Against analytic Schwarzschild results and conserved-quantity drift checks before any visual tuning; cmake build correctness precedes beauty.

## Q21: What is a reasonable cmake build schedule?
**A:** Physics validation first, single frame next, movie pipeline last; cmake build ordering prevents rework when physics changes.

## Q22: How does cmake build manage data files?
**A:** Version registers, snapshot metadata, and hash checks before rendering so cmake build always knows exactly which data made the image.

## Q23: What logging does cmake build produce?
**A:** Progress per frame, step stats per region, and warnings for unphysical states; cmake build logs are written to machine-parseable format.

## Q24: How does cmake build make a movie?
**A:** Render each frame to an image file, then encode with ffmpeg using a fixed color pipeline; cmake build encodes losslessly first, then to final.

## Q25: What does cmake build do for performance budgeting?
**A:** Records time per frame phase (import, trace, post) and asserts budgets; cmake build finds regressions before users notice them.

## Q26: How does cmake build approach documentation?
**A:** A README per stage, a one-page architecture diagram, and a changelog; cmake build documentation is updated with the code it explains.

## Q27: What is cmake build quality-of-life?
**A:** Fast debug renders at low resolution, hot-reloaded config, and a progress bar - cmake build makes iteration pleasant enough to be productive.

## Q28: How does cmake build ensure portability?
**A:** Optional CUDA paths with CPU fallbacks and hardware queries; cmake build runs on laptops and clusters with the same command line.

## Q29: What is the cmake build acceptance test suite?
**A:** Verify build, run unit tests, render a small golden image, run a tiny movie, and check hashes - all automated in cmake build CI.

## Q30: How does cmake build select rendering parameters?
**A:** Defaults live in config files with ranges; cmake build records effective parameters in the output metadata for every render.

## Q31: What is cmake build two-tier testing?
**A:** Fast smoke tests on every commit plus full-scale golden renders nightly; cmake build balances speed against coverage.

## Q32: How does cmake build handle GPU-specific bugs?
**A:** Reproduce on the reference CPU path and bisect parameters; cmake build isolates hardware issues from logic issues by identical interfaces.

## Q33: What does cmake build require before a release?
**A:** Clean checkout builds, tests pass, golden images regenerated deliberately, and a versioned changelog; after that cmake build is releasable.

## Q34: How does cmake build inherit good practices from research code?
**A:** Every paper figure must be reproducible; cmake build enforces the same discipline with stored parameters and hashed inputs.

## Q35: What is the role of cmake build code review?
**A:** Catch numeric and architecture mistakes early; cmake build review checklist includes dimension checks, tolerance choices, and unit conventions.

## Q36: How is cmake build balanced against research freedom?
**A:** Experiments go in branches; the mainline stays green behind cmake build gates so nothing is ever rendered from a broken tree.

## Q37: What is the final measure of cmake build success?
**A:** A fresh checkout reproduces published images in a known time, letting anyone extend the work - that is production-grade cmake build.

## Q38: What is the final measure of cmake build success - justify your answer with a concrete production example.
**A:** A fresh checkout reproduces published images in a known time, letting anyone extend the work - that is production-grade cmake build. A concrete example: consistently applying cmake build in code review and regression tests keeps the whole pipeline trustworthy.

## Q39: How is cmake build balanced against research freedom - justify your answer with a concrete production example.
**A:** Experiments go in branches; the mainline stays green behind cmake build gates so nothing is ever rendered from a broken tree. A concrete example: consistently applying cmake build in code review and regression tests keeps the whole pipeline trustworthy.

## Q40: What is the role of cmake build code review - justify your answer with a concrete production example.
**A:** Catch numeric and architecture mistakes early; cmake build review checklist includes dimension checks, tolerance choices, and unit conventions. A concrete example: consistently applying cmake build in code review and regression tests keeps the whole pipeline trustworthy.

## Q41: How does cmake build inherit good practices from research code - justify your answer with a concrete production example.
**A:** Every paper figure must be reproducible; cmake build enforces the same discipline with stored parameters and hashed inputs. A concrete example: consistently applying cmake build in code review and regression tests keeps the whole pipeline trustworthy.

## Q42: What does cmake build require before a release - justify your answer with a concrete production example.
**A:** Clean checkout builds, tests pass, golden images regenerated deliberately, and a versioned changelog; after that cmake build is releasable. A concrete example: consistently applying cmake build in code review and regression tests keeps the whole pipeline trustworthy.

## Q43: How does cmake build handle GPU-specific bugs - justify your answer with a concrete production example.
**A:** Reproduce on the reference CPU path and bisect parameters; cmake build isolates hardware issues from logic issues by identical interfaces. A concrete example: consistently applying cmake build in code review and regression tests keeps the whole pipeline trustworthy.

## Q44: What is cmake build two-tier testing - justify your answer with a concrete production example.
**A:** Fast smoke tests on every commit plus full-scale golden renders nightly; cmake build balances speed against coverage. A concrete example: consistently applying cmake build in code review and regression tests keeps the whole pipeline trustworthy.

## Q45: How does cmake build select rendering parameters - justify your answer with a concrete production example.
**A:** Defaults live in config files with ranges; cmake build records effective parameters in the output metadata for every render. A concrete example: consistently applying cmake build in code review and regression tests keeps the whole pipeline trustworthy.

## Q46: What is the cmake build acceptance test suite - justify your answer with a concrete production example.
**A:** Verify build, run unit tests, render a small golden image, run a tiny movie, and check hashes - all automated in cmake build CI. A concrete example: consistently applying cmake build in code review and regression tests keeps the whole pipeline trustworthy.

## Q47: How does cmake build ensure portability - justify your answer with a concrete production example.
**A:** Optional CUDA paths with CPU fallbacks and hardware queries; cmake build runs on laptops and clusters with the same command line. A concrete example: consistently applying cmake build in code review and regression tests keeps the whole pipeline trustworthy.

## Q48: What is cmake build quality-of-life - justify your answer with a concrete production example.
**A:** Fast debug renders at low resolution, hot-reloaded config, and a progress bar - cmake build makes iteration pleasant enough to be productive. A concrete example: consistently applying cmake build in code review and regression tests keeps the whole pipeline trustworthy.

## Q49: How does cmake build approach documentation - justify your answer with a concrete production example.
**A:** A README per stage, a one-page architecture diagram, and a changelog; cmake build documentation is updated with the code it explains. A concrete example: consistently applying cmake build in code review and regression tests keeps the whole pipeline trustworthy.

## Q50: What does cmake build do for performance budgeting - justify your answer with a concrete production example.
**A:** Records time per frame phase (import, trace, post) and asserts budgets; cmake build finds regressions before users notice them. A concrete example: consistently applying cmake build in code review and regression tests keeps the whole pipeline trustworthy.

## Q51: How does cmake build make a movie - justify your answer with a concrete production example.
**A:** Render each frame to an image file, then encode with ffmpeg using a fixed color pipeline; cmake build encodes losslessly first, then to final. A concrete example: consistently applying cmake build in code review and regression tests keeps the whole pipeline trustworthy.

## Q52: What logging does cmake build produce - justify your answer with a concrete production example.
**A:** Progress per frame, step stats per region, and warnings for unphysical states; cmake build logs are written to machine-parseable format. A concrete example: consistently applying cmake build in code review and regression tests keeps the whole pipeline trustworthy.

## Q53: How does cmake build manage data files - justify your answer with a concrete production example.
**A:** Version registers, snapshot metadata, and hash checks before rendering so cmake build always knows exactly which data made the image. A concrete example: consistently applying cmake build in code review and regression tests keeps the whole pipeline trustworthy.

## Q54: What is a reasonable cmake build schedule - justify your answer with a concrete production example.
**A:** Physics validation first, single frame next, movie pipeline last; cmake build ordering prevents rework when physics changes. A concrete example: consistently applying cmake build in code review and regression tests keeps the whole pipeline trustworthy.

## Q55: How is cmake build validated numerically - justify your answer with a concrete production example.
**A:** Against analytic Schwarzschild results and conserved-quantity drift checks before any visual tuning; cmake build correctness precedes beauty. A concrete example: consistently applying cmake build in code review and regression tests keeps the whole pipeline trustworthy.

## Q56: What does cmake build add to the learning process - justify your answer with a concrete production example.
**A:** Small milestones with acceptance criteria turn 'make an image' into 'make a trustworthy image'; cmake build is how you actually finish. A concrete example: consistently applying cmake build in code review and regression tests keeps the whole pipeline trustworthy.

## Q57: How does cmake build handle environment variability - justify your answer with a concrete production example.
**A:** CMake + containers pin compilers and CUDA versions; cmake build reproducibility starts with a deterministic build environment. A concrete example: consistently applying cmake build in code review and regression tests keeps the whole pipeline trustworthy.

## Q58: What is the role of cmake build configuration - justify your answer with a concrete production example.
**A:** Camera pose, metric, integrator, resolution, and data paths become CLI/JSON inputs so cmake build runs are documented by their arguments. A concrete example: consistently applying cmake build in code review and regression tests keeps the whole pipeline trustworthy.

## Q59: How does cmake build structure code for tests - justify your answer with a concrete production example.
**A:** Pure functions with injected parameters, golden-image comparisons, and analytic fixtures; cmake build makes kernels unit-testable on the host. A concrete example: consistently applying cmake build in code review and regression tests keeps the whole pipeline trustworthy.

## Q60: What does cmake build guarantee in a CI pipeline - justify your answer with a concrete production example.
**A:** Every change builds, the golden images still match, and performance did not regress; cmake build automation protects the project from careless commits. A concrete example: consistently applying cmake build in code review and regression tests keeps the whole pipeline trustworthy.

## Q61: Why does cmake build matter for a research raytracer - justify your answer with a concrete production example.
**A:** Because the tool must be reproducible, testable, and maintainable for months of tuning; cmake build turns a script into a reliable product. A concrete example: consistently applying cmake build in code review and regression tests keeps the whole pipeline trustworthy.

## Q62: Why does cmake build matter for a research raytracer - justify your answer with a concrete production example.
**A:** Because the tool must be reproducible, testable, and maintainable for months of tuning; cmake build turns a script into a reliable product. A concrete example: consistently applying cmake build in code review and regression tests keeps the whole pipeline trustworthy.

## Q63: What does cmake build guarantee in a CI pipeline - justify your answer with a concrete production example.
**A:** Every change builds, the golden images still match, and performance did not regress; cmake build automation protects the project from careless commits. A concrete example: consistently applying cmake build in code review and regression tests keeps the whole pipeline trustworthy.

## Q64: How does cmake build structure code for tests - justify your answer with a concrete production example.
**A:** Pure functions with injected parameters, golden-image comparisons, and analytic fixtures; cmake build makes kernels unit-testable on the host. A concrete example: consistently applying cmake build in code review and regression tests keeps the whole pipeline trustworthy.

## Q65: What is the role of cmake build configuration - justify your answer with a concrete production example.
**A:** Camera pose, metric, integrator, resolution, and data paths become CLI/JSON inputs so cmake build runs are documented by their arguments. A concrete example: consistently applying cmake build in code review and regression tests keeps the whole pipeline trustworthy.

## Q66: How does cmake build handle environment variability - justify your answer with a concrete production example.
**A:** CMake + containers pin compilers and CUDA versions; cmake build reproducibility starts with a deterministic build environment. A concrete example: consistently applying cmake build in code review and regression tests keeps the whole pipeline trustworthy.

## Q67: What does cmake build add to the learning process - justify your answer with a concrete production example.
**A:** Small milestones with acceptance criteria turn 'make an image' into 'make a trustworthy image'; cmake build is how you actually finish. A concrete example: consistently applying cmake build in code review and regression tests keeps the whole pipeline trustworthy.

## Q68: How is cmake build validated numerically - justify your answer with a concrete production example.
**A:** Against analytic Schwarzschild results and conserved-quantity drift checks before any visual tuning; cmake build correctness precedes beauty. A concrete example: consistently applying cmake build in code review and regression tests keeps the whole pipeline trustworthy.

## Q69: What is a reasonable cmake build schedule - justify your answer with a concrete production example.
**A:** Physics validation first, single frame next, movie pipeline last; cmake build ordering prevents rework when physics changes. A concrete example: consistently applying cmake build in code review and regression tests keeps the whole pipeline trustworthy.

## Q70: How does cmake build manage data files - justify your answer with a concrete production example.
**A:** Version registers, snapshot metadata, and hash checks before rendering so cmake build always knows exactly which data made the image. A concrete example: consistently applying cmake build in code review and regression tests keeps the whole pipeline trustworthy.

## Q71: What logging does cmake build produce - justify your answer with a concrete production example.
**A:** Progress per frame, step stats per region, and warnings for unphysical states; cmake build logs are written to machine-parseable format. A concrete example: consistently applying cmake build in code review and regression tests keeps the whole pipeline trustworthy.

## Q72: How does cmake build make a movie - justify your answer with a concrete production example.
**A:** Render each frame to an image file, then encode with ffmpeg using a fixed color pipeline; cmake build encodes losslessly first, then to final. A concrete example: consistently applying cmake build in code review and regression tests keeps the whole pipeline trustworthy.

## Q73: What does cmake build do for performance budgeting - justify your answer with a concrete production example.
**A:** Records time per frame phase (import, trace, post) and asserts budgets; cmake build finds regressions before users notice them. A concrete example: consistently applying cmake build in code review and regression tests keeps the whole pipeline trustworthy.

## Q74: How does cmake build approach documentation - justify your answer with a concrete production example.
**A:** A README per stage, a one-page architecture diagram, and a changelog; cmake build documentation is updated with the code it explains. A concrete example: consistently applying cmake build in code review and regression tests keeps the whole pipeline trustworthy.

## Q75: What is cmake build quality-of-life - justify your answer with a concrete production example.
**A:** Fast debug renders at low resolution, hot-reloaded config, and a progress bar - cmake build makes iteration pleasant enough to be productive. A concrete example: consistently applying cmake build in code review and regression tests keeps the whole pipeline trustworthy.

## Q76: How does cmake build ensure portability - justify your answer with a concrete production example.
**A:** Optional CUDA paths with CPU fallbacks and hardware queries; cmake build runs on laptops and clusters with the same command line. A concrete example: consistently applying cmake build in code review and regression tests keeps the whole pipeline trustworthy.

## Q77: What is the cmake build acceptance test suite - justify your answer with a concrete production example.
**A:** Verify build, run unit tests, render a small golden image, run a tiny movie, and check hashes - all automated in cmake build CI. A concrete example: consistently applying cmake build in code review and regression tests keeps the whole pipeline trustworthy.

## Q78: How does cmake build select rendering parameters - justify your answer with a concrete production example.
**A:** Defaults live in config files with ranges; cmake build records effective parameters in the output metadata for every render. A concrete example: consistently applying cmake build in code review and regression tests keeps the whole pipeline trustworthy.

## Q79: What is cmake build two-tier testing - justify your answer with a concrete production example.
**A:** Fast smoke tests on every commit plus full-scale golden renders nightly; cmake build balances speed against coverage. A concrete example: consistently applying cmake build in code review and regression tests keeps the whole pipeline trustworthy.

## Q80: How does cmake build handle GPU-specific bugs - justify your answer with a concrete production example.
**A:** Reproduce on the reference CPU path and bisect parameters; cmake build isolates hardware issues from logic issues by identical interfaces. A concrete example: consistently applying cmake build in code review and regression tests keeps the whole pipeline trustworthy.

## Q81: What does cmake build require before a release - justify your answer with a concrete production example.
**A:** Clean checkout builds, tests pass, golden images regenerated deliberately, and a versioned changelog; after that cmake build is releasable. A concrete example: consistently applying cmake build in code review and regression tests keeps the whole pipeline trustworthy.

## Q82: How does cmake build inherit good practices from research code - justify your answer with a concrete production example.
**A:** Every paper figure must be reproducible; cmake build enforces the same discipline with stored parameters and hashed inputs. A concrete example: consistently applying cmake build in code review and regression tests keeps the whole pipeline trustworthy.

## Q83: What is the role of cmake build code review - justify your answer with a concrete production example.
**A:** Catch numeric and architecture mistakes early; cmake build review checklist includes dimension checks, tolerance choices, and unit conventions. A concrete example: consistently applying cmake build in code review and regression tests keeps the whole pipeline trustworthy.

## Q84: How is cmake build balanced against research freedom - justify your answer with a concrete production example.
**A:** Experiments go in branches; the mainline stays green behind cmake build gates so nothing is ever rendered from a broken tree. A concrete example: consistently applying cmake build in code review and regression tests keeps the whole pipeline trustworthy.

## Q85: What is the final measure of cmake build success - justify your answer with a concrete production example.
**A:** A fresh checkout reproduces published images in a known time, letting anyone extend the work - that is production-grade cmake build. A concrete example: consistently applying cmake build in code review and regression tests keeps the whole pipeline trustworthy.

## Q86: What is the final measure of cmake build success - justify your answer with a concrete production example.
**A:** A fresh checkout reproduces published images in a known time, letting anyone extend the work - that is production-grade cmake build. A concrete example: consistently applying cmake build in code review and regression tests keeps the whole pipeline trustworthy.

## Q87: How is cmake build balanced against research freedom - justify your answer with a concrete production example.
**A:** Experiments go in branches; the mainline stays green behind cmake build gates so nothing is ever rendered from a broken tree. A concrete example: consistently applying cmake build in code review and regression tests keeps the whole pipeline trustworthy.

## Q88: What is the role of cmake build code review - justify your answer with a concrete production example.
**A:** Catch numeric and architecture mistakes early; cmake build review checklist includes dimension checks, tolerance choices, and unit conventions. A concrete example: consistently applying cmake build in code review and regression tests keeps the whole pipeline trustworthy.

## Q89: How does cmake build inherit good practices from research code - justify your answer with a concrete production example.
**A:** Every paper figure must be reproducible; cmake build enforces the same discipline with stored parameters and hashed inputs. A concrete example: consistently applying cmake build in code review and regression tests keeps the whole pipeline trustworthy.

## Q90: What does cmake build require before a release - justify your answer with a concrete production example.
**A:** Clean checkout builds, tests pass, golden images regenerated deliberately, and a versioned changelog; after that cmake build is releasable. A concrete example: consistently applying cmake build in code review and regression tests keeps the whole pipeline trustworthy.

## Q91: How does cmake build handle GPU-specific bugs - justify your answer with a concrete production example.
**A:** Reproduce on the reference CPU path and bisect parameters; cmake build isolates hardware issues from logic issues by identical interfaces. A concrete example: consistently applying cmake build in code review and regression tests keeps the whole pipeline trustworthy.

## Q92: What is cmake build two-tier testing - justify your answer with a concrete production example.
**A:** Fast smoke tests on every commit plus full-scale golden renders nightly; cmake build balances speed against coverage. A concrete example: consistently applying cmake build in code review and regression tests keeps the whole pipeline trustworthy.

## Q93: How does cmake build select rendering parameters - justify your answer with a concrete production example.
**A:** Defaults live in config files with ranges; cmake build records effective parameters in the output metadata for every render. A concrete example: consistently applying cmake build in code review and regression tests keeps the whole pipeline trustworthy.

## Q94: What is the cmake build acceptance test suite - justify your answer with a concrete production example.
**A:** Verify build, run unit tests, render a small golden image, run a tiny movie, and check hashes - all automated in cmake build CI. A concrete example: consistently applying cmake build in code review and regression tests keeps the whole pipeline trustworthy.

## Q95: How does cmake build ensure portability - justify your answer with a concrete production example.
**A:** Optional CUDA paths with CPU fallbacks and hardware queries; cmake build runs on laptops and clusters with the same command line. A concrete example: consistently applying cmake build in code review and regression tests keeps the whole pipeline trustworthy.

## Q96: What is cmake build quality-of-life - justify your answer with a concrete production example.
**A:** Fast debug renders at low resolution, hot-reloaded config, and a progress bar - cmake build makes iteration pleasant enough to be productive. A concrete example: consistently applying cmake build in code review and regression tests keeps the whole pipeline trustworthy.

## Q97: How does cmake build approach documentation - justify your answer with a concrete production example.
**A:** A README per stage, a one-page architecture diagram, and a changelog; cmake build documentation is updated with the code it explains. A concrete example: consistently applying cmake build in code review and regression tests keeps the whole pipeline trustworthy.

## Q98: What does cmake build do for performance budgeting - justify your answer with a concrete production example.
**A:** Records time per frame phase (import, trace, post) and asserts budgets; cmake build finds regressions before users notice them. A concrete example: consistently applying cmake build in code review and regression tests keeps the whole pipeline trustworthy.

## Q99: How does cmake build make a movie - justify your answer with a concrete production example.
**A:** Render each frame to an image file, then encode with ffmpeg using a fixed color pipeline; cmake build encodes losslessly first, then to final. A concrete example: consistently applying cmake build in code review and regression tests keeps the whole pipeline trustworthy.

## Q100: What logging does cmake build produce - justify your answer with a concrete production example.
**A:** Progress per frame, step stats per region, and warnings for unphysical states; cmake build logs are written to machine-parseable format. A concrete example: consistently applying cmake build in code review and regression tests keeps the whole pipeline trustworthy.
