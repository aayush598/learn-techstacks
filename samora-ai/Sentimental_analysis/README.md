# Sentiment Analysis Interview Questions and Answers

## Q1: What is sentiment analysis?
**A:** Sentiment analysis (also called opinion mining) is a Natural Language Processing technique that identifies, extracts, and quantifies the emotional tone, attitude, or opinion expressed in text. It classifies text as positive, negative, or neutral, and can detect more fine-grained emotions or sentiment intensity.

## Q2: What are the different levels of sentiment analysis?
**A:** 1) Document-level: assigns sentiment to the entire document. 2) Sentence-level: classifies the sentiment of each sentence. 3) Aspect-based: identifies sentiment toward specific entities/aspects mentioned (e.g., "The food was great but service was slow"). 4) Entity-level: sentiment toward a specific entity.

## Q3: What are the main approaches to sentiment analysis?
**A:** 1) Rule-based/Lexicon-based (VADER, TextBlob, SentiWordNet). 2) Machine learning (Naive Bayes, SVM, Logistic Regression with features like n-grams and TF-IDF). 3) Deep learning (LSTM, CNN, Transformer models like BERT, RoBERTa). 4) Hybrid approaches combining multiple methods.

## Q4: What is the difference between polarity and subjectivity in sentiment analysis?
**A:** Polarity measures the direction of sentiment (positive, negative, neutral) and often its intensity. Subjectivity measures whether text is factual (objective) or opinion-based (subjective). "The Earth orbits the Sun" is objective; "The sunset was beautiful" is subjective.

## Q5: What are the common challenges in sentiment analysis?
**A:** 1) Sarcasm and irony. 2) Negation handling ("not bad" is positive). 3) Context-dependency ("This is sick!" can be positive or negative). 4) Polysemy (words with multiple meanings). 5) Domain-dependent sentiment. 6) Emoji and slang. 7) Code-switching (multiple languages).

## Q6: How do you handle sarcasm in sentiment analysis?
**A:** Sarcasm detection requires understanding context beyond literal words. Approaches include: 1) Using contextual models like BERT that capture nuanced patterns. 2) Adding punctuation/emoticon features. 3) Contrast-based features (positive words in negative context). 4) Transformer models fine-tuned on sarcasm datasets.

## Q7: What is aspect-based sentiment analysis (ABSA)?
**A:** ABSA identifies sentiment toward specific aspects or features of an entity. For "The camera quality is amazing but the battery life is poor," ABSA identifies: camera quality -> positive, battery life -> negative. It involves two subtasks: aspect extraction and aspect sentiment classification.

## Q8: How does domain affect sentiment analysis?
**A:** The same word can have different sentiment across domains. "Unpredictable" is negative for a car but positive for a movie. "Sterile" is positive for a hospital but negative for a restaurant. Domain adaptation or domain-specific training is essential.

## Q9: What is the difference between fine-grained and coarse-grained sentiment?
**A:** Coarse-grained uses broad categories (positive, negative, neutral). Fine-grained uses more granular classes such as 5-point scales (1-5 stars) or specific emotions. Fine-grained provides more nuance but is harder to classify.

## Q10: What is emotion detection and how is it different from sentiment?
**A:** Emotion detection identifies specific emotions (joy, anger, sadness, fear, disgust, surprise) rather than just polarity. Sentiment is simpler (positive/negative), while emotion detection is more nuanced, often following models like Ekman's six basic emotions.

## Q11: What are the common datasets for sentiment analysis?
**A:** 1) IMDb Reviews (movie reviews, binary). 2) SST (Stanford Sentiment Treebank, fine-grained). 3) Amazon Reviews (1-5 stars). 4) SemEval Twitter datasets. 5) Yelp Reviews. 6) Sentiment140 (tweets). 7) GoEmotions (emotion classification). 8) Multi-Domain Sentiment Dataset.

## Q12: What is the Stanford Sentiment Treebank (SST)?
**A:** SST is a dataset of 11,855 movie review sentences with fine-grained sentiment labels (very negative, negative, neutral, positive, very positive). Each sentence is parsed into a binary tree with sentiment labels at every node, useful for compositional sentiment analysis.

## Q13: What is the difference between SST-1 and SST-2?
**A:** SST-1 has 5 classes: very negative, negative, neutral, positive, very positive. SST-2 is binary: it removes neutral and merges very negative/negative into negative, very positive/positive into positive.

## Q14: What is the SemEval sentiment analysis task?
**A:** SemEval (Semantic Evaluation) is a series of workshops with shared tasks including sentiment analysis. Notable tasks include SemEval-2014 Task 4 (ABSA), SemEval-2015 Task 12, and SemEval-2016 Task 5. They provide benchmark datasets and evaluation frameworks.

## Q15: What are evaluation metrics for sentiment analysis?
**A:** Common metrics: 1) Accuracy. 2) Precision, Recall, F1-score. 3) Macro-F1 (average F1 across classes). 4) Weighted-F1 (weighted by class support). 5) Confusion Matrix. 6) ROC-AUC for binary. 7) MAE and RMSE for fine-grained/regression.

## Q16: How do you handle class imbalance in sentiment analysis?
**A:** Techniques: 1) Resampling (oversample minority, undersample majority). 2) Weighted loss function. 3) Focal Loss (focus on hard examples). 4) Synthetic data generation (SMOTE, back-translation). 5) Ensemble methods. 6) Threshold tuning.

## Q17: What is the role of negation in sentiment analysis?
**A:** Negation flips sentiment polarity (e.g., "good" -> "not good" = negative). Approaches: 1) Negation scope detection. 2) Adding "NOT_" prefix to negated words. 3) Rule-based handling (like VADER). 4) Contextual models (BERT learns negation patterns). 5) Dependency parsing for negation scope.

## Q18: How do you handle negations like "not bad"?
**A:** "Not bad" expresses positive sentiment despite containing negative words. Approaches: 1) Lexicon-based: treat as negation + negative -> positive. 2) Machine learning: models learn "not bad" pattern correlates with positive. 3) BERT captures this from context. 4) N-gram features like "not_bad" bigram.

## Q19: What are n-grams and how are they used in sentiment analysis?
**A:** N-grams are contiguous sequences of n items (words or characters). Unigrams (n=1), bigrams (n=2), trigrams (n=3). In sentiment analysis, n-grams capture word patterns: "not good" (bigram) signals negative better than individual words.

## Q20: What is TF-IDF and how is it used in sentiment analysis?
**A:** TF-IDF (Term Frequency-Inverse Document Frequency) weights words by importance in a document relative to a corpus. It reduces the impact of common words and highlights distinctive words. Used as features for ML classifiers (SVM, Logistic Regression).

## Q21: What are word embeddings in sentiment analysis?
**A:** Word embeddings are dense vector representations of words capturing semantic meaning. Word2Vec, GloVe, and FastText generate static embeddings. Contextual embeddings (BERT, ELMo) produce different vectors based on context, improving sentiment analysis.

## Q22: What is the difference between static and contextual embeddings?
**A:** Static embeddings (Word2Vec, GloVe) produce the same vector regardless of context - "bank" in "river bank" and "money bank" have the same vector. Contextual embeddings (BERT, ELMo) produce different vectors based on surrounding words, capturing polysemy.

## Q23: How do you perform sentiment analysis on social media text?
**A:** Social media has unique challenges: slang, hashtags, emoji, irregular grammar. Approaches: 1) Use VADER (designed for social media). 2) Fine-tune BERT on social media data (BERTweet). 3) Preprocess: normalize slang, handle URLs/mentions. 4) Emoji sentiment mapping.

## Q24: What is BERTweet?
**A:** BERTweet is a pre-trained language model for English tweets based on RoBERTa, trained on 850 million tweets. It outperforms general BERT on social media NLP tasks including sentiment analysis due to domain-specific training.

## Q25: How do you handle emoji in sentiment analysis?
**A:** Approaches: 1) Emoji sentiment lexicons (mapping emojis to scores). 2) Convert emoji to text descriptions or special tokens. 3) Keep emoji as unicode and let the model learn embeddings. 4) Use pre-trained models that saw emoji during training.

## Q26: What is the role of hashtags in sentiment analysis?
**A:** Hashtags (#happy, #fail) often explicitly express sentiment. Approaches: 1) Extract sentiment from hashtag words. 2) Segment hashtags (#HavingABadDay -> "having a bad day"). 3) Use hashtags as features or labels.

## Q27: How do you build a real-time sentiment analysis system?
**A:** Architecture: 1) Data ingestion (Kafka, Kinesis). 2) Preprocessing pipeline (Flink, Spark Streaming). 3) Sentiment model (VADER for speed, optimized BERT for accuracy). 4) Storage (Elasticsearch). 5) Visualization (Grafana, Kibana). 6) Alerting on negative sentiment spikes.

## Q28: What is the difference between batch and streaming sentiment analysis?
**A:** Batch analysis processes large volumes of historical data at scheduled intervals (e.g., daily review analysis). Streaming analysis processes data in real-time as it arrives (e.g., monitoring social media). Streaming requires low-latency and fault-tolerant architecture.

## Q29: How do you handle multilingual sentiment analysis?
**A:** Approaches: 1) Multilingual models (mBERT, XLM-RoBERTa). 2) Translate to English then analyze (introduces errors). 3) Language-specific models. 4) Cross-lingual zero-shot transfer. 5) Character-level models that work across languages.

## Q30: What is cross-lingual sentiment analysis?
**A:** Cross-lingual sentiment analysis trains on one language (source) and applies to another (target) without target-language training data. Achieved through: 1) Multilingual BERT (shared embedding space). 2) Adapter-based approaches. 3) Machine translation + sentiment. 4) Zero-shot transfer.

## Q31: What is zero-shot sentiment analysis?
**A:** Zero-shot sentiment analysis classifies sentiment for classes unseen during training. Using models like BART or T5, you can formulate it as a natural language inference task. Hugging Face's pipeline supports zero-shot classification natively.

## Q32: What is few-shot sentiment analysis?
**A:** Few-shot learning trains with very few labeled examples (e.g., 5-50 per class). Approaches: 1) Fine-tune pre-trained model with strong regularization. 2) Pattern-exploiting training (PET). 3) In-context learning with LLMs (GPT-3, Llama). 4) SetFit (efficient few-shot fine-tuning).

## Q33: What is SetFit?
**A:** SetFit (Sentence Transformer Fine-tuning) is an efficient few-shot learning method for text classification. It uses sentence transformers to generate embeddings and trains a classifier head with contrastive learning, achieving high accuracy with as few as 8-64 examples per class.

## Q34: What is in-context learning for sentiment analysis?
**A:** In-context learning uses large language models by providing examples in the prompt. For example: "Classify as positive, negative, or neutral: 'I love this product' -> Positive". The model infers the task from examples without weight updates.

## Q35: What is the difference between generative and discriminative approaches?
**A:** Generative approaches model joint probability of text and sentiment (can generate text). Discriminative approaches model conditional probability of sentiment given text (classify only). Most sentiment models (BERT, SVM) are discriminative. GPT models are generative.

## Q36: What is supervised sentiment analysis?
**A:** Supervised sentiment analysis trains a model on a labeled dataset where each text has an associated sentiment label. The model learns patterns correlating with labels. Requires sufficient labeled data but achieves the highest accuracy.

## Q37: What is unsupervised sentiment analysis?
**A:** Unsupervised sentiment analysis uses no labeled data. Approaches: 1) Lexicon-based (VADER, SentiWordNet). 2) Embedding clustering (infer sentiment from cluster characteristics). 3) Rule-based patterns. Less accurate but requires no training data.

## Q38: What is semi-supervised sentiment analysis?
**A:** Semi-supervised learning uses a small labeled dataset and a large unlabeled dataset. The model is trained on labeled data, then pseudo-labels unlabeled data iteratively. Self-training and co-training are common approaches.

## Q39: What is weak supervision in sentiment analysis?
**A:** Weak supervision uses heuristic rules or distant supervision to generate noisy labels automatically. For example, using star ratings as sentiment labels. Snorkel combines multiple noisy label sources into probabilistic training labels.

## Q40: How do you perform distant supervision for sentiment?
**A:** Distant supervision uses existing data as noisy labels: 1) Emoticons in tweets (:)=positive, :(=negative). 2) Star ratings as labels. 3) Hashtags (#happy, #angry). Labels are noisy but allow training without manual annotation.

## Q41: What is the role of preprocessing in sentiment analysis?
**A:** Steps include: lowercasing, removing HTML/URLs, expanding contractions, punctuation handling, stemming/lemmatization, stop word removal, spell correction. The right preprocessing depends on the approach. Over-processing can harm VADER but help traditional ML.

## Q42: What is the impact of stop word removal?
**A:** Stop word removal can harm sentiment analysis because: 1) Negation words ("not", "no") are stop words but crucial. 2) Intensifiers ("very", "extremely") are short but significant. 3) Sentiment words can be short ("good", "bad"). Keep stop words or remove selectively.

## Q43: What is stemming and lemmatization in sentiment analysis?
**A:** Stemming removes suffixes ("running" -> "run"). Lemmatization returns dictionary form ("better" -> "good"). Lemmatization is more accurate but slower. Both reduce sparsity in traditional ML. Not needed for BERT (uses subword tokenization).

## Q44: What are sentiment lexicons?
**A:** Sentiment lexicons map words to sentiment scores/classes. Examples: 1) VADER lexicon (social media). 2) AFINN (-5 to +5). 3) SentiWordNet (WordNet synsets). 4) MPQA Subjectivity Lexicon. 5) Bing Liu Opinion Lexicon. 6) Loughran-McDonald (financial).

## Q45: What is SentiWordNet?
**A:** SentiWordNet assigns each WordNet synset three scores: positivity, negativity, and objectivity (summing to 1). Covers over 117,000 synsets. Used for lexicon-based sentiment analysis, especially when no domain-specific lexicon is available.

## Q46: What is the difference between SentiWordNet and VADER?
**A:** SentiWordNet covers more words (117K synsets) but is not domain-optimized. VADER has fewer words (~7,500) but is specifically tuned for social media with heuristics for intensifiers, negation, and emoticons. VADER outperforms on informal text.

## Q47: How do you handle code-mixed text (Hinglish, Spanglish)?
**A:** Approaches: 1) Normalize each language variant. 2) Character-level models (handle unknown words). 3) Multilingual BERT. 4) Train on code-mixed datasets. 5) Transliteration. 6) Specialized models like HingBERT.

## Q48: What is HingBERT?
**A:** HingBERT is a BERT model trained on Hinglish (Hindi-English code-mixed text). It handles unique patterns of code-mixed text and outperforms multilingual BERT on Hinglish NLP tasks including sentiment analysis.

## Q49: How do you handle sentiment analysis for long documents?
**A:** Challenges: model input limits, varying sentiment across sections. Approaches: 1) Truncation (keep most relevant part). 2) Sentence-level with aggregation (average, majority vote). 3) Hierarchical models (encode sentences, then document). 4) Longformer/BigBird (long-context).

## Q50: How do you handle sentiment analysis for customer reviews?
**A:** For product/service reviews: 1) Aspect-based sentiment analysis per feature. 2) Handle comparative statements. 3) Handle hyperbole and review-specific language. 4) Detect fake/spam reviews. 5) Temporal sentiment trends. 6) Combine with ratings.

## Q51: What is opinion summarization?
**A:** Opinion summarization generates a concise summary of sentiments from multiple reviews. It identifies key aspects and associated sentiment distribution. Example: "80% of reviews praise battery life, 60% complain about camera quality."

## Q52: How do you detect fake reviews?
**A:** Approaches: 1) Anomaly detection in sentiment patterns. 2) Review metadata analysis (timing, user behavior). 3) Text patterns (repetition, generic language). 4) Sentiment vs rating inconsistency. 5) Stylometric analysis. 6) Graph-based methods.

## Q53: What is the relationship between sentiment analysis and opinion mining?
**A:** Often used interchangeably. Opinion mining is broader: it includes sentiment analysis plus opinion holder identification, target extraction, and opinion summarization.

## Q54: What is opinion target extraction?
**A:** Identifying the specific entity or aspect being evaluated. In "The battery life is amazing," the target is "battery life." Approached as sequence labeling (NER-like) task.

## Q55: What is the role of dependency parsing in sentiment analysis?
**A:** Dependency parsing reveals grammatical relationships, helping identify: 1) Word modifications ("very" modifies "good"). 2) Negation scope. 3) Relations between opinion words and targets. 4) Long-distance dependencies.

## Q56: What is a dependency tree-based sentiment model?
**A:** Models using dependency trees to capture sentiment flow. Tree-LSTM applies recurrent networks over dependency trees, propagating sentiment from words to parents, capturing composition (e.g., "not" flips child's sentiment).

## Q57: What are attention mechanisms in sentiment analysis?
**A:** Attention allows the model to focus on relevant input parts when predicting. It learns to give higher weight to sentiment-bearing words. Self-attention (in BERT) captures relationships between all token pairs.

## Q58: What is aspect-level attention?
**A:** Aspect-level attention focuses on text segments relevant to a specific aspect. For "The food was great but service was slow," different attention is assigned to "great" for food sentiment and "slow" for service sentiment.

## Q59: What is the difference between global and local attention?
**A:** Global attention considers all input tokens. Local attention focuses on positions near a target. Local attention is more efficient for aspect-based sentiment where local context is most relevant.

## Q60: How do traditional ML and deep learning compare for sentiment?
**A:** Traditional ML (SVM, NB, with TF-IDF): fast, interpretable, works with small data, limited accuracy. Deep learning (LSTM, BERT): higher accuracy, handles context and nuance, requires more data and compute. BERT now dominates benchmarks.

## Q61: What are advantages of transformer models for sentiment?
**A:** 1) Bidirectional context. 2) Pre-trained on massive text. 3) Transfer learning (fine-tune with moderate data). 4) Self-attention captures long-range dependencies. 5) State-of-the-art on most benchmarks.

## Q62: What is the performance of different models on benchmarks?
**A:** On SST-2: Logistic Regression ~82%, LSTM ~87%, ELMo ~90%, BERT-base ~93%, BERT-large ~94.5%, RoBERTa-large ~96.4%. On SST-5: BERT-base ~54%, RoBERTa-large ~57%.

## Q63: How do you choose between simple and complex models?
**A:** Consider: 1) Data size: small -> simpler or few-shot. 2) Latency: real-time -> VADER, distilled BERT. 3) Accuracy: high stakes -> BERT-level. 4) Resources: limited -> VADER, abundant -> BERT.

## Q64: What is the cold start problem?
**A:** The cold start problem occurs when launching sentiment analysis for a new domain without labeled data. Solutions: 1) Pre-trained models/lexicons (zero-shot). 2) Transfer learning. 3) Active learning. 4) Weak supervision with heuristics.

## Q65: What is active learning for sentiment analysis?
**A:** Active learning reduces labeling effort by selecting the most informative examples for annotation. Strategies: 1) Uncertainty sampling. 2) Diversity sampling. 3) Query-by-committee. Significantly reduces labeled data needed.

## Q66: How do you handle temporal drift?
**A:** Language evolves over time. Mitigation: 1) Regular retraining on recent data. 2) Online learning. 3) Monitor performance drift. 4) Maintain up-to-date lexicons. 5) Use recently pre-trained models.

## Q67: What is data drift in sentiment analysis?
**A:** Data drift occurs when input data distribution changes, degrading performance. Examples: new slang emerges, new products discussed. Monitor by comparing current data statistics with training data; retrain when drift is detected.

## Q68: What is concept drift in sentiment analysis?
**A:** Concept drift occurs when the relationship between features and sentiment changes. "Sick" meant negative but became positive slang. Requires model retraining or adaptation.

## Q69: How do you deploy a sentiment analysis model?
**A:** Options: 1) REST API (FastAPI, Flask). 2) Batch pipeline (Spark). 3) Edge deployment (TensorFlow Lite). 4) Serverless (Lambda). 5) ML serving (SageMaker, TorchServe). 6) Optimized models (quantization, ONNX) for production.

## Q70: How do you handle sentiment analysis at scale?
**A:** Strategies: 1) Distributed processing (Spark). 2) Load balancing. 3) Caching results. 4) Asynchronous processing (queues). 5) Model optimization (distillation, quantization). 6) Tiered models (fast filter + accurate model).

## Q71: What is the role of confidence scores?
**A:** Confidence scores indicate prediction certainty. Uses: 1) Filter low-confidence predictions for human review. 2) Calibrate model. 3) Build reject options. 4) Weighted aggregation. 5) Uncertainty estimation.

## Q72: How do you calibrate probabilities?
**A:** Methods: 1) Platt scaling (logistic regression on outputs). 2) Isotonic regression. 3) Temperature scaling (softmax parameter). 4) Histogram binning. BERT models benefit from calibration as they tend to be overconfident.

## Q73: What is model ensembling for sentiment?
**A:** Ensembling combines multiple models. Approaches: 1) Voting (majority). 2) Weighted averaging. 3) Stacking (meta-model). 4) Bagging. 5) Boosting. Ensembles reduce variance and improve robustness.

## Q74: How do you perform error analysis?
**A:** Steps: 1) Build confusion matrix. 2) Analyze misclassified examples for patterns (sarcasm, negation). 3) Slice analysis by length, domain, intensity. 4) Identify systematic errors. 5) Use explainability tools.

## Q75: What is slice-based evaluation?
**A:** Measures performance across data subgroups (slices) to identify bias. Slices: text length, product category, demographic group, language variant. A model may perform well overall but poorly on a critical slice.

## Q76: What is gender bias in sentiment models?
**A:** Models can learn gender biases from training data (e.g., associating "nurse" with female sentiment differently). Mitigation: 1) Balanced data. 2) Counterfactual augmentation. 3) Debiasing embeddings. 4) Adversarial debiasing. 5) Fairness evaluation.

## Q77: How do you audit for bias?
**A:** Steps: 1) Evaluation datasets with protected attributes. 2) Measure performance disparities. 3) Counterfactual testing (swap gender/race terms). 4) Analyze false positive/negative rates across groups. 5) Report and mitigate disparities.

## Q78: What is the GDPR impact on sentiment analysis?
**A:** GDPR affects processing of personal data. Requirements: 1) Legal basis for processing. 2) Data minimization. 3) Right to explanation (automated decisions). 4) Data subject rights. 5) Anonymization/pseudonymization.

## Q79: How do you handle privacy in sentiment analysis?
**A:** Measures: 1) Anonymize personal information. 2) Differential privacy. 3) On-device processing. 4) Data retention policies. 5) Consent management. 6) Federated learning.

## Q80: What is federated learning for sentiment?
**A:** Federated learning trains models across decentralized devices without raw data leaving the device. Model updates (gradients) are aggregated centrally. Useful for privacy-sensitive applications (personal messages).

## Q81: How do you handle financial sentiment analysis?
**A:** Challenges: domain-specific terms, regulatory language, numerical data. Approaches: 1) FinBERT (pre-trained on financial text). 2) Loughran-McDonald dictionary. 3) Incorporate numerical data. 4) Handle earnings calls, SEC filings.

## Q82: What is FinBERT?
**A:** FinBERT is pre-trained on financial text (SEC filings, earnings reports) and fine-tuned for financial sentiment. It outperforms general BERT on financial tasks, handling terms like "bearish," "volatility," "EPS."

## Q83: How do you handle healthcare sentiment?
**A:** Healthcare involves medical terminology and patient narratives. Approaches: 1) BioBERT/PubMedBERT. 2) Handle negation carefully (critical in medical). 3) Address HIPAA/privacy. 4) Analyze patient feedback, clinical notes.

## Q84: How do you handle legal document sentiment?
**A:** Legal text has complex language and nuanced tone. Approaches: 1) Legal-BERT. 2) Hierarchical approaches for long documents. 3) Aspect-based analysis. 4) Fine-grained sentiment for subtle tones.

## Q85: What is aspect-category sentiment analysis?
**A:** Predicts sentiment toward predefined aspect categories (food, service, ambiance, price) rather than extracting specific terms. The model predicts sentiment for each category present.

## Q86: What is targeted sentiment analysis?
**A:** Identifies sentiment toward a specific target entity. "Apple's new iPhone is amazing but customer service is terrible" -> iPhone: positive, customer service: negative.

## Q87: How do you handle comparative sentences?
**A:** Comparative sentences compare entities ("X is better than Y"). Approaches: 1) Identify comparative structure via dependency parsing. 2) Extract comparative preference. 3) Separate into two sentiment statements.

## Q88: What is conditional sentiment analysis?
**A:** Handles sentiment dependent on conditions. "If the battery lasted longer, it would be perfect" expresses conditional negative sentiment about current battery. Requires understanding hypotheticals.

## Q89: How do you handle low-resource languages?
**A:** Approaches: 1) Cross-lingual transfer (mBERT, XLM-R). 2) Zero-shot. 3) Data augmentation (back-translation). 4) Lexicon translation. 5) Active learning. 6) Character-level models.

## Q90: What is the role of data annotation?
**A:** High-quality annotation is critical for supervised models. Best practices: 1) Clear guidelines with examples. 2) Multiple annotators. 3) Calculate inter-annotator agreement. 4) Resolve disagreements. 5) Ongoing quality checks.

## Q91: What is inter-annotator agreement?
**A:** Measures how consistently annotators label data. Cohen's kappa (2 annotators) or Fleiss' kappa (3+) corrects for chance agreement. >0.8 is strong, 0.6-0.8 moderate. Low agreement indicates ambiguous task.

## Q92: How do you handle ambiguous or neutral texts?
**A:** Neutral texts are challenging. Approaches: 1) Include neutral as a class. 2) Confidence thresholding (classify only high-confidence). 3) Multi-label (both positive and negative). 4) Regression output.

## Q93: How do you handle sentiment intensity?
**A:** Intensity measures how strong the sentiment is. Approaches: 1) Fine-grained classification (1-5 stars). 2) Regression (continuous score). 3) Ordinal regression (preserves order). 4) VADER compound score (normalized -1 to +1).

## Q94: What is multimodal sentiment analysis?
**A:** Combines text with other modalities (audio, video, images) for richer sentiment understanding. For example, analyzing facial expressions, tone of voice, and text together. Models like MERT and Video-Audio-Text transformers.

## Q95: What is aspect extraction in ABSA?
**A:** Aspect extraction identifies specific aspects/features mentioned. Approaches: 1) Rule-based (dependency patterns). 2) Sequence labeling (NER-like with BIO tagging). 3) BERT-based (fine-tune token classification). 4) Joint extraction and classification.

## Q96: What are end-to-end ABSA models?
**A:** End-to-end ABSA simultaneously extracts aspects and predicts sentiment without separate pipeline stages. Models like BERT-ABSA, Span-ASTE use unified architectures. Reduces error propagation from pipeline approaches.

## Q97: How do you handle sentiment in conversational AI?
**A:** In chatbots and voice assistants: 1) Real-time sentiment tracking across turns. 2) Context from conversation history. 3) Handle mixed sentiments within turns. 4) Respond empathetically based on detected sentiment. 5) Transfer learning from general sentiment to conversational.

## Q98: What is sentiment-aware recommendation?
**A:** Combines sentiment analysis with recommendation systems. Instead of just using ratings, sentiment from review text provides richer signals about user preferences. Improves recommendation quality by understanding why users like/dislike items.

## Q99: How do you evaluate a deployed sentiment model?
**A:** Ongoing evaluation: 1) Track production metrics (distribution of predictions, confidence scores). 2) Human evaluation on random samples. 3) A/B testing with model updates. 4) Monitor for drift. 5) Collect user feedback. 6) Golden dataset for regression testing.

## Q100: What are the future trends in sentiment analysis?
**A:** 1) Large language models (GPT-4, Llama) for nuanced understanding. 2) Multimodal sentiment (text + audio + video). 3) Few-shot and zero-shot (reduce annotation needs). 4) Explainable sentiment (LLMs can explain reasoning). 5) Real-time on-device processing. 6) Personalized sentiment (adapt to user expression patterns). 7) Ethical and responsible sentiment AI.
