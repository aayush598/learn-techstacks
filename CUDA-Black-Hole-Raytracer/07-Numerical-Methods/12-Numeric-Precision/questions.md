# Numerical Methods — Numeric Precision Interview Questions and Answers

## Q1: What numeric types does the integrator use?
**A:** Double (64-bit) for phase-space and metric; floats for emissivity textures and image buffers where the 6-7 digit precision suffices for display.

## Q2: What is the roundoff limit?
**A:** ~ 2^-52 relative on doubles; error control can't push global error below ~1e-13 without compensated arithmetic - never request tighter tolerances.

## Q3: What is catastrophic cancellation?
**A:** Subtracting nearly equal numbers (e.g., r near r+, (r - 2M) small) loses digits; rewrite as (r - r+)*(r - r-) where possible.

## Q4: Where does cancellation bite in GR?
**A:** The Kerr metric terms (r^2 - 2Mr + a^2) and redshift ratios near the horizon - restructure formulas or the adaptive step chases ghosts.

## Q5: What is Kahan compensated summation for the accumulation?
**A:** Summing thousands of ray contributions naively drifts; Kahan/Neumaier summation keeps the running error ~machine-epsilon - a must for the pixels.

## Q6: What is the 'epsilon drift' of conserved quantities?
**A:** p_t/p_phi drift 1e-13 per step with doubles; over 10k steps the total ~1e-9 - acceptable, but monitor it as the integrator's health meter.

## Q7: How do you choose float vs double per stage?
**A:** State, metric, momenta: double; texture/emissivity data and final image: float; keep one 'precision layout' documented to avoid mixed-product surprises.

## Q8: What is the role of long double/quad?
**A:** Available as a fallback near the ring for debugging; production stays double for speed - long double is 2-4x slower and often maps to the same hardware.

## Q9: What are the GPU precision traps?
**A:** Different GPUs compute transcendentals differently; deterministic reproducibility requires fixed (sin/cos/sqrt) function selection and fmaf/FMA discipline.

## Q10: How do you check NaN/Inf?
**A:** Guard the metric and momentum updates: any NaN infects the whole frame - report the ray's initial (pixel, direction) plus step history for the debugger.

## Q11: What is the accumulate normalization precision risk?
**A:** Dividing the pixel sum by N_rays after adding floats loses small contributions; accumulate in double, convert only at I/O.

## Q12: How is determinism validated across runs?
**A:** Same input+tolerances must produce bit-identical frames; if not, audit thread-order reductions and instruction selection - reproducibility's bedrock.

## Q13: What precision does the shadow boundary require?
**A:** Pixel-scale b resolution ~ 0.1%/shadow; double with the guarded metric gives that comfortably - floats alone blur it to ~1%.

## Q14: What is the summary?
**A:** Numeric precision discipline: doubles for physics, compensated sums for outcomes, cancellation-avoiding metric algebra, deterministic GPU math - the foundation of trust.

## Q15: How do you communicate precision settings in logs?
**A:** Log precision plan + residual drift + reproducibility hash with each render - so a downstream claim of '1e-6 shadow' is actually checkable.

## Q16: Why is numeric precision central to geodesic ray tracing?
**A:** The ray trajectory is the solution of an ODE system; numeric precision decides how accurately and cheaply that solution is advanced per pixel.

## Q17: What does numeric precision have to guarantee for correctness?
**A:** Convergence to the analytic geodesic as tolerances shrink and stability across the whole domain - numeric precision failures appear as image artifacts.

## Q18: How is numeric precision chosen for a GPU kernel?
**A:** The scheme must be fixed-step or cheaply adaptive, register-light, and deterministic so numeric precision runs identically on a million parallel threads.

## Q19: What is the typical default integrator for numeric precision?
**A:** Fourth-order Runge-Kutta for its good accuracy-to-cost ratio, upgraded to embedded RK45 when adaptive error control is needed.

## Q20: How does numeric precision handle adaptive step sizes?
**A:** Estimate the local error with two approximations (e.g., RK4 vs RK5), halve/double the step, and maintain a tolerance - classic numeric precision practice.

## Q21: What happens to numeric precision near singularities?
**A:** Steps must shrink dramatically around coordinate and curvature singularities; numeric precision avoids runaway cost by terminating captured rays early.

## Q22: How do you compute the interpolation needed by numeric precision?
**A:** For grid fields, numeric precision uses multilinear interpolation with the cell coordinates; for analytic metrics none is needed at all.

## Q23: What is the role of the affine parameter in numeric precision?
**A:** The parameter governs how fast the state evolves; numeric precision integrates physical time and space the same way, avoiding division-by-zero at turning points.

## Q24: What are the error diagnostics for numeric precision?
**A:** Per-step local error, drift of conserved quantities, and final-impact parameter; numeric precision code monitors all three during development.

## Q25: How does numeric precision achieve determinism?
**A:** Fixed order of operations and epsilon-stable reductions; numeric precision output is identical across runs and across GPUs when the scheme is fixed.

## Q26: What limits real-time numeric precision?
**A:** The integrator cost per ray and rays per frame; numeric precision optimization typically targets the step-evaluation loop which dominates runtime.

## Q27: How is numeric precision verified against analytic results?
**A:** Schwarzschild light deflection, photon orbits, and precession rates have closed forms; numeric precision reproduces them as regression tests.

## Q28: What safeguards protect numeric precision from silent NaN?
**A:** Bounded step sizes, magnitude checks on state, and fail-fast on invalid intermediate values so numeric precision never writes a corrupted frame.

## Q29: How does numeric precision interact with precision?
**A:** Double precision shrinks accumulated error for long grazing trajectories but halves GPU throughput; numeric precision picks the least precision that passes validation.

## Q30: What makes numeric precision hard to debug?
**A:** A single bad step corrupts a whole trajectory; numeric precision debugging isolates by replaying one ray with logging forced on.

## Q31: How do you interpret numeric precision convergence plots?
**A:** Error versus step size on a log-log plot should follow the scheme's order; a discrepancy in numeric precision signals a bug in the step equations.

## Q32: What is the cost model for numeric precision?
**A:** Each step costs a fixed number of metric evaluations; numeric precision budget = evaluations-per-step times steps-per-ray times rays-per-frame.

## Q33: How does numeric precision handle termination for escaped rays?
**A:** An outer radius wall: once the ray exits the computational domain, numeric precision passes control to the background sky mapping.

## Q34: What is the recommended first step in implementing numeric precision?
**A:** Get Euler working on analytic Schwarzschild, then upgrade to RK4 with conserved-quantity drift as the acceptance metric - numeric precision then grows feature by feature.

## Q35: How does numeric precision ensure the photon sphere region is handled?
**A:** Tighter adaptive tolerances and more steps there, since orbits near the sphere are the most error-sensitive structures in numeric precision.

## Q36: What should the interpolation order be for numeric precision?
**A:** Start bilinear/trilinear; cubic reduces imprinting of the simulation cells but costs more - numeric precision validates visually before investing.

## Q37: What are the common failure modes of numeric precision?
**A:** Runaway step growth, step shrink to zero, conserved-quantity drift, and oscillation between grid cells - each has a diagnostic for numeric precision.

## Q38: How is numeric precision benchmarked on hardware?
**A:** Steps per second per thread times active threads measures throughput; numeric precision compares integrators under identical scene settings.

## Q39: What documentation should numeric precision carry?
**A:** The governing ODEs, step-size policy, tolerance defaults, and the known-good parameter set are the minimum numeric precision documentation.

## Q40: What documentation should numeric precision carry - justify your answer with a concrete production example.
**A:** The governing ODEs, step-size policy, tolerance defaults, and the known-good parameter set are the minimum numeric precision documentation. A concrete example: consistently applying numeric precision in code review and regression tests keeps the whole pipeline trustworthy.

## Q41: How is numeric precision benchmarked on hardware - justify your answer with a concrete production example.
**A:** Steps per second per thread times active threads measures throughput; numeric precision compares integrators under identical scene settings. A concrete example: consistently applying numeric precision in code review and regression tests keeps the whole pipeline trustworthy.

## Q42: What are the common failure modes of numeric precision - justify your answer with a concrete production example.
**A:** Runaway step growth, step shrink to zero, conserved-quantity drift, and oscillation between grid cells - each has a diagnostic for numeric precision. A concrete example: consistently applying numeric precision in code review and regression tests keeps the whole pipeline trustworthy.

## Q43: What should the interpolation order be for numeric precision - justify your answer with a concrete production example.
**A:** Start bilinear/trilinear; cubic reduces imprinting of the simulation cells but costs more - numeric precision validates visually before investing. A concrete example: consistently applying numeric precision in code review and regression tests keeps the whole pipeline trustworthy.

## Q44: How does numeric precision ensure the photon sphere region is handled - justify your answer with a concrete production example.
**A:** Tighter adaptive tolerances and more steps there, since orbits near the sphere are the most error-sensitive structures in numeric precision. A concrete example: consistently applying numeric precision in code review and regression tests keeps the whole pipeline trustworthy.

## Q45: What is the recommended first step in implementing numeric precision - justify your answer with a concrete production example.
**A:** Get Euler working on analytic Schwarzschild, then upgrade to RK4 with conserved-quantity drift as the acceptance metric - numeric precision then grows feature by feature. A concrete example: consistently applying numeric precision in code review and regression tests keeps the whole pipeline trustworthy.

## Q46: How does numeric precision handle termination for escaped rays - justify your answer with a concrete production example.
**A:** An outer radius wall: once the ray exits the computational domain, numeric precision passes control to the background sky mapping. A concrete example: consistently applying numeric precision in code review and regression tests keeps the whole pipeline trustworthy.

## Q47: What is the cost model for numeric precision - justify your answer with a concrete production example.
**A:** Each step costs a fixed number of metric evaluations; numeric precision budget = evaluations-per-step times steps-per-ray times rays-per-frame. A concrete example: consistently applying numeric precision in code review and regression tests keeps the whole pipeline trustworthy.

## Q48: How do you interpret numeric precision convergence plots - justify your answer with a concrete production example.
**A:** Error versus step size on a log-log plot should follow the scheme's order; a discrepancy in numeric precision signals a bug in the step equations. A concrete example: consistently applying numeric precision in code review and regression tests keeps the whole pipeline trustworthy.

## Q49: What makes numeric precision hard to debug - justify your answer with a concrete production example.
**A:** A single bad step corrupts a whole trajectory; numeric precision debugging isolates by replaying one ray with logging forced on. A concrete example: consistently applying numeric precision in code review and regression tests keeps the whole pipeline trustworthy.

## Q50: How does numeric precision interact with precision - justify your answer with a concrete production example.
**A:** Double precision shrinks accumulated error for long grazing trajectories but halves GPU throughput; numeric precision picks the least precision that passes validation. A concrete example: consistently applying numeric precision in code review and regression tests keeps the whole pipeline trustworthy.

## Q51: What safeguards protect numeric precision from silent NaN - justify your answer with a concrete production example.
**A:** Bounded step sizes, magnitude checks on state, and fail-fast on invalid intermediate values so numeric precision never writes a corrupted frame. A concrete example: consistently applying numeric precision in code review and regression tests keeps the whole pipeline trustworthy.

## Q52: How is numeric precision verified against analytic results - justify your answer with a concrete production example.
**A:** Schwarzschild light deflection, photon orbits, and precession rates have closed forms; numeric precision reproduces them as regression tests. A concrete example: consistently applying numeric precision in code review and regression tests keeps the whole pipeline trustworthy.

## Q53: What limits real-time numeric precision - justify your answer with a concrete production example.
**A:** The integrator cost per ray and rays per frame; numeric precision optimization typically targets the step-evaluation loop which dominates runtime. A concrete example: consistently applying numeric precision in code review and regression tests keeps the whole pipeline trustworthy.

## Q54: How does numeric precision achieve determinism - justify your answer with a concrete production example.
**A:** Fixed order of operations and epsilon-stable reductions; numeric precision output is identical across runs and across GPUs when the scheme is fixed. A concrete example: consistently applying numeric precision in code review and regression tests keeps the whole pipeline trustworthy.

## Q55: What are the error diagnostics for numeric precision - justify your answer with a concrete production example.
**A:** Per-step local error, drift of conserved quantities, and final-impact parameter; numeric precision code monitors all three during development. A concrete example: consistently applying numeric precision in code review and regression tests keeps the whole pipeline trustworthy.

## Q56: What is the role of the affine parameter in numeric precision - justify your answer with a concrete production example.
**A:** The parameter governs how fast the state evolves; numeric precision integrates physical time and space the same way, avoiding division-by-zero at turning points. A concrete example: consistently applying numeric precision in code review and regression tests keeps the whole pipeline trustworthy.

## Q57: How do you compute the interpolation needed by numeric precision - justify your answer with a concrete production example.
**A:** For grid fields, numeric precision uses multilinear interpolation with the cell coordinates; for analytic metrics none is needed at all. A concrete example: consistently applying numeric precision in code review and regression tests keeps the whole pipeline trustworthy.

## Q58: What happens to numeric precision near singularities - justify your answer with a concrete production example.
**A:** Steps must shrink dramatically around coordinate and curvature singularities; numeric precision avoids runaway cost by terminating captured rays early. A concrete example: consistently applying numeric precision in code review and regression tests keeps the whole pipeline trustworthy.

## Q59: How does numeric precision handle adaptive step sizes - justify your answer with a concrete production example.
**A:** Estimate the local error with two approximations (e.g., RK4 vs RK5), halve/double the step, and maintain a tolerance - classic numeric precision practice. A concrete example: consistently applying numeric precision in code review and regression tests keeps the whole pipeline trustworthy.

## Q60: What is the typical default integrator for numeric precision - justify your answer with a concrete production example.
**A:** Fourth-order Runge-Kutta for its good accuracy-to-cost ratio, upgraded to embedded RK45 when adaptive error control is needed. A concrete example: consistently applying numeric precision in code review and regression tests keeps the whole pipeline trustworthy.

## Q61: How is numeric precision chosen for a GPU kernel - justify your answer with a concrete production example.
**A:** The scheme must be fixed-step or cheaply adaptive, register-light, and deterministic so numeric precision runs identically on a million parallel threads. A concrete example: consistently applying numeric precision in code review and regression tests keeps the whole pipeline trustworthy.

## Q62: What does numeric precision have to guarantee for correctness - justify your answer with a concrete production example.
**A:** Convergence to the analytic geodesic as tolerances shrink and stability across the whole domain - numeric precision failures appear as image artifacts. A concrete example: consistently applying numeric precision in code review and regression tests keeps the whole pipeline trustworthy.

## Q63: Why is numeric precision central to geodesic ray tracing - justify your answer with a concrete production example.
**A:** The ray trajectory is the solution of an ODE system; numeric precision decides how accurately and cheaply that solution is advanced per pixel. A concrete example: consistently applying numeric precision in code review and regression tests keeps the whole pipeline trustworthy.

## Q64: Why is numeric precision central to geodesic ray tracing - justify your answer with a concrete production example.
**A:** The ray trajectory is the solution of an ODE system; numeric precision decides how accurately and cheaply that solution is advanced per pixel. A concrete example: consistently applying numeric precision in code review and regression tests keeps the whole pipeline trustworthy.

## Q65: What does numeric precision have to guarantee for correctness - justify your answer with a concrete production example.
**A:** Convergence to the analytic geodesic as tolerances shrink and stability across the whole domain - numeric precision failures appear as image artifacts. A concrete example: consistently applying numeric precision in code review and regression tests keeps the whole pipeline trustworthy.

## Q66: How is numeric precision chosen for a GPU kernel - justify your answer with a concrete production example.
**A:** The scheme must be fixed-step or cheaply adaptive, register-light, and deterministic so numeric precision runs identically on a million parallel threads. A concrete example: consistently applying numeric precision in code review and regression tests keeps the whole pipeline trustworthy.

## Q67: What is the typical default integrator for numeric precision - justify your answer with a concrete production example.
**A:** Fourth-order Runge-Kutta for its good accuracy-to-cost ratio, upgraded to embedded RK45 when adaptive error control is needed. A concrete example: consistently applying numeric precision in code review and regression tests keeps the whole pipeline trustworthy.

## Q68: How does numeric precision handle adaptive step sizes - justify your answer with a concrete production example.
**A:** Estimate the local error with two approximations (e.g., RK4 vs RK5), halve/double the step, and maintain a tolerance - classic numeric precision practice. A concrete example: consistently applying numeric precision in code review and regression tests keeps the whole pipeline trustworthy.

## Q69: What happens to numeric precision near singularities - justify your answer with a concrete production example.
**A:** Steps must shrink dramatically around coordinate and curvature singularities; numeric precision avoids runaway cost by terminating captured rays early. A concrete example: consistently applying numeric precision in code review and regression tests keeps the whole pipeline trustworthy.

## Q70: How do you compute the interpolation needed by numeric precision - justify your answer with a concrete production example.
**A:** For grid fields, numeric precision uses multilinear interpolation with the cell coordinates; for analytic metrics none is needed at all. A concrete example: consistently applying numeric precision in code review and regression tests keeps the whole pipeline trustworthy.

## Q71: What is the role of the affine parameter in numeric precision - justify your answer with a concrete production example.
**A:** The parameter governs how fast the state evolves; numeric precision integrates physical time and space the same way, avoiding division-by-zero at turning points. A concrete example: consistently applying numeric precision in code review and regression tests keeps the whole pipeline trustworthy.

## Q72: What are the error diagnostics for numeric precision - justify your answer with a concrete production example.
**A:** Per-step local error, drift of conserved quantities, and final-impact parameter; numeric precision code monitors all three during development. A concrete example: consistently applying numeric precision in code review and regression tests keeps the whole pipeline trustworthy.

## Q73: How does numeric precision achieve determinism - justify your answer with a concrete production example.
**A:** Fixed order of operations and epsilon-stable reductions; numeric precision output is identical across runs and across GPUs when the scheme is fixed. A concrete example: consistently applying numeric precision in code review and regression tests keeps the whole pipeline trustworthy.

## Q74: What limits real-time numeric precision - justify your answer with a concrete production example.
**A:** The integrator cost per ray and rays per frame; numeric precision optimization typically targets the step-evaluation loop which dominates runtime. A concrete example: consistently applying numeric precision in code review and regression tests keeps the whole pipeline trustworthy.

## Q75: How is numeric precision verified against analytic results - justify your answer with a concrete production example.
**A:** Schwarzschild light deflection, photon orbits, and precession rates have closed forms; numeric precision reproduces them as regression tests. A concrete example: consistently applying numeric precision in code review and regression tests keeps the whole pipeline trustworthy.

## Q76: What safeguards protect numeric precision from silent NaN - justify your answer with a concrete production example.
**A:** Bounded step sizes, magnitude checks on state, and fail-fast on invalid intermediate values so numeric precision never writes a corrupted frame. A concrete example: consistently applying numeric precision in code review and regression tests keeps the whole pipeline trustworthy.

## Q77: How does numeric precision interact with precision - justify your answer with a concrete production example.
**A:** Double precision shrinks accumulated error for long grazing trajectories but halves GPU throughput; numeric precision picks the least precision that passes validation. A concrete example: consistently applying numeric precision in code review and regression tests keeps the whole pipeline trustworthy.

## Q78: What makes numeric precision hard to debug - justify your answer with a concrete production example.
**A:** A single bad step corrupts a whole trajectory; numeric precision debugging isolates by replaying one ray with logging forced on. A concrete example: consistently applying numeric precision in code review and regression tests keeps the whole pipeline trustworthy.

## Q79: How do you interpret numeric precision convergence plots - justify your answer with a concrete production example.
**A:** Error versus step size on a log-log plot should follow the scheme's order; a discrepancy in numeric precision signals a bug in the step equations. A concrete example: consistently applying numeric precision in code review and regression tests keeps the whole pipeline trustworthy.

## Q80: What is the cost model for numeric precision - justify your answer with a concrete production example.
**A:** Each step costs a fixed number of metric evaluations; numeric precision budget = evaluations-per-step times steps-per-ray times rays-per-frame. A concrete example: consistently applying numeric precision in code review and regression tests keeps the whole pipeline trustworthy.

## Q81: How does numeric precision handle termination for escaped rays - justify your answer with a concrete production example.
**A:** An outer radius wall: once the ray exits the computational domain, numeric precision passes control to the background sky mapping. A concrete example: consistently applying numeric precision in code review and regression tests keeps the whole pipeline trustworthy.

## Q82: What is the recommended first step in implementing numeric precision - justify your answer with a concrete production example.
**A:** Get Euler working on analytic Schwarzschild, then upgrade to RK4 with conserved-quantity drift as the acceptance metric - numeric precision then grows feature by feature. A concrete example: consistently applying numeric precision in code review and regression tests keeps the whole pipeline trustworthy.

## Q83: How does numeric precision ensure the photon sphere region is handled - justify your answer with a concrete production example.
**A:** Tighter adaptive tolerances and more steps there, since orbits near the sphere are the most error-sensitive structures in numeric precision. A concrete example: consistently applying numeric precision in code review and regression tests keeps the whole pipeline trustworthy.

## Q84: What should the interpolation order be for numeric precision - justify your answer with a concrete production example.
**A:** Start bilinear/trilinear; cubic reduces imprinting of the simulation cells but costs more - numeric precision validates visually before investing. A concrete example: consistently applying numeric precision in code review and regression tests keeps the whole pipeline trustworthy.

## Q85: What are the common failure modes of numeric precision - justify your answer with a concrete production example.
**A:** Runaway step growth, step shrink to zero, conserved-quantity drift, and oscillation between grid cells - each has a diagnostic for numeric precision. A concrete example: consistently applying numeric precision in code review and regression tests keeps the whole pipeline trustworthy.

## Q86: How is numeric precision benchmarked on hardware - justify your answer with a concrete production example.
**A:** Steps per second per thread times active threads measures throughput; numeric precision compares integrators under identical scene settings. A concrete example: consistently applying numeric precision in code review and regression tests keeps the whole pipeline trustworthy.

## Q87: What documentation should numeric precision carry - justify your answer with a concrete production example.
**A:** The governing ODEs, step-size policy, tolerance defaults, and the known-good parameter set are the minimum numeric precision documentation. A concrete example: consistently applying numeric precision in code review and regression tests keeps the whole pipeline trustworthy.

## Q88: What documentation should numeric precision carry - justify your answer with a concrete production example.
**A:** The governing ODEs, step-size policy, tolerance defaults, and the known-good parameter set are the minimum numeric precision documentation. A concrete example: consistently applying numeric precision in code review and regression tests keeps the whole pipeline trustworthy.

## Q89: How is numeric precision benchmarked on hardware - justify your answer with a concrete production example.
**A:** Steps per second per thread times active threads measures throughput; numeric precision compares integrators under identical scene settings. A concrete example: consistently applying numeric precision in code review and regression tests keeps the whole pipeline trustworthy.

## Q90: What are the common failure modes of numeric precision - justify your answer with a concrete production example.
**A:** Runaway step growth, step shrink to zero, conserved-quantity drift, and oscillation between grid cells - each has a diagnostic for numeric precision. A concrete example: consistently applying numeric precision in code review and regression tests keeps the whole pipeline trustworthy.

## Q91: What should the interpolation order be for numeric precision - justify your answer with a concrete production example.
**A:** Start bilinear/trilinear; cubic reduces imprinting of the simulation cells but costs more - numeric precision validates visually before investing. A concrete example: consistently applying numeric precision in code review and regression tests keeps the whole pipeline trustworthy.

## Q92: How does numeric precision ensure the photon sphere region is handled - justify your answer with a concrete production example.
**A:** Tighter adaptive tolerances and more steps there, since orbits near the sphere are the most error-sensitive structures in numeric precision. A concrete example: consistently applying numeric precision in code review and regression tests keeps the whole pipeline trustworthy.

## Q93: What is the recommended first step in implementing numeric precision - justify your answer with a concrete production example.
**A:** Get Euler working on analytic Schwarzschild, then upgrade to RK4 with conserved-quantity drift as the acceptance metric - numeric precision then grows feature by feature. A concrete example: consistently applying numeric precision in code review and regression tests keeps the whole pipeline trustworthy.

## Q94: How does numeric precision handle termination for escaped rays - justify your answer with a concrete production example.
**A:** An outer radius wall: once the ray exits the computational domain, numeric precision passes control to the background sky mapping. A concrete example: consistently applying numeric precision in code review and regression tests keeps the whole pipeline trustworthy.

## Q95: What is the cost model for numeric precision - justify your answer with a concrete production example.
**A:** Each step costs a fixed number of metric evaluations; numeric precision budget = evaluations-per-step times steps-per-ray times rays-per-frame. A concrete example: consistently applying numeric precision in code review and regression tests keeps the whole pipeline trustworthy.

## Q96: How do you interpret numeric precision convergence plots - justify your answer with a concrete production example.
**A:** Error versus step size on a log-log plot should follow the scheme's order; a discrepancy in numeric precision signals a bug in the step equations. A concrete example: consistently applying numeric precision in code review and regression tests keeps the whole pipeline trustworthy.

## Q97: What makes numeric precision hard to debug - justify your answer with a concrete production example.
**A:** A single bad step corrupts a whole trajectory; numeric precision debugging isolates by replaying one ray with logging forced on. A concrete example: consistently applying numeric precision in code review and regression tests keeps the whole pipeline trustworthy.

## Q98: How does numeric precision interact with precision - justify your answer with a concrete production example.
**A:** Double precision shrinks accumulated error for long grazing trajectories but halves GPU throughput; numeric precision picks the least precision that passes validation. A concrete example: consistently applying numeric precision in code review and regression tests keeps the whole pipeline trustworthy.

## Q99: What safeguards protect numeric precision from silent NaN - justify your answer with a concrete production example.
**A:** Bounded step sizes, magnitude checks on state, and fail-fast on invalid intermediate values so numeric precision never writes a corrupted frame. A concrete example: consistently applying numeric precision in code review and regression tests keeps the whole pipeline trustworthy.

## Q100: How is numeric precision verified against analytic results - justify your answer with a concrete production example.
**A:** Schwarzschild light deflection, photon orbits, and precession rates have closed forms; numeric precision reproduces them as regression tests. A concrete example: consistently applying numeric precision in code review and regression tests keeps the whole pipeline trustworthy.
