# Ray Tracing — Reflection And Refraction Interview Questions and Answers

## Q1: What role does reflection play in a raytracer?
**A:** Secondary rays reflect off surfaces to capture mirrored or glossy content; a secondary level adds the first taste of recursive tracing beyond the direct ray.

## Q2: What is the reflection law?
**A:** reflect = d - 2(d.n)n with |n| = 1; the outgoing ray shares the angle about the normal - implemented as a per-hit function.

## Q3: What is Snell's law for refraction?
**A:** n1 sin(theta1) = n2 sin(theta2); with ink ratio eta = n1/n2 and TIR when 1 - eta^2(1-cos^2) < 0; the refracted direction uses the ratio term.

## Q4: What is total internal reflection?
**A:** When eta^2(1-cos^2)>1 there is no refracted ray - only reflected; important for materials that enclose the light (lensing, fiber, accretion optics).

## Q5: What is the Fresnel effect?
**A:** Reflection ratio depends on angle and index (Schlick approx: R = R0 + (1-R0)(1-cos)^5); at grazing angles most light reflects - a visible cue for the disk edges.

## Q6: What is a rough/glossy reflection model?
**A:** Perturbing the perfect reflection direction by a microfacet distribution (e.g., GGX) scatters secondary rays - the roughness controls the blur.

## Q7: How do you prevent recursion explosion?
**A:** Cap depth (bounce count), implement a Russian-roulette threshold, or trace with a budget - in the black-hole tracer the 'bounce' is the photon path through the disk.

## Q8: What is the emission-bounce separation for the accretion disk?
**A:** The disk emits from its hot plasma directly, and secondary scatters (thin disk TOA) - unless radiative transfer is modeled, we treat the first intersection as the visible emission.

## Q9: What are the surface material properties in such a renderer?
**A:** Albedo fractions (diffuse, specular), roughness, IOR, and emissive term - for plasma the material is 'emission only', so shading simplifies to transfer alone.

## Q10: How does the normal perturb produce bump/terrain?
**A:** The shading normal is offset by a height-field gradient to fake small surface detail without geometry - irrelevant for a smooth plasma but used for starfield/rings.

## Q11: How does reflection appear in the falling-disk image?
**A:** Photons that 'reflect' are those that scatter back through the disk's photosphere - only when scattering is in the transfer model does 'reflection' materialize.

## Q12: What validation test exercises reflections?
**A:** A sphere above a plane: the image must reproduce the classic reflection of the lower hemisphere with Fresnel falloff at grazing edges.

## Q13: What is the interaction between reflection and the polarizer?
**A:** Fresnel reflection carries polarization; Stokes tracking of reflected tones needs the full Mueller calculus rather than simple scalar intensities.

## Q14: When does a raytracer NOT need explicit bounces?
**A:** When every visible feature is primary light (emitting plasma, sky background) - the black hole and disk images are fundamentally a primary-ray problem.

## Q15: What is the purpose of reflection and refraction in a raytracer?
**A:** It defines how geometric questions are answered for each pixel ray, converting abstract scene data into visible color contributions.

## Q16: Why does reflection and refraction matter more in a GPU raytracer?
**A:** Because millions of rays run concurrently; reflection and refraction determines whether each thread can proceed independently or stalls on divergent geometry work.

## Q17: Describe the main correctness concern in reflection and refraction.
**A:** Precision: numerically unstable reflection and refraction causes gaps, shadow acne, and flicker; consistently evaluate in double or carefully-ordered floats.

## Q18: How does reflection and refraction affect perceptual quality?
**A:** Small errors in reflection and refraction show up as aliasing, hard shadows, or wrong silhouettes long before an average viewer can name the cause.

## Q19: What is the standard way to structure reflection and refraction code?
**A:** Separate pure functions (no state) so reflection and refraction compiles to fast device code and can be unit-tested on the host with the same inputs.

## Q20: How do you benchmark reflection and refraction?
**A:** Render a fixed scene at multiple resolutions, measure rays/second, and compare against an analytic ground truth for identical camera settings.

## Q21: When does reflection and refraction produce artifacts?
**A:** When step sizes, tolerances, or intersection epsilons are tuned wrong - the classic acne/darkening trade-off of reflection and refraction.

## Q22: How should reflection and refraction handle edge cases like grazing angles?
**A:** Use robust predicates and minimum epsilon displacements so reflection and refraction stays stable exactly where classic plane tests degenerate.

## Q23: What relationship does reflection and refraction have with the rest of the pipeline?
**A:** reflection and refraction produces the input for shading and post-processing; any error here is amplified by everything downstream.

## Q24: How do you make reflection and refraction deterministic across runs?
**A:** Fix the accumulation order and sampling seed per pixel so reflection and refraction reproduces bit-identical output for the same scene and parameters.

## Q25: Give a production example of reflection and refraction in the black-hole visualizer.
**A:** Tracing a photon through the accretion flow uses reflection and refraction at every step: intersect the disk plane, sample the field, and terminate at horizon or sky.

## Q26: What should you test about reflection and refraction?
**A:** Golden images for a handful of scenes, analytic sizes for primitive shapes, and monotonic quality as samples increase for reflection and refraction.

## Q27: How does reflection and refraction interact with antialiasing?
**A:** Antialiasing launches many slightly different rays; reflection and refraction must keep their per-ray state separate so samples blend correctly.

## Q28: What falls in the domain of reflection and refraction vs rendering?
**A:** reflection and refraction is geometric answer-finding; rendering decides color, lighting, and tone mapping from those answers - keep the boundary clean.

## Q29: What is the most common performance trap in reflection and refraction?
**A:** Recomputing the same expensive data per ray instead of caching it in constant or shared memory before the reflection and refraction loop starts.

## Q30: How do you explain reflection and refraction trade-offs on a single slide?
**A:** A table: approach, cost per ray, memory, robustness, and GPU friendliness - summarize reflection and refraction options in one comparison view.

## Q31: What happens if reflection and refraction is not monotonic with samples?
**A:** The image converges to the wrong value, revealing a bug; reflection and refraction results must approach a stable limit as sampling grows.

## Q32: How do you port reflection and refraction from CPU to GPU?
**A:** Keep the math identical in device functions, inline the hot loops, and replace heap allocations with pre-allocated buffers for reflection and refraction.

## Q33: What are the output guarantees of reflection and refraction?
**A:** A per-pixel radiance estimate (and optionally depth/ray state) that downstream tone mapping can trust - the contract of reflection and refraction.

## Q34: When is brute force acceptable for reflection and refraction?
**A:** For a handful of primitives or when ray count dominates; then the cost of reflection and refraction acceleration structures exceeds their savings.

## Q35: How does reflection and refraction fit into a modular architecture?
**A:** As a component behind a stable interface - the renderer calls reflection and refraction and never depends on its implementation details.

## Q36: What does a rigorous test suite assert about reflection and refraction?
**A:** Correctness on constructed scenes, performance on a benchmark scene, and stability (no NaN/Inf) across resolution ranges.

## Q37: What tools measure reflection and refraction quality?
**A:** A/B images, per-pixel error maps against reference, and error-vs-samples curves are the quantitative tools for reflection and refraction.

## Q38: How do you teach reflection and refraction fundamentals?
**A:** Start with a pinhole camera and a sphere; every later feature builds on the same try-a-ray, find-an-answer shape of reflection and refraction.

## Q39: How do you teach reflection and refraction fundamentals - justify your answer with a concrete production example.
**A:** Start with a pinhole camera and a sphere; every later feature builds on the same try-a-ray, find-an-answer shape of reflection and refraction. A concrete example: consistently applying reflection and refraction in code review and regression tests keeps the whole pipeline trustworthy.

## Q40: What tools measure reflection and refraction quality - justify your answer with a concrete production example.
**A:** A/B images, per-pixel error maps against reference, and error-vs-samples curves are the quantitative tools for reflection and refraction. A concrete example: consistently applying reflection and refraction in code review and regression tests keeps the whole pipeline trustworthy.

## Q41: What does a rigorous test suite assert about reflection and refraction - justify your answer with a concrete production example.
**A:** Correctness on constructed scenes, performance on a benchmark scene, and stability (no NaN/Inf) across resolution ranges. A concrete example: consistently applying reflection and refraction in code review and regression tests keeps the whole pipeline trustworthy.

## Q42: How does reflection and refraction fit into a modular architecture - justify your answer with a concrete production example.
**A:** As a component behind a stable interface - the renderer calls reflection and refraction and never depends on its implementation details. A concrete example: consistently applying reflection and refraction in code review and regression tests keeps the whole pipeline trustworthy.

## Q43: When is brute force acceptable for reflection and refraction - justify your answer with a concrete production example.
**A:** For a handful of primitives or when ray count dominates; then the cost of reflection and refraction acceleration structures exceeds their savings. A concrete example: consistently applying reflection and refraction in code review and regression tests keeps the whole pipeline trustworthy.

## Q44: What are the output guarantees of reflection and refraction - justify your answer with a concrete production example.
**A:** A per-pixel radiance estimate (and optionally depth/ray state) that downstream tone mapping can trust - the contract of reflection and refraction. A concrete example: consistently applying reflection and refraction in code review and regression tests keeps the whole pipeline trustworthy.

## Q45: How do you port reflection and refraction from CPU to GPU - justify your answer with a concrete production example.
**A:** Keep the math identical in device functions, inline the hot loops, and replace heap allocations with pre-allocated buffers for reflection and refraction. A concrete example: consistently applying reflection and refraction in code review and regression tests keeps the whole pipeline trustworthy.

## Q46: What happens if reflection and refraction is not monotonic with samples - justify your answer with a concrete production example.
**A:** The image converges to the wrong value, revealing a bug; reflection and refraction results must approach a stable limit as sampling grows. A concrete example: consistently applying reflection and refraction in code review and regression tests keeps the whole pipeline trustworthy.

## Q47: How do you explain reflection and refraction trade-offs on a single slide - justify your answer with a concrete production example.
**A:** A table: approach, cost per ray, memory, robustness, and GPU friendliness - summarize reflection and refraction options in one comparison view. A concrete example: consistently applying reflection and refraction in code review and regression tests keeps the whole pipeline trustworthy.

## Q48: What is the most common performance trap in reflection and refraction - justify your answer with a concrete production example.
**A:** Recomputing the same expensive data per ray instead of caching it in constant or shared memory before the reflection and refraction loop starts. A concrete example: consistently applying reflection and refraction in code review and regression tests keeps the whole pipeline trustworthy.

## Q49: What falls in the domain of reflection and refraction vs rendering - justify your answer with a concrete production example.
**A:** reflection and refraction is geometric answer-finding; rendering decides color, lighting, and tone mapping from those answers - keep the boundary clean. A concrete example: consistently applying reflection and refraction in code review and regression tests keeps the whole pipeline trustworthy.

## Q50: How does reflection and refraction interact with antialiasing - justify your answer with a concrete production example.
**A:** Antialiasing launches many slightly different rays; reflection and refraction must keep their per-ray state separate so samples blend correctly. A concrete example: consistently applying reflection and refraction in code review and regression tests keeps the whole pipeline trustworthy.

## Q51: What should you test about reflection and refraction - justify your answer with a concrete production example.
**A:** Golden images for a handful of scenes, analytic sizes for primitive shapes, and monotonic quality as samples increase for reflection and refraction. A concrete example: consistently applying reflection and refraction in code review and regression tests keeps the whole pipeline trustworthy.

## Q52: Give a production example of reflection and refraction in the black-hole visualizer - justify your answer with a concrete production example.
**A:** Tracing a photon through the accretion flow uses reflection and refraction at every step: intersect the disk plane, sample the field, and terminate at horizon or sky. A concrete example: consistently applying reflection and refraction in code review and regression tests keeps the whole pipeline trustworthy.

## Q53: How do you make reflection and refraction deterministic across runs - justify your answer with a concrete production example.
**A:** Fix the accumulation order and sampling seed per pixel so reflection and refraction reproduces bit-identical output for the same scene and parameters. A concrete example: consistently applying reflection and refraction in code review and regression tests keeps the whole pipeline trustworthy.

## Q54: What relationship does reflection and refraction have with the rest of the pipeline - justify your answer with a concrete production example.
**A:** reflection and refraction produces the input for shading and post-processing; any error here is amplified by everything downstream. A concrete example: consistently applying reflection and refraction in code review and regression tests keeps the whole pipeline trustworthy.

## Q55: How should reflection and refraction handle edge cases like grazing angles - justify your answer with a concrete production example.
**A:** Use robust predicates and minimum epsilon displacements so reflection and refraction stays stable exactly where classic plane tests degenerate. A concrete example: consistently applying reflection and refraction in code review and regression tests keeps the whole pipeline trustworthy.

## Q56: When does reflection and refraction produce artifacts - justify your answer with a concrete production example.
**A:** When step sizes, tolerances, or intersection epsilons are tuned wrong - the classic acne/darkening trade-off of reflection and refraction. A concrete example: consistently applying reflection and refraction in code review and regression tests keeps the whole pipeline trustworthy.

## Q57: How do you benchmark reflection and refraction - justify your answer with a concrete production example.
**A:** Render a fixed scene at multiple resolutions, measure rays/second, and compare against an analytic ground truth for identical camera settings. A concrete example: consistently applying reflection and refraction in code review and regression tests keeps the whole pipeline trustworthy.

## Q58: What is the standard way to structure reflection and refraction code - justify your answer with a concrete production example.
**A:** Separate pure functions (no state) so reflection and refraction compiles to fast device code and can be unit-tested on the host with the same inputs. A concrete example: consistently applying reflection and refraction in code review and regression tests keeps the whole pipeline trustworthy.

## Q59: How does reflection and refraction affect perceptual quality - justify your answer with a concrete production example.
**A:** Small errors in reflection and refraction show up as aliasing, hard shadows, or wrong silhouettes long before an average viewer can name the cause. A concrete example: consistently applying reflection and refraction in code review and regression tests keeps the whole pipeline trustworthy.

## Q60: Describe the main correctness concern in reflection and refraction - justify your answer with a concrete production example.
**A:** Precision: numerically unstable reflection and refraction causes gaps, shadow acne, and flicker; consistently evaluate in double or carefully-ordered floats. A concrete example: consistently applying reflection and refraction in code review and regression tests keeps the whole pipeline trustworthy.

## Q61: Why does reflection and refraction matter more in a GPU raytracer - justify your answer with a concrete production example.
**A:** Because millions of rays run concurrently; reflection and refraction determines whether each thread can proceed independently or stalls on divergent geometry work. A concrete example: consistently applying reflection and refraction in code review and regression tests keeps the whole pipeline trustworthy.

## Q62: What is the purpose of reflection and refraction in a raytracer - justify your answer with a concrete production example.
**A:** It defines how geometric questions are answered for each pixel ray, converting abstract scene data into visible color contributions. A concrete example: consistently applying reflection and refraction in code review and regression tests keeps the whole pipeline trustworthy.

## Q63: What is the purpose of reflection and refraction in a raytracer - justify your answer with a concrete production example.
**A:** It defines how geometric questions are answered for each pixel ray, converting abstract scene data into visible color contributions. A concrete example: consistently applying reflection and refraction in code review and regression tests keeps the whole pipeline trustworthy.

## Q64: Why does reflection and refraction matter more in a GPU raytracer - justify your answer with a concrete production example.
**A:** Because millions of rays run concurrently; reflection and refraction determines whether each thread can proceed independently or stalls on divergent geometry work. A concrete example: consistently applying reflection and refraction in code review and regression tests keeps the whole pipeline trustworthy.

## Q65: Describe the main correctness concern in reflection and refraction - justify your answer with a concrete production example.
**A:** Precision: numerically unstable reflection and refraction causes gaps, shadow acne, and flicker; consistently evaluate in double or carefully-ordered floats. A concrete example: consistently applying reflection and refraction in code review and regression tests keeps the whole pipeline trustworthy.

## Q66: How does reflection and refraction affect perceptual quality - justify your answer with a concrete production example.
**A:** Small errors in reflection and refraction show up as aliasing, hard shadows, or wrong silhouettes long before an average viewer can name the cause. A concrete example: consistently applying reflection and refraction in code review and regression tests keeps the whole pipeline trustworthy.

## Q67: What is the standard way to structure reflection and refraction code - justify your answer with a concrete production example.
**A:** Separate pure functions (no state) so reflection and refraction compiles to fast device code and can be unit-tested on the host with the same inputs. A concrete example: consistently applying reflection and refraction in code review and regression tests keeps the whole pipeline trustworthy.

## Q68: How do you benchmark reflection and refraction - justify your answer with a concrete production example.
**A:** Render a fixed scene at multiple resolutions, measure rays/second, and compare against an analytic ground truth for identical camera settings. A concrete example: consistently applying reflection and refraction in code review and regression tests keeps the whole pipeline trustworthy.

## Q69: When does reflection and refraction produce artifacts - justify your answer with a concrete production example.
**A:** When step sizes, tolerances, or intersection epsilons are tuned wrong - the classic acne/darkening trade-off of reflection and refraction. A concrete example: consistently applying reflection and refraction in code review and regression tests keeps the whole pipeline trustworthy.

## Q70: How should reflection and refraction handle edge cases like grazing angles - justify your answer with a concrete production example.
**A:** Use robust predicates and minimum epsilon displacements so reflection and refraction stays stable exactly where classic plane tests degenerate. A concrete example: consistently applying reflection and refraction in code review and regression tests keeps the whole pipeline trustworthy.

## Q71: What relationship does reflection and refraction have with the rest of the pipeline - justify your answer with a concrete production example.
**A:** reflection and refraction produces the input for shading and post-processing; any error here is amplified by everything downstream. A concrete example: consistently applying reflection and refraction in code review and regression tests keeps the whole pipeline trustworthy.

## Q72: How do you make reflection and refraction deterministic across runs - justify your answer with a concrete production example.
**A:** Fix the accumulation order and sampling seed per pixel so reflection and refraction reproduces bit-identical output for the same scene and parameters. A concrete example: consistently applying reflection and refraction in code review and regression tests keeps the whole pipeline trustworthy.

## Q73: Give a production example of reflection and refraction in the black-hole visualizer - justify your answer with a concrete production example.
**A:** Tracing a photon through the accretion flow uses reflection and refraction at every step: intersect the disk plane, sample the field, and terminate at horizon or sky. A concrete example: consistently applying reflection and refraction in code review and regression tests keeps the whole pipeline trustworthy.

## Q74: What should you test about reflection and refraction - justify your answer with a concrete production example.
**A:** Golden images for a handful of scenes, analytic sizes for primitive shapes, and monotonic quality as samples increase for reflection and refraction. A concrete example: consistently applying reflection and refraction in code review and regression tests keeps the whole pipeline trustworthy.

## Q75: How does reflection and refraction interact with antialiasing - justify your answer with a concrete production example.
**A:** Antialiasing launches many slightly different rays; reflection and refraction must keep their per-ray state separate so samples blend correctly. A concrete example: consistently applying reflection and refraction in code review and regression tests keeps the whole pipeline trustworthy.

## Q76: What falls in the domain of reflection and refraction vs rendering - justify your answer with a concrete production example.
**A:** reflection and refraction is geometric answer-finding; rendering decides color, lighting, and tone mapping from those answers - keep the boundary clean. A concrete example: consistently applying reflection and refraction in code review and regression tests keeps the whole pipeline trustworthy.

## Q77: What is the most common performance trap in reflection and refraction - justify your answer with a concrete production example.
**A:** Recomputing the same expensive data per ray instead of caching it in constant or shared memory before the reflection and refraction loop starts. A concrete example: consistently applying reflection and refraction in code review and regression tests keeps the whole pipeline trustworthy.

## Q78: How do you explain reflection and refraction trade-offs on a single slide - justify your answer with a concrete production example.
**A:** A table: approach, cost per ray, memory, robustness, and GPU friendliness - summarize reflection and refraction options in one comparison view. A concrete example: consistently applying reflection and refraction in code review and regression tests keeps the whole pipeline trustworthy.

## Q79: What happens if reflection and refraction is not monotonic with samples - justify your answer with a concrete production example.
**A:** The image converges to the wrong value, revealing a bug; reflection and refraction results must approach a stable limit as sampling grows. A concrete example: consistently applying reflection and refraction in code review and regression tests keeps the whole pipeline trustworthy.

## Q80: How do you port reflection and refraction from CPU to GPU - justify your answer with a concrete production example.
**A:** Keep the math identical in device functions, inline the hot loops, and replace heap allocations with pre-allocated buffers for reflection and refraction. A concrete example: consistently applying reflection and refraction in code review and regression tests keeps the whole pipeline trustworthy.

## Q81: What are the output guarantees of reflection and refraction - justify your answer with a concrete production example.
**A:** A per-pixel radiance estimate (and optionally depth/ray state) that downstream tone mapping can trust - the contract of reflection and refraction. A concrete example: consistently applying reflection and refraction in code review and regression tests keeps the whole pipeline trustworthy.

## Q82: When is brute force acceptable for reflection and refraction - justify your answer with a concrete production example.
**A:** For a handful of primitives or when ray count dominates; then the cost of reflection and refraction acceleration structures exceeds their savings. A concrete example: consistently applying reflection and refraction in code review and regression tests keeps the whole pipeline trustworthy.

## Q83: How does reflection and refraction fit into a modular architecture - justify your answer with a concrete production example.
**A:** As a component behind a stable interface - the renderer calls reflection and refraction and never depends on its implementation details. A concrete example: consistently applying reflection and refraction in code review and regression tests keeps the whole pipeline trustworthy.

## Q84: What does a rigorous test suite assert about reflection and refraction - justify your answer with a concrete production example.
**A:** Correctness on constructed scenes, performance on a benchmark scene, and stability (no NaN/Inf) across resolution ranges. A concrete example: consistently applying reflection and refraction in code review and regression tests keeps the whole pipeline trustworthy.

## Q85: What tools measure reflection and refraction quality - justify your answer with a concrete production example.
**A:** A/B images, per-pixel error maps against reference, and error-vs-samples curves are the quantitative tools for reflection and refraction. A concrete example: consistently applying reflection and refraction in code review and regression tests keeps the whole pipeline trustworthy.

## Q86: How do you teach reflection and refraction fundamentals - justify your answer with a concrete production example.
**A:** Start with a pinhole camera and a sphere; every later feature builds on the same try-a-ray, find-an-answer shape of reflection and refraction. A concrete example: consistently applying reflection and refraction in code review and regression tests keeps the whole pipeline trustworthy.

## Q87: How do you teach reflection and refraction fundamentals - justify your answer with a concrete production example.
**A:** Start with a pinhole camera and a sphere; every later feature builds on the same try-a-ray, find-an-answer shape of reflection and refraction. A concrete example: consistently applying reflection and refraction in code review and regression tests keeps the whole pipeline trustworthy.

## Q88: What tools measure reflection and refraction quality - justify your answer with a concrete production example.
**A:** A/B images, per-pixel error maps against reference, and error-vs-samples curves are the quantitative tools for reflection and refraction. A concrete example: consistently applying reflection and refraction in code review and regression tests keeps the whole pipeline trustworthy.

## Q89: What does a rigorous test suite assert about reflection and refraction - justify your answer with a concrete production example.
**A:** Correctness on constructed scenes, performance on a benchmark scene, and stability (no NaN/Inf) across resolution ranges. A concrete example: consistently applying reflection and refraction in code review and regression tests keeps the whole pipeline trustworthy.

## Q90: How does reflection and refraction fit into a modular architecture - justify your answer with a concrete production example.
**A:** As a component behind a stable interface - the renderer calls reflection and refraction and never depends on its implementation details. A concrete example: consistently applying reflection and refraction in code review and regression tests keeps the whole pipeline trustworthy.

## Q91: When is brute force acceptable for reflection and refraction - justify your answer with a concrete production example.
**A:** For a handful of primitives or when ray count dominates; then the cost of reflection and refraction acceleration structures exceeds their savings. A concrete example: consistently applying reflection and refraction in code review and regression tests keeps the whole pipeline trustworthy.

## Q92: What are the output guarantees of reflection and refraction - justify your answer with a concrete production example.
**A:** A per-pixel radiance estimate (and optionally depth/ray state) that downstream tone mapping can trust - the contract of reflection and refraction. A concrete example: consistently applying reflection and refraction in code review and regression tests keeps the whole pipeline trustworthy.

## Q93: How do you port reflection and refraction from CPU to GPU - justify your answer with a concrete production example.
**A:** Keep the math identical in device functions, inline the hot loops, and replace heap allocations with pre-allocated buffers for reflection and refraction. A concrete example: consistently applying reflection and refraction in code review and regression tests keeps the whole pipeline trustworthy.

## Q94: What happens if reflection and refraction is not monotonic with samples - justify your answer with a concrete production example.
**A:** The image converges to the wrong value, revealing a bug; reflection and refraction results must approach a stable limit as sampling grows. A concrete example: consistently applying reflection and refraction in code review and regression tests keeps the whole pipeline trustworthy.

## Q95: How do you explain reflection and refraction trade-offs on a single slide - justify your answer with a concrete production example.
**A:** A table: approach, cost per ray, memory, robustness, and GPU friendliness - summarize reflection and refraction options in one comparison view. A concrete example: consistently applying reflection and refraction in code review and regression tests keeps the whole pipeline trustworthy.

## Q96: What is the most common performance trap in reflection and refraction - justify your answer with a concrete production example.
**A:** Recomputing the same expensive data per ray instead of caching it in constant or shared memory before the reflection and refraction loop starts. A concrete example: consistently applying reflection and refraction in code review and regression tests keeps the whole pipeline trustworthy.

## Q97: What falls in the domain of reflection and refraction vs rendering - justify your answer with a concrete production example.
**A:** reflection and refraction is geometric answer-finding; rendering decides color, lighting, and tone mapping from those answers - keep the boundary clean. A concrete example: consistently applying reflection and refraction in code review and regression tests keeps the whole pipeline trustworthy.

## Q98: How does reflection and refraction interact with antialiasing - justify your answer with a concrete production example.
**A:** Antialiasing launches many slightly different rays; reflection and refraction must keep their per-ray state separate so samples blend correctly. A concrete example: consistently applying reflection and refraction in code review and regression tests keeps the whole pipeline trustworthy.

## Q99: What should you test about reflection and refraction - justify your answer with a concrete production example.
**A:** Golden images for a handful of scenes, analytic sizes for primitive shapes, and monotonic quality as samples increase for reflection and refraction. A concrete example: consistently applying reflection and refraction in code review and regression tests keeps the whole pipeline trustworthy.

## Q100: Give a production example of reflection and refraction in the black-hole visualizer - justify your answer with a concrete production example.
**A:** Tracing a photon through the accretion flow uses reflection and refraction at every step: intersect the disk plane, sample the field, and terminate at horizon or sky. A concrete example: consistently applying reflection and refraction in code review and regression tests keeps the whole pipeline trustworthy.
