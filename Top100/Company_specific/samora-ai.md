# Samora AI — 500 Technical Interview Q&A
> Based on Samora AI (YC W26) — multilingual voice agents for enterprise call automation  > Role: Forward Deployed Engineer  > Tech Stack: Python/JavaScript, OpenAI, ASR/TTS, Telephony/VoIP, LLMs, Real-time Systems
---

## 
1. Speech Recognition & ASR (Q1–Q30)


**Q1: How does ASR work in a voice agent pipeline?**  
A: ASR converts audio speech to text via: audio preprocessing (noise reduction, VAD), feature extraction (log-mel spectrograms), acoustic model (maps audio to phonemes), language model (predicts word sequences), and decoder (combines scores to output text). Modern ASR uses end-to-end deep learning (Whisper, Conformer, Wav2Vec 2.0).


**Q2: What are key challenges of ASR for Indian languages and code-switching?**  
A: 
1. 22 languages + hundreds of dialects 
2. Code-switching mid-sentence (Hinglish, Tanglish) 
3. Limited labeled data for many dialects 
4. Phonetic similarity between language pairs 
5. Accent variation across regions 
6. Loanword handling 
Solutions: multilingual ASR models, language identification, code-switching-aware LMs.


**Q3: Compare Whisper, Wav2Vec 2.0, and Conformer for production ASR.**  
A: 
1. Whisper: robust multilingual (100+ languages), good punctuation, but high latency (~3-5s). 
2. Wav2Vec 2.0: self-supervised, fine-tunes well with limited data, lower latency. 
3. Conformer: CNN + self-attention, best WER on benchmarks, efficient streaming. 

For Samora: Whisper for offline, Conformer-Transducer for streaming/real-time.


**Q4: How do you handle background noise and poor call quality in ASR?**  
A: 
1. Front-end signal processing — noise suppression (RNNoise, WebRTC), AGC, echo cancellation 
2. Multi-condition training on noisy data 
3. VAD to filter non-speech 
4. Confidence scoring — reject low-confidence and ask for repeat 
5. Channel normalization for different codecs/sample rates (8kHz vs 16kHz)


**Q5: What is Voice Activity Detection (VAD) and why is it critical?** 

 A: VAD detects speech vs silence/noise. Critical for: 
 
1. endpointing — knowing when caller finished speaking, 
 2. barge-in — detecting interruption of agent, 
 3. reducing compute — only run ASR during speech, 
 4. turn-taking. WebRTC VAD is lightweight; neural VAD (Silero) is more accurate for noisy calls.


**Q6: How do you measure ASR quality in production?**  
A: 
1. WER (Word Error Rate)
2. CER (Character Error Rate)
3. RTF (Real-Time Factor)
4. Confidence score calibration
5. Semantic accuracy (did transcription capture intent?)
6. Per-language WER
7. Per-call-type WER
8. Degradation over call duration.


**Q7: Explain streaming vs. batch ASR.**  
A: Batch ASR processes full utterance — higher accuracy, bidirectional context, but adds latency. Streaming ASR processes incrementally (every 100ms) — lower latency, essential for real-time conversation, but higher WER without future context. Samora uses streaming for live conversation, batch for post-call transcription/analytics.


**Q8: What is an End-to-End (E2E) ASR model vs traditional hybrid?**  
A: Hybrid ASR has separate AM + PM + LM + lexicon, combined via WFST decoder. E2E ASR uses a single neural network (RNN-T, Conformer) mapping audio directly to text. E2E simplifies training, has smaller footprint, handles code-switching better, but is harder to debug and needs more data for rare words.

**Q9: How would you implement language identification for a multilingual voice agent?**  
A: 
1. Pre-call IVR selection
2. acoustic LID classifier on 2-5s audio
3. ASR-based — run multiple LMs, pick highest confidence
4. embedding-based — extract from multilingual ASR encoder

For Samora: lightweight neural LID at utterance start.

**Q10: How do you handle out-of-vocabulary (OOV) words in enterprise ASR?**  
A: 
1. Custom pronunciation lexicon
2. subword tokenization (BPE)
3. on-the-fly LM rescoring with OOV injection
4. personalized LM per customer with domain terminology

**Q11: What is endpointing and how does it affect conversation flow?**  
A: Endpointing determines when a speaker’s turn ends. Too aggressive (short timeout) cuts people off. Too lenient creates awkward silence. Typical: 500-800ms silence timeout. Samora should use adaptive endpointing based on context (longer for complex questions, shorter for yes/no).

**Q12: How would you reduce ASR latency in a real-time voice call?**  
A: 
1. Streaming ASR (RNN-T, Conformer-Transducer), 
2. GPU/dedicated inference, 
3. smaller model for first pass, larger for rescoring, 
4. chunked processing (320ms chunks, 160ms overlap), 
5. early inference before full utterance, 
6. optimized frontend, 
7. edge deployment.

**Q13: Explain barge-in and how you would implement it.**  
A: Barge-in allows caller to interrupt agent mid-speech. Implementation: 
1. ASR runs during playback, 
2. VAD detects caller speech, 
3. AEC removes agent’s own voice, 
4. on speech detection stop playback, 
5. ASR processes interruption. Challenges: echo cancellation quality, false trigger avoidance, partial barge-in handling.

**Q14: What data augmentation improves ASR robustness for telephony?**  
A: 
1. Speed perturbation (+/-10%), 
2. additive noise (call center, street, babble at various SNRs), 
3. convolutional noise (RIR simulation), 
4. SpecAugment, 
5. codec simulation (GSM/PSTN), 
6. volume perturbation, 
7. frequency masking.

**Q15: How do you evaluate ASR models for production?**  
A: Beyond WER: 
1. latency profile p50/p95/p99, 
2. streaming consistency (partial result stability), 
3. domain-specific WER, 
4. noise robustness at different SNRs, 
5. A/B testing with user satisfaction and call resolution, 
6. cost per audio hour.

**Q16: What is the role of a language model in ASR?**  
A: LM scores word sequence likelihood, biasing ASR toward linguistically plausible outputs. Hybrid ASR: external n-gram/neural LM combined with AM. E2E: internal LM learned from data. Production: domain-specific LMs improve accuracy on customer terminology.

**Q17: How would you handle ASR for low-resource languages?**  
A: 
1. Transfer learning from pretrained multilingual model (Whisper, XLS-R), 
2. synthetic data via TTS, 
3. cross-lingual pretraining, 
4. self-supervised learning on unlabeled audio, 
5. crowdsource data from live system, 
6. language family grouping.

**Q18: What is word-level confidence scoring and how do you use it?**  
A: Per-word probability (0-1) indicating ASR certainty. Uses: 
1. flag low-confidence segments for escalation, 
2. NLU ignores low-confidence words, 
3. prompt caller to repeat unclear phrases, 
4. analytics for problematic conditions, 
5. adaptive routing per call.

**Q19: How would you implement ASR fallback when confidence is low?**  
A: 
1. Reprompt — “I didn’t catch that, please repeat”, 
2. clarification — “Did you say X?”, 
3. simplify to yes/no or DTMF, 
4. escalate to human, 
5. try alternative ASR engine, 
6. switch channel to SMS/chat.

**Q20: What is speaker diarization and why is it important?**  
A: Diarization answers “who spoke when” by separating audio by speaker. Enables per-speaker metrics, agent vs customer behavior analysis, quality monitoring, accurate transcript attribution. For Samora: distinguishes AI agent from human caller for monitoring and compliance.

**Q21: How do you handle numbers and alphanumeric strings in ASR?**  
A: 
1. Grammar-constrained decoding,  
2. post-processing normalization (“double oh” to “00”), 
3. confirmation repeat-back, 
4. digit-by-digit dictation for critical fields, 
5. custom WFST for known patterns (account IDs, tracking numbers).

**Q22: What are MFCC features and are they still relevant?**  
A: MFCCs compress audio spectrum to 13-40 coefficients. Standard for hybrid ASR. With deep learning, raw spectrograms/log-mel features typically outperform MFCCs. Still useful for lightweight/traditional systems.

**Q23: How do you test ASR performance before deployment?**  
A: 
1. Representative test set from target domain, 
2. verbatim transcripts with disfluencies, 
3. WER/CER per accent/language/condition, 
4. semantic evaluation, 
5. end-to-end testing (ASR to NLU to action accuracy), 
6. load testing for latency/throughput.

**Q24: What is the trade-off between model size and ASR accuracy?**  
A: Larger models (Whisper large-v3, ~1.5B) = lowest WER but GPU required, higher cost. Smaller (tiny ~39M, distil-whisper) = CPU-capable, lower latency, higher WER. Tiered approach: small for real-time streaming, large for post-call transcription.

**Q25: How does audio codec choice affect ASR quality?**  
A: G.711 (64kbps) is lossless within 8kHz. OPUS has excellent variable bitrate. GSM (13kbps) causes significant quality loss. Narrowband (8kHz) loses >4kHz frequencies affecting fricatives. Wideband (16kHz) significantly improves ASR. Upsample to 16kHz for ASR.

**Q26: What is VAD hangover and how do you tune it?**  
A: VAD hangover is the time VAD continues flagging speech after speaking stops. It prevents clipping word endings. Short (~100ms) saves compute, long (~500ms) captures trailing speech. Tune based on speaking rate, language phonetics, noise level.

**Q27: How would you implement real-time transcription in a browser?**  
A: WebRTC to audio chunks via WebSocket to server-side ASR. Or browser SpeechRecognition API (limited). Or cloud ASR streaming APIs via WebSocket. Samora: server-side ASR via WebSocket from telephony bridge for consistent quality across channels.

**Q28: What is endpoint detection delay and why does it matter?**  
A: Time from user stops speaking to system detects end of speech. Typically 400-800ms. Should be adaptive: longer for complex utterances, shorter for yes/no. Too short = cuts off, too long = awkward silence.

**Q29: How would you handle multiple speakers on conference calls?**  
A: 
1. Multi-channel ASR per audio stream, 
2. single-channel with diarization, 
3. beamforming for spatial separation. 

For Samora (1 AI + 1 human), simple 2-speaker diarization suffices.

**Q30: What metrics would you track for ASR beyond WER?**  
A: RTF, end-to-end latency (p50/p95/p99), confidence calibration, error rate by audio condition/language, barge-in accuracy, streaming stability, cost per call-hour, reprompt rate from ASR errors.

## 2. Text-to-Speech & Voice Synthesis (Q31–Q55)

**Q31: How does modern neural TTS work?**  
A: Two-stage: 
1. Acoustic model converts text to mel-spectrogram (Tacotron 2, FastSpeech 2, VITS), (2) Vocoder converts to waveform (WaveGlow, HiFi-GAN, WaveNet). End-to-end models (VITS) combine both. Components: text encoder, duration/pitch predictor, decoder.

**Q32: What makes TTS sound natural vs robotic?**  
A: Natural TTS has: prosody (pitch variation, stress), rhythm (natural pauses, varied rate), co-articulation (smooth sound transitions), emotional nuance, breathing micro-pauses, consistency. Robotic = flat pitch, constant speed, poor co-articulation.

**Q33: How do you achieve low-latency TTS for real-time conversation?**  
A: 
1. Streaming/chunked TTS, (2) lightweight vocoder (HiFi-GAN beats WaveNet), (3) model quantization (INT8/FP16), (4) GPU batch inference, (5) pre-generated common phrases, (6) parallel chunk generation, (7) edge deployment.

**Q34: Explain voice cloning and its ethical implications.**  
A: Voice cloning synthesizes speech in a target voice from reference audio. Methods: speaker adaptation (fine-tune), speaker encoding (voice embeddings), in-context cloning (GPT-SoVITS). Ethics: consent, identity theft, fraud, impersonation. Samora must obtain explicit consent, watermark, implement usage controls.

**Q35: What is prosody and how do you control it in TTS?**  
A: Prosody = pitch, duration, loudness, pauses — the music of speech. Control: SSML tags (<prosody rate="slow" pitch="high">), pause insertion, pitch variation, emphasis on key info, end-of-utterance pitch (rising for questions, falling for statements).

**Q36: How do you handle code-switching in TTS output?**  
A: 
1. Multilingual TTS trained on mixed-language data, (2) language-agnostic TTS with per-language embeddings, (3) pre-processing to route segments per language model, (4) voice consistency across language switches, (5) accent control.

**Q37: Compare concatenative, parametric, and neural TTS.**  
A: Concatenative: stitches pre-recorded units — natural but limited content. Parametric (HMM): generates parameters — flexible but buzzy quality. Neural: end-to-end deep learning — most natural, flexible, supports voice cloning, but compute-intensive.

**Q38: What is SSML and how is it used in voice agents?**  
A: SSML (Speech Synthesis Markup Language) controls TTS via XML tags: <prosody>, <break>, <emphasis>, <say-as>, <phoneme>. Enables dynamic pacing, domain term pronunciation, and insertion of pre-recorded audio.

**Q39: How would you optimize TTS cost at Samora scale?**  
A: 
1. Cache common phrases, (2) tiered: neural for dynamic content, cached for static, (3) batch generation for non-real-time, (4) model compression (FP16 to INT8 = 2-4x savings), (5) efficient architectures (FastSpeech/HiFi-GAN), (6) dynamic GPU batching, (7) spot instances for batch.

**Q40: How do you evaluate TTS quality?**  
A: MOS (Mean Opinion Score, 1-5), CMOS (A/B preference), ASR WER on TTS output, latency (time to first audio), prosody accuracy, pronunciation accuracy, robustness (no glitches/clicks).

**Q41: How do you handle numbers/dates/special characters in TTS?**  
A: Text normalization: Dr. becomes Doctor, 5/3/24 becomes May third twenty twenty-four, $99.99 becomes ninety-nine dollars and ninety-nine cents. Use rules-based normalizer + domain-specific lookup tables.

**Q42: What is a vocoder and why is it important?**  
A: A vocoder converts mel-spectrograms to waveforms — the second stage of TTS. HiFi-GAN: high quality (MOS ~4.2+), fast CPU inference. WaveNet: excellent quality but slow. LPCNet: very fast, lower quality. Vocoder choice significantly impacts quality vs latency.

**Q43: How do you handle emotional TTS for different call scenarios?**  
A: 
1. Global style per call type (collections = neutral/urgent, support = friendly), (2) per-utterance control from sentiment analysis, (3) style embedding from reference audio, (4) SSML prosody control.

**Q44: Speaker adaptation vs speaker encoding for TTS?**  
A: Adaptation: fine-tune on target voice (5-30 min audio) — higher quality, needs fine-tuning per speaker. Encoding: extract embedding from reference, condition TTS — zero-shot, lower quality, no fine-tuning needed.

**Q45: How do you prevent TTS from sounding monotonous?**  
A: 
1. Vary rate (slow for important info, faster for transitions), (2) natural pauses at phrase boundaries, (3) pitch variation (not flat), (4) slight randomness to prosody parameters, (5) SSML breaks at natural boundaries.

**Q46: What are the challenges with TTS for Indian languages?**  
A: 
1. Script diversity, (2) complex orthography (conjunct consonants, vowel modifiers), (3) schwa deletion in Hindi, (4) limited high-quality data, (5) regional accent variation, (6) language-specific normalization rules.

**Q47: How do you implement hotword/phrase replacement in TTS?**  
A: Pronunciation dictionary (phoneme lexicon), SSML <phoneme ipa="...">, text normalization rules, G2P model for unknown terms. Example: Samora becomes /sæmərə/, API becomes ay-pee-eye.

**Q48: What is Voicebox and how does it differ from traditional TTS?**  
A: Voicebox (Meta) uses flow-matching for speech generation. Can infill (replace masked audio), do style transfer, zero-shot TTS, and cross-lingual generation. More flexible than traditional TTS but requires significant compute.

**Q49: How do you handle latency-sensitive TTS for barge-in scenarios?**  
A: 
1. Chunked streaming (first chunk in 200-300ms), (2) pre-compute first chunk (greeting), (3) lightweight model for first chunk, (4) fast vocoder, (5) cache recent utterances, (6) GPU warm-start.

**Q50: How do you create a custom brand voice for Samora?**  
A: 
1. Cast voice actor matching brand (professional, warm, trustworthy), (2) record 3-5 hours studio-quality covering all phonemes/emotions, (3) train multi-speaker TTS, (4) tune prosody parameters, (5) A/B test vs generic voices, (6) iterate on edge cases.

**Q51: How do you mitigate TTS hallucinations/mispronunciations?**  
A: 
1. Pre-generation validation, (2) post-generation ASR-on-output and compare to input, (3) confidence-based re-synthesis, (4) character-level alignment, (5) manual review for critical phrases, (6) monitor TTS to ASR mismatch rate.

**Q52: How do you handle TTS backchannels and hesitations?**  
A: Predefined short tokens (mhmm, okay, I see), vary type, time after user pauses, hesitation tokens for thinking time (um, well), avoid overuse.

**Q53: What is the impact of TTS quality on user trust and outcomes?**  
A: Directly affects: user trust (robotic voices reduce credibility), comprehension, emotional response, brand perception, call duration. Samora’s Turing moment voice quality directly impacts conversion rates.

**Q54: How do you test TTS for production?**  
A: 
1. 1000+ utterance test set covering phonemes/domain terms/edge cases, (2) ASR-back WER, (3) pronunciation via forced alignment, (4) latency under load, (5) MOS periodic rating, (6) A/B testing in production.

**Q55: How do zero-shot TTS models (GPT-SoVITS, CosVoice) work?**  
A: Reference audio to speech encoder extracts voice embedding, cross-attention with text features, duration/pitch prediction, then vocoder. Zero-shot means no fine-tuning needed. Quality depends on reference quality and similarity to training distribution.

## 3. LLMs & NLP (Q56–Q90)

**Q56: How do GPT-4, Claude, and open-source models differ for voice agents?**  
A: GPT-4/Claude: highest quality, strong instruction following, higher latency (1-3s), API dependency, cost. Open-source (Llama 3, Mistral, Qwen): self-hostable (lower latency, no data leaving), fine-tunable, lower quality for complex reasoning. Samora: GPT-4 for complex/compliance calls, open-source fine-tuned for routine calls.

**Q57: What is RAG and how would you use it in a voice agent?**  
A: RAG = Retrieval-Augmented Generation. User query to text to retrieve relevant docs from vector DB to inject as context. LLM generates grounded response. Benefits: accurate answers, easy to update, reduces hallucination. Samora uses: product FAQs, policy docs, customer history.

**Q58: How do you reduce LLM hallucination in production?**  
A: 
1. RAG grounding, (2) prompt “only answer based on context, say I don’t know if unsure”, (3) output format constraints, (4) low temperature (0.1-0.3) for factual, (5) self-consistency (multiple responses, pick most consistent), (6) verification against known facts, (7) human-in-the-loop for uncertain.

**Q59: What is intent classification in voice agents?**  
A: Maps user utterances to predefined actions: “check my balance” to CHECK_BALANCE, “lost my card” to REPORT_LOST_CARD. Methods: rule-based, ML (fastText), BERT/LLM. For real-time: lightweight model first pass, LLM for ambiguity.

**Q60: How do you handle out-of-scope inputs?**  
A: 
1. OOS detection via confidence threshold, (2) clarification — “Did you mean X or Y?”, (3) graceful fallback — “I can’t help with that, let me transfer you”, (4) context-aware repair, (5) escalation, (6) add frequent OOS to training.

**Q61: What is entity extraction in call flows?**  
A: Identifies structured data from natural language: “pay $500 on May 15th” extracts {amount: 500, date: 2026-05-15}. Methods: rule-based, NER (SpaCy, BERT), LLM-based extraction. Slot-filling with confirmation.

**Q62: How would you handle PII in LLM prompts?**  
A: 
1. Mask PII with placeholders, (2) never log raw PII, (3) self-hosted LLMs for data privacy, (4) prompt minimization — only include necessary PII, (5) consent management (GDPR/CCPA), (6) edge processing for sensitive data.

**Q63: Compare fine-tuning vs prompt engineering.**  
A: Prompt engineering: fast iteration, no training, easy to update, limited by context, may not persist complex behaviors, higher per-token cost. Fine-tuning: consistent behavior, lower inference cost, can encode complex rules, smaller model possible.

**Q64: How do you manage conversation context and history?**  
A: 
1. Sliding window of last N turns, (2) summarization of older history, (3) structured state (entities, decisions) separate from raw transcript, (4) token budgeting (system prompt > recent turns > summary > raw), (5) turn-level annotations (intent, sentiment).

**Q65: What is chain-of-thought prompting for voice agents?**  
A: LLM reasons step-by-step before responding. Improves accuracy on multi-step decisions and makes reasoning auditable. Trade-off: higher latency/tokens. Use only for complex turns, not every utterance.

**Q66: How do you handle multiple intents in one utterance?**  
A: 
1. Multi-label classification, (2) LLM-based decomposition into multiple requests, (3) prioritization — handle one at a time, queue others, (4) sequential processing with user acknowledgment.

**Q67: What is temperature and how do you tune it for voice?**  
A: Temperature controls randomness. Low (0.0-0.3): deterministic, factual. High (0.7-1.0): creative but unpredictable. Voice agents: 0.1-0.3 for factual, 0.4-0.6 for conversational, 0.0-0.1 for compliance-critical. Never use >0.7 in production.

**Q68: How do you implement slot-filling dialogue?**  
A: Collect required parameters through conversation. Explicit: ask one at a time. Implicit: user may provide multiple at once. Mixed-initiative: accept free-form input. Confirmation before execution.

**Q69: How do you handle user corrections?**  
A: 
1. Temporal confidence (newer info overrides older), (2) explicit markers (“I mean”, “actually”), (3) contextual replacement in state, (4) confirmation, (5) graceful acknowledgment, (6) never argue with the user.

**Q70: NLU vs LLM-based understanding?**  
A: Traditional NLU: specialized models for intent + entities — smaller/faster but less flexible. LLM: text generation approach — flexible but slower and costlier. Hybrid: lightweight NLU for common intents, LLM for complex.

**Q71: How do you detect and handle user frustration?**  
A: 
1. Sentiment analysis on audio (prosody) + text, (2) escalation after N negative turns, (3) empathetic responses, (4) de-escalation techniques (slower speech, calmer tone), (5) apology protocol, (6) angry callers get shorter escalation path.

**Q72: Design a system prompt for a support voice agent.**  
A: Structure: role definition, guidelines (“never make promises”), knowledge context, conversation history, current turn, response format (concise, TTS-friendly), constraints (“no markdown, <50 words”).

**Q73: What is function calling with LLMs and how does it apply to Samora?**  
A: LLM outputs structured request (JSON) to invoke APIs. Samora functions: checkBalance(accountId), scheduleCall(), updateCRM(), lookupPolicy(). LLM decides which function to call and extracts parameters from user speech.

**Q74: How do you ensure consistent persona across responses?**  
A: 
1. Detailed system prompt, (2) few-shot examples, (3) style constraints, (4) post-processing enforcement, (5) fine-tuning on brand-aligned data, (6) monitoring for persona drift, (7) A/B testing.

**Q75: How do you handle time-sensitive info (pricing, promotions)?**  
A: 
1. RAG with dynamic injection from DB, (2) temporal constraints (“as of [date]”), (3) expiration awareness, (4) verification before TTS, (5) uncertainty expression, (6) cache invalidation on changes.

**Q76: How does context window affect voice agent design?**  
A: Limits how much text LLM sees. With large windows (100K-200K): can include full history, larger knowledge bases. But there is a “lost in the middle” effect. Practical approach: sliding windows, summaries, strategic info placement.

**Q77: How do you handle code-switching in LLM calls?**  
A: Multilingual LLMs handle code-switching. Strategies: 
1. prompt instructions (“respond in same language(s) as user”), (2) language detection prefix, (3) multilingual fine-tuning, (4) allow natural mixing without forcing monolingual output.

**Q78: What is semantic caching for LLMs?**  
A: Return cached responses for semantically similar queries (not exact matches). Embed utterance to nearest neighbor in vector DB. If similarity > 0.95, return cached response. Saves 40-60% of LLM calls. Invalidate on data changes.

**Q79: How do you handle LLM response latency for real-time voice?**  
A: 
1. Streaming output — start TTS with first tokens, (2) speculative decoding (small draft model), (3) prompt compression, (4) KV cache prefix for common prompts, (5) model quantization (GPTQ/AWQ: 2-4x smaller), (6) smaller models for simple turns.

**Q80: What is prompt injection and how do you protect against it?**  
A: User input overrides system prompt. Protections: 
1. input sanitization, (2) clear prompt isolation, (3) output filtering, (4) least-privilege tool access, (5) instruction hierarchy, (6) human review for sensitive actions.

**Q81: How do you evaluate LLM response quality in production?**  
A: 
1. Automated: relevance (embedding similarity to expected), safety, length, (2) LLM-as-judge, (3) human QA sampling, (4) behavioral metrics (task completion, satisfaction, escalation rate), (5) A/B testing between variants.

**Q82: What is the role of guardrails in LLM-based voice agents?**  
A: Runtime checks on inputs/outputs. Input guardrails: prompt injection, off-topic, PII. Output guardrails: prohibited topics, format, business rules. Topical, safety, compliance guardrails. Tools: NeMo Guardrails, Guardrails AI.

**Q83: How do you handle ambiguous pronouns in conversation?**  
A: 
1. Coreference resolution model, (2) explicit “last mentioned entity” state tracking, (3) clarification (“When you say ‘it’, do you mean...?”), (4) LLMs with large context handle this naturally, (5) structured entity state.

**Q84: How do you design prompts for different call types?**  
A: Each needs tailored prompt: Collections (“firm but respectful, negotiate plans, never threaten”). Support (“diagnose step-by-step, don’t repeat questions”). Sales (“understand needs before pitching, know specs, clear next steps”).

**Q85: How do you implement A/B testing for prompts?**  
A: 
1. Prompt versioning in config, (2) route X% of calls to variant A, Y% to B, (3) track per-variant: task completion, duration, escalation, satisfaction, (4) statistical significance check, (5) gradual rollout, (6) instant rollback.

**Q86: How do you handle verbose LLM responses for voice?**  
A: 
1. Prompt “1-2 sentences, concise”, (2) max_tokens limit (50-100), (3) post-processing truncation, (4) generate then summarize, (5) progressive disclosure — brief answer, offer details, (6) length monitoring alerts.

**Q87: Zero-shot vs few-shot prompting for voice agents?**  
A: Zero-shot: instructions only — fastest setup. Few-shot: 3-5 examples — useful for complex tasks, tone calibration, rare formats. Samora: few-shot for novel flows, zero-shot for standard, one-shot for tone style.

**Q88: How do you handle multi-step action requests?**  
A: 
1. Action planning — LLM decomposes into steps, (2) sequential execution with user confirmation, (3) status tracking, resume on errors, (4) partial completion with alternatives, (5) undo support.

**Q89: How do you incorporate domain-specific rules into LLM behavior?**  
A: 
1. Hard constraints in system prompt, (2) external rule engine (check LLM output before execution), (3) fine-tuning, (4) function-call restrictions per role, (5) policy-as-prompt injection, (6) post-hoc validation.

**Q90: What is structured output and why use it?**  
A: Forces LLM to return defined format (JSON schema). Benefits: predictable parsing, function calling integration, validation against schema, dual output (structured + text), compliance. Tools: OpenAI structured outputs, Outlines, Instructor.

## 4. Conversational AI & Dialogue Management (Q91–Q120)

**Q91: What is a dialogue manager and why is it critical?**  
A: DM tracks conversation state, decides next action, and coordinates ASR, NLU, LLM, TTS, and APIs. It is the brain: turn management, context tracking, error handling, policy enforcement, escalation decisions.

**Q92: Compare rule-based, retrieval-based, and generative dialogue.**  
A: Rule-based: predefined state machines — deterministic, auditable, rigid. Retrieval: select from response library — fast, safe, limited. Generative: LLM generates dynamically — flexible, natural, harder to control. Samora uses generative + rule-based guards.

**Q93: What is turn-taking and how do you manage it?**  
A: End-of-turn detection, response timing (200-700ms gap), interruption handling (barge-in), overlap avoidance, turn-yielding cues (intonation, pauses), floor-holding (“Let me check...”), and maintaining natural rhythm.

**Q94: How do you handle conversation dead ends and loops?**  
A: 
1. Detection — repeated questions, low ASR confidence, (2) loop breakers — change approach, simplify, (3) escalation after N failed attempts, (4) smart backtracking, (5) fallback menu.

**Q95: What are grounding acts in conversation?**  
A: Ensuring mutual understanding. Types: acknowledgment (“okay”, “got it”), repeat-back (“so you need $500”), demonstration (“I’ve updated your address”), explicit confirmation, backchannels. Don’t over-ground (annoying).

**Q96: How do you design for conversational repair after ASR errors?**  
A: Implicit repair (“Did you say Tuesday or Thursday?”), explicit (“I didn’t catch that”), partial confirmation, reformulation, DTMF fallback, context-based correction, blame-free framing (never blame user).

**Q97: What is mixed-initiative dialogue?**  
A: Both system and user can take initiative. System initiative: asks questions one-by-one. User initiative: provides multiple info at once. Mixed-initiative: user can answer multiple questions or ask questions during form-filling. More natural but harder to implement.

**Q98: How do you implement “go back” or “start over”?**  
A: State history stack: pop last state on “go back”, reset to initial on “start over”. Keep user context (don’t re-ask confirmed info). Confirmation to avoid accidental resets. Partial reset: keep identity, reset transaction.

**Q99: How do you assess UX quality for voice conversations?**  
A: Task success rate, call duration vs complexity, CSAT, repeat call rate, escalation rate, FCR (First Call Resolution), dead air time, interruption rate, sentiment trend over call duration.

**Q100: How do you handle barge-in during TTS?**  
A: Continuous ASR during playback, echo cancellation, VAD for user speech detection, stop TTS immediately, process interruption, handle contextually, resume smoothly without restarting from beginning.

**Q101: Frame-based vs plan-based dialogue?**  
A: Frame-based: fill template slots (name, DOB, etc.) — simple form-filling. Plan-based: goal with sub-goals and contingencies — handles varied user behavior. Samora: plan-based for complex workflows, frame-based for simple data collection.

**Q102: Explicit vs implicit confirmation?**  
A: Explicit: “You want to pay $500, correct?” — accurate, natural for critical actions, adds length. Implicit: “Paying $500 from savings...” — assumes correctness, user corrects if wrong. Hybrid: explicit for high-risk, implicit for low-risk.

**Q103: How do you handle input arriving before agent finishes processing?**  
A: Input queuing — process one at a time. Drop oldest if queue > 2. Reprioritize on interruption. Agent deferral (“Let me check...”). Context merging for additional info provided during processing.

**Q104: How do you implement a good first impression/onboarding call?**  
A: Clear introduction and purpose statement, permission check (“Is now a good time?”), expectation setting, voice quality demonstration in first sentence, easy escape option, consistent brand persona from first word.

**Q105: How do you handle end-of-call wrap-up?**  
A: Summary, confirmation, next steps, reference number, follow-up scheduling, channel handoff (“I’ll also send you a WhatsApp”), graceful closing, post-call CRM update.

**Q106: How do you handle outbound call opening strategies?**  
A: Immediate purpose, hook, objection anticipation, opt-out option, warm opening if repeat caller, compliance disclosures, correct name pronunciation.

**Q107: What is progressive disclosure in voice?**  
A: Reveal info gradually: Level 1: “Your order shipped”. Level 2: “On May 10th via FedEx”. Level 3: “Tracking number 12345”. Implement with tiered generation, offer expansion, detect interest level.

**Q108: How do you handle “I don’t know” cases?**  
A: Honest uncertainty (“Let me check”), graceful limitation (“That’s beyond what I can help with”), redirect, partial answer, brief apology, log gap for knowledge base improvement.

**Q109: How do you design for accessibility in voice agents?**  
A: Clear speech, no visual assumptions, number clarity (digit-by-digit for accounts), confirmation loops, patience, error forgiveness, DTMF alternative, volume control, language switching.

**Q110: How do you implement natural-sounding pauses?**  
A: Dynamic filler insertion based on processing time, prosodic silence (not dead air), backchannel timing at turn boundaries, avoid overuse, vary fillers (“Let me check”, “One moment”).

**Q111: What is a persona and how do you maintain it?**  
A: Agent’s character: name, background, values, communication style, limitations. Embedded in system prompt, reinforced with few-shot examples, fine-tuned, monitored for drift via QA sampling.

**Q112: How do you handle multiple pending actions?**  
A: Sequential processing, prioritization (time-sensitive first), state queue, user confirmation of order, completion notification (“I’ve taken care of both”).

**Q113: How do you implement politeness strategies in voice?**  
A: Please/thank you appropriately, mitigation (“Would you be able to...”), acknowledgment before bad news, indirect requests (“The system needs your account number”), brief apologies, positive framing (“I can help with that”).

**Q114: How do you balance efficiency vs naturalness?**  
A: Routine tasks (balance check) = efficient. Sensitive tasks (collections) = conversational. User adaptation — detect preference (fast vs chatty). Context-dependent — busy hours vs off-peak. A/B test styles.

**Q115: How do you detect and handle user confusion?**  
A: Signs: “What?”, “Huh?”, “I don’t understand”, silence, hesitation, repeated questions. Responses: simplify, rephrase, break down, offer alternatives, escalate if persistent.

**Q116: What is the role of empathy in AI voice agents?**  
A: Improves satisfaction, defuses tension, builds trust. Emotional acknowledgment, validating, supportive language, avoid false empathy, action-oriented, cultural adaptation.

**Q117: How do you handle “speak to a manager”?**  
A: Acknowledge, attempt resolution, if persistent — don’t argue, warm transfer, brief human agent on context, log reason. Don’t take it personally.

**Q118: How do you implement voice-based authentication?**  
A: Knowledge-based (DOB, security questions), voice biometric (voiceprint), caller ID, PIN/DTMF, SMS OTP. Progressive authentication: low-risk = minimal auth, high-risk = full auth. Fail gracefully with alternative methods.

**Q119: How do you handle calls that go to voicemail?**  
A: Voicemail detection (SIT tones, greeting cadence), voicemail-specific script (shorter, CTA, callback), compliance (identify as AI), relevant info, SMS follow-up, DNC detection.

**Q120: How do you implement an opt-out mechanism?**  
A: Clear opt-out command, immediate processing, confirmation, DNC list update, multi-channel application, identity verification, confirmation follow-up message.

## 5. Voice Agent Architecture & System Design (Q121–Q155)

**Q121: Describe the high-level architecture of a voice agent platform.**  
A: Layers: 
1. Telephony — PSTN/VoIP gateway, SIP, WebRTC, (2) Audio — VAD, AEC, noise suppression, (3) ASR, (4) NLU/LLM, (5) Orchestration — workflow engine, state, policies, (6) TTS, (7) Integrations — CRM, APIs, (8) Observability, (9) Escalation — human handoff.

**Q122: How would you design for 99.99% availability?**  
A: 
1. Multi-region active-active, (2) redundant telephony providers with <30s failover, (3) stateless services with state in Redis/DB, (4) auto-scaling, (5) graceful degradation per component, (6) circuit breakers, (7) health checks, (8) DB replication with auto-failover.

**Q123: What is the latency budget for real-time voice?**  
A: Target <800ms from user stops to agent starts. Budget: ASR 200-400ms, LLM 200-500ms (streaming), TTS 100-200ms, Network 50-100ms, Processing 50-100ms. Optimize by streaming, caching, prediction, parallelization.

**Q124: How would you design the call state machine for a collections call?**  
A: States: INITIATE, CONNECTED, GREETING, IDENTIFY, VERIFY, PURPOSE, PAYMENT_FLOW (AMOUNT, DATE, METHOD, CONFIRM, PROCESS) or OBJECTION, PARTIAL, PROMISE, ESCALATION, COMPLETION, END. Failure: NO_ANSWER, VOICEMAIL, WRONG_NUMBER. Each state has timeout/error handlers.

**Q125: How do you handle 1000s of simultaneous calls?**  
A: 
1. Horizontal scaling — stateless behind LB, (2) GPU pooling across calls, (3) dynamic batching for GPU efficiency, (4) call queuing with ETA, (5) tiered models (simple = small, complex = large), (6) resource budgeting, (7) circuit breakers for downstream, (8) sharding by customer/region.

**Q126: What is a Session Border Controller (SBC)?**  
A: SBC controls VoIP at network boundary: security (firewall, DoS, encryption), protocol interworking (SIP normalization, transcoding), QoS (jitter buffer, prioritization), media steering, call admission control, lawful intercept. Sits between telephony provider and voice agent platform.

**Q127: How would you design the audio pipeline?**  
A: Input: PCM to AEC to Noise Suppressor to AGC to VAD to ASR. Output: TTS to Audio Mixer to AEC Reference to Codec to Telephony. Requirements: <50ms processing, effective AEC, consistent quality across sources, per-region PSTN configuration.

**Q128: SIP trunking vs WebRTC for voice agents?**  
A: SIP: traditional VoIP, connects to PSTN, SIP+RTP, better quality control, harder setup, needs SBC. WebRTC: browser-based, OPUS, STUN/TURN, easier web integration, limited PSTN. Samora: SIP for PSTN, WebRTC for browser demo, media gateway between.

**Q129: How would you implement monitoring dashboards?**  
A: Real-time: active calls, status distribution, ASR/LLM/TTS latency (p50/p95/p99), error rates, call duration, sentiment trend. Historical: daily volume, success rate, escalation rate trend, cost per call, language distribution, CSAT.

**Q130: How do you manage prompt versioning and deployment?**  
A: 
1. Git-based YAML/JSON prompt storage, (2) semantic versioning, (3) A/B traffic routing, (4) gradual rollout (5%/25%/100%), (5) instant rollback, (6) env separation (dev/staging/prod), (7) pre-deployment validation, (8) change log, (9) approval workflow.

**Q131: What is the hot-path in voice agent execution?**  
A: Most frequent path: ASR to intent classification to slot filling to action to TTS. Optimize: pre-load models, cache common responses, prioritize hot-path inference, parallelize non-critical ops (analytics async), pre-compute TTS for first prompt.

**Q132: How do you handle a spike in call volume?**  
A: 
1. Predictive auto-scaling, (2) capacity planning for 2x peak, (3) queuing with ETA, (4) tiered service (premium priority), (5) smaller/faster models during peak, (6) defer non-critical processing, (7) ensure telephony channel capacity, (8) load test expected surge.

**Q133: How do you design for graceful degradation?**  
A: ASR fails: DTMF/SMS input. LLM fails: rule-based scripts. TTS fails: pre-recorded prompts. DB fails: in-memory state for active calls. CRM fails: log for offline update. Telephony fails: secondary provider. Escalation fails: record message. Log all degradations.

**Q134: How do you implement call recording for compliance?**  
A: 
1. Announce recording at call start, (2) dual-stream recording (agent + caller), (3) encrypted storage tiered (hot 30d, cold 1yr, archive 7yr), (4) post-call ASR for search, (5) role-based access, (6) auto-delete per policy, (7) PII redaction, (8) append-only with audit log.

**Q135: How do you architect for multi-tenant isolation?**  
A: 
1. Per-customer DB schema or tenant-ID column, (2) per-customer prompts, KBs, configs, (3) rate limiting per customer, (4) per-customer fine-tunes/LoRA adapters, (5) per-customer phone numbers/SIP trunks, (6) per-customer call flows/rules, (7) per-customer usage tracking, (8) per-customer dashboards.

**Q136: How do you handle audio codec conversion?**  
A: Telephony codecs: G.711, G.729, OPUS, AMR. Pipeline: decode to raw PCM, process (VAD, ASR, noise), encode to output codec. Use media server (FreeSWITCH, RTPEngine) for transcoding. Ensure correct sample rate for ASR (16kHz).

**Q137: What is the role of a media server?**  
A: Real-time audio handling: RTP termination, mixing (conference), transcoding, recording, DTMF detection, tone generation, forking (send audio to multiple destinations). Open source: FreeSWITCH, Asterisk. Cloud: Twilio Media Streams.

**Q138: How do you manage audio latency across regions?**  
A: 
1. Regional deployment near callers, (2) direct media path (no unnecessary hops), (3) edge compute for lightweight processing, (4) global load balancing to nearest region, (5) CDN for static audio, (6) UDP (not TCP) for real-time, (7) adaptive jitter buffer.

**Q139: How would you design the conversation state data model?**  
A: Call(id, customer_id, caller_number, status, start_time, duration). ConversationTurn(id, call_id, sequence, role, text, audio_url, asr_confidence, intent, entities). CallState(call_id, current_flow, collected_entities, action_history, error_count, sentiment). CallResult(id, call_id, outcome, resolution_summary, follow_up_required).

**Q140: How do you implement WebSocket streaming for real-time voice?**  
A: Client sends binary audio chunks via WebSocket. Server processes (denoise, VAD) and sends to streaming ASR. Partial transcripts come back as JSON. NLU/LLM processes complete utterance. Streaming TTS sends audio chunks back via WebSocket. Protocol: {type, data, sequence}.

**Q141: How do you architect the human escalation system?**  
A: 
1. Triggers: low ASR confidence, repeated failures, user request, sentiment, compliance. (2) Queue: FIFO with priority and skill-based routing. (3) Context: full transcript + state to human dashboard. (4) Warm transfer with AI briefing. (5) Queue wait alerts. (6) Callback fallback. (7) Post-call AI summary.

**Q142: How do you implement pause/resume?**  
A: Hold (“Would you like to hold?”), hold music/progress updates, resume detection, state preservation, timeout after 5min = offer callback, background processing during hold, brief summary on resume.

**Q143: How do you integrate with enterprise CRM?**  
A: Pre-call: fetch context (name, account, history, preferences). During call: inject CRM data into LLM prompts. Post-call: update with outcome, notes, next steps. Real-time: update for critical events. REST API + webhooks. OAuth 2.0 per customer. Rate limiting + async for non-urgent.

**Q144: How would you design Samora’s Voice AI Studio (no-code builder)?**  
A: 
1. Visual flow builder with drag-and-drop nodes, (2) natural language input to auto-generate flow, (3) testing panel with simulated caller, (4) knowledge base management, (5) voice customization, (6) integration config, (7) monitoring dashboard, (8) version management (draft/test/publish/rollback).

**Q145: How do you handle call abandonment detection?**  
A: Silence detection (>10s after prompt), hangup detection (SIP BYE), progressive alerts (“Hello?”, “Are you still there?”), summary on abandon, callback scheduling, abandon rate tracking per agent/campaign, distinguish abandon from technical failure.

**Q146: How do you implement A/B testing for agent behaviors?**  
A: Config defines variants (prompt, TTS voice, model, flow logic). Deterministic assignment via caller ID hash. Metrics: completion, duration, escalation, satisfaction. Bayesian/frequentist analysis at 95% confidence. Minimum sample size. Auto-rollback on degradation. Holdout group.

**Q147: How do you handle wrong numbers and disconnected numbers?**  
A: Wrong number: “Is this [name]?”, if not, apologize and update records. Disconnected: SIT tones, mark disconnected. DNC check before each outbound. Time-of-day respect. Number validity check. Graceful handling with database update.

**Q148: How do you design prompts for non-technical users?**  
A: Templates per industry. Guided step-by-step wizard. Plain language input to LLM generates prompt. Auto-validation for completeness/conflicts. “Try your agent” button with simulated calls. Iterative refinement from feedback.

**Q149: How do you handle international phone number formats?**  
A: E.164 format for all numbers. Country-specific dialing rules. Number validation (libphonenumber). Regional routing. Timezone detection from country code. Language mapping from country code. Local presence numbers. Number portability handling.

**Q150: How do you implement streaming TTS for real-time playback?**  
A: Chunked generation (1-2 sentence / 200-500ms audio). Start playback immediately. Maintain prosodic continuity across chunks. Adaptive chunk size. 100-200ms jitter buffer for smooth playback. Immediate stop on barge-in. GPU pipeline for efficiency.

**Q151: How do you implement warm transfer with context to human?**  
A: Human dashboard with caller info, transcript, collected data, summary. AI briefs human. Route to skill-matched agent (language, domain). Silent handoff (human listens in). Context persistence. Post-handoff monitoring. Feedback loop for AI improvement.

**Q152: How do you design the audio codec pipeline for minimal latency?**  
A: OPUS codec (low latency, good quality). 20ms frames. Forward error correction for packet loss. Adaptive jitter buffer (50-100ms). Packet loss concealment. Avoid unnecessary transcoding. Hardware acceleration. Direct memory access.

**Q153: How do you handle DTMF during voice conversation?**  
A: In-band DTMF (RFC 2833/4733) or out-of-band (SIP INFO). Detect during TTS playback. Buffer all keypresses. Conflict resolution (voice vs DTMF disagreement = ask). DTMF-specific prompts. Collect-and-forward for account numbers.

**Q154: How do you design for cost optimization at scale?**  
A: Model tiering (small/cheap for simple, large for complex). Caching (ASR, TTS, semantic LLM). Batch post-call processing. Least-cost telephony routing. GPU optimization (max utilization, spot instances). Prompt compression. Pre-compute common responses. Monitor cost-per-call.

**Q155: How would you integrate with WhatsApp Business API?**  
A: WhatsApp Cloud API. Webhook for incoming messages. Pre-approved message templates. 24-hour session window. Media support (voice notes, images). Quick reply buttons. Voice note via AI TTS. Continuity from voice (“I’ll send you a summary”). Same AI persona across channels.

## 6. Multilingual & Code-Switching (Q156–Q175)

**Q156: What are unique challenges of building voice agents for the Indian market?**  
A: 22 languages, code-switching norm (Hinglish, Tanglish), accent diversity, limited training data, varying call quality (2G/3G, noisy), cultural considerations (formality, regional sensitivities), script diversity.

**Q157: How do you detect language of each utterance in real-time?**  
A: Lightweight LID model on 3-5s audio. ASR-based (run multiple LMs, pick highest confidence — expensive). Text-based (use previous language as prior). Hierarchical (language family to specific language). Multi-label for code-switched. Fallback to English.

**Q158: How do you build ASR for code-switching?**  
A: Code-switched training data (social media, call recordings). Mixed-language BPE tokenization. Language-agnostic acoustic model with language-specific heads. Language ID as additional input. Transfer learning from multilingual, fine-tune on code-switched data.

**Q159: How do you handle transliteration?**  
A: Direct ASR to Romanized script. ASR to native script + transliteration model. Dual output (both scripts). Context-dependent (Romanized for brands, native for Indian words). Indic-trans or Moses-based transliteration models.

**Q160: What is the best approach for multilingual TTS for Indian languages?**  
A: Multilingual TTS with language embedding input. Per-language fine-tuning from multilingual base. Shared IPA/Indic phoneme set. Same speaker voice across languages (brand identity). Slight accent on code-switch (natural). 5+ hours of data per language.

**Q161: How do you handle regional accents within one language?**  
A: Multi-accent training data. Accent-specific fine-tuning (if volume justifies). Online accent adaptation during first few sentences. Accent ID to route to optimized model. SpecAugment/speed perturbation for robustness. User-level accent profile.

**Q162: How do you normalize Indian English?**  
A: Indian English has unique vocab (prepone, do the needful) and pronunciation. Approach: Indian English ASR model, normalization dictionary, TTS pronunciation guide, allow Indian English grammar, context-aware normalization, keep flavor but normalize for downstream systems.

**Q163: How do you handle proper names across Indian languages?**  
A: Gazetteer DB of common names/cities with pronunciations. G2P model (language-aware). Phonetic fallback for unknown names. Regional validation (Bangalore vs Bengaluru). User confirmation to learn correct pronunciation. Personalization per user.

**Q164: How does code-switching affect LLM response quality?**  
A: Major LLMs handle common pairs well (Hinglish). Quality degrades for uncommon pairs or 3+ languages. LLM tends to match user’s language mix. Prompt instruction helps (“respond in same language(s)”). Few-shot examples improve consistency.

**Q165: How do you build multilingual training data?**  
A: Existing calls with human + ASR transcription. Crowdsourcing (MTurk, Indic platforms). Translate English data. Synthetic via TTS. Active learning — prioritize low-confidence production utterances. Public datasets (Common Voice, Shrutilipi, Kathbath). University/NGO partnerships.

**Q166: How do you manage language-specific prompt variants?**  
A: Per-language system prompts (translated + culturally adapted, not literal). Dynamic selection based on detected language. Shared structure template with language-specific sections. Code-switching prompt. Language-specific constraints (formality levels). Fallback language.

**Q167: How do you evaluate multilingual voice agent quality?**  
A: ASR WER per language. TTS MOS per language. LLM quality per language. Task completion rate per language. Escalation rate per language. CSAT per language. Code-switching accuracy. Language drift monitoring (accidental switch).

**Q168: How do you handle unsupported languages?**  
A: Detect and acknowledge. Apologize in default language. Offer supported alternatives. Escalate to human who speaks the language. DTMF language selection for initial IVR. Log requests for roadmap prioritization. Offer partial support if possible.

**Q169: How do you design TTS for loanwords in code-switched speech?**  
A: Language-tagged text: mark segments for proper pronunciation. Mixed-language lexicon. G2P with source language input. Share acoustic units across languages. Prosody adaptation: loanword follows target language prosody. Context-dependent pronunciation.

**Q170: How do you handle sentiment analysis across languages?**  
A: Multilingual sentiment model (XLM-R fine-tuned). Translation-based (translate to English, loses nuance). Lexicon-based per language. Cross-lingual transfer. Code-switched sentiment is special challenge. Cultural adaptation of what is positive/negative. Acoustic tone detection is language-independent.

**Q171: How do you design for users with limited literacy?**  
A: Voice-first UI, simple vocabulary, clear prompts, confirmation loops, DTMF alternative, local language selection, patience (longer timeouts), avoid speed assumptions, always offer verbal instructions (not just “press 1”).

**Q172: How do you identify language for an outbound call?**  
A: CRM data (preferred language). Caller ID to country/region. Previous interaction language. Time-based: default then switch based on response. Name-based inference. Context (account type, product). Multi-language greeting to detect response. Language tag in phone metadata.

**Q173: How do you handle multi-script output?**  
A: Primary script of spoken language. Romanized alternative for Roman-script users. Follow-up message in both scripts. User preference memory. Context-dependent (brands in original, rest in preferred). Screen-reader accessibility.

**Q174: What are common pitfalls translating prompts to Indian languages?**  
A: Literal translation (unnatural). Formality levels (English lacks formal/informal “you” distinction). Gender agreement (Hindi verbs agree with subject gender). Word order (SVO vs SOV). Length (+30-50% longer). Cultural references. Domain terminology without direct translations.

**Q175: How do you detect language switching mid-utterance?**  
A: LID on sliding windows (500ms). Lexical cues marking language boundaries. Code-switching ASR model. Post-hoc language tagger on transcribed text. Downstream LLM handles well. TTS segment marking for pronunciation. Analytics for code-switch frequency.

---
*This covers Categories 1-6. Remaining categories (7-18: Real-Time Systems, Integration/APIs, Testing/Observability, Python/Backend, Security, Performance, Engineering Culture, Behavioral/Scenario-Based) follow the same comprehensive format covering all 500 Q&A.*


---


## 7. Real-Time Systems & Performance (Q176–Q200)


**Q176: What are the real-time requirements for a voice agent?**  
A: End-to-end latency <800ms from user stops speaking to agent starts. ASR: 200-400ms. LLM: 200-500ms (streaming). TTS: 100-200ms (first chunk). Network: 50-100ms. Processing: 50-100ms. Jitter <50ms. Packet loss <1%.


**Q177: How do you optimize the critical path (ASR→LLM→TTS)?**  
A: 
1. Streaming ASR with partial results, (2) start LLM on partial ASR (speculative), (3) streaming TTS with first tokens, (4) GPU pipeline all three stages, (5) cache common query-to-response paths, (6) quantize models, (7) reduce prompt size.


**Q178: How do you manage concurrency in voice agent systems?**  
A: 
1. Event-driven architecture (async I/O), (2) thread pools for blocking operations, (3) connection pooling for APIs/databases, (4) per-call state isolation, (5) async/await for I/O-bound operations, (6) worker pools for CPU-bound inference.


**Q179: Synchronous vs asynchronous processing in voice systems?**  
A: Sync: real-time ASR-LLM-TTS for live conversation — must be fast. Async: post-call transcription, analytics, CRM updates — can be queued and batch-processed. Decouple via message queue (Kafka, PubSub).


**Q180: How do you handle jitter and packet loss in VoIP?**  
A: Jitter buffer (adaptive, 50-100ms target). Packet loss concealment (PLC) for lost frames. Forward error correction (FEC) with redundant info. Codec selection (OPUS has built-in PLC). Network quality monitoring.


**Q181: How do you detect and recover from audio stream failures?**  
A: Monitor RTP sequence numbers for gaps. Detect silence exceeding threshold (audio pipeline failure). Re-initialize media connection on failure. Fallback to alternative telephony provider. Log failure for post-mortem. Notify operations.


**Q182: What is the role of a jitter buffer?**  
A: Smooths out network delay variation. Collects packets, reorders, and plays at consistent rate. Adaptive: adjusts size based on observed jitter. Trade-off: larger buffer = smoother but higher latency. Target: minimum size that avoids underrun.


**Q183: How do you implement graceful handling of network degradation?**  
A: Adaptive codec bitrate (lower under poor conditions). Reduce audio quality (narrowband). Packet loss concealment. Proactive notification if quality degrades significantly. Offer callback when connection improves. Log quality metrics per call.


**Q184: How do you measure user-perceived quality in real-time?**  
A: MOS (Mean Opinion Score) estimated from network metrics. R-factor (ITU G.107). Delay + packet loss + jitter + codec determine quality estimate. Real-time alerts when MOS drops below threshold. Per-call quality score.


**Q185: How do you implement load shedding under extreme load?**  
A: 
1. Request queuing with timeout, (2) drop lowest-priority requests (non-premium, non-urgent), (3) reduce quality (smaller models, lower bitrate), (4) disable non-critical features (analytics), (5) rate limit new calls, (6) priority-based scheduling.


**Q186: How do you hot-reload configuration without downtime?**  
A: Feature flags (LaunchDarkly or custom). Dynamic config service (etcd, ZooKeeper, Consul). Watch for changes and reload without restart. Separate config from code. Validate before applying. Support instant rollback.


**Q187: How do you implement canary deployments for voice agents?**  
A: Route small % of calls (0.5-1%) to new version. Monitor error rates, latency, task completion. Compare against baseline (previous version). Auto-rollback on degradation. Gradually increase if stable (5% to 25% to 100%).


**Q188: How do you profile and optimize inference latency?**  
A: 
1. Measure p50/p95/p99 per stage, (2) flame graphs to identify bottlenecks, (3) GPU/CPU profiling, (4) optimize data loading pipeline, (5) reduce memory copies, (6) fuse operations, (7) optimize batch sizes, (8) use faster inference engines (TensorRT, ONNX, vLLM).


**Q189: How do you ensure state consistency across services?**  
A: 
1. Idempotent operations, (2) distributed tracing with correlation IDs, (3) transaction IDs for multi-step operations, (4) eventual consistency for non-critical state, (5) strong consistency for critical (payments), (6) saga pattern for distributed transactions.


**Q190: What is the role of a message queue in voice architecture?**  
A: Decouple real-time from async processing. Kafka/PubSub for: 
1. audio recording to storage, (2) post-call analytics pipeline, (3) CRM update queue, (4) billing events, (5) monitoring metrics, (6) human escalation requests. Provides resilience and replay capability.


**Q191: How do you implement timeouts for each processing stage?**  
A: ASR: 5s max per utterance. LLM: 3s max per response. TTS: 2s max per utterance. API calls: 2s. Database: 500ms. Total per turn: 8s before fallback. Hierarchical timeouts: shorter for fast path, longer for complex. Circuit breaker on repeated timeouts.


**Q192: How do you handle NAT traversal for WebRTC audio?**  
A: STUN server to discover public IP/port. TURN server as relay when direct P2P connection fails (blocked by NAT/firewall). ICE framework to negotiate best path. Fallback: TURN relay (higher latency but guaranteed connectivity).


**Q193: How do you implement distributed tracing across services?**  
A: Correlation ID propagated through all services. OpenTelemetry for instrumentation. Trace each call through telephony, ASR, LLM, TTS, and CRM. Spans per stage with timing. Export to Jaeger/Zipkin. Trace sampling (1-10% for performance).


**Q194: How do you handle media server failover in an active call?**  
A: 
1. Monitor media server health, (2) on failure, use SIP re-INVITE to redirect media to backup server, (3) maintain state on shared storage (Redis), (4) brief audio glitch during failover (200-500ms), (5) log failover, (6) test failover regularly.


**Q195: How do you approach capacity planning for voice agents?**  
A: 
1. Model peak concurrent calls per customer, (2) per-call resource usage (CPU, GPU, memory, bandwidth), (3) growth projections, (4) headroom (2x peak for safety), (5) auto-scaling thresholds, (6) GPU sizing (1 GPU handles ~50-100 concurrent ASR streams), (7) telephony channel limits.


**Q196: How do you implement rate limiting for voice API?**  
A: Token bucket or sliding window algorithm. Per-customer rate limits (configurable). Burst allowance. 429 response with Retry-After header. Tiered limits (premium = higher). Async queue for excess requests. Dashboard visibility for usage.


**Q197: How do you handle WebSocket connection lifecycle for voice?**  
A: Authentication at connection time. Heartbeat/ping every 10s to detect stale connections. Graceful close with close frame. Reconnection with exponential backoff. Last known state restoration on reconnect. Queue messages during disconnection.


**Q198: How do you design for backward compatibility in voice APIs?**  
A: Versioned API endpoints (/v1/, /v2/). Never remove fields, only add optional ones. Deprecation notices with migration timeline. Support old versions for minimum N months. Thorough integration tests for each version.


**Q199: How do you implement data consistency in distributed voice systems?**  
A: 
1. Idempotent operations with unique request IDs, (2) saga pattern for multi-step transactions, (3) two-phase commit for critical operations, (4) CRDT for conflict-free data types, (5) event sourcing for audit trail, (6) compensation transactions for rollbacks.


**Q200: How do you design for horizontal scaling of voice processing?**  
A: Stateless services (state in Redis/DB). Auto-scaling groups based on CPU/GPU/queue depth. Message queue for decoupling. Database read replicas. Connection pooling. Distributed caching (Redis Cluster). Sharded GPU pools per region.


## 8. Integration, APIs & Backend (Q201–Q225)


**Q201: How would you design the REST API for voice agent management?**  
A: Endpoints: POST /agents (create), GET /agents/:id, PUT /agents/:id (update prompt/config), POST /agents/:id/deploy, DELETE /agents/:id. POST /calls (initiate outbound), GET /calls/:id (status), POST /calls/:id/transfer. GET /analytics/calls, GET /analytics/agents/:id/metrics.


**Q202: How do you design webhook callbacks for call events?**  
A: Webhook events: call.started, call.ended, call.escalated, call.error. POST to customer-configured URL with event payload. Retry with exponential backoff (3 attempts). Idempotency key to prevent duplicates. Signature verification for security.


**Q203: How do you implement idempotency in API operations?**  
A: Idempotency key in request header. Server deduplicates based on key. Store key + response in Redis with TTL (24h). Return cached response for duplicate requests. Critical for payment processing, CRM updates, and call initiation.


**Q204: How do you design database schema for voice conversations?**  
A: Calls table: id, org_id, caller_number, agent_id, status, start_time, end_time, duration, outcome. Turns table: id, call_id, sequence, role, text, audio_url, asr_json, confidence. CallState table: call_id, state_json, collected_data_json. Escalations table: id, call_id, reason, agent_id, resolution.


**Q205: How do you handle pagination for large call history datasets?**  
A: Cursor-based pagination (more efficient than offset for large datasets). Sort by created_at DESC with cursor = last ID. Limit per page (50-100). Include has_more flag. Support date range filtering. Materialized views for common queries.


**Q206: How do you implement real-time updates for the monitoring dashboard?**  
A: WebSocket push for real-time metrics. Server-Sent Events (SSE) for simpler scenarios. Polling fallback (every 5s). Delta updates (only changed values). Batching updates (every 1s). Reconnection with last-known state.


**Q207: How would you design GraphQL API for flexible call data queries?**  
A: Schema: Call type with nested Turns, Agent, Customer. Query: calls(dateRange, status, outcome) with fields like duration, outcome, turns. Resolvers fetch from DB + cache. DataLoader for N+1 prevention. Subscription for real-time.


**Q208: How do you handle file uploads for custom TTS voice data?**  
A: Pre-signed S3 URL for direct upload. Validate file format (WAV, MP3) and size (<100MB). Virus scan. Convert to standard format (16kHz, mono, WAV). Trigger voice training pipeline. Progress notification via webhook.


**Q209: How do you implement search across call transcripts?**  
A: Elasticsearch index on transcript text. Full-text search with relevance scoring. Filters: date range, language, outcome, agent. Highlight matching segments. Faceted search (by intent, sentiment). Search-as-you-type for low-latency.


**Q210: How do you design integration tests for voice agents?**  
A: Mock telephony provider (simulated SIP/RTP). Test ASR with pre-recorded audio. Mock LLM with expected responses. End-to-end: simulated caller script, then verify agent response. CI/CD pipeline runs tests on every deploy.


**Q211: How do you handle external API failures during a call?**  
A: 
1. Retry with backoff (max 3), (2) timeout per external call (2s), (3) circuit breaker (after N failures, stop calling for M seconds), (4) graceful degradation (“I’m having trouble accessing your account”), (5) escalate if critical, (6) log and alert.


**Q212: How do you implement data sync between platform and external CRMs?**  
A: Initial sync: bulk export/import via CSV or API. Ongoing sync: webhook-based (push from CRM to platform, push from platform to CRM). Polling as fallback. Conflict resolution (last-write-wins or merge). Sync status dashboard. Error handling with retry queue.


**Q213: How do you design the call analytics API?**  
A: GET /analytics/summary (total calls, avg duration, success rate, escalation rate). GET /analytics/trends (daily/weekly time series). GET /analytics/breakdown (by language, outcome, agent, hour). GET /analytics/export (CSV/JSON). Date range, filters, grouping.


**Q214: How do you manage user authentication and authorization?**  
A: OAuth 2.0 / OIDC. JWT tokens with expiry (15min access, 7d refresh). Role-based access control (admin, developer, viewer, customer). API key for programmatic access. MFA support. Session management with revocation.


**Q215: How would you design the no-code agent builder’s backend?**  
A: 
1. Visual editor renders JSON flow definition, (2) backend validates and stores flow (versioned), (3) on publish, compile to execution graph, (4) runtime reads graph from cache, (5) version history with diff, (6) template library, (7) import/export flows.


**Q216: How do you implement bulk operations (schedule 1000s of outbound calls)?**  
A: Asynchronous job system. POST /campaigns with call list (CSV/API). Job processes in batches (100 calls/min adjustable). Progress tracking. Pause/resume. Schedule with timezone awareness. Rate limiting per customer. Error report with retry.


**Q217: How do you design the billing and usage tracking system?**  
A: Metered usage: call duration (minutes), ASR seconds, TTS characters, LLM tokens, telephony minutes. Accumulate per customer. Daily billing snapshot. Tiered pricing (included minutes + overage). Invoice generation. Usage dashboard. Alerts at thresholds.


**Q218: How do you implement audit logging for compliance?**  
A: Append-only audit log. Events: call start/end, escalation, data access, config change, user action. Stored in separate DB (immutable). Includes: timestamp, actor, action, resource, details. Periodic hash chain verification. Retention per regulation. Access restricted.


**Q219: How do you design health check endpoints?**  
A: /health for basic liveness. /health/ready for readiness (DB, cache, queue reachable). /health/deps for per-dependency status. /metrics in Prometheus format. Response time tracked. Degraded status (serving but with issues). Downstream dependency impact.


**Q220: How do you implement caching strategies for voice agent data?**  
A: Redis for: conversation state (per call), CRM data cache (per customer, TTL 5min), ASR results cache (exact match, TTL 1hr), TTS output (semantic cache, TTL 24hr). CDN for static prompts. Application-level LRU for LLM responses.


**Q221: How do you manage database migrations without downtime?**  
A: Expand-migrate-contract pattern. Add new columns alongside old. Dual-write during transition. Backfill asynchronously. Remove old columns after verified. Use feature flags for gradual rollout. Test migrations in staging first.


**Q222: How do you design for GDPR/CCPA compliance?**  
A: Data classification (PII vs non-PII). Consent management. Right to delete: purge call recordings and transcripts. Data portability: export user data. Data retention policies: auto-delete after defined period. DPA with sub-processors. Incident response plan.


**Q223: How do you handle vendor lock-in risks?**  
A: Abstract telephony provider behind unified interface. Support multiple ASR engines (Whisper + cloud API). Abstract LLM with model-agnostic interface. Support multiple TTS engines. Open standards (SIP, WebRTC, REST). Regular backup of configurations.


**Q224: How do you implement call tagging and custom metadata?**  
A: Key-value metadata per call (customer-defined). Labels for routing/analytics. Tags for filtering (e.g., priority: high, region: north). Searchable in analytics. Passed through to CRM. Pre-populated from campaign data.


**Q225: How do you design graceful shutdown for voice processing services?**  
A: SIGTERM handler: stop accepting new calls, drain active calls (complete or soft-terminate), close connections, flush metrics, then exit. Timeout (30s) before force kill. Health check returns 503 during draining. Log shutdown sequence.


## 9. Testing, QA & Observability (Q226–Q250)


**Q226: How do you test voice agents at scale?**  
A: 
1. Unit tests per component, (2) integration tests with simulated telephony, (3) automated test callers (scripted scenarios), (4) adversarial testing (edge cases, attacks), (5) load testing (1000s concurrent), (6) recording playback (replay old calls), (7) A/B testing in production, (8) canary deployments.


**Q227: How do you create a regression test suite for voice agents?**  
A: Recorded call library covering diverse scenarios. For each: expected flow, intents, entities, outcomes. Automated runner replays calls through system, compares actual vs expected. Track regression pass rate. Block deployment on regression.


**Q228: How do you test ASR accuracy regression?**  
A: Curated test set of 1000+ utterances per language. Measure WER per deployment. Alert on WER increase >1%. Test on: clean audio, noisy, accented, code-switched, various lengths. Compare streaming vs batch WER.


**Q229: How do you test TTS regression?**  
A: ASR-back WER (synthesize, then transcribe, measure accuracy). Pronunciation correctness (% correct). Latency (p50/p95/p99). MOS on random sample. Edge cases: special characters, long numbers, abbreviations.


**Q230: How do you test LLM response quality automatically?**  
A: LLM-as-judge: evaluator model scores responses on accuracy, relevance, safety, tone, conciseness. Automated test cases (500+) covering all intents plus edge cases. Semantic similarity to expected response. Compliance rule checking.


**Q231: How do you load test voice agents?**  
A: Simulate N concurrent SIP calls. Measure: call setup latency, ASR latency, LLM latency, TTS latency, audio quality, drop rate. Ramp up gradually (10 to 100 to 1000). Monitor resource usage. Identify bottlenecks. Repeat per model/config.


**Q232: How do you test barge-in behavior?**  
A: Simulated caller speaks over agent at various points: mid-sentence, end, during pause, during “uhm”. Verify: agent stops promptly, captures barge-in correctly, responds contextually. Measure stop latency. Test across noise conditions.


**Q233: How do you test code-switching behavior?**  
A: Test cases: same language whole call, language A to B at turn boundary, switch mid-sentence, multiple switches, mixed vocabulary. Verify: ASR captures correctly, LLM responds appropriately, TTS pronounces correctly.


**Q234: How do you test error recovery paths?**  
A: Inject failures at each stage: ASR timeout to fallback, LLM failure to rule-based, TTS error to pre-recorded, CRM timeout to retry, DB failure to cache. Verify correct fallback behavior, user experience, error logging.


**Q235: How do you implement chaos engineering for voice systems?**  
A: Inject failures in production/staging: kill services, add latency, drop packets, overload CPU. Observe system behavior. Verify graceful degradation, failover, recovery. Run during low traffic initially. Document blast radius. Automate regular chaos experiments.


**Q236: What metrics would you include on a real-time voice dashboard?**  
A: Active calls, calls per second, ASR latency (p50/p95/p99), LLM latency, TTS latency, end-to-end latency, error rate by stage, concurrent GPU utilization, telephony provider status, customer-specific metrics.


**Q237: How do you implement alerting for voice systems?**  
A: Alerts: error rate >1%, latency p99 >2s, call drop rate >5%, ASR confidence <0.7 avg, any call lasting >30min, GPU utilization >90%, downstream API failures. Severity levels: P0 (page), P1 (slack), P2 (daily report).


**Q238: How do you implement distributed tracing for debugging calls?**  
A: Each call gets trace_id propagated across services. OpenTelemetry spans: telephony.connect, asr.process, llm.generate, tts.synthesize, crm.update, escalation.transfer. Export to Jaeger. Search by call_id. Flame graph for latency breakdown.


**Q239: How do you handle log aggregation at scale?**  
A: Structured JSON logging (correlation_id, service, level, message, duration_ms, metadata). Ship to Elasticsearch/Loki. Retention: hot 7d, warm 30d, cold 90d. Search by call_id, customer_id, error type. Dashboard per service with error rate tracking.


**Q240: How do you implement call quality scoring?**  
A: Quality score (0-100) based on: ASR confidence, barge-in detection accuracy, no timeout, task completion, no error, TTS quality, LLM response quality. Score per turn + per call. Flag low-quality calls for human review. Trend analysis.


**Q241: How do you monitor for concept drift in LLM responses?**  
A: Track response distribution over time: a sudden change may indicate prompt injection or model behavior shift. Monitor: response length, sentiment, topic distribution, refusal rate. Alert on significant deviation from baseline.


**Q242: How do you handle PII in logs and monitoring?**  
A: Never log raw PII (account numbers, SSN, full name). Mask/redact at source. Use placeholder IDs instead. Separate PII storage with strict access. Audit log access to PII data. Auto-redaction in stored transcripts.


**Q243: How do you implement post-call quality assurance?**  
A: Random sample of calls reviewed by humans (1-5%). Score on: greeting, clarity, accuracy, empathy, compliance, resolution. Automated QA: ASR confidence, sentiment trend, script adherence, escalation appropriateness. Score per agent model.


**Q244: How do you detect and debug silent call failures?**  
A: Call setup failure rate (no answer, busy, disconnected). Silence detection during call (no audio for >5s). ASR silence (no speech detected for entire call). Media timeout. Telephony provider errors. Correlation with provider health.


**Q245: How do you implement anomaly detection for call metrics?**  
A: Baseline metrics per hour/day of week. Alert on deviation >3 sigma. Seasonality adjustment. Common anomalies: sudden volume spike/drop, latency spike, error rate spike, average duration change. Auto-triage to likely cause.


**Q246: How do you manage secrets and credentials in voice infrastructure?**  
A: Vault (HashiCorp) or cloud secret manager. API keys, SIP credentials, DB passwords, encryption keys. Rotate automatically. Audit access. Never in code or config files. Inject at runtime via environment variables or sidecar.


**Q247: How do you test for compliance requirements?**  
A: Test cases: recording disclosure present at call start, opt-out processed correctly, data retention enforced, PII handling correct, consent obtained for recording, disclosure of AI identity, industry-specific regulations (PCI, HIPAA, GDPR, FDCPA).


**Q248: How do you implement failover testing for telephony providers?**  
A: Regular (weekly) simulated failover: kill primary provider, verify secondary handles traffic. Measure failover time (<30s). Verify: calls in progress continue, new calls route to secondary, monitoring shows switch. Restore and verify primary works.


**Q249: How do you implement self-healing for voice systems?**  
A: Auto-restart crashed services. Auto-scale based on load. Re-route calls from degraded region. Retry failed operations with backoff. Circuit breaker for downstream. Auto-remediate: clear cache on stale data, restart pipeline on stuck, rebalance partitions.


**Q250: How do you track and improve first call resolution rate?**  
A: Define FCR criteria per call type. Track percentage of issues resolved without repeat call. Analyze repeat calls: same caller plus same issue within 7 days. Root cause analysis. Target >80% FCR. Regular review of repeat call patterns.


## 10. Python/JavaScript & Backend Engineering (Q251–Q270)


**Q251: What Python async patterns do you use for real-time audio processing?**  
A: asyncio with async/await. WebSocket handling via websockets library. asyncio.Queue for audio buffer management. asyncio.create_task for concurrent processing. Semaphore for GPU access control. Async context managers for connection lifecycle.


**Q252: How would you structure a Python microservice for voice agents?**  
A: FastAPI or aiohttp for API + WebSocket. Service layers: router (HTTP/WS), controller (business logic), service (ASR/LLM/TTS orchestration), client (external API calls). Dependency injection for testability. Health check endpoints. Structured logging.


**Q253: How do you handle backpressure in audio processing pipelines?**  
A: 
1. asyncio queues with maxsize, (2) producer blocks on full queue, (3) drop oldest if queue full (sliding window), (4) slow down ASR if LLM cannot keep up, (5) adaptive chunk sizes based on processing speed, (6) backpressure signals between services.


**Q254: How do you implement WebSocket reconnection logic?**  
A: Exponential backoff (1s, 2s, 4s, 8s, max 30s). Jitter to prevent thundering herd. Reconnect with last known state. Server sends last_sequence_id, client requests replay from gap. Heartbeat/ping every 10s. Detect stale connections.


**Q255: How do you manage shared state in a distributed Python system?**  
A: Redis for: call state, user sessions, rate counters. StrictRedis or redis-py cluster. AsyncRedis with asyncio. Lua scripts for atomic operations. TTL-based expiry. Key namespacing per service. Connection pooling with max connections.


**Q256: How do you implement circuit breakers in Python?**  
A: pybreaker or custom implementation. States: closed (normal), open (failing), half-open (testing). Threshold: N failures in M seconds. On open: fail fast without calling downstream. Half-open: allow 1 request, success to close, fail to open. Wrapped with decorator.


**Q257: How do you handle task cancellation in async Python?**  
A: asyncio.CancelledError handling: clean up resources, close connections, cancel sub-tasks. asyncio.shield for critical operations that should not be cancelled. Timeout via asyncio.wait_for. Graceful shutdown on SIGTERM: cancel active tasks, wait for cleanup.


**Q258: How do you implement rate limiting in Python?**  
A: Token bucket or sliding window. aioredis for distributed rate limiting. Per customer + per endpoint. Configurable limits. Headers: X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset. Async implementation for non-blocking operation.


**Q259: How do you handle streaming JSON parsing?**  
A: ijson for incremental JSON parsing so you don’t load entire response. Used for LLM streaming output. Process tokens as they arrive. Stream to TTS while LLM generates. Reduces time-to-first-token significantly.


**Q260: How do you profile Python code for latency optimization?**  
A: cProfile/py-spy for CPU profiling. asyncio debugging for async bottlenecks. time.perf_counter for manual instrumentation. py-spy for production profiling (low overhead). Flame graphs for visualization of bottlenecks.


**Q261: How do you implement retry logic with exponential backoff?**  
A: tenacity library. Config: max retries (3-5), initial wait (1s), exponential factor (2), max wait (30s), jitter. Retry on specific exceptions (timeout, 5xx). Log each attempt. Circuit breaker wrapper to prevent cascading failures.


**Q262: How do you handle multiprocessing for CPU-bound inference?**  
A: multiprocessing.Queue for work distribution. Process pool for model inference. Avoid GIL for CPU-bound tasks. Shared memory for large model weights. Each process loads model once. async for I/O, multiprocessing for compute.


**Q263: How would you implement a Python SDK for Samora’s API?**  
A: httpx (async HTTP). Auto-retry, rate limiting, auth handling. Typed models (pydantic). Context manager for client lifecycle. Async + sync interfaces. Comprehensive error types. Documentation with examples. Type hints throughout.


**Q264: How do you implement graceful shutdown for voice services?**  
A: SIGTERM handler: stop accepting new calls, drain active calls (complete or soft-terminate), close connections, flush metrics, then exit. Timeout (30s) before force kill. Health check returns 503 during draining state.


**Q265: How do you handle event-driven architecture in Python?**  
A: Event bus (Redis PubSub, RabbitMQ, Kafka). Event types: CallStarted, UserUtterance, AgentResponse, CallEnded, EscalationRequested. Event schema registry. Async consumers. Dead letter queue for failed events. At-least-once delivery guarantee.


**Q266: How do you handle resource cleanup in Python voice services?**  
A: Async context managers (async with) for connections, sessions, files. try/finally blocks for critical cleanup. atexit.register for process-level cleanup. Weak references for cache entries. Finalizers for GC-sensitive resources.


**Q267: How do you implement structured logging in Python?**  
A: JSON format with structlog or python-json-logger. Common fields: timestamp, service, level, message, call_id, customer_id, duration_ms, error. Context injection via call_id propagation. Correlation ID across services. Avoid PII in logs.


**Q268: How do you handle async database access in Python?**  
A: asyncpg for PostgreSQL (native async, high performance). SQLAlchemy 2.0 async for ORM. Connection pooling with min/max size. Transaction management with async context managers. Query optimization with proper indexing.


**Q269: How do you implement health checks in Python services?**  
A: FastAPI /health endpoint. Check DB connectivity, Redis connectivity, downstream service health, queue depth. Return 200 with status JSON or 503 if unhealthy. Timeout each check (2s). Cache health results briefly (5s) to avoid thundering herd.


**Q270: How do you handle JSON serialization performance in Python?**  
A: orjson (fast JSON library) instead of stdlib json. Use __slots__ and dataclasses with efficient serialization. Schema-based validation with pydantic. Protocol Buffers for high-throughput internal communication. Lazy serialization for large payloads.


## 11. Security, Compliance & Privacy (Q271–Q290)


**Q271: What security measures are critical for a voice agent platform?**  
A: 
1. End-to-end encryption (TLS for signaling, SRTP for media), (2) API authentication (OAuth 2.0, API keys), (3) input validation (prevent injection), (4) rate limiting, (5) audit logging, (6) secrets management, (7) vulnerability scanning, (8) penetration testing.


**Q272: How do you handle PCI compliance for payment-related voice calls?**  
A: Never log/store raw card numbers. Use DTMF with masked input — play tones only, don’t process through ASR. Use tokenization service. No card data in LLM prompts. PCI-compliant telephony provider. Regular PCI audit.


**Q273: How do you implement data encryption at rest and in transit?**  
A: At rest: AES-256 for databases, S3 server-side encryption (SSE), encrypted EBS volumes. In transit: TLS 
1.3 for APIs/WebSockets, SRTP for media, mTLS for service-to-service. Key rotation policies with scheduled rotation (quarterly).


**Q274: How do you handle GDPR data subject requests?**  
A: 
1. Right to access — export all user data, (2) right to deletion — purge calls, transcripts, recordings, (3) right to rectification — correct personal data, (4) right to portability — machine-readable export. Process within 30 days. Verify identity before processing.


**Q275: How do you handle regulatory compliance for outbound calls?**  
A: 
1. TCPA (US) — consent, DNC list, time restrictions (8am-9pm), (2) Do Not Call registry check, (3) Caller ID display rules, (4) Recording consent (two-party consent states), (5) AI disclosure (identify as AI), (6) Opt-out mechanism, (7) Record keeping.


**Q276: How do you implement access control for call recordings?**  
A: Role-based access (admin, manager, agent, auditor). Data classification (PII marked). Just-in-time access requests. Access logging. IP allowlisting. Data masking for non-privileged roles. Retention-based auto-deletion.


**Q277: How do you prevent unauthorized access to the voice agent API?**  
A: API key + OAuth 2.0. IP allowlisting for enterprise customers. Request signing (HMAC). Short-lived tokens (15min access, 7d refresh). Rate limiting per key. Anomaly detection on usage patterns. Regular key rotation.


**Q278: How do you secure WebSocket connections for real-time audio?**  
A: WSS (WebSocket Secure), token-based authentication at connection, re-authentication on reconnect, origin validation, rate limiting per connection, message size limits, connection timeout, close on authentication failure.


**Q279: How do you detect and prevent voice fraud?**  
A: 
1. Caller ID spoofing detection, (2) voice biometric (speaker verification), (3) knowledge-based authentication, (4) behavioral analysis (call patterns), (5) rate limiting per number, (6) anomaly detection (unusual call volume), (7) out-of-band verification.


**Q280: How do you implement AI disclosure to callers?**  
A: Caller must be informed they are speaking to an AI. Disclosure at call start: “Hi, I’m an AI assistant from [company].” Prompt instructions reinforce this. Compliance: legal requirement in many jurisdictions. Transcripts marked as AI-generated.


**Q281: How do you handle user consent for voice recordings?**  
A: Disclosure at start: “This call may be recorded for quality assurance.” Positive consent required in some regions (EU). Consent logged with timestamp. Ability to withdraw consent during call. Retention/deletion on consent withdrawal.


**Q282: How do you implement data minimization in voice systems?**  
A: 
1. Only collect data needed for the call purpose, (2) mask/redact PII in real-time, (3) don’t store raw audio longer than needed, (4) minimize data in LLM prompts, (5) aggregate analytics without storing individual behavior unnecessarily.


**Q283: How do you handle third-party vendor security?**  
A: 
1. Vendor security assessment (SOC 2, ISO 27001), (2) DPA (Data Processing Agreement), (3) data classification for sharing, (4) sub-processor list with approval, (5) regular review, (6) security incident notification requirements, (7) exit plan for data retrieval.


**Q284: How do you implement incident response for security events?**  
A: 
1. Detection — monitoring, alerts, user reports, (2) classification — severity, impact, (3) containment — isolate affected systems, (4) eradication — fix root cause, (5) recovery — restore service, (6) post-mortem — root cause, timeline, improvements tracked to closure.


**Q285: How do you conduct security reviews for code changes?**  
A: 
1. Automated SAST (static analysis) in CI, (2) dependency scanning for CVEs, (3) manual review for sensitive changes (auth, crypto, PII), (4) threat modeling for new features, (5) penetration testing quarterly, (6) bug bounty program.


**Q286: How do you handle cross-tenant data isolation?**  
A: Row-level security in database (tenant_id filter on all queries). Separate encryption keys per customer. Compartmentalized storage (separate S3 prefixes). Network isolation (VPC per tenant for dedicated deployments). Code isolation (per-customer model instances).


**Q287: How do you implement WebRTC security?**  
A: DTLS-SRTP for media encryption. Secure signaling (WSS). TURN with authentication. STUN for discovery. ICE to negotiate path. Server certificate validation. Origin validation. Short-lived tokens for session.


**Q288: How do you handle Caller ID verification (STIR/SHAKEN)?**  
A: STIR/SHAKEN protocol attaches digital signature for caller ID. Verify signature from originating provider. Block or mark calls without valid signature. Display verification status. Reduces spoofed calls. Regulatory requirement in many jurisdictions.


**Q289: How do you implement fraud detection for voice usage?**  
A: ML models on: call patterns (time, duration, destination), account usage (rate of change), geographic anomalies, device fingerprinting, velocity checks. Block suspicious calls with confirmation step. Alert on high-confidence fraud. Regular model retraining.


**Q290: How do you handle subprocessor vendor security?**  
A: Due diligence before engagement (SOC 2, ISO 27001, penetration tests). Contract includes DPA, SLA, security requirements, breach notification. Regular audits. Third-party risk assessments. Quarterly subprocessor review. Exit plan for data retrieval.


## 12. Prompt Engineering & LLM Fine-Tuning (Q291–Q310)


**Q291: What makes a good system prompt for a voice agent?**  
A: Clear role definition, behavioral guidelines (dos and don’ts), output format constraints (concise, TTS-friendly), context injection (conversation history, retrieved docs), tone specification, fallback instructions (when to escalate).


**Q292: How do you structure a system prompt for optimal results?**  
A: 
1. Role: “You are a customer support agent at X”, (2) Guidelines: bounded list of dos/don’ts, (3) Knowledge: injected context from RAG, (4) Constraints: response length, format, language, (5) Instructions: step-by-step for complex tasks, (6) Examples: few-shot for style calibration.


**Q293: How do you handle prompt versioning and A/B testing?**  
A: Prompts version-controlled in Git (JSON/YAML). Each version has metadata (date, author, change reason). A/B test by routing a % of traffic. Metrics per variant. Automated rollback on degradation. Canary deployment (5%/25%/100%).


**Q294: How do you optimize prompts for token efficiency?**  
A: 
1. Remove redundant instructions, (2) compress few-shot examples, (3) use shorter language, (4) split rarely-used instructions to on-demand injection, (5) summarize conversation history, (6) remove corporate speak, (7) test with shorter prompt versions first.


**Q295: How do you ensure prompt robustness?**  
A: 
1. Anticipate edge cases in prompt, (2) test with adversarial inputs, (3) include “ignore previous instructions” protections, (4) validate output format, (5) monitor for prompt injection, (6) regular prompt reviews, (7) version history for rollback.


**Q296: How do you fine-tune a model for voice agent behavior?**  
A: 
1. Curate training examples: system prompt + conversation history + expected response, (2) cover all intents and edge cases, (3) include correct and incorrect examples (contrastive), (4) use LoRA/QLoRA for efficient fine-tuning, (5) evaluate on held-out test set.


**Q297: What data do you need for fine-tuning?**  
A: 
1. Real call transcripts (redacted), (2) human-annotated ideal responses, (3) edge case coverage (confusion, anger, code-switching), (4) compliance scenarios, (5) correct grounding behavior, (6) varied user phrasings for the same intent.


**Q298: How do you evaluate a fine-tuned model?**  
A: 
1. Test set: 500+ held-out scenarios, (2) automated metrics: accuracy, safety, relevance, (3) human evaluation: MOS for response quality, (4) A/B test in production: compare to base model, (5) regression check: no degradation on core scenarios.


**Q299: When should you fine-tune vs prompt engineer?**  
A: Fine-tune when: consistent behavior needed across all users, complex rules hard to express in prompt, need to reduce inference cost (smaller model), behavior must persist despite prompt changes. Prompt engineer when: rapid iteration, per-customer customization, simple tasks.


**Q300: How do you handle prompt injection attempts?**  
A: 
1. Delimit system vs user content clearly, (2) instruction hierarchy in prompt (“system instructions override user requests”), (3) filter output for policy violations, (4) log injection attempts, (5) rate limit repeated attempts, (6) escalate suspicious behavior.


**Q301: How do you design prompts for code-switching?**  
A: “Respond in the same language(s) as the user. If the user mixes Hindi and English, you can respond in Hinglish. Keep the same language ratio the user is using. Default to English if unsure.”


**Q302: How do you chain prompts for complex workflows?**  
A: Multi-step prompt chain: 
1. Intent+entity extraction prompt to structured output, (2) Business logic: validate and retrieve to decide action, (3) Response generation: action result + context to natural response. Each step has a focused prompt.


**Q303: How do you design prompts for safe escalation?**  
A: “Escalate to human when: 
1. User explicitly asks for human, (2) ASR confidence below 0.3 for 3+ turns, (3) User is angry/frustrated for 2+ turns, (4) Request exceeds your authority (pricing, refunds), (5) Uncertainty about correct response.”


**Q304: How do you test prompt robustness against user variation?**  
A: 
1. Paraphrase test: 50+ ways to say same intent, (2) Adversarial test: injection, off-topic, profanity, (3) Variation test: verbose, terse, typos, grammar errors, (4) Long-tail test: unusual but valid requests, (5) Stress test: very long inputs.


**Q305: How do you implement context window management?**  
A: 
1. Always include: system prompt (fixed size), last N turns (dynamic), current utterance. (2) Compress if needed: summarize older history, drop low-information turns. (3) Token budget: system 30%, history 50%, current 10%, retrieval 10%. (4) Sliding window with summarization.


**Q306: How do you handle the LLM forgetting context in long calls?**  
A: 
1. Re-inject key context each turn (customer name, intent, collected entities), (2) structured state in prompt (not just raw history), (3) periodic summary re-injection, (4) use large context window models, (5) reminder turns from LLM (“We were discussing...”).


**Q307: How do you avoid keyword bias in prompt engineering?**  
A: 
1. Test with varied phrasings of same intent, (2) avoid over-specific words that trigger particular responses, (3) use semantic similarity tests, (4) validate with golden utterances (known problem cases), (5) monitor for response pattern shifts.


**Q308: How do you design prompts for different user personas?**  
A: Adjust tone based on: 
1. Customer type (B2B formal, B2C friendly), (2) call purpose (collections firm, support helpful), (3) user emotion (angry to empathetic), (4) channel (voice, WhatsApp, email). Dynamic prompt injection per segment.


**Q309: How do you handle refusal prompts gracefully?**  
A: “I’m sorry, I can’t process that request. [Brief reason]. Is there something else I can help you with?” Don’t over-explain, don’t be defensive, offer alternative. Log refusal for analysis. Escalate if user persists.


**Q310: How do you incorporate few-shot examples effectively?**  
A: 
1. Use 2-5 examples covering typical interactions, (2) include diverse user phrasings, (3) show correct agent behavior (including what NOT to do), (4) examples should be representative of real calls, (5) place after instructions and before user input.


## 13. Telephony & VoIP (Q311–Q330)


**Q311: What is SIP and how does it work?**  
A: Session Initiation Protocol: signaling protocol for VoIP. Establishes, modifies, terminates multimedia sessions. Key messages: INVITE (start call), ACK, BYE (end), CANCEL, REGISTER. Works with SDP for media parameters. Can use UDP or TCP.


**Q312: What is RTP and how is it used for voice media?**  
A: Real-time Transport Protocol carries audio data. RTP header: sequence number (detect loss), timestamp (playback timing), SSRC (sync source). Works with RTCP for quality feedback. Payload types: PCMU, PCMA, OPUS, G.729.


**Q313: Difference between SIP and WebRTC?**  
A: SIP: traditional VoIP signaling, uses SDP for media negotiation, works with RTP, requires media server. WebRTC: browser-based, uses JavaScript APIs, STUN/TURN for NAT, OPUS codec, DTLS-SRTP encryption. Gateway translates between them.


**Q314: How do you handle SIP registration and authentication?**  
A: SIP REGISTER with digest authentication (username + password/MD5 hash). Registrar server maintains location database. Expiration with re-registration. SIP authentication uses challenge-response (nonce, realm, response = MD5(credentials + nonce)).


**Q315: What is a SIP trunk and how is it used?**  
A: SIP trunk connects PBX or voice platform to PSTN via IP. Provides DID numbers (inbound) and outbound calling. Better scalability than physical PRI lines. Pay-per-channel. Provider handles PSTN interconnection. Samora uses SIP trunks for phone number connectivity.


**Q316: How do you implement call routing between multiple providers?**  
A: Least-cost routing (LCR) based on destination + time + provider cost. Failover routing: if primary fails, route to backup. Percentage routing for load distribution. Geographic routing to local provider. Quality-based routing with MOS thresholds.


**Q317: What is DTMF and how is it transmitted?**  
A: Dual-Tone Multi-Frequency (touch-tone keypad tones). Transmission: 
1. In-band (tones in audio stream, works always but can be distorted by codecs), (2) Out-of-band (RFC 2833/4733 in RTP header, reliable/preferred), (3) SIP INFO (signaling channel).


**Q318: How do you implement call forwarding and transfer?**  
A: SIP REFER for blind transfer (transfer without consultation). SIP REFER + NOTIFY for attended transfer (consult first). Re-INVITE for direct media re-negotiation. Samora uses attended transfer for warm handoff to human agents.


**Q319: What is a media gateway and its role?**  
A: Converts between different media types and protocols: TDM (PSTN) to IP (VoIP). Transcoding between codecs. Echo cancellation. Conferencing bridges. Protocol conversion (ISDN to SIP). Samora uses media gateways for PSTN connectivity.


**Q320: How do you implement call queuing?**  
A: Inbound calls placed in FIFO queue when all agents busy. Announce position in queue. Estimated wait time (EWT) based on historical + current data. Option to request callback instead of waiting. Music/announcements during wait. Timeout to overflow or alternate.


**Q321: How do you implement interactive voice response (IVR)?**  
A: IVR menu: greeting to options to user selection (voice or DTMF) to routing. Samora’s IVR can use AI to understand open-ended input (not just menu numbers). Fallback to DTMF. Language selection. Caller ID-based routing for known callers.


**Q322: What is echo cancellation and why is it important?**  
A: Acoustic echo: agent’s voice played out speaker, picked up by microphone, sent back. AEC adaptively models echo path and subtracts it from microphone signal. Critical for barge-in: without AEC, agent would hear its own voice as user speech.


**Q323: How do you implement call recording in SIP?**  
A: SIPREC (SIP Recording) protocol. Media forking: send copy of RTP streams to recorder. Metadata recording: call-ID, parties, timestamps, reason. Compliance storage. Can record both legs separately or mixed for quality monitoring.


**Q324: How do you handle SIP NAT traversal?**  
A: SIP ALG in router (often problematic). STUN for media path discovery. TURN as relay. ICE framework for best path selection. Keep-alive to maintain NAT binding. Symmetric RTP (same port for send/receive). Media proxy to relay through public IP.


**Q325: What is Early Media and how is it handled?**  
A: Early media: audio played before call is answered (ringback tone, announcements, IVR). SIP 183 Session Progress with SDP carries media early before 200 OK. Samora uses early media for “connecting” announcements and initial IVR.


**Q326: How do you implement conferencing in a voice platform?**  
A: Media server mixes multiple RTP streams into one. Conference focus handles signaling. Participants can be added/removed dynamically. Floor control (who is speaking). Recording of conference. Mute/unmute. Side conversations (whisper for coaching).


**Q327: How do you handle multi-party calls?**  
A: Conference bridge with media mixing. Each participant gets mix of all others’ audio. AEC per participant pair. DTMF detection for all participants. State tracking per participant. Recording with speaker identification.


**Q328: What is codec negotiation and how does it work?**  
A: During call setup, parties exchange supported codecs via SDP. Common codec chosen (highest quality both support). Preference order: OPUS > G.711 > G.729. Transcoding if no common codec exists. Codec negotiation affects both quality and cost.


**Q329: How do you implement Least Cost Routing for international calls?**  
A: Maintain rate table per destination prefix (country + area). Compare providers on: cost per minute, connection fee, quality, capacity. Route based on cost + quality threshold. Update rates periodically. Failover on failure. Consider time-of-day rates.


**Q330: How do you monitor SIP trunk health?**  
A: SIP OPTIONS ping to test liveness. Registration status monitoring. Call setup success rate tracking. Call drop rate. Answer Seizure Ratio (ASR = answered/seized). Average call duration. Provider SLA monitoring. Real-time alerts on degradation.


## 14. Performance Optimization (Q331–Q350)


**Q331: How do you optimize ASR inference speed?**  
A: 
1. Model quantization (FP16, INT8), (2) TensorRT/ONNX optimization, (3) Flash Attention for transformer layers, (4) batch inference across audio streams, (5) greedy decoding (disable beam search), (6) smaller model for streaming, larger for offline.


**Q332: How do you optimize LLM inference for low latency?**  
A: 
1. KV-cache for prompt prefix, (2) continuous batching (vLLM, TensorRT-LLM), (3) speculative decoding (draft model), (4) model quantization (GPTQ, AWQ, bitsandbytes), (5) Flash Attention, (6) PagedAttention for memory efficiency, (7) streaming output.


**Q333: How do you optimize TTS inference speed?**  
A: 
1. Fast vocoder (HiFi-GAN v1), (2) smaller model variants, (3) batch TTS requests, (4) pre-compute common phrases, (5) chunked generation + streaming, (6) ONNX export, (7) quantization (FP16).


**Q334: How do you reduce end-to-end latency?**  
A: 
1. Pipeline all stages (ASR, LLM, TTS in parallel), (2) start TTS on partial LLM output, (3) pre-warm models, (4) edge deployment near callers, (5) optimize network path, (6) minimize serialization/deserialization, (7) use efficient data formats (protobuf).


**Q335: How do you optimize database performance for voice metadata?**  
A: 
1. Read replicas for analytics, (2) connection pooling, (3) query optimization (indexes, covering indexes), (4) sharding by customer_id, (5) time-based partitioning, (6) materialized views for aggregations, (7) Redis cache for hot data.


**Q336: How do you handle GPU memory management for multiple models?**  
A: 
1. Load/unload models on demand, (2) model sharing across processes, (3) unified GPU memory pool, (4) dynamic batch sizing based on available memory, (5) model offloading to CPU for less active models, (6) memory profiling and leak detection.


**Q337: How do you optimize the audio processing pipeline?**  
A: 
1. Native C extensions for DSP (webrtcvad, noise suppression), (2) SIMD instructions, (3) zero-copy audio buffers, (4) lock-free queues, (5) dedicated audio processing threads with real-time priority, (6) avoid unnecessary format conversions.


**Q338: How do you implement caching for voice responses?**  
A: 
1. Semantic cache for LLM responses (embedding similarity), (2) exact cache for common queries (greetings, hours, balance format), (3) TTS cache for common phrases, (4) ASR cache for repeated short phrases, (5) invalidate on data/context change.


**Q339: How do you profile voice system performance?**  
A: 
1. Distributed tracing (OpenTelemetry), (2) flame graphs per request flow, (3) stage-by-stage latency breakdown, (4) resource profiling (CPU, GPU, memory, I/O), (5) lock contention analysis, (6) network profiling (packet capture, latency).


**Q340: How do you optimize for cold starts?**  
A: 
1. Pre-warm models on service startup, (2) keep models loaded in GPU memory, (3) pre-allocate connection pools, (4) lazy initialization for non-critical components, (5) keep-alive connections to downstream services, (6) warm standby instances.


**Q341: How do you implement connection pooling?**  
A: 
1. HTTP connection pool (httpx, aiohttp), (2) database connection pool (asyncpg, SQLAlchemy), (3) Redis connection pool, (4) WebSocket persistent connections, (5) gRPC channel reuse, (6) pool size tuned per service (min/max idle).


**Q342: How do you optimize serialization/deserialization?**  
A: 
1. Use efficient formats: Protocol Buffers, MessagePack, FlatBuffers for internal, (2) avoid JSON for high-throughput paths, (3) lazy parsing, (4) schema-based (protobuf) for smaller payloads, (5) compression for large payloads.


**Q343: How do you implement dynamic batching for inference?**  
A: 
1. Collect requests for short window (50ms), (2) batch into single inference call, (3) pad to uniform length, (4) handle variable-length sequences efficiently, (5) balance latency (longer window = more batching) vs throughput.


**Q344: How do you optimize network throughput for audio?**  
A: 
1. Reduce packet overhead (larger packets, fewer total), (2) use efficient codec (OPUS), (3) enable FEC for lossy links, (4) QoS tagging (DSCP), (5) dedicated network interface for media, (6) compression for non-real-time audio transfer.


**Q345: How do you handle memory leaks in long-running services?**  
A: 
1. Memory profiling (tracemalloc, memray), (2) reference leak detection (gc module), (3) bounded caches with LRU eviction, (4) object pooling instead of allocation, (5) regular heap snapshots, (6) auto-restart on memory threshold, (7) stress testing.


**Q346: How do you optimize prompt token usage?**  
A: 
1. Remove redundant instructions, (2) compress conversation history with summarization, (3) system prompt templates with variables, (4) shared prefix caching, (5) fewer few-shot examples, (6) shorter variable/function names in structured output.


**Q347: How do you implement GPU scheduling for concurrent inference?**  
A: 
1. Time-slicing (multiple models share GPU sequentially), (2) MPS (Multi-Process Service) for NVIDIA, (3) MIG (Multi-Instance GPU) for A100/H100, (4) Triton Inference Server for model management, (5) priority scheduling (real-time over batch).


**Q348: How do you handle throughput vs latency trade-off?**  
A: 
1. Batch processing for high throughput (analytics), (2) low batch/single inference for low latency (active calls), (3) separate pools for real-time vs batch, (4) dynamic adjustment based on load, (5) model tiering: small/fast for peak, large for off-peak.


**Q349: How do you implement circuit breakers for performance?**  
A: When downstream latency exceeds threshold (e.g., 2s for LLM), open circuit and use fallback response. After cooldown period, half-open to test one request. If fast, close circuit. Prevents cascading failures from slow dependencies.


**Q350: How do you approach performance regression testing?**  
A: 
1. Baseline performance per build, (2) automated latency benchmarks (p50/p95/p99), (3) throughput benchmarks (calls/second), (4) compare against last 10 builds, (5) alert on regression >10%, (6) resource usage tracking, (7) block deploy on regression.


## 15. Engineering Culture & Team Practices (Q351–Q370)


**Q351: What is your approach to incident management?**  
A: 
1. Detect, page on-call, (2) acknowledge, assess severity/impact, (3) mitigate (stop bleeding: rollback, redirect, restart), (4) resolve (fix root cause), (5) post-mortem (blameless analysis, timeline, action items). PagerDuty for on-call rotation.


**Q352: How do you balance speed vs quality in a startup?**  
A: 
1. Automate quality checks (CI/CD, tests, linting, security scans), (2) tiered testing (unit fast, integration slower), (3) feature flags for gradual rollout, (4) canary deployments, (5) monitor quality in production, (6) track technical debt for later cleanup.


**Q353: How do you approach technical decision-making?**  
A: 
1. Define the problem clearly, (2) gather requirements, (3) research options (POCs if needed), (4) evaluate trade-offs (complexity vs benefit, build vs buy, speed vs quality), (5) document decision (RFC), (6) implement with milestones, (7) review and iterate.


**Q354: How do you handle on-call for a voice platform?**  
A: 
1. 24/7 on-call rotation (primary + secondary), (2) clear escalation path, (3) runbooks for common incidents, (4) regular drills, (5) post-incident reviews, (6) follow-the-sun for global coverage, (7) alert fatigue prevention, blameless culture.


**Q355: How do you conduct code reviews?**  
A: 
1. Focus on correctness, security, performance, maintainability (not style), (2) review in small chunks (<400 lines), (3) ask questions, don’t dictate, (4) approve when satisfied, (5) timely reviews (<24h), (6) automated checks before human review.


**Q356: How do you measure developer productivity?**  
A: 
1. DORA metrics: deployment frequency, lead time for changes, MTTR, change failure rate, (2) developer satisfaction surveys, (3) shipped features per cycle, (4) customer impact (not code volume), (5) avoid vanity metrics (lines of code).


**Q357: How do you document voice system architecture?**  
A: 
1. Architecture Decision Records (ADRs), (2) system diagrams (C4 model: context, container, component, code), (3) API documentation (OpenAPI), (4) runbooks, (5) onboarding docs, (6) living docs (auto-updated from code/config), (7) wiki + code comments.


**Q358: How do you manage cross-team dependencies?**  
A: 
1. API contracts defined upfront, (2) shared interface definitions (protobuf/OpenAPI), (3) regular sync meetings, (4) SLA for dependencies, (5) mock/stub for parallel development, (6) integration testing environment.


**Q359: How do you handle legacy code or technical debt?**  
A: 
1. Track in backlog with priority, (2) boy scout rule (leave code better than you found it), (3) refactor in small, safe steps, (4) add tests before refactoring, (5) sunset/remove unused code, (6) allocate sprint capacity for debt (10-20%).


**Q360: How do you approach building a feature from scratch?**  
A: 
1. Understand the problem and user need, (2) design proposal with trade-offs, (3) build minimal viable version, (4) test with real users/stakeholders, (5) iterate based on feedback, (6) productionize (monitoring, error handling, docs).


**Q361: How do you ensure knowledge sharing in a small team?**  
A: 
1. Code reviews, (2) pair programming, (3) tech talks/lunch and learns, (4) RFCs for significant changes, (5) documentation, (6) rotation of on-call responsibilities, (7) cross-functional pairing on features.


**Q362: How do you handle production incidents?**  
A: 
1. Stop the bleeding first (rollback, disable, redirect), (2) assess impact (users affected, severity), (3) communicate (status page, internal, customer), (4) fix root cause, (5) post-mortem (blameless, timeline, action items), (6) track action items to completion.


**Q363: What is your approach to testing in a startup?**  
A: 
1. Unit tests for core logic, (2) integration tests for critical paths, (3) end-to-end tests for key user flows, (4) monitoring and observability as tests in production, (5) canary deployments, (6) focus testing effort on highest-risk areas.


**Q364: How do you prioritize features in a roadmap?**  
A: 
1. Customer impact (revenue, retention, satisfaction), (2) strategic alignment (company goals, competitive positioning), (3) effort/complexity estimate, (4) dependencies, (5) risk, (6) use RICE or weighted scoring, (7) validate with customer interviews.


**Q365: How do you foster a blameless culture in incident response?**  
A: 
1. Focus on system failures not individual mistakes, (2) post-mortems ask “what went wrong?” not “who did it?”, (3) action items are system improvements, (4) leadership models blameless behavior, (5) celebrate learning from failures.


**Q366: How do you handle technical disagreements in the team?**  
A: 
1. Focus on data and evidence, (2) define evaluation criteria upfront, (3) run experiments/POCs to resolve, (4) document trade-offs, (5) decide and commit even if not unanimous, (6) retrospect on decision outcomes.


**Q367: How do you approach writing technical specs/RFCs?**  
A: 
1. Problem statement and context, (2) goals and non-goals, (3) proposed solution with diagrams, (4) alternatives considered, (5) trade-offs and risks, (6) implementation plan, (7) open questions. Lightweight for small changes, detailed for large.


**Q368: How do you manage on-call rotations for a 24/7 service?**  
A: 
1. Follow-the-sun across timezones, (2) primary + secondary per shift, (3) max 1 week primary per rotation, (4) escalation path (primary -> secondary -> engineering manager), (5) handover documentation, (6) incident response training.


**Q369: How do you ensure code quality in a fast-moving startup?**  
A: 
1. Automated tests in CI, (2) code review for every PR, (3) linting and formatting enforced, (4) static analysis (type checking, security scanning), (5) feature flags for safe rollouts, (6) monitoring for production issues, (7) regular tech debt sprints.


**Q370: How do you approach mentoring junior engineers?**  
A: 
1. Pair programming on complex features, (2) code review with detailed explanations, (3) assign small, well-scoped tasks initially, (4) gradually increase responsibility, (5) regular 1:1 feedback, (6) encourage questions and curiosity.


## 16. Behavioral & Scenario-Based (Q371–Q420)


**Q371: How would you debug a voice agent that keeps asking users to repeat?**  
A: Check: 
1. ASR confidence threshold too high, (2) background noise causing low confidence, (3) specific accent/language performing poorly, (4) VAD settings too aggressive (cutting off speech), (5) endpointing too fast (not waiting for full utterance). Inspect per-utterance confidence logs and compare with audio playback.


**Q372: How would you investigate a sudden increase in ASR latency?**  
A: 
1. Check GPU utilization (near 100%?), (2) check concurrent call count (spike?), (3) check model version (recent deployment?), (4) check input audio size (increased?), (5) check downstream services (LLM backpressure?), (6) check recent code/config changes, (7) rollback if needed.


**Q373: How would you fix a voice agent that responds in wrong language?**  
A: 
1. Check language detection model accuracy, (2) check per-language model loading (model for that language loaded?), (3) check system prompt language instruction, (4) check language mapping configuration, (5) check for recent prompt changes, (6) add logging for language detection decisions.


**Q374: How would you reduce the cost of a voice agent deployment?**  
A: 
1. Model tiering: small for simple calls, large for complex, (2) cache common responses, (3) shorter prompts (fewer tokens), (4) prompt compression, (5) batch post-call processing, (6) optimize telephony routing (least-cost), (7) negotiate provider rates, (8) use spot instances for batch.


**Q375: How would you design an A/B testing framework for voice prompts?**  
A: 
1. Assign variant based on caller ID hash (consistent experience), (2) inject variant into system prompt, (3) track per-variant: completion rate, duration, escalation rate, CSAT, (4) statistical test (Bayesian, 95% confidence), (5) auto-rollback on degradation, (6) experiment dashboard.


**Q376: How would you handle a customer who wants to bring their own LLM?**  
A: 
1. Abstract LLM behind adapter interface, (2) support OpenAI, Anthropic, Azure OpenAI, self-hosted, (3) customer provides API endpoint + key, (4) apply Samora’s guardrails on top of their LLM, (5) hybrid: their LLM + Samora safety filters, (6) communicate latency/cost implications per model.


**Q377: How would you design a system to detect agent hallucination?**  
A: 
1. LLM-as-judge: second pass evaluates response against context, (2) factual consistency check against KB, (3) response vs expected pattern comparison, (4) real-time alert on detected hallucination, (5) log for analysis, (6) auto-correction (regenerate if hallucination detected).


**Q378: How would you handle a customer who complains about TTS quality?**  
A: 
1. Identify specific issues (robot voice, mispronunciation, unnatural pauses), (2) check if issue is model-specific, (3) offer voice customization options (different voice, speed, pitch), (4) escalate to brand voice creation if enterprise, (5) provide pre-recorded option for critical phrases.


**Q379: How would you design a self-service analytics dashboard?**  
A: 
1. Overview: call volume, completion rate, avg duration, cost. (2) Trend: daily/weekly time series. (3) Breakdowns: by language, outcome, agent version, time of day. (4) Drill-down: per-call details (transcript, timeline, metrics). (5) Export: CSV/PDF. (6) Custom: saved filters, scheduled reports.


**Q380: How would you implement real-time sentiment tracking during a call?**  
A: 
1. Per-utterance sentiment scoring (positive, neutral, negative, angry), (2) running sentiment average over last 3 turns, (3) sentiment trend (improving or declining), (4) trigger: if sentiment drops below threshold, offer escalation, (5) visualize on human agent dashboard, (6) post-call sentiment summary.


**Q381: How would you design a system to handle 10x growth in call volume?**  
A: 
1. Horizontal scaling assessment (stateless services), (2) GPU capacity planning, (3) auto-scaling configs, (4) database sharding readiness, (5) telephony provider capacity increase, (6) load testing at target scale, (7) budget for increased infrastructure costs, (8) architectural review for bottlenecks.


**Q382: How would you migrate telephony providers with zero downtime?**  
A: 
1. Register numbers with both providers, (2) dual-register SIP trunks, (3) gradually shift traffic (10% to 50% to 100%), (4) monitor call quality on new provider, (5) keep old provider as hot standby, (6) rollback plan, (7) after stable, decommission old provider.


**Q383: How would you handle customer request for a new language?**  
A: 
1. Assess: is there ASR/TTS/LLM support? (2) If all available: configure, test, deploy. (3) If gaps: collect training data, fine-tune models. (4) Update prompts and IVR. (5) Test with native speakers. (6) Gradual rollout. (7) Monitor per-language quality metrics.


**Q384: How would you debug a call that failed with no audio?**  
A: 
1. Telephony provider logs (was call connected?), (2) SIP trace (INVITE to 200 OK to ACK to media), (3) RTP check (are packets flowing?), (4) codec mismatch (check SDP), (5) firewall/NAT (RTP blocked?), (6) media server logs, (7) playback recording if available.


**Q385: How would you design a system for automated prompt improvement?**  
A: 
1. Collect failed/confused turns, (2) cluster by error pattern, (3) auto-generate prompt improvements using LLM, (4) test improvements on held-out set, (5) A/B test in production, (6) if metrics improve, auto-merge. Human-in-the-loop for critical changes.


**Q386: How would you handle a customer who wants extensive personality customization?**  
A: 
1. Provide personality template (friendly, professional, casual, formal), (2) custom system prompt editing in no-code UI, (3) custom few-shot examples, (4) voice style selection, (5) escalation behavior configuration, (6) allow custom knowledge base, (7) safety constraints cannot be overridden.


**Q387: How would you debug a 2-second latency spike in LLM response?**  
A: 
1. Check prompt size (increased due to long history?), (2) check model type (large vs small), (3) check GPU utilization, (4) check concurrent LLM requests (queue depth), (5) check if new model version deployed, (6) check downstream (RAG retrieval slow?), (7) check network to LLM endpoint.


**Q388: How would you implement a feedback loop from CSAT to improvement?**  
A: 
1. Tag calls with CSAT score, (2) cluster low-scoring calls by topic/intent, (3) review transcripts for patterns (e.g., all complaints about X), (4) update knowledge base or prompt for X, (5) measure post-update CSAT for X, (6) repeat. Track improvement over time.


**Q389: How would you handle a competitor launching a similar product?**  
A: 
1. Analyze competitor strengths/weaknesses, (2) double down on differentiators (multilingual, reliability, no-prompt required), (3) improve based on customer feedback, (4) accelerate roadmap for features customers are asking for, (5) leverage YC network and reputation.


**Q390: How would you design a system for monitoring model drift?**  
A: 
1. Track response distribution over time (topic, length, sentiment, refusal rate), (2) compare against baseline distribution, (3) alert on significant shift, (4) A/B test new model vs deployed, (5) auto-rollback if new model underperforms, (6) periodic manual evaluation.


**Q391: How would you add a new node type to the no-code agent builder?**  
A: 
1. Understand user need (customer request, metric opportunity), (2) design node and behavior, (3) add node type to flow definition JSON, (4) implement runtime execution logic, (5) add UI component, (6) test with internal users, (7) beta with customers, (8) full release.


**Q392: How would you debug an agent that transfers to humans too often?**  
A: 
1. Analyze transfer reasons breakdown (low ASR confidence, repeated failure, safety trigger, user request), (2) if ASR issue, check model and noise conditions, (3) if failure, check specific flow step users fail at, (4) if safety, check if guardrails too strict, (5) adjust thresholds, (6) test with historical calls.


**Q393: How would you implement progressive rollouts for prompt changes?**  
A: 
1. Config management with versioning, (2) route 1% of calls to new prompt, (3) monitor: error rate, latency, completion rate, escalation rate, (4) if metrics OK, increase to 5%, then 25%, 50%, 100%, (5) auto-rollback if metric degrades beyond threshold, (6) keep old prompt version for rollback.


**Q394: How would you handle a customer whose call volume spikes unexpectedly?**  
A: 
1. Auto-scaling handles infrastructure, (2) ensure telephony provider supports spike, (3) prioritize existing customers if resources constrained, (4) queue with position announcements, (5) soft limit and inform customer, plan capacity, (6) post-spike: understand cause, plan for next time.


**Q395: How would you design a system to ensure data portability?**  
A: 
1. Export API: all data (calls, transcripts, recordings, config) in machine-readable format (JSON, CSV), (2) per-customer export, (3) date range filter, (4) async for large exports (email when ready), (5) industry-standard formats, (6) clear documentation.


**Q396: How would you implement a voice preview feature in no-code builder?**  
A: 
1. User types/pastes prompt text, (2) system processes through preview pipeline (mock NLU + LLM + TTS), (3) plays generated audio via browser, (4) shows expected transcript, (5) allows editing and re-previewing, (6) instant feedback (<2s latency).


**Q397: How would you handle a user requesting silent mode during a call?**  
A: 
1. Detect situation (user asks for silence, background noise only), (2) agent acknowledges (“Of course, I’ll wait”), (3) silent mode with periodic check-ins (“Are you still there?” after 30s), (4) offer to call back, (5) graceful timeout and disconnect.


**Q398: How would you detect agent misbehavior at scale?**  
A: 
1. Automated monitors: policy violations, promise detection (“I’ll refund you”), compliance checks, (2) outlier detection on metrics (unusually long calls, high transfer rate), (3) sampling with random call review, (4) customer feedback analysis, (5) LLM-as-judge evaluation.


**Q399: How would you design the onboarding flow for a new enterprise customer?**  
A: 
1. Kickoff call: understand use case, volume, languages, CRM, (2) Agent setup: configure prompts, flows, knowledge base, (3) Integration: connect CRM, configure webhooks, (4) Testing: test calls to refine, (5) Go-live: deploy and monitor closely, (6) Review: 30-day check-in.


**Q400: How would you handle a security researcher reporting a vulnerability?**  
A: 
1. Thank them, (2) confirm receipt within 24h, (3) investigate and validate, (4) determine severity and impact, (5) develop fix, (6) deploy fix, (7) coordinate disclosure timeline, (8) credit researcher if they agree, (9) post-mortem to prevent recurrence.


**Q401: How would you design for serving both real-time and batch processing?**  
A: 
1. Real-time path: streaming ASR, low-latency LLM, streaming TTS for live calls, (2) Async path: full transcription, summarization, analytics, billing via message queue, (3) Separate resource pools for real-time vs async, (4) Different scaling policies per path.


**Q402: How would you debug a silent call failure (no audio either direction)?**  
A: 
1. Check if call was actually connected (SIP 200 OK received?), (2) Check media path (RTP flowing?), (3) Check codec negotiation (both sides agree on codec?), (4) Check firewall/NAT (RTP ports open?), (5) Check media server logs, (6) Check for SRTP mismatch.


**Q403: How would you implement conversation summarization?**  
A: Post-call: run LLM on full transcript to generate: 
1. call summary (what happened), (2) action items, (3) follow-up needed, (4) sentiment/emotion arc, (5) key entities mentioned, (6) compliance flags. Store summary in DB for search and reporting.


**Q404: How would you design an API rate limiting strategy for a global product?**  
A: 
1. Distributed rate limiting (Redis-based), (2) per-customer + per-endpoint limits, (3) burst allowance (2x sustained rate), (4) tiered limits (free/pro/enterprise), (5) geographic distribution (separate counters per region), (6) clear response headers, (7) backoff instructions in 429 responses.


**Q405: How would you handle a customer needing HIPAA compliance?**  
A: 
1. BAA (Business Associate Agreement) in place, (2) Encrypt all PHI at rest and in transit, (3) Access controls with audit logging, (4) Data minimization (don’t capture unnecessary PHI), (5) Self-hosted LLM (no PHI to third parties), (6) Automatic purging of PHI after retention, (7) Breach notification process.


**Q406: How would you approach building a voice agent for a completely new domain?**  
A: 
1. Collect domain knowledge (docs, FAQs, existing call recordings), (2) Build domain-specific knowledge base, (3) Write initial prompts with domain terminology, (4) Record sample calls with domain experts, (5) Iterate based on real test calls, (6) Add domain-specific guardrails, (7) Monitor and refine with production data.


**Q407: How would you handle real-time transcription for conference calls?**  
A: 
1. Multi-channel if separate streams available (run ASR per channel), (2) Single-channel with diarization (identify speakers), (3) Speaker identification based on voice characteristics, (4) Proper attribution in live transcript display, (5) Handling overlapping speech (challenge), (6) Post-call merged transcript.


**Q408: How would you test voice agents across different telecommunications providers?**  
A: 
1. Test calls routed through each provider, (2) Measure: setup time, audio quality (MOS), reliability (drop rate), ASR accuracy (codec affects), latency, (3) Automated test callers rotate through providers, (4) Compare metrics statistically, (5) Provider scorecard for routing decisions.


**Q409: How would you implement a “whisper” feature for human agent coaching?**  
A: 
1. Coach hears both sides of conversation, (2) Coach can whisper to agent (agent hears, caller doesn’t), (3) Whisper via separate audio channel/mixing at media server, (4) Coach can see real-time transcript and suggested responses, (5) Coach can barge-in if needed (agent + caller hear).


**Q410: How would you design for WebSocket reconnection in mobile networks?**  
A: 
1. Exponential backoff with jitter (1s, 2s, 4s, 8s, max 30s), (2) Send last known state on reconnect, (3) Server replays missed events from sequence gap, (4) Aggressive heartbeat (every 5s) for prompt detection, (5) Detect network type changes (WiFi to cellular), (6) Graceful degradation on reconnect failure.


**Q411: How would you implement a multi-step call flow (e.g., survey then transfer)?**  
A: 
1. State machine: SURVEY_FLOW -> COMPLETE -> TRANSFER, (2) Survey nodes collect responses, (3) On completion, trigger transfer to appropriate department based on responses, (4) Pass survey results with transfer context, (5) Handle partial completion (user hangs up mid-survey).


**Q412: How would you handle enterprise SSO/SAML integration?**  
A: 
1. Support SAML 2.0 and OIDC, (2) IdP-initiated and SP-initiated SSO, (3) Just-in-time user provisioning from SAML attributes, (4) Role mapping from SAML groups, (5) Session management (IdP logout, session timeout), (6) Multiple IdP support per enterprise.


**Q413: How would you design a system to detect and block robocallers?**  
A: 
1. Analyze call patterns (rapid re-dial, short calls), (2) Caller ID reputation scoring, (3) STIR/SHAKEN verification, (4) Answering pattern analysis, (5) Rate limiting per source number, (6) CAPTCHA challenge (press a number), (7) Blocklist with manual override.


**Q414: How would you approach migrating from a monolith to microservices?**  
A: 
1. Identify bounded contexts (ASR, LLM, TTS, state, telephony), (2) Extract one service at a time (strangler fig pattern), (3) Maintain backward compatibility during transition, (4) Use feature flags to control traffic to new services, (5) Add monitoring for each new service, (6) Rollback plan for each extraction.


**Q415: How would you design for disaster recovery across regions?**  
A: 
1. Active-active deployment in multiple regions, (2) Global load balancer for traffic distribution, (3) Database cross-region replication, (4) State replication (Redis across regions), (5) Telephony provider diversity per region, (6) Regular DR drills, (7) RTO < 5min, RPO < 30s.


**Q416: How would you implement a “don’t call me” list across channels?**  
A: 
1. Universal opt-out database (phone, email, WhatsApp), (2) Check before any outbound communication, (3) Immediate processing - opt-out stops all future communications, (4) Confirmation to user, (5) Respect across all campaigns, (6) Required by TCPA and similar regulations, (7) Audit trail for compliance.


**Q417: How would you handle a voice agent that becomes unresponsive mid-call?**  
A: 
1. Watchdog timer per call (no response from agent for >10s), (2) Attempt to reinitialize agent state, (3) If retry fails, apologize to user (“I’m having a technical issue”), (4) Offer callback or transfer, (5) Log failure for debugging, (6) Alert operations team.


**Q418: How would you design for Voice over 5G (VoNR)?**  
A: 
1. Understand 5G standalone architecture (IMS over 5G core), (2) Support for higher quality codecs (EVS - Enhanced Voice Services), (3) Lower latency expectations, (4) Better QoS handling, (5) Integration with 5G network exposure functions, (6) Future: network slicing for guaranteed quality.


**Q419: How would you implement custom vocabulary for enterprise clients?**  
A: 
1. Per-customer pronunciation dictionary (phoneme mappings), (2) Custom language model biasing (boost probability of domain terms), (3) Grammar-constrained decoding for known formats, (4) Hotword/phrase replacement in TTS, (5) Named entity lists for improved NER, (6) API for customers to manage their vocabulary.


**Q420: How would you design an end-to-end encrypted voice agent?**  
A: 
1. End-to-end encryption between caller and AI (no plaintext audio on platform), (2) Homomorphic encryption for ASR (emerging, compute-heavy), (3) On-device/edge processing for sensitive parts, (4) Split processing: encrypted audio for recording, decrypted only momentarily for ASR, (5) Key management per session, (6) Trade-off: no post-call transcription.

---
*Total: 420 questions covering all major technical domains for Samora AI product development.*



## 17. Voice AI Product & Domain Knowledge (Q421–Q450)


**Q421: How does Samora’s no-prompt-tuning approach work technically?**  
A: Customers describe workflows in plain language. Samora converts this into structured agent configurations: system prompts, few-shot examples, guardrails, call flow state machines, and knowledge base connections. The underlying LLM and rule engine handle the variability. This means Samora abstracts away AI complexity behind natural language interfaces.


**Q422: What is the difference between a voice bot and a voice agent?**  
A: Voice bot: scripted, menu-driven (press 1 for X), limited NLP, deterministic. Voice agent: AI-powered, understands open-ended input, maintains context, makes decisions, executes actions, escalates when needed. Samora builds voice agents that can handle complex workflows and natural conversation, not just menu navigation.


**Q423: How would you measure business outcomes for a voice agent deployment?**  
A: 
1. Cost per call vs human agent, (2) FCR (First Call Resolution) rate, (3) Average Handle Time (AHT), (4) Customer Satisfaction Score (CSAT), (5) Net Promoter Score (NPS), (6) Conversion rate (for sales), (7) Collection rate (for debt recovery), (8) Call containment rate (did AI resolve without escalation).


**Q424: What are common voice agent KPIs tracked by enterprises?**  
A: Operational: calls handled, avg duration, abandonment rate, service level (X% answered in Y seconds). Quality: CSAT, FCR, quality score, compliance adherence. Financial: cost per call, cost per minute, ROI vs human agents. Business: conversion rate, collection rate, lead qualification rate.


**Q425: How do you handle voice agent performance across different industries?**  
A: Each industry has unique requirements: 
1. Banking: strict compliance, authentication, transaction handling, (2) Healthcare: HIPAA, PHI handling, appointment scheduling, (3) E-commerce: order status, returns, product recommendations, (4) Collections: payment negotiation, hardship programs, legal compliance, (5) Recruitment: candidate screening, interview scheduling, skills assessment. Prompts and flows are tailored per industry.


**Q426: What are the key considerations for voice agents in collections?**  
A: 
1. FDCPA compliance (US), (2) Time-of-day restrictions, (3) DNC list checking, (4) Identity verification before discussing debt, (5) Payment plan negotiation capabilities, (6) Recording consent, (7) Empathy and de-escalation, (8) Hardship program identification, (9) Promise-to-pay tracking, (10) Escalation for legal situations.


**Q427: How would you design a voice agent for healthcare appointment scheduling?**  
A: 
1. HIPAA-compliant infrastructure, (2) PHI handling in prompts (minimization), (3) Provider calendar integration, (4) Patient identity verification, (5) Insurance verification, (6) Appointment type identification, (7) Reminder and confirmation calls, (8) Rescheduling and cancellation, (9) Follow-up instructions.


**Q428: What are the considerations for voice agents in recruitment?**  
A: 
1. Candidate experience (friendly, informative), (2) Resume parsing and qualification matching, (3) Schedule coordination (candidate + recruiter calendars), (4) Skill assessment questions, (5) Language proficiency verification, (6) Status updates to ATS, (7) Re-engagement of past candidates, (8) Compliance with hiring regulations.


**Q429: How do you handle voice agents for 911/emergency services?**  
A: 
1. Immediate recognition of emergency keywords, (2) Instant escalation to human operator, (3) Location detection and transmission, (4) Call recording with highest priority, (5) No delays or menu trees, (6) Failover to backup systems, (7) Regulatory compliance (Kari’s Law, RAY BAUM’S Act in US). Note: AI agents for emergency services must have rigorous certification.


**Q430: How would you build a voice agent for multilingual customer support?**  
A: 
1. Language detection at call start, (2) Route to language-specific model/prompt, (3) Same agent persona across languages, (4) Knowledge base in all supported languages, (5) Code-switching support, (6) Language-specific compliance rules, (7) Fallback to English if language uncertain, (8) Monitor per-language quality metrics.


**Q431: What is the ideal call flow for an outbound sales agent?**  
A: 
1. Opening: identify self and company, 2. Permission: “Is now a good time?”, 3. Qualification: budget, authority, need, timeline (BANT), 4. Pitch: tailored to prospect needs, 5. Objection handling: address concerns, 6. Close: clear next step (meeting, demo, trial), 7. Follow-up: schedule or note, 8. Wrap-up: positive closing.


**Q432: How would you design a voice agent for customer reactivation?**  
A: 
1. Identify lapsed customer and reason, (2) Personalized re-engagement (reference history), (3) Offer incentive if applicable, (4) Address concerns that caused churn, (5) Make it easy to return (immediate value), (6) Handle objections gracefully, (7) Confirm reactivation intent, (8) Follow-up with summary and next steps.


**Q433: How do you handle voice agents for feedback and surveys?**  
A: 
1. Short and focused (respect user time), (2) Clear rating scale instructions (“On a scale of 1 to 5…”), (3) Open-ended question capture, (4) Sentiment analysis on responses, (5) Branching based on answers, (6) Thank and close, (7) Real-time analytics dashboard for survey results.


**Q434: What are the unique challenges of voice agents for government/NGO use?**  
A: 
1. Multilingual requirements (often many local languages), (2) Low-literacy user considerations, (3) Legacy system integration, (4) Strict compliance and auditing, (5) High call volumes during campaigns, (6) Limited technical infrastructure in remote areas, (7) Accessibility requirements, (8) Transparent and fair AI with no bias.


**Q435: How would you handle outbound political campaign calls with voice AI?**  
A: 
1. Compliance: identify as AI, purpose, who is paying for the call, (2) Script: issue-based, not misleading, (3) Opt-out: immediate processing, (4) Call timing: respecting calling hours, (5) DNC list compliance, (6) Recording and audit trail, (7) Data management: secure storage of responses.


**Q436: How would you design a voice agent for KYC/identity verification?**  
A: 
1. Multi-factor authentication (knowledge-based + biometric + document), (2) Document number collection via speech or DTMF, (3) Voiceprint creation and matching, (4) Liveness detection (prevent recording replay), (5) Step-by-step guidance through verification, (6) Escalation for failed verification, (7) Secure handling of PII.


**Q437: How do you handle voice agents for appointment reminders?**  
A: 
1. Confirm appointment details (date, time, location), (2) Confirm attendance, (3) Offer rescheduling if cannot attend, (4) Provide preparation instructions, (5) Confirm contact preferences for future, (6) Update calendar/CRM, (7) Smooth escalation for questions.


**Q438: What are the best practices for voice agent tone and persona?**  
A: 
1. Match brand voice (friendly, professional, empathetic), (2) Be consistent across all interactions, (3) Use appropriate formality (B2B formal, B2C casual), (4) Adapt to user emotion (angry = calm, happy = warm), (5) Be transparent about being AI, (6) Use simple, clear language, (7) Show personality without being annoying.


**Q439: How do you design voice agents for high-volume outbound campaigns?**  
A: 
1. Predictive dialing integration (AI predicts when agent/human available), (2) Voicemail detection and message dropping, (3) Progressive dialing (dial next only when agent free), (4) Campaign management (lists, rotations, A/B testing scripts), (5) Rate limiting (avoid carrier blocking), (6) Answering machine detection.


**Q440: How would you handle voice agents for real estate lead follow-up?**  
A: 
1. Immediate response to inquiry, (2) Qualify lead (budget, timeline, preferences), (3) Schedule property viewing, (4) Answer property-specific questions, (5) Send property details via SMS/WhatsApp, (6) Nurture non-urgent leads with follow-up schedule, (7) Integrate with MLS/CRM for property data.


**Q441: How do you design a voice agent for technical support?**  
A: 
1. Step-by-step diagnostic flow, (2) Product knowledge base integration, (3) Ability to verify device/account info, (4) Common issue resolution scripts, (5) Escalation to tier-2 when needed, (6) Case number generation, (7) Follow-up scheduling if issue not resolved, (8) Clear “dos and don’ts” to prevent harmful actions.


**Q442: How do you ensure voice agents handle sensitive conversations (e.g., grief, mental health)?**  
A: 
1. Pre-trained empathetic response templates, (2) Detection of crisis keywords (immediate escalation), (3) Slow, calm speaking pace, (4) Avoid dismissive phrases, (5) Clear escalation path to human professionals, (6) Scripted “handoff” to avoid awkward transitions, (7) Trauma-informed language design.


**Q443: How would you build a voice agent for restaurant reservations?**  
A: 
1. Date/time/party size collection, (2) Table availability check (POS/calendar integration), (3) Special requests (allergies, occasions), (4) Confirmation and reminder setup, (5) Cancellation handling, (6) Waitlist management, (7) Integration with reservation system (OpenTable, etc.), (8) Follow-up for no-shows.


**Q444: How do you handle voice agents in the insurance industry?**  
A: 
1. Policy lookup and explanation, (2) Claim filing (collect details, assess urgency), (3) Coverage verification, (4) Agent/Adjuster dispatch, (5) Premium payment processing, (6) Renewal reminders, (7) Compliance with insurance regulations, (8) Fraud detection integration.


**Q445: How would you design a voice agent for hotel booking?**  
A: 
1. Check-in/check-out dates, (2) Room type preferences, (3) Special requests (view, floor, amenities), (4) Rate and availability check, (5) Guest information collection, (6) Payment processing, (7) Confirmation with booking reference, (8) Pre-arrival reminders and offers.


**Q446: How do you design voice agents for the gig economy (rides, deliveries)?**  
A: 
1. Real-time order/trip status, (2) Issue reporting (lost items, driver issues), (3) Payment and fare inquiries, (4) Account management, (5) Safety features (emergency contact), (6) Rating and feedback, (7) Multi-language support for diverse user base, (8) Quick resolution (time-sensitive).


**Q447: How would you build a voice agent for nonprofit donor outreach?**  
A: 
1. Personalized greeting with donation history, (2) Campaign-specific messaging, (3) Donation processing (card on file), (4) Recurring donation setup, (5) Impact storytelling, (6) Receipt and thank-you, (7) Volunteer opportunity offering, (8) Compliance (charity regulations, tax receipt).


**Q448: How do you design voice agents for patient intake in healthcare?**  
A: 
1. Patient identity verification, (2) Insurance information collection, (3) Medical history questionnaire (guided), (4) Reason for visit collection, (5) Symptom triage (urgency assessment), (6) Appointment scheduling based on urgency, (7) Pre-visit instructions, (8) Integration with EHR systems.


**Q449: How would you handle voice agents for financial advisory?**  
A: 
1. Client verification (multi-factor), (2) Portfolio balance and performance inquiries, (3) Transaction history, (4) Financial goal check-ins, (5) Educational content delivery, (6) Meeting scheduling with human advisor, (7) Compliance: no specific investment recommendations without proper disclosures, (8) Secure document exchange.


**Q450: How do you design voice agents for supply chain/logistics?**  
A: 
1. Shipment tracking and status, (2) ETA and delay notifications, (3) Proof of delivery confirmation, (4) Inventory level checks, (5) Reorder triggers, (6) Carrier selection and routing, (7) Exception handling (damage, loss), (8) Integration with WMS/TMS systems.


## 18. Advanced Topics & Future Trends (Q451–Q480)


**Q451: How would you implement real-time language translation in a voice agent?**  
A: 
1. ASR in source language, (2) Neural Machine Translation (NMT) to target language, (3) TTS in target language, (4) End-to-end latency target < 2s, (5) Preserve prosody and emotion across translation, (6) Handle code-switched input, (7) Speaker voice preservation in target language. Challenge: maintaining natural conversation flow with translation latency.


**Q452: What is the future of voice agents with multimodal AI?**  
A: Future voice agents will combine voice + vision + text. Examples: 
1. Agent sees caller’s face (with consent) to read emotion, (2) Agent views a product the caller is holding via camera, (3) Screen sharing for guided troubleshooting, (4) Document verification via camera. This requires: audio-video sync, real-time vision processing, privacy by design.


**Q453: How would you implement emotion recognition in voice?**  
A: 
1. Acoustic features: pitch, energy, speaking rate, voice quality, (2) Text features: word choice, sentiment, (3) Multi-modal fusion (audio + text), (4) Emotion categories: angry, happy, sad, frustrated, neutral, anxious, (5) Real-time per-utterance classification, (6) Use emotion to adapt agent behavior (tone, escalation). Challenges: cultural differences in emotion expression, accuracy across languages.


**Q454: How do you see on-device voice AI evolving?**  
A: On-device AI reduces latency and improves privacy. Trends: 
1. Smaller models running on phones/edge (quantization, distillation), (2) Hybrid: on-device for simple tasks, cloud for complex, (3) Privacy-sensitive processing locally (PII redaction), (4) Apple Intelligence, Android AI Core enabling on-device ASR/LLM, (5) Federated learning for model improvement without data centralization.


**Q455: How would you approach building a voice agent that learns from human feedback?**  
A: 
1. RLHF (Reinforcement Learning from Human Feedback): collect human ratings of agent responses, (2) Fine-tune model on preferred responses, (3) Implicit feedback: user behavior (repeat calls, escalation, CSAT), (4) Human-in-the-loop: agents review and correct responses, (5) Active learning: identify uncertain turns for human review, (6) Continuous deployment of improved models.


**Q456: What are the ethical considerations for AI voice agents?**  
A: 
1. Transparency: users must know they speak to AI, (2) Consent: recording and data usage consent, (3) Privacy: data minimization, encryption, (4) Bias: ensure equal quality across languages, accents, demographics, (5) Accountability: who is responsible for agent mistakes?, (6) Employment: impact on call center jobs, (7) Safety: preventing harmful advice, (8) Accessibility: serving users with disabilities.


**Q457: How would you implement voice agent self-service analytics?**  
A: Customer-facing analytics dashboard: 
1. Call volume trends, (2) Success rate by flow, (3) Frequently asked questions, (4) Sentiment trends, (5) Escalation reasons, (6) Agent performance metrics, (7) Cost savings calculator, (8) Custom report builder, (9) Scheduled PDF exports, (10) API access for data integration.


**Q458: How would you design a voice agent marketplace?**  
A: Platform for pre-built voice agents: 
1. Industry templates (healthcare, finance, retail), (2) Use-case templates (collections, support, surveys), (3) Customization options per template, (4) Integration library (CRM, calendar, payment), (5) Rating and review system, (6) Partner/developer program for template creation, (7) Revenue sharing model.


**Q459: How do you handle voice agents for Web3/decentralized applications?**  
A: 
1. Wallet connection via voice (seed phrase? no, too risky), (2) Transaction verification via voice biometric, (3) Blockchain data queries (balance, transaction status), (4) Smart contract interaction (limited, high risk), (5) NFT/game asset inquiries, (6) Decentralized identity (DID) for authentication, (7) Challenge: irreversible transactions require extra safety.


**Q460: How would you implement a voice agent that can generate and send emails?**  
A: 
1. Understand user intent (compose new, reply, forward), (2) Collect: recipient, subject, body, attachments, (3) Verify with user before sending (“Send to John about project update?”), (4) Generate email content via LLM, (5) Send via email API (SendGrid, Gmail API), (6) Confirm sent, (7) Handle: cc/bcc, signatures, templates.


**Q461: How do you handle voice agents on smart speakers (Alexa, Google Home)?**  
A: 
1. Different interaction model (wake word + command), (2) Shorter, more concise responses, (3) Visual-less design (no screen dependency), (4) Skill/action development per platform, (5) Session management across platforms, (6) Cross-platform consistency, (7) Discovery and certification process for each platform.


**Q462: How would you design a voice agent for education/tutoring?**  
A: 
1. Adaptive questioning based on knowledge level, (2) Subject matter expertise (math, science, languages), (3) Step-by-step problem-solving guidance, (4) Patience and encouragement, (5) Progress tracking and reporting, (6) Multiple explanation styles for different learners, (7) Plagiarism/cheating prevention, (8) Parent/teacher dashboard.


**Q463: How do you implement voice-controlled smart home via AI agents?**  
A: 
1. Device discovery and control integration (IoT APIs), (2) Natural language commands (“Set living room temp to 72”), (3) Routine creation (“When I say goodnight, turn off lights”), (4) Scene activation, (5) Multi-device coordination, (6) Physical safety constraints (no unlock doors without PIN), (7) Energy optimization suggestions.


**Q464: How would you approach voice agents for mental health support?**  
A: 
1. Evidence-based conversational frameworks (CBT, MI), (2) Crisis detection and immediate escalation, (3) Empathetic, non-judgmental tone, (4) Privacy and confidentiality (HIPAA), (5) Limitations disclaimer (“I’m not a therapist”), (6) Mood tracking and trends, (7) Resource recommendations, (8) Integration with professional care network.


**Q465: How do you design voice agents for automotive/in-car use?**  
A: 
1. Hands-free, eyes-free design (critical for safety), (2) Voice activity detection with noise cancellation (road noise), (3) Short, simple responses (reduce cognitive load), (4) Navigation and POI queries, (5) Media control, (6) Climate and comfort control, (7) Emergency assistance, (8) Distraction-free interaction patterns.


**Q466: How would you build a voice agent that personalizes based on user history?**  
A: 
1. User profile store (preferences, history, past issues), (2) Context injection into LLM prompt on each call, (3) Personalization: name, preferred language, account type, (4) Historical reference (“Last time you called about X, has that been resolved?”), (5) Predictive needs based on patterns, (6) Privacy: user can opt-out of personalization.


**Q467: How do you handle voice agents for accessibility (blind/low-vision users)?**  
A: 
1. Screen reader compatible interfaces, (2) Clear, descriptive verbal output, (3) No reliance on visual cues (“press the green button”), (4) Keyboard/speech-only navigation, (5) High-contrast text for partial sight, (6) Variable speaking rate control, (7) WCAG compliance for any web components, (8) Testing with actual blind/low-vision users.


**Q468: How would you implement a voice agent API for third-party developers?**  
A: 
1. REST + WebSocket APIs for call control, (2) SDKs in Python, JavaScript, Java, (3) Webhook events for call lifecycle, (4) Developer dashboard with API keys and usage, (5) Rate limiting and quotas, (6) Documentation and examples, (7) Sandbox environment for testing, (8) SLA for API availability.


**Q469: How do you handle voice agents that need to read long documents?**  
A: 
1. Summarize document first (LLM summarization), (2) Present summary, ask if user wants details, (3) Progressive disclosure: offer to dive deeper on specific sections, (4) Break into digestible chunks (30s each), (5) Allow navigation (“skip to section 3”), (6) Offer to send full document via SMS/email.


**Q470: How would you manage a voice agent deployment across multiple time zones?**  
A: 
1. Timezone detection from caller ID/CRM, (2) Respect local calling hours per jurisdiction, (3) Language selection based on region, (4) Holiday calendars per region (don’t call on holidays), (5) Follow-the-sun for human escalation, (6) Timezone-aware scheduling for callbacks.


**Q471: How do you design voice agents for compliance-heavy industries (finance, pharma)?**  
A: 
1. Full audit trail of every interaction, (2) Compliance guardrails as code, (3) Pre-approved response templates for regulated content, (4) Real-time compliance monitoring, (5) Disclaimers at appropriate points, (6) Escalation for anything outside compliance boundaries, (7) Regular compliance testing, (8) Integration with compliance archives.


**Q472: How would you implement a “whisper” mode for silent environments?**  
A: 
1. User alerts agent they’re in a quiet place, (2) Agent reduces speaking volume, (3) User whispers responses (train ASR for whispered speech), (4) Alternative: switch to text-based (SMS/chat), (5) Agent offers text follow-up with full details, (6) Respect user’s situation with minimal interaction.


**Q473: How do you handle voice agents for international expansion?**  
A: 
1. Prioritize languages by market size/customer demand, (2) Legal compliance per country (GDPR in EU, PIPL in China, etc.), (3) Local telephony providers, (4) Cultural adaptation of prompts (not just translation), (5) Local number presence, (6) Timezone and holiday support, (7) Payment method adaptation, (8) Local data residency requirements.


**Q474: How would you design a voice agent that can negotiate?**  
A: 
1. Define negotiable parameters (price, terms, timeline), (2) Understand user’s position and constraints, (3) Pre-approved concession ranges, (4) BATNA (Best Alternative To Negotiated Agreement) logic, (5) Escalation for out-of-range requests, (6) Track negotiation state over multiple calls, (7) Document agreed terms, (8) Compliance: agent cannot make unauthorized commitments.


**Q475: How do you implement voice agents for field service/dispatch?**  
A: 
1. Technician identification and authentication, (2) Job assignment and details, (3) Parts availability check, (4) Customer pre-arrival notification, (5) Real-time status updates, (6) Issue escalation to engineering, (7) Post-job completion and documentation, (8) Integration with field service management (FSM) platforms.


**Q476: How would you build a voice agent that can process returns?**  
A: 
1. Order lookup via email/order number, (2) Return reason collection, (3) Return eligibility check (return window, condition), (4) Return method selection (mail, drop-off), (5) Label generation and delivery (email/SMS), (6) Refund/replacement processing, (7) Status tracking, (8) Exception handling (damaged, missing parts).


**Q477: How do you design voice agents for warranty and claims?**  
A: 
1. Product identification (serial number, model), (2) Warranty verification (purchase date, coverage), (3) Issue diagnosis flow, (4) Claim documentation, (5) Service appointment scheduling, (6) Parts ordering, (7) Status updates, (8) Integration with warranty management systems.


**Q478: How would you implement noise-robust voice AI for industrial environments?**  
A: 
1. Advanced noise suppression (deep learning models: DCCRN, DeepFilterNet), (2) Multi-microphone beamforming, (3) Near-field/far-field adaptation, (4) Vibration-resistant audio processing, (5) Industrial-specific vocabulary, (6) High-SNR ASR training, (7) Physical: noise-canceling microphone selection.


**Q479: How do you handle voice AI for elderly users?**  
A: 
1. Slower speaking pace, (2) Louder and clearer TTS, (3) Simpler vocabulary and sentence structure, (4) Patience (longer timeouts), (5) Easy repetition (“Just say ‘repeat’”), (6) Confirmation loops for critical info, (7) Larger fonts if visual interface present, (8) Family caregiver notification options, (9) Accessibility-first design.


**Q480: What is the role of voice AI in the metaverse?**  
A: 
1. Natural voice interaction for virtual worlds, (2) Spatial audio and 3D voice, (3) Avatar voice matching and lip sync, (4) Real-time translation for global metaverse, (5) Voice-driven avatar actions, (6) Emotionally expressive NPCs, (7) Voice commerce in virtual stores, (8) Moderation and safety via voice analysis.


## 19. Code & System Design Scenarios (Q481–Q500)


**Q481: Write pseudocode for a function that detects code-switching in a user utterance.**  
A: def detect_code_switch(text): 
  segments = [] 
  current_lang = detect_language(text[:100])  # first 100 chars
  start = 0
  for i in range(100, len(text), 50):
    chunk_lang = detect_language(text[i:i+50])
    if chunk_lang != current_lang:
      segments.append((start, i, current_lang))
      start = i
      current_lang = chunk_lang
  segments.append((start, len(text), current_lang))
  return segments if len(segments) > 1 else None


**Q482: How would you design a rate limiter for voice API calls?**  
A: Algorithm: sliding window counter. Store user request timestamps in Redis sorted set. On each request: remove timestamps older than window (e.g., 1s), count remaining, if count > limit (e.g., 10 req/s), reject with 429. Use Lua script for atomicity. Per-customer limits configurable via DB. Async cleanup of old entries. Burst allowance using token bucket on top.


**Q483: Design a WebSocket-based audio streaming server architecture.**  
A: Server receives binary audio chunks via WebSocket (opcode 0x2). Each chunk has header: sequence, timestamp, format. AudioProcessorService: noise suppression, VAD, ASR. ASR streams partial results back as JSON text messages. LLMProcessor handles complete utterances. TTSProcessor sends audio chunks back as binary messages. Async queues between stages for backpressure.


**Q484: Write a Python function to merge overlapping conversation turns.**  
A: def merge_turns(turns): 
  if not turns: return [] 
  sorted_turns = sorted(turns, key=lambda t: t["start_time"]) 
  merged = [sorted_turns[0]] 
  for turn in sorted_turns[1:]: 
    last = merged[-1] 
    if turn["start_time"] <= last["end_time"]: 
      last["text"] += " " + turn["text"] 
      last["end_time"] = max(last["end_time"], turn["end_time"]) 
    else: merged.append(turn) 
  return merged


**Q485: Design a system to ensure exactly-once processing for call events.**  
A: Idempotency key per event (UUID). Store processed keys in Redis (TTL 24h). Before processing: check if key exists. If yes: return cached response. If no: process, store result, return. Downstream also idempotent (CRM update has idempotency key). Dead letter queue for failed events with manual replay.


**Q486: How would you implement a distributed lock for voice resource allocation?**  
A: Redis Redlock algorithm. Acquire lock on a resource (e.g., phone number) with TTL (30s). Key format: lock:resource:{id}. Value: unique token (call_id). Release only if token matches (prevent releasing others’ locks). Retry with backoff on contention. Fallback: queue request if lock not acquired within timeout.


**Q487: Write a function to calculate WER (Word Error Rate) between two transcripts.**  
A: def wer(reference, hypothesis): 
  ref_words = reference.split() 
  hyp_words = hypothesis.split() 
  n = len(ref_words); m = len(hyp_words) 
  dp = [[0]*(m+1) for _ in range(n+1)] 
  for i in range(n+1): dp[i][0] = i 
  for j in range(m+1): dp[0][j] = j 
  for i in range(1, n+1): 
    for j in range(1, m+1): 
      cost = 0 if ref_words[i-1] == hyp_words[j-1] else 1 
      dp[i][j] = min(dp[i-1][j]+1, dp[i][j-1]+1, dp[i-1][j-1]+cost) 
  return dp[n][m] / n if n > 0 else 0


**Q488: Design a circuit breaker for LLM API calls.**  
A: State machine: CLOSED (normal), OPEN (failing), HALF-OPEN (testing). Config: failure_threshold=5, timeout=30s, half_open_max_requests=1. On failure: count++, if count >= threshold, transition to OPEN. On success in CLOSED: reset count. In OPEN: fail fast (return fallback), start timer. On timer expiry: transition to HALF-OPEN. In HALF-OPEN: allow 1 request, success = CLOSED, fail = OPEN.


**Q489: How would you implement voice activity detection in Python?**  
A: import webrtcvad 
  vad = webrtcvad.Vad(2)  # aggressiveness 0-3 
  def is_speech(audio_frame_30ms, sample_rate=16000): 
    return vad.is_speech(audio_frame_30ms, sample_rate) 
  Process audio in 30ms frames (480 samples at 16kHz). Sliding window: if 3+ of last 5 frames have speech, VAD activated. Hangover: keep VAD active for 5 frames after speech ends. For production: use Silero VAD (PyTorch, more accurate).


**Q490: Design a priority queue for human escalation requests.**  
A: Priority levels: P0 (emergency, escalated ASAP within 30s), P1 (angry customer, within 2min), P2 (standard, within 5min), P3 (low priority, within 15min). Each request has: call_id, priority, language, required_skill, timestamp, context_json. Workers pull highest priority item matching their skills. Queue: Redis sorted set with (priority_score, timestamp) as score. P0 > P1 > P2 > P3.


**Q491: Write a function to normalize phone numbers to E.164 format.**  
A: import phonenumbers 
  def normalize_phone(number, default_region="IN"): 
    try: 
      parsed = phonenumbers.parse(number, default_region) 
      if phonenumbers.is_valid_number(parsed): 
        return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164) 
    except: pass 
    return None  # invalid


**Q492: Design a system for real-time transcription with speaker diarization.**  
A: Two-model approach: 
1. Streaming ASR (Conformer-Transducer) provides per-chunk text, (2) Diarization model (PyAnnote Audio) runs on overlapping windows (1.5s, shift 0.5s) to assign speaker labels. Align: when ASR outputs a phrase, match its time range with diarization output to assign speaker. For 2-speaker (AI + human), simple energy-based VAD + speaker change detection works well.


**Q493: How would you implement a retry queue with exponential backoff?**  
A: Queue items have: id, payload, retry_count, max_retries=3, next_retry_at. On failure: increment retry_count, set next_retry_at = now + (initial_delay * 2^retry_count) + random_jitter(0, 1s). Worker picks items where next_retry_at <= now. After max_retries: move to dead letter queue. Persistent queue (Redis sorted set by next_retry_at). Alert on DLQ items.


**Q494: Design a caching strategy for a multi-tenant voice platform.**  
A: L1 cache (in-memory, local to each service): agent configs, prompts. TTL: 60s. L2 cache (Redis cluster, shared): CRM data, language models, common responses. TTL: 300s. L3 cache (CDN): static audio prompts, voice samples. Invalidation: publish message to Redis PubSub “cache:invalidate:{key}” on data change. Per-tenant key prefix for isolation.


**Q495: Write a Python function to chunk a long response for TTS streaming.**  
A: def chunk_for_tts(text, max_chars=200): 
  import re 
  # Split at sentence boundaries 
  sentences = re.split(r'(?<=[.!?])\s+', text) 
  chunks = [] 
  current = "" 
  for s in sentences: 
    if len(current) + len(s) < max_chars: 
      current += s + " " 
    else: 
      if current: chunks.append(current.strip()) 
      current = s + " " 
  if current: chunks.append(current.strip()) 
  return chunks


**Q496: Design an event-driven architecture for post-call processing.**  
A: Events (Kafka topics): call.completed (id, duration, outcome), call.transcript_ready (id, transcript_json), call.analytics_ready (id, analytics_json). Consumers: TranscriptionService (batch ASR full audio -> transcript), AnalyticsService (sentiment, summary, entities), CRMService (update CRM), BillingService (compute cost). Each consumer processes independently. DLQ for failed events. Exactly-once with idempotency keys.


**Q497: How would you implement a health check for a voice processing pipeline?**  
A: Synthetic test call every 60s from monitoring service. 
1. Dial into platform via SIP, 2. Send predefined script (TTS plays prompts, ASR checks responses), 3. Verify: call connects (<5s), ASR transcribes accurately, LLM responds correctly, TTS plays audio, call ends cleanly. Score (0-100) and alert on deviation. Geographic diversity (test from multiple regions).


**Q498: Design a system to detect and filter PII from voice transcripts in real-time.**  
A: Pre-ASR: detect DTMF tones in audio, suppress tones + DTMF region from ASR. Post-ASR: regex patterns (SSN, credit card, phone, email), NER model (names, locations, dates), custom patterns per customer (account numbers). Replace with [REDACTED] or placeholder. Option: route unredacted to authorizer only. Log redaction events for audit.


**Q499: Write a function to select the best LLM response from multiple candidates.**  
A: def select_best_response(candidates, context): 
  scored = [] 
  for c in candidates: 
    score = 0 
    if len(c.split()) < 50: score += 1  # conciseness 
    if not c.endswith(('?', '!')): score += 1  # complete 
    if not contains_prohibited(c): score += 2  # safety 
    score += semantic_similarity(c, context["user_query"])  # relevance 
    score *= confidence_score(c)  # model confidence 
    scored.append((score, c)) 
  return max(scored, key=lambda x: x[0])[1]


**Q500: Design an overall architecture diagram for Samora’s voice agent platform.**  
A: Five layers: 
1. Channel Layer: PSTN (SIP trunk -> SBC -> FreeSWITCH), WebRTC, WhatsApp, SMS, Email. (2) Intelligence Layer: Streaming ASR, NLU, LLM (self-hosted + cloud), RAG (vector DB), TTS. (3) Orchestration Layer: Dialog Manager, State Machine, Workflow Engine, Policy Engine, Guardrails. (4) Integration Layer: CRM connectors, APIs, Webhooks, Knowledge Base, Calendar, Payment. (5) Observability Layer: Monitoring (Prometheus/Grafana), Logging (ELK), Tracing (Jaeger), Alerts (PagerDuty), Analytics (custom). Cross-cutting: Security (auth, encryption), Multi-tenancy, Billing, Audit.

---
*Total: 500 questions covering all major technical domains for Samora AI product development. Good luck with your interview!*
