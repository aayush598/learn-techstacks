# Gr Ray Tracing — Ray As Geodesic Interview Questions and Answers

## Q1: What is a ray in GR ray tracing?
**A:** A null geodesic: the path of a photon through curved spacetime, a curve with ds^2 = 0 whose tangent vector is parallel transported along itself.

## Q2: Why do we trace geodesics backwards from the camera?
**A:** Rays originate from the camera and are run into the scene; backwards (retrograde) tracing guarantees each image pixel receives exactly one ray and avoids losing photons.

## Q3: What is the relation between a worldline and a rendering?
**A:** Each image pixel corresponds to a bundle of null geodesics leaving the camera; integrating one representative photon per pixel assembles the whole image, outer-nulled.

## Q4: How do you initialize a ray?
**A:** At the camera event set position and 4-momentum: p_mu computed from the pixel direction times a scale chosen so p^mu p_mu = 0; E fixed sets the overall scale.

## Q5: What does the affine parameter represent for a photon?
**A:** lambda parametrizes the traversal; it is not proper time (photons have none) but a monotonic coordinate along which positions and momenta evolve smoothly.

## Q6: How do you detect the ray's end?
**A:** The ray terminates on a hit (reaching the emitting surface/disk), capture (crossing the horizon), or miss (exiting a bounding sphere at r_max).

## Q7: What is the first requirement for an integrator?
**A:** Preserving the null constraint p^2 = 0 within tolerance along the whole path - any drift in the null condition is evidence of numerical error, not physics.

## Q8: How does the geodesic property translate to code?
**A:** The tangent vector obeys the geodesic equation; integration advances (x^mu, p_mu) in tandem so the stated null/mass-shell condition stays satisfied.

## Q9: What is the retrograde-scatter symmetry?
**A:** Running rays backward from observer to source is equivalent to forward emission - the adaptive rays never know which direction is 'real' because null geometry is time-symmetric.

## Q10: What precisely is meant by a geodesic in terms of the affine connection?
**A:** A curve whose velocity u satisfies u^mu;nu u^nu = 0 - the parallel-transported velocity; in coordinates that is x'' + Gamma x'x' = 0.

## Q11: What is a per-pixel bundle and supersampling?
**A:** Each pixel samples its direction with multiple rays (e.g., stratified 4x) to average the chaotic lensing - the improvement that makes shadow edges smooth.

## Q12: How do you know the ray 'reaches' the emitter?
**A:** Intersections with the disk's 3-surface (e.g., equatorial theta=pi/2 + geodesics of radius r) are tested as the path steps; the first intersection wins.

## Q13: What is the numerical termination condition near capture?
**A:** When r < r_able (horizon radius in chart coordinates) plus a margin, the ray is marked 'captured', contributes to the shadow, and stepping halts.

## Q14: Why must adaptive step sizes kick in near strong-field regions?
**A:** The trajectory's curvature grows near the photon sphere; fixed-step tracing there produces systematic shadow-ring errors - adaptivity maintains accuracy.

## Q15: What is a validation ray set?
**A:** A golden grid: equatorial circular orbits, radial in/out, sky-scan impact parameters; each checks a closed-form relation (deflection, timers, shadow boundary).

## Q16: How many rays does a production frame need?
**A:** With supersampling ~16-64 rays/pixel, a 4k frame is tens of millions of geodesics - the whole engine's cost centers on efficient null-geodesic stepping.

## Q17: What does ray as geodesic concretely do inside the raytracer?
**A:** It advances photon trajectories in the curved spacetime, applying the equations of motion so each camera ray follows a true null geodesic.

## Q18: Why is ray as geodesic the heart of a black-hole visualizer?
**A:** Every visual signature - lensing, photon ring, shadow, redshift - emerges from exactly how ray as geodesic bends and time-shifts each ray.

## Q19: How is ray as geodesic implemented on the GPU?
**A:** As a numerical integration loop in device code with per-ray state in registers, stepping through ray as geodesic until the ray is captured or escapes.

## Q20: What are the two families of integration for ray as geodesic?
**A:** The direct geodesic integration of the equations of motion, and Hamilton-Jacobi reduced systems using conserved constants; ray as geodesic chooses per codebase.

## Q21: How do you validate ray as geodesic?
**A:** Reproduce the analytic Schwarzschild lensing angle, the photon ring, and the projected shadow shape measured against published figures.

## Q22: What is the typical step-size strategy in ray as geodesic?
**A:** Adaptive stepping that refines near the photon sphere and the horizon, where ray as geodesic gradients are steepest and error grows fastest.

## Q23: What state does the integrator track for ray as geodesic?
**A:** Position, four-momentum components, affine parameter, and accumulated redshift - ray as geodesic state vector is small enough to fit in registers.

## Q24: How does ray as geodesic handle captured photons?
**A:** It terminates integration at the horizon and records absorption; ray as geodesic distinguishes capture from scatter by the radial turning point.

## Q25: What role do conserved constants play in ray as geodesic?
**A:** They let you solve impact parameters analytically or prune impossible trajectories, dramatically speeding ray as geodesic for large image grids.

## Q26: Describe the numerical error budget of ray as geodesic.
**A:** Per-step truncation error and accumulated drift; ray as geodesic budgets a relative tolerance and verifies the final image is stable.

## Q27: How does ray as geodesic map the sky to the image plane?
**A:** Each image pixel defines an initial direction; ray as geodesic evolves that direction backward in time until it leaves the domain to a background sky or hits the disk.

## Q28: What is the most common bug in ray as geodesic?
**A:** A sign error in the equations of motion or a wrong coordinate transformation that produces plausible-but-wrong lensing; ray as geodesic needs golden-image regression tests.

## Q29: How do you parallelize ray as geodesic?
**A:** Every pixel is an independent ray as geodesic problem, so one thread per ray gives embarrassingly parallel behavior with no inter-thread communication.

## Q30: What determines the visual shadow size in ray as geodesic?
**A:** The photon sphere and horizon geometry: captured rays draw the shadow whose boundary in ray as geodesic is the photon ring.

## Q31: When do you need full Kerr ray as geodesic instead of Schwarzschild?
**A:** Whenever the disk's rotation and frame dragging matter - most real astrophysical images; ray as geodesic must support spin to be credible.

## Q32: What is the 'second/third image' vocabulary of ray as geodesic?
**A:** Light winding around the black hole produces multiple images; ray as geodesic naturally produces the primary, secondary, and higher-order photon ring.

## Q33: How does ray as geodesic produce the bright thin ring?
**A:** Rays that graze the photon sphere travel long path lengths through the brightest disk region, so averaged intensity peaks at the ray as geodesic critical impact parameter.

## Q34: How does ray as geodesic decide frequencies for render?
**A:** It integrates the redshift factor along the ray; ray as geodesic multiplies emitted frequency by it before applying the transfer equation.

## Q35: What modes does ray as geodesic render the accretion disk?
**A:** First as a geometric emitter grid, later using GRMHD data; ray as geodesic is agnostic to the source as long as it can query emissivity along the path.

## Q36: How is ray as geodesic performance quantified?
**A:** Mega-rays per second and time per frame; ray as geodesic usually spends its budget in the integration loop, so its step count is the key metric.

## Q37: What is the effect of camera position in ray as geodesic?
**A:** Face-on, edge-on, and plunging camera setups change the projected ring shape; ray as geodesic validates each against known renders.

## Q38: How does ray as geodesic incorporate the disk's fluid velocity?
**A:** Doppler and beaming appear when the emissivity frame is boosted; ray as geodesic applies that boost per photon ray path segment.

## Q39: What is the horizon-catching strategy in ray as geodesic?
**A:** Rather than refine forever, you flag a ray as captured once r drops below the horizon radius; ray as geodesic then terminates that lane.

## Q40: How should you commission ray as geodesic output?
**A:** Side-by-side with published stills of the same metric and camera to confirm lensing, ring, and shadow match within a few percent.

## Q41: How should you commission ray as geodesic output - justify your answer with a concrete production example.
**A:** Side-by-side with published stills of the same metric and camera to confirm lensing, ring, and shadow match within a few percent. A concrete example: consistently applying ray as geodesic in code review and regression tests keeps the whole pipeline trustworthy.

## Q42: What is the horizon-catching strategy in ray as geodesic - justify your answer with a concrete production example.
**A:** Rather than refine forever, you flag a ray as captured once r drops below the horizon radius; ray as geodesic then terminates that lane. A concrete example: consistently applying ray as geodesic in code review and regression tests keeps the whole pipeline trustworthy.

## Q43: How does ray as geodesic incorporate the disk's fluid velocity - justify your answer with a concrete production example.
**A:** Doppler and beaming appear when the emissivity frame is boosted; ray as geodesic applies that boost per photon ray path segment. A concrete example: consistently applying ray as geodesic in code review and regression tests keeps the whole pipeline trustworthy.

## Q44: What is the effect of camera position in ray as geodesic - justify your answer with a concrete production example.
**A:** Face-on, edge-on, and plunging camera setups change the projected ring shape; ray as geodesic validates each against known renders. A concrete example: consistently applying ray as geodesic in code review and regression tests keeps the whole pipeline trustworthy.

## Q45: How is ray as geodesic performance quantified - justify your answer with a concrete production example.
**A:** Mega-rays per second and time per frame; ray as geodesic usually spends its budget in the integration loop, so its step count is the key metric. A concrete example: consistently applying ray as geodesic in code review and regression tests keeps the whole pipeline trustworthy.

## Q46: What modes does ray as geodesic render the accretion disk - justify your answer with a concrete production example.
**A:** First as a geometric emitter grid, later using GRMHD data; ray as geodesic is agnostic to the source as long as it can query emissivity along the path. A concrete example: consistently applying ray as geodesic in code review and regression tests keeps the whole pipeline trustworthy.

## Q47: How does ray as geodesic decide frequencies for render - justify your answer with a concrete production example.
**A:** It integrates the redshift factor along the ray; ray as geodesic multiplies emitted frequency by it before applying the transfer equation. A concrete example: consistently applying ray as geodesic in code review and regression tests keeps the whole pipeline trustworthy.

## Q48: How does ray as geodesic produce the bright thin ring - justify your answer with a concrete production example.
**A:** Rays that graze the photon sphere travel long path lengths through the brightest disk region, so averaged intensity peaks at the ray as geodesic critical impact parameter. A concrete example: consistently applying ray as geodesic in code review and regression tests keeps the whole pipeline trustworthy.

## Q49: What is the 'second/third image' vocabulary of ray as geodesic - justify your answer with a concrete production example.
**A:** Light winding around the black hole produces multiple images; ray as geodesic naturally produces the primary, secondary, and higher-order photon ring. A concrete example: consistently applying ray as geodesic in code review and regression tests keeps the whole pipeline trustworthy.

## Q50: When do you need full Kerr ray as geodesic instead of Schwarzschild - justify your answer with a concrete production example.
**A:** Whenever the disk's rotation and frame dragging matter - most real astrophysical images; ray as geodesic must support spin to be credible. A concrete example: consistently applying ray as geodesic in code review and regression tests keeps the whole pipeline trustworthy.

## Q51: What determines the visual shadow size in ray as geodesic - justify your answer with a concrete production example.
**A:** The photon sphere and horizon geometry: captured rays draw the shadow whose boundary in ray as geodesic is the photon ring. A concrete example: consistently applying ray as geodesic in code review and regression tests keeps the whole pipeline trustworthy.

## Q52: How do you parallelize ray as geodesic - justify your answer with a concrete production example.
**A:** Every pixel is an independent ray as geodesic problem, so one thread per ray gives embarrassingly parallel behavior with no inter-thread communication. A concrete example: consistently applying ray as geodesic in code review and regression tests keeps the whole pipeline trustworthy.

## Q53: What is the most common bug in ray as geodesic - justify your answer with a concrete production example.
**A:** A sign error in the equations of motion or a wrong coordinate transformation that produces plausible-but-wrong lensing; ray as geodesic needs golden-image regression tests. A concrete example: consistently applying ray as geodesic in code review and regression tests keeps the whole pipeline trustworthy.

## Q54: How does ray as geodesic map the sky to the image plane - justify your answer with a concrete production example.
**A:** Each image pixel defines an initial direction; ray as geodesic evolves that direction backward in time until it leaves the domain to a background sky or hits the disk. A concrete example: consistently applying ray as geodesic in code review and regression tests keeps the whole pipeline trustworthy.

## Q55: Describe the numerical error budget of ray as geodesic - justify your answer with a concrete production example.
**A:** Per-step truncation error and accumulated drift; ray as geodesic budgets a relative tolerance and verifies the final image is stable. A concrete example: consistently applying ray as geodesic in code review and regression tests keeps the whole pipeline trustworthy.

## Q56: What role do conserved constants play in ray as geodesic - justify your answer with a concrete production example.
**A:** They let you solve impact parameters analytically or prune impossible trajectories, dramatically speeding ray as geodesic for large image grids. A concrete example: consistently applying ray as geodesic in code review and regression tests keeps the whole pipeline trustworthy.

## Q57: How does ray as geodesic handle captured photons - justify your answer with a concrete production example.
**A:** It terminates integration at the horizon and records absorption; ray as geodesic distinguishes capture from scatter by the radial turning point. A concrete example: consistently applying ray as geodesic in code review and regression tests keeps the whole pipeline trustworthy.

## Q58: What state does the integrator track for ray as geodesic - justify your answer with a concrete production example.
**A:** Position, four-momentum components, affine parameter, and accumulated redshift - ray as geodesic state vector is small enough to fit in registers. A concrete example: consistently applying ray as geodesic in code review and regression tests keeps the whole pipeline trustworthy.

## Q59: What is the typical step-size strategy in ray as geodesic - justify your answer with a concrete production example.
**A:** Adaptive stepping that refines near the photon sphere and the horizon, where ray as geodesic gradients are steepest and error grows fastest. A concrete example: consistently applying ray as geodesic in code review and regression tests keeps the whole pipeline trustworthy.

## Q60: How do you validate ray as geodesic - justify your answer with a concrete production example.
**A:** Reproduce the analytic Schwarzschild lensing angle, the photon ring, and the projected shadow shape measured against published figures. A concrete example: consistently applying ray as geodesic in code review and regression tests keeps the whole pipeline trustworthy.

## Q61: What are the two families of integration for ray as geodesic - justify your answer with a concrete production example.
**A:** The direct geodesic integration of the equations of motion, and Hamilton-Jacobi reduced systems using conserved constants; ray as geodesic chooses per codebase. A concrete example: consistently applying ray as geodesic in code review and regression tests keeps the whole pipeline trustworthy.

## Q62: How is ray as geodesic implemented on the GPU - justify your answer with a concrete production example.
**A:** As a numerical integration loop in device code with per-ray state in registers, stepping through ray as geodesic until the ray is captured or escapes. A concrete example: consistently applying ray as geodesic in code review and regression tests keeps the whole pipeline trustworthy.

## Q63: Why is ray as geodesic the heart of a black-hole visualizer - justify your answer with a concrete production example.
**A:** Every visual signature - lensing, photon ring, shadow, redshift - emerges from exactly how ray as geodesic bends and time-shifts each ray. A concrete example: consistently applying ray as geodesic in code review and regression tests keeps the whole pipeline trustworthy.

## Q64: What does ray as geodesic concretely do inside the raytracer - justify your answer with a concrete production example.
**A:** It advances photon trajectories in the curved spacetime, applying the equations of motion so each camera ray follows a true null geodesic. A concrete example: consistently applying ray as geodesic in code review and regression tests keeps the whole pipeline trustworthy.

## Q65: What does ray as geodesic concretely do inside the raytracer - justify your answer with a concrete production example.
**A:** It advances photon trajectories in the curved spacetime, applying the equations of motion so each camera ray follows a true null geodesic. A concrete example: consistently applying ray as geodesic in code review and regression tests keeps the whole pipeline trustworthy.

## Q66: Why is ray as geodesic the heart of a black-hole visualizer - justify your answer with a concrete production example.
**A:** Every visual signature - lensing, photon ring, shadow, redshift - emerges from exactly how ray as geodesic bends and time-shifts each ray. A concrete example: consistently applying ray as geodesic in code review and regression tests keeps the whole pipeline trustworthy.

## Q67: How is ray as geodesic implemented on the GPU - justify your answer with a concrete production example.
**A:** As a numerical integration loop in device code with per-ray state in registers, stepping through ray as geodesic until the ray is captured or escapes. A concrete example: consistently applying ray as geodesic in code review and regression tests keeps the whole pipeline trustworthy.

## Q68: What are the two families of integration for ray as geodesic - justify your answer with a concrete production example.
**A:** The direct geodesic integration of the equations of motion, and Hamilton-Jacobi reduced systems using conserved constants; ray as geodesic chooses per codebase. A concrete example: consistently applying ray as geodesic in code review and regression tests keeps the whole pipeline trustworthy.

## Q69: How do you validate ray as geodesic - justify your answer with a concrete production example.
**A:** Reproduce the analytic Schwarzschild lensing angle, the photon ring, and the projected shadow shape measured against published figures. A concrete example: consistently applying ray as geodesic in code review and regression tests keeps the whole pipeline trustworthy.

## Q70: What is the typical step-size strategy in ray as geodesic - justify your answer with a concrete production example.
**A:** Adaptive stepping that refines near the photon sphere and the horizon, where ray as geodesic gradients are steepest and error grows fastest. A concrete example: consistently applying ray as geodesic in code review and regression tests keeps the whole pipeline trustworthy.

## Q71: What state does the integrator track for ray as geodesic - justify your answer with a concrete production example.
**A:** Position, four-momentum components, affine parameter, and accumulated redshift - ray as geodesic state vector is small enough to fit in registers. A concrete example: consistently applying ray as geodesic in code review and regression tests keeps the whole pipeline trustworthy.

## Q72: How does ray as geodesic handle captured photons - justify your answer with a concrete production example.
**A:** It terminates integration at the horizon and records absorption; ray as geodesic distinguishes capture from scatter by the radial turning point. A concrete example: consistently applying ray as geodesic in code review and regression tests keeps the whole pipeline trustworthy.

## Q73: What role do conserved constants play in ray as geodesic - justify your answer with a concrete production example.
**A:** They let you solve impact parameters analytically or prune impossible trajectories, dramatically speeding ray as geodesic for large image grids. A concrete example: consistently applying ray as geodesic in code review and regression tests keeps the whole pipeline trustworthy.

## Q74: Describe the numerical error budget of ray as geodesic - justify your answer with a concrete production example.
**A:** Per-step truncation error and accumulated drift; ray as geodesic budgets a relative tolerance and verifies the final image is stable. A concrete example: consistently applying ray as geodesic in code review and regression tests keeps the whole pipeline trustworthy.

## Q75: How does ray as geodesic map the sky to the image plane - justify your answer with a concrete production example.
**A:** Each image pixel defines an initial direction; ray as geodesic evolves that direction backward in time until it leaves the domain to a background sky or hits the disk. A concrete example: consistently applying ray as geodesic in code review and regression tests keeps the whole pipeline trustworthy.

## Q76: What is the most common bug in ray as geodesic - justify your answer with a concrete production example.
**A:** A sign error in the equations of motion or a wrong coordinate transformation that produces plausible-but-wrong lensing; ray as geodesic needs golden-image regression tests. A concrete example: consistently applying ray as geodesic in code review and regression tests keeps the whole pipeline trustworthy.

## Q77: How do you parallelize ray as geodesic - justify your answer with a concrete production example.
**A:** Every pixel is an independent ray as geodesic problem, so one thread per ray gives embarrassingly parallel behavior with no inter-thread communication. A concrete example: consistently applying ray as geodesic in code review and regression tests keeps the whole pipeline trustworthy.

## Q78: What determines the visual shadow size in ray as geodesic - justify your answer with a concrete production example.
**A:** The photon sphere and horizon geometry: captured rays draw the shadow whose boundary in ray as geodesic is the photon ring. A concrete example: consistently applying ray as geodesic in code review and regression tests keeps the whole pipeline trustworthy.

## Q79: When do you need full Kerr ray as geodesic instead of Schwarzschild - justify your answer with a concrete production example.
**A:** Whenever the disk's rotation and frame dragging matter - most real astrophysical images; ray as geodesic must support spin to be credible. A concrete example: consistently applying ray as geodesic in code review and regression tests keeps the whole pipeline trustworthy.

## Q80: What is the 'second/third image' vocabulary of ray as geodesic - justify your answer with a concrete production example.
**A:** Light winding around the black hole produces multiple images; ray as geodesic naturally produces the primary, secondary, and higher-order photon ring. A concrete example: consistently applying ray as geodesic in code review and regression tests keeps the whole pipeline trustworthy.

## Q81: How does ray as geodesic produce the bright thin ring - justify your answer with a concrete production example.
**A:** Rays that graze the photon sphere travel long path lengths through the brightest disk region, so averaged intensity peaks at the ray as geodesic critical impact parameter. A concrete example: consistently applying ray as geodesic in code review and regression tests keeps the whole pipeline trustworthy.

## Q82: How does ray as geodesic decide frequencies for render - justify your answer with a concrete production example.
**A:** It integrates the redshift factor along the ray; ray as geodesic multiplies emitted frequency by it before applying the transfer equation. A concrete example: consistently applying ray as geodesic in code review and regression tests keeps the whole pipeline trustworthy.

## Q83: What modes does ray as geodesic render the accretion disk - justify your answer with a concrete production example.
**A:** First as a geometric emitter grid, later using GRMHD data; ray as geodesic is agnostic to the source as long as it can query emissivity along the path. A concrete example: consistently applying ray as geodesic in code review and regression tests keeps the whole pipeline trustworthy.

## Q84: How is ray as geodesic performance quantified - justify your answer with a concrete production example.
**A:** Mega-rays per second and time per frame; ray as geodesic usually spends its budget in the integration loop, so its step count is the key metric. A concrete example: consistently applying ray as geodesic in code review and regression tests keeps the whole pipeline trustworthy.

## Q85: What is the effect of camera position in ray as geodesic - justify your answer with a concrete production example.
**A:** Face-on, edge-on, and plunging camera setups change the projected ring shape; ray as geodesic validates each against known renders. A concrete example: consistently applying ray as geodesic in code review and regression tests keeps the whole pipeline trustworthy.

## Q86: How does ray as geodesic incorporate the disk's fluid velocity - justify your answer with a concrete production example.
**A:** Doppler and beaming appear when the emissivity frame is boosted; ray as geodesic applies that boost per photon ray path segment. A concrete example: consistently applying ray as geodesic in code review and regression tests keeps the whole pipeline trustworthy.

## Q87: What is the horizon-catching strategy in ray as geodesic - justify your answer with a concrete production example.
**A:** Rather than refine forever, you flag a ray as captured once r drops below the horizon radius; ray as geodesic then terminates that lane. A concrete example: consistently applying ray as geodesic in code review and regression tests keeps the whole pipeline trustworthy.

## Q88: How should you commission ray as geodesic output - justify your answer with a concrete production example.
**A:** Side-by-side with published stills of the same metric and camera to confirm lensing, ring, and shadow match within a few percent. A concrete example: consistently applying ray as geodesic in code review and regression tests keeps the whole pipeline trustworthy.

## Q89: How should you commission ray as geodesic output - justify your answer with a concrete production example.
**A:** Side-by-side with published stills of the same metric and camera to confirm lensing, ring, and shadow match within a few percent. A concrete example: consistently applying ray as geodesic in code review and regression tests keeps the whole pipeline trustworthy.

## Q90: What is the horizon-catching strategy in ray as geodesic - justify your answer with a concrete production example.
**A:** Rather than refine forever, you flag a ray as captured once r drops below the horizon radius; ray as geodesic then terminates that lane. A concrete example: consistently applying ray as geodesic in code review and regression tests keeps the whole pipeline trustworthy.

## Q91: How does ray as geodesic incorporate the disk's fluid velocity - justify your answer with a concrete production example.
**A:** Doppler and beaming appear when the emissivity frame is boosted; ray as geodesic applies that boost per photon ray path segment. A concrete example: consistently applying ray as geodesic in code review and regression tests keeps the whole pipeline trustworthy.

## Q92: What is the effect of camera position in ray as geodesic - justify your answer with a concrete production example.
**A:** Face-on, edge-on, and plunging camera setups change the projected ring shape; ray as geodesic validates each against known renders. A concrete example: consistently applying ray as geodesic in code review and regression tests keeps the whole pipeline trustworthy.

## Q93: How is ray as geodesic performance quantified - justify your answer with a concrete production example.
**A:** Mega-rays per second and time per frame; ray as geodesic usually spends its budget in the integration loop, so its step count is the key metric. A concrete example: consistently applying ray as geodesic in code review and regression tests keeps the whole pipeline trustworthy.

## Q94: What modes does ray as geodesic render the accretion disk - justify your answer with a concrete production example.
**A:** First as a geometric emitter grid, later using GRMHD data; ray as geodesic is agnostic to the source as long as it can query emissivity along the path. A concrete example: consistently applying ray as geodesic in code review and regression tests keeps the whole pipeline trustworthy.

## Q95: How does ray as geodesic decide frequencies for render - justify your answer with a concrete production example.
**A:** It integrates the redshift factor along the ray; ray as geodesic multiplies emitted frequency by it before applying the transfer equation. A concrete example: consistently applying ray as geodesic in code review and regression tests keeps the whole pipeline trustworthy.

## Q96: How does ray as geodesic produce the bright thin ring - justify your answer with a concrete production example.
**A:** Rays that graze the photon sphere travel long path lengths through the brightest disk region, so averaged intensity peaks at the ray as geodesic critical impact parameter. A concrete example: consistently applying ray as geodesic in code review and regression tests keeps the whole pipeline trustworthy.

## Q97: What is the 'second/third image' vocabulary of ray as geodesic - justify your answer with a concrete production example.
**A:** Light winding around the black hole produces multiple images; ray as geodesic naturally produces the primary, secondary, and higher-order photon ring. A concrete example: consistently applying ray as geodesic in code review and regression tests keeps the whole pipeline trustworthy.

## Q98: When do you need full Kerr ray as geodesic instead of Schwarzschild - justify your answer with a concrete production example.
**A:** Whenever the disk's rotation and frame dragging matter - most real astrophysical images; ray as geodesic must support spin to be credible. A concrete example: consistently applying ray as geodesic in code review and regression tests keeps the whole pipeline trustworthy.

## Q99: What determines the visual shadow size in ray as geodesic - justify your answer with a concrete production example.
**A:** The photon sphere and horizon geometry: captured rays draw the shadow whose boundary in ray as geodesic is the photon ring. A concrete example: consistently applying ray as geodesic in code review and regression tests keeps the whole pipeline trustworthy.

## Q100: How do you parallelize ray as geodesic - justify your answer with a concrete production example.
**A:** Every pixel is an independent ray as geodesic problem, so one thread per ray gives embarrassingly parallel behavior with no inter-thread communication. A concrete example: consistently applying ray as geodesic in code review and regression tests keeps the whole pipeline trustworthy.
