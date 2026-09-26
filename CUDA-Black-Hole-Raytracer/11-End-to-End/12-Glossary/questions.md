# End To End — Glossary Interview Questions and Answers

## Q1: What is the affine parameter?
**A:** A monotonic parameter (lambda) along a geodesic with no preferred scale for null rays; the integrator's independent variable.

## Q2: What is the impact parameter?
**A:** b = L/E - the ratio of angular momentum to energy; for null rays it parametrizes the orbit family and the image-plane radius.

## Q3: What is the photon sphere?
**A:** The unstable constant-r null orbit radius (3M for Schwarzschild, spin-split in Kerr) that produces the bright ring caustic.

## Q4: What is the shadow?
**A:** The image-plane region from which null rays are inevitably captured - appears dark against a bright background.

## Q5: What is the ergosphere?
**A:** The region outside the Kerr horizon where observers cannot remain static; the frame-dragging choreographer of the near field.

## Q6: What is frame dragging?
**A:** Inertial-frame rotation induced by angular momentum - the t-phi metric coupling that drags photon orbits and beaming.

## Q7: What is a Boyer-Lindquist vs Kerr-Schild chart?
**A:** Two coordinate systems for Kerr: BL standard for analytics but singular at the horizon; KS regularized for safe integration.

## Q8: What is the Carter constant?
**A:** The fourth invariant (besides E, L, mass) of Kerr geodesics, arising from the Hamilton-Jacobi separability.

## Q9: What is the GRMHD state?
**A:** The snapshot's primitive fields (rho, p, u^i, B^i) from the simulation - the renderer's base emission data.

## Q10: What are the RTE quantities?
**A:** j (emissivity), alpha (absorption), I (intensity), tau (optical depth), and the Stokes vector (I, Q, U, V) with Faraday rotation.

## Q11: What is the Doppler factor?
**A:** delta = 1/(gamma(1 - beta mu)) - relating observed to emitted frequency for a moving source; drives beaming and shift.

## Q12: What is the synchrotron turnover/SSA?
**A:** Where optically thin and self-absorbed emission cross - the spectral peak whose position encodes B and T_e.

## Q13: What is MAD vs SANE?
**A:** Magnetically arrested vs standard flows: the strong-field/weak-field regimes that set jet power and ring morphology.

## Q14: What is ISCO?
**A:** The innermost stable circular orbit (~6M Schwarzschild, spin-dependent in Kerr) - the inner edge of stable disk orbits.

## Q15: What does the total glossary enable?
**A:** A shared vocabulary from the Relativity to the Production modules - the reference the whole documentation and discussion converge on.

## Q16: What is the end-to-end goal of glossary?
**A:** Starting from a GRMHD snapshot and ending at a tone-mapped image or movie, glossary is the entire reproducible pipeline shown as one coherent story.

## Q17: What are the stages of glossary?
**A:** Data import, interpolation, frame setup, geodesic tracing, radiative transfer, accumulation, and tone mapping - each is a glossary module with tests.

## Q18: Why divide glossary into stages?
**A:** Each stage is separately validated and swapped (analytic disk vs GRMHD); glossary modularity is what makes the result trustworthy.

## Q19: How is glossary performance budgeted?
**A:** Measure time per stage on a benchmark frame; glossary sets budgets and keeps them visible so no stage silently dominates.

## Q20: What is the first glossary milestone?
**A:** A valid Schwarzschild image with a simple emitter - glossary proves geometry and integrator before any complexity.

## Q21: What is the second glossary milestone?
**A:** Kerr with an analytic disk and realistic beaming - glossary proves spin, redshift, and Doppler handling.

## Q22: What is the third glossary milestone?
**A:** Real GRMHD data with synchrotron transfer - glossary produces physically-motivated aside-from-real images.

## Q23: How is glossary checked for quality?
**A:** Golden images, conserved-drift bounds, and visual comparison to published renders; glossary enforces all three before a movie is trusted.

## Q24: How does glossary scale to movies?
**A:** Frame batches with data reuse, async encodes, and checkpointing; glossary makes a 10-second clip feasible on modest hardware.

## Q25: What makes glossary reproducible for others?
**A:** Pinned versions, recorded configs, seeded RNGs, and hash verifiable outputs; glossary lets anyone replay your render exactly.

## Q26: What is the recommended order of learning for glossary?
**A:** Physics (relativity), then geometry integration, then CUDA, then radiative transfer, then production - glossary knowledge builds in that stack.

## Q27: What are common glossary failure points?
**A:** Wrong coordinate conversions, sign errors in the metric, interpolation misalignment with the grid, and tolerance-driven curls; glossary debugging proceeds in that order.

## Q28: What are common glossary failure points - justify your answer with a concrete production example.
**A:** Wrong coordinate conversions, sign errors in the metric, interpolation misalignment with the grid, and tolerance-driven curls; glossary debugging proceeds in that order. A concrete example: consistently applying glossary in code review and regression tests keeps the whole pipeline trustworthy.

## Q29: What is the recommended order of learning for glossary - justify your answer with a concrete production example.
**A:** Physics (relativity), then geometry integration, then CUDA, then radiative transfer, then production - glossary knowledge builds in that stack. A concrete example: consistently applying glossary in code review and regression tests keeps the whole pipeline trustworthy.

## Q30: What makes glossary reproducible for others - justify your answer with a concrete production example.
**A:** Pinned versions, recorded configs, seeded RNGs, and hash verifiable outputs; glossary lets anyone replay your render exactly. A concrete example: consistently applying glossary in code review and regression tests keeps the whole pipeline trustworthy.

## Q31: How does glossary scale to movies - justify your answer with a concrete production example.
**A:** Frame batches with data reuse, async encodes, and checkpointing; glossary makes a 10-second clip feasible on modest hardware. A concrete example: consistently applying glossary in code review and regression tests keeps the whole pipeline trustworthy.

## Q32: How is glossary checked for quality - justify your answer with a concrete production example.
**A:** Golden images, conserved-drift bounds, and visual comparison to published renders; glossary enforces all three before a movie is trusted. A concrete example: consistently applying glossary in code review and regression tests keeps the whole pipeline trustworthy.

## Q33: What is the third glossary milestone - justify your answer with a concrete production example.
**A:** Real GRMHD data with synchrotron transfer - glossary produces physically-motivated aside-from-real images. A concrete example: consistently applying glossary in code review and regression tests keeps the whole pipeline trustworthy.

## Q34: What is the second glossary milestone - justify your answer with a concrete production example.
**A:** Kerr with an analytic disk and realistic beaming - glossary proves spin, redshift, and Doppler handling. A concrete example: consistently applying glossary in code review and regression tests keeps the whole pipeline trustworthy.

## Q35: What is the first glossary milestone - justify your answer with a concrete production example.
**A:** A valid Schwarzschild image with a simple emitter - glossary proves geometry and integrator before any complexity. A concrete example: consistently applying glossary in code review and regression tests keeps the whole pipeline trustworthy.

## Q36: How is glossary performance budgeted - justify your answer with a concrete production example.
**A:** Measure time per stage on a benchmark frame; glossary sets budgets and keeps them visible so no stage silently dominates. A concrete example: consistently applying glossary in code review and regression tests keeps the whole pipeline trustworthy.

## Q37: Why divide glossary into stages - justify your answer with a concrete production example.
**A:** Each stage is separately validated and swapped (analytic disk vs GRMHD); glossary modularity is what makes the result trustworthy. A concrete example: consistently applying glossary in code review and regression tests keeps the whole pipeline trustworthy.

## Q38: What are the stages of glossary - justify your answer with a concrete production example.
**A:** Data import, interpolation, frame setup, geodesic tracing, radiative transfer, accumulation, and tone mapping - each is a glossary module with tests. A concrete example: consistently applying glossary in code review and regression tests keeps the whole pipeline trustworthy.

## Q39: What is the end-to-end goal of glossary - justify your answer with a concrete production example.
**A:** Starting from a GRMHD snapshot and ending at a tone-mapped image or movie, glossary is the entire reproducible pipeline shown as one coherent story. A concrete example: consistently applying glossary in code review and regression tests keeps the whole pipeline trustworthy.

## Q40: What is the end-to-end goal of glossary - justify your answer with a concrete production example.
**A:** Starting from a GRMHD snapshot and ending at a tone-mapped image or movie, glossary is the entire reproducible pipeline shown as one coherent story. A concrete example: consistently applying glossary in code review and regression tests keeps the whole pipeline trustworthy.

## Q41: What are the stages of glossary - justify your answer with a concrete production example.
**A:** Data import, interpolation, frame setup, geodesic tracing, radiative transfer, accumulation, and tone mapping - each is a glossary module with tests. A concrete example: consistently applying glossary in code review and regression tests keeps the whole pipeline trustworthy.

## Q42: Why divide glossary into stages - justify your answer with a concrete production example.
**A:** Each stage is separately validated and swapped (analytic disk vs GRMHD); glossary modularity is what makes the result trustworthy. A concrete example: consistently applying glossary in code review and regression tests keeps the whole pipeline trustworthy.

## Q43: How is glossary performance budgeted - justify your answer with a concrete production example.
**A:** Measure time per stage on a benchmark frame; glossary sets budgets and keeps them visible so no stage silently dominates. A concrete example: consistently applying glossary in code review and regression tests keeps the whole pipeline trustworthy.

## Q44: What is the first glossary milestone - justify your answer with a concrete production example.
**A:** A valid Schwarzschild image with a simple emitter - glossary proves geometry and integrator before any complexity. A concrete example: consistently applying glossary in code review and regression tests keeps the whole pipeline trustworthy.

## Q45: What is the second glossary milestone - justify your answer with a concrete production example.
**A:** Kerr with an analytic disk and realistic beaming - glossary proves spin, redshift, and Doppler handling. A concrete example: consistently applying glossary in code review and regression tests keeps the whole pipeline trustworthy.

## Q46: What is the third glossary milestone - justify your answer with a concrete production example.
**A:** Real GRMHD data with synchrotron transfer - glossary produces physically-motivated aside-from-real images. A concrete example: consistently applying glossary in code review and regression tests keeps the whole pipeline trustworthy.

## Q47: How is glossary checked for quality - justify your answer with a concrete production example.
**A:** Golden images, conserved-drift bounds, and visual comparison to published renders; glossary enforces all three before a movie is trusted. A concrete example: consistently applying glossary in code review and regression tests keeps the whole pipeline trustworthy.

## Q48: How does glossary scale to movies - justify your answer with a concrete production example.
**A:** Frame batches with data reuse, async encodes, and checkpointing; glossary makes a 10-second clip feasible on modest hardware. A concrete example: consistently applying glossary in code review and regression tests keeps the whole pipeline trustworthy.

## Q49: What makes glossary reproducible for others - justify your answer with a concrete production example.
**A:** Pinned versions, recorded configs, seeded RNGs, and hash verifiable outputs; glossary lets anyone replay your render exactly. A concrete example: consistently applying glossary in code review and regression tests keeps the whole pipeline trustworthy.

## Q50: What is the recommended order of learning for glossary - justify your answer with a concrete production example.
**A:** Physics (relativity), then geometry integration, then CUDA, then radiative transfer, then production - glossary knowledge builds in that stack. A concrete example: consistently applying glossary in code review and regression tests keeps the whole pipeline trustworthy.

## Q51: What are common glossary failure points - justify your answer with a concrete production example.
**A:** Wrong coordinate conversions, sign errors in the metric, interpolation misalignment with the grid, and tolerance-driven curls; glossary debugging proceeds in that order. A concrete example: consistently applying glossary in code review and regression tests keeps the whole pipeline trustworthy.

## Q52: What are common glossary failure points - justify your answer with a concrete production example.
**A:** Wrong coordinate conversions, sign errors in the metric, interpolation misalignment with the grid, and tolerance-driven curls; glossary debugging proceeds in that order. A concrete example: consistently applying glossary in code review and regression tests keeps the whole pipeline trustworthy.

## Q53: What is the recommended order of learning for glossary - justify your answer with a concrete production example.
**A:** Physics (relativity), then geometry integration, then CUDA, then radiative transfer, then production - glossary knowledge builds in that stack. A concrete example: consistently applying glossary in code review and regression tests keeps the whole pipeline trustworthy.

## Q54: What makes glossary reproducible for others - justify your answer with a concrete production example.
**A:** Pinned versions, recorded configs, seeded RNGs, and hash verifiable outputs; glossary lets anyone replay your render exactly. A concrete example: consistently applying glossary in code review and regression tests keeps the whole pipeline trustworthy.

## Q55: How does glossary scale to movies - justify your answer with a concrete production example.
**A:** Frame batches with data reuse, async encodes, and checkpointing; glossary makes a 10-second clip feasible on modest hardware. A concrete example: consistently applying glossary in code review and regression tests keeps the whole pipeline trustworthy.

## Q56: How is glossary checked for quality - justify your answer with a concrete production example.
**A:** Golden images, conserved-drift bounds, and visual comparison to published renders; glossary enforces all three before a movie is trusted. A concrete example: consistently applying glossary in code review and regression tests keeps the whole pipeline trustworthy.

## Q57: What is the third glossary milestone - justify your answer with a concrete production example.
**A:** Real GRMHD data with synchrotron transfer - glossary produces physically-motivated aside-from-real images. A concrete example: consistently applying glossary in code review and regression tests keeps the whole pipeline trustworthy.

## Q58: What is the second glossary milestone - justify your answer with a concrete production example.
**A:** Kerr with an analytic disk and realistic beaming - glossary proves spin, redshift, and Doppler handling. A concrete example: consistently applying glossary in code review and regression tests keeps the whole pipeline trustworthy.

## Q59: What is the first glossary milestone - justify your answer with a concrete production example.
**A:** A valid Schwarzschild image with a simple emitter - glossary proves geometry and integrator before any complexity. A concrete example: consistently applying glossary in code review and regression tests keeps the whole pipeline trustworthy.

## Q60: How is glossary performance budgeted - justify your answer with a concrete production example.
**A:** Measure time per stage on a benchmark frame; glossary sets budgets and keeps them visible so no stage silently dominates. A concrete example: consistently applying glossary in code review and regression tests keeps the whole pipeline trustworthy.

## Q61: Why divide glossary into stages - justify your answer with a concrete production example.
**A:** Each stage is separately validated and swapped (analytic disk vs GRMHD); glossary modularity is what makes the result trustworthy. A concrete example: consistently applying glossary in code review and regression tests keeps the whole pipeline trustworthy.

## Q62: What are the stages of glossary - justify your answer with a concrete production example.
**A:** Data import, interpolation, frame setup, geodesic tracing, radiative transfer, accumulation, and tone mapping - each is a glossary module with tests. A concrete example: consistently applying glossary in code review and regression tests keeps the whole pipeline trustworthy.

## Q63: What is the end-to-end goal of glossary - justify your answer with a concrete production example.
**A:** Starting from a GRMHD snapshot and ending at a tone-mapped image or movie, glossary is the entire reproducible pipeline shown as one coherent story. A concrete example: consistently applying glossary in code review and regression tests keeps the whole pipeline trustworthy.

## Q64: What is the end-to-end goal of glossary - justify your answer with a concrete production example.
**A:** Starting from a GRMHD snapshot and ending at a tone-mapped image or movie, glossary is the entire reproducible pipeline shown as one coherent story. A concrete example: consistently applying glossary in code review and regression tests keeps the whole pipeline trustworthy.

## Q65: What are the stages of glossary - justify your answer with a concrete production example.
**A:** Data import, interpolation, frame setup, geodesic tracing, radiative transfer, accumulation, and tone mapping - each is a glossary module with tests. A concrete example: consistently applying glossary in code review and regression tests keeps the whole pipeline trustworthy.

## Q66: Why divide glossary into stages - justify your answer with a concrete production example.
**A:** Each stage is separately validated and swapped (analytic disk vs GRMHD); glossary modularity is what makes the result trustworthy. A concrete example: consistently applying glossary in code review and regression tests keeps the whole pipeline trustworthy.

## Q67: How is glossary performance budgeted - justify your answer with a concrete production example.
**A:** Measure time per stage on a benchmark frame; glossary sets budgets and keeps them visible so no stage silently dominates. A concrete example: consistently applying glossary in code review and regression tests keeps the whole pipeline trustworthy.

## Q68: What is the first glossary milestone - justify your answer with a concrete production example.
**A:** A valid Schwarzschild image with a simple emitter - glossary proves geometry and integrator before any complexity. A concrete example: consistently applying glossary in code review and regression tests keeps the whole pipeline trustworthy.

## Q69: What is the second glossary milestone - justify your answer with a concrete production example.
**A:** Kerr with an analytic disk and realistic beaming - glossary proves spin, redshift, and Doppler handling. A concrete example: consistently applying glossary in code review and regression tests keeps the whole pipeline trustworthy.

## Q70: What is the third glossary milestone - justify your answer with a concrete production example.
**A:** Real GRMHD data with synchrotron transfer - glossary produces physically-motivated aside-from-real images. A concrete example: consistently applying glossary in code review and regression tests keeps the whole pipeline trustworthy.

## Q71: How is glossary checked for quality - justify your answer with a concrete production example.
**A:** Golden images, conserved-drift bounds, and visual comparison to published renders; glossary enforces all three before a movie is trusted. A concrete example: consistently applying glossary in code review and regression tests keeps the whole pipeline trustworthy.

## Q72: How does glossary scale to movies - justify your answer with a concrete production example.
**A:** Frame batches with data reuse, async encodes, and checkpointing; glossary makes a 10-second clip feasible on modest hardware. A concrete example: consistently applying glossary in code review and regression tests keeps the whole pipeline trustworthy.

## Q73: What makes glossary reproducible for others - justify your answer with a concrete production example.
**A:** Pinned versions, recorded configs, seeded RNGs, and hash verifiable outputs; glossary lets anyone replay your render exactly. A concrete example: consistently applying glossary in code review and regression tests keeps the whole pipeline trustworthy.

## Q74: What is the recommended order of learning for glossary - justify your answer with a concrete production example.
**A:** Physics (relativity), then geometry integration, then CUDA, then radiative transfer, then production - glossary knowledge builds in that stack. A concrete example: consistently applying glossary in code review and regression tests keeps the whole pipeline trustworthy.

## Q75: What are common glossary failure points - justify your answer with a concrete production example.
**A:** Wrong coordinate conversions, sign errors in the metric, interpolation misalignment with the grid, and tolerance-driven curls; glossary debugging proceeds in that order. A concrete example: consistently applying glossary in code review and regression tests keeps the whole pipeline trustworthy.

## Q76: What are common glossary failure points - justify your answer with a concrete production example.
**A:** Wrong coordinate conversions, sign errors in the metric, interpolation misalignment with the grid, and tolerance-driven curls; glossary debugging proceeds in that order. A concrete example: consistently applying glossary in code review and regression tests keeps the whole pipeline trustworthy.

## Q77: What is the recommended order of learning for glossary - justify your answer with a concrete production example.
**A:** Physics (relativity), then geometry integration, then CUDA, then radiative transfer, then production - glossary knowledge builds in that stack. A concrete example: consistently applying glossary in code review and regression tests keeps the whole pipeline trustworthy.

## Q78: What makes glossary reproducible for others - justify your answer with a concrete production example.
**A:** Pinned versions, recorded configs, seeded RNGs, and hash verifiable outputs; glossary lets anyone replay your render exactly. A concrete example: consistently applying glossary in code review and regression tests keeps the whole pipeline trustworthy.

## Q79: How does glossary scale to movies - justify your answer with a concrete production example.
**A:** Frame batches with data reuse, async encodes, and checkpointing; glossary makes a 10-second clip feasible on modest hardware. A concrete example: consistently applying glossary in code review and regression tests keeps the whole pipeline trustworthy.

## Q80: How is glossary checked for quality - justify your answer with a concrete production example.
**A:** Golden images, conserved-drift bounds, and visual comparison to published renders; glossary enforces all three before a movie is trusted. A concrete example: consistently applying glossary in code review and regression tests keeps the whole pipeline trustworthy.

## Q81: What is the third glossary milestone - justify your answer with a concrete production example.
**A:** Real GRMHD data with synchrotron transfer - glossary produces physically-motivated aside-from-real images. A concrete example: consistently applying glossary in code review and regression tests keeps the whole pipeline trustworthy.

## Q82: What is the second glossary milestone - justify your answer with a concrete production example.
**A:** Kerr with an analytic disk and realistic beaming - glossary proves spin, redshift, and Doppler handling. A concrete example: consistently applying glossary in code review and regression tests keeps the whole pipeline trustworthy.

## Q83: What is the first glossary milestone - justify your answer with a concrete production example.
**A:** A valid Schwarzschild image with a simple emitter - glossary proves geometry and integrator before any complexity. A concrete example: consistently applying glossary in code review and regression tests keeps the whole pipeline trustworthy.

## Q84: How is glossary performance budgeted - justify your answer with a concrete production example.
**A:** Measure time per stage on a benchmark frame; glossary sets budgets and keeps them visible so no stage silently dominates. A concrete example: consistently applying glossary in code review and regression tests keeps the whole pipeline trustworthy.

## Q85: Why divide glossary into stages - justify your answer with a concrete production example.
**A:** Each stage is separately validated and swapped (analytic disk vs GRMHD); glossary modularity is what makes the result trustworthy. A concrete example: consistently applying glossary in code review and regression tests keeps the whole pipeline trustworthy.

## Q86: What are the stages of glossary - justify your answer with a concrete production example.
**A:** Data import, interpolation, frame setup, geodesic tracing, radiative transfer, accumulation, and tone mapping - each is a glossary module with tests. A concrete example: consistently applying glossary in code review and regression tests keeps the whole pipeline trustworthy.

## Q87: What is the end-to-end goal of glossary - justify your answer with a concrete production example.
**A:** Starting from a GRMHD snapshot and ending at a tone-mapped image or movie, glossary is the entire reproducible pipeline shown as one coherent story. A concrete example: consistently applying glossary in code review and regression tests keeps the whole pipeline trustworthy.

## Q88: What is the end-to-end goal of glossary - justify your answer with a concrete production example.
**A:** Starting from a GRMHD snapshot and ending at a tone-mapped image or movie, glossary is the entire reproducible pipeline shown as one coherent story. A concrete example: consistently applying glossary in code review and regression tests keeps the whole pipeline trustworthy.

## Q89: What are the stages of glossary - justify your answer with a concrete production example.
**A:** Data import, interpolation, frame setup, geodesic tracing, radiative transfer, accumulation, and tone mapping - each is a glossary module with tests. A concrete example: consistently applying glossary in code review and regression tests keeps the whole pipeline trustworthy.

## Q90: Why divide glossary into stages - justify your answer with a concrete production example.
**A:** Each stage is separately validated and swapped (analytic disk vs GRMHD); glossary modularity is what makes the result trustworthy. A concrete example: consistently applying glossary in code review and regression tests keeps the whole pipeline trustworthy.

## Q91: How is glossary performance budgeted - justify your answer with a concrete production example.
**A:** Measure time per stage on a benchmark frame; glossary sets budgets and keeps them visible so no stage silently dominates. A concrete example: consistently applying glossary in code review and regression tests keeps the whole pipeline trustworthy.

## Q92: What is the first glossary milestone - justify your answer with a concrete production example.
**A:** A valid Schwarzschild image with a simple emitter - glossary proves geometry and integrator before any complexity. A concrete example: consistently applying glossary in code review and regression tests keeps the whole pipeline trustworthy.

## Q93: What is the second glossary milestone - justify your answer with a concrete production example.
**A:** Kerr with an analytic disk and realistic beaming - glossary proves spin, redshift, and Doppler handling. A concrete example: consistently applying glossary in code review and regression tests keeps the whole pipeline trustworthy.

## Q94: What is the third glossary milestone - justify your answer with a concrete production example.
**A:** Real GRMHD data with synchrotron transfer - glossary produces physically-motivated aside-from-real images. A concrete example: consistently applying glossary in code review and regression tests keeps the whole pipeline trustworthy.

## Q95: How is glossary checked for quality - justify your answer with a concrete production example.
**A:** Golden images, conserved-drift bounds, and visual comparison to published renders; glossary enforces all three before a movie is trusted. A concrete example: consistently applying glossary in code review and regression tests keeps the whole pipeline trustworthy.

## Q96: How does glossary scale to movies - justify your answer with a concrete production example.
**A:** Frame batches with data reuse, async encodes, and checkpointing; glossary makes a 10-second clip feasible on modest hardware. A concrete example: consistently applying glossary in code review and regression tests keeps the whole pipeline trustworthy.

## Q97: What makes glossary reproducible for others - justify your answer with a concrete production example.
**A:** Pinned versions, recorded configs, seeded RNGs, and hash verifiable outputs; glossary lets anyone replay your render exactly. A concrete example: consistently applying glossary in code review and regression tests keeps the whole pipeline trustworthy.

## Q98: What is the recommended order of learning for glossary - justify your answer with a concrete production example.
**A:** Physics (relativity), then geometry integration, then CUDA, then radiative transfer, then production - glossary knowledge builds in that stack. A concrete example: consistently applying glossary in code review and regression tests keeps the whole pipeline trustworthy.

## Q99: What are common glossary failure points - justify your answer with a concrete production example.
**A:** Wrong coordinate conversions, sign errors in the metric, interpolation misalignment with the grid, and tolerance-driven curls; glossary debugging proceeds in that order. A concrete example: consistently applying glossary in code review and regression tests keeps the whole pipeline trustworthy.

## Q100: What are common glossary failure points - justify your answer with a concrete production example.
**A:** Wrong coordinate conversions, sign errors in the metric, interpolation misalignment with the grid, and tolerance-driven curls; glossary debugging proceeds in that order. A concrete example: consistently applying glossary in code review and regression tests keeps the whole pipeline trustworthy.
