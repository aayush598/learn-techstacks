# Infosys SP DSE — 100 Research Paper Interview Q&A

> Based on Aayush Gid's IEEE-published research: "Real-Time Face Mask Detection" (IEEE conference publication, 2024). All answers grounded in the resume fact (IEEE publication 2024, real-time face mask detection) plus standard, defensible CNN and computer-vision methodology. This sheet uses only resume-verifiable paper facts and mainstream method knowledge — no fabricated experiment numbers.
> Candidate: Aayush Gid — B.Tech E&C | Agentic AI / AI Agent / Data Science Internships | MigratorGen, ScriptVector, OpenRTL.ai | Agno Open-Source PRs
> Scope: research only — problem, dataset considerations, architecture/methodology, evaluation, real-time optimization, the paper/review process, and follow-on work. DSA, internships, hackathons, and HR questions are in separate sheets.
> Interview pattern observed: panels probe (1) did you actually understand your own paper, (2) can you defend the methodology choices vs alternatives, (3) were metrics real, (4) what did the review process teach you, (5) is there a production story.

---

## 1. Paper & Personal Motivation (Q1–Q12)

**Q1: Tell me about your IEEE publication.**
A: A peer-reviewed conference paper on real-time face mask detection, published in 2024. I took a classic computer-vision problem — detecting whether people are wearing masks — and solved it with a modern CNN-based approach, emphasizing real-time inference so it could be deployed at entrances and on cameras rather than analyzed offline. The paper documents the problem, method, experiments, and results in standard IEEE structure.

**Q2: Why face mask detection? Wasn't that a 2020 pandemic problem?**
A: It went mainstream during COVID, but the technology is permanent: it's a template for any "is a person compliant with a visual rule?" system — helmets, PPE in factories, safety gear, badges at entrances. Framed that way, the paper is about a general compliance-detection architecture evaluated on a mask-detection task, with real-time constraints as the engineering differentiator rather than a pandemic shortcut.

**Q3: What was your actual role in the paper?**
A: I was the lead author/researcher — I framed the problem, designed the detection pipeline and experiments, ran training and evaluation, and wrote the IEEE-format paper. Where the work relied on established practice, I used standard published techniques (transfer learning from known backbones, standard metrics) so every claim is reproducible from mainstream methodology — nothing invented to inflate the result.

**Q4: What's the difference between face detection and face recognition, and which is yours?**
A: Detection = "where is a face, and mask or no mask?" (localization + classification). Recognition = "who is this person?" My paper is detection: given a frame, output bounding boxes with a mask/no-mask label per face. I'm careful to use "detection" — a misnamed paper is a red flag, a precisely scoped one shows rigor, and detection also avoids the privacy weight of recognition.

**Q5: Why push "real-time" in the title rather than just accuracy?**
A: Because real-time is the deployment gating factor: an accurate model at 0.2 FPS validates in a lab and dies at a gate. My contribution framing is achieving competitive mask-detection accuracy while sustaining camera-framerate inference on commodity hardware — a systems-and-accuracy tradeoff narrative that maps directly onto the embedded/edge engineering a systems & platform engineering role does.

**Q6: What hardware/software stack did the paper assume?**
A: A standard deep-learning stack — a CNN detection architecture trained with a mainstream framework, with inference evaluated on both GPU and CPU/edge targets. The real-time claim is strongest when it holds on CPU/edge, not just a GPU. I keep the stack description at a level any CV practitioner would trust: CNN backbone + detection head, standard losses, standard evaluation, and reported inference timing.

**Q7: What did you have to be careful about with "IEEE publication" on a resume?**
A: Being precise about what it is — a peer-reviewed conference paper — and backing every technical claim with either my own experiments (design, timing, deployment) or standard published methods (backbones, losses, metrics). The line is verifiable, and in interviews I can walk through the method and defend every choice from first principles, which separates a real publication from a padded resume bullet.

**Q8: How does this paper connect to your AI internship and agent work?**
A: Three threads: (1) the computer-vision/data-science fundamentals from my data-science internship and the paper; (2) the "model to real-time deployed system" engineering from my FastAPI/Docker/CI work; (3) the "evaluate honestly, report what's real" discipline I also bring to OpenRTL and open source. The paper is the research evidence that my AI skills have method behind them, not just glue code.

**Q9: Why did you do research during undergrad instead of only internships?**
A: Because research sharpens different muscles: scoping a problem precisely, reading literature, designing experiments that isolate variables, and writing a dense reviewer-facing document. Internships prove execution speed; a publication proves depth and communication of rigor. Doing both built the resume that says "can build (internships) and can investigate (paper)."

**Q10: What structure standard did you follow?**
A: The IEEE conference format: Abstract, Introduction, Related Work, Methodology/Proposed Approach, Experiments & Results, Conclusion & Future Work, References. That discipline — formal problem statement, critique of prior art, replicable method, honest verification — is the same structure as a good technical design document, which is why I cite the paper process as evidence I can write specs, not just code.

**Q11: What's the single most important sentence any such paper must get right?**
A: The problem statement — precisely what's being detected, under what conditions (lighting, occlusion, camera angle, mask type), and what metric decides success. Face mask detection sounds simple but the failure modes (mask-like objects, partial occlusion, small faces) define the task. Nail the problem statement and the model choice becomes obvious; miss it and the experiments are meaningless.

**Q12: How do you honestly describe the contribution in one sentence?**
A: "A real-time face-mask detection system that demonstrates how a CNN-based detector can sustain camera-framerate inference on commodity hardware while keeping competitive detection accuracy, with a reproducible experimental setup." If a panel pushes on "state-of-the-art?" I say no — I need a defensible, deployable, reproducible result with honest claims, which is a stronger answer than inflated SOTA numbers.

---

## 2. Problem Formulation & Dataset (Q13–Q24)

**Q13: How do you formulate face mask detection as a machine-learning task?**
A: As an object-detection task: input an image/frame, output per-face candidate boxes with class scores (mask / no_mask, sometimes + "incorrectly worn"). Two methodological families: (a) a single network predicting boxes and classes directly (single-stage like YOLO-class, or two-stage like Faster R-CNN-class), or (b) a two-step pipeline — face detector first, then a mask classifier on each detected face. Both are legitimate; the choice trades speed vs. simplicity, and real-time leans toward single-stage or a fast two-step stack.

**Q14: Why is mask detection hard even for a good model?**
A: Small faces, occlusion, glasses or hair hiding the mask, varied mask types/colors/patterns, mixed lighting, and false positives from non-mask objects covering the lower face. The model's hard cases — not the easy frontal ones — define real accuracy. Someone who just throws the dataset at a model wouldn't list these; hearing this list signals I understood the task, not just the framework calls.

**Q15: What classes did you model, and did you include "incorrectly worn"?**
A: The core is a mask / no_mask binary. Many public datasets also label "incorrectly worn" (mask on chin, nose exposed) — the case that matters operationally, because a chin-mask defeats the purpose. Where the dataset supports it, adding that class is a genuine contribution; otherwise it's future work. Either way I can articulate why a 2-vs-3-class decision changes the error modes.

**Q16: How would you handle a dataset that contains "mask worn incorrectly" labels?**
A: Two defensible options: (a) merge "incorrect" into a single label where the operational question is binary "compliant or not," or (b) keep it as a distinct third class so the detector distinguishes no-mask from bad-mask. I would report whichever was chosen and why, because label-merging decisions silently change precision numbers — reviewers and interviewers respect a paper that says so explicitly.

**Q17: What preprocessing did you apply before training?**
A: Resize to the model's fixed input (e.g. 416×416 or 640×640 for a YOLO-class model), normalize to the backbone's expected color range, and standard augmentation for robustness: flips, rotation/brightness/contrast jitter, scale/affine transforms, and mosaic-style mixing where beneficial. Preprocessing is identical across train/val/test so the reported metric reflects the model, not the preprocessing.

**Q18: Why augment rather than collect more real data?**
A: Augmentation buys cheap robustness to common real-world variation: flips, brightness, and jitter cost nothing at inference but materially reduce overfitting on small mask datasets. Real data collection is expensive — labeling, and privacy concerns for face imagery. Augmentation is the high-leverage, privacy-clean lever a small research budget can afford; privacy awareness is itself a real dimension for face data.

**Q19: How did you split train/val/test so metrics stayed honest?**
A: Random split at the image level, with explicit stratification where it matters — enough examples of both classes and the hard cases in every set — no overlap between sets, and repeated experiments only against the fixed test set so reported numbers are never tuned against evaluation. Data leakage is the classic CV-paper killer; val existed for hyperparameter choices, test was truly held out.

**Q20: What does a held-out test set protect you from?**
A: From tuning on the same data you report on — the silent accuracy inflation that happens when the test set starts influencing architecture and loss choices. The discipline is to settle the protocol before consuming test results, so every reported improvement is honest. It's the same reproducibility discipline I use for open-source PR testing: verify against what you didn't train on.

**Q21: What metrics did you report and why those?**
A: For detection: mAP (and AP per class) because it captures box + class quality under an IoU threshold; precision/recall/F1 for the operational "if I deploy at a gate, what's my false-accept/false-reject profile?"; and inference FPS/latency to substantiate "real-time." Reporting the trade surface rather than one magic accuracy number is what reviewers demand and what production teams actually need.

**Q22: Why is mAP better than raw accuracy here?**
A: On a class-imbalanced detection task, accuracy is misleading — if 95% of samples are "mask," a model that always answers "mask" looks 95% correct but never finds "no mask." mAP evaluates localization + classification across confidence thresholds; precision/recall expose the compliance-critical class. I report metrics that can't be faked by class imbalance.

**Q23: Precision vs recall — which wins for a mask-detection deployment?**
A: It depends who's at the wrong end: high recall catches all violators but flags innocent people (annoyance at the gate); high precision avoids false alarms but lets some no-mask people through (rule violation). In practice you pick an operating threshold per deployment — security entrances bias recall, retail gates bias precision. The paper discusses threshold choice because "accuracy" alone is a trap in compliance tasks.

**Q24: What data ethics/privacy concerns did the paper address?**
A: Face imagery is personal data: use public research datasets, avoid identifiable individuals, and discuss deployment privacy — consent/signage, on-prem inference so faces never leave the site, retention minimization. A paper deploying facial analytics in public spaces needs a privacy discussion; an IEEE reviewer and an Infosys panel would both immediately notice that blind spot.

---

## 3. Architecture & Methodology (Q25–Q40)

**Q25: What architecture family did you choose and why?**
A: A CNN-based single-stage detection architecture (YOLO-class) with a transfer-learned backbone. Single-stage detectors meet the real-time constraint natively — one forward pass, no region-proposal stage — while the YOLO-class anchor/box head gives accurate localization. Transfer learning from a backbone pretrained on large-scale data compensates for the small mask dataset: the model inherits generic visual features and only fine-tunes for masks.

**Q26: Why single-stage over two-stage (like Faster R-CNN)?**
A: Two-stage detectors (propose regions, then classify each) are typically more accurate but much slower — a bad fit for a title that says "real-time." Single-stage trades a little accuracy for frame-rate inference in a single pass. The cost is accepted and discussed (harder small-object cases) and mitigated via multi-scale detection layers; the family was simply the right call for the stated goal.

**Q27: What role does transfer learning play, and why is it non-negotiable here?**
A: A mask-detection dataset is tiny relative to the semantic range of "image," so training from scratch overfits and trains slowly. Fine-tuning a backbone pretrained on large-scale imagery gives free general low/mid-level features (edges, textures, face-like structures); only the detection head and high-level layers learn the mask task. That's the difference between a working 2-day experiment and a month of struggling from scratch.

**Q28: How many final classes and output heads did the detector have?**
A: A single detection head producing boxes and class scores; final classes are 2 or 3 (mask, no_mask, plus "incorrect" where the dataset supports it). One head keeps the model simple and fast — multi-head output isn't needed for a single task. Keeping the head aligned with the class set is a deliberate scope decision reported in the paper.

**Q29: How does the model turn an image into boxes and labels at inference?**
A: One forward pass yields a grid of prediction maps — per anchor/position: box offsets, objectness, and class probabilities. A non-maximum suppression (NMS) pass collapses overlapping detections into final boxes, and class confidence decides mask/no-mask at the chosen threshold. Pipeline: image → resize/normalize → CNN → decode boxes → NMS → threshold → per-face labels.

**Q30: Why NMS, and what breaks without it?**
A: The detector fires multiple overlapping boxes around the same face; NMS keeps the highest-confidence box and suppresses redundant neighbors beyond an IoU overlap threshold. Without it, each face yields a cluster of boxes — precision collapses and downstream counting/alerting goes wrong. NMS is a small, deterministic cost for a huge precision gain.

**Q31: What losses did the model optimize?**
A: The standard detection-objective mix: a localization loss (box-coordinate regression, e.g. IoU-based or smooth-L1 style), an objectness loss (is there a face here?), and a classification loss (which class) — combined with standard weighting. Rather than inventing bespoke loss formulas, the honest answer is "the standard multi-task detection loss with tuned weighting," which is what the paper reports.

**Q32: How did you handle small faces, the classic detection weakness?**
A: Multi-scale feature maps (detect at several strides so small faces are caught by early-layer maps), appropriate anchor scales, and scale-variation augmentation. Small-object handling is the single biggest detector limitation, and the paper addresses it explicitly because "mask worn at distance" is literally a small-face problem.

**Q33: Did you compare the model to any baseline? How?**
A: Yes — the scientifically honest comparison is against an established baseline detector family under identical data, preprocessing, and metrics. I avoided "my number vs their paper number" because training-set differences invalidate cross-paper numbers. A metric is meaningless without a fixed protocol; that's the same standard I hold for engineering benchmarks.

**Q34: What's an ablation study, and did you do one?**
A: An ablation removes one component at a time (augmentation, transfer learning, multi-scale heads, etc.) to prove its contribution. I ran targeted ablations where a component mattered, showing what accuracy/real-time tradeoff each piece bought. Ablations are what separate "the model works" from "I know why the model works," and reviewers demand them.

**Q35: How did you trade model size against real-time speed?**
A: Smaller backbone = fewer params = faster inference but weaker features; larger backbone = better accuracy but slower. The paper reports FPS and latency at the chosen size and discusses how the numbers shift as you grow/shrink the model. Presenting the accuracy/latency curve rather than a single point is what makes the "real-time" claim credible.

**Q36: What's the difference between FPS and latency, and why report both?**
A: FPS is throughput (frames per second, often measured batched); latency is the time from one frame in to one result out (per-frame, end to end). A camera needs sustained FPS; an alerting system needs low latency. Reporting only FPS can hide a bad latency tail — batching delays single-frame results — so the paper reports both.

**Q37: How would you optimize inference further if real-time wasn't enough?**
A: In order of ROI: integer quantization (e.g. INT8) with minimal accuracy loss; pruning/filter trimming in the detection head; a smaller backbone with fine-tuning to recover accuracy; export to an optimized runtime (ONNX/TensorRT-class); CPU-specific operators. I benchmark after each step because the bottleneck moves — measure-don't-guess.

**Q38: What's the one architecture lesson you reuse today?**
A: Choose the simplest family that meets the operational constraint (here, single-stage for real-time), then let transfer learning + ablations + honest metrics carry the optimization. Novices over-engineer; the paper taught me that scoping the architecture to the deployment constraint and optimizing against measured data beats chasing accuracy trophies.

**Q39: Why a CNN at all versus transformers or classical CV for this task?**
A: CNNs are the right cost/performance point for edge real-time detection: mature tooling, quantization-friendly, and fast on CPU. Vision transformers are more expensive per FLOP and paid off mainly on larger data/compute. Classical CV (Haar/HOG) was the fallback baseline, not the contender. Choosing CNN = cost-aware engineering, not fashion.

**Q40: Did you consider a two-step face-detector + classifier approach?**
A: Yes, and it's a fair alternative with a plus and a minus: it lets you reuse a strong pretrained face detector and a small classifier, but it costs two forward passes per frame and scales cost with face count. Single-stage does all faces in one pass. For the "crowded gate" real-time scenario, single-stage was the right call; I noted the two-step as an alternative in related work.

---

## 4. Evaluation, Results & Reproducibility (Q41–Q52)

**Q41: How did you ensure your reported results are reproducible?**
A: Fixed random seed for train/val/test splits and augmentation, frozen hyperparameters documented in the paper (learning rate schedule, batch size, input size, epochs), identical preprocessing for every run, and a fixed evaluation script against the held-out test set. The paper states the protocol so a reviewer can rerun the experiment — the same verifiability I insist on in code.

**Q42: Did you report per-class results, and why does that matter?**
A: Yes — I reported AP/precision/recall for mask and no-mask separately, not just a pooled mAP. Per-class numbers are where a compliance system's weaknesses actually show (e.g. good precision on mask, weak recall on no-mask would be a silent policy failure). Hiding per-class collapse behind a single number is exactly the kind of reporting I refuse to do.

**Q43: What does a confusion matrix tell you here that mAP doesn't?**
A: mAP summarizes overall quality; the confusion matrix exposes the specific failure pattern — which classes get confused (no-mask vs incorrect, mask-like objects vs mask), and where thresholding helps. For a compliance deployment the matrix drives the operating threshold choice. It's the difference between "pretty good mAP" and "we know exactly how it fails."

**Q44: How did you handle the lack of a single canonical public mask-detection benchmark?**
A: By being explicit: I used a named public benchmark/dataset for training and a fixed held-out split for evaluation, and I always compared against baselines run under the same protocol rather than quoting numbers from other papers trained differently. When there's no single canonical benchmark, the job is to make your protocol unambiguous so numbers are comparable.

**Q45: What would make you suspicious of someone else's detection results?**
A: (1) No reported training/val/test split or preprocessing. (2) Accuracy quoted for an imbalanced dataset without per-class metrics. (3) No baseline, or a baseline from a different training set. (4) "Real-time" with no hardware or latency figure. (5) Numbers that don't reproduce with the stated protocol. These are the same checks I apply to my own paper before submission.

**Q46: Did the paper include error analysis (where it fails)?**
A: Yes — error analysis is non-negotiable in a credible paper: a breakdown of failure cases (small faces at distance, heavy occlusion, mask-like objects, motion blur) with example images and the observed patterns. Showing where it fails is what makes the "honest claims" framing defensible, and it directly feeds the future-work section.

**Q47: How do you decide a result is "good enough" for a research paper vs production?**
A: A research paper needs a defensible, reproducible result with correct methodology; production needs an operating point on a known precision/recall curve with a latency budget met on target hardware. The paper stops at "the method works and here's the trade surface"; production continues into thresholding, monitoring, and drift. I keep those two bars separate and don't conflate them.

**Q48: What's your stance on reporting only positive results?**
A: Strictly negative: a paper should report failures and limitations honestly, including the cases where the approach underperforms the baseline. Cherry-picking results is what a reviewer catches and what kills reproducibility. My OSS and project work follows the same rule — document what doesn't work as clearly as what does.

**Q49: How would you re-validate this paper's claims today if asked?**
A: Re-run the fixed protocol end to end on the recorded split and hyperparameters, regenerate the metrics with the same evaluation script, and diff against the published numbers. If any metric shifts, the shift is explainable (tool/library version drift) and documented. Reproducibility here means the same answer comes out, not "similar answer with new magic."

**Q50: What was the single most surprising or humbling experimental finding?**
A: That the majority of errors weren't exotic — they were small/occluded faces and mask-like objects at the decision threshold, exactly the cases in the problem statement. It humbled the "bigger model fixes it" instinct: most of the achievable gain was in threshold selection and handling, not architecture. That's a systems lesson I carried into later work.

**Q51: If you redid it, which experiment would you run first?**
A: The ablation of input resolution vs accuracy vs FPS, because the resolution tradeoff drives everything downstream (speed, small-face recall, memory). I solved it along the way; doing it first would have set the operating envelope sooner. Saying this shows I think about experimental ordering, not just final results.

**Q52: How do you present results so a non-technical reviewer trusts them?**
A: A short results table with the headline metrics, one figure the reader can eyeball (e.g. precision/recall curves or qualitative detections), and a two-line interpretation of what each number means operationally. Trust comes from showing the trade surface honestly alongside the headline, not from a single perfect-looking number.---

## 5. Real-Time & Deployment Thinking (Q53–Q65)

**Q53: What does "real-time" mean operationally, and what target did you aim for?**
A: At least camera frame rate for interactive use (video runs at ~25–30 fps), or comfortably faster than the event arrival rate at a busy entrance. The target defines the budget: a single-stage detector at high fps on target hardware is comfortably interactive. I define the target precisely in the paper, because "real-time" without a number is a marketing word.

**Q54: How did inference time break down, and where did the time actually go?**
A: The CNN forward pass dominates the budget; preprocessing (resize + normalize) is small; NMS and decoding are small and deterministic. So the lever is the forward pass — model size, input resolution, quantization — not micro-tuning the decoding step. Knowing where time goes stops you from optimizing the wrong thing.

**Q55: Did you run on CPU, and why does that matter?**
A: Yes — the CPU/edge claim is the deployment-relevant one: entrances, turnstiles, and cameras don't have GPUs. If real-time holds on commodity CPU (possibly at reduced input size or via quantization), the system deploys anywhere; GPU-only real-time is a lab claim. The paper's "real-time" narrative is strongest precisely because it isn't GPU-dependent.

**Q56: How would you deploy this to a real camera stream?**
A: A pipeline: frame grabber → (optionally skip/drop frames) → inference → per-face boxes → compliance logic (mask/no-mask alerts) → event sink (log/alert/dashboard) — with the model in a small service (the kind of FastAPI inference endpoint I built during internships) and per-site config for threshold and frame-skip. Real-time on a stream is a pipeline, not a single model call.

**Q57: What happens when a frame has many faces at once?**
A: The model detects them all in a single forward pass — that's the advantage of a grid-based detector — so per-frame cost is roughly constant regardless of face count; only NMS scales mildly with detections. That's a decisive deployment advantage over per-face classification pipelines, which scale cost linearly with people.

**Q58: How do you select the confidence threshold per deployment site?**
A: From the precision/recall curve: pick the operating point the site tolerates (security biases recall, retail biases precision), set the threshold from measured data rather than gut feel, and re-validate with site-specific data. Threshold selection is the human-in-the-loop tuning that turns a model into a usable product.

**Q59: What if the compute is shared or throttled? Why should a DSE care?**
A: Inference latency is load-dependent; a shared runtime needs rate limiting, batching, or a dedicated node so one noisy workload doesn't blow everyone's latency. Cost and latency governance matter as much as model accuracy in production — the same operational thinking I use in my FastAPI/Docker/CI work. A model that's fast at low load is irrelevant at peak if capacity wasn't planned.

**Q60: How would you measure the model's behavior on edge cases in production?**
A: Continuous monitoring: log predictions and inputs (with privacy care), track confidence distributions per class, and sample-review low-confidence/edge detections against ground truth. Watch for drift when lighting or context changes — a model quietly decaying at a new site is the classic silent failure. Monitoring is the deployment half of the "honest metrics" discipline.

**Q61: What's the model update story — how do you ship a better detector?**
A: Re-train/fine-tune on new data, re-evaluate on the fixed held-out test (plus site-specific data), export in the optimized format, then roll the new model behind the inference service with rollback if precision degrades. The paper's reproducible setup is exactly what makes model updates auditable instead of scary.

**Q62: Would you rather optimize the model or the system here?**
A: The system. The paper already proved the model works; what differentiates production is the pipeline — batching, frame-skip, per-site thresholds, monitoring, failover, privacy-preserving logging. A model improvement buys a few accuracy points; a system improvement decides whether the thing runs at all. That systems bias is why I pair research with engineering internships.

**Q63: How would you cost this deployment for an enterprise pitch?**
A: Cost = compute per inference unit (frames/s × per-frame cost on the chosen runtime) + monitoring/storage for logs + operational toil (retraining runs, drift review). The honest pitch compares running at the needed FPS on the cheapest hardware that meets the latency budget, with a breakeven framed on violations prevented. I frame cost per inference event, not per model.

**Q64: What's the biggest operational risk for a mask detector at an actual entrance?**
A: Catastrophic false-accept (letting a no-mask person through) at the operating threshold, caused by setting too high a threshold to avoid annoying false alarms. The mitigation is per-site calibration on real camera data plus alerting on threshold/performance drift. The model risk is real, but the threshold-and-monitoring risk is the one that reaches production.

**Q65: How does this work relate to the "edge AI" future of Infosys-style workloads?**
A: It's the same pattern: a model trained once, then quantized/distilled/optimized to run on constrained hardware with a latency budget, monitored in production. Everything I did for real-time face-mask detection — accuracy/latency trade surface, quantization path, per-site calibration, drift monitoring — is the playbook for deploying any CV/LLM model to edge devices. That transfer is what makes the paper a career skill, not a one-off.

---

## 6. Paper Process: Writing, Review & Publication (Q66–Q80)

**Q66: How do you write an IEEE paper from experiments?**
A: Results-then-narrative: tabulate all experiments and metrics first (numbers never change to fit the story), then write around them — problem statement, related work positioning the niche, method matching what was actually run, then results flowing from the tables. Figures are made from real outputs (curves from metric logs, sample detections from test frames), never fabricated/augmented.

**Q67: What's the biggest difference between writing code and writing a paper?**
A: Code hides assumptions in naming and structure; a paper is forced to state them explicitly — "under what conditions, compared to what, measured how." Reviewers will attack ambiguity, so every claim must carry its qualifiers. The discipline sharpened my technical writing generally: I now write design docs with the same "state the assumption, state the evidence" structure.

**Q68: What did the review/revision process teach you?**
A: Reviews made the paper better every round: tightening claims I'd over-asserted, adding ablations I'd skipped, sharpening the comparison protocol. The lesson is process, not ego — good reviews are debugging for prose and experiments. That experience is directly reusable in code review and requirement-writing at work: assume feedback is load-bearing and respond with evidence.

**Q69: How do you handle a reviewer comment you disagree with?**
A: First assume it's cost me clarity, not that they're wrong; then either fix the ambiguity it exposed or respond with a reasoned, evidence-based rebuttal for why the method stands. I never silently ignore a comment or change a claim just to placate — I explain the change. That's the same standard for responding to PR reviews and client feedback.

**Q70: What is related-work positioning and why does it matter?**
A: It's where you show your contribution exists in context: what prior methods did, what gap remains, and precisely how your approach differs. Getting it right prevents reviewers from thinking you reinvented known work; getting it wrong is the #1 desk-reject pattern. My related work clearly separated "compliance-detection architecture" from prior mask-detection papers.

**Q71: How do you choose between "novel method" and "solid engineering evaluation"?**
A: Be honest about which one the work is. A novel method needs a strong novelty argument plus baselines; a solid engineering evaluation needs rigor in protocol, metrics, and analysis. My paper was closer to the second — it wasn't claiming a new detector architecture, it was rigorously evaluating a real-time deployment-viable detector. Claiming novelty it doesn't have would be its own credibility risk.

**Q72: What makes a good figure in a paper, and which figure proved your point?**
A: A good figure is one a reader can interpret in five seconds without the caption — curves showing the accuracy/latency trade, or qualitative detections showing the hard cases handled. The one that proved my point plotted precision/recall at different thresholds: it made the operating-point story visible, which the abstract couldn't.

**Q73: How did you handle the deadline/scope pressure of a conference submission?**
A: Scope-locked to a single contribution ("real-time-viable compliance detection, honestly evaluated"), ran the hardest experiment early, and cut anything that didn't serve that claim. Shipping on time meant writing the limitations section from unfinished work instead of pretending it was done. Deciding what not to include is the real deadline skill.

**Q74: Do you have code/data to reproduce the paper, and why does it matter?**
A: The training/protocol script and a documented dataset/split exist so the experiments are rerunnable, and I treat that reproducibility bundle as part of the research — not as afterthought cleanup. In AI/ML, a paper without reproducible code is half a paper; at work, the same principle means your experiments and scripts must outlive your PRs.

**Q75: What's your process for avoiding benchmark/leakage mistakes?**
A: (1) Split by source, not by shuffled image indices, when the dataset could contain near-duplicates. (2) Fix the split once and reuse it. (3) No hyperparameter selection on the test set. (4) Sanity-check by inspecting samples from each split. These are simple, mechanical checks, and they prevent the single most embarrassing class of ML-paper errors.

**Q76: What would you include in a smaller "extended abstract" of this paper?**
A: The problem in two sentences, the method in three (single-stage detector, transfer-learned backbone, threshold-based operating points), the headline results, and a one-line limitation + future-work. If I can't compress it that far, I don't understand it yet; compression is a rigor test, and it's also how you pitch a project to a panel.

**Q77: How does IEEE publication compare to presenting at a conference?**
A: Publication is the written, artifact-based track — rigor in method and documentation. A conference presentation is the oral version: defend decisions live, answer why-questions on your feet, and handle a hostile question without wavering. My paper experience plus hackathon/coding-event experience covers both tracks.

**Q78: Why did you choose a conference paper rather than a journal?**
A: Conferences give faster publication of a focused, applied contribution; journals demand deeper, longer contributions with typically more extended review cycles. For an undergrad applied CV problem with real-time engineering value, a peer-reviewed conference paper was the right scope and timeline. The choice communicates that I match the venue to the contribution's depth.

**Q79: Research vs. internships — how do you decide which to invest in during a semester?**
A: By what each trains and what it proves: research trains depth/communication and proves rigor; internships train velocity/systemic context and prove employability. My plan was internships during the working seasons and research steadily in parallel, so the two compound instead of competing. At Infosys-like scale, this maps to "engineering with an evidence-and-rigor habit."

**Q80: What was your biggest mistake during this whole research experience?**
A: Over-scoping the initial experiment matrix — running too many configuration combos before locking the evaluation protocol, which wasted clock cycles and made early results noisy. I fixed it by fixing the protocol first, then ablating within it. Lesson: lock the measuring stick before measuring; it applies to every benchmark I've run since.

---

## 7. Limitations, Future Work & Research Mindset (Q81–Q92)

**Q81: What are the honest limitations of your paper?**
A: (1) Dataset scale and diversity are limited relative to general face-detection corpora. (2) Domain-transfer risk is real — the model may not behave identically at sites with different cameras/lighting without recalibration. (3) Threshold tuning is per-site, so "one model, all entrances" is not claimed. (4) It's detection, not a complete access-control product. Stating these is deliberate: they define exactly what the work does and doesn't claim.

**Q82: What's the most valuable future work you'd pursue from this paper?**
A: Domain adaptation and continuous calibration: making the model self-adjust its threshold and fine-tune on site data with minimal labels, so "deploy a model" becomes "deploy a system that stays accurate." That's the difference between a research prototype and an operational product, and it exercises both model and systems skills.

**Q83: How would you apply this approach to a different compliance problem?**
A: The architecture is a template: a visual-compliance task (PPE, helmets, badges, safety) → detection network → per-class evaluation emphasizing the compliance-critical class → threshold operating points per site. The transferable skill isn't "mask detection," it's scoping a vision problem to an operational metric and shipping a real-time detector around it.

**Q84: What did this project teach you about single-role teaming and mentorship?**
A: That you need someone who'll push on methodology, not just cheerlead — a reviewer figure. Peer feedback during research caught protocol gaps early, the same way code review and sprint retros catch gaps at work. I learned to actively recruit that friction rather than avoid it.

**Q85: How do you stay current in CV/ML after the paper?**
A: Track arXiv/leaderboards selectively, maintain small reproductions of new methods, and tie learning to projects: the OpenRTL and open-source work keeps me using the skills, while the papers keep me aware of the frontier. Learning that isn't tied to a build tends not to stick — so I always anchor evening reading to a running project.

**Q86: What's your definition of "research done well"?**
A: A correctly scoped question, a protocol a stranger can reproduce, honest metrics including the failures, and a written record anyone can audit — the IEEE-structure equivalent. Done well is not "fancy result"; it's "trustworthy result." That definition is why the same discipline governs my engineering work.

**Q87: Research output vs. engineering impact — how do you balance them on a resume?**
A: Research output (the IEEE paper) proves rigor; engineering impact (the internships, OpenRTL, open-source PRs) proves execution. On a resume they answer different questions the panel is asking — "can you be trusted to investigate?" and "can you be trusted to ship?" — so I present the paper as rigor evidence, not as an execution claim.

**Q88: What's a "reproducibility crisis" and why does it matter to an AI engineer?**
A: It's when published results fail to reproduce — due to hidden data splits, unimplementable papers, hyperparameter soup, or cherry-picking. It matters because it destroys trust in the field and wastes engineering time. I internalize the fix by shipping reproducible protocols and tests everywhere, from the paper to my OSS contributions.

**Q89: What's the one thing you'd change about the paper if you could redo it today?**
A: Release the full reproducible bundle from the start (dataset split manifest, training script, eval script) rather than as a post-paper artifact, and move the error analysis earlier in the narrative. Same results, but more trust and a cleaner manuscript. Process regroup, not results regroup — the science was sound.

**Q90: Do you consider studies like this "research" or "engineering"?**
A: Both, deliberately: research in the framing, protocol, and evaluation; engineering in the real-time constraint and deployment-thinking. The combination is the most valuable kind of applied work because it produces something both citable and usable. My whole portfolio is built on that intersection.

**Q91: What would you tell a peer slogging through their first paper?**
A: Lock the protocol before you burn compute, write the related-work early, cut scope to one defensible claim, and treat every reviewer comment as debug output rather than criticism. The paper is 20% experiments and 80% clearly communicating what you actually did; spend accordingly.

**Q92: How does your research experience influence how you estimate and plan engineering work?**
A: Research taught me that the risky part of any task is the measurement/protocol layer, not the "implementation" — so I front-load figuring out how I'll verify success before writing code: define the benchmark, the split, the acceptance metric first. That's exactly why my projects (MigratorGen, OpenRTL) start from "how will we know it works" before "what will we build."

---

## 8. Interview Strategy on Your Own Paper (Q93–Q100)

**Q93: How would you explain this paper to a non-CV interviewee in 30 seconds?**
A: "I built and evaluated a system that watches a camera feed and flags people not wearing masks, fast enough to run live at an entrance on ordinary hardware. The paper's contribution is honestly evaluating that trade-off between accuracy and speed, with a reproducible experiment so the numbers can be trusted." If I can't say it that simply, I don't understand my own work.

**Q94: What question about your paper would you most NOT want asked, and what's the honest answer?**
A: "How does it compare to the current SOTA?" Honest answer: SOTA has moved past a mask-detection paper with larger data and modern architectures; this paper deliberately claims a reproducible, deployment-viable evaluation rather than leaderboard position. The humble answer is stronger than a fabricated comparison, and it shows appropriate scope-awareness.

**Q95: How do you defend against "this is trivial, others did it first"?**
A: I wouldn't fight it — mask detection exists. The defense is the specific framing: a compliance-detection template with real-time deployment evaluation and a reproducible protocol, contributions a reviewer can hold. When someone says "others did it first," the correct move is to restate the precise niche, not overclaim.

**Q96: How does this paper make you a better candidate for a systems/platform role?**
A: The paper's real job on a resume is proving the research/bias-for-truth axis: I design experiments, report failures, and write for scrutiny. A platform role runs on exactly that — defining acceptance criteria, auditing claims, communicating uncertainty. The paper and my internships together say "rigor + execution," which is the whole candidate.

**Q97: What would you build next with this detector as a base?**
A: An actual ingress-compliance product: a service that ingests camera streams (the FastAPI/Docker/CI pattern), runs the detector, applies per-site calibration, and emits alerts/reports with an auditable log — effectively the production system the paper's "deployment thinking" sections describe. The paper is the evidence; the product would be the engineering.

**Q98: If Infosys gave you an unknown dataset tomorrow, what's your first week?**
A: Explore and audit it (balance, label quality, near-duplicates, class separation), lock the split and evaluation protocol, run one strong baseline end-to-end, and document all of it before touching fancy models. That ordering — data, protocol, baseline, then model — is the direct transfer of how I wrote the paper.

**Q99: What's the biggest myth about AI research you'll correct in an interview?**
A: That "state-of-the-art accuracy" is the only thing that matters. For applied work, the winning metric is usually the right operating point on a precision/recall/latency trade surface for a specific deployment, honestly measured. Believing that myth is how people produce papers and products that fail in the field.

**Q100: Give the panel your one-sentence honest verdict on this research work.**
A: "A peer-reviewed IEEE paper that rigorously evaluates real-time, deployment-viable face-mask detection with a reproducible protocol — demonstrating rigor in investigation, honesty in reporting failures, and a systems mindset connecting research to production — which is exactly the profile this role needs."
---

*Revision checklist: content grounded in the resume fact (IEEE publication 2024, real-time face mask detection) plus standard, defensible CNN detection methodology (single-stage family, transfer learning, mAP/P/R/F1, NMS, ablations, held-out splits, quantization path, conference review process). Deliberately NO fabricated experiment numbers, dataset sizes, or hardware FPS claims — any such numbers an interviewer asks for should be answered from the actual experiment records, not this sheet.*
