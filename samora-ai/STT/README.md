# STT Interview Questions and Answers

## Q1: What is Speech-to-Text?
**A:** Speech-to-Text (STT), also known as Automatic Speech Recognition (ASR), is a technology that converts spoken language into written text. It uses acoustic and language models to transcribe audio signals into readable text format.

## Q2: How does Speech-to-Text technology work?
**A:** STT works by capturing audio through a microphone, converting analog signals to digital, then processing the audio through feature extraction (MFCCs, spectrograms), acoustic modeling (mapping audio features to phonemes), language modeling (predicting word sequences), and finally decoding to produce text output.

## Q3: What are the main components of an ASR system?
**A:** The main components are: (1) Acoustic Model — maps audio signals to phonetic units, (2) Language Model — predicts word sequences using probability, (3) Lexicon/Pronunciation Dictionary — maps words to their phonetic representations, and (4) Decoder — combines all models to produce the final transcription.

## Q4: What is the difference between online and offline STT?
**A:** Online STT processes audio in real-time as it is being spoken, providing immediate (streaming) transcription with lower latency. Offline STT processes a complete audio recording after it ends, allowing for higher accuracy since the entire context is available for decoding.

## Q5: What are MFCCs and why are they used in STT?
**A:** Mel-Frequency Cepstral Coefficients (MFCCs) are features extracted from audio signals that represent the short-term power spectrum on the Mel scale. They are widely used because they effectively capture the phonetic characteristics of human speech while being robust to noise and compression artifacts.

## Q6: Explain the role of the Language Model in STT.
**A:** The Language Model (LM) assigns probabilities to word sequences, helping the decoder choose the most linguistically plausible transcription. It resolves ambiguities by favoring grammatically and semantically coherent outputs. N-gram models and neural LMs (like Transformers) are commonly used.

## Q7: What is Word Error Rate (WER) and how is it calculated?
**A:** WER is the most common metric for STT accuracy. It is calculated as: WER = (Substitutions + Insertions + Deletions) / Total Words in Reference. Lower WER indicates better accuracy. A WER of 5% means 95% of words were transcribed correctly.

## Q8: What is the difference between WER and CER?
**A:** WER (Word Error Rate) operates at the word level and is standard for most transcription tasks. CER (Character Error Rate) operates at the character level and is preferred for languages without clear word boundaries (e.g., Chinese, Japanese) or when measuring fine-grained accuracy.

## Q9: What are the challenges of STT for low-resource languages?
**A:** Challenges include lack of transcribed training data, absence of phonetic dictionaries, limited language model corpora, dialectal variations, and difficulty in building accurate acoustic models. Techniques like transfer learning, multilingual training, and data augmentation are used to address these.

## Q10: How does noise reduction improve STT accuracy?
**A:** Noise reduction pre-processes audio to remove background sounds (traffic, fan noise, music) before feeding it to the ASR model. Techniques include spectral subtraction, Wiener filtering, and deep learning-based denoising autoencoders. Cleaner input leads to better feature extraction and lower WER.

## Q11: What is the difference between traditional HMM-based ASR and end-to-end ASR?
**A:** Traditional HMM-based ASR uses separate components (acoustic model, language model, lexicon) trained independently with Hidden Markov Models and Gaussian Mixture Models. End-to-end ASR uses a single deep neural network (e.g., RNN-T, CTC, Transformer) that directly maps audio to text, simplifying the pipeline and often achieving better accuracy.

## Q12: Explain Connectionist Temporal Classification (CTC) loss.
**A:** CTC is a loss function used in sequence-to-sequence tasks like STT. It allows the model to output a variable-length label sequence from a fixed-length input by introducing a blank token. CTC sums over all possible alignments between input and output, eliminating the need for pre-segmented audio data.

## Q13: What is an RNN-Transducer (RNN-T)?
**A:** RNN-Transducer is an end-to-end ASR architecture combining a transcription network (encoder), a prediction network (language model), and a joint network. It is well-suited for streaming/online ASR because it processes audio incrementally without requiring the full utterance, making it popular for on-device and real-time applications.

## Q14: What is the role of the Attention mechanism in modern STT?
**A:** Attention allows the decoder to focus on relevant parts of the audio input when generating each output token. In Transformer-based ASR models, self-attention and cross-attention replace recurrent connections, enabling parallel computation and better handling of long-range dependencies in speech.

## Q15: What is a Transformer-based ASR model?
**A:** A Transformer-based ASR model uses the Transformer architecture (encoder-decoder with self-attention) instead of RNNs or CNNs for speech recognition. Examples include Whisper, Wav2Vec 2.0, and SpeechTransformer. They achieve state-of-the-art results by modeling long-range audio dependencies efficiently.

## Q16: What is OpenAI Whisper and how does it work?
**A:** Whisper is a large-scale, multitask ASR model by OpenAI trained on 680,000 hours of multilingual data. It uses a Transformer encoder-decoder architecture, processes 30-second audio chunks, and can perform transcription, translation, language identification, and timestamps. It supports 99+ languages.

## Q17: What is Wav2Vec 2.0?
**A:** Wav2Vec 2.0 is a self-supervised learning framework by Meta AI for speech representation. It learns powerful audio representations from unlabeled data by masking latent speech features and solving a contrastive task. Fine-tuning with labeled data achieves state-of-the-art results with minimal supervision.

## Q18: What is the difference between streaming and non-streaming ASR?
**A:** Streaming ASR processes audio in chunks and produces partial results in real-time with low latency, suitable for live captions or voice assistants. Non-streaming ASR waits for complete audio before processing, achieving higher accuracy but higher latency. The trade-off is latency vs. accuracy.

## Q19: How does Voice Activity Detection (VAD) help STT?
**A:** VAD detects whether a segment of audio contains speech or silence. It segments the audio stream, removing non-speech portions before STT processing. This reduces computational cost, improves accuracy by avoiding transcription of silence/noise, and enables features like end-of-speech detection.

## Q20: What is speaker diarization and how does it relate to STT?
**A:** Speaker diarization answers "who spoke when" by partitioning an audio stream into homogeneous segments per speaker. Combined with STT, it enables rich transcription output with speaker labels. It typically uses clustering on speaker embeddings (e.g., x-vectors, d-vectors).

## Q21: What are the common data augmentation techniques for STT?
**A:** Common augmentation techniques include: adding background noise, speed perturbation, pitch shifting, SpecAugment (masking frequency/time dimensions), room impulse response simulation, and voice conversion. These improve model robustness to real-world acoustic variations.

## Q22: What is SpecAugment?
**A:** SpecAugment is a data augmentation technique for ASR that operates directly on spectrograms. It applies time warping, frequency masking (masking consecutive frequency channels), and time masking (masking consecutive time steps). It significantly improves generalization without requiring additional data.

## Q23: How does beam search decoding work in ASR?
**A:** Beam search maintains a set of the top-k partial hypotheses at each decoding step. At each step, it expands all candidates, scores them using acoustic and language models, prunes to keep only the k best, and continues until an end-of-sentence token is produced. The highest-scoring complete hypothesis is the final output.

## Q24: What is language model rescoring?
**A:** Language model rescoring is a two-pass decoding technique. The first pass uses a lightweight LM to generate an n-best list of hypotheses. The second pass re-ranks these hypotheses using a larger, more powerful LM (e.g., Transformer LM) to select the best transcription. This improves accuracy while keeping first-pass latency low.

## Q25: What is the difference between greedy decoding and beam search?
**A:** Greedy decoding picks the most likely token at each step without considering future context, making it fast but less accurate. Beam search explores multiple hypotheses simultaneously, choosing the overall best sequence, providing higher accuracy at the cost of more computation.

## Q26: How do you handle out-of-vocabulary (OOV) words in STT?
**A:** OOV words can be handled through subword tokenization (BPE, unigram, SentencePiece) which breaks words into smaller units, character-based models that output characters directly, or dynamic vocabulary updates via a hotlist/bias list that boosts probability for specific rare terms.

## Q27: What is subword tokenization and why is it important for STT?
**A:** Subword tokenization splits words into smaller meaningful units (e.g., "playing" → "play" + "ing"). It handles OOV words, reduces vocabulary size, and improves data efficiency. BPE (Byte Pair Encoding) and unigram LM tokenization are common in modern ASR systems.

## Q28: What is a hotlist or bias list in STT?
**A:** A hotlist (or bias list) is a set of words or phrases given higher probability during decoding. It is used to improve recognition of domain-specific terms, names, or rare words. Biasing can be applied at the language model level or through shallow fusion during beam search.

## Q29: How do you evaluate an STT system in production?
**A:** Evaluation metrics include WER/CER, Real-Time Factor (RTF), latency (first-word latency, end-of-utterance latency), and subjective quality scores. A/B testing with human raters, measuring downstream task performance (e.g., intent recognition accuracy), and monitoring for specific failure modes are also important.

## Q30: What is Real-Time Factor (RTF) in ASR?
**A:** RTF measures processing speed as the ratio of processing time to audio duration. RTF < 1 means faster than real-time (e.g., RTF = 0.5 means 1 second of audio is processed in 0.5 seconds). RTF > 1 means slower than real-time. Streaming ASR requires RTF well below 1 for real-time use.

## Q31: What is first-word latency in streaming STT?
**A:** First-word latency is the time from when a user starts speaking to when the first transcribed word appears. It includes audio buffering, VAD triggering, network transmission, and decoding time. Low first-word latency (under 200ms) is critical for natural conversational experiences.

## Q32: How do you handle punctuation restoration in STT?
**A:** Punctuation restoration adds commas, periods, question marks, etc. to raw ASR output. It is typically done by a separate punctuation model (often a fine-tuned BERT-style transformer) that processes the raw transcript and predicts punctuation tokens. Some end-to-end models directly output punctuation.

## Q33: What is inverse text normalization (ITN)?
**A:** Inverse Text Normalization converts raw ASR output (spoken-form) into written-form text. For example, "five hundred dollars and thirty cents" → "$530.30", "twenty twenty four" → "2024". ITN is essential for producing human-readable transcripts in applications like messaging and note-taking.

## Q34: How does domain adaptation work for STT?
**A:** Domain adaptation fine-tunes a general ASR model on domain-specific data (e.g., medical, legal, financial). Techniques include full fine-tuning, adapter layers, or using domain-specific language models and hotlists. It significantly improves accuracy for specialized terminology and speaking styles.

## Q35: What is the difference between supervised and self-supervised learning for ASR?
**A:** Supervised learning requires paired audio-text data for training. Self-supervised learning (e.g., Wav2Vec 2.0, HuBERT) learns useful representations from unlabeled audio alone by solving pretext tasks (masked prediction, contrastive learning), then fine-tunes on limited labeled data. Self-supervision drastically reduces labeled data requirements.

## Q36: What is HuBERT?
**A:** HuBERT (Hidden-Unit BERT) is a self-supervised speech representation model by Meta AI. It learns by predicting clustered hidden units from masked speech features. It iteratively refines cluster assignments and representations, achieving state-of-the-art results on multiple ASR benchmarks.

## Q37: How do you handle multiple languages in a single STT model?
**A:** Multilingual ASR models (e.g., Whisper, Multilingual Wav2Vec 2.0) are trained on data from many languages. They use a shared encoder and separate language-specific decoders or a shared output vocabulary. Language identification may be done automatically or provided as input. Zero-shot cross-lingual transfer is also possible.

## Q38: What is code-switching in STT and why is it challenging?
**A:** Code-switching occurs when speakers alternate between two or more languages in a single utterance (e.g., "Let's meet at the café for chai"). It is challenging because the model must handle multiple languages, phonetics, and grammars simultaneously, often with limited code-switched training data.

## Q39: What are the ethical considerations in STT deployment?
**A:** Key considerations include: bias against certain accents or dialects leading to higher WER for minority groups, privacy concerns with audio data storage, consent for recording, transparency about recording, and ensuring accessibility for non-standard speech patterns. Fairness evaluation across demographic groups is essential.

## Q40: How does accent bias manifest in ASR systems?
**A:** ASR systems often perform worse for non-native speakers, regional accents, and dialects underrepresented in training data. For example, an English ASR trained primarily on US data will have higher WER for Indian, Scottish, or African American Vernacular English. Mitigation requires diverse training data and accent-specific fine-tuning.

## Q41: What is the role of a pronunciation dictionary in ASR?
**A:** A pronunciation dictionary (lexicon) maps words to their phonetic transcriptions (sequences of phonemes). It guides the acoustic model during training and decoding. The CMU Pronouncing Dictionary is a common example for English. For end-to-end models, the lexicon role is absorbed by the model's learned mapping.

## Q42: What are phonemes and why are they important?
**A:** Phonemes are the smallest distinct units of sound in a language that can distinguish meaning (e.g., /p/ vs /b/ in "pat" vs "bat"). They are important because they form the basic building blocks for acoustic modeling, allowing the system to recognize words by identifying their constituent sounds.

## Q43: What is a triphone model?
**A:** A triphone model captures context-dependent phonemes — a phoneme in the context of its left and right neighbors (e.g., "b-ae-t" for "bat"). Triphones dramatically improve accuracy over monophones because speech sounds are heavily influenced by adjacent sounds (coarticulation).

## Q44: How do you handle disfluencies in speech (ums, uh, repetitions)?
**A:** Disfluencies can be handled by: (1) including them in training data so the model transcribes them naturally, (2) using a post-processing module to filter them out, or (3) training the model to directly output fluent text. The approach depends on the application (verbatim vs. cleaned transcripts).

## Q45: What is the difference between verbatim and non-verbatim transcription?
**A:** Verbatim transcription captures every word exactly as spoken, including disfluencies (um, uh), false starts, and repetitions. Non-verbatim transcription produces cleaned, fluent text with disfluencies removed and grammar normalized. Verbatim is used in call centers and legal; non-verbatim for subtitles and notes.

## Q46: How do you measure STT latency in a production system?
**A:** Latency is measured end-to-end from audio capture to text output. Key metrics include: first-word latency (time to first word), intermediate latency (time between partial results), and final latency (time until final transcription). Monitoring p50, p95, and p99 latencies across requests is standard.

## Q47: What is a language model warm-up in STT?
**A:** Language model warm-up refers to pre-loading and compiling the language model into memory before serving requests. This avoids cold-start latency where the first request incurs model loading time. Warm-up can be done by running dummy inference passes during server initialization.

## Q48: How do you implement STT for children's speech?
**A:** Children's speech has different acoustic properties (higher pitch, shorter vocal tracts) and linguistic patterns. Solutions include: fine-tuning on children's speech data, using pitch-normalized features, training separate child-specific models, or using age-aware data augmentation.

## Q49: What are the challenges of STT for medical applications?
**A:** Challenges include: specialized medical terminology, acronyms, medications, varying speaking styles (dictation vs. conversation), background noise in clinical settings, HIPAA/privacy compliance, need for extremely high accuracy, and integration with EHR systems. Domain-specific models and hotlists are essential.

## Q50: How does streaming ASR handle endpoint detection?
**A:** Streaming ASR uses Endpoint Detection to determine when the user has finished speaking. It combines VAD (silence detection), decoder confidence scores, and timeout heuristics. Common strategies include: fixed silence timeout, adaptive thresholds based on speaking rate, and lookback windows.

## Q51: What is the difference between LAS (Listen, Attend, Spell) and RNN-T?
**A:** LAS is an encoder-decoder attention-based model that attends over the entire audio sequence, making it non-streaming by nature. RNN-T uses a prediction network with a joint network for frame-synchronous output, naturally supporting streaming. RNN-T is preferred for low-latency applications.

## Q52: What is external language model fusion?
**A:** External language model fusion combines a separately trained language model with the ASR decoder during inference. Shallow fusion adds LM scores during beam search. Deep fusion integrates the LM into the model architecture. Cold fusion initializes the LM component before training.

## Q53: How do you perform language identification with ASR?
**A:** Language identification can be done by: (1) a separate classifier using acoustic features (i-vectors, x-vectors, or embeddings from a pre-trained model), (2) a multilingual ASR model that outputs language tokens, or (3) a dedicated LID model before the ASR pipeline.

## Q54: What is the role of the encoder in a Transformer-based ASR model?
**A:** The encoder processes input audio features (log-mel spectrograms) through multiple self-attention and feed-forward layers, producing a sequence of hidden representations. These representations capture acoustic and phonetic information that the decoder uses to generate text.

## Q55: How do you reduce model size for on-device STT?
**A:** Techniques include: quantization (INT8, FP16), pruning (removing less important weights), knowledge distillation (training a smaller student model from a larger teacher), using efficient architectures (Conformers, depthwise separable convolutions), and weight sharing.

## Q56: What is knowledge distillation in the context of STT?
**A:** Knowledge distillation trains a smaller "student" model to mimic a larger "teacher" model's outputs. For ASR, the student learns from the teacher's soft probability distributions (logits) over tokens. This compresses the model significantly while retaining most of the teacher's accuracy.

## Q57: How does end-to-end ASR handle speaker adaptation?
**A:** End-to-end ASR can handle speaker adaptation through: (1) speaker embeddings (d-vectors, x-vectors) concatenated with encoder features, (2) feature-wise linear modulation (FiLM) layers, (3) adapter modules fine-tuned per speaker, or (4) training with speaker perturbation augmentation.

## Q58: What is the purpose of voice biometrics in STT systems?
**A:** Voice biometrics (speaker recognition) identifies or verifies a person based on their voice characteristics. In STT systems, it enables speaker identification for diarization, personalized models, and security (voice authentication). It is often implemented using speaker embedding extractors like ECAPA-TDNN.

## Q59: How do you handle overlapping speech in STT?
**A:** Overlapping speech (multiple speakers talking simultaneously) is very challenging. Solutions include: (1) permutation invariant training (PIT) that handles label permutation, (2) target-speaker extraction models, (3) multi-channel processing with beamforming, and (4) separating streams before ASR.

## Q60: What is Permutation Invariant Training (PIT)?
**A:** PIT is a training technique for multi-speaker ASR that computes the loss across all permutations of speaker-label assignments and picks the minimum. This solves the label permutation problem (not knowing which output corresponds to which speaker) during training.

## Q61: What are x-vectors and how are they used in speaker diarization?
**A:** x-vectors are fixed-dimensional speaker embeddings extracted from variable-length speech segments using a time-delay neural network (TDNN). They capture speaker identity characteristics and are used in clustering-based speaker diarization to group segments by speaker.

## Q62: What is the difference between chunk-based and non-chunk-based streaming ASR?
**A:** Chunk-based streaming ASR processes fixed-size audio chunks (e.g., 320ms) with a look-ahead context. Non-chunk-based methods process frames one at a time. Chunk-based methods offer better accuracy due to contextual information while maintaining low latency through chunk-level parallelism.

## Q63: What is causal convolution and why is it used in streaming ASR?
**A:** Causal convolution ensures that the output at time t depends only on inputs at times ≤ t (no future context). This is critical for streaming ASR to maintain causality. It is implemented by padding only to the left side of the input, allowing real-time processing without future leakage.

## Q64: How do you implement a real-time ASR pipeline?
**A:** A real-time pipeline consists of: (1) audio capture with a ring buffer, (2) VAD for speech/silence detection, (3) feature extraction (log-mel features), (4) streaming inference with a causal model (RNN-T or causal Conformer), (5) beam search or greedy decoding with LM fusion, (6) endpoint detection, (7) optional punctuation/ITN post-processing.

## Q65: What is the Word Piece model in ASR?
**A:** WordPiece is a subword tokenization algorithm (used in BERT, etc.) that splits words into common subword units based on likelihood. In ASR, it provides a vocabulary that balances between character and word levels, improving OOV handling and training efficiency.

## Q66: How do you handle numbers, dates, and times in ASR output?
**A:** The ASR model typically outputs spoken forms ("twenty twenty four"). Inverse Text Normalization (ITN) converts these to written forms ("2024"). ITN uses rule-based grammars (e.g., with Thrax, Pynini) or neural models for context-aware normalization.

## Q67: What is the role of self-attention in speech transformers?
**A:** Self-attention computes weighted representations of all positions in the input sequence, capturing long-range dependencies. In speech transformers, it models temporal relationships across the entire utterance, handling phenomena like coarticulation and prosody better than RNNs.

## Q68: How do you test an STT system for fairness?
**A:** Fairness testing involves: measuring WER across demographic groups (gender, accent, age, dialect), ensuring balanced representation in test sets, performing disaggregated evaluations, testing with adversarially selected inputs, and auditing for biased performance in specific use cases.

## Q69: What is the difference between monophone, triphone, and quinphone models?
**A:** Monophone models each phoneme independently. Triphone models capture left-right phoneme context (3 phonemes). Quinphone models capture two phonemes on each side (5 phonemes). Wider context better captures coarticulation but increases model complexity and data requirements.

## Q70: How do you implement custom commands in a wake-word system?
**A:** Custom commands are implemented by: (1) training a small-footprint model (e.g., with depthwise separable CNNs) to recognize specific phrases, (2) using a two-stage approach — wake-word detection triggers a larger ASR model for command recognition, or (3) keyword spotting with CTC.

## Q71: What is a conformer architecture?
**A:** A Conformer combines convolutional neural networks (CNNs) and Transformers for ASR. It adds a convolutional module between the self-attention and feed-forward modules in each encoder block. The convolution captures local patterns effectively while self-attention handles global context, achieving state-of-the-art accuracy.

## Q72: How does SpecAugment improve ASR model robustness?
**A:** SpecAugment randomly masks contiguous frequency bins (frequency masking) and time steps (time masking) in the spectrogram during training. This forces the model to rely on broader context and prevents overfitting to specific spectral or temporal patterns, improving generalization.

## Q73: What is the purpose of endpointing in conversational ASR?
**A:** Endpointing determines when a user has stopped speaking, triggering the final transcription and response generation. Good endpointing balances between cutting off the user too early (barge-in) and waiting too long (awkward pauses). It uses VAD, decoder confidence, and duration heuristics.

## Q74: How do you handle barge-in during voice interactions?
**A:** Barge-in allows a user to interrupt the system's response. The ASR system continuously listens even while the system is speaking. Acoustic echo cancellation removes the system's own speech from the microphone input. Barge-in detection triggers response interruption and new query processing.

## Q75: What is acoustic echo cancellation (AEC)?
**A:** AEC removes the echo of the system's own audio output from the microphone input. It uses adaptive filters to model the acoustic path between speaker and microphone, subtracting the estimated echo from the captured signal. AEC is critical for hands-free voice interaction systems.

## Q76: How do you train an ASR model from scratch?
**A:** Training from scratch requires: (1) large amounts of paired audio-text data (1000+ hours), (2) audio preprocessing (resampling, normalization), (3) feature extraction, (4) defining the model architecture (e.g., Conformer + RNN-T), (5) choosing a loss function (CTC or RNN-T loss), (6) training with distributed computing (multiple GPUs), and (7) evaluation and iteration.

## Q77: What is transfer learning for ASR?
**A:** Transfer learning pre-trains a model on a large dataset (e.g., LibriSpeech, Common Voice) and fine-tunes on a smaller target domain. This dramatically reduces the data needed for new domains/languages. Self-supervised pre-training (Wav2Vec 2.0, HuBERT) is a powerful form of transfer learning.

## Q78: What are the challenges of ASR for call center applications?
**A:** Challenges include: varying audio quality (landline, VoIP, mobile), background noise, overlapping speech, emotional speech, domain-specific terminology, long conversations, speaker diarization requirements, and strict latency requirements. Specialized models with noise robustness are typically needed.

## Q79: How do you perform real-time analytics on ASR transcripts?
**A:** Real-time analytics include: keyword spotting, sentiment analysis, intent detection, entity extraction, topic classification, compliance monitoring (flagging prohibited phrases), and agent performance scoring. These are typically applied as the transcript streams in, using lightweight NLP models.

## Q80: What is the difference between generative and discriminative models in ASR?
**A:** Generative models (e.g., HMM-GMM) model the joint probability P(audio, text) and use Bayes' rule for decoding. Discriminative models (e.g., neural networks) directly model P(text | audio). Modern end-to-end models are discriminative, achieving higher accuracy.

## Q81: How does beam width affect ASR performance?
**A:** Beam width controls the number of hypotheses maintained during beam search. A larger beam width increases the chance of finding the optimal transcription but requires more computation and memory. Typical values range from 4 to 20. The optimal width balances accuracy gains against latency.

## Q82: What is a look-ahead context in streaming ASR?
**A:** Look-ahead context allows the model to see a small number of future frames beyond the current time step. For example, 10ms of look-ahead helps the model make better predictions. It introduces minimal latency while significantly improving accuracy. Causal models may use right-context blocks.

## Q83: How do you handle very long audio recordings with ASR?
**A:** Long audio is handled by: (1) segmentation using VAD or fixed-length windows with overlap, (2) processing segments independently, (3) merging results with overlap handling. For non-streaming models, sliding window and overlap averaging improves consistency at segment boundaries.

## Q84: What is whisper.cpp?
**A:** whisper.cpp is a C++ implementation of OpenAI's Whisper model optimized for local/on-device inference. It supports CPU-only execution, quantization (GGML format), and various hardware backends. It enables privacy-preserving, offline STT on laptops, phones, and edge devices.

## Q85: How do you measure the quality of STT for subtitling?
**A:** Beyond WER, subtitling quality includes: latency (must be near real-time), reading speed (characters per second limits), synchronization accuracy (subtitle timing), punctuation quality, speaker tracking, and handling of multiple languages. Human evaluation with Mean Opinion Scores (MOS) is common.

## Q86: What is the difference between frame-level and sequence-level ASR training?
**A:** Frame-level training (cross-entropy with forced alignment) requires frame-label alignment, often using HMMs. Sequence-level training (CTC, RNN-T, and attention) optimizes directly for correct output sequences without explicit per-frame labels, simplifying training and often improving end-to-end accuracy.

## Q87: How do you implement ASR for streaming voice search?
**A:** Voice search requires: (1) wake-word detection, (2) streaming ASR with low first-word latency, (3) endpoint detection to know when the query is complete, (4) inverse text normalization, (5) query routing to search engine, and (6) returning results. Accuracy-speed trade-off favors speed.

## Q88: What is a neural transducer?
**A:** A neural transducer is an end-to-end ASR architecture that produces output tokens monotonically aligned with input frames. RNN-T is the most common neural transducer. It naturally handles streaming, variable-length input/output, and does not require attention over the full sequence.

## Q89: How do you handle emotion and tone in STT?
**A:** Standard STT does not capture emotion/tone. For emotion recognition, a separate model (speech emotion recognition, SER) analyzes prosodic features (pitch, energy, speaking rate) and spectral features. Multi-task learning can jointly predict text and emotion from speech.

## Q90: What is grapheme-based ASR?
**A:** Grapheme-based ASR predicts characters/letters directly instead of phonemes. It eliminates the need for a pronunciation dictionary and phoneme alignment. While simpler, it must handle irregular spelling (e.g., "enough" ≠ "enuff"). It works well with large amounts of data.

## Q91: What is best path decoding in CTC?
**A:** Best path decoding (greedy decoding) for CTC takes the most probable label at each time step, then collapses repeated non-blank labels and removes blank tokens. It is simple and fast but may miss the optimal sequence that beam search would find.

## Q92: How do you perform semi-supervised learning for ASR?
**A:** Semi-supervised learning uses unlabeled audio by generating pseudo-labels from a teacher model, then training on the combined labeled + pseudo-labeled data. Techniques like noisy student training, self-training with confidence filtering, and iterative refinement improve pseudo-label quality.

## Q93: What is noisy student training for ASR?
**A:** Noisy student training is a semi-supervised approach where: (1) a teacher ASR model generates pseudo-labels on unlabeled data, (2) a student model is trained on labeled + pseudo-labeled data with noise added (SpecAugment, dropout), (3) the student becomes the new teacher and repeats.

## Q94: How do you handle capitalization in ASR output?
**A:** Capitalization is handled through: (1) a truecasing model that predicts proper capitalization from lowercase text, (2) including capitalization in the ASR output vocabulary, or (3) using a post-processing model (often BERT-based) that restores correct casing.

## Q95: What is a Conformer and how does it differ from a standard Transformer?
**A:** A Conformer adds a convolutional module (typically using depthwise separable convolutions) between the self-attention and feed-forward modules in each encoder block. This captures local patterns better than standard Transformers while maintaining global context, leading to superior ASR accuracy.

## Q96: How do you deploy an ASR model on edge devices?
**A:** Deployment involves: converting the model to an optimized format (ONNX, TFLite, CoreML), quantization (FP16 or INT8), reducing model size via knowledge distillation, implementing streaming inference with a ring buffer, using hardware accelerators (NPU, DSP), and minimizing memory footprint.

## Q97: What is the role of data curation in building a good ASR system?
**A:** Data curation involves ensuring audio quality (SNR, sample rate), accurate transcriptions, diverse speaker representation (gender, accent, age), balanced domain coverage, proper punctuation, and removal of personally identifiable information (PII). Data diversity is often more important than quantity.

## Q98: How do you handle profanity filtering in ASR?
**A:** Profanity filtering can be done: (1) during post-processing with a profanity list and replacement/redaction, (2) by biasing the decoder away from profane words, or (3) using a classification model to flag inappropriate content. The approach depends on application requirements.

## Q99: What future trends are shaping STT technology?
**A:** Key trends include: large-scale multimodal models (audio + text + vision), real-time emotion and paralinguistic understanding, ultra-low-power on-device ASR for wearables, zero-shot cross-lingual transfer, personalized ASR with adaptation, and integration with LLMs for context-aware transcription.

## Q100: How would you design an STT system for a live lecture transcription service handling 10,000 concurrent users?
**A:** Design considerations: (1) distributed streaming ingestion with load balancers, (2) model servers with GPU/NPU inference, (3) WebSocket-based streaming for low latency, (4) geographic distribution for regional users, (5) auto-scaling based on concurrent stream count, (6) fault tolerance with replica models, (7) post-processing pipeline (punctuation, ITN) asynchronously, (8) storage for transcripts with timestamp alignment, (9) monitoring for WER, latency p95/p99, and (10) fallback to offline batch processing when streaming fails.
