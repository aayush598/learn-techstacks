# Numerical Methods — Error Control Interview Questions and Answers

## Q1: What is the purpose of error control?
**A:** To keep the GLOBAL solution error within a defined tolerance while spending the minimum number of derivative evaluations - quality at minimum cost.

## Q2: What is local vs global error?
**A:** Local: the error committed in ONE step; global: accumulated over the whole path. Global ~ local_error * (number_of_steps)^(1/2) for random, or ~ n*local for systematic drift.

## Q3: How do you choose atol vs rtol?
**A:** atol sets the absolute floor (protects near-zero states), rtol the relative scale; geodesics use rtol-dominated settings with a tiny atol.

## Q4: What is the 'step accepted but wrong' failure?
**A:** Local error passes, but the solution has drifted off the null shell (H != 0): the null residual must be independently monitored as a physical error.

## Q5: What is the error estimator's validity?
**A:** Embedded pairs estimate LOCAL error to one order higher; using it as GLOBAL tolerance is an approximation - validate globally a few times.

## Q6: What is the role of the null-residual monitor?
**A:** Track |2H| = |p^2| along the ray; if it exceeds a bound (e.g., 1e-8 of E^2), subdivide the next step - a safeguard independent of step size.

## Q7: How is error distributed over space?
**A:** The controller makes local error uniform; regions of high curvature (ring) get more steps - this 'equidistribution' is exactly what you want for smooth imaging.

## Q8: What is the effect of tolerance on shadow edge sharpness?
**A:** Tolerances too loose blur the capture boundary (rays misclassify); tighter tolerances sharpen it at cost - a quality knob, not a physics toggle.

## Q9: What does IEEE/roundoff impose?
**A:** Roundoff ~ 1e-16 per operation; error control can't see below ~1e-14 on doubles - never ask for tighter tolerances, they silently plateau.

## Q10: What is a 'swamp' of rejected steps?
**A:** Near a steep fold the controller bounces between acceptance/rejection; a bounded step count with last-step fallback avoids wasted iterations.

## Q11: How do you validate error control?
**A:** Compare a reference high-tolerance integration against looser runs for a set of representative rays; the shadow boundary must stabilize monotonically.

## Q12: What is the cost model of a rejection?
**A:** A rejected step wastes its stages AND forces a re-evaluation - keep rejection < 15% or the adaptivity budget evaporates.

## Q13: How does error control interact with emission?
**A:** Emissivity sampled at accepted steps is consistent with the trajectory; error-controlled integration doubles as the quadrature grid - no mismatch.

## Q14: What is the golden rule?
**A:** Set error control to the worst-case NEED (ring resolution), then verify globally - never trust local control without a full-path residual check.

## Q15: What is the summary?
**A:** Error control balances accuracy and cost: local embedded estimates + null-residual monitoring + global validation - the contract of the integrator's quality.

## Q16: Why is error control central to geodesic ray tracing?
**A:** The ray trajectory is the solution of an ODE system; error control decides how accurately and cheaply that solution is advanced per pixel.

## Q17: What does error control have to guarantee for correctness?
**A:** Convergence to the analytic geodesic as tolerances shrink and stability across the whole domain - error control failures appear as image artifacts.

## Q18: How is error control chosen for a GPU kernel?
**A:** The scheme must be fixed-step or cheaply adaptive, register-light, and deterministic so error control runs identically on a million parallel threads.

## Q19: What is the typical default integrator for error control?
**A:** Fourth-order Runge-Kutta for its good accuracy-to-cost ratio, upgraded to embedded RK45 when adaptive error control is needed.

## Q20: How does error control handle adaptive step sizes?
**A:** Estimate the local error with two approximations (e.g., RK4 vs RK5), halve/double the step, and maintain a tolerance - classic error control practice.

## Q21: What happens to error control near singularities?
**A:** Steps must shrink dramatically around coordinate and curvature singularities; error control avoids runaway cost by terminating captured rays early.

## Q22: How do you compute the interpolation needed by error control?
**A:** For grid fields, error control uses multilinear interpolation with the cell coordinates; for analytic metrics none is needed at all.

## Q23: What is the role of the affine parameter in error control?
**A:** The parameter governs how fast the state evolves; error control integrates physical time and space the same way, avoiding division-by-zero at turning points.

## Q24: What are the error diagnostics for error control?
**A:** Per-step local error, drift of conserved quantities, and final-impact parameter; error control code monitors all three during development.

## Q25: How does error control achieve determinism?
**A:** Fixed order of operations and epsilon-stable reductions; error control output is identical across runs and across GPUs when the scheme is fixed.

## Q26: What limits real-time error control?
**A:** The integrator cost per ray and rays per frame; error control optimization typically targets the step-evaluation loop which dominates runtime.

## Q27: How is error control verified against analytic results?
**A:** Schwarzschild light deflection, photon orbits, and precession rates have closed forms; error control reproduces them as regression tests.

## Q28: What safeguards protect error control from silent NaN?
**A:** Bounded step sizes, magnitude checks on state, and fail-fast on invalid intermediate values so error control never writes a corrupted frame.

## Q29: How does error control interact with precision?
**A:** Double precision shrinks accumulated error for long grazing trajectories but halves GPU throughput; error control picks the least precision that passes validation.

## Q30: What makes error control hard to debug?
**A:** A single bad step corrupts a whole trajectory; error control debugging isolates by replaying one ray with logging forced on.

## Q31: How do you interpret error control convergence plots?
**A:** Error versus step size on a log-log plot should follow the scheme's order; a discrepancy in error control signals a bug in the step equations.

## Q32: What is the cost model for error control?
**A:** Each step costs a fixed number of metric evaluations; error control budget = evaluations-per-step times steps-per-ray times rays-per-frame.

## Q33: How does error control handle termination for escaped rays?
**A:** An outer radius wall: once the ray exits the computational domain, error control passes control to the background sky mapping.

## Q34: What is the recommended first step in implementing error control?
**A:** Get Euler working on analytic Schwarzschild, then upgrade to RK4 with conserved-quantity drift as the acceptance metric - error control then grows feature by feature.

## Q35: How does error control ensure the photon sphere region is handled?
**A:** Tighter adaptive tolerances and more steps there, since orbits near the sphere are the most error-sensitive structures in error control.

## Q36: What should the interpolation order be for error control?
**A:** Start bilinear/trilinear; cubic reduces imprinting of the simulation cells but costs more - error control validates visually before investing.

## Q37: What are the common failure modes of error control?
**A:** Runaway step growth, step shrink to zero, conserved-quantity drift, and oscillation between grid cells - each has a diagnostic for error control.

## Q38: How is error control benchmarked on hardware?
**A:** Steps per second per thread times active threads measures throughput; error control compares integrators under identical scene settings.

## Q39: What documentation should error control carry?
**A:** The governing ODEs, step-size policy, tolerance defaults, and the known-good parameter set are the minimum error control documentation.

## Q40: What documentation should error control carry - justify your answer with a concrete production example.
**A:** The governing ODEs, step-size policy, tolerance defaults, and the known-good parameter set are the minimum error control documentation. A concrete example: consistently applying error control in code review and regression tests keeps the whole pipeline trustworthy.

## Q41: How is error control benchmarked on hardware - justify your answer with a concrete production example.
**A:** Steps per second per thread times active threads measures throughput; error control compares integrators under identical scene settings. A concrete example: consistently applying error control in code review and regression tests keeps the whole pipeline trustworthy.

## Q42: What are the common failure modes of error control - justify your answer with a concrete production example.
**A:** Runaway step growth, step shrink to zero, conserved-quantity drift, and oscillation between grid cells - each has a diagnostic for error control. A concrete example: consistently applying error control in code review and regression tests keeps the whole pipeline trustworthy.

## Q43: What should the interpolation order be for error control - justify your answer with a concrete production example.
**A:** Start bilinear/trilinear; cubic reduces imprinting of the simulation cells but costs more - error control validates visually before investing. A concrete example: consistently applying error control in code review and regression tests keeps the whole pipeline trustworthy.

## Q44: How does error control ensure the photon sphere region is handled - justify your answer with a concrete production example.
**A:** Tighter adaptive tolerances and more steps there, since orbits near the sphere are the most error-sensitive structures in error control. A concrete example: consistently applying error control in code review and regression tests keeps the whole pipeline trustworthy.

## Q45: What is the recommended first step in implementing error control - justify your answer with a concrete production example.
**A:** Get Euler working on analytic Schwarzschild, then upgrade to RK4 with conserved-quantity drift as the acceptance metric - error control then grows feature by feature. A concrete example: consistently applying error control in code review and regression tests keeps the whole pipeline trustworthy.

## Q46: How does error control handle termination for escaped rays - justify your answer with a concrete production example.
**A:** An outer radius wall: once the ray exits the computational domain, error control passes control to the background sky mapping. A concrete example: consistently applying error control in code review and regression tests keeps the whole pipeline trustworthy.

## Q47: What is the cost model for error control - justify your answer with a concrete production example.
**A:** Each step costs a fixed number of metric evaluations; error control budget = evaluations-per-step times steps-per-ray times rays-per-frame. A concrete example: consistently applying error control in code review and regression tests keeps the whole pipeline trustworthy.

## Q48: How do you interpret error control convergence plots - justify your answer with a concrete production example.
**A:** Error versus step size on a log-log plot should follow the scheme's order; a discrepancy in error control signals a bug in the step equations. A concrete example: consistently applying error control in code review and regression tests keeps the whole pipeline trustworthy.

## Q49: What makes error control hard to debug - justify your answer with a concrete production example.
**A:** A single bad step corrupts a whole trajectory; error control debugging isolates by replaying one ray with logging forced on. A concrete example: consistently applying error control in code review and regression tests keeps the whole pipeline trustworthy.

## Q50: How does error control interact with precision - justify your answer with a concrete production example.
**A:** Double precision shrinks accumulated error for long grazing trajectories but halves GPU throughput; error control picks the least precision that passes validation. A concrete example: consistently applying error control in code review and regression tests keeps the whole pipeline trustworthy.

## Q51: What safeguards protect error control from silent NaN - justify your answer with a concrete production example.
**A:** Bounded step sizes, magnitude checks on state, and fail-fast on invalid intermediate values so error control never writes a corrupted frame. A concrete example: consistently applying error control in code review and regression tests keeps the whole pipeline trustworthy.

## Q52: How is error control verified against analytic results - justify your answer with a concrete production example.
**A:** Schwarzschild light deflection, photon orbits, and precession rates have closed forms; error control reproduces them as regression tests. A concrete example: consistently applying error control in code review and regression tests keeps the whole pipeline trustworthy.

## Q53: What limits real-time error control - justify your answer with a concrete production example.
**A:** The integrator cost per ray and rays per frame; error control optimization typically targets the step-evaluation loop which dominates runtime. A concrete example: consistently applying error control in code review and regression tests keeps the whole pipeline trustworthy.

## Q54: How does error control achieve determinism - justify your answer with a concrete production example.
**A:** Fixed order of operations and epsilon-stable reductions; error control output is identical across runs and across GPUs when the scheme is fixed. A concrete example: consistently applying error control in code review and regression tests keeps the whole pipeline trustworthy.

## Q55: What are the error diagnostics for error control - justify your answer with a concrete production example.
**A:** Per-step local error, drift of conserved quantities, and final-impact parameter; error control code monitors all three during development. A concrete example: consistently applying error control in code review and regression tests keeps the whole pipeline trustworthy.

## Q56: What is the role of the affine parameter in error control - justify your answer with a concrete production example.
**A:** The parameter governs how fast the state evolves; error control integrates physical time and space the same way, avoiding division-by-zero at turning points. A concrete example: consistently applying error control in code review and regression tests keeps the whole pipeline trustworthy.

## Q57: How do you compute the interpolation needed by error control - justify your answer with a concrete production example.
**A:** For grid fields, error control uses multilinear interpolation with the cell coordinates; for analytic metrics none is needed at all. A concrete example: consistently applying error control in code review and regression tests keeps the whole pipeline trustworthy.

## Q58: What happens to error control near singularities - justify your answer with a concrete production example.
**A:** Steps must shrink dramatically around coordinate and curvature singularities; error control avoids runaway cost by terminating captured rays early. A concrete example: consistently applying error control in code review and regression tests keeps the whole pipeline trustworthy.

## Q59: How does error control handle adaptive step sizes - justify your answer with a concrete production example.
**A:** Estimate the local error with two approximations (e.g., RK4 vs RK5), halve/double the step, and maintain a tolerance - classic error control practice. A concrete example: consistently applying error control in code review and regression tests keeps the whole pipeline trustworthy.

## Q60: What is the typical default integrator for error control - justify your answer with a concrete production example.
**A:** Fourth-order Runge-Kutta for its good accuracy-to-cost ratio, upgraded to embedded RK45 when adaptive error control is needed. A concrete example: consistently applying error control in code review and regression tests keeps the whole pipeline trustworthy.

## Q61: How is error control chosen for a GPU kernel - justify your answer with a concrete production example.
**A:** The scheme must be fixed-step or cheaply adaptive, register-light, and deterministic so error control runs identically on a million parallel threads. A concrete example: consistently applying error control in code review and regression tests keeps the whole pipeline trustworthy.

## Q62: What does error control have to guarantee for correctness - justify your answer with a concrete production example.
**A:** Convergence to the analytic geodesic as tolerances shrink and stability across the whole domain - error control failures appear as image artifacts. A concrete example: consistently applying error control in code review and regression tests keeps the whole pipeline trustworthy.

## Q63: Why is error control central to geodesic ray tracing - justify your answer with a concrete production example.
**A:** The ray trajectory is the solution of an ODE system; error control decides how accurately and cheaply that solution is advanced per pixel. A concrete example: consistently applying error control in code review and regression tests keeps the whole pipeline trustworthy.

## Q64: Why is error control central to geodesic ray tracing - justify your answer with a concrete production example.
**A:** The ray trajectory is the solution of an ODE system; error control decides how accurately and cheaply that solution is advanced per pixel. A concrete example: consistently applying error control in code review and regression tests keeps the whole pipeline trustworthy.

## Q65: What does error control have to guarantee for correctness - justify your answer with a concrete production example.
**A:** Convergence to the analytic geodesic as tolerances shrink and stability across the whole domain - error control failures appear as image artifacts. A concrete example: consistently applying error control in code review and regression tests keeps the whole pipeline trustworthy.

## Q66: How is error control chosen for a GPU kernel - justify your answer with a concrete production example.
**A:** The scheme must be fixed-step or cheaply adaptive, register-light, and deterministic so error control runs identically on a million parallel threads. A concrete example: consistently applying error control in code review and regression tests keeps the whole pipeline trustworthy.

## Q67: What is the typical default integrator for error control - justify your answer with a concrete production example.
**A:** Fourth-order Runge-Kutta for its good accuracy-to-cost ratio, upgraded to embedded RK45 when adaptive error control is needed. A concrete example: consistently applying error control in code review and regression tests keeps the whole pipeline trustworthy.

## Q68: How does error control handle adaptive step sizes - justify your answer with a concrete production example.
**A:** Estimate the local error with two approximations (e.g., RK4 vs RK5), halve/double the step, and maintain a tolerance - classic error control practice. A concrete example: consistently applying error control in code review and regression tests keeps the whole pipeline trustworthy.

## Q69: What happens to error control near singularities - justify your answer with a concrete production example.
**A:** Steps must shrink dramatically around coordinate and curvature singularities; error control avoids runaway cost by terminating captured rays early. A concrete example: consistently applying error control in code review and regression tests keeps the whole pipeline trustworthy.

## Q70: How do you compute the interpolation needed by error control - justify your answer with a concrete production example.
**A:** For grid fields, error control uses multilinear interpolation with the cell coordinates; for analytic metrics none is needed at all. A concrete example: consistently applying error control in code review and regression tests keeps the whole pipeline trustworthy.

## Q71: What is the role of the affine parameter in error control - justify your answer with a concrete production example.
**A:** The parameter governs how fast the state evolves; error control integrates physical time and space the same way, avoiding division-by-zero at turning points. A concrete example: consistently applying error control in code review and regression tests keeps the whole pipeline trustworthy.

## Q72: What are the error diagnostics for error control - justify your answer with a concrete production example.
**A:** Per-step local error, drift of conserved quantities, and final-impact parameter; error control code monitors all three during development. A concrete example: consistently applying error control in code review and regression tests keeps the whole pipeline trustworthy.

## Q73: How does error control achieve determinism - justify your answer with a concrete production example.
**A:** Fixed order of operations and epsilon-stable reductions; error control output is identical across runs and across GPUs when the scheme is fixed. A concrete example: consistently applying error control in code review and regression tests keeps the whole pipeline trustworthy.

## Q74: What limits real-time error control - justify your answer with a concrete production example.
**A:** The integrator cost per ray and rays per frame; error control optimization typically targets the step-evaluation loop which dominates runtime. A concrete example: consistently applying error control in code review and regression tests keeps the whole pipeline trustworthy.

## Q75: How is error control verified against analytic results - justify your answer with a concrete production example.
**A:** Schwarzschild light deflection, photon orbits, and precession rates have closed forms; error control reproduces them as regression tests. A concrete example: consistently applying error control in code review and regression tests keeps the whole pipeline trustworthy.

## Q76: What safeguards protect error control from silent NaN - justify your answer with a concrete production example.
**A:** Bounded step sizes, magnitude checks on state, and fail-fast on invalid intermediate values so error control never writes a corrupted frame. A concrete example: consistently applying error control in code review and regression tests keeps the whole pipeline trustworthy.

## Q77: How does error control interact with precision - justify your answer with a concrete production example.
**A:** Double precision shrinks accumulated error for long grazing trajectories but halves GPU throughput; error control picks the least precision that passes validation. A concrete example: consistently applying error control in code review and regression tests keeps the whole pipeline trustworthy.

## Q78: What makes error control hard to debug - justify your answer with a concrete production example.
**A:** A single bad step corrupts a whole trajectory; error control debugging isolates by replaying one ray with logging forced on. A concrete example: consistently applying error control in code review and regression tests keeps the whole pipeline trustworthy.

## Q79: How do you interpret error control convergence plots - justify your answer with a concrete production example.
**A:** Error versus step size on a log-log plot should follow the scheme's order; a discrepancy in error control signals a bug in the step equations. A concrete example: consistently applying error control in code review and regression tests keeps the whole pipeline trustworthy.

## Q80: What is the cost model for error control - justify your answer with a concrete production example.
**A:** Each step costs a fixed number of metric evaluations; error control budget = evaluations-per-step times steps-per-ray times rays-per-frame. A concrete example: consistently applying error control in code review and regression tests keeps the whole pipeline trustworthy.

## Q81: How does error control handle termination for escaped rays - justify your answer with a concrete production example.
**A:** An outer radius wall: once the ray exits the computational domain, error control passes control to the background sky mapping. A concrete example: consistently applying error control in code review and regression tests keeps the whole pipeline trustworthy.

## Q82: What is the recommended first step in implementing error control - justify your answer with a concrete production example.
**A:** Get Euler working on analytic Schwarzschild, then upgrade to RK4 with conserved-quantity drift as the acceptance metric - error control then grows feature by feature. A concrete example: consistently applying error control in code review and regression tests keeps the whole pipeline trustworthy.

## Q83: How does error control ensure the photon sphere region is handled - justify your answer with a concrete production example.
**A:** Tighter adaptive tolerances and more steps there, since orbits near the sphere are the most error-sensitive structures in error control. A concrete example: consistently applying error control in code review and regression tests keeps the whole pipeline trustworthy.

## Q84: What should the interpolation order be for error control - justify your answer with a concrete production example.
**A:** Start bilinear/trilinear; cubic reduces imprinting of the simulation cells but costs more - error control validates visually before investing. A concrete example: consistently applying error control in code review and regression tests keeps the whole pipeline trustworthy.

## Q85: What are the common failure modes of error control - justify your answer with a concrete production example.
**A:** Runaway step growth, step shrink to zero, conserved-quantity drift, and oscillation between grid cells - each has a diagnostic for error control. A concrete example: consistently applying error control in code review and regression tests keeps the whole pipeline trustworthy.

## Q86: How is error control benchmarked on hardware - justify your answer with a concrete production example.
**A:** Steps per second per thread times active threads measures throughput; error control compares integrators under identical scene settings. A concrete example: consistently applying error control in code review and regression tests keeps the whole pipeline trustworthy.

## Q87: What documentation should error control carry - justify your answer with a concrete production example.
**A:** The governing ODEs, step-size policy, tolerance defaults, and the known-good parameter set are the minimum error control documentation. A concrete example: consistently applying error control in code review and regression tests keeps the whole pipeline trustworthy.

## Q88: What documentation should error control carry - justify your answer with a concrete production example.
**A:** The governing ODEs, step-size policy, tolerance defaults, and the known-good parameter set are the minimum error control documentation. A concrete example: consistently applying error control in code review and regression tests keeps the whole pipeline trustworthy.

## Q89: How is error control benchmarked on hardware - justify your answer with a concrete production example.
**A:** Steps per second per thread times active threads measures throughput; error control compares integrators under identical scene settings. A concrete example: consistently applying error control in code review and regression tests keeps the whole pipeline trustworthy.

## Q90: What are the common failure modes of error control - justify your answer with a concrete production example.
**A:** Runaway step growth, step shrink to zero, conserved-quantity drift, and oscillation between grid cells - each has a diagnostic for error control. A concrete example: consistently applying error control in code review and regression tests keeps the whole pipeline trustworthy.

## Q91: What should the interpolation order be for error control - justify your answer with a concrete production example.
**A:** Start bilinear/trilinear; cubic reduces imprinting of the simulation cells but costs more - error control validates visually before investing. A concrete example: consistently applying error control in code review and regression tests keeps the whole pipeline trustworthy.

## Q92: How does error control ensure the photon sphere region is handled - justify your answer with a concrete production example.
**A:** Tighter adaptive tolerances and more steps there, since orbits near the sphere are the most error-sensitive structures in error control. A concrete example: consistently applying error control in code review and regression tests keeps the whole pipeline trustworthy.

## Q93: What is the recommended first step in implementing error control - justify your answer with a concrete production example.
**A:** Get Euler working on analytic Schwarzschild, then upgrade to RK4 with conserved-quantity drift as the acceptance metric - error control then grows feature by feature. A concrete example: consistently applying error control in code review and regression tests keeps the whole pipeline trustworthy.

## Q94: How does error control handle termination for escaped rays - justify your answer with a concrete production example.
**A:** An outer radius wall: once the ray exits the computational domain, error control passes control to the background sky mapping. A concrete example: consistently applying error control in code review and regression tests keeps the whole pipeline trustworthy.

## Q95: What is the cost model for error control - justify your answer with a concrete production example.
**A:** Each step costs a fixed number of metric evaluations; error control budget = evaluations-per-step times steps-per-ray times rays-per-frame. A concrete example: consistently applying error control in code review and regression tests keeps the whole pipeline trustworthy.

## Q96: How do you interpret error control convergence plots - justify your answer with a concrete production example.
**A:** Error versus step size on a log-log plot should follow the scheme's order; a discrepancy in error control signals a bug in the step equations. A concrete example: consistently applying error control in code review and regression tests keeps the whole pipeline trustworthy.

## Q97: What makes error control hard to debug - justify your answer with a concrete production example.
**A:** A single bad step corrupts a whole trajectory; error control debugging isolates by replaying one ray with logging forced on. A concrete example: consistently applying error control in code review and regression tests keeps the whole pipeline trustworthy.

## Q98: How does error control interact with precision - justify your answer with a concrete production example.
**A:** Double precision shrinks accumulated error for long grazing trajectories but halves GPU throughput; error control picks the least precision that passes validation. A concrete example: consistently applying error control in code review and regression tests keeps the whole pipeline trustworthy.

## Q99: What safeguards protect error control from silent NaN - justify your answer with a concrete production example.
**A:** Bounded step sizes, magnitude checks on state, and fail-fast on invalid intermediate values so error control never writes a corrupted frame. A concrete example: consistently applying error control in code review and regression tests keeps the whole pipeline trustworthy.

## Q100: How is error control verified against analytic results - justify your answer with a concrete production example.
**A:** Schwarzschild light deflection, photon orbits, and precession rates have closed forms; error control reproduces them as regression tests. A concrete example: consistently applying error control in code review and regression tests keeps the whole pipeline trustworthy.
