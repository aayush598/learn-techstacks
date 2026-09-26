# Production — Reproducibility Interview Questions and Answers

## Q1: What does reproducibility mean for a renderer?
**A:** The same version, input snapshot, config, and seed produce bit-identical frames on the same hardware - the scientist's trust contract.

## Q2: What is the nondeterminism budget?
**A:** Thread order (reductions, atomics), FP associative reordering, and driver/library version drift - each must be explicitly controlled or documented.

## Q3: How do you control thread-order variance?
**A:** Pin the reduction tree order (a defined index order), launch grids deterministically, and avoid order-dependent atomics in accumulation.

## Q4: How do you pin floating-point?
**A:** Fixed --ffp-contract / explicit-fma policy, no fast-math on the reproducible path, and a determinism test per build.

## Q5: What is the version-hash metadata?
**A:** Every output records git-hash, binary EXIF-ish stamp, CUDA runtime, driver, and the config hash - an audit trail without a special file manifest.

## Q6: What is the input pinning?
**A:** Store the snapshot's checksum + the converter version in the scene record - the 'what exact data' part of reproducibility.

## Q7: Why separate GPU determinism from CPU-determinism?
**A:** Different GPUs have different transcendental accuracy; the guarantee is per-GPU-bit-exact + cross-GPU-agrees-to-tolerance - state it explicitly.

## Q8: What is a golden regression?
**A:** Version-coded expected hashes for the analytic scenes - if a legitimate physics change bumps them, the golden file is reviewed and re-pinned.

## Q9: How do you reproduce a third-party run?
**A:** Ship the exact command from the run-id's record: bin same hash, config same, seed same - a colleague re-runs and diff-bits match.

## Q10: What is the summary?
**A:** Reproducibility = pinned seed/order/FP/version/input, captured in metadata, enforced by a determinism gate — the difference between imagery and evidence.

## Q11: Why does reproducibility matter for a research raytracer?
**A:** Because the tool must be reproducible, testable, and maintainable for months of tuning; reproducibility turns a script into a reliable product.

## Q12: What does reproducibility guarantee in a CI pipeline?
**A:** Every change builds, the golden images still match, and performance did not regress; reproducibility automation protects the project from careless commits.

## Q13: How does reproducibility structure code for tests?
**A:** Pure functions with injected parameters, golden-image comparisons, and analytic fixtures; reproducibility makes kernels unit-testable on the host.

## Q14: What is the role of reproducibility configuration?
**A:** Camera pose, metric, integrator, resolution, and data paths become CLI/JSON inputs so reproducibility runs are documented by their arguments.

## Q15: How does reproducibility handle environment variability?
**A:** CMake + containers pin compilers and CUDA versions; reproducibility reproducibility starts with a deterministic build environment.

## Q16: What does reproducibility add to the learning process?
**A:** Small milestones with acceptance criteria turn 'make an image' into 'make a trustworthy image'; reproducibility is how you actually finish.

## Q17: How is reproducibility validated numerically?
**A:** Against analytic Schwarzschild results and conserved-quantity drift checks before any visual tuning; reproducibility correctness precedes beauty.

## Q18: What is a reasonable reproducibility schedule?
**A:** Physics validation first, single frame next, movie pipeline last; reproducibility ordering prevents rework when physics changes.

## Q19: How does reproducibility manage data files?
**A:** Version registers, snapshot metadata, and hash checks before rendering so reproducibility always knows exactly which data made the image.

## Q20: What logging does reproducibility produce?
**A:** Progress per frame, step stats per region, and warnings for unphysical states; reproducibility logs are written to machine-parseable format.

## Q21: How does reproducibility make a movie?
**A:** Render each frame to an image file, then encode with ffmpeg using a fixed color pipeline; reproducibility encodes losslessly first, then to final.

## Q22: What does reproducibility do for performance budgeting?
**A:** Records time per frame phase (import, trace, post) and asserts budgets; reproducibility finds regressions before users notice them.

## Q23: How does reproducibility approach documentation?
**A:** A README per stage, a one-page architecture diagram, and a changelog; reproducibility documentation is updated with the code it explains.

## Q24: What is reproducibility quality-of-life?
**A:** Fast debug renders at low resolution, hot-reloaded config, and a progress bar - reproducibility makes iteration pleasant enough to be productive.

## Q25: How does reproducibility ensure portability?
**A:** Optional CUDA paths with CPU fallbacks and hardware queries; reproducibility runs on laptops and clusters with the same command line.

## Q26: What is the reproducibility acceptance test suite?
**A:** Verify build, run unit tests, render a small golden image, run a tiny movie, and check hashes - all automated in reproducibility CI.

## Q27: How does reproducibility select rendering parameters?
**A:** Defaults live in config files with ranges; reproducibility records effective parameters in the output metadata for every render.

## Q28: What is reproducibility two-tier testing?
**A:** Fast smoke tests on every commit plus full-scale golden renders nightly; reproducibility balances speed against coverage.

## Q29: How does reproducibility handle GPU-specific bugs?
**A:** Reproduce on the reference CPU path and bisect parameters; reproducibility isolates hardware issues from logic issues by identical interfaces.

## Q30: What does reproducibility require before a release?
**A:** Clean checkout builds, tests pass, golden images regenerated deliberately, and a versioned changelog; after that reproducibility is releasable.

## Q31: How does reproducibility inherit good practices from research code?
**A:** Every paper figure must be reproducible; reproducibility enforces the same discipline with stored parameters and hashed inputs.

## Q32: What is the role of reproducibility code review?
**A:** Catch numeric and architecture mistakes early; reproducibility review checklist includes dimension checks, tolerance choices, and unit conventions.

## Q33: How is reproducibility balanced against research freedom?
**A:** Experiments go in branches; the mainline stays green behind reproducibility gates so nothing is ever rendered from a broken tree.

## Q34: What is the final measure of reproducibility success?
**A:** A fresh checkout reproduces published images in a known time, letting anyone extend the work - that is production-grade reproducibility.

## Q35: What is the final measure of reproducibility success - justify your answer with a concrete production example.
**A:** A fresh checkout reproduces published images in a known time, letting anyone extend the work - that is production-grade reproducibility. A concrete example: consistently applying reproducibility in code review and regression tests keeps the whole pipeline trustworthy.

## Q36: How is reproducibility balanced against research freedom - justify your answer with a concrete production example.
**A:** Experiments go in branches; the mainline stays green behind reproducibility gates so nothing is ever rendered from a broken tree. A concrete example: consistently applying reproducibility in code review and regression tests keeps the whole pipeline trustworthy.

## Q37: What is the role of reproducibility code review - justify your answer with a concrete production example.
**A:** Catch numeric and architecture mistakes early; reproducibility review checklist includes dimension checks, tolerance choices, and unit conventions. A concrete example: consistently applying reproducibility in code review and regression tests keeps the whole pipeline trustworthy.

## Q38: How does reproducibility inherit good practices from research code - justify your answer with a concrete production example.
**A:** Every paper figure must be reproducible; reproducibility enforces the same discipline with stored parameters and hashed inputs. A concrete example: consistently applying reproducibility in code review and regression tests keeps the whole pipeline trustworthy.

## Q39: What does reproducibility require before a release - justify your answer with a concrete production example.
**A:** Clean checkout builds, tests pass, golden images regenerated deliberately, and a versioned changelog; after that reproducibility is releasable. A concrete example: consistently applying reproducibility in code review and regression tests keeps the whole pipeline trustworthy.

## Q40: How does reproducibility handle GPU-specific bugs - justify your answer with a concrete production example.
**A:** Reproduce on the reference CPU path and bisect parameters; reproducibility isolates hardware issues from logic issues by identical interfaces. A concrete example: consistently applying reproducibility in code review and regression tests keeps the whole pipeline trustworthy.

## Q41: What is reproducibility two-tier testing - justify your answer with a concrete production example.
**A:** Fast smoke tests on every commit plus full-scale golden renders nightly; reproducibility balances speed against coverage. A concrete example: consistently applying reproducibility in code review and regression tests keeps the whole pipeline trustworthy.

## Q42: How does reproducibility select rendering parameters - justify your answer with a concrete production example.
**A:** Defaults live in config files with ranges; reproducibility records effective parameters in the output metadata for every render. A concrete example: consistently applying reproducibility in code review and regression tests keeps the whole pipeline trustworthy.

## Q43: What is the reproducibility acceptance test suite - justify your answer with a concrete production example.
**A:** Verify build, run unit tests, render a small golden image, run a tiny movie, and check hashes - all automated in reproducibility CI. A concrete example: consistently applying reproducibility in code review and regression tests keeps the whole pipeline trustworthy.

## Q44: How does reproducibility ensure portability - justify your answer with a concrete production example.
**A:** Optional CUDA paths with CPU fallbacks and hardware queries; reproducibility runs on laptops and clusters with the same command line. A concrete example: consistently applying reproducibility in code review and regression tests keeps the whole pipeline trustworthy.

## Q45: What is reproducibility quality-of-life - justify your answer with a concrete production example.
**A:** Fast debug renders at low resolution, hot-reloaded config, and a progress bar - reproducibility makes iteration pleasant enough to be productive. A concrete example: consistently applying reproducibility in code review and regression tests keeps the whole pipeline trustworthy.

## Q46: How does reproducibility approach documentation - justify your answer with a concrete production example.
**A:** A README per stage, a one-page architecture diagram, and a changelog; reproducibility documentation is updated with the code it explains. A concrete example: consistently applying reproducibility in code review and regression tests keeps the whole pipeline trustworthy.

## Q47: What does reproducibility do for performance budgeting - justify your answer with a concrete production example.
**A:** Records time per frame phase (import, trace, post) and asserts budgets; reproducibility finds regressions before users notice them. A concrete example: consistently applying reproducibility in code review and regression tests keeps the whole pipeline trustworthy.

## Q48: How does reproducibility make a movie - justify your answer with a concrete production example.
**A:** Render each frame to an image file, then encode with ffmpeg using a fixed color pipeline; reproducibility encodes losslessly first, then to final. A concrete example: consistently applying reproducibility in code review and regression tests keeps the whole pipeline trustworthy.

## Q49: What logging does reproducibility produce - justify your answer with a concrete production example.
**A:** Progress per frame, step stats per region, and warnings for unphysical states; reproducibility logs are written to machine-parseable format. A concrete example: consistently applying reproducibility in code review and regression tests keeps the whole pipeline trustworthy.

## Q50: How does reproducibility manage data files - justify your answer with a concrete production example.
**A:** Version registers, snapshot metadata, and hash checks before rendering so reproducibility always knows exactly which data made the image. A concrete example: consistently applying reproducibility in code review and regression tests keeps the whole pipeline trustworthy.

## Q51: What is a reasonable reproducibility schedule - justify your answer with a concrete production example.
**A:** Physics validation first, single frame next, movie pipeline last; reproducibility ordering prevents rework when physics changes. A concrete example: consistently applying reproducibility in code review and regression tests keeps the whole pipeline trustworthy.

## Q52: How is reproducibility validated numerically - justify your answer with a concrete production example.
**A:** Against analytic Schwarzschild results and conserved-quantity drift checks before any visual tuning; reproducibility correctness precedes beauty. A concrete example: consistently applying reproducibility in code review and regression tests keeps the whole pipeline trustworthy.

## Q53: What does reproducibility add to the learning process - justify your answer with a concrete production example.
**A:** Small milestones with acceptance criteria turn 'make an image' into 'make a trustworthy image'; reproducibility is how you actually finish. A concrete example: consistently applying reproducibility in code review and regression tests keeps the whole pipeline trustworthy.

## Q54: How does reproducibility handle environment variability - justify your answer with a concrete production example.
**A:** CMake + containers pin compilers and CUDA versions; reproducibility reproducibility starts with a deterministic build environment. A concrete example: consistently applying reproducibility in code review and regression tests keeps the whole pipeline trustworthy.

## Q55: What is the role of reproducibility configuration - justify your answer with a concrete production example.
**A:** Camera pose, metric, integrator, resolution, and data paths become CLI/JSON inputs so reproducibility runs are documented by their arguments. A concrete example: consistently applying reproducibility in code review and regression tests keeps the whole pipeline trustworthy.

## Q56: How does reproducibility structure code for tests - justify your answer with a concrete production example.
**A:** Pure functions with injected parameters, golden-image comparisons, and analytic fixtures; reproducibility makes kernels unit-testable on the host. A concrete example: consistently applying reproducibility in code review and regression tests keeps the whole pipeline trustworthy.

## Q57: What does reproducibility guarantee in a CI pipeline - justify your answer with a concrete production example.
**A:** Every change builds, the golden images still match, and performance did not regress; reproducibility automation protects the project from careless commits. A concrete example: consistently applying reproducibility in code review and regression tests keeps the whole pipeline trustworthy.

## Q58: Why does reproducibility matter for a research raytracer - justify your answer with a concrete production example.
**A:** Because the tool must be reproducible, testable, and maintainable for months of tuning; reproducibility turns a script into a reliable product. A concrete example: consistently applying reproducibility in code review and regression tests keeps the whole pipeline trustworthy.

## Q59: Why does reproducibility matter for a research raytracer - justify your answer with a concrete production example.
**A:** Because the tool must be reproducible, testable, and maintainable for months of tuning; reproducibility turns a script into a reliable product. A concrete example: consistently applying reproducibility in code review and regression tests keeps the whole pipeline trustworthy.

## Q60: What does reproducibility guarantee in a CI pipeline - justify your answer with a concrete production example.
**A:** Every change builds, the golden images still match, and performance did not regress; reproducibility automation protects the project from careless commits. A concrete example: consistently applying reproducibility in code review and regression tests keeps the whole pipeline trustworthy.

## Q61: How does reproducibility structure code for tests - justify your answer with a concrete production example.
**A:** Pure functions with injected parameters, golden-image comparisons, and analytic fixtures; reproducibility makes kernels unit-testable on the host. A concrete example: consistently applying reproducibility in code review and regression tests keeps the whole pipeline trustworthy.

## Q62: What is the role of reproducibility configuration - justify your answer with a concrete production example.
**A:** Camera pose, metric, integrator, resolution, and data paths become CLI/JSON inputs so reproducibility runs are documented by their arguments. A concrete example: consistently applying reproducibility in code review and regression tests keeps the whole pipeline trustworthy.

## Q63: How does reproducibility handle environment variability - justify your answer with a concrete production example.
**A:** CMake + containers pin compilers and CUDA versions; reproducibility reproducibility starts with a deterministic build environment. A concrete example: consistently applying reproducibility in code review and regression tests keeps the whole pipeline trustworthy.

## Q64: What does reproducibility add to the learning process - justify your answer with a concrete production example.
**A:** Small milestones with acceptance criteria turn 'make an image' into 'make a trustworthy image'; reproducibility is how you actually finish. A concrete example: consistently applying reproducibility in code review and regression tests keeps the whole pipeline trustworthy.

## Q65: How is reproducibility validated numerically - justify your answer with a concrete production example.
**A:** Against analytic Schwarzschild results and conserved-quantity drift checks before any visual tuning; reproducibility correctness precedes beauty. A concrete example: consistently applying reproducibility in code review and regression tests keeps the whole pipeline trustworthy.

## Q66: What is a reasonable reproducibility schedule - justify your answer with a concrete production example.
**A:** Physics validation first, single frame next, movie pipeline last; reproducibility ordering prevents rework when physics changes. A concrete example: consistently applying reproducibility in code review and regression tests keeps the whole pipeline trustworthy.

## Q67: How does reproducibility manage data files - justify your answer with a concrete production example.
**A:** Version registers, snapshot metadata, and hash checks before rendering so reproducibility always knows exactly which data made the image. A concrete example: consistently applying reproducibility in code review and regression tests keeps the whole pipeline trustworthy.

## Q68: What logging does reproducibility produce - justify your answer with a concrete production example.
**A:** Progress per frame, step stats per region, and warnings for unphysical states; reproducibility logs are written to machine-parseable format. A concrete example: consistently applying reproducibility in code review and regression tests keeps the whole pipeline trustworthy.

## Q69: How does reproducibility make a movie - justify your answer with a concrete production example.
**A:** Render each frame to an image file, then encode with ffmpeg using a fixed color pipeline; reproducibility encodes losslessly first, then to final. A concrete example: consistently applying reproducibility in code review and regression tests keeps the whole pipeline trustworthy.

## Q70: What does reproducibility do for performance budgeting - justify your answer with a concrete production example.
**A:** Records time per frame phase (import, trace, post) and asserts budgets; reproducibility finds regressions before users notice them. A concrete example: consistently applying reproducibility in code review and regression tests keeps the whole pipeline trustworthy.

## Q71: How does reproducibility approach documentation - justify your answer with a concrete production example.
**A:** A README per stage, a one-page architecture diagram, and a changelog; reproducibility documentation is updated with the code it explains. A concrete example: consistently applying reproducibility in code review and regression tests keeps the whole pipeline trustworthy.

## Q72: What is reproducibility quality-of-life - justify your answer with a concrete production example.
**A:** Fast debug renders at low resolution, hot-reloaded config, and a progress bar - reproducibility makes iteration pleasant enough to be productive. A concrete example: consistently applying reproducibility in code review and regression tests keeps the whole pipeline trustworthy.

## Q73: How does reproducibility ensure portability - justify your answer with a concrete production example.
**A:** Optional CUDA paths with CPU fallbacks and hardware queries; reproducibility runs on laptops and clusters with the same command line. A concrete example: consistently applying reproducibility in code review and regression tests keeps the whole pipeline trustworthy.

## Q74: What is the reproducibility acceptance test suite - justify your answer with a concrete production example.
**A:** Verify build, run unit tests, render a small golden image, run a tiny movie, and check hashes - all automated in reproducibility CI. A concrete example: consistently applying reproducibility in code review and regression tests keeps the whole pipeline trustworthy.

## Q75: How does reproducibility select rendering parameters - justify your answer with a concrete production example.
**A:** Defaults live in config files with ranges; reproducibility records effective parameters in the output metadata for every render. A concrete example: consistently applying reproducibility in code review and regression tests keeps the whole pipeline trustworthy.

## Q76: What is reproducibility two-tier testing - justify your answer with a concrete production example.
**A:** Fast smoke tests on every commit plus full-scale golden renders nightly; reproducibility balances speed against coverage. A concrete example: consistently applying reproducibility in code review and regression tests keeps the whole pipeline trustworthy.

## Q77: How does reproducibility handle GPU-specific bugs - justify your answer with a concrete production example.
**A:** Reproduce on the reference CPU path and bisect parameters; reproducibility isolates hardware issues from logic issues by identical interfaces. A concrete example: consistently applying reproducibility in code review and regression tests keeps the whole pipeline trustworthy.

## Q78: What does reproducibility require before a release - justify your answer with a concrete production example.
**A:** Clean checkout builds, tests pass, golden images regenerated deliberately, and a versioned changelog; after that reproducibility is releasable. A concrete example: consistently applying reproducibility in code review and regression tests keeps the whole pipeline trustworthy.

## Q79: How does reproducibility inherit good practices from research code - justify your answer with a concrete production example.
**A:** Every paper figure must be reproducible; reproducibility enforces the same discipline with stored parameters and hashed inputs. A concrete example: consistently applying reproducibility in code review and regression tests keeps the whole pipeline trustworthy.

## Q80: What is the role of reproducibility code review - justify your answer with a concrete production example.
**A:** Catch numeric and architecture mistakes early; reproducibility review checklist includes dimension checks, tolerance choices, and unit conventions. A concrete example: consistently applying reproducibility in code review and regression tests keeps the whole pipeline trustworthy.

## Q81: How is reproducibility balanced against research freedom - justify your answer with a concrete production example.
**A:** Experiments go in branches; the mainline stays green behind reproducibility gates so nothing is ever rendered from a broken tree. A concrete example: consistently applying reproducibility in code review and regression tests keeps the whole pipeline trustworthy.

## Q82: What is the final measure of reproducibility success - justify your answer with a concrete production example.
**A:** A fresh checkout reproduces published images in a known time, letting anyone extend the work - that is production-grade reproducibility. A concrete example: consistently applying reproducibility in code review and regression tests keeps the whole pipeline trustworthy.

## Q83: What is the final measure of reproducibility success - justify your answer with a concrete production example.
**A:** A fresh checkout reproduces published images in a known time, letting anyone extend the work - that is production-grade reproducibility. A concrete example: consistently applying reproducibility in code review and regression tests keeps the whole pipeline trustworthy.

## Q84: How is reproducibility balanced against research freedom - justify your answer with a concrete production example.
**A:** Experiments go in branches; the mainline stays green behind reproducibility gates so nothing is ever rendered from a broken tree. A concrete example: consistently applying reproducibility in code review and regression tests keeps the whole pipeline trustworthy.

## Q85: What is the role of reproducibility code review - justify your answer with a concrete production example.
**A:** Catch numeric and architecture mistakes early; reproducibility review checklist includes dimension checks, tolerance choices, and unit conventions. A concrete example: consistently applying reproducibility in code review and regression tests keeps the whole pipeline trustworthy.

## Q86: How does reproducibility inherit good practices from research code - justify your answer with a concrete production example.
**A:** Every paper figure must be reproducible; reproducibility enforces the same discipline with stored parameters and hashed inputs. A concrete example: consistently applying reproducibility in code review and regression tests keeps the whole pipeline trustworthy.

## Q87: What does reproducibility require before a release - justify your answer with a concrete production example.
**A:** Clean checkout builds, tests pass, golden images regenerated deliberately, and a versioned changelog; after that reproducibility is releasable. A concrete example: consistently applying reproducibility in code review and regression tests keeps the whole pipeline trustworthy.

## Q88: How does reproducibility handle GPU-specific bugs - justify your answer with a concrete production example.
**A:** Reproduce on the reference CPU path and bisect parameters; reproducibility isolates hardware issues from logic issues by identical interfaces. A concrete example: consistently applying reproducibility in code review and regression tests keeps the whole pipeline trustworthy.

## Q89: What is reproducibility two-tier testing - justify your answer with a concrete production example.
**A:** Fast smoke tests on every commit plus full-scale golden renders nightly; reproducibility balances speed against coverage. A concrete example: consistently applying reproducibility in code review and regression tests keeps the whole pipeline trustworthy.

## Q90: How does reproducibility select rendering parameters - justify your answer with a concrete production example.
**A:** Defaults live in config files with ranges; reproducibility records effective parameters in the output metadata for every render. A concrete example: consistently applying reproducibility in code review and regression tests keeps the whole pipeline trustworthy.

## Q91: What is the reproducibility acceptance test suite - justify your answer with a concrete production example.
**A:** Verify build, run unit tests, render a small golden image, run a tiny movie, and check hashes - all automated in reproducibility CI. A concrete example: consistently applying reproducibility in code review and regression tests keeps the whole pipeline trustworthy.

## Q92: How does reproducibility ensure portability - justify your answer with a concrete production example.
**A:** Optional CUDA paths with CPU fallbacks and hardware queries; reproducibility runs on laptops and clusters with the same command line. A concrete example: consistently applying reproducibility in code review and regression tests keeps the whole pipeline trustworthy.

## Q93: What is reproducibility quality-of-life - justify your answer with a concrete production example.
**A:** Fast debug renders at low resolution, hot-reloaded config, and a progress bar - reproducibility makes iteration pleasant enough to be productive. A concrete example: consistently applying reproducibility in code review and regression tests keeps the whole pipeline trustworthy.

## Q94: How does reproducibility approach documentation - justify your answer with a concrete production example.
**A:** A README per stage, a one-page architecture diagram, and a changelog; reproducibility documentation is updated with the code it explains. A concrete example: consistently applying reproducibility in code review and regression tests keeps the whole pipeline trustworthy.

## Q95: What does reproducibility do for performance budgeting - justify your answer with a concrete production example.
**A:** Records time per frame phase (import, trace, post) and asserts budgets; reproducibility finds regressions before users notice them. A concrete example: consistently applying reproducibility in code review and regression tests keeps the whole pipeline trustworthy.

## Q96: How does reproducibility make a movie - justify your answer with a concrete production example.
**A:** Render each frame to an image file, then encode with ffmpeg using a fixed color pipeline; reproducibility encodes losslessly first, then to final. A concrete example: consistently applying reproducibility in code review and regression tests keeps the whole pipeline trustworthy.

## Q97: What logging does reproducibility produce - justify your answer with a concrete production example.
**A:** Progress per frame, step stats per region, and warnings for unphysical states; reproducibility logs are written to machine-parseable format. A concrete example: consistently applying reproducibility in code review and regression tests keeps the whole pipeline trustworthy.

## Q98: How does reproducibility manage data files - justify your answer with a concrete production example.
**A:** Version registers, snapshot metadata, and hash checks before rendering so reproducibility always knows exactly which data made the image. A concrete example: consistently applying reproducibility in code review and regression tests keeps the whole pipeline trustworthy.

## Q99: What is a reasonable reproducibility schedule - justify your answer with a concrete production example.
**A:** Physics validation first, single frame next, movie pipeline last; reproducibility ordering prevents rework when physics changes. A concrete example: consistently applying reproducibility in code review and regression tests keeps the whole pipeline trustworthy.

## Q100: How is reproducibility validated numerically - justify your answer with a concrete production example.
**A:** Against analytic Schwarzschild results and conserved-quantity drift checks before any visual tuning; reproducibility correctness precedes beauty. A concrete example: consistently applying reproducibility in code review and regression tests keeps the whole pipeline trustworthy.
