# Gr Ray Tracing — Integration Strategy Interview Questions and Answers

## Q1: What is the adaptive-step strategy?
**A:** Step size selected from local error estimates (RK vs embedded, or null-residual size); doubling/halving keeps accuracy while bounding cost.

## Q2: What scheme do production codes use?
**A:** Dormand-Prince (rk45) or velocity-Verlet/symplectic variants; performance-tuned code compiles to AVX-512/FP16-GEMM kernels or uses graph-compiled engines at millions of rays/sec.

## Q3: How do you choose the initial step?
**A:** From the local inverse derivative scale (e.g., dlambda ~ h0 * M / |p|), then the controller quantifies; avoiding giant first jumps near the horizon matters.

## Q4: What is the rejection loop?
**A:** Each trial step compares two orders; on failure the step retries smaller - the near-ring rejection cost is the main accuracy/cost tradeoff of the code.

## Q5: How is the derivative kernel vectorized?
**A:** The metric+derivative evaluation is a pure function of (r, cos theta); batch it: SIMD across rays with fixed lambda, feeding the integrator per SIMD-lane.

## Q6: What is the halo/threshold r_max for termination?
**A:** Rays that reach r > r_out (e.g., 2000M) without a hit are 'missed' - termination guarantees linear cost, no wandering after the geometry does its work.

## Q7: How are crossings found (disk/horizon)?
**A:** Bracketing (sign change of r - r_isp or r - r+) between steps, then a bisection/regdsolve to refine the crossing - precise hit positions without extra integration.

## Q8: What precision does the shadow need?
**A:** Pixel-scale: relative errors 1e-6 keep ring boundary clean; the camera supersample covers the rest - no need for long double globally.

## Q9: How do you reuse work across frames?
**A:** Static-geometry cache: precompute b/phi maps and the capture table once per (a, i); only the emission/velocity changes per frame - the real production optimization.

## Q10: What is the memory layout for ray batches?
**A:** Structure-of-arrays: (r,theta,phi,p_r,p_theta,p_phi,t) as separate arrays so SIMD/L1 work flat; a batch = a warp of rays with a common adaptive step.

## Q11: What is the stopping criterion on conserved residuals?
**A:** Where H drift exceeds a threshold (indicating lost symplecticity), subdivide/re-seed the ray - the safety valve against silent integration drift.

## Q12: How does the strategy adapt near the photon sphere?
**A:** A cluster detector (rdot transitions, winding counter) triggers step reduction while within a factor of b_crit - the targeted way to resolve rings cheaply.

## Q13: What about the affine parameter blowups in t?
**A:** t integrates fine but grows; keep t saved as a separate offset double and only accumulate it at output to avoid losing precision.

## Q14: What is the validation workflow of the integrator?
**A:** A regression suite: circular orbit closure, deflection asymptotic, shadow boundary, beaming map - every refactor of integration strategy must re-pass.

## Q15: What is the recommended architecture summary?
**A:** Adaptive rk45 in SIMD-batched form, chart-switching to KS at the horizon, analytic shadow seeding, supersample only the boundary - the full strategy in one line.

## Q16: What does integration strategy concretely do inside the raytracer?
**A:** It advances photon trajectories in the curved spacetime, applying the equations of motion so each camera ray follows a true null geodesic.

## Q17: Why is integration strategy the heart of a black-hole visualizer?
**A:** Every visual signature - lensing, photon ring, shadow, redshift - emerges from exactly how integration strategy bends and time-shifts each ray.

## Q18: How is integration strategy implemented on the GPU?
**A:** As a numerical integration loop in device code with per-ray state in registers, stepping through integration strategy until the ray is captured or escapes.

## Q19: What are the two families of integration for integration strategy?
**A:** The direct geodesic integration of the equations of motion, and Hamilton-Jacobi reduced systems using conserved constants; integration strategy chooses per codebase.

## Q20: How do you validate integration strategy?
**A:** Reproduce the analytic Schwarzschild lensing angle, the photon ring, and the projected shadow shape measured against published figures.

## Q21: What is the typical step-size strategy in integration strategy?
**A:** Adaptive stepping that refines near the photon sphere and the horizon, where integration strategy gradients are steepest and error grows fastest.

## Q22: What state does the integrator track for integration strategy?
**A:** Position, four-momentum components, affine parameter, and accumulated redshift - integration strategy state vector is small enough to fit in registers.

## Q23: How does integration strategy handle captured photons?
**A:** It terminates integration at the horizon and records absorption; integration strategy distinguishes capture from scatter by the radial turning point.

## Q24: What role do conserved constants play in integration strategy?
**A:** They let you solve impact parameters analytically or prune impossible trajectories, dramatically speeding integration strategy for large image grids.

## Q25: Describe the numerical error budget of integration strategy.
**A:** Per-step truncation error and accumulated drift; integration strategy budgets a relative tolerance and verifies the final image is stable.

## Q26: How does integration strategy map the sky to the image plane?
**A:** Each image pixel defines an initial direction; integration strategy evolves that direction backward in time until it leaves the domain to a background sky or hits the disk.

## Q27: What is the most common bug in integration strategy?
**A:** A sign error in the equations of motion or a wrong coordinate transformation that produces plausible-but-wrong lensing; integration strategy needs golden-image regression tests.

## Q28: How do you parallelize integration strategy?
**A:** Every pixel is an independent integration strategy problem, so one thread per ray gives embarrassingly parallel behavior with no inter-thread communication.

## Q29: What determines the visual shadow size in integration strategy?
**A:** The photon sphere and horizon geometry: captured rays draw the shadow whose boundary in integration strategy is the photon ring.

## Q30: When do you need full Kerr integration strategy instead of Schwarzschild?
**A:** Whenever the disk's rotation and frame dragging matter - most real astrophysical images; integration strategy must support spin to be credible.

## Q31: What is the 'second/third image' vocabulary of integration strategy?
**A:** Light winding around the black hole produces multiple images; integration strategy naturally produces the primary, secondary, and higher-order photon ring.

## Q32: How does integration strategy produce the bright thin ring?
**A:** Rays that graze the photon sphere travel long path lengths through the brightest disk region, so averaged intensity peaks at the integration strategy critical impact parameter.

## Q33: How does integration strategy decide frequencies for render?
**A:** It integrates the redshift factor along the ray; integration strategy multiplies emitted frequency by it before applying the transfer equation.

## Q34: What modes does integration strategy render the accretion disk?
**A:** First as a geometric emitter grid, later using GRMHD data; integration strategy is agnostic to the source as long as it can query emissivity along the path.

## Q35: How is integration strategy performance quantified?
**A:** Mega-rays per second and time per frame; integration strategy usually spends its budget in the integration loop, so its step count is the key metric.

## Q36: What is the effect of camera position in integration strategy?
**A:** Face-on, edge-on, and plunging camera setups change the projected ring shape; integration strategy validates each against known renders.

## Q37: How does integration strategy incorporate the disk's fluid velocity?
**A:** Doppler and beaming appear when the emissivity frame is boosted; integration strategy applies that boost per photon ray path segment.

## Q38: What is the horizon-catching strategy in integration strategy?
**A:** Rather than refine forever, you flag a ray as captured once r drops below the horizon radius; integration strategy then terminates that lane.

## Q39: How should you commission integration strategy output?
**A:** Side-by-side with published stills of the same metric and camera to confirm lensing, ring, and shadow match within a few percent.

## Q40: How should you commission integration strategy output - justify your answer with a concrete production example.
**A:** Side-by-side with published stills of the same metric and camera to confirm lensing, ring, and shadow match within a few percent. A concrete example: consistently applying integration strategy in code review and regression tests keeps the whole pipeline trustworthy.

## Q41: What is the horizon-catching strategy in integration strategy - justify your answer with a concrete production example.
**A:** Rather than refine forever, you flag a ray as captured once r drops below the horizon radius; integration strategy then terminates that lane. A concrete example: consistently applying integration strategy in code review and regression tests keeps the whole pipeline trustworthy.

## Q42: How does integration strategy incorporate the disk's fluid velocity - justify your answer with a concrete production example.
**A:** Doppler and beaming appear when the emissivity frame is boosted; integration strategy applies that boost per photon ray path segment. A concrete example: consistently applying integration strategy in code review and regression tests keeps the whole pipeline trustworthy.

## Q43: What is the effect of camera position in integration strategy - justify your answer with a concrete production example.
**A:** Face-on, edge-on, and plunging camera setups change the projected ring shape; integration strategy validates each against known renders. A concrete example: consistently applying integration strategy in code review and regression tests keeps the whole pipeline trustworthy.

## Q44: How is integration strategy performance quantified - justify your answer with a concrete production example.
**A:** Mega-rays per second and time per frame; integration strategy usually spends its budget in the integration loop, so its step count is the key metric. A concrete example: consistently applying integration strategy in code review and regression tests keeps the whole pipeline trustworthy.

## Q45: What modes does integration strategy render the accretion disk - justify your answer with a concrete production example.
**A:** First as a geometric emitter grid, later using GRMHD data; integration strategy is agnostic to the source as long as it can query emissivity along the path. A concrete example: consistently applying integration strategy in code review and regression tests keeps the whole pipeline trustworthy.

## Q46: How does integration strategy decide frequencies for render - justify your answer with a concrete production example.
**A:** It integrates the redshift factor along the ray; integration strategy multiplies emitted frequency by it before applying the transfer equation. A concrete example: consistently applying integration strategy in code review and regression tests keeps the whole pipeline trustworthy.

## Q47: How does integration strategy produce the bright thin ring - justify your answer with a concrete production example.
**A:** Rays that graze the photon sphere travel long path lengths through the brightest disk region, so averaged intensity peaks at the integration strategy critical impact parameter. A concrete example: consistently applying integration strategy in code review and regression tests keeps the whole pipeline trustworthy.

## Q48: What is the 'second/third image' vocabulary of integration strategy - justify your answer with a concrete production example.
**A:** Light winding around the black hole produces multiple images; integration strategy naturally produces the primary, secondary, and higher-order photon ring. A concrete example: consistently applying integration strategy in code review and regression tests keeps the whole pipeline trustworthy.

## Q49: When do you need full Kerr integration strategy instead of Schwarzschild - justify your answer with a concrete production example.
**A:** Whenever the disk's rotation and frame dragging matter - most real astrophysical images; integration strategy must support spin to be credible. A concrete example: consistently applying integration strategy in code review and regression tests keeps the whole pipeline trustworthy.

## Q50: What determines the visual shadow size in integration strategy - justify your answer with a concrete production example.
**A:** The photon sphere and horizon geometry: captured rays draw the shadow whose boundary in integration strategy is the photon ring. A concrete example: consistently applying integration strategy in code review and regression tests keeps the whole pipeline trustworthy.

## Q51: How do you parallelize integration strategy - justify your answer with a concrete production example.
**A:** Every pixel is an independent integration strategy problem, so one thread per ray gives embarrassingly parallel behavior with no inter-thread communication. A concrete example: consistently applying integration strategy in code review and regression tests keeps the whole pipeline trustworthy.

## Q52: What is the most common bug in integration strategy - justify your answer with a concrete production example.
**A:** A sign error in the equations of motion or a wrong coordinate transformation that produces plausible-but-wrong lensing; integration strategy needs golden-image regression tests. A concrete example: consistently applying integration strategy in code review and regression tests keeps the whole pipeline trustworthy.

## Q53: How does integration strategy map the sky to the image plane - justify your answer with a concrete production example.
**A:** Each image pixel defines an initial direction; integration strategy evolves that direction backward in time until it leaves the domain to a background sky or hits the disk. A concrete example: consistently applying integration strategy in code review and regression tests keeps the whole pipeline trustworthy.

## Q54: Describe the numerical error budget of integration strategy - justify your answer with a concrete production example.
**A:** Per-step truncation error and accumulated drift; integration strategy budgets a relative tolerance and verifies the final image is stable. A concrete example: consistently applying integration strategy in code review and regression tests keeps the whole pipeline trustworthy.

## Q55: What role do conserved constants play in integration strategy - justify your answer with a concrete production example.
**A:** They let you solve impact parameters analytically or prune impossible trajectories, dramatically speeding integration strategy for large image grids. A concrete example: consistently applying integration strategy in code review and regression tests keeps the whole pipeline trustworthy.

## Q56: How does integration strategy handle captured photons - justify your answer with a concrete production example.
**A:** It terminates integration at the horizon and records absorption; integration strategy distinguishes capture from scatter by the radial turning point. A concrete example: consistently applying integration strategy in code review and regression tests keeps the whole pipeline trustworthy.

## Q57: What state does the integrator track for integration strategy - justify your answer with a concrete production example.
**A:** Position, four-momentum components, affine parameter, and accumulated redshift - integration strategy state vector is small enough to fit in registers. A concrete example: consistently applying integration strategy in code review and regression tests keeps the whole pipeline trustworthy.

## Q58: What is the typical step-size strategy in integration strategy - justify your answer with a concrete production example.
**A:** Adaptive stepping that refines near the photon sphere and the horizon, where integration strategy gradients are steepest and error grows fastest. A concrete example: consistently applying integration strategy in code review and regression tests keeps the whole pipeline trustworthy.

## Q59: How do you validate integration strategy - justify your answer with a concrete production example.
**A:** Reproduce the analytic Schwarzschild lensing angle, the photon ring, and the projected shadow shape measured against published figures. A concrete example: consistently applying integration strategy in code review and regression tests keeps the whole pipeline trustworthy.

## Q60: What are the two families of integration for integration strategy - justify your answer with a concrete production example.
**A:** The direct geodesic integration of the equations of motion, and Hamilton-Jacobi reduced systems using conserved constants; integration strategy chooses per codebase. A concrete example: consistently applying integration strategy in code review and regression tests keeps the whole pipeline trustworthy.

## Q61: How is integration strategy implemented on the GPU - justify your answer with a concrete production example.
**A:** As a numerical integration loop in device code with per-ray state in registers, stepping through integration strategy until the ray is captured or escapes. A concrete example: consistently applying integration strategy in code review and regression tests keeps the whole pipeline trustworthy.

## Q62: Why is integration strategy the heart of a black-hole visualizer - justify your answer with a concrete production example.
**A:** Every visual signature - lensing, photon ring, shadow, redshift - emerges from exactly how integration strategy bends and time-shifts each ray. A concrete example: consistently applying integration strategy in code review and regression tests keeps the whole pipeline trustworthy.

## Q63: What does integration strategy concretely do inside the raytracer - justify your answer with a concrete production example.
**A:** It advances photon trajectories in the curved spacetime, applying the equations of motion so each camera ray follows a true null geodesic. A concrete example: consistently applying integration strategy in code review and regression tests keeps the whole pipeline trustworthy.

## Q64: What does integration strategy concretely do inside the raytracer - justify your answer with a concrete production example.
**A:** It advances photon trajectories in the curved spacetime, applying the equations of motion so each camera ray follows a true null geodesic. A concrete example: consistently applying integration strategy in code review and regression tests keeps the whole pipeline trustworthy.

## Q65: Why is integration strategy the heart of a black-hole visualizer - justify your answer with a concrete production example.
**A:** Every visual signature - lensing, photon ring, shadow, redshift - emerges from exactly how integration strategy bends and time-shifts each ray. A concrete example: consistently applying integration strategy in code review and regression tests keeps the whole pipeline trustworthy.

## Q66: How is integration strategy implemented on the GPU - justify your answer with a concrete production example.
**A:** As a numerical integration loop in device code with per-ray state in registers, stepping through integration strategy until the ray is captured or escapes. A concrete example: consistently applying integration strategy in code review and regression tests keeps the whole pipeline trustworthy.

## Q67: What are the two families of integration for integration strategy - justify your answer with a concrete production example.
**A:** The direct geodesic integration of the equations of motion, and Hamilton-Jacobi reduced systems using conserved constants; integration strategy chooses per codebase. A concrete example: consistently applying integration strategy in code review and regression tests keeps the whole pipeline trustworthy.

## Q68: How do you validate integration strategy - justify your answer with a concrete production example.
**A:** Reproduce the analytic Schwarzschild lensing angle, the photon ring, and the projected shadow shape measured against published figures. A concrete example: consistently applying integration strategy in code review and regression tests keeps the whole pipeline trustworthy.

## Q69: What is the typical step-size strategy in integration strategy - justify your answer with a concrete production example.
**A:** Adaptive stepping that refines near the photon sphere and the horizon, where integration strategy gradients are steepest and error grows fastest. A concrete example: consistently applying integration strategy in code review and regression tests keeps the whole pipeline trustworthy.

## Q70: What state does the integrator track for integration strategy - justify your answer with a concrete production example.
**A:** Position, four-momentum components, affine parameter, and accumulated redshift - integration strategy state vector is small enough to fit in registers. A concrete example: consistently applying integration strategy in code review and regression tests keeps the whole pipeline trustworthy.

## Q71: How does integration strategy handle captured photons - justify your answer with a concrete production example.
**A:** It terminates integration at the horizon and records absorption; integration strategy distinguishes capture from scatter by the radial turning point. A concrete example: consistently applying integration strategy in code review and regression tests keeps the whole pipeline trustworthy.

## Q72: What role do conserved constants play in integration strategy - justify your answer with a concrete production example.
**A:** They let you solve impact parameters analytically or prune impossible trajectories, dramatically speeding integration strategy for large image grids. A concrete example: consistently applying integration strategy in code review and regression tests keeps the whole pipeline trustworthy.

## Q73: Describe the numerical error budget of integration strategy - justify your answer with a concrete production example.
**A:** Per-step truncation error and accumulated drift; integration strategy budgets a relative tolerance and verifies the final image is stable. A concrete example: consistently applying integration strategy in code review and regression tests keeps the whole pipeline trustworthy.

## Q74: How does integration strategy map the sky to the image plane - justify your answer with a concrete production example.
**A:** Each image pixel defines an initial direction; integration strategy evolves that direction backward in time until it leaves the domain to a background sky or hits the disk. A concrete example: consistently applying integration strategy in code review and regression tests keeps the whole pipeline trustworthy.

## Q75: What is the most common bug in integration strategy - justify your answer with a concrete production example.
**A:** A sign error in the equations of motion or a wrong coordinate transformation that produces plausible-but-wrong lensing; integration strategy needs golden-image regression tests. A concrete example: consistently applying integration strategy in code review and regression tests keeps the whole pipeline trustworthy.

## Q76: How do you parallelize integration strategy - justify your answer with a concrete production example.
**A:** Every pixel is an independent integration strategy problem, so one thread per ray gives embarrassingly parallel behavior with no inter-thread communication. A concrete example: consistently applying integration strategy in code review and regression tests keeps the whole pipeline trustworthy.

## Q77: What determines the visual shadow size in integration strategy - justify your answer with a concrete production example.
**A:** The photon sphere and horizon geometry: captured rays draw the shadow whose boundary in integration strategy is the photon ring. A concrete example: consistently applying integration strategy in code review and regression tests keeps the whole pipeline trustworthy.

## Q78: When do you need full Kerr integration strategy instead of Schwarzschild - justify your answer with a concrete production example.
**A:** Whenever the disk's rotation and frame dragging matter - most real astrophysical images; integration strategy must support spin to be credible. A concrete example: consistently applying integration strategy in code review and regression tests keeps the whole pipeline trustworthy.

## Q79: What is the 'second/third image' vocabulary of integration strategy - justify your answer with a concrete production example.
**A:** Light winding around the black hole produces multiple images; integration strategy naturally produces the primary, secondary, and higher-order photon ring. A concrete example: consistently applying integration strategy in code review and regression tests keeps the whole pipeline trustworthy.

## Q80: How does integration strategy produce the bright thin ring - justify your answer with a concrete production example.
**A:** Rays that graze the photon sphere travel long path lengths through the brightest disk region, so averaged intensity peaks at the integration strategy critical impact parameter. A concrete example: consistently applying integration strategy in code review and regression tests keeps the whole pipeline trustworthy.

## Q81: How does integration strategy decide frequencies for render - justify your answer with a concrete production example.
**A:** It integrates the redshift factor along the ray; integration strategy multiplies emitted frequency by it before applying the transfer equation. A concrete example: consistently applying integration strategy in code review and regression tests keeps the whole pipeline trustworthy.

## Q82: What modes does integration strategy render the accretion disk - justify your answer with a concrete production example.
**A:** First as a geometric emitter grid, later using GRMHD data; integration strategy is agnostic to the source as long as it can query emissivity along the path. A concrete example: consistently applying integration strategy in code review and regression tests keeps the whole pipeline trustworthy.

## Q83: How is integration strategy performance quantified - justify your answer with a concrete production example.
**A:** Mega-rays per second and time per frame; integration strategy usually spends its budget in the integration loop, so its step count is the key metric. A concrete example: consistently applying integration strategy in code review and regression tests keeps the whole pipeline trustworthy.

## Q84: What is the effect of camera position in integration strategy - justify your answer with a concrete production example.
**A:** Face-on, edge-on, and plunging camera setups change the projected ring shape; integration strategy validates each against known renders. A concrete example: consistently applying integration strategy in code review and regression tests keeps the whole pipeline trustworthy.

## Q85: How does integration strategy incorporate the disk's fluid velocity - justify your answer with a concrete production example.
**A:** Doppler and beaming appear when the emissivity frame is boosted; integration strategy applies that boost per photon ray path segment. A concrete example: consistently applying integration strategy in code review and regression tests keeps the whole pipeline trustworthy.

## Q86: What is the horizon-catching strategy in integration strategy - justify your answer with a concrete production example.
**A:** Rather than refine forever, you flag a ray as captured once r drops below the horizon radius; integration strategy then terminates that lane. A concrete example: consistently applying integration strategy in code review and regression tests keeps the whole pipeline trustworthy.

## Q87: How should you commission integration strategy output - justify your answer with a concrete production example.
**A:** Side-by-side with published stills of the same metric and camera to confirm lensing, ring, and shadow match within a few percent. A concrete example: consistently applying integration strategy in code review and regression tests keeps the whole pipeline trustworthy.

## Q88: How should you commission integration strategy output - justify your answer with a concrete production example.
**A:** Side-by-side with published stills of the same metric and camera to confirm lensing, ring, and shadow match within a few percent. A concrete example: consistently applying integration strategy in code review and regression tests keeps the whole pipeline trustworthy.

## Q89: What is the horizon-catching strategy in integration strategy - justify your answer with a concrete production example.
**A:** Rather than refine forever, you flag a ray as captured once r drops below the horizon radius; integration strategy then terminates that lane. A concrete example: consistently applying integration strategy in code review and regression tests keeps the whole pipeline trustworthy.

## Q90: How does integration strategy incorporate the disk's fluid velocity - justify your answer with a concrete production example.
**A:** Doppler and beaming appear when the emissivity frame is boosted; integration strategy applies that boost per photon ray path segment. A concrete example: consistently applying integration strategy in code review and regression tests keeps the whole pipeline trustworthy.

## Q91: What is the effect of camera position in integration strategy - justify your answer with a concrete production example.
**A:** Face-on, edge-on, and plunging camera setups change the projected ring shape; integration strategy validates each against known renders. A concrete example: consistently applying integration strategy in code review and regression tests keeps the whole pipeline trustworthy.

## Q92: How is integration strategy performance quantified - justify your answer with a concrete production example.
**A:** Mega-rays per second and time per frame; integration strategy usually spends its budget in the integration loop, so its step count is the key metric. A concrete example: consistently applying integration strategy in code review and regression tests keeps the whole pipeline trustworthy.

## Q93: What modes does integration strategy render the accretion disk - justify your answer with a concrete production example.
**A:** First as a geometric emitter grid, later using GRMHD data; integration strategy is agnostic to the source as long as it can query emissivity along the path. A concrete example: consistently applying integration strategy in code review and regression tests keeps the whole pipeline trustworthy.

## Q94: How does integration strategy decide frequencies for render - justify your answer with a concrete production example.
**A:** It integrates the redshift factor along the ray; integration strategy multiplies emitted frequency by it before applying the transfer equation. A concrete example: consistently applying integration strategy in code review and regression tests keeps the whole pipeline trustworthy.

## Q95: How does integration strategy produce the bright thin ring - justify your answer with a concrete production example.
**A:** Rays that graze the photon sphere travel long path lengths through the brightest disk region, so averaged intensity peaks at the integration strategy critical impact parameter. A concrete example: consistently applying integration strategy in code review and regression tests keeps the whole pipeline trustworthy.

## Q96: What is the 'second/third image' vocabulary of integration strategy - justify your answer with a concrete production example.
**A:** Light winding around the black hole produces multiple images; integration strategy naturally produces the primary, secondary, and higher-order photon ring. A concrete example: consistently applying integration strategy in code review and regression tests keeps the whole pipeline trustworthy.

## Q97: When do you need full Kerr integration strategy instead of Schwarzschild - justify your answer with a concrete production example.
**A:** Whenever the disk's rotation and frame dragging matter - most real astrophysical images; integration strategy must support spin to be credible. A concrete example: consistently applying integration strategy in code review and regression tests keeps the whole pipeline trustworthy.

## Q98: What determines the visual shadow size in integration strategy - justify your answer with a concrete production example.
**A:** The photon sphere and horizon geometry: captured rays draw the shadow whose boundary in integration strategy is the photon ring. A concrete example: consistently applying integration strategy in code review and regression tests keeps the whole pipeline trustworthy.

## Q99: How do you parallelize integration strategy - justify your answer with a concrete production example.
**A:** Every pixel is an independent integration strategy problem, so one thread per ray gives embarrassingly parallel behavior with no inter-thread communication. A concrete example: consistently applying integration strategy in code review and regression tests keeps the whole pipeline trustworthy.

## Q100: What is the most common bug in integration strategy - justify your answer with a concrete production example.
**A:** A sign error in the equations of motion or a wrong coordinate transformation that produces plausible-but-wrong lensing; integration strategy needs golden-image regression tests. A concrete example: consistently applying integration strategy in code review and regression tests keeps the whole pipeline trustworthy.
