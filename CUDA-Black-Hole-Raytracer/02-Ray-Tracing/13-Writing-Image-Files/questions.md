# Ray Tracing — Writing Image Files Interview Questions and Answers

## Q1: What is the file format selection for HDR frames?
**A:** OpenEXR (float, exact dynamic range) for master frames; PNG (8-bit sRGB) for previews; PPM for debug. The pipeline writes both into the same buffers.

## Q2: Why NOT use a lossy format (JPEG) for the master?
**A:** JPEG's DCT artifacts damage the exact physics pixels and re-encoding compounds - the master must stay lossless (EXR/PNG) and JPEG only at the final funnel.

## Q3: How is the image stored in memory?
**A:** A float4 buffer W*H (RGB + optional alpha), row-major, row-aligned to 16-byte; the trace kernel writes it directly, the writer flattens to the format.

## Q4: What are the image dimensions and stride?
**A:** W and H independent of alignment for output; the buffer stride = W*4 floats; PNG writer converts to 8-bit per channel with the sRGB encoding applied first.

## Q5: How do you write EXR from CUDA?
**A:** Copy the float buffer to host, then feed tinyexr or OpenEXR's API a header + pixel-array - one library call per file after the kernel completes.

## Q6: What is the standard PNG encode path?
**A:** host buffer -> stb_write_png (zlib) or libpng; both accept 32-bit RGBA and 8-bit after conversion; mind thread-safe library choice.

## Q7: How is a movie built from frames?
**A:** The renderer writes N sequential EXR/PNG frames (named frame_%05d.png) and ffmpeg x264 promises the encode - no render-time video codecs needed.

## Q8: What is the color conversion to sRGB?
**A:** Apply the linear->sRGB curve (c <= 0.0031308 ? c*12.92 : 1.055*c^(1/2.4) - 0.055) per channel, then [0-255]. Where the tone mapper already includes it, skip.

## Q9: What alpha does the raytracer write?
**A:** Blend alpha = opacity of the composite (sky + disk); for a fully opaque frame alpha=1 everywhere; keep format flexible (PNG supports alpha).

## Q10: How do you embed metadata?
**A:** EXR/PNG chunk data (timestamp, camera config, integrator, random seeds, data hash) - enables exact reproducibility of every master frame.

## Q11: What is the debug PPM format?
**A:** P6: 'P6\nW H\n255\n' + raw bytes; trivially written for tests and diffable by readers - the toilet test format.

## Q12: How do you verify a written file?
**A:** Re-read it, compare pixels to the source buffer, and assert the loop and format round-trip - catches byte-order and width/height bugs immediately.

## Q13: What are the thread-safety concerns of writing?
**A:** Only one thread writes; use a mutex or render each frame to its own buffer and write sequentially from the host after sync.

## Q14: How does the writer interact with determinism?
**A:** The file bytes must be identical across identical runs for a given config (deterministic float->int rounding) - a checksum test enforces it.

## Q15: What is the purpose of writing image files in a raytracer?
**A:** It defines how geometric questions are answered for each pixel ray, converting abstract scene data into visible color contributions.

## Q16: Why does writing image files matter more in a GPU raytracer?
**A:** Because millions of rays run concurrently; writing image files determines whether each thread can proceed independently or stalls on divergent geometry work.

## Q17: Describe the main correctness concern in writing image files.
**A:** Precision: numerically unstable writing image files causes gaps, shadow acne, and flicker; consistently evaluate in double or carefully-ordered floats.

## Q18: How does writing image files affect perceptual quality?
**A:** Small errors in writing image files show up as aliasing, hard shadows, or wrong silhouettes long before an average viewer can name the cause.

## Q19: What is the standard way to structure writing image files code?
**A:** Separate pure functions (no state) so writing image files compiles to fast device code and can be unit-tested on the host with the same inputs.

## Q20: How do you benchmark writing image files?
**A:** Render a fixed scene at multiple resolutions, measure rays/second, and compare against an analytic ground truth for identical camera settings.

## Q21: When does writing image files produce artifacts?
**A:** When step sizes, tolerances, or intersection epsilons are tuned wrong - the classic acne/darkening trade-off of writing image files.

## Q22: How should writing image files handle edge cases like grazing angles?
**A:** Use robust predicates and minimum epsilon displacements so writing image files stays stable exactly where classic plane tests degenerate.

## Q23: What relationship does writing image files have with the rest of the pipeline?
**A:** writing image files produces the input for shading and post-processing; any error here is amplified by everything downstream.

## Q24: How do you make writing image files deterministic across runs?
**A:** Fix the accumulation order and sampling seed per pixel so writing image files reproduces bit-identical output for the same scene and parameters.

## Q25: Give a production example of writing image files in the black-hole visualizer.
**A:** Tracing a photon through the accretion flow uses writing image files at every step: intersect the disk plane, sample the field, and terminate at horizon or sky.

## Q26: What should you test about writing image files?
**A:** Golden images for a handful of scenes, analytic sizes for primitive shapes, and monotonic quality as samples increase for writing image files.

## Q27: How does writing image files interact with antialiasing?
**A:** Antialiasing launches many slightly different rays; writing image files must keep their per-ray state separate so samples blend correctly.

## Q28: What falls in the domain of writing image files vs rendering?
**A:** writing image files is geometric answer-finding; rendering decides color, lighting, and tone mapping from those answers - keep the boundary clean.

## Q29: What is the most common performance trap in writing image files?
**A:** Recomputing the same expensive data per ray instead of caching it in constant or shared memory before the writing image files loop starts.

## Q30: How do you explain writing image files trade-offs on a single slide?
**A:** A table: approach, cost per ray, memory, robustness, and GPU friendliness - summarize writing image files options in one comparison view.

## Q31: What happens if writing image files is not monotonic with samples?
**A:** The image converges to the wrong value, revealing a bug; writing image files results must approach a stable limit as sampling grows.

## Q32: How do you port writing image files from CPU to GPU?
**A:** Keep the math identical in device functions, inline the hot loops, and replace heap allocations with pre-allocated buffers for writing image files.

## Q33: What are the output guarantees of writing image files?
**A:** A per-pixel radiance estimate (and optionally depth/ray state) that downstream tone mapping can trust - the contract of writing image files.

## Q34: When is brute force acceptable for writing image files?
**A:** For a handful of primitives or when ray count dominates; then the cost of writing image files acceleration structures exceeds their savings.

## Q35: How does writing image files fit into a modular architecture?
**A:** As a component behind a stable interface - the renderer calls writing image files and never depends on its implementation details.

## Q36: What does a rigorous test suite assert about writing image files?
**A:** Correctness on constructed scenes, performance on a benchmark scene, and stability (no NaN/Inf) across resolution ranges.

## Q37: What tools measure writing image files quality?
**A:** A/B images, per-pixel error maps against reference, and error-vs-samples curves are the quantitative tools for writing image files.

## Q38: How do you teach writing image files fundamentals?
**A:** Start with a pinhole camera and a sphere; every later feature builds on the same try-a-ray, find-an-answer shape of writing image files.

## Q39: How do you teach writing image files fundamentals - justify your answer with a concrete production example.
**A:** Start with a pinhole camera and a sphere; every later feature builds on the same try-a-ray, find-an-answer shape of writing image files. A concrete example: consistently applying writing image files in code review and regression tests keeps the whole pipeline trustworthy.

## Q40: What tools measure writing image files quality - justify your answer with a concrete production example.
**A:** A/B images, per-pixel error maps against reference, and error-vs-samples curves are the quantitative tools for writing image files. A concrete example: consistently applying writing image files in code review and regression tests keeps the whole pipeline trustworthy.

## Q41: What does a rigorous test suite assert about writing image files - justify your answer with a concrete production example.
**A:** Correctness on constructed scenes, performance on a benchmark scene, and stability (no NaN/Inf) across resolution ranges. A concrete example: consistently applying writing image files in code review and regression tests keeps the whole pipeline trustworthy.

## Q42: How does writing image files fit into a modular architecture - justify your answer with a concrete production example.
**A:** As a component behind a stable interface - the renderer calls writing image files and never depends on its implementation details. A concrete example: consistently applying writing image files in code review and regression tests keeps the whole pipeline trustworthy.

## Q43: When is brute force acceptable for writing image files - justify your answer with a concrete production example.
**A:** For a handful of primitives or when ray count dominates; then the cost of writing image files acceleration structures exceeds their savings. A concrete example: consistently applying writing image files in code review and regression tests keeps the whole pipeline trustworthy.

## Q44: What are the output guarantees of writing image files - justify your answer with a concrete production example.
**A:** A per-pixel radiance estimate (and optionally depth/ray state) that downstream tone mapping can trust - the contract of writing image files. A concrete example: consistently applying writing image files in code review and regression tests keeps the whole pipeline trustworthy.

## Q45: How do you port writing image files from CPU to GPU - justify your answer with a concrete production example.
**A:** Keep the math identical in device functions, inline the hot loops, and replace heap allocations with pre-allocated buffers for writing image files. A concrete example: consistently applying writing image files in code review and regression tests keeps the whole pipeline trustworthy.

## Q46: What happens if writing image files is not monotonic with samples - justify your answer with a concrete production example.
**A:** The image converges to the wrong value, revealing a bug; writing image files results must approach a stable limit as sampling grows. A concrete example: consistently applying writing image files in code review and regression tests keeps the whole pipeline trustworthy.

## Q47: How do you explain writing image files trade-offs on a single slide - justify your answer with a concrete production example.
**A:** A table: approach, cost per ray, memory, robustness, and GPU friendliness - summarize writing image files options in one comparison view. A concrete example: consistently applying writing image files in code review and regression tests keeps the whole pipeline trustworthy.

## Q48: What is the most common performance trap in writing image files - justify your answer with a concrete production example.
**A:** Recomputing the same expensive data per ray instead of caching it in constant or shared memory before the writing image files loop starts. A concrete example: consistently applying writing image files in code review and regression tests keeps the whole pipeline trustworthy.

## Q49: What falls in the domain of writing image files vs rendering - justify your answer with a concrete production example.
**A:** writing image files is geometric answer-finding; rendering decides color, lighting, and tone mapping from those answers - keep the boundary clean. A concrete example: consistently applying writing image files in code review and regression tests keeps the whole pipeline trustworthy.

## Q50: How does writing image files interact with antialiasing - justify your answer with a concrete production example.
**A:** Antialiasing launches many slightly different rays; writing image files must keep their per-ray state separate so samples blend correctly. A concrete example: consistently applying writing image files in code review and regression tests keeps the whole pipeline trustworthy.

## Q51: What should you test about writing image files - justify your answer with a concrete production example.
**A:** Golden images for a handful of scenes, analytic sizes for primitive shapes, and monotonic quality as samples increase for writing image files. A concrete example: consistently applying writing image files in code review and regression tests keeps the whole pipeline trustworthy.

## Q52: Give a production example of writing image files in the black-hole visualizer - justify your answer with a concrete production example.
**A:** Tracing a photon through the accretion flow uses writing image files at every step: intersect the disk plane, sample the field, and terminate at horizon or sky. A concrete example: consistently applying writing image files in code review and regression tests keeps the whole pipeline trustworthy.

## Q53: How do you make writing image files deterministic across runs - justify your answer with a concrete production example.
**A:** Fix the accumulation order and sampling seed per pixel so writing image files reproduces bit-identical output for the same scene and parameters. A concrete example: consistently applying writing image files in code review and regression tests keeps the whole pipeline trustworthy.

## Q54: What relationship does writing image files have with the rest of the pipeline - justify your answer with a concrete production example.
**A:** writing image files produces the input for shading and post-processing; any error here is amplified by everything downstream. A concrete example: consistently applying writing image files in code review and regression tests keeps the whole pipeline trustworthy.

## Q55: How should writing image files handle edge cases like grazing angles - justify your answer with a concrete production example.
**A:** Use robust predicates and minimum epsilon displacements so writing image files stays stable exactly where classic plane tests degenerate. A concrete example: consistently applying writing image files in code review and regression tests keeps the whole pipeline trustworthy.

## Q56: When does writing image files produce artifacts - justify your answer with a concrete production example.
**A:** When step sizes, tolerances, or intersection epsilons are tuned wrong - the classic acne/darkening trade-off of writing image files. A concrete example: consistently applying writing image files in code review and regression tests keeps the whole pipeline trustworthy.

## Q57: How do you benchmark writing image files - justify your answer with a concrete production example.
**A:** Render a fixed scene at multiple resolutions, measure rays/second, and compare against an analytic ground truth for identical camera settings. A concrete example: consistently applying writing image files in code review and regression tests keeps the whole pipeline trustworthy.

## Q58: What is the standard way to structure writing image files code - justify your answer with a concrete production example.
**A:** Separate pure functions (no state) so writing image files compiles to fast device code and can be unit-tested on the host with the same inputs. A concrete example: consistently applying writing image files in code review and regression tests keeps the whole pipeline trustworthy.

## Q59: How does writing image files affect perceptual quality - justify your answer with a concrete production example.
**A:** Small errors in writing image files show up as aliasing, hard shadows, or wrong silhouettes long before an average viewer can name the cause. A concrete example: consistently applying writing image files in code review and regression tests keeps the whole pipeline trustworthy.

## Q60: Describe the main correctness concern in writing image files - justify your answer with a concrete production example.
**A:** Precision: numerically unstable writing image files causes gaps, shadow acne, and flicker; consistently evaluate in double or carefully-ordered floats. A concrete example: consistently applying writing image files in code review and regression tests keeps the whole pipeline trustworthy.

## Q61: Why does writing image files matter more in a GPU raytracer - justify your answer with a concrete production example.
**A:** Because millions of rays run concurrently; writing image files determines whether each thread can proceed independently or stalls on divergent geometry work. A concrete example: consistently applying writing image files in code review and regression tests keeps the whole pipeline trustworthy.

## Q62: What is the purpose of writing image files in a raytracer - justify your answer with a concrete production example.
**A:** It defines how geometric questions are answered for each pixel ray, converting abstract scene data into visible color contributions. A concrete example: consistently applying writing image files in code review and regression tests keeps the whole pipeline trustworthy.

## Q63: What is the purpose of writing image files in a raytracer - justify your answer with a concrete production example.
**A:** It defines how geometric questions are answered for each pixel ray, converting abstract scene data into visible color contributions. A concrete example: consistently applying writing image files in code review and regression tests keeps the whole pipeline trustworthy.

## Q64: Why does writing image files matter more in a GPU raytracer - justify your answer with a concrete production example.
**A:** Because millions of rays run concurrently; writing image files determines whether each thread can proceed independently or stalls on divergent geometry work. A concrete example: consistently applying writing image files in code review and regression tests keeps the whole pipeline trustworthy.

## Q65: Describe the main correctness concern in writing image files - justify your answer with a concrete production example.
**A:** Precision: numerically unstable writing image files causes gaps, shadow acne, and flicker; consistently evaluate in double or carefully-ordered floats. A concrete example: consistently applying writing image files in code review and regression tests keeps the whole pipeline trustworthy.

## Q66: How does writing image files affect perceptual quality - justify your answer with a concrete production example.
**A:** Small errors in writing image files show up as aliasing, hard shadows, or wrong silhouettes long before an average viewer can name the cause. A concrete example: consistently applying writing image files in code review and regression tests keeps the whole pipeline trustworthy.

## Q67: What is the standard way to structure writing image files code - justify your answer with a concrete production example.
**A:** Separate pure functions (no state) so writing image files compiles to fast device code and can be unit-tested on the host with the same inputs. A concrete example: consistently applying writing image files in code review and regression tests keeps the whole pipeline trustworthy.

## Q68: How do you benchmark writing image files - justify your answer with a concrete production example.
**A:** Render a fixed scene at multiple resolutions, measure rays/second, and compare against an analytic ground truth for identical camera settings. A concrete example: consistently applying writing image files in code review and regression tests keeps the whole pipeline trustworthy.

## Q69: When does writing image files produce artifacts - justify your answer with a concrete production example.
**A:** When step sizes, tolerances, or intersection epsilons are tuned wrong - the classic acne/darkening trade-off of writing image files. A concrete example: consistently applying writing image files in code review and regression tests keeps the whole pipeline trustworthy.

## Q70: How should writing image files handle edge cases like grazing angles - justify your answer with a concrete production example.
**A:** Use robust predicates and minimum epsilon displacements so writing image files stays stable exactly where classic plane tests degenerate. A concrete example: consistently applying writing image files in code review and regression tests keeps the whole pipeline trustworthy.

## Q71: What relationship does writing image files have with the rest of the pipeline - justify your answer with a concrete production example.
**A:** writing image files produces the input for shading and post-processing; any error here is amplified by everything downstream. A concrete example: consistently applying writing image files in code review and regression tests keeps the whole pipeline trustworthy.

## Q72: How do you make writing image files deterministic across runs - justify your answer with a concrete production example.
**A:** Fix the accumulation order and sampling seed per pixel so writing image files reproduces bit-identical output for the same scene and parameters. A concrete example: consistently applying writing image files in code review and regression tests keeps the whole pipeline trustworthy.

## Q73: Give a production example of writing image files in the black-hole visualizer - justify your answer with a concrete production example.
**A:** Tracing a photon through the accretion flow uses writing image files at every step: intersect the disk plane, sample the field, and terminate at horizon or sky. A concrete example: consistently applying writing image files in code review and regression tests keeps the whole pipeline trustworthy.

## Q74: What should you test about writing image files - justify your answer with a concrete production example.
**A:** Golden images for a handful of scenes, analytic sizes for primitive shapes, and monotonic quality as samples increase for writing image files. A concrete example: consistently applying writing image files in code review and regression tests keeps the whole pipeline trustworthy.

## Q75: How does writing image files interact with antialiasing - justify your answer with a concrete production example.
**A:** Antialiasing launches many slightly different rays; writing image files must keep their per-ray state separate so samples blend correctly. A concrete example: consistently applying writing image files in code review and regression tests keeps the whole pipeline trustworthy.

## Q76: What falls in the domain of writing image files vs rendering - justify your answer with a concrete production example.
**A:** writing image files is geometric answer-finding; rendering decides color, lighting, and tone mapping from those answers - keep the boundary clean. A concrete example: consistently applying writing image files in code review and regression tests keeps the whole pipeline trustworthy.

## Q77: What is the most common performance trap in writing image files - justify your answer with a concrete production example.
**A:** Recomputing the same expensive data per ray instead of caching it in constant or shared memory before the writing image files loop starts. A concrete example: consistently applying writing image files in code review and regression tests keeps the whole pipeline trustworthy.

## Q78: How do you explain writing image files trade-offs on a single slide - justify your answer with a concrete production example.
**A:** A table: approach, cost per ray, memory, robustness, and GPU friendliness - summarize writing image files options in one comparison view. A concrete example: consistently applying writing image files in code review and regression tests keeps the whole pipeline trustworthy.

## Q79: What happens if writing image files is not monotonic with samples - justify your answer with a concrete production example.
**A:** The image converges to the wrong value, revealing a bug; writing image files results must approach a stable limit as sampling grows. A concrete example: consistently applying writing image files in code review and regression tests keeps the whole pipeline trustworthy.

## Q80: How do you port writing image files from CPU to GPU - justify your answer with a concrete production example.
**A:** Keep the math identical in device functions, inline the hot loops, and replace heap allocations with pre-allocated buffers for writing image files. A concrete example: consistently applying writing image files in code review and regression tests keeps the whole pipeline trustworthy.

## Q81: What are the output guarantees of writing image files - justify your answer with a concrete production example.
**A:** A per-pixel radiance estimate (and optionally depth/ray state) that downstream tone mapping can trust - the contract of writing image files. A concrete example: consistently applying writing image files in code review and regression tests keeps the whole pipeline trustworthy.

## Q82: When is brute force acceptable for writing image files - justify your answer with a concrete production example.
**A:** For a handful of primitives or when ray count dominates; then the cost of writing image files acceleration structures exceeds their savings. A concrete example: consistently applying writing image files in code review and regression tests keeps the whole pipeline trustworthy.

## Q83: How does writing image files fit into a modular architecture - justify your answer with a concrete production example.
**A:** As a component behind a stable interface - the renderer calls writing image files and never depends on its implementation details. A concrete example: consistently applying writing image files in code review and regression tests keeps the whole pipeline trustworthy.

## Q84: What does a rigorous test suite assert about writing image files - justify your answer with a concrete production example.
**A:** Correctness on constructed scenes, performance on a benchmark scene, and stability (no NaN/Inf) across resolution ranges. A concrete example: consistently applying writing image files in code review and regression tests keeps the whole pipeline trustworthy.

## Q85: What tools measure writing image files quality - justify your answer with a concrete production example.
**A:** A/B images, per-pixel error maps against reference, and error-vs-samples curves are the quantitative tools for writing image files. A concrete example: consistently applying writing image files in code review and regression tests keeps the whole pipeline trustworthy.

## Q86: How do you teach writing image files fundamentals - justify your answer with a concrete production example.
**A:** Start with a pinhole camera and a sphere; every later feature builds on the same try-a-ray, find-an-answer shape of writing image files. A concrete example: consistently applying writing image files in code review and regression tests keeps the whole pipeline trustworthy.

## Q87: How do you teach writing image files fundamentals - justify your answer with a concrete production example.
**A:** Start with a pinhole camera and a sphere; every later feature builds on the same try-a-ray, find-an-answer shape of writing image files. A concrete example: consistently applying writing image files in code review and regression tests keeps the whole pipeline trustworthy.

## Q88: What tools measure writing image files quality - justify your answer with a concrete production example.
**A:** A/B images, per-pixel error maps against reference, and error-vs-samples curves are the quantitative tools for writing image files. A concrete example: consistently applying writing image files in code review and regression tests keeps the whole pipeline trustworthy.

## Q89: What does a rigorous test suite assert about writing image files - justify your answer with a concrete production example.
**A:** Correctness on constructed scenes, performance on a benchmark scene, and stability (no NaN/Inf) across resolution ranges. A concrete example: consistently applying writing image files in code review and regression tests keeps the whole pipeline trustworthy.

## Q90: How does writing image files fit into a modular architecture - justify your answer with a concrete production example.
**A:** As a component behind a stable interface - the renderer calls writing image files and never depends on its implementation details. A concrete example: consistently applying writing image files in code review and regression tests keeps the whole pipeline trustworthy.

## Q91: When is brute force acceptable for writing image files - justify your answer with a concrete production example.
**A:** For a handful of primitives or when ray count dominates; then the cost of writing image files acceleration structures exceeds their savings. A concrete example: consistently applying writing image files in code review and regression tests keeps the whole pipeline trustworthy.

## Q92: What are the output guarantees of writing image files - justify your answer with a concrete production example.
**A:** A per-pixel radiance estimate (and optionally depth/ray state) that downstream tone mapping can trust - the contract of writing image files. A concrete example: consistently applying writing image files in code review and regression tests keeps the whole pipeline trustworthy.

## Q93: How do you port writing image files from CPU to GPU - justify your answer with a concrete production example.
**A:** Keep the math identical in device functions, inline the hot loops, and replace heap allocations with pre-allocated buffers for writing image files. A concrete example: consistently applying writing image files in code review and regression tests keeps the whole pipeline trustworthy.

## Q94: What happens if writing image files is not monotonic with samples - justify your answer with a concrete production example.
**A:** The image converges to the wrong value, revealing a bug; writing image files results must approach a stable limit as sampling grows. A concrete example: consistently applying writing image files in code review and regression tests keeps the whole pipeline trustworthy.

## Q95: How do you explain writing image files trade-offs on a single slide - justify your answer with a concrete production example.
**A:** A table: approach, cost per ray, memory, robustness, and GPU friendliness - summarize writing image files options in one comparison view. A concrete example: consistently applying writing image files in code review and regression tests keeps the whole pipeline trustworthy.

## Q96: What is the most common performance trap in writing image files - justify your answer with a concrete production example.
**A:** Recomputing the same expensive data per ray instead of caching it in constant or shared memory before the writing image files loop starts. A concrete example: consistently applying writing image files in code review and regression tests keeps the whole pipeline trustworthy.

## Q97: What falls in the domain of writing image files vs rendering - justify your answer with a concrete production example.
**A:** writing image files is geometric answer-finding; rendering decides color, lighting, and tone mapping from those answers - keep the boundary clean. A concrete example: consistently applying writing image files in code review and regression tests keeps the whole pipeline trustworthy.

## Q98: How does writing image files interact with antialiasing - justify your answer with a concrete production example.
**A:** Antialiasing launches many slightly different rays; writing image files must keep their per-ray state separate so samples blend correctly. A concrete example: consistently applying writing image files in code review and regression tests keeps the whole pipeline trustworthy.

## Q99: What should you test about writing image files - justify your answer with a concrete production example.
**A:** Golden images for a handful of scenes, analytic sizes for primitive shapes, and monotonic quality as samples increase for writing image files. A concrete example: consistently applying writing image files in code review and regression tests keeps the whole pipeline trustworthy.

## Q100: Give a production example of writing image files in the black-hole visualizer - justify your answer with a concrete production example.
**A:** Tracing a photon through the accretion flow uses writing image files at every step: intersect the disk plane, sample the field, and terminate at horizon or sky. A concrete example: consistently applying writing image files in code review and regression tests keeps the whole pipeline trustworthy.
