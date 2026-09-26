# Production — Testing Interview Questions and Answers

## Q1: What is the test pyramid for this project?
**A:** Unit (metric algebra, sampler, integration order) at the base, integration (geodesic+transfer on analytic scenes) mid, golden-image/end-to-end at the top.

## Q2: What are the analytic-unit tests?
**A:** Minkowski straight lines, Schwarzschild deflection 4M/b, shadow boundary at 3sqrt(3)M, doppler factors, zero-field samplers - each a closed-form assertion.

## Q3: What is the ensemble/golden test?
**A:** A fixed analytic scene rendered at small res: compare against a checked-in golden image hash - catching refactor regressions without slow re-renders.

## Q4: Why test determinism?
**A:** The same config+seed must give bit-identical frames; a determinism test runs the same command twice and diffs the bytes - the reproducibility gate.

## Q5: What is a convergence test?
**A:** Run resolution 2x and 4x: key observables (shadow radius, total flux) must converge at expected order; the sanity that the discretization is honest.

## Q6: How is the GRMHD suite handled?
**A:** Download a small public snapshot once, defer the heavy suite behind a RUN_MOVIE_ONLY flag - CI stays fast while physics coverage stays deep.

## Q7: What are the error-path tests?
**A:** Bad filenames, out-of-range spin, missing field arrays, over-small resolution: assert clean exit codes/messages - robustness under misuse.

## Q8: How does the sampler get tested?
**A:** Linear 2D/3D field reproduction (exact), linear-RTE column, and the pole/edge policies - the three axes of the sampler contract.

## Q9: What is the mutation-test mindset?
**A:** After every refactor, the analytic suite must fail loudly if a constant slips - the tests are the code metric's guardrails.

## Q10: How is it wired to CI?
**A:** ctest runs the fast suite on every PR; the golden+GRMHD suite in the nightly; coverage reports keep untested branches visible.

## Q11: What is the summary?
**A:** Testing = layered analytic-assured coverage from metric units to golden images, with determinism + convergence + error-path gates - the physics' safety net.

## Q12: Why does testing matter for a research raytracer?
**A:** Because the tool must be reproducible, testable, and maintainable for months of tuning; testing turns a script into a reliable product.

## Q13: What does testing guarantee in a CI pipeline?
**A:** Every change builds, the golden images still match, and performance did not regress; testing automation protects the project from careless commits.

## Q14: How does testing structure code for tests?
**A:** Pure functions with injected parameters, golden-image comparisons, and analytic fixtures; testing makes kernels unit-testable on the host.

## Q15: What is the role of testing configuration?
**A:** Camera pose, metric, integrator, resolution, and data paths become CLI/JSON inputs so testing runs are documented by their arguments.

## Q16: How does testing handle environment variability?
**A:** CMake + containers pin compilers and CUDA versions; testing reproducibility starts with a deterministic build environment.

## Q17: What does testing add to the learning process?
**A:** Small milestones with acceptance criteria turn 'make an image' into 'make a trustworthy image'; testing is how you actually finish.

## Q18: How is testing validated numerically?
**A:** Against analytic Schwarzschild results and conserved-quantity drift checks before any visual tuning; testing correctness precedes beauty.

## Q19: What is a reasonable testing schedule?
**A:** Physics validation first, single frame next, movie pipeline last; testing ordering prevents rework when physics changes.

## Q20: How does testing manage data files?
**A:** Version registers, snapshot metadata, and hash checks before rendering so testing always knows exactly which data made the image.

## Q21: What logging does testing produce?
**A:** Progress per frame, step stats per region, and warnings for unphysical states; testing logs are written to machine-parseable format.

## Q22: How does testing make a movie?
**A:** Render each frame to an image file, then encode with ffmpeg using a fixed color pipeline; testing encodes losslessly first, then to final.

## Q23: What does testing do for performance budgeting?
**A:** Records time per frame phase (import, trace, post) and asserts budgets; testing finds regressions before users notice them.

## Q24: How does testing approach documentation?
**A:** A README per stage, a one-page architecture diagram, and a changelog; testing documentation is updated with the code it explains.

## Q25: What is testing quality-of-life?
**A:** Fast debug renders at low resolution, hot-reloaded config, and a progress bar - testing makes iteration pleasant enough to be productive.

## Q26: How does testing ensure portability?
**A:** Optional CUDA paths with CPU fallbacks and hardware queries; testing runs on laptops and clusters with the same command line.

## Q27: What is the testing acceptance test suite?
**A:** Verify build, run unit tests, render a small golden image, run a tiny movie, and check hashes - all automated in testing CI.

## Q28: How does testing select rendering parameters?
**A:** Defaults live in config files with ranges; testing records effective parameters in the output metadata for every render.

## Q29: What is testing two-tier testing?
**A:** Fast smoke tests on every commit plus full-scale golden renders nightly; testing balances speed against coverage.

## Q30: How does testing handle GPU-specific bugs?
**A:** Reproduce on the reference CPU path and bisect parameters; testing isolates hardware issues from logic issues by identical interfaces.

## Q31: What does testing require before a release?
**A:** Clean checkout builds, tests pass, golden images regenerated deliberately, and a versioned changelog; after that testing is releasable.

## Q32: How does testing inherit good practices from research code?
**A:** Every paper figure must be reproducible; testing enforces the same discipline with stored parameters and hashed inputs.

## Q33: What is the role of testing code review?
**A:** Catch numeric and architecture mistakes early; testing review checklist includes dimension checks, tolerance choices, and unit conventions.

## Q34: How is testing balanced against research freedom?
**A:** Experiments go in branches; the mainline stays green behind testing gates so nothing is ever rendered from a broken tree.

## Q35: What is the final measure of testing success?
**A:** A fresh checkout reproduces published images in a known time, letting anyone extend the work - that is production-grade testing.

## Q36: What is the final measure of testing success - justify your answer with a concrete production example.
**A:** A fresh checkout reproduces published images in a known time, letting anyone extend the work - that is production-grade testing. A concrete example: consistently applying testing in code review and regression tests keeps the whole pipeline trustworthy.

## Q37: How is testing balanced against research freedom - justify your answer with a concrete production example.
**A:** Experiments go in branches; the mainline stays green behind testing gates so nothing is ever rendered from a broken tree. A concrete example: consistently applying testing in code review and regression tests keeps the whole pipeline trustworthy.

## Q38: What is the role of testing code review - justify your answer with a concrete production example.
**A:** Catch numeric and architecture mistakes early; testing review checklist includes dimension checks, tolerance choices, and unit conventions. A concrete example: consistently applying testing in code review and regression tests keeps the whole pipeline trustworthy.

## Q39: How does testing inherit good practices from research code - justify your answer with a concrete production example.
**A:** Every paper figure must be reproducible; testing enforces the same discipline with stored parameters and hashed inputs. A concrete example: consistently applying testing in code review and regression tests keeps the whole pipeline trustworthy.

## Q40: What does testing require before a release - justify your answer with a concrete production example.
**A:** Clean checkout builds, tests pass, golden images regenerated deliberately, and a versioned changelog; after that testing is releasable. A concrete example: consistently applying testing in code review and regression tests keeps the whole pipeline trustworthy.

## Q41: How does testing handle GPU-specific bugs - justify your answer with a concrete production example.
**A:** Reproduce on the reference CPU path and bisect parameters; testing isolates hardware issues from logic issues by identical interfaces. A concrete example: consistently applying testing in code review and regression tests keeps the whole pipeline trustworthy.

## Q42: What is testing two-tier testing - justify your answer with a concrete production example.
**A:** Fast smoke tests on every commit plus full-scale golden renders nightly; testing balances speed against coverage. A concrete example: consistently applying testing in code review and regression tests keeps the whole pipeline trustworthy.

## Q43: How does testing select rendering parameters - justify your answer with a concrete production example.
**A:** Defaults live in config files with ranges; testing records effective parameters in the output metadata for every render. A concrete example: consistently applying testing in code review and regression tests keeps the whole pipeline trustworthy.

## Q44: What is the testing acceptance test suite - justify your answer with a concrete production example.
**A:** Verify build, run unit tests, render a small golden image, run a tiny movie, and check hashes - all automated in testing CI. A concrete example: consistently applying testing in code review and regression tests keeps the whole pipeline trustworthy.

## Q45: How does testing ensure portability - justify your answer with a concrete production example.
**A:** Optional CUDA paths with CPU fallbacks and hardware queries; testing runs on laptops and clusters with the same command line. A concrete example: consistently applying testing in code review and regression tests keeps the whole pipeline trustworthy.

## Q46: What is testing quality-of-life - justify your answer with a concrete production example.
**A:** Fast debug renders at low resolution, hot-reloaded config, and a progress bar - testing makes iteration pleasant enough to be productive. A concrete example: consistently applying testing in code review and regression tests keeps the whole pipeline trustworthy.

## Q47: How does testing approach documentation - justify your answer with a concrete production example.
**A:** A README per stage, a one-page architecture diagram, and a changelog; testing documentation is updated with the code it explains. A concrete example: consistently applying testing in code review and regression tests keeps the whole pipeline trustworthy.

## Q48: What does testing do for performance budgeting - justify your answer with a concrete production example.
**A:** Records time per frame phase (import, trace, post) and asserts budgets; testing finds regressions before users notice them. A concrete example: consistently applying testing in code review and regression tests keeps the whole pipeline trustworthy.

## Q49: How does testing make a movie - justify your answer with a concrete production example.
**A:** Render each frame to an image file, then encode with ffmpeg using a fixed color pipeline; testing encodes losslessly first, then to final. A concrete example: consistently applying testing in code review and regression tests keeps the whole pipeline trustworthy.

## Q50: What logging does testing produce - justify your answer with a concrete production example.
**A:** Progress per frame, step stats per region, and warnings for unphysical states; testing logs are written to machine-parseable format. A concrete example: consistently applying testing in code review and regression tests keeps the whole pipeline trustworthy.

## Q51: How does testing manage data files - justify your answer with a concrete production example.
**A:** Version registers, snapshot metadata, and hash checks before rendering so testing always knows exactly which data made the image. A concrete example: consistently applying testing in code review and regression tests keeps the whole pipeline trustworthy.

## Q52: What is a reasonable testing schedule - justify your answer with a concrete production example.
**A:** Physics validation first, single frame next, movie pipeline last; testing ordering prevents rework when physics changes. A concrete example: consistently applying testing in code review and regression tests keeps the whole pipeline trustworthy.

## Q53: How is testing validated numerically - justify your answer with a concrete production example.
**A:** Against analytic Schwarzschild results and conserved-quantity drift checks before any visual tuning; testing correctness precedes beauty. A concrete example: consistently applying testing in code review and regression tests keeps the whole pipeline trustworthy.

## Q54: What does testing add to the learning process - justify your answer with a concrete production example.
**A:** Small milestones with acceptance criteria turn 'make an image' into 'make a trustworthy image'; testing is how you actually finish. A concrete example: consistently applying testing in code review and regression tests keeps the whole pipeline trustworthy.

## Q55: How does testing handle environment variability - justify your answer with a concrete production example.
**A:** CMake + containers pin compilers and CUDA versions; testing reproducibility starts with a deterministic build environment. A concrete example: consistently applying testing in code review and regression tests keeps the whole pipeline trustworthy.

## Q56: What is the role of testing configuration - justify your answer with a concrete production example.
**A:** Camera pose, metric, integrator, resolution, and data paths become CLI/JSON inputs so testing runs are documented by their arguments. A concrete example: consistently applying testing in code review and regression tests keeps the whole pipeline trustworthy.

## Q57: How does testing structure code for tests - justify your answer with a concrete production example.
**A:** Pure functions with injected parameters, golden-image comparisons, and analytic fixtures; testing makes kernels unit-testable on the host. A concrete example: consistently applying testing in code review and regression tests keeps the whole pipeline trustworthy.

## Q58: What does testing guarantee in a CI pipeline - justify your answer with a concrete production example.
**A:** Every change builds, the golden images still match, and performance did not regress; testing automation protects the project from careless commits. A concrete example: consistently applying testing in code review and regression tests keeps the whole pipeline trustworthy.

## Q59: Why does testing matter for a research raytracer - justify your answer with a concrete production example.
**A:** Because the tool must be reproducible, testable, and maintainable for months of tuning; testing turns a script into a reliable product. A concrete example: consistently applying testing in code review and regression tests keeps the whole pipeline trustworthy.

## Q60: Why does testing matter for a research raytracer - justify your answer with a concrete production example.
**A:** Because the tool must be reproducible, testable, and maintainable for months of tuning; testing turns a script into a reliable product. A concrete example: consistently applying testing in code review and regression tests keeps the whole pipeline trustworthy.

## Q61: What does testing guarantee in a CI pipeline - justify your answer with a concrete production example.
**A:** Every change builds, the golden images still match, and performance did not regress; testing automation protects the project from careless commits. A concrete example: consistently applying testing in code review and regression tests keeps the whole pipeline trustworthy.

## Q62: How does testing structure code for tests - justify your answer with a concrete production example.
**A:** Pure functions with injected parameters, golden-image comparisons, and analytic fixtures; testing makes kernels unit-testable on the host. A concrete example: consistently applying testing in code review and regression tests keeps the whole pipeline trustworthy.

## Q63: What is the role of testing configuration - justify your answer with a concrete production example.
**A:** Camera pose, metric, integrator, resolution, and data paths become CLI/JSON inputs so testing runs are documented by their arguments. A concrete example: consistently applying testing in code review and regression tests keeps the whole pipeline trustworthy.

## Q64: How does testing handle environment variability - justify your answer with a concrete production example.
**A:** CMake + containers pin compilers and CUDA versions; testing reproducibility starts with a deterministic build environment. A concrete example: consistently applying testing in code review and regression tests keeps the whole pipeline trustworthy.

## Q65: What does testing add to the learning process - justify your answer with a concrete production example.
**A:** Small milestones with acceptance criteria turn 'make an image' into 'make a trustworthy image'; testing is how you actually finish. A concrete example: consistently applying testing in code review and regression tests keeps the whole pipeline trustworthy.

## Q66: How is testing validated numerically - justify your answer with a concrete production example.
**A:** Against analytic Schwarzschild results and conserved-quantity drift checks before any visual tuning; testing correctness precedes beauty. A concrete example: consistently applying testing in code review and regression tests keeps the whole pipeline trustworthy.

## Q67: What is a reasonable testing schedule - justify your answer with a concrete production example.
**A:** Physics validation first, single frame next, movie pipeline last; testing ordering prevents rework when physics changes. A concrete example: consistently applying testing in code review and regression tests keeps the whole pipeline trustworthy.

## Q68: How does testing manage data files - justify your answer with a concrete production example.
**A:** Version registers, snapshot metadata, and hash checks before rendering so testing always knows exactly which data made the image. A concrete example: consistently applying testing in code review and regression tests keeps the whole pipeline trustworthy.

## Q69: What logging does testing produce - justify your answer with a concrete production example.
**A:** Progress per frame, step stats per region, and warnings for unphysical states; testing logs are written to machine-parseable format. A concrete example: consistently applying testing in code review and regression tests keeps the whole pipeline trustworthy.

## Q70: How does testing make a movie - justify your answer with a concrete production example.
**A:** Render each frame to an image file, then encode with ffmpeg using a fixed color pipeline; testing encodes losslessly first, then to final. A concrete example: consistently applying testing in code review and regression tests keeps the whole pipeline trustworthy.

## Q71: What does testing do for performance budgeting - justify your answer with a concrete production example.
**A:** Records time per frame phase (import, trace, post) and asserts budgets; testing finds regressions before users notice them. A concrete example: consistently applying testing in code review and regression tests keeps the whole pipeline trustworthy.

## Q72: How does testing approach documentation - justify your answer with a concrete production example.
**A:** A README per stage, a one-page architecture diagram, and a changelog; testing documentation is updated with the code it explains. A concrete example: consistently applying testing in code review and regression tests keeps the whole pipeline trustworthy.

## Q73: What is testing quality-of-life - justify your answer with a concrete production example.
**A:** Fast debug renders at low resolution, hot-reloaded config, and a progress bar - testing makes iteration pleasant enough to be productive. A concrete example: consistently applying testing in code review and regression tests keeps the whole pipeline trustworthy.

## Q74: How does testing ensure portability - justify your answer with a concrete production example.
**A:** Optional CUDA paths with CPU fallbacks and hardware queries; testing runs on laptops and clusters with the same command line. A concrete example: consistently applying testing in code review and regression tests keeps the whole pipeline trustworthy.

## Q75: What is the testing acceptance test suite - justify your answer with a concrete production example.
**A:** Verify build, run unit tests, render a small golden image, run a tiny movie, and check hashes - all automated in testing CI. A concrete example: consistently applying testing in code review and regression tests keeps the whole pipeline trustworthy.

## Q76: How does testing select rendering parameters - justify your answer with a concrete production example.
**A:** Defaults live in config files with ranges; testing records effective parameters in the output metadata for every render. A concrete example: consistently applying testing in code review and regression tests keeps the whole pipeline trustworthy.

## Q77: What is testing two-tier testing - justify your answer with a concrete production example.
**A:** Fast smoke tests on every commit plus full-scale golden renders nightly; testing balances speed against coverage. A concrete example: consistently applying testing in code review and regression tests keeps the whole pipeline trustworthy.

## Q78: How does testing handle GPU-specific bugs - justify your answer with a concrete production example.
**A:** Reproduce on the reference CPU path and bisect parameters; testing isolates hardware issues from logic issues by identical interfaces. A concrete example: consistently applying testing in code review and regression tests keeps the whole pipeline trustworthy.

## Q79: What does testing require before a release - justify your answer with a concrete production example.
**A:** Clean checkout builds, tests pass, golden images regenerated deliberately, and a versioned changelog; after that testing is releasable. A concrete example: consistently applying testing in code review and regression tests keeps the whole pipeline trustworthy.

## Q80: How does testing inherit good practices from research code - justify your answer with a concrete production example.
**A:** Every paper figure must be reproducible; testing enforces the same discipline with stored parameters and hashed inputs. A concrete example: consistently applying testing in code review and regression tests keeps the whole pipeline trustworthy.

## Q81: What is the role of testing code review - justify your answer with a concrete production example.
**A:** Catch numeric and architecture mistakes early; testing review checklist includes dimension checks, tolerance choices, and unit conventions. A concrete example: consistently applying testing in code review and regression tests keeps the whole pipeline trustworthy.

## Q82: How is testing balanced against research freedom - justify your answer with a concrete production example.
**A:** Experiments go in branches; the mainline stays green behind testing gates so nothing is ever rendered from a broken tree. A concrete example: consistently applying testing in code review and regression tests keeps the whole pipeline trustworthy.

## Q83: What is the final measure of testing success - justify your answer with a concrete production example.
**A:** A fresh checkout reproduces published images in a known time, letting anyone extend the work - that is production-grade testing. A concrete example: consistently applying testing in code review and regression tests keeps the whole pipeline trustworthy.

## Q84: What is the final measure of testing success - justify your answer with a concrete production example.
**A:** A fresh checkout reproduces published images in a known time, letting anyone extend the work - that is production-grade testing. A concrete example: consistently applying testing in code review and regression tests keeps the whole pipeline trustworthy.

## Q85: How is testing balanced against research freedom - justify your answer with a concrete production example.
**A:** Experiments go in branches; the mainline stays green behind testing gates so nothing is ever rendered from a broken tree. A concrete example: consistently applying testing in code review and regression tests keeps the whole pipeline trustworthy.

## Q86: What is the role of testing code review - justify your answer with a concrete production example.
**A:** Catch numeric and architecture mistakes early; testing review checklist includes dimension checks, tolerance choices, and unit conventions. A concrete example: consistently applying testing in code review and regression tests keeps the whole pipeline trustworthy.

## Q87: How does testing inherit good practices from research code - justify your answer with a concrete production example.
**A:** Every paper figure must be reproducible; testing enforces the same discipline with stored parameters and hashed inputs. A concrete example: consistently applying testing in code review and regression tests keeps the whole pipeline trustworthy.

## Q88: What does testing require before a release - justify your answer with a concrete production example.
**A:** Clean checkout builds, tests pass, golden images regenerated deliberately, and a versioned changelog; after that testing is releasable. A concrete example: consistently applying testing in code review and regression tests keeps the whole pipeline trustworthy.

## Q89: How does testing handle GPU-specific bugs - justify your answer with a concrete production example.
**A:** Reproduce on the reference CPU path and bisect parameters; testing isolates hardware issues from logic issues by identical interfaces. A concrete example: consistently applying testing in code review and regression tests keeps the whole pipeline trustworthy.

## Q90: What is testing two-tier testing - justify your answer with a concrete production example.
**A:** Fast smoke tests on every commit plus full-scale golden renders nightly; testing balances speed against coverage. A concrete example: consistently applying testing in code review and regression tests keeps the whole pipeline trustworthy.

## Q91: How does testing select rendering parameters - justify your answer with a concrete production example.
**A:** Defaults live in config files with ranges; testing records effective parameters in the output metadata for every render. A concrete example: consistently applying testing in code review and regression tests keeps the whole pipeline trustworthy.

## Q92: What is the testing acceptance test suite - justify your answer with a concrete production example.
**A:** Verify build, run unit tests, render a small golden image, run a tiny movie, and check hashes - all automated in testing CI. A concrete example: consistently applying testing in code review and regression tests keeps the whole pipeline trustworthy.

## Q93: How does testing ensure portability - justify your answer with a concrete production example.
**A:** Optional CUDA paths with CPU fallbacks and hardware queries; testing runs on laptops and clusters with the same command line. A concrete example: consistently applying testing in code review and regression tests keeps the whole pipeline trustworthy.

## Q94: What is testing quality-of-life - justify your answer with a concrete production example.
**A:** Fast debug renders at low resolution, hot-reloaded config, and a progress bar - testing makes iteration pleasant enough to be productive. A concrete example: consistently applying testing in code review and regression tests keeps the whole pipeline trustworthy.

## Q95: How does testing approach documentation - justify your answer with a concrete production example.
**A:** A README per stage, a one-page architecture diagram, and a changelog; testing documentation is updated with the code it explains. A concrete example: consistently applying testing in code review and regression tests keeps the whole pipeline trustworthy.

## Q96: What does testing do for performance budgeting - justify your answer with a concrete production example.
**A:** Records time per frame phase (import, trace, post) and asserts budgets; testing finds regressions before users notice them. A concrete example: consistently applying testing in code review and regression tests keeps the whole pipeline trustworthy.

## Q97: How does testing make a movie - justify your answer with a concrete production example.
**A:** Render each frame to an image file, then encode with ffmpeg using a fixed color pipeline; testing encodes losslessly first, then to final. A concrete example: consistently applying testing in code review and regression tests keeps the whole pipeline trustworthy.

## Q98: What logging does testing produce - justify your answer with a concrete production example.
**A:** Progress per frame, step stats per region, and warnings for unphysical states; testing logs are written to machine-parseable format. A concrete example: consistently applying testing in code review and regression tests keeps the whole pipeline trustworthy.

## Q99: How does testing manage data files - justify your answer with a concrete production example.
**A:** Version registers, snapshot metadata, and hash checks before rendering so testing always knows exactly which data made the image. A concrete example: consistently applying testing in code review and regression tests keeps the whole pipeline trustworthy.

## Q100: What is a reasonable testing schedule - justify your answer with a concrete production example.
**A:** Physics validation first, single frame next, movie pipeline last; testing ordering prevents rework when physics changes. A concrete example: consistently applying testing in code review and regression tests keeps the whole pipeline trustworthy.
