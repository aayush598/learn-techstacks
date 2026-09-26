# Production — Documentation Interview Questions and Answers

## Q1: What documentation does a scientific raytracer need?
**A:** README (what/why/quickstart), a physics/derivations chapter, a build/dev guide, an API reference, and an observables/metrics glossary - a pyramid, not a monograph.

## Q2: What is the minimal README?
**A:** One page: what it renders, install/build 2 commands, run 1 command, and 2 grounding images (Schwarzschild, Kerr) - enough to orient in a glance.

## Q3: How deep does the physics chapter go?
**A:** Metric definitions, geodesic/Hamiltonian derivation, the transfer equation and synchrotron formulas - with derivations, sources, and the code's parameter names.

## Q4: What is a beginner's run-through?
**A:** A 'first movie' tutorial: install, download a public snapshot, render one frame, then a 10-line movie — the onboarding path that makes the tool usable.

## Q5: How is the API documented?
**A:** Doxygen (or docstring) on the public header API: function contract, units, thread-safety, and the error contract - the maintenance wall of the core.

## Q6: What is the parameter glossary?
**A:** Every CLI/config key: meaning, units, default, valid range - the reference index that keeps a growing option surface coherent.

## Q7: What are the run-recipe docs?
**A:** Curated examples (Schwarzschild still, Kerr movie, M87-like fit) with the exact config files - 'do this to get this' saved as reproduction recipes.

## Q8: How do docs stay current?
**A:** A CI doc-check (links, examples runnable, option names matched) plus the rule that changing a CLI key without updating the glossary is a bug.

## Q9: What is the contributor guide?
**A:** Reading order, code layout map, test running, and the golden-number philosophy - the documentation that makes growth possible.

## Q10: What is the summary?
**A:** Documentation is the interface of a tool meant to be studied, extended, and trusted - a pyramid of README, physics, API, glossary, recipes, kept alive by CI.

## Q11: Why does documentation matter for a research raytracer?
**A:** Because the tool must be reproducible, testable, and maintainable for months of tuning; documentation turns a script into a reliable product.

## Q12: What does documentation guarantee in a CI pipeline?
**A:** Every change builds, the golden images still match, and performance did not regress; documentation automation protects the project from careless commits.

## Q13: How does documentation structure code for tests?
**A:** Pure functions with injected parameters, golden-image comparisons, and analytic fixtures; documentation makes kernels unit-testable on the host.

## Q14: What is the role of documentation configuration?
**A:** Camera pose, metric, integrator, resolution, and data paths become CLI/JSON inputs so documentation runs are documented by their arguments.

## Q15: How does documentation handle environment variability?
**A:** CMake + containers pin compilers and CUDA versions; documentation reproducibility starts with a deterministic build environment.

## Q16: What does documentation add to the learning process?
**A:** Small milestones with acceptance criteria turn 'make an image' into 'make a trustworthy image'; documentation is how you actually finish.

## Q17: How is documentation validated numerically?
**A:** Against analytic Schwarzschild results and conserved-quantity drift checks before any visual tuning; documentation correctness precedes beauty.

## Q18: What is a reasonable documentation schedule?
**A:** Physics validation first, single frame next, movie pipeline last; documentation ordering prevents rework when physics changes.

## Q19: How does documentation manage data files?
**A:** Version registers, snapshot metadata, and hash checks before rendering so documentation always knows exactly which data made the image.

## Q20: What logging does documentation produce?
**A:** Progress per frame, step stats per region, and warnings for unphysical states; documentation logs are written to machine-parseable format.

## Q21: How does documentation make a movie?
**A:** Render each frame to an image file, then encode with ffmpeg using a fixed color pipeline; documentation encodes losslessly first, then to final.

## Q22: What does documentation do for performance budgeting?
**A:** Records time per frame phase (import, trace, post) and asserts budgets; documentation finds regressions before users notice them.

## Q23: How does documentation approach documentation?
**A:** A README per stage, a one-page architecture diagram, and a changelog; documentation documentation is updated with the code it explains.

## Q24: What is documentation quality-of-life?
**A:** Fast debug renders at low resolution, hot-reloaded config, and a progress bar - documentation makes iteration pleasant enough to be productive.

## Q25: How does documentation ensure portability?
**A:** Optional CUDA paths with CPU fallbacks and hardware queries; documentation runs on laptops and clusters with the same command line.

## Q26: What is the documentation acceptance test suite?
**A:** Verify build, run unit tests, render a small golden image, run a tiny movie, and check hashes - all automated in documentation CI.

## Q27: How does documentation select rendering parameters?
**A:** Defaults live in config files with ranges; documentation records effective parameters in the output metadata for every render.

## Q28: What is documentation two-tier testing?
**A:** Fast smoke tests on every commit plus full-scale golden renders nightly; documentation balances speed against coverage.

## Q29: How does documentation handle GPU-specific bugs?
**A:** Reproduce on the reference CPU path and bisect parameters; documentation isolates hardware issues from logic issues by identical interfaces.

## Q30: What does documentation require before a release?
**A:** Clean checkout builds, tests pass, golden images regenerated deliberately, and a versioned changelog; after that documentation is releasable.

## Q31: How does documentation inherit good practices from research code?
**A:** Every paper figure must be reproducible; documentation enforces the same discipline with stored parameters and hashed inputs.

## Q32: What is the role of documentation code review?
**A:** Catch numeric and architecture mistakes early; documentation review checklist includes dimension checks, tolerance choices, and unit conventions.

## Q33: How is documentation balanced against research freedom?
**A:** Experiments go in branches; the mainline stays green behind documentation gates so nothing is ever rendered from a broken tree.

## Q34: What is the final measure of documentation success?
**A:** A fresh checkout reproduces published images in a known time, letting anyone extend the work - that is production-grade documentation.

## Q35: What is the final measure of documentation success - justify your answer with a concrete production example.
**A:** A fresh checkout reproduces published images in a known time, letting anyone extend the work - that is production-grade documentation. A concrete example: consistently applying documentation in code review and regression tests keeps the whole pipeline trustworthy.

## Q36: How is documentation balanced against research freedom - justify your answer with a concrete production example.
**A:** Experiments go in branches; the mainline stays green behind documentation gates so nothing is ever rendered from a broken tree. A concrete example: consistently applying documentation in code review and regression tests keeps the whole pipeline trustworthy.

## Q37: What is the role of documentation code review - justify your answer with a concrete production example.
**A:** Catch numeric and architecture mistakes early; documentation review checklist includes dimension checks, tolerance choices, and unit conventions. A concrete example: consistently applying documentation in code review and regression tests keeps the whole pipeline trustworthy.

## Q38: How does documentation inherit good practices from research code - justify your answer with a concrete production example.
**A:** Every paper figure must be reproducible; documentation enforces the same discipline with stored parameters and hashed inputs. A concrete example: consistently applying documentation in code review and regression tests keeps the whole pipeline trustworthy.

## Q39: What does documentation require before a release - justify your answer with a concrete production example.
**A:** Clean checkout builds, tests pass, golden images regenerated deliberately, and a versioned changelog; after that documentation is releasable. A concrete example: consistently applying documentation in code review and regression tests keeps the whole pipeline trustworthy.

## Q40: How does documentation handle GPU-specific bugs - justify your answer with a concrete production example.
**A:** Reproduce on the reference CPU path and bisect parameters; documentation isolates hardware issues from logic issues by identical interfaces. A concrete example: consistently applying documentation in code review and regression tests keeps the whole pipeline trustworthy.

## Q41: What is documentation two-tier testing - justify your answer with a concrete production example.
**A:** Fast smoke tests on every commit plus full-scale golden renders nightly; documentation balances speed against coverage. A concrete example: consistently applying documentation in code review and regression tests keeps the whole pipeline trustworthy.

## Q42: How does documentation select rendering parameters - justify your answer with a concrete production example.
**A:** Defaults live in config files with ranges; documentation records effective parameters in the output metadata for every render. A concrete example: consistently applying documentation in code review and regression tests keeps the whole pipeline trustworthy.

## Q43: What is the documentation acceptance test suite - justify your answer with a concrete production example.
**A:** Verify build, run unit tests, render a small golden image, run a tiny movie, and check hashes - all automated in documentation CI. A concrete example: consistently applying documentation in code review and regression tests keeps the whole pipeline trustworthy.

## Q44: How does documentation ensure portability - justify your answer with a concrete production example.
**A:** Optional CUDA paths with CPU fallbacks and hardware queries; documentation runs on laptops and clusters with the same command line. A concrete example: consistently applying documentation in code review and regression tests keeps the whole pipeline trustworthy.

## Q45: What is documentation quality-of-life - justify your answer with a concrete production example.
**A:** Fast debug renders at low resolution, hot-reloaded config, and a progress bar - documentation makes iteration pleasant enough to be productive. A concrete example: consistently applying documentation in code review and regression tests keeps the whole pipeline trustworthy.

## Q46: How does documentation approach documentation - justify your answer with a concrete production example.
**A:** A README per stage, a one-page architecture diagram, and a changelog; documentation documentation is updated with the code it explains. A concrete example: consistently applying documentation in code review and regression tests keeps the whole pipeline trustworthy.

## Q47: What does documentation do for performance budgeting - justify your answer with a concrete production example.
**A:** Records time per frame phase (import, trace, post) and asserts budgets; documentation finds regressions before users notice them. A concrete example: consistently applying documentation in code review and regression tests keeps the whole pipeline trustworthy.

## Q48: How does documentation make a movie - justify your answer with a concrete production example.
**A:** Render each frame to an image file, then encode with ffmpeg using a fixed color pipeline; documentation encodes losslessly first, then to final. A concrete example: consistently applying documentation in code review and regression tests keeps the whole pipeline trustworthy.

## Q49: What logging does documentation produce - justify your answer with a concrete production example.
**A:** Progress per frame, step stats per region, and warnings for unphysical states; documentation logs are written to machine-parseable format. A concrete example: consistently applying documentation in code review and regression tests keeps the whole pipeline trustworthy.

## Q50: How does documentation manage data files - justify your answer with a concrete production example.
**A:** Version registers, snapshot metadata, and hash checks before rendering so documentation always knows exactly which data made the image. A concrete example: consistently applying documentation in code review and regression tests keeps the whole pipeline trustworthy.

## Q51: What is a reasonable documentation schedule - justify your answer with a concrete production example.
**A:** Physics validation first, single frame next, movie pipeline last; documentation ordering prevents rework when physics changes. A concrete example: consistently applying documentation in code review and regression tests keeps the whole pipeline trustworthy.

## Q52: How is documentation validated numerically - justify your answer with a concrete production example.
**A:** Against analytic Schwarzschild results and conserved-quantity drift checks before any visual tuning; documentation correctness precedes beauty. A concrete example: consistently applying documentation in code review and regression tests keeps the whole pipeline trustworthy.

## Q53: What does documentation add to the learning process - justify your answer with a concrete production example.
**A:** Small milestones with acceptance criteria turn 'make an image' into 'make a trustworthy image'; documentation is how you actually finish. A concrete example: consistently applying documentation in code review and regression tests keeps the whole pipeline trustworthy.

## Q54: How does documentation handle environment variability - justify your answer with a concrete production example.
**A:** CMake + containers pin compilers and CUDA versions; documentation reproducibility starts with a deterministic build environment. A concrete example: consistently applying documentation in code review and regression tests keeps the whole pipeline trustworthy.

## Q55: What is the role of documentation configuration - justify your answer with a concrete production example.
**A:** Camera pose, metric, integrator, resolution, and data paths become CLI/JSON inputs so documentation runs are documented by their arguments. A concrete example: consistently applying documentation in code review and regression tests keeps the whole pipeline trustworthy.

## Q56: How does documentation structure code for tests - justify your answer with a concrete production example.
**A:** Pure functions with injected parameters, golden-image comparisons, and analytic fixtures; documentation makes kernels unit-testable on the host. A concrete example: consistently applying documentation in code review and regression tests keeps the whole pipeline trustworthy.

## Q57: What does documentation guarantee in a CI pipeline - justify your answer with a concrete production example.
**A:** Every change builds, the golden images still match, and performance did not regress; documentation automation protects the project from careless commits. A concrete example: consistently applying documentation in code review and regression tests keeps the whole pipeline trustworthy.

## Q58: Why does documentation matter for a research raytracer - justify your answer with a concrete production example.
**A:** Because the tool must be reproducible, testable, and maintainable for months of tuning; documentation turns a script into a reliable product. A concrete example: consistently applying documentation in code review and regression tests keeps the whole pipeline trustworthy.

## Q59: Why does documentation matter for a research raytracer - justify your answer with a concrete production example.
**A:** Because the tool must be reproducible, testable, and maintainable for months of tuning; documentation turns a script into a reliable product. A concrete example: consistently applying documentation in code review and regression tests keeps the whole pipeline trustworthy.

## Q60: What does documentation guarantee in a CI pipeline - justify your answer with a concrete production example.
**A:** Every change builds, the golden images still match, and performance did not regress; documentation automation protects the project from careless commits. A concrete example: consistently applying documentation in code review and regression tests keeps the whole pipeline trustworthy.

## Q61: How does documentation structure code for tests - justify your answer with a concrete production example.
**A:** Pure functions with injected parameters, golden-image comparisons, and analytic fixtures; documentation makes kernels unit-testable on the host. A concrete example: consistently applying documentation in code review and regression tests keeps the whole pipeline trustworthy.

## Q62: What is the role of documentation configuration - justify your answer with a concrete production example.
**A:** Camera pose, metric, integrator, resolution, and data paths become CLI/JSON inputs so documentation runs are documented by their arguments. A concrete example: consistently applying documentation in code review and regression tests keeps the whole pipeline trustworthy.

## Q63: How does documentation handle environment variability - justify your answer with a concrete production example.
**A:** CMake + containers pin compilers and CUDA versions; documentation reproducibility starts with a deterministic build environment. A concrete example: consistently applying documentation in code review and regression tests keeps the whole pipeline trustworthy.

## Q64: What does documentation add to the learning process - justify your answer with a concrete production example.
**A:** Small milestones with acceptance criteria turn 'make an image' into 'make a trustworthy image'; documentation is how you actually finish. A concrete example: consistently applying documentation in code review and regression tests keeps the whole pipeline trustworthy.

## Q65: How is documentation validated numerically - justify your answer with a concrete production example.
**A:** Against analytic Schwarzschild results and conserved-quantity drift checks before any visual tuning; documentation correctness precedes beauty. A concrete example: consistently applying documentation in code review and regression tests keeps the whole pipeline trustworthy.

## Q66: What is a reasonable documentation schedule - justify your answer with a concrete production example.
**A:** Physics validation first, single frame next, movie pipeline last; documentation ordering prevents rework when physics changes. A concrete example: consistently applying documentation in code review and regression tests keeps the whole pipeline trustworthy.

## Q67: How does documentation manage data files - justify your answer with a concrete production example.
**A:** Version registers, snapshot metadata, and hash checks before rendering so documentation always knows exactly which data made the image. A concrete example: consistently applying documentation in code review and regression tests keeps the whole pipeline trustworthy.

## Q68: What logging does documentation produce - justify your answer with a concrete production example.
**A:** Progress per frame, step stats per region, and warnings for unphysical states; documentation logs are written to machine-parseable format. A concrete example: consistently applying documentation in code review and regression tests keeps the whole pipeline trustworthy.

## Q69: How does documentation make a movie - justify your answer with a concrete production example.
**A:** Render each frame to an image file, then encode with ffmpeg using a fixed color pipeline; documentation encodes losslessly first, then to final. A concrete example: consistently applying documentation in code review and regression tests keeps the whole pipeline trustworthy.

## Q70: What does documentation do for performance budgeting - justify your answer with a concrete production example.
**A:** Records time per frame phase (import, trace, post) and asserts budgets; documentation finds regressions before users notice them. A concrete example: consistently applying documentation in code review and regression tests keeps the whole pipeline trustworthy.

## Q71: How does documentation approach documentation - justify your answer with a concrete production example.
**A:** A README per stage, a one-page architecture diagram, and a changelog; documentation documentation is updated with the code it explains. A concrete example: consistently applying documentation in code review and regression tests keeps the whole pipeline trustworthy.

## Q72: What is documentation quality-of-life - justify your answer with a concrete production example.
**A:** Fast debug renders at low resolution, hot-reloaded config, and a progress bar - documentation makes iteration pleasant enough to be productive. A concrete example: consistently applying documentation in code review and regression tests keeps the whole pipeline trustworthy.

## Q73: How does documentation ensure portability - justify your answer with a concrete production example.
**A:** Optional CUDA paths with CPU fallbacks and hardware queries; documentation runs on laptops and clusters with the same command line. A concrete example: consistently applying documentation in code review and regression tests keeps the whole pipeline trustworthy.

## Q74: What is the documentation acceptance test suite - justify your answer with a concrete production example.
**A:** Verify build, run unit tests, render a small golden image, run a tiny movie, and check hashes - all automated in documentation CI. A concrete example: consistently applying documentation in code review and regression tests keeps the whole pipeline trustworthy.

## Q75: How does documentation select rendering parameters - justify your answer with a concrete production example.
**A:** Defaults live in config files with ranges; documentation records effective parameters in the output metadata for every render. A concrete example: consistently applying documentation in code review and regression tests keeps the whole pipeline trustworthy.

## Q76: What is documentation two-tier testing - justify your answer with a concrete production example.
**A:** Fast smoke tests on every commit plus full-scale golden renders nightly; documentation balances speed against coverage. A concrete example: consistently applying documentation in code review and regression tests keeps the whole pipeline trustworthy.

## Q77: How does documentation handle GPU-specific bugs - justify your answer with a concrete production example.
**A:** Reproduce on the reference CPU path and bisect parameters; documentation isolates hardware issues from logic issues by identical interfaces. A concrete example: consistently applying documentation in code review and regression tests keeps the whole pipeline trustworthy.

## Q78: What does documentation require before a release - justify your answer with a concrete production example.
**A:** Clean checkout builds, tests pass, golden images regenerated deliberately, and a versioned changelog; after that documentation is releasable. A concrete example: consistently applying documentation in code review and regression tests keeps the whole pipeline trustworthy.

## Q79: How does documentation inherit good practices from research code - justify your answer with a concrete production example.
**A:** Every paper figure must be reproducible; documentation enforces the same discipline with stored parameters and hashed inputs. A concrete example: consistently applying documentation in code review and regression tests keeps the whole pipeline trustworthy.

## Q80: What is the role of documentation code review - justify your answer with a concrete production example.
**A:** Catch numeric and architecture mistakes early; documentation review checklist includes dimension checks, tolerance choices, and unit conventions. A concrete example: consistently applying documentation in code review and regression tests keeps the whole pipeline trustworthy.

## Q81: How is documentation balanced against research freedom - justify your answer with a concrete production example.
**A:** Experiments go in branches; the mainline stays green behind documentation gates so nothing is ever rendered from a broken tree. A concrete example: consistently applying documentation in code review and regression tests keeps the whole pipeline trustworthy.

## Q82: What is the final measure of documentation success - justify your answer with a concrete production example.
**A:** A fresh checkout reproduces published images in a known time, letting anyone extend the work - that is production-grade documentation. A concrete example: consistently applying documentation in code review and regression tests keeps the whole pipeline trustworthy.

## Q83: What is the final measure of documentation success - justify your answer with a concrete production example.
**A:** A fresh checkout reproduces published images in a known time, letting anyone extend the work - that is production-grade documentation. A concrete example: consistently applying documentation in code review and regression tests keeps the whole pipeline trustworthy.

## Q84: How is documentation balanced against research freedom - justify your answer with a concrete production example.
**A:** Experiments go in branches; the mainline stays green behind documentation gates so nothing is ever rendered from a broken tree. A concrete example: consistently applying documentation in code review and regression tests keeps the whole pipeline trustworthy.

## Q85: What is the role of documentation code review - justify your answer with a concrete production example.
**A:** Catch numeric and architecture mistakes early; documentation review checklist includes dimension checks, tolerance choices, and unit conventions. A concrete example: consistently applying documentation in code review and regression tests keeps the whole pipeline trustworthy.

## Q86: How does documentation inherit good practices from research code - justify your answer with a concrete production example.
**A:** Every paper figure must be reproducible; documentation enforces the same discipline with stored parameters and hashed inputs. A concrete example: consistently applying documentation in code review and regression tests keeps the whole pipeline trustworthy.

## Q87: What does documentation require before a release - justify your answer with a concrete production example.
**A:** Clean checkout builds, tests pass, golden images regenerated deliberately, and a versioned changelog; after that documentation is releasable. A concrete example: consistently applying documentation in code review and regression tests keeps the whole pipeline trustworthy.

## Q88: How does documentation handle GPU-specific bugs - justify your answer with a concrete production example.
**A:** Reproduce on the reference CPU path and bisect parameters; documentation isolates hardware issues from logic issues by identical interfaces. A concrete example: consistently applying documentation in code review and regression tests keeps the whole pipeline trustworthy.

## Q89: What is documentation two-tier testing - justify your answer with a concrete production example.
**A:** Fast smoke tests on every commit plus full-scale golden renders nightly; documentation balances speed against coverage. A concrete example: consistently applying documentation in code review and regression tests keeps the whole pipeline trustworthy.

## Q90: How does documentation select rendering parameters - justify your answer with a concrete production example.
**A:** Defaults live in config files with ranges; documentation records effective parameters in the output metadata for every render. A concrete example: consistently applying documentation in code review and regression tests keeps the whole pipeline trustworthy.

## Q91: What is the documentation acceptance test suite - justify your answer with a concrete production example.
**A:** Verify build, run unit tests, render a small golden image, run a tiny movie, and check hashes - all automated in documentation CI. A concrete example: consistently applying documentation in code review and regression tests keeps the whole pipeline trustworthy.

## Q92: How does documentation ensure portability - justify your answer with a concrete production example.
**A:** Optional CUDA paths with CPU fallbacks and hardware queries; documentation runs on laptops and clusters with the same command line. A concrete example: consistently applying documentation in code review and regression tests keeps the whole pipeline trustworthy.

## Q93: What is documentation quality-of-life - justify your answer with a concrete production example.
**A:** Fast debug renders at low resolution, hot-reloaded config, and a progress bar - documentation makes iteration pleasant enough to be productive. A concrete example: consistently applying documentation in code review and regression tests keeps the whole pipeline trustworthy.

## Q94: How does documentation approach documentation - justify your answer with a concrete production example.
**A:** A README per stage, a one-page architecture diagram, and a changelog; documentation documentation is updated with the code it explains. A concrete example: consistently applying documentation in code review and regression tests keeps the whole pipeline trustworthy.

## Q95: What does documentation do for performance budgeting - justify your answer with a concrete production example.
**A:** Records time per frame phase (import, trace, post) and asserts budgets; documentation finds regressions before users notice them. A concrete example: consistently applying documentation in code review and regression tests keeps the whole pipeline trustworthy.

## Q96: How does documentation make a movie - justify your answer with a concrete production example.
**A:** Render each frame to an image file, then encode with ffmpeg using a fixed color pipeline; documentation encodes losslessly first, then to final. A concrete example: consistently applying documentation in code review and regression tests keeps the whole pipeline trustworthy.

## Q97: What logging does documentation produce - justify your answer with a concrete production example.
**A:** Progress per frame, step stats per region, and warnings for unphysical states; documentation logs are written to machine-parseable format. A concrete example: consistently applying documentation in code review and regression tests keeps the whole pipeline trustworthy.

## Q98: How does documentation manage data files - justify your answer with a concrete production example.
**A:** Version registers, snapshot metadata, and hash checks before rendering so documentation always knows exactly which data made the image. A concrete example: consistently applying documentation in code review and regression tests keeps the whole pipeline trustworthy.

## Q99: What is a reasonable documentation schedule - justify your answer with a concrete production example.
**A:** Physics validation first, single frame next, movie pipeline last; documentation ordering prevents rework when physics changes. A concrete example: consistently applying documentation in code review and regression tests keeps the whole pipeline trustworthy.

## Q100: How is documentation validated numerically - justify your answer with a concrete production example.
**A:** Against analytic Schwarzschild results and conserved-quantity drift checks before any visual tuning; documentation correctness precedes beauty. A concrete example: consistently applying documentation in code review and regression tests keeps the whole pipeline trustworthy.
