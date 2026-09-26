# Gr Ray Tracing — Kerr Geodesic Integration Interview Questions and Answers

## Q1: What is the challenge of integrating Kerr geodesics numerically?
**A:** The metric couples r-theta strongly and near the photon sphere the solutions become hyper-sensitive (chaotic sensitivities) - integrators must be adaptive and quasi-symplectic.

## Q2: What is the canonical integrator choice?
**A:** An adaptive 4th/5th-order RK (Dormand-Prince) with step control from the null-residual, or symplectic schemes where affordable for long rays.

## Q3: How is the step size controlled?
**A:** Compute two estimates of (x, p) per step and shrink/expand via local tolerance; the null residual gives a physical error floor.

## Q4: What variables are integrated?
**A:** The 8 phase-space coordinates (x^mu, p_mu) over affine lambda; or the 2-OD reduced HJ pair in (r, theta) when separating.

## Q5: How do you handle the equatorial case?
**A:** theta=pi/2 reduces to 1-D (with sigma=r^2); the integrator then cross-checks the analytic solutions in 2D for fast, high-precision validation.

## Q6: What is 'crossing the horizon' numerically?
**A:** Detect r < r+ with chord sampling; tall rays that cross get marked captured - the flag is tested when the radial step crosses threshold.

## Q7: What about the polar singularity?
**A:** At theta ~ 0 the phi-derivatives blow up in BL; code must either cross via coordinate handling or keep r-del methods.


## Q8: What is the sensitivity near the photon ring?
**A:** b near b_crit produces winding instability; error amplifies - hence high precision (long double / compensated) near the ring segment.

## Q9: What is the usual adaptive error budget?
**A:** Relative 1e-10-1e-12 with moderate oversampling keeps shadow/ring errors below a pixel; too-tight budgets blow cost near the ring.

## Q10: How do you seed the ray's momenta for a given pixel?
**A:** Convert the pixel's direction to Bishop frame components, obtain p_mu = g xdot with the null condition fixing the overall scale.

## Q11: What is the scheme's symplecticity guarantee?
**A:** The flow is Hamiltonian; non-symplectic RK drifts H slowly over many steps - symplectic/integrator variants preserve conserved quantities far longer.

## Q12: What performance vs accuracy trade exists?
**A:** Every rejection costs a re-step; near the ring rejection inflates cost, so a good predictor (e.g., analytic turning-point guess) is worth the code.

## Q13: What output record does a ray produce?
**A:** Hit or miss/capture, the t-arrival, the redshift, the accumulated polarization, and r_theta of hit - the building blocks of the sampler.

## Q14: How do you recover analytic boundary geometry?
**A:** The boundary separatrix in (b, gamma) that separates capture from scatter is double-root of V_r; numeric integration of its neighbors validates the code.

## Q15: How do you test long integration stability?
**A:** Integrate a closed orbit for hundreds of periods; trajectory closure and conserved p_t drift at 1e-12 = pass, drift = reset.

## Q16: What does kerr geodesic integration concretely do inside the raytracer?
**A:** It advances photon trajectories in the curved spacetime, applying the equations of motion so each camera ray follows a true null geodesic.

## Q17: Why is kerr geodesic integration the heart of a black-hole visualizer?
**A:** Every visual signature - lensing, photon ring, shadow, redshift - emerges from exactly how kerr geodesic integration bends and time-shifts each ray.

## Q18: How is kerr geodesic integration implemented on the GPU?
**A:** As a numerical integration loop in device code with per-ray state in registers, stepping through kerr geodesic integration until the ray is captured or escapes.

## Q19: What are the two families of integration for kerr geodesic integration?
**A:** The direct geodesic integration of the equations of motion, and Hamilton-Jacobi reduced systems using conserved constants; kerr geodesic integration chooses per codebase.

## Q20: How do you validate kerr geodesic integration?
**A:** Reproduce the analytic Schwarzschild lensing angle, the photon ring, and the projected shadow shape measured against published figures.

## Q21: What is the typical step-size strategy in kerr geodesic integration?
**A:** Adaptive stepping that refines near the photon sphere and the horizon, where kerr geodesic integration gradients are steepest and error grows fastest.

## Q22: What state does the integrator track for kerr geodesic integration?
**A:** Position, four-momentum components, affine parameter, and accumulated redshift - kerr geodesic integration state vector is small enough to fit in registers.

## Q23: How does kerr geodesic integration handle captured photons?
**A:** It terminates integration at the horizon and records absorption; kerr geodesic integration distinguishes capture from scatter by the radial turning point.

## Q24: What role do conserved constants play in kerr geodesic integration?
**A:** They let you solve impact parameters analytically or prune impossible trajectories, dramatically speeding kerr geodesic integration for large image grids.

## Q25: Describe the numerical error budget of kerr geodesic integration.
**A:** Per-step truncation error and accumulated drift; kerr geodesic integration budgets a relative tolerance and verifies the final image is stable.

## Q26: How does kerr geodesic integration map the sky to the image plane?
**A:** Each image pixel defines an initial direction; kerr geodesic integration evolves that direction backward in time until it leaves the domain to a background sky or hits the disk.

## Q27: What is the most common bug in kerr geodesic integration?
**A:** A sign error in the equations of motion or a wrong coordinate transformation that produces plausible-but-wrong lensing; kerr geodesic integration needs golden-image regression tests.

## Q28: How do you parallelize kerr geodesic integration?
**A:** Every pixel is an independent kerr geodesic integration problem, so one thread per ray gives embarrassingly parallel behavior with no inter-thread communication.

## Q29: What determines the visual shadow size in kerr geodesic integration?
**A:** The photon sphere and horizon geometry: captured rays draw the shadow whose boundary in kerr geodesic integration is the photon ring.

## Q30: When do you need full Kerr kerr geodesic integration instead of Schwarzschild?
**A:** Whenever the disk's rotation and frame dragging matter - most real astrophysical images; kerr geodesic integration must support spin to be credible.

## Q31: What is the 'second/third image' vocabulary of kerr geodesic integration?
**A:** Light winding around the black hole produces multiple images; kerr geodesic integration naturally produces the primary, secondary, and higher-order photon ring.

## Q32: How does kerr geodesic integration produce the bright thin ring?
**A:** Rays that graze the photon sphere travel long path lengths through the brightest disk region, so averaged intensity peaks at the kerr geodesic integration critical impact parameter.

## Q33: How does kerr geodesic integration decide frequencies for render?
**A:** It integrates the redshift factor along the ray; kerr geodesic integration multiplies emitted frequency by it before applying the transfer equation.

## Q34: What modes does kerr geodesic integration render the accretion disk?
**A:** First as a geometric emitter grid, later using GRMHD data; kerr geodesic integration is agnostic to the source as long as it can query emissivity along the path.

## Q35: How is kerr geodesic integration performance quantified?
**A:** Mega-rays per second and time per frame; kerr geodesic integration usually spends its budget in the integration loop, so its step count is the key metric.

## Q36: What is the effect of camera position in kerr geodesic integration?
**A:** Face-on, edge-on, and plunging camera setups change the projected ring shape; kerr geodesic integration validates each against known renders.

## Q37: How does kerr geodesic integration incorporate the disk's fluid velocity?
**A:** Doppler and beaming appear when the emissivity frame is boosted; kerr geodesic integration applies that boost per photon ray path segment.

## Q38: What is the horizon-catching strategy in kerr geodesic integration?
**A:** Rather than refine forever, you flag a ray as captured once r drops below the horizon radius; kerr geodesic integration then terminates that lane.

## Q39: How should you commission kerr geodesic integration output?
**A:** Side-by-side with published stills of the same metric and camera to confirm lensing, ring, and shadow match within a few percent.

## Q40: How should you commission kerr geodesic integration output - justify your answer with a concrete production example.
**A:** Side-by-side with published stills of the same metric and camera to confirm lensing, ring, and shadow match within a few percent. A concrete example: consistently applying kerr geodesic integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q41: What is the horizon-catching strategy in kerr geodesic integration - justify your answer with a concrete production example.
**A:** Rather than refine forever, you flag a ray as captured once r drops below the horizon radius; kerr geodesic integration then terminates that lane. A concrete example: consistently applying kerr geodesic integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q42: How does kerr geodesic integration incorporate the disk's fluid velocity - justify your answer with a concrete production example.
**A:** Doppler and beaming appear when the emissivity frame is boosted; kerr geodesic integration applies that boost per photon ray path segment. A concrete example: consistently applying kerr geodesic integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q43: What is the effect of camera position in kerr geodesic integration - justify your answer with a concrete production example.
**A:** Face-on, edge-on, and plunging camera setups change the projected ring shape; kerr geodesic integration validates each against known renders. A concrete example: consistently applying kerr geodesic integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q44: How is kerr geodesic integration performance quantified - justify your answer with a concrete production example.
**A:** Mega-rays per second and time per frame; kerr geodesic integration usually spends its budget in the integration loop, so its step count is the key metric. A concrete example: consistently applying kerr geodesic integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q45: What modes does kerr geodesic integration render the accretion disk - justify your answer with a concrete production example.
**A:** First as a geometric emitter grid, later using GRMHD data; kerr geodesic integration is agnostic to the source as long as it can query emissivity along the path. A concrete example: consistently applying kerr geodesic integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q46: How does kerr geodesic integration decide frequencies for render - justify your answer with a concrete production example.
**A:** It integrates the redshift factor along the ray; kerr geodesic integration multiplies emitted frequency by it before applying the transfer equation. A concrete example: consistently applying kerr geodesic integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q47: How does kerr geodesic integration produce the bright thin ring - justify your answer with a concrete production example.
**A:** Rays that graze the photon sphere travel long path lengths through the brightest disk region, so averaged intensity peaks at the kerr geodesic integration critical impact parameter. A concrete example: consistently applying kerr geodesic integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q48: What is the 'second/third image' vocabulary of kerr geodesic integration - justify your answer with a concrete production example.
**A:** Light winding around the black hole produces multiple images; kerr geodesic integration naturally produces the primary, secondary, and higher-order photon ring. A concrete example: consistently applying kerr geodesic integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q49: When do you need full Kerr kerr geodesic integration instead of Schwarzschild - justify your answer with a concrete production example.
**A:** Whenever the disk's rotation and frame dragging matter - most real astrophysical images; kerr geodesic integration must support spin to be credible. A concrete example: consistently applying kerr geodesic integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q50: What determines the visual shadow size in kerr geodesic integration - justify your answer with a concrete production example.
**A:** The photon sphere and horizon geometry: captured rays draw the shadow whose boundary in kerr geodesic integration is the photon ring. A concrete example: consistently applying kerr geodesic integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q51: How do you parallelize kerr geodesic integration - justify your answer with a concrete production example.
**A:** Every pixel is an independent kerr geodesic integration problem, so one thread per ray gives embarrassingly parallel behavior with no inter-thread communication. A concrete example: consistently applying kerr geodesic integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q52: What is the most common bug in kerr geodesic integration - justify your answer with a concrete production example.
**A:** A sign error in the equations of motion or a wrong coordinate transformation that produces plausible-but-wrong lensing; kerr geodesic integration needs golden-image regression tests. A concrete example: consistently applying kerr geodesic integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q53: How does kerr geodesic integration map the sky to the image plane - justify your answer with a concrete production example.
**A:** Each image pixel defines an initial direction; kerr geodesic integration evolves that direction backward in time until it leaves the domain to a background sky or hits the disk. A concrete example: consistently applying kerr geodesic integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q54: Describe the numerical error budget of kerr geodesic integration - justify your answer with a concrete production example.
**A:** Per-step truncation error and accumulated drift; kerr geodesic integration budgets a relative tolerance and verifies the final image is stable. A concrete example: consistently applying kerr geodesic integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q55: What role do conserved constants play in kerr geodesic integration - justify your answer with a concrete production example.
**A:** They let you solve impact parameters analytically or prune impossible trajectories, dramatically speeding kerr geodesic integration for large image grids. A concrete example: consistently applying kerr geodesic integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q56: How does kerr geodesic integration handle captured photons - justify your answer with a concrete production example.
**A:** It terminates integration at the horizon and records absorption; kerr geodesic integration distinguishes capture from scatter by the radial turning point. A concrete example: consistently applying kerr geodesic integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q57: What state does the integrator track for kerr geodesic integration - justify your answer with a concrete production example.
**A:** Position, four-momentum components, affine parameter, and accumulated redshift - kerr geodesic integration state vector is small enough to fit in registers. A concrete example: consistently applying kerr geodesic integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q58: What is the typical step-size strategy in kerr geodesic integration - justify your answer with a concrete production example.
**A:** Adaptive stepping that refines near the photon sphere and the horizon, where kerr geodesic integration gradients are steepest and error grows fastest. A concrete example: consistently applying kerr geodesic integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q59: How do you validate kerr geodesic integration - justify your answer with a concrete production example.
**A:** Reproduce the analytic Schwarzschild lensing angle, the photon ring, and the projected shadow shape measured against published figures. A concrete example: consistently applying kerr geodesic integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q60: What are the two families of integration for kerr geodesic integration - justify your answer with a concrete production example.
**A:** The direct geodesic integration of the equations of motion, and Hamilton-Jacobi reduced systems using conserved constants; kerr geodesic integration chooses per codebase. A concrete example: consistently applying kerr geodesic integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q61: How is kerr geodesic integration implemented on the GPU - justify your answer with a concrete production example.
**A:** As a numerical integration loop in device code with per-ray state in registers, stepping through kerr geodesic integration until the ray is captured or escapes. A concrete example: consistently applying kerr geodesic integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q62: Why is kerr geodesic integration the heart of a black-hole visualizer - justify your answer with a concrete production example.
**A:** Every visual signature - lensing, photon ring, shadow, redshift - emerges from exactly how kerr geodesic integration bends and time-shifts each ray. A concrete example: consistently applying kerr geodesic integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q63: What does kerr geodesic integration concretely do inside the raytracer - justify your answer with a concrete production example.
**A:** It advances photon trajectories in the curved spacetime, applying the equations of motion so each camera ray follows a true null geodesic. A concrete example: consistently applying kerr geodesic integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q64: What does kerr geodesic integration concretely do inside the raytracer - justify your answer with a concrete production example.
**A:** It advances photon trajectories in the curved spacetime, applying the equations of motion so each camera ray follows a true null geodesic. A concrete example: consistently applying kerr geodesic integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q65: Why is kerr geodesic integration the heart of a black-hole visualizer - justify your answer with a concrete production example.
**A:** Every visual signature - lensing, photon ring, shadow, redshift - emerges from exactly how kerr geodesic integration bends and time-shifts each ray. A concrete example: consistently applying kerr geodesic integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q66: How is kerr geodesic integration implemented on the GPU - justify your answer with a concrete production example.
**A:** As a numerical integration loop in device code with per-ray state in registers, stepping through kerr geodesic integration until the ray is captured or escapes. A concrete example: consistently applying kerr geodesic integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q67: What are the two families of integration for kerr geodesic integration - justify your answer with a concrete production example.
**A:** The direct geodesic integration of the equations of motion, and Hamilton-Jacobi reduced systems using conserved constants; kerr geodesic integration chooses per codebase. A concrete example: consistently applying kerr geodesic integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q68: How do you validate kerr geodesic integration - justify your answer with a concrete production example.
**A:** Reproduce the analytic Schwarzschild lensing angle, the photon ring, and the projected shadow shape measured against published figures. A concrete example: consistently applying kerr geodesic integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q69: What is the typical step-size strategy in kerr geodesic integration - justify your answer with a concrete production example.
**A:** Adaptive stepping that refines near the photon sphere and the horizon, where kerr geodesic integration gradients are steepest and error grows fastest. A concrete example: consistently applying kerr geodesic integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q70: What state does the integrator track for kerr geodesic integration - justify your answer with a concrete production example.
**A:** Position, four-momentum components, affine parameter, and accumulated redshift - kerr geodesic integration state vector is small enough to fit in registers. A concrete example: consistently applying kerr geodesic integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q71: How does kerr geodesic integration handle captured photons - justify your answer with a concrete production example.
**A:** It terminates integration at the horizon and records absorption; kerr geodesic integration distinguishes capture from scatter by the radial turning point. A concrete example: consistently applying kerr geodesic integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q72: What role do conserved constants play in kerr geodesic integration - justify your answer with a concrete production example.
**A:** They let you solve impact parameters analytically or prune impossible trajectories, dramatically speeding kerr geodesic integration for large image grids. A concrete example: consistently applying kerr geodesic integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q73: Describe the numerical error budget of kerr geodesic integration - justify your answer with a concrete production example.
**A:** Per-step truncation error and accumulated drift; kerr geodesic integration budgets a relative tolerance and verifies the final image is stable. A concrete example: consistently applying kerr geodesic integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q74: How does kerr geodesic integration map the sky to the image plane - justify your answer with a concrete production example.
**A:** Each image pixel defines an initial direction; kerr geodesic integration evolves that direction backward in time until it leaves the domain to a background sky or hits the disk. A concrete example: consistently applying kerr geodesic integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q75: What is the most common bug in kerr geodesic integration - justify your answer with a concrete production example.
**A:** A sign error in the equations of motion or a wrong coordinate transformation that produces plausible-but-wrong lensing; kerr geodesic integration needs golden-image regression tests. A concrete example: consistently applying kerr geodesic integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q76: How do you parallelize kerr geodesic integration - justify your answer with a concrete production example.
**A:** Every pixel is an independent kerr geodesic integration problem, so one thread per ray gives embarrassingly parallel behavior with no inter-thread communication. A concrete example: consistently applying kerr geodesic integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q77: What determines the visual shadow size in kerr geodesic integration - justify your answer with a concrete production example.
**A:** The photon sphere and horizon geometry: captured rays draw the shadow whose boundary in kerr geodesic integration is the photon ring. A concrete example: consistently applying kerr geodesic integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q78: When do you need full Kerr kerr geodesic integration instead of Schwarzschild - justify your answer with a concrete production example.
**A:** Whenever the disk's rotation and frame dragging matter - most real astrophysical images; kerr geodesic integration must support spin to be credible. A concrete example: consistently applying kerr geodesic integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q79: What is the 'second/third image' vocabulary of kerr geodesic integration - justify your answer with a concrete production example.
**A:** Light winding around the black hole produces multiple images; kerr geodesic integration naturally produces the primary, secondary, and higher-order photon ring. A concrete example: consistently applying kerr geodesic integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q80: How does kerr geodesic integration produce the bright thin ring - justify your answer with a concrete production example.
**A:** Rays that graze the photon sphere travel long path lengths through the brightest disk region, so averaged intensity peaks at the kerr geodesic integration critical impact parameter. A concrete example: consistently applying kerr geodesic integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q81: How does kerr geodesic integration decide frequencies for render - justify your answer with a concrete production example.
**A:** It integrates the redshift factor along the ray; kerr geodesic integration multiplies emitted frequency by it before applying the transfer equation. A concrete example: consistently applying kerr geodesic integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q82: What modes does kerr geodesic integration render the accretion disk - justify your answer with a concrete production example.
**A:** First as a geometric emitter grid, later using GRMHD data; kerr geodesic integration is agnostic to the source as long as it can query emissivity along the path. A concrete example: consistently applying kerr geodesic integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q83: How is kerr geodesic integration performance quantified - justify your answer with a concrete production example.
**A:** Mega-rays per second and time per frame; kerr geodesic integration usually spends its budget in the integration loop, so its step count is the key metric. A concrete example: consistently applying kerr geodesic integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q84: What is the effect of camera position in kerr geodesic integration - justify your answer with a concrete production example.
**A:** Face-on, edge-on, and plunging camera setups change the projected ring shape; kerr geodesic integration validates each against known renders. A concrete example: consistently applying kerr geodesic integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q85: How does kerr geodesic integration incorporate the disk's fluid velocity - justify your answer with a concrete production example.
**A:** Doppler and beaming appear when the emissivity frame is boosted; kerr geodesic integration applies that boost per photon ray path segment. A concrete example: consistently applying kerr geodesic integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q86: What is the horizon-catching strategy in kerr geodesic integration - justify your answer with a concrete production example.
**A:** Rather than refine forever, you flag a ray as captured once r drops below the horizon radius; kerr geodesic integration then terminates that lane. A concrete example: consistently applying kerr geodesic integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q87: How should you commission kerr geodesic integration output - justify your answer with a concrete production example.
**A:** Side-by-side with published stills of the same metric and camera to confirm lensing, ring, and shadow match within a few percent. A concrete example: consistently applying kerr geodesic integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q88: How should you commission kerr geodesic integration output - justify your answer with a concrete production example.
**A:** Side-by-side with published stills of the same metric and camera to confirm lensing, ring, and shadow match within a few percent. A concrete example: consistently applying kerr geodesic integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q89: What is the horizon-catching strategy in kerr geodesic integration - justify your answer with a concrete production example.
**A:** Rather than refine forever, you flag a ray as captured once r drops below the horizon radius; kerr geodesic integration then terminates that lane. A concrete example: consistently applying kerr geodesic integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q90: How does kerr geodesic integration incorporate the disk's fluid velocity - justify your answer with a concrete production example.
**A:** Doppler and beaming appear when the emissivity frame is boosted; kerr geodesic integration applies that boost per photon ray path segment. A concrete example: consistently applying kerr geodesic integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q91: What is the effect of camera position in kerr geodesic integration - justify your answer with a concrete production example.
**A:** Face-on, edge-on, and plunging camera setups change the projected ring shape; kerr geodesic integration validates each against known renders. A concrete example: consistently applying kerr geodesic integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q92: How is kerr geodesic integration performance quantified - justify your answer with a concrete production example.
**A:** Mega-rays per second and time per frame; kerr geodesic integration usually spends its budget in the integration loop, so its step count is the key metric. A concrete example: consistently applying kerr geodesic integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q93: What modes does kerr geodesic integration render the accretion disk - justify your answer with a concrete production example.
**A:** First as a geometric emitter grid, later using GRMHD data; kerr geodesic integration is agnostic to the source as long as it can query emissivity along the path. A concrete example: consistently applying kerr geodesic integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q94: How does kerr geodesic integration decide frequencies for render - justify your answer with a concrete production example.
**A:** It integrates the redshift factor along the ray; kerr geodesic integration multiplies emitted frequency by it before applying the transfer equation. A concrete example: consistently applying kerr geodesic integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q95: How does kerr geodesic integration produce the bright thin ring - justify your answer with a concrete production example.
**A:** Rays that graze the photon sphere travel long path lengths through the brightest disk region, so averaged intensity peaks at the kerr geodesic integration critical impact parameter. A concrete example: consistently applying kerr geodesic integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q96: What is the 'second/third image' vocabulary of kerr geodesic integration - justify your answer with a concrete production example.
**A:** Light winding around the black hole produces multiple images; kerr geodesic integration naturally produces the primary, secondary, and higher-order photon ring. A concrete example: consistently applying kerr geodesic integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q97: When do you need full Kerr kerr geodesic integration instead of Schwarzschild - justify your answer with a concrete production example.
**A:** Whenever the disk's rotation and frame dragging matter - most real astrophysical images; kerr geodesic integration must support spin to be credible. A concrete example: consistently applying kerr geodesic integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q98: What determines the visual shadow size in kerr geodesic integration - justify your answer with a concrete production example.
**A:** The photon sphere and horizon geometry: captured rays draw the shadow whose boundary in kerr geodesic integration is the photon ring. A concrete example: consistently applying kerr geodesic integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q99: How do you parallelize kerr geodesic integration - justify your answer with a concrete production example.
**A:** Every pixel is an independent kerr geodesic integration problem, so one thread per ray gives embarrassingly parallel behavior with no inter-thread communication. A concrete example: consistently applying kerr geodesic integration in code review and regression tests keeps the whole pipeline trustworthy.

## Q100: What is the most common bug in kerr geodesic integration - justify your answer with a concrete production example.
**A:** A sign error in the equations of motion or a wrong coordinate transformation that produces plausible-but-wrong lensing; kerr geodesic integration needs golden-image regression tests. A concrete example: consistently applying kerr geodesic integration in code review and regression tests keeps the whole pipeline trustworthy.
