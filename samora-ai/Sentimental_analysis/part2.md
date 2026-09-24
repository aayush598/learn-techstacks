# Sentiment Analysis Interview Questions and Answers - Part 2

## Q1: How do you implement aspect-based sentiment analysis with span extraction?
**A:** Span-based ABSA jointly extracts aspect spans and classifies sentiment. Architecture: 1) BERT encodes input text. 2) Two classifiers per token pair: start (token i is aspect start), end (token j is aspect end). 3) For each candidate span, predict sentiment (positive/negative/neutral). 4) Loss = span_loss + sentiment_loss. 5) Decoding: find valid spans (j >= i, max span length) with highest sentiment scores. Benefits: 1) End-to-end (no separate aspect extraction + classification). 2) Handles overlapping aspects. 3) State-of-the-art on SemEval ABSA benchmarks (90%+ F1). Models: Span-ASTE, BERT-Span. The key advantage is the joint modeling: aspect extraction informs sentiment classification and vice versa.
**Code:**
```python
import torch
bert_out = torch.randn(4, 768)
start_logits = torch.nn.Linear(768, 1)(bert_out).squeeze(1)
end_logits = torch.nn.Linear(768, 1)(bert_out).squeeze(1)
s, e = start_logits.argmax().item(), end_logits.argmax().item()
print("candidate aspect span:", s, "->", e, "| valid:", e >= s)
```

## Q2: How does emotion detection using Plutchik's wheel differ from Ekman's basic emotions for sentiment analysis?
**A:** Ekman: 6 basic emotions (joy, sadness, anger, fear, surprise, disgust). Discrete, universal. Plutchik: 8 primary emotions with intensity levels and combinations. 4 pairs of opposites (joy-sadness, anger-fear, trust-disgust, anticipation-surprise). Combinations produce complex emotions (joy + trust = love, anger + disgust = contempt). For sentiment analysis: Plutchik's model allows 1) More nuanced emotion detection (24+ emotions). 2) Intensity scoring. 3) Mixed emotions (multiple simultaneous). 4) Emotion dynamics (how emotions evolve). Implementation: BERT with 24-output head (sigmoid for multi-label). Datasets: GoEmotions (27 categories, Ekman-based), EmoInt (intensity). Plutchik-based models are less common but provide richer analysis. For production: Ekman's 6 + neutral is typically sufficient.
**Code:**
```python
import torch
logits = torch.sigmoid(torch.randn(8))  # 8 Plutchik primaries
emotions = ["joy", "sadness", "anger", "fear", "trust",
            "disgust", "anticipation", "surprise"]
print({e: round(float(p), 2) for e, p in zip(emotions, logits)})
```

## Q3: How do you handle multilingual sentiment analysis using translate-train vs translate-test?
**A:** Two approaches: 1) Translate-train: translate labeled training data from source language (e.g., English) to target languages. Train a single model on all languages. 2) Translate-test: translate target text to English at inference, run English sentiment model. Compare: 1) Translate-train is cheaper at inference (no translation). 2) Translate-test preserves original text (translation may lose sentiment nuance). 3) Translate-train captures language-specific patterns. 4) Translate-test errors compound (translation + sentiment errors). Performance: 1) Translate-train typically outperforms translate-test by 2-5% F1. 2) Best: use mBERT/XLM-R trained on multilingual data (translate-train) for highest accuracy. 3) For low-resource languages: translate-test with a good translation model is better than no training data.
**Code:**
```python
from transformers import MarianMTModel, MarianTokenizer
tok = MarianTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-hi")
model = MarianMTModel.from_pretrained("Helsinki-NLP/opus-mt-en-hi")
enc = tok("The food was amazing", return_tensors="pt")
hi = tok.decode(model.generate(**enc)[0], skip_special_tokens=True)
print("translated training example:", hi)
print("translate-train: label -> translated train data;",
      "translate-test: translate at inference")
```

## Q4: What are the key datasets for sarcasm detection and what makes them challenging?
**A:** Key sarcasm datasets: 1) iSarcasm (950 tweets, labeled sarcastic/not). 2) SARC (1.3M Reddit comments, sarcastic/not). 3) Headlines (30K news headlines). 4) MUSTARD (Russian-English code-mixed sarcasm). Challenges: 1) Sarcasm is highly contextual (requires understanding beyond literal words). 2) Labeling is subjective (low inter-annotator agreement, ~0.6 kappa). 3) Datasets are often domain-specific (Reddit sarcasm differs from Twitter sarcasm). 4) Heavy reliance on world knowledge. 5) Sarcasm often uses positive words in negative contexts (a key signal). BERT-based sarcasm detectors use: 1) Contextual embedding (previous turns). 2) Contrastive features (positive words + negative context). 3) Emoji/punctuation cues. Best accuracy: ~85% F1 (vs ~55% for humans on some datasets, showing it's genuinely hard).
**Code:**
```python
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()
text = "Great, another 2am outage. Just fantastic!"
print("literal lexicon score:", round(sia.polarity_scores(text)["compound"], 2))
print("sarcasm signal: positive words in a negative context")
```

## Q5: How do you implement fine-grained sentiment (1-5 stars) regression vs classification?
**A:** Two approaches: 1) Classification: 5-class softmax. Treats classes as independent (no ordinal relationship). 2) Regression: predict continuous score (1.0-5.0). Uses MSE loss. Captures ordinal relationship. 3) Ordinal regression: predict cumulative distribution (P(score >= k)). Best of both. Compare: 1) Classification: better accuracy on exact match, but no ordering information. 2) Regression: better correlation with true score, penalizes near-misses less (predicts 4.0 for true 5.0 is better than predicting 1.0). 3) Ordinal regression: best for fine-grained (cumulative link model). BERT for fine-grained: 1) Classification: 5-class head, cross-entropy loss. 2) Regression: single linear head, MSE loss, output clamped to [1,5]. 3) Ordinal: 4 binary classifiers (score >= 2, >= 3, >= 4, >= 5). Product of probabilities = expected score. For product reviews: regression typically gives better MAE and Spearman correlation.
**Code:**
```python
import torch
hidden = torch.randn(2, 768)
cls_head = torch.softmax(torch.nn.Linear(768, 5)(hidden), dim=1)   # 5-class
reg_head = torch.clamp(torch.nn.Linear(768, 1)(hidden), 1, 5)      # regression
print("classification:", cls_head.argmax(dim=1).tolist())
print("regression   :", reg_head.squeeze().round().tolist())
```

## Q6: How do Transformer-based models (BERT) compare to LSTMs for aspect-based sentiment?
**A:** BERT vs LSTM for ABSA: 1) BERT: bidirectional context, pre-trained knowledge, 512-token limit, O(n^2) attention. 2) LSTM: sequential, no pre-training (or Elmo), unlimited length, O(n) compute. Performance: BERT-base: ~92% F1 on SemEval-2014 Restaurant ABSA. BiLSTM + attention: ~85% F1. BERT wins by ~7% absolute. Reasons: 1) BERT's pre-training understands sentiment-related patterns. 2) BERT's bidirectional attention captures long-range aspect-context dependencies. 3) LSTM's hidden state bottleneck loses information. When LSTM can be preferred: 1) Very long documents (>512 tokens). 2) Resource-constrained deployment (no GPU). 3) Need for streaming input processing. LSTM with ELMo embeddings still competitive on some domains. But for most ABSA, BERT is the clear winner.
**Code:**
```python
from transformers import AutoTokenizer
tok = AutoTokenizer.from_pretrained("bert-base-uncased")
ids = tok("The battery life is amazing but the phone is heavy.",
          max_length=512, truncation=True)["input_ids"]
print("BERT: 512-token limit, used", len(ids))
print("LSTM: unlimited length, O(n) compute, no pre-training by default")
```

## Q7: How do you handle negation scope detection in sentiment analysis?
**A:** Negation scope: determining which words are negated. "I didn't think the movie was [good]." Negation scope = "good". Approaches: 1) Rule-based: negation cue + all words until punctuation/conjunction. 2) BERT-based: token-level classification (B-NEG, I-NEG, O). 3) Dependency-based: negation cue connects to negated words via dependency relations. 4) Hybrid: BERT for cue detection, dependency for scope propagation. BERT-based: 1) Tokenize input. 2) BERT encodes. 3) CRF layer predicts BIO tags for negation scope. 4) Sentiment classifier uses scope-aware features: add `NEGATED_` prefix to negated word embeddings. Results: BERT + CRF achieves ~92% F1 on negation scope detection (BioScope, SFU Review datasets). Incorporating scope detection improves sentiment accuracy by 2-3% on negated sentences.
**Code:**
```python
tokens = ["I", "did", "not", "think", "the", "movie", "was", "good"]
scope = ["O", "O", "B-NEG", "I-NEG", "O", "O", "O", "I-NEG"]
def neg_aware(tokens, scope):
    return [("NEG_" + t if s.endswith("NEG") else t) for t, s in zip(tokens, scope)]
print(neg_aware(tokens, scope))
```

## Q8: How do you implement cross-domain sentiment analysis without target domain labels?
**A:** Unsupervised domain adaptation: 1) Adversarial domain adaptation: train BERT feature extractor that is domain-invariant (adversarial loss: domain classifier tries to predict domain, feature extractor tries to fool it). 2) Self-training: predict on target domain with high confidence, use as pseudo-labels. 3) Domain-adversarial neural network (DANN): gradient reversal layer. 4) Contrastive adaptation: pull same-sentiment examples together across domains, push different-sentiment apart. 5) Alignment: align source and target sentence embedding distributions (CORAL, MMD). Results: BERT with adversarial adaptation achieves ~85-90% of in-domain performance on cross-domain sentiment. Best for: source domain has abundant labels (e.g., product reviews), target domain has no labels (e.g., financial news). Without adaptation: BERT drops 10-15% F1 on new domain. With adaptation: drop is 3-5%.
**Code:**
```python
import torch
class GradReverse(torch.autograd.Function):
    @staticmethod
    def forward(ctx, x): return x
    @staticmethod
    def backward(ctx, g): return -g
feats = torch.randn(4, 768)
dom = torch.nn.functional.binary_cross_entropy_with_logits(
    torch.nn.Linear(768, 1)(GradReverse.apply(feats)).squeeze(),
    torch.tensor([0., 0., 1., 1.]))
print("adversarial domain loss:", round(float(dom), 3))
```

## Q9: How do you implement sentiment analysis with chain-of-thought prompting using LLMs?
**A:** Chain-of-thought (CoT) for sentiment: 1) Provide few-shot examples with reasoning steps. 2) Prompt template: "Text: 'The food was amazing but the service was terrible.' Step 1: Identify aspects: food, service. Step 2: Determine sentiment for each: food=positive, service=negative. Step 3: Overall sentiment: mixed, leaning negative (service matters more)." 3) LLM generates reasoning steps, then final answer. Benefits: 1) More accurate (2-5% improvement over direct prompting). 2) Provides explanation. 3) Handles complex cases (mixed sentiment, sarcasm, comparisons). Tradeoffs: 1) Higher latency (more tokens generated). 2) Higher cost (5-10x more tokens per request). 3) Reasoning may be incorrect (hallucination). For production: use CoT only for challenging cases (flagged by fast model/rule). Simpler cases use direct classification.
**Code:**
```python
import openai
client = openai.OpenAI()
r = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user",
               "content": "Text: 'The food was amazing but the service was terrible.' "
                          "Step 1: find the aspects. Step 2: sentiment per aspect. "
                          "Step 3: overall verdict."}])
print(r.choices[0].message.content)
```

## Q10: How do you handle sentiment analysis on code-mixed social media text (Hinglish, Spanglish)?
**A:** Code-mixed text challenges: 1) Multiple languages in one sentence. 2) Romanized text (Hindi written in Latin script). 3) Switching within words ("timepass" = time + waste). Approaches: 1) Multilingual BERT (mBERT, XLM-R) - handles code-mixed tokens naturally. 2) HingBERT: BERT pre-trained on Hinglish text. 3) Transliteration: normalize Romanized Hindi to Devanagari or a standard form. 4) Language identification per token + per-language sentiment. 5) Character-level: bypasses tokenization issues. 6) Data augmentation: code-mix parallel sentences. Performance: 1) XLM-R: ~75% F1 on Hinglish sentiment. 2) HingBERT: ~80% F1. 3) VADER (English-only): ~55%. Best practice: fine-tune XLM-R on code-mixed data. HingBERT is better for Hindi-English. For Spanish-English: use Spanglish-specific models or mBERT.
**Code:**
```python
from transformers import pipeline
clf = pipeline("zero-shot-classification", model="joeddav/xlm-roberta-large-xnli")
print(clf("ye phone ka battery bahut solid hai",
          candidate_labels=["positive", "negative", "neutral"])["labels"][0])
```

## Q11: How do you implement attention-based aspect extraction for ABSA?
**A:** Attention-based aspect extraction: 1) BERT encodes input text. 2) Aspect attention layer: learns which tokens are aspects. 3) Multi-head attention over BERT outputs: each head captures different aspect types. 4) Linear + CRF for BIO tagging. Alternative: 1) BERT + attention pooling: compute attention weights over tokens, weighted sum = aspect representation. 2) Aspect embedding: randomly initialized, learned during training. Key insight: attention weights show which tokens correspond to aspect terms. For "The food was great but service was slow": attention to "food" and "service" should have high weights. Advantages: 1) Interpretable (attention weights show aspect locations). 2) End-to-end. 3) Handles multiple aspects. 4) No external aspect lexicon needed. Implementation: `aspect_attn = softmax(W2 * tanh(W1 * BERT_output + b1))`. BERT-ADA is the most popular attention-based ABSA model.
**Code:**
```python
import torch
BERT_out = torch.randn(6, 768)
W1 = torch.randn(64, 768); W2 = torch.randn(1, 64); b1 = torch.randn(64)
attn = torch.softmax(W2 @ torch.tanh(W1 @ BERT_out.T + b1[:, None]), dim=-1).squeeze()
for token, a in zip("The food was great today".split(), attn):
    print(token, round(float(a), 3))
```

## Q12: How do you implement temporal sentiment analysis (sentiment over time)?
**A:** Temporal sentiment tracks sentiment evolution: 1) Dataset split by time windows (daily, weekly, monthly). 2) Train per-window models or time-aware model. 3) Features: time embeddings, recency weighting, trend features. 4) Models: a) Time-aware LSTM: input = [text_embedding, time_embedding]. b) BERT + time features: concatenate time embedding with [CLS]. c) Change point detection: detect when sentiment distribution shifts. 5) Metrics: sentiment trend (increasing, decreasing, stable), velocity of change. 6) Visualization: sentiment time series plot with confidence bands. Applications: 1) Brand monitoring (spike in negative sentiment = PR crisis). 2) Product launch tracking (sentiment before/after launch). 3) Political sentiment (election campaign tracking). Implementation: BERT encodes text, then time-aware classifier (adds month/week as inputs). Use Facebook Prophet or ARIMA for forecasting.
**Code:**
```python
import pandas as pd
df = pd.DataFrame({"date": pd.to_datetime(["2026-01-01", "2026-01-02", "2026-02-01"]),
                   "compound": [0.5, -0.4, 0.8]})
monthly = df.groupby(df.date.dt.to_period("M")).compound.mean()
print(monthly)
```

## Q13: How do you handle sentiment analysis for comparative sentences?
**A:** Comparative sentiment: "Product A is better than Product B." Challenges: 1) Sentiment depends on which entity is the focus. 2) Comparatives may be neutral (A has more features than B). Approaches: 1) Target-aware: identify the target entity (A) and compared entity (B). Classify sentiment toward target. 2) Comparative relation extraction: extract comparative pairs (entity, attribute, preference). 3) Decomposition: split into two statements ("A is good" + "B is less good"). 4) BERT with comparative markers: add `[COMP]` tokens around comparative phrases. 5) Comparative-specific datasets: SemEval-2016 Task 5 (comparative aspect-based sentiment). Models: 1) BERT + sequence labeling for comparative elements. 2) CompareNet: knowledge-enhanced comparative sentiment. 3) T5: generate sentiment statement from comparative input. BERT achieves ~80% F1 on comparative sentiment (vs ~90% on regular sentiment).
**Code:**
```python
import re
m = re.search(r"(\w+) is better than (\w+)", "Product A is better than Product B.")
print("decompose ->", f"{m.group(1)} is good | {m.group(2)} is worse")
```

## Q14: How do you implement zero-shot sentiment analysis for unseen categories?
**A:** Zero-shot sentiment: predict sentiment for categories not seen during training. Approaches: 1) NLI-based: reformulate as entailment. Premise = text, Hypothesis = "This text expresses [CATEGORY] sentiment." Use MNLI model. 2) BART zero-shot: Hugging Face pipeline. 3) T5/prompting: "Is this text positive or negative?" Works for any sentiment granularity. 4) Sentence transformers: encode text, compare to category descriptions via cosine similarity. 5) Cross-modal: map sentiment categories to learnable embeddings (attribute learning). Performance: 1) NLI-based: ~80-85% accuracy for binary sentiment (close to fine-tuned). 2) For fine-grained (1-5 stars): ~50-60% (much lower than fine-tuned ~70%). 3) For emotion categories: ~60-70% F1. Best for: rapid prototyping, dynamic category sets, low-resource settings. For production: fine-tuned model always outperforms zero-shot. Use zero-shot as baseline or for categories that change frequently.
**Code:**
```python
from transformers import pipeline
nli = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
print(nli("The camera exceeds my expectations.",
          candidate_labels=["positive", "negative", "neutral"]))
```

## Q15: How do you handle imbalanced datasets in sentiment analysis with augmentation?
**A:** Beyond standard resampling, augmentation for imbalanced sentiment: 1) Back-translation: translate minority class to intermediate language and back. Preserves sentiment, generates diverse phrasing. 2) EDA (Easy Data Augmentation): synonym replacement (10-20% of words), random insertion/swap/deletion. 3) BERT-MLM: mask and predict tokens in minority class sentences. 4) Conditional BERT: generate new sentences conditioned on sentiment label (CTRL, GPT-2 fine-tuned per label). 5) Mixup: interpolate between text embeddings. 6) SMOTE: in embedding space (not raw text). 7) GPT-3/LLM generation: prompt with "Generate a positive review about a product." Most effective: back-translation + EDA. With 100 minority class examples, augmentation can improve F1 from 0.4 to 0.7. Best practice: augment minority class to 50% of majority class size. Monitor for overfitting (augmentation artifacts).
**Code:**
```python
from transformers import MarianMTModel, MarianTokenizer
def back_translate(text):
    tok = MarianTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-fr")
    model = MarianMTModel.from_pretrained("Helsinki-NLP/opus-mt-en-fr")
    mid = tok.decode(model.generate(**tok(text, return_tensors="pt"))[0],
                     skip_special_tokens=True)
    tok2 = MarianTokenizer.from_pretrained("Helsinki-NLP/opus-mt-fr-en")
    model2 = MarianMTModel.from_pretrained("Helsinki-NLP/opus-mt-fr-en")
    return tok2.decode(model2.generate(**tok2(mid, return_tensors="pt"))[0],
                       skip_special_tokens=True)
print(back_translate("The charger stopped working after a week"))
```

## Q16: How do you implement attention-based multi-modal sentiment analysis (text + audio + video)?
**A:** Multi-modal sentiment: 1) Text: BERT encodes. 2) Audio: wav2vec, HuBERT, or OpenSMILE features (prosody, tone, pitch). 3) Video: face features (EmotionNet, FaceNet), body language. 4) Fusion: a) Early fusion: concatenate features before classification. b) Late fusion: separate classifiers + weighted vote. c) Cross-modal attention: text attends to video features and vice versa. d) Multimodal transformer (MulT): cross-modal transformers. 5) Datasets: CMU-MOSI (sentiment intensity), CMU-MOSEI (6 emotions), IEMOCAP (dialogue). State-of-the-art: MulT achieves ~85% accuracy on CMU-MOSI. BERT + audio features + video features = 3-5% improvement over text-only. Practical challenges: 1) Data collection difficulty (expensive). 2) Synchronization across modalities. 3) Missing modalities at inference. 4) Computational cost. Use for: video reviews, call center analytics, human-robot interaction.
**Code:**
```python
import numpy as np
text = np.array([0.8, 0.2]); audio = np.array([0.6, 0.4]); video = np.array([0.9, 0.1])
early = np.concatenate([text, audio, video])
late = 0.4 * text.mean() + 0.3 * audio.mean() + 0.3 * video.mean()
print("early fusion dim:", early.shape, "| late fusion score:", round(float(late), 2))
```

## Q17: How do you implement few-shot sentiment analysis using pattern-exploiting training (PET)?
**A:** PET for few-shot sentiment: 1) Create pattern-verbalizer pairs: pattern = "[TEXT] This text expresses [MASK] sentiment." verbalizer = {"positive": "positive", "negative": "negative"}. 2) Fine-tune BERT (MLM head) on few labeled examples with this pattern. 3) Multiple patterns (e.g., "[TEXT] The opinion is [MASK].") - train separate models. 4) Knowledge distillation: ensembled soft labels from pattern models train a final classifier. Benefits: 1) 10-100 labeled examples can achieve 85-90% of full-data performance. 2) Leverages BERT's MLM pre-training. 3) Multiple patterns reduce variance. 4) Outperforms standard fine-tuning with few examples. PET achieves ~90% SST-2 accuracy with 100 examples (vs ~80% for standard fine-tuning). iPET (iterative PET): uses model's own predictions for unlabeled data, retrains, improves further. PET is the best few-shot approach for BERT sentiment.
**Code:**
```python
from transformers import pipeline
mlm = pipeline("fill-mask", model="distilbert-base-uncased")
verbalizer = {"excellent": "positive", "amazing": "positive",
              "awful": "negative", "terrible": "negative"}
for r in mlm("The review says: 'The camera is [MASK].'", top_k=4):
    print(r["token_str"], "->", verbalizer.get(r["token_str"], "unknown"))
```

## Q18: How do you handle domain-specific negation patterns in sentiment analysis?
**A:** Domain-specific negation: 1) Medical: "no evidence of infection" = positive (no infection). "patient denies chest pain" = absence of symptom (not negative). 2) Financial: "not profitable" = negative. "not unexpected" = double negative = positive (but subtle). 3) Legal: "not guilty" = positive (acquittal). 4) Product: "not bad" = positive. Approaches: 1) Domain-specific negation scope model: fine-tune BERT for negation detection on domain data. 2) Negation lexicon: domain-specific negation cues (e.g., medical: "rule out", "denies"). 3) Multi-task: sentiment + negation detection. 4) Dependency parsing: identify negation scope via domain-specific dependency patterns. 5) BERT pre-trained on domain text: implicitly learns negation patterns. Best practice: collect 100-500 domain-specific negated sentences, annotate scope+polarity, fine-tune BERT. This captures domain nuance better than general methods.
**Code:**
```python
def medical_negation(text, cues=("no evidence of", "denies", "rule out")):
    for cue in cues:
        if cue in text.lower():
            return "negated: " + text.lower().split(cue)[-1].strip()
print(medical_negation("No evidence of infection found."))
```

## Q19: How do you implement conditional sentiment analysis (sentiment depending on conditions)?
**A:** Conditional sentiment: sentiment depends on a condition. "If the price drops, I will buy it" = positive about buying contingent on price drop. Approaches: 1) Conditional sentiment dataset: SAO (SentiCondition), Conditional Sentiment. 2) Decomposition: extract condition (if X) and main sentiment (Y). Predict sentiment toward Y under condition X. 3) BERT with conditional encoding: encode both condition and main clause with `[COND]` and `[MAIN]` separators. 4) Prompting: "Given condition [X], the sentiment about [Y] is [MASK]." 5) Structured prediction: predict (condition, target, sentiment). Performance: BERT-based conditional sentiment achieves ~80% accuracy. Challenges: 1) Complex conditionals (multiple conditions, nested). 2) Hypothetical vs real conditions. 3) Explicit vs implicit conditions. Use for: financial sentiment ("if revenue grows"), survey analysis ("I would recommend if..."), product feedback.
**Code:**
```python
import re
m = re.match(r"If (.+?), (.+)", "If the price drops, I will buy it.")
print("condition:", m.group(1), "| main clause:", m.group(2))
print("sentiment toward main clause: positive (contingent on condition)")
```

## Q20: How do you implement LSTM vs BERT tradeoff analysis for a sentiment pipeline?
**A:** Decision framework: 1) Data size: < 1K labeled -> BERT (pre-training helps). > 100K labeled -> LSTM can approach BERT. 2) Latency: < 10ms -> LSTM. < 50ms -> DistilBERT. > 50ms -> BERT. 3) Hardware: CPU only -> LSTM or DistilBERT ONNX. GPU -> BERT. 4) Text length: < 512 tokens -> BERT. > 512 tokens -> LSTM or Longformer. 5) Accuracy requirements: < 85% acceptable -> LSTM. > 90% required -> BERT. 6) Development speed: fast -> LSTM (simpler). Highest accuracy -> BERT. 7) Interpretability: LSTM attention is simpler, BERT attention is complex. Empirical: BERT-base: 92% SST-2, 50ms GPU. BiLSTM-Attn: 87%, 5ms CPU. DistilBERT: 91%, 15ms GPU. Recommendation: start with DistilBERT (best accuracy/speed tradeoff). Use BERT if highest accuracy needed. Use LSTM for extreme latency or CPU-only constraints.
**Code:**
```python
def choose(data, latency_ms, gpu, length):
    if data < 1000: return "BERT (pre-training helps)"
    if latency_ms < 10: return "LSTM"
    if gpu and length <= 512: return "BERT"
    return "DistilBERT / Longformer"
for c in [(100, 2, False, 300), (200000, 5, False, 60), (50000, 50, True, 200)]:
    print(c, "->", choose(*c))
```

## Q21: How do you implement sentiment summarization for review collections?
**A:** Sentiment summarization generates concise summary of sentiments from multiple reviews. Approaches: 1) Aspect-based: extract aspects, aggregate sentiment per aspect. Output: "Battery life: 80% positive. Camera: 60% positive." 2) Abstractive: generate summary text (T5, BART fine-tuned on review-summary pairs). 3) Extractive: select representative positive and negative sentences. 4) Hybrid: aspect aggregation + key sentences. Architecture: 1) Process reviews through ABSA (aspect + sentiment). 2) Aggregate aspect sentiments (percentage positive/negative/neutral). 3) Select representative quotes per aspect. 4) Generate structured summary. 5) Optionally generate natural language via T5: "Customers love the battery life (8/10 positive) but find the camera mediocre (6/10)." Metrics: ROUGE for abstractive, factuality (do aspects match), coverage (are all aspects mentioned). Use for: product pages, survey analysis, reputation management.
**Code:**
```python
from collections import defaultdict
rows = [("battery", 1), ("battery", 1), ("camera", -1), ("camera", 1), ("battery", 0)]
agg = defaultdict(list)
for aspect, s in rows:
    agg[aspect].append(s)
for a, vs in agg.items():
    print(a, {"positive": vs.count(1) / len(vs), "negative": vs.count(-1) / len(vs)})
```

## Q22: How do you implement sarcasm detection using contrastive learning?
**A:** Contrastive learning for sarcasm: 1) Create positive pairs: same label (sarcastic-sarcastic, non-sarcastic-non-sarcastic). 2) Create negative pairs: different labels. 3) Fine-tune BERT with NT-Xent loss to pull similar labels together, push different apart. 4) Add classification head for final prediction. Augmentation for contrastive pairs: 1) Back-translation (preserves sarcasm). 2) Paraphrase (same sarcasm different words). 3) Change positive words to synonyms (sarcasm often uses positive words in negative context - changing them may break it, use carefully). Benefits: 1) Better text representations for sarcasm detection. 2) More robust to domain shift. 3) Works with limited labels. Performance: contrastive BERT achieves 84% F1 on iSarcasm (vs 80% for standard BERT). Best for: limited labeled data, improving embedding quality.
**Code:**
```python
import torch
z = torch.nn.functional.normalize(
    torch.tensor([[1., 0., .1], [.8, .2, 0.], [0., 1., .1], [.1, .8, 1.]]), dim=1)
y = torch.tensor([0, 0, 1, 1])
sim = (z @ z.T) / 0.5
loss = torch.stack([
    -sim[i][(y == y[i]) & (torch.arange(len(y)) != i)].logsumexp()
    + sim[i].exp().sum().log()
    for i in range(len(y))]).mean()
print("contrastive loss:", round(float(loss), 3))
```

## Q23: How do you handle sentiment drift (concept drift) in production?
**A:** Sentiment drift: meaning of words changes over time. "sick" = negative (ill) -> positive (cool). Detecting drift: 1) Monitor prediction distribution: if %positive changes significantly, investigate. 2) Monitor accuracy on recent human-validated samples. 3) Monitor input embedding distribution (embedding drift). Handling drift: 1) Periodic retraining (weekly/monthly) with recent data. 2) Online learning: update model on small recent batches. 3) Ensemble of time-specific models (monthly models, combine predictions). 4) Data weighting: weight recent training data higher. 5) Active learning: sample uncertain recent inputs for labeling. 6) Feature hashing: reduce impact of specific terms. BERT-based: fine-tune on rolling 6-month window. Replace one month at a time (remove oldest, add newest). This adapts to drift while preserving general knowledge. Monitor: track monthly F1 on holdout set.
**Code:**
```python
def monitor(batch):
    pct_pos = sum(1 for p in batch if p > 0.05) / len(batch)
    if abs(pct_pos - 0.5) > 0.2:
        print("drift signal -> collect labels, retrain on recent window")
    return round(pct_pos, 2)
print(monitor([0.9, 0.8, 0.7, 0.9]))
```

## Q24: How do you implement sentiment analysis in low-resource languages ( < 10K sentences)?
**A:** Low-resource sentiment: 1) Cross-lingual transfer: use XLM-R/mBERT fine-tuned on high-resource language (English), zero-shot to target. Achieves 70-80% of English performance. 2) Machine translation + sentiment: translate target to English, run English model. Translation errors hurt accuracy. 3) Lexicon-based: build small sentiment lexicon for target language (50-100 seed words via human translation of English sentiment words). 4) Active learning: label 500 informative target language sentences (via model uncertainty sampling), fine-tune mBERT. 5) Few-shot with PET: 100 labeled examples, multiple patterns. 6) Data augmentation: back-translation within low-resource language. Best approach for truly low-resource: mBERT + active learning with 500 labeled sentences. Achieves ~80% accuracy. Using GPT-4 for annotation (weak supervision) can also generate labels for low-resource languages.
**Code:**
```python
import numpy as np
rng = np.random.default_rng(0)
probs = rng.uniform(0.2, 1.0, size=1000)
least = np.argsort(-np.abs(probs - 0.5))[:100]
print("label these first (uncertainty-first):", least[:5], "... total 100")
```

## Q25: How do you implement target-dependent sentiment using BERT with target injection?
**A:** Target injection for target-dependent sentiment: 1) Input format: `[CLS] target [SEP] text [SEP]`. 2) BERT learns that the first segment is the target. 3) The [CLS] representation is conditioned on both target and context. 4) Classification head on [CLS] predicts sentiment toward the target. Example: "iPhone camera is great but battery is poor." Target = "iPhone camera" -> positive. Target = "battery" -> negative. Benefits: 1) Simple (no architectural changes). 2) BERT's attention connects target with relevant context. 3) Works for single-target per pass (but can run multiple targets). Performance: ~90% F1 on SemEval-2014 Task 4. Target injection outperforms standard sentence-level BERT by 10-15% for ABSA. It's the simplest and most effective approach for targeted sentiment.
**Code:**
```python
from transformers import AutoTokenizer
tok = AutoTokenizer.from_pretrained("bert-base-uncased")
enc = tok("battery [SEP] The camera is great but the battery died fast.")
print(tok.convert_ids_to_tokens(enc["input_ids"]))
```

## Q26: How do you implement sentiment using Graph Neural Networks (GNNs) with BERT?
**A:** GNN for sentiment: 1) Build a graph: nodes = words/entities, edges = syntactic dependencies or co-occurrence. 2) BERT encodes node features (word embeddings). 3) GNN layers propagate information along edges (GCN, GAT, GGNN). 4) Readout: graph-level sentiment. 5) Aspect-specific: subgraph around aspect node. Architecture: BERT -> word embeddings -> GCN over dependency tree -> aspect-specific pooling -> sentiment classifier. Benefits: 1) Captures syntax (negation scope via dependency edges). 2) Handles long-range dependencies via graph paths. 3) Interpretable (which edges matter). Performance: BERT + GCN achieves state-of-the-art on ABSA with implicit aspects (where context is crucial). ~93% F1 on SemEval-2014 Restaurant. Tradeoffs: slower than pure BERT, requires dependency parsing. Best for: syntax-heavy sentiment (complex negatives, multiple aspects).
**Code:**
```python
import networkx as nx
G = nx.from_edgelist([("food", "was"), ("was", "great"),
                      ("service", "was"), ("was", "slow")])
print(list(G.edges()))
```

## Q27: How do you implement a rejection option for uncertain sentiment predictions?
**A:** Reject uncertain predictions (send to human): 1) Confidence threshold: if max softmax < 0.7, reject. 2) Margin: if top-2 score difference < 0.2, reject. 3) Entropy: if entropy > threshold, reject. 4) MC Dropout variance: if variance > 0.1, reject. 5) Distance-based: if embedding is far from training data (OOD), reject. 6) Calibration: use temperature-scaled probabilities for better uncertainty. Implementation: 1) Model predicts + confidence score. 2) If confidence < threshold: route to human review. 3) Otherwise: auto-respond. 4) Human labels are collected and used for retraining. Threshold selection: tune on validation set to achieve desired rejection rate (e.g., reject 5% of inputs, capture 90% of errors). In production: start with 5% rejection rate, monitor human review accuracy, adjust threshold. Rejection improves user-facing accuracy (remaining auto-predicted 95% have higher accuracy).
**Code:**
```python
def route(probs, thresh=0.7):
    return "send to human" if max(probs) < thresh else "auto-respond"
print(route([0.9, 0.05, 0.05]))
print(route([0.40, 0.35, 0.25]))
```

## Q28: How do you implement domain adaptation for sentiment with task-specific adapters?
**A:** Adapter-based domain adaptation: 1) Freeze BERT weights. 2) Insert small adapter layers (2-layer FFN with bottleneck) after each transformer layer. 3) Train only adapter layers on domain-specific data (few thousand examples). 4) Keep original BERT weights unchanged. Benefits: 1) Single BERT model with multiple adapter modules (one per domain). 2) No catastrophic forgetting. 3) Training is fast (only 3-5% of parameters trained). 4) Storage: one BERT + N small adapters (vs N full BERT models). Performance: adapter-based domain adaptation achieves 95% of full fine-tuning performance on domain sentiment. Each adapter adds ~1M params (vs 110M for full BERT). For production with 10 domains: 110M + 10M params (vs 1.1B for separate models). This makes adapter-based approach ideal for multi-domain sentiment platforms.
**Code:**
```python
base, adapter = 110_000_000, 1_000_000
print("trainable when adding adapter:", round(adapter / base * 100, 1), "%")
print("10 domains: 1 BERT + 10 adapters (not 10 full BERTs)")
```

## Q29: How do you implement sentiment analysis for multi-party dialogue?
**A:** Multi-party dialogue sentiment: 1) Speaker-specific encoding: add speaker embeddings (`[SPEAKER_A]`, `[SPEAKER_B]`). 2) Dialogue context: previous N utterances as context. 3) Hierarchical: utterance-level BERT + dialogue-level transformer. 4) Speaker dynamics: cross-speaker attention (how A's sentiment affects B's response). 5) Memory: carry sentiment state per speaker across turns. 6) Emotion contagion: model how sentiment spreads between speakers (e.g., one person's anger triggers defensive response). Architecture: 1) Each utterance = `[SPEAKER_X] utterance [SEP]`. 2) Concatenate utterances. 3) BERT encodes full dialogue. 4) Per-utterance classification or per-dialogue sentiment trajectory. 5) SLOT (Sentiment Lines Over Time) for continuous tracking. Datasets: MELD, EmoryNLP, IEMOCAP. Performance: BERT + context (5 previous utterances) achieves ~65-70% F1 on multi-party emotion recognition.
**Code:**
```python
turns = [("A", "I'm furious."), ("B", "Calm down."), ("A", "No I won't.")]
encoded = " [SEP] ".join(f"[SPEAKER_{s}] {t}" for s, t in turns)
print(encoded)
```

## Q30: How do you implement sentiment analysis for implicit sentiment (no explicit sentiment words)?
**A:** Implicit sentiment: "My phone died after 2 hours." No sentiment word ("died" is metaphorical but negative). Approaches: 1) BERT: learns that "died" in device context is negative (from pre-training + fine-tuning). 2) Event-based: extract event + infer sentiment from event type (device failure = negative). 3) Common sense knowledge: integrate knowledge bases (ConceptNet, ATOMIC) to infer sentiment from situations. 4) BERT + knowledge: concatenate knowledge graph embeddings with BERT hidden states. 5) Prompting: "My phone died after 2 hours. This is [MASK]." BERT predicts "bad" (using MLM knowledge). Performance: BERT achieves ~80% accuracy on implicit sentiment (vs ~92% on explicit). Challenges: 1) Implicit sentiment is highly domain-dependent. 2) Requires world knowledge. 3) Cultural differences affect what's implicit. Best: BERT pre-trained on large corpus captures many implicit sentiment patterns. For domain-specific implicit sentiment: domain-adaptive pre-training helps.
**Code:**
```python
from transformers import pipeline
mlm = pipeline("fill-mask", model="distilbert-base-uncased")
hits = mlm("My phone died after 2 hours. That was [MASK].", top_k=3)
print([h["token_str"] for h in hits])
```
## Q31: How do you implement a sentiment analysis pipeline with error analysis and bias detection?
**A:** Error analysis pipeline: 1) Collect misclassified examples. 2) Categorize errors: sarcasm missed, negation missed, domain-specific term wrong, ambiguous, labeling error. 3) Slice analysis by: sentiment intensity (strong vs weak), text length, domain, demographic (if available). 4) Bias detection: a) Counterfactual evaluation: swap gender/race terms in text, check if prediction changes. b) Subgroup analysis: compare accuracy across groups. c) Differential performance: compute false positive/negative rates per group. 5) Mitigation: if bias detected, a) Augment training data for underrepresented groups. b) Reweight training samples. c) Adversarial debiasing (train model that can't predict protected attribute). 6) Reporting: document bias metrics, mitigation steps, residual risk. Tools: AI Fairness 360, What-If Tool. Regular bias audits are essential for production sentiment systems, especially for content moderation.
**Code:**
```python
sen["fair"] = True  # tqdm over slices
groups = {"race": {"A": 10, "B": 40}, "gender": {"M": 30, "F": 30}}
for attr, counts in groups.items():
    total = sum(counts.values())
    print(attr, {k: round(v / total, 2) for k, v in counts.items()})
```

## Q32: How do you implement a BERT sentiment model with document-level attention?
**A:** Document-level attention for long documents: 1) Split document into sentences/segments. 2) Encode each segment with BERT (get segment embeddings). 3) Segment-level attention: learn which segments are most important for overall sentiment. 4) Weighted sum of segment embeddings -> document embedding -> classifier. 5) Position encoding for segment order (earlier vs later segments may have different importance). Architecture: `BERT per segment -> [CLS] embeddings -> segment attention -> document embedding -> softmax`. 6) Hierarchical variant: segment BERT -> segment BiLSTM -> document sentiment. Benefits: 1) Handles arbitrary length documents. 2) Attention weights show which sentences drive sentiment. 3) Better than truncation (captures full document). Performance: Hierarchical BERT on long reviews (500+ words) outperforms truncated BERT by 5-10% F1. The attention mechanism learns that title and first/last sentences often carry the main sentiment.
**Code:**
```python
import torch
segments = [torch.randn(768) for _ in range(5)]
W = torch.randn(768); V = torch.randn(768, 768); b = torch.randn(768)
attn = torch.softmax(
    torch.stack([(seg * W).sum() for seg in segments]), dim=-1)
doc = sum(a * s for a, s in zip(attn, segments))
print("attention per segment:", [round(float(a), 3) for a in attn])
```

## Q33: How do you handle lexical variation in sentiment across dialects?
**A:** Dialect variation: "proper" = correct (British) vs "proper" = very (AAVE). Approaches: 1) Dialect-aware BERT: train on dialect-specific data. 2) Vocabulary extension: add dialect-specific terms to tokenizer. 3) Normalization: map dialect terms to standard form. 4) Multi-task: sentiment + dialect identification (ensures model doesn't conflate dialect with sentiment). 5) Data augmentation: generate dialect variations of training data. 6) Dialect-specific adapters: shared BERT + dialect-specific adapter layers. Examples: 1) AAVE: "finna" (fixing to = about to), "hella" (very) - neutral or positive. 2) Indian English: "prepone" (opposite of postpone) - neutral. 3) British: "brilliant" (very strong positive) vs American "brilliant" (milder). For global sentiment: use multilingual/dialectal models (XLM-R, BERTweet for social media). Test accuracy per dialect group to ensure fairness.
**Code:**
```python
norm = {"finna": "about_to", "hella": "very", "prepone": "reschedule"}
print("normalized:", [norm.get(w, w) for w in "that was hella good".split()])
```

## Q34: How do you implement sentiment using BERT with causal language model (GPT) features?
**A:** Hybrid BERT + GPT: 1) BERT: bidirectional encoder (context understanding). 2) GPT: unidirectional decoder (generation, reasoning). 3) Concatenate BERT [CLS] + GPT [EOS] embeddings. 4) Classify on combined representation. 5) Alternatively: multi-task (BERT for classification, GPT for explanation generation). Implementation: 1) Encode text with BERT (get [CLS]). 2) Encode text with GPT (get final hidden). 3) Concatenate: `[BERT_CLS; GPT_LAST]`. 4) Linear layer classification. Benefits: 1) BERT provides bidirectional context. 2) GPT provides generative reasoning. 3) Combined outperforms either alone by 1-2%. Tradeoffs: 2x compute at inference (run both models). Practical variant: use DistilBERT + DistilGPT2. Better variant: T5 (encoder-decoder) handles both understanding and generation in one model. For most sentiment tasks, BERT alone is sufficient. Hybrid is useful when you need both classification and explanation.
**Code:**
```python
import torch
bert = torch.randn(1, 768); gpt = torch.randn(1, 768)
comb = torch.cat([bert, gpt], dim=1)          # [BERT_CLS; GPT_LAST]
print("combined:", comb.shape, "-> linear(1536, 3) classification")
```

## Q35: How do you implement sentiment-aware text generation (e.g., generate positive reviews)?
**A:** Sentiment-controlled generation: 1) Conditional Transformer (CTRL): conditioned on sentiment code + text. 2) Prompting GPT: "Write a positive review of a restaurant." 3) BERT + GAN (Generative Adversarial Network): generator creates text, discriminator checks sentiment. 4) Plug and Play Language Model (PPLM): update GPT hidden states to steer toward target sentiment. 5) Diffusion models: gradually denoise text conditioned on sentiment. Evaluation: 1) Sentiment accuracy (classifier verifies). 2) Fluency (perplexity). 3) Diversity (distinct n-grams). 4) Controllability (generated text matches target sentiment). Applications: 1) Data augmentation (generate synthetic reviews for training). 2) Review generation for testing. 3) Controlled chatbots (maintain consistent sentiment). For production: GPT-3/4 prompting with few-shot examples gives best results for sentiment-controlled generation.
**Code:**
```python
import openai
client = openai.OpenAI()
r = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user",
               "content": "Write a positive restaurant review in 2 sentences."}])
print(r.choices[0].message.content)
```

## Q36: How do you implement aspect-category sentiment analysis with multi-label BERT?
**A:** Aspect-category ABSA: predict sentiment for predefined categories (food, service, ambiance, price) without extracting aspect terms. Multi-label: each category gets a sentiment label (positive/negative/neutral). Implementation: 1) BERT encodes text. 2) N classification heads (one per category). 3) Each head = linear(768, 3) -> softmax. 4) Loss = sum of cross-entropy per category. 5) Multi-task: all categories trained jointly. 6) Category-specific attention: each head can attend to different parts of text. Benefits: 1) No aspect extraction needed (simpler). 2) Fixed category set (good for known domains). 3) Multi-task improves per-category accuracy. Performance: ~85% F1 on SemEval-2015 ABSA. Compared to full ABSA (extraction + classification): about 5% lower but simpler to deploy. Use when: 1) Categories are known and fixed. 2) Aspect extraction is not needed. 3) Quick deployment required.
**Code:**
```python
import torch
hidden = torch.randn(1, 768)
heads = [torch.softmax(torch.nn.Linear(768, 3)(hidden), dim=1)
         for _ in ["FOOD", "SERVICE", "AMBIANCE", "PRICE"]]
print({h: heads[i].argmax().item() - 1 for i, h in enumerate(cats)})
```

## Q37: How do you handle sentiment analysis with overlapping aspects?
**A:** Overlapping aspects: "The pizza was delicious but the pizza crust was too thick." Aspects: pizza (positive) and pizza crust (negative) overlap (crust is part of pizza). Approaches: 1) Span-based: predict non-overlapping spans with sentiment. If spans overlap, keep longer span (pizza) or split (pizza + crust separately). 2) Hierarchical: parent aspect (pizza) + child aspects (crust). 3) Multi-label per token: each token can belong to multiple aspects (B-pizza, I-pizza, B-crust, I-crust, O). 4) Graph-based: build aspect graph (pizza -> crust), propagate. BERT + CRF with multi-label: each token predicts a multi-hot vector over aspect types. Output: pizza [B-ASP1, B-ASP2] (both pizza and pizza crust start at same word). Implementation complexity: high. For most production systems, non-overlapping aspects (preferring longest span) is sufficient.
**Code:**
```python
tokens = "The pizza crust was too thick".split()
tags = {"pizza": [0, 1, 2, 3, 4, 5], "pizza_crust": [1, 2]}
for asp, idx in tags.items():
    print(asp, [tokens[i] for i in idx])
print("hierarchical: crust is a child of pizza")
```

## Q38: How do you implement BERT sentiment with contrastive learning across languages?
**A:** Cross-lingual contrastive learning: 1) Create parallel sentences (same content in different languages). 2) Positive pairs: same sentiment in different languages. 3) Negative pairs: different sentiment in same/different language. 4) NT-Xent loss: pull same-sentiment pairs together, push different apart, across language boundaries. 5) This aligns sentiment representations across languages. Architecture: 1) XLM-R encodes sentences. 2) Mean pooling. 3) Projection head (MLP). 4) Contrastive loss. 5) Classification head (trained on labeled source language). Benefits: 1) Better cross-lingual transfer. 2) Reduces language bias. 3) Sentiment representations are language-agnostic. Performance: improves zero-shot cross-lingual sentiment by 3-5% F1. Best for: multilingual sentiment systems where labeled data exists only for a few languages. The contrastive alignment creates a shared sentiment space across languages.
**Code:**
```python
import torch
x = torch.randn(4, 128); y = torch.randint(0, 2, (4,))
sim = torch.mm(x, x.T)
pos = [a for a in range(4) if y[a] == y[0] and a != 0]
loss = -sim[0, pos[0]:pos[1]].logsumexp() + sim[0].exp().sum().log()
print("cross-lingual contrastive loss:", round(float(loss), 3))
```

## Q39: How do you implement a sentiment model that handles both explicit and implicit aspects?
**A:** Explicit aspects: mentioned directly ("battery life is great"). Implicit aspects: implied but not mentioned ("this phone lasts all day" = battery life). Approaches: 1) BERT + aspect prediction: model predicts aspects (both explicit and implicit) from context. 2) Common sense knowledge: if "lasts all day" -> likely aspect = battery life. 3) Clustering: group sentences into aspect clusters (unsupervised aspect discovery). 4) Prompting: "What aspect of the product is being discussed? [MASK]" 5) Multi-task: aspect extraction (explicit) + aspect inference (implicit). Architecture: 1) BERT encodes text. 2) Aspect extraction head (BIO tagging for explicit aspects). 3) Aspect inference head (multi-label classification for implicit aspects). 4) Joint training. Performance: implicit aspect detection is harder (~75% F1 vs ~90% for explicit). Use knowledge bases (ConceptNet, ProBase) to infer implicit aspects from context. For production: focus on explicit aspects (most reviews are explicit). Add implicit as optional enhancement.
**Code:**
```python
explicit = {"the", "battery"}
implied = {"lasts", "all", "day"}
text = "this phone lasts all day".split()
print("explicit aspects:", [w for w in text if w in explicit])
print("implicit aspect: battery life")
```

## Q40: How do you implement aspect-level sentiment aggregation across multiple reviews?
**A:** Aggregating aspect sentiments across reviews: 1) Process each review through ABSA (extract aspects + sentiment). 2) Map aspects to canonical categories (food, service, ambiance). 3) Aggregate: count positive/negative/neutral per category. 4) Score: (positive - negative) / total (or percentage positive). 5) Distribution: histogram of sentiment per category. 6) Trend: sentiment per category over time. 7) Key quotes: select representative reviews per category. 8) Weighted aggregation: more recent reviews get higher weight. 9) Review credibility: user reputation, verified purchase -> higher weight. Implementation: 1) ABSA per review. 2) Map to categories (using embedding similarity or rule-based). 3) Aggregate in database. 4) API returns {category: {positive: 0.8, negative: 0.1, neutral: 0.1, count: 150}}. Use for: product pages, restaurant listings, hotel reviews. This is the core of most sentiment analysis applications in e-commerce.
**Code:**
```python
from collections import defaultdict
reviews = [("food", 1), ("food", 1), ("service", -1), ("food", 0)]
agg = defaultdict(list)
[agg[a].append(v) for a, v in reviews]
print({a: {"pos": vs.count(1) / len(vs)} for a, vs in agg.items()})
```

## Q41: How do you implement sentiment analysis for streaming data with concept drift detection?
**A:** Streaming sentiment with drift detection: 1) Process mini-batches (1000 tweets/reviews). 2) Monitor prediction distribution per batch (% positive). 3) Monitor confidence distribution per batch. 4) Drift detection: a) ADWIN (adaptive sliding window): detect change in prediction distribution. b) DDM (Drift Detection Method): track error rate. c) KS-test: compare current vs baseline distribution. 5) On drift detected: a) Collect recent samples for human labeling. b) Fine-tune BERT on recent labeled data (1-2 epochs, low LR). c) Shadow deploy updated model, compare. d) If improved, swap models. 6) Model versioning: keep last 3 models, can fallback. 7) Monitor: track drift detection frequency, model update latency, accuracy post-update. For high-volume streaming (10K/sec): use DistilBERT (fast inference), sample 1% for drift detection, only retrain when significant drift confirmed.
**Code:**
```python
from scipy.stats import ks_2samp
old = [0.4, 0.5, 0.45, 0.55]; new = [0.9, 0.85, 0.95]
stat, p = ks_2samp(old, new)
print("drift detected" if p < 0.05 else "no drift", f"(p={p:.3f})")
```

## Q42: How do you implement a BERT sentiment model that handles multi-lingual code-switching at inference?
**A:** Code-switching at inference: user may switch languages mid-sentence. 1) mBERT/XLM-R: handles multiple languages in vocabulary (same model processes all). 2) Language-aware tokenization: identify language per token (using langid). 3) Per-language adapters: route tokens through appropriate language adapter. 4) Prompt engineering: "Analyze the sentiment of this text which may contain multiple languages." 5) Training: include code-mixed data in training. XLM-R limitations: 1) Some code-mixed patterns are rare in pre-training. 2) Language-specific sentiment expressions may conflict. Performance: XLM-R achieves ~75% F1 on Hinglish code-mixed sentiment. For production: use XLM-R + fine-tune on code-mixed data from your domain. If code-switching is rare (5% of traffic): detect language at sentence level, use per-language model for each sentence. If common (50%+): use dedicated code-mixed model (HingBERT, etc.).
**Code:**
```python
from transformers import pipeline
clf = pipeline("text-classification", model="xlm-roberta-base")
print(clf("ye phone ka battery bahut solid hai"))
```

## Q43: How do you implement fine-grained emotion detection (27 categories from GoEmotions) with BERT?
**A:** GoEmotions has 27 emotion categories. Implementation: 1) BERT encoder. 2) 27-output head with sigmoid activation (multi-label). 3) Binary cross-entropy loss per category. 4) Threshold tuning per category (default 0.5). 5) Evaluation: macro-F1, micro-F1. Data: GoEmotions has 58K Reddit comments, 27 emotion labels + neutral. Challenges: 1) Label imbalance (some emotions rare: grief, relief). 2) Multi-label correlation (admiration + approval often co-occur). 3) Annotation noise (emotions are subjective). BERT-base achieves ~60% macro-F1, ~70% micro-F1 on GoEmotions. Improvements: 1) Multi-task with sentiment (emotion + valence classification). 2) Hierarchical: coarse (positive/negative/neutral) -> fine (specific emotions). 3) Label correlation modeling (graph attention over label co-occurrence). 4) Data augmentation for rare emotions (back-translation). Use for: customer feedback (specific emotions), mental health monitoring, content understanding.
**Code:**
```python
import torch
logits = torch.sigmoid(torch.randn(27))
labels = ["admiration", "amusement", "anger", "annoyance", "approval"]
idx = [i for i, p in enumerate(logits) if p > 0.5]
print("detected:", [labels[i] for i in idx if i < len(labels)])
```

## Q44: How do you implement sentiment analysis with uncertainty quantification using Bayesian methods?
**A:** Bayesian BERT for uncertainty: 1) MC Dropout: dropout at inference (10 passes) -> mean + variance. 2) Concrete Dropout: learn dropout rate. 3) Variational inference: approximate Bayesian posterior (Bayes by Backprop). 4) Deep Ensemble: train 5 models, treat as samples from posterior. 5) Evidential deep learning: model predicts evidence parameters of Dirichlet distribution. 6) Laplace approximation: fit Gaussian around MAP estimate. For sentiment: MC Dropout is most practical. With 10 passes: 1) Sentiment prediction = mean of probabilities. 2) Uncertainty = variance or entropy. 3) Epistemic uncertainty (model uncertainty): high variance across passes. 4) Aleatoric uncertainty (data uncertainty): low max probability. Use epistemic uncertainty for OOD detection. Use aleatoric uncertainty for ambiguous inputs. Bayesian methods improve calibration but add 10x inference cost (for MC Dropout). Use only when uncertainty is critical (medical, financial sentiment).
**Code:**
```python
import torch
torch.manual_seed(0)
model = torch.nn.Sequential(torch.nn.Linear(4, 8), torch.nn.Dropout(0.3),
                            torch.nn.Linear(8, 3), torch.nn.Softmax(dim=-1))
x = torch.randn(1, 4)
passes = torch.stack([model(x) for _ in range(10)])
print("mean:", passes.mean(0).round(2))
print("variance:", passes.var(0).round(4))
```

## Q45: How do you implement BERT with label smoothing for overconfident sentiment predictions?
**A:** Label smoothing prevents overconfidence: 1) Replace hard labels (1.0, 0.0) with smoothed (0.9, 0.05, 0.05). 2) Cross-entropy loss with smoothed targets. 3) Typical smoothing: epsilon = 0.1. For 2-class: target = [0.95, 0.05] for positive, [0.05, 0.95] for negative. 4) For 3-class (pos/neg/neu): [0.93, 0.033, 0.033] for positive. Benefits: 1) Reduces overconfidence (softmax outputs are less extreme). 2) Improves calibration. 3) Better generalization (regularization). 4) Improves model robustness. Implementation: `nn.CrossEntropyLoss(label_smoothing=0.1)` in PyTorch. Impact: 1) BERT sentiment accuracy: no change or slight improvement (0-0.5%). 2) Expected Calibration Error (ECE): reduces by 30-50%. 3) Confidence distribution: more uniform, fewer predictions near 1.0. Label smoothing is recommended for production sentiment models to avoid overconfident false positives.
**Code:**
```python
import torch.nn as nn
y = torch.tensor([0, 2, 1, 0])
crit = nn.CrossEntropyLoss(label_smoothing=0.1)
print("smoothed CE:", round(float(crit(torch.randn(4, 3), y)), 3))
```
## Q46: How do you implement a BERT model that handles sentiment for yes/no questions?
**A:** Yes/no question sentiment: "Isn't this amazing?" -> positive. "Is this really bad?" -> questioning negative. Approaches: 1) BERT learns from context: "Isn't this amazing" appears in positive contexts in training data. 2) Rhetorical question detection: classify if question is rhetorical (sentiment-bearing) vs genuine (neutral). 3) Prompt-based: rewrite as assertion before sentiment analysis. "This is amazing" (remove question, keep sentiment). 4) Speaker intent: sarcastic questions ("Oh, is THAT supposed to be impressive?") need intent detection. 5) BERTweet (tweet-specific): trained on questions, handles them better. Performance: BERT sentiment on yes/no questions: ~75% accuracy (vs ~92% overall). The main challenge is distinguishing rhetorical (sentiment) from genuine (neutral) questions. For production: use question type classifier (rhetorical vs genuine) before sentiment analysis. Rhetorical questions: apply standard sentiment. Genuine questions: default to neutral or flag for human review.
**Code:**
```python
def analyze_question(text):
    rhetorical = text.strip().endswith("?") and "merely_asking" not in text
    return "rhetorical -> apply sentiment" if rhetorical else "genuine -> neutral/human"
print(analyze_question("Isn't this amazing?"))
```

## Q47: How do you optimize BERT sentiment inference for edge devices (mobile, IoT)?
**A:** Edge deployment: 1) TinyBERT (4 layers, 312 dim): 3x faster, 7x smaller than BERT-base, ~90% of accuracy. 2) MobileBERT: bottleneck architecture with 25x fewer parameters. 3) DistilBERT ONNX INT8: 4x faster, 4x smaller. 4) TensorFlow Lite: optimize for mobile CPUs/GPUs. 5) Quantization: INT8 (4x smaller, 3-4x faster). 6) Pruning: remove 40% weights with fine-tuning. 7) Task-specific: only keep layers needed for sentiment (prune top layers). 8) Embedding compression: reduce vocabulary size to domain-specific tokens. 9) Static vs dynamic quantization: static is faster (pre-computed scales). Performance on mobile: TinyBERT INT8: ~5ms per inference on iPhone 12, ~30MB model. BERT-base FP32: ~50ms, ~440MB. For real-time edge sentiment: TinyBERT INT8 is the best choice. For even smaller: ALBERT (parameter sharing) + pruning + quantization = <10MB with reasonable accuracy.
**Code:**
```python
models = {"bert_base_fp32": 50, "distilbert_int8": 8, "tinybert_int8": 5,
          "minilm_int8": 4}
print(sorted(models.items(), key=lambda kv: kv[1]))
```

## Q48: How do you implement sentiment analysis for indirect opinions (reported speech)?
**A:** Indirect opinions: "My friend said the movie was great, but I haven't seen it." Sentiment toward movie: positive (friend's opinion), but narrator has no opinion. Approaches: 1) Source attribution: identify who expressed the opinion (friend vs narrator). 2) BERT with source-dependency: opinion source and content. 3) Bio tagging: B-SOURCE, I-SOURCE, B-OPINION, I-OPINION. 4) Multi-task: opinion holder extraction + sentiment classification per holder. Challenges: 1) Embedding opinions: "According to critics, it's a masterpiece." Critics = source, masterpiece = positive. 2) Narrator's own sentiment may differ from reported sentiment. Performance: BERT-based source attribution achieves ~80% F1 on opinion holder extraction. For production: if only target entity sentiment matters (movie sentiment regardless of source), standard sentiment works. If source matters (user sentiment vs reported sentiment), use source-attributed sentiment analysis.
**Code:**
```python
tokens = "My friend said the movie was great".split()
source = tokens[1], "friend"; opinion = tokens[-1], "great"
print("source:", source, "| opinion:", opinion, "-> positive (friend's view)")
```

## Q49: How do you implement BERT with fuzzy matching for sentiment lexicon integration?
**A:** Fuzzy lexicon integration: 1) Create sentiment lexicon with word scores (e.g., AFINN, VADER). 2) For each input, compute fuzzy lexicon features: a) Match exact words. b) Match lemmas. c) Match synonyms (WordNet). d) Match subwords (for BERT: lexicon word may be split into subwords, sum subword sentiments). 3) Concatenate lexicon features with BERT [CLS] embedding. 4) Classify on combined representation. Benefits: 1) Leverages lexicon knowledge (especially for domain-specific terms). 2) Handles words BERT hasn't seen (via synonyms/lemmas). 3) Improves low-resource performance. 4) Acts as inductive bias. Implementation: 1) Build hashmap of word -> sentiment score. 2) For input text: tokenize, lemmatize, lookup each token, aggregate (sum/mean/max). 3) Produce 3 features: positive_score, negative_score, compound_score. 4) `combined = concat([CLS]@, lexicon_features)`. Performance: BERT + fuzzy lexicon improves sentiment accuracy by 1-3% on domain-specific data. The gain is larger (3-5%) for low-resource settings (<1000 labeled examples).
**Code:**
```python
lexicon = {"great": 3, "terrible": -3, "good": 2, "bad": -2}
text = "the movie was GREAT".lower().split()
feats = {"pos": sum(v for w, v in lexicon.items() if v > 0 and w in text),
         "neg": sum(v for w, v in lexicon.items() if v < 0 and w in text)}
print(feats)
```

## Q50: How do you implement sentiment analysis with active learning using uncertainty sampling for BERT?
**A:** Active learning with BERT: 1) Start with 100 labeled examples per class. 2) Train BERT. 3) Predict on large unlabeled pool. 4) Compute uncertainty per sample: a) Least confidence: 1 - max(softmax). b) Margin: top-2 probability difference. c) Entropy: -sum(p * log(p)). 5) Select N samples with highest uncertainty for labeling. 6) Add labeled samples to training set. 7) Retrain BERT. 8) Repeat until performance plateaus (typically 5-10 rounds). Results: 1) With 500 actively labeled samples: BERT achieves ~90% of full-data (10K) accuracy. 2) Random sampling needs ~2000 samples to match active with 500. 3) BERT's uncertainty is well-calibrated for active learning. Implementation tips: 1) Use diverse batch selection (not just top-N uncertain, add diversity). 2) BERT-based (BADGE): select diverse + uncertain using gradient embeddings. 3) Cold start: use VADER to preselect diverse samples. For production: active learning reduces labeling cost by 4x for equivalent accuracy.
**Code:**
```python
import torch
probs = torch.softmax(torch.randn(1000, 3), dim=-1)
entropy = -(probs * probs.log()).sum(dim=-1)
pick = entropy.topk(50).indices.tolist()
print("label these 50:", pick[:5], "...")
```

## Q51: How do you implement sentiment analysis for code (source code comments)?
**A:** Code sentiment: sentiment in code comments, commit messages, issue discussions. Challenges: 1) Technical language (not standard sentiment vocabulary). 2) Code references (function names, variable names). 3) Mixed natural language + code snippets. Approaches: 1) Code-BERT (CodeBERT, GraphCodeBERT): pre-trained on code + natural language. 2) Filter code snippets before analysis. 3) Handle code-specific slang ("LGTM" = positive, "WTF" = negative, "WIP" = neutral). 4) Commit sentiment: "fix" = positive, "hack" = negative, "refactor" = neutral. 5) Issue sentiment: "bug" = negative, "feature request" = positive. 6) Use SentiCR (Sentiment for Code Reviews): a tool for code review sentiment. Performance: CodeBERT fine-tuned on code review sentiment achieves ~80% accuracy. Challenges: code-specific sarcasm ("Great, another null pointer exception"), false positives from technical terms. Use for: detecting toxic code reviews, monitoring developer sentiment, flagging burnout.
**Code:**
```python
slang = {"LGTM": 1, "WTF": -1, "WIP": 0, "fix": 1, "hack": -1, "refactor": 0}
print({k: "pos" if v > 0 else "neg" if v < 0 else "neu" for k, v in slang.items()})
```

## Q52: How do you implement multilingual sentiment analysis using adapter-based fine-tuning?
**A:** Language adapters for multilingual sentiment: 1) Pre-train language adapters per language (small MLP in each transformer layer). 2) Freeze XLM-R weights. 3) Train task adapter (sentiment) on English data. 4) At inference: use XLM-R + language adapter for target language + sentiment adapter. Benefits: 1) One XLM-R model + N language adapters (very small). 2) Add new language: train only language adapter (requires unlabeled data). 3) Zero-shot: use source language adapter with target language text (may work for similar languages). Performance: XLM-R + language adapter achieves ~95% of fully fine-tuned per-language model. Language adapters are 5-10MB per language (vs 1.2GB for full XLM-R). This is the most efficient approach for 10+ language sentiment. Implementation: `Adapter-BERT` or `Hugging Face Adapters` library. Train language adapter via MLM on target language, then task adapter via sentiment fine-tuning.
**Code:**
```python
print("one frozen XLM-R (1.2GB) + language adapters")
for lang in ["en", "hi", "fr", "de", "ja"]:
    print(f"  {lang}-adapter: 8MB (MLM pre-train, then sentiment task)")
```

## Q53: How do you implement sentiment-aware text embeddings for information retrieval?
**A:** Sentiment-aware embeddings for search: 1) Fine-tune Sentence-BERT on sentiment data with contrastive loss (positive pairs: same sentiment). 2) Query embedding + sentiment vector (e.g., `concat([embedding, sentiment_embedding])`). 3) Filter search results by sentiment: retrieve > re-rank by sentiment relevance. 4) Dual encoder: query encoder (text) + sentiment encoder. Example: "Find positive reviews about laptop battery." Query: "laptop battery positive sentiment". Embed query, compute cosine similarity with review embeddings that are sentiment-aware. Benefits: 1) Finds reviews that match both content and sentiment. 2) Enables sentiment filtering without explicit classification. Implementation: 1) SBERT fine-tuned with sentiment triplet loss. 2) FAISS index for similarity search. 3) Hybrid: semantic similarity + sentiment filtering. Performance: sentiment-aware embeddings improve sentiment-specific search precision by 20-30% over general embeddings. Use for: review search, feedback analysis, competitive intelligence.
**Code:**
```python
import numpy as np
emb = np.array([[0.9, 0.1, 0.5], [0.2, 0.8, 0.4], [0.8, 0.3, 0.6]])
sent = np.array([1, -1, 1])
q = np.array([0.85, 0.2, 0.5])
sim = emb @ q
top = np.where(sent == 1)[0]
print("positive matches:", sim[top].argmax(), "filtered by sentiment")
```

## Q54: How do you handle sentiment analysis for figurative language (metaphor, irony)?
**A:** Figurative language sentiment: "This software is a gift from heaven" (metaphor, positive). "My toaster is smarter than this app" (irony, negative). Approaches: 1) BERT: learns figurative patterns from data if training includes figurative examples. 2) Figurative language detection: first detect if figurative (METAPHOR, IRONY), then sentiment. 3) Multi-task: figurative detection + sentiment (shared BERT, task-specific heads). 4) Common sense reasoning: knowledge bases help interpret figurative language (gift from heaven = very good). 5) Large Language Models (GPT-4): better at understanding figurative language. Performance: 1) BERT on literal text: 92% accuracy. 2) BERT on figurative text: 75-80% accuracy (15% drop). 3) BERT after figurative detection: 85% accuracy. 4) GPT-4: 90% on figurative. Best for production: BERT + figurative language classifier (separate model). If figurative is detected, route to special model or human review.
**Code:**
```python
def route(sent, figurative):
    return "LLM/human review" if figurative else "BERT sentiment"
print(route("The app is a gift from heaven", figurative=True))
```

## Q55: How do you implement a BERT sentiment model with multiple training objectives?
**A:** Multi-task BERT for sentiment: 1) Shared BERT encoder. 2) Task heads: a) Sentiment classification (CE loss). b) Sentiment regression (MSE loss). c) Masked language model (MLM loss) - keep pre-training signal. d) Contrastive loss (pull same-sentiment pairs). e) Domain classification (adversarial). f) Aspect extraction (token-level). 3) Joint loss: `L = L_sentiment + 0.5 * L_mlm + 0.1 * L_contrastive + 0.1 * L_domain`. Benefits: 1) MLM prevents catastrophic forgetting of language knowledge. 2) Contrastive improves embedding quality. 3) Adversarial improves domain robustness. 4) Multi-task improves main task by 1-3%. Tradeoffs: 1) Slower training (multiple losses). 2) Memory for multiple heads. 3) Loss weighting needs tuning. Implementation: Hugging Face Trainer with custom loss function. For sentiment-focused models: sentiment + MLM is the most effective multi-task combination.
**Code:**
```python
def loss(sent, mlm, cont, dom):
    return sent + 0.5 * mlm + 0.1 * cont + 0.1 * dom
print("joint loss:", round(float(loss(1.2, 0.8, 0.5, 0.7)), 3))
```

## Q56: How do you implement BERT with graph attention for aspect-based sentiment?
**A:** Graph Attention (GAT) for ABSA: 1) Build graph: nodes = words, edges = dependency relations (nsubj, amod, conj). 2) Node features from BERT (word embeddings). 3) GAT layers: each node attends to neighbors with learned attention weights. 4) Aspect-specific: aspect node attends to relevant context nodes. 5) Readout: aspect node representation -> sentiment classifier. Benefits: 1) Captures syntactic structure (negation scope via dependency edges). 2) Long-range dependencies via graph paths. 3) Interpretable (attention on dependency edges). 4) GAT handles variable graph structure. Performance: BERT + GAT achieves 92-94% F1 on SemEval-2014 Restaurant ABSA, matching or exceeding BERT-ADA. Advantages over pure BERT: 1) Handles long-distance aspect-context relations. 2) Better with complex syntax. 3) More robust to word order variations. Tradeoffs: slower (dependency parsing + GAT layers), requires parser. Best for: syntax-heavy domains (formal text, news).
**Code:**
```python
import networkx as nx
G = nx.DiGraph()
G.add_edges_from([("great", "food"), ("slow", "service")])
print("aspect nodes attend to:", list(G.neighbors("food")))
```

## Q57: How do you implement sentiment analysis for implicit comparative sentences?
**A:** Implicit comparison: "Phone A has a 48MP camera. Phone B is more affordable." Not directly comparative but implies comparison. Approaches: 1) Comparative mention detection: classify if sentence implies comparison. 2) Entity extraction: identify entities being compared (Phone A vs Phone B). 3) Attribute extraction: identify what attribute (camera, price). 4) Preference inference: infer which entity the author prefers. 5) BERT + comparative reasoning: attention across sentences in same review. 6) Discourse analysis: "but" often signals comparison. Example: "I love Phone A's camera. But Phone B is cheaper." Implicit comparison: Phone A (camera = positive), Phone B (price = positive). Preference: unclear (depends on user priorities). BERT with sentence-pair encoding (encode both sentences together) can capture implicit comparisons. Performance: ~70% F1 on implicit comparative extraction. Use for: competitive intelligence (what do customers compare?), product positioning analysis.
**Code:**
```python
s1 = "Phone A has a 48MP camera."
s2 = "Phone B is more affordable."
print("compare attributes: camera(A) vs price(B); preference: context-dependent")
```

## Q58: How do you implement sentiment analysis with a BERT-based scoring model for survey responses?
**A:** Survey sentiment: 1) Open-ended text responses scored -1 to +1. 2) BERT for text encoding. 3) Regression head for continuous score. 4) Connect to Likert scale: map -1 to +1 -> 1-5 stars. 5) Aspect extraction: identify what the respondent is commenting on. 6) Cross-tabulation: sentiment by demographic, segment, question. 7) Drift tracking: sentiment trends over survey waves. 8) Key driver analysis: which aspects most impact overall satisfaction. Implementation: 1) Encode each response with BERT. 2) Predict sentiment score. 3) Aggregate by question: mean score, distribution. 4) Aspect tagging: "The staff was friendly" -> Service. 5) Visualize: sentiment by question, segment, time. BERT regression predicts sentiment within ±0.3 MAE on a -1 to +1 scale. For survey analysis: this provides granular sentiment measurement beyond simple positive/negative classification.
**Code:**
```python
def to_likert(score):
    return max(1, min(5, round((score + 1) * 2)))
for s in [-0.8, 0.1, 0.9]:
    print(s, "->", to_likert(s), "stars")
```

## Q59: How do you implement a BERT sentiment model with input gradient explainability?
**A:** Input gradients for sentiment explanation: 1) Compute gradient of sentiment score w.r.t. each input token's embedding. 2) Gradient magnitude = token importance for sentiment. 3) Positive gradient = token pushed toward positive class. 4) Negative gradient = token pushed toward negative class. 5) Aggregate gradients across embedding dimensions (L2 norm). 6) SmoothGrad: add noise to input multiple times, average gradients (smoother explanations). Implementation: 1) Forward pass -> get sentiment logit. 2) Backward pass -> gradients on token embeddings. 3) `token_importance = grad.norm(dim=1)`. 4) Normalize to [0,1]. 5) Highlight tokens by importance. Benefits: 1) Fast (single backward pass). 2) Faithful to model's computation. 3) Highlights both positive and negative contributors. Comparison with attention: gradients are more faithful than attention weights (attention ≠ importance, debated). Input gradients are state-of-the-art for BERT sentiment explainability.
**Code:**
```python
import torch
x = torch.randn(6, 768, requires_grad=True)
score = (torch.nn.Linear(768, 1)(x)).squeeze().mean()
score.backward()
imp = x.grad.norm(dim=1)
print("token importance:", [round(float(v), 3) for v in imp])
```

## Q60: How do you implement sentiment analysis for economic/financial news with event-based sentiment?
**A:** Event-based financial sentiment: 1) Extract economic events from text: "Fed raises interest rates by 25bps." 2) Map event to financial entities (interest rates, Fed). 3) Sentiment depends on context (rate hike = negative for bonds, positive for banks). 4) Multi-perspective: sentiment toward economy vs sentiment toward specific sectors. Approaches: 1) BERT + event extraction: identify event trigger + arguments. 2) Domain-specific BERT (FinBERT) pre-trained on financial text. 3) Knowledge graph: company-events-sentiment relationships. 4) Numeric sentiment: "profits fell 20%" -> negative. "beat estimates" -> positive. 5) Tone analysis: "cautious optimism" (mixed), "strong headwinds" (negative). FinBERT achieves ~90% accuracy on financial sentiment. Event-based extraction adds structured understanding (not just bag-of-words). Use for: algorithmic trading, portfolio management, risk monitoring.
**Code:**
```python
event = {"trigger": "raises", "object": "interest rates", "amount": "25bps"}
print("entity:", event["object"], "| direction: - bonds, + banks")
```

## Q61: How do you implement BERT for sentiment analysis of user intent in chatbots?
**A:** Conversation sentiment + intent: 1) Real-time sentiment tracking per turn. 2) Intent classification (complain, request, feedback, chitchat). 3) Multi-task: BERT with intent head + sentiment head. 4) Dialogue context: previous N turns fed to BERT. 5) Sentiment-aware response selection: if user is angry, route to senior agent. 6) Escalation trigger: sentiment < threshold for N consecutive turns. Architecture: 1) User utterance -> BERT. 2) [CLS] -> intent classifier (20 intents). 3) [CLS] -> sentiment classifier (3 classes). 4) Additional features: utterance length, response time, history. 5) Decision: based on intent + sentiment + rules. Performance: BERT multi-task achieves ~90% intent accuracy + ~85% sentiment accuracy on conversation data. The multi-task approach improves both tasks (intent helps sentiment, sentiment helps intent). Use for: customer support chatbots, voice assistants, sales bots.
**Code:**
```python
def escalate(intent, sentiment, turns):
    if sentiment == "angry" and turns >= 3:
        return "route to human agent"
    return "respond with bot"
print(escalate("complain", "angry", 4))
```

## Q62: How do you handle sentiment analysis for headlines (clickbait detection)?
**A:** Headline sentiment vs actual sentiment: "You won't believe what happened next!" (headline = excited, but likely clickbait). Approaches: 1) Headline sentiment + article sentiment comparison (clickbait if mismatch). 2) BERT fine-tuned on clickbait dataset (Clickbait Challenge, Webis Clickbait). 3) Features: excessive punctuation (!!!), superlatives (unbelievable), second-person (you). 4) Multi-task: sentiment + clickbait classification. 5) Engagement score: predict how many clicks the headline gets. 6) Misleading sentiment: "This tragedy will make you cry" -> headline sentiment = sad, but actual content may be neutral factual. Challenges: 1) Headlines are short (limited context). 2) Sarcasm in headlines. 3) Cultural norms vary by publication. BERT achieves ~85% F1 on headline clickbait detection. Best practice: if headline sentiment diverges from article sentiment by > threshold, flag as potential clickbait.
**Code:**
```python
h, a = 0.9, 0.1
print("clickbait" if abs(h - a) > 0.5 else "consistent", f"(delta={h - a:.1f})")
```

## Q63: How do you implement BERT with conditional random fields (CRF) for aspect extraction?
**A:** BERT-CRF for aspect extraction: 1) BERT encodes tokens. 2) Linear layer: BERT outputs -> tag scores (B-ASPECT, I-ASPECT, O). 3) CRF layer: learn transition probabilities between tags (e.g., B->I = high, I->O = high, O->B = high, O->I = low). 4) Loss: CRF negative log-likelihood. 5) Decoding: Viterbi algorithm finds best tag sequence. 6) No need for post-processing to fix invalid sequences. Benefits: 1) CRF ensures valid label transitions (no I without B, no B after B). 2) Learns tag dependencies (e.g., aspect is usually 1-3 tokens long). 3) Improves F1 by 2-4% over BERT + softmax. Performance: BERT-CRF achieves ~92% F1 on aspect extraction (SemEval datasets). BERT + softmax: ~88% F1. The CRF adds marginal inference cost but significantly improves sequence consistency. BERT-CRF is the standard for aspect extraction in ABSA.
**Code:**
```python
from torchcrf import CRF as CRF
model = CRF(num_tags=3, batch_first=True)
tags = model.decode([[0.9, 0.1, 0.2], [0.1, 0.8, 0.3],
                     [0.1, 0.2, 0.7]])
print("Viterbi decoding:", [[3 - 1 for _ in t] for t in tags])
```

## Q64: How do you implement a BERT sentiment model that handles temporal expressions (time-aware sentiment)?
**A:** Time-aware sentiment: "The service was terrible in 2020 but improved in 2021." Approaches: 1) Time expression extraction: identify temporal phrases (in 2020, last year). 2) Time-aware encoding: add time embeddings to BERT (concatenate or add). 3) Entity-time-sentiment tuples: (service, 2020, negative), (service, 2021, positive). 4) Sentiment time series: aggregate sentiment by time period. 5) BERT + time features: encode time as special tokens (e.g., "the service was terrible in [YEAR_2020] but improved in [YEAR_2021]"). BERT can learn time-specific sentiment from time features. Performance: time-aware BERT achieves ~85% accuracy on temporally-sensitive sentiment (vs ~75% for vanilla BERT). Use for: product reviews over time, company reputation analysis, trend analysis. The key challenge is associating sentiment with correct time period when multiple periods are mentioned.
**Code:**
```python
pairs = [("2020", "terrible", -1), ("2021", "improved", 1)]
print([{"time": t, "sentiment": s} for t, w, s in pairs])
```

## Q65: How do you implement BERT for sentiment analysis of memes (multimodal)?
**A:** Meme sentiment: text + image. Approaches: 1) ViLT (Vision-and-Language Transformer): unified transformer for text + image. 2) CLIP: separate encoders for text and image, fusion. 3) BERT + ViT: encode text with BERT, image with Vision Transformer, fuse with cross-attention. 4) Meme-specific: detect meme template (Distracted Boyfriend, Drake Hotline Bling) -> template has known sentiment patterns. 5) OCR: extract text overlay from meme. Datasets: Memotion (10K memes, 6 emotion categories). Performance: CLIP-based sentiment achieves ~70% accuracy on memes (vs ~50% for text-only). Challenges: 1) Sarcastic memes (text may be ironic). 2) Cultural references. 3) Image context changes text meaning. Best for: social media monitoring, brand mentions in memes. For production: CLIP + ViLT ensemble achieves best results but is computationally expensive.
**Code:**
```python
from transformers import CLIPModel, CLIPProcessor
cl = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
print("CLIP encoders -> text + image features -> fusion for meme sentiment")
```

## Q66: How do you handle data sparsity for rare sentiment classes in BERT?
**A:** Rare sentiment classes (1% of data). Strategies: 1) Weighted loss: class_weight = total_samples / (num_classes * class_count). 2) Focal loss: gamma=2 focuses on hard examples. 3) Data augmentation: back-translate rare class examples. 4) Prototypical networks: represent each class by its prototype (mean embedding), classify by nearest prototype. 5) Few-shot learning: treat rare classes as few-shot problem (MAML, ProtoNet). 6) Oversampling: replicate rare class examples (risk: overfitting). 7) Mixup: interpolate rare class with other classes. 8) Knowledge distillation: use LLM to generate synthetic rare class examples. For BERT: weighted loss + data augmentation works best. Example: rare sentiment = "disgust" (2% of data). Weight = 1/0.02 = 50. Augment disgust examples via back-translation (5x). Combined approach improves F1 from 0.2 to 0.6 on rare class.
**Code:**
```python
total, cls_count = 10000, 200
w = total / (3 * cls_count)
print("class weight:", round(w, 2))
```

## Q67: How do you implement a BERT model for sentiment with span-based aspect extraction?
**A:** Span-based extraction: predict start and end token indices for each aspect span. Architecture: 1) BERT encodes text. 2) Start classifier: for each token, probability it's an aspect start. 3) End classifier: for each token, probability it's an aspect end. 4) For each valid span (start <= end, max length L): compute span representation (BERT outputs of start to end, pooled). 5) Span sentiment classifier. 6) Loss: start_loss + end_loss + sentiment_loss. Decoding: 1) Predict start/end probabilities. 2) Consider all valid spans. 3) Compute span scores. 4) Non-maximum suppression: keep highest scoring non-overlapping spans. Benefits: 1) Handles multi-word aspects naturally. 2) No BIO tagging needed (no sequential constraints to learn). 3) Can extract overlapping aspects. 4) State-of-the-art on ABSA. Performance: span-based BERT achieves 93% F1 on aspect extraction + 88% on aspect sentiment. Models: Span-ASTE, BART-ABSA.
**Code:**
```python
import torch
s = torch.softmax(torch.randn(8, 2), dim=-1)[:, 1]
e = torch.softmax(torch.randn(8, 2), dim=-1)[:, 1]
best = [(i, j) for i in range(8) for j in range(i, min(i + 3, 8))]
score = [s[i] * e[j] for i, j in best]
print("best span:", best[int(torch.argmax(torch.tensor(score)))])
```

## Q68: How do you implement sentiment analysis with constraint-based learning (knowledge constraints)?
**A:** Constraint-based sentiment: enforce domain knowledge during training. Constraints: 1) "not good" = NOT positive (negation constraint). 2) "but" after positive -> negative dominates (contrastive constraint). 3) If aspect X is mentioned with word Y, sentiment = Z (domain rule). Implementation: 1) Regularized loss: L_total = L_supervised + lambda * L_constraint. 2) Constraint loss: penalize violation of known rules. 3) Convert constraints to differentiable functions: if input has "not good", penalty if model predicts positive. 4) Posterior regularization: constrain model's predictions to satisfy expected label proportions. 5) Logic tensor networks: integrate logical rules with neural networks. Benefits: 1) Improves accuracy with limited data. 2) Enforces domain-specific patterns. 3) Reduces obvious errors. Constraints are most useful when data is limited but domain knowledge is available. For BERT: constraint-based learning improves low-resource sentiment by 5-10%.
**Code:**
```python
def constraint_penalty(text, probs):
    if "not good" in text and probs[0] > probs[1]:
        return abs(probs[0] - probs[1])  # penalize predicting positive
    return 0.0
print("penalty:", round(float(constraint_penalty("not good", [0.8, 0.2])), 2))
```

## Q69: How do you implement BERT for sentiment in low-resource environments (no GPU)?
**A:** CPU-only BERT sentiment: 1) DistilBERT ONNX Runtime INT8: ~10ms per inference on modern CPU. 2) ALBERT-xxlarge INT8: ~15ms. 3) MiniLM (Microsoft): ~5ms, ~95% of BERT accuracy. 4) Fastformer: linear attention, ~2ms. 5) Pruned BERT: remove 40% heads, fine-tune, ~6ms. 6) Static quantization: pre-compute quantization scales (no calibration data needed). 7) Threading: ONNX Runtime with multi-threading (OMP_NUM_THREADS). 8) Batch processing: process multiple inputs together for CPU efficiency. Comparisons (~Sentence length=50): 1) BERT-base FP32 ONNX: ~50ms. 2) DistilBERT FP32 ONNX: ~20ms. 3) DistilBERT INT8 ONNX: ~8ms. 4) MiniLM INT8 ONNX: ~4ms. 5) FastText: ~0.01ms (but much lower accuracy). For CPU-only production: MiniLM or DistilBERT INT8 ONNX provides the best accuracy/speed tradeoff.
**Code:**
```python
import onnxruntime as ort
sess = ort.InferenceSession("mini_model.onnx", providers=["CPUExecutionProvider"])
print("CPU inference with MiniLM INT8 ONNX: ~4ms per sample")
```

## Q70: How do you implement sentiment analysis with knowledge distillation from large to small model?
**A:** Distill BERT-large (teacher) to DistilBERT (student). Process: 1) Teacher (BERT-large) predicts on large unlabeled dataset. 2) Soft labels = teacher's softmax probabilities (temperature-scaled, T=5). 3) Student is trained on: a) Soft target loss: KL divergence with teacher's soft labels. b) Hard target loss: cross-entropy with true labels (if available). c) Hidden state loss: MSE between student and teacher hidden states (optional, improves quality). 4) Distillation loss: `L = alpha * KL(teacher_soft, student_soft) + (1-alpha) * CE(student, true_label)`. Alpha = 0.7 typically. Benefits: 1) Student learns teacher's generalization patterns. 2) Student is 40% smaller, 60% faster but retains 96-98% of teacher's accuracy. 3) Unlabeled data is sufficient for distillation (no labels needed). Sentiment-specific: distill BERT-large (94% SST-2) to DistilBERT (93% SST-2). The distilled model captures the teacher's superior sentiment understanding. Best for: improving small model accuracy without more labeled data.
**Code:**
```python
import torch.nn.functional as F
L = 0.7 * F.kl_div(F.log_softmax(torch.randn(1, 3), dim=-1),
                   torch.randn(1, 3), reduction="batchmean")
print("distillation soft-target loss:", round(float(L), 3))
```

## Q71: How do you implement sentiment analysis for product features with opinion summarization?
**A:** Opinion summarization: 1) ABSA per review. 2) Aggregate by feature (camera, battery, screen). 3) Summarize sentiments: "Camera: 80% positive (24 reviews), 10% negative (3 reviews), 10% neutral. Customers praise image quality but criticize low-light performance." 4) Extractive: select representative quotes per feature. 5) Abstractive: fine-tune T5 on review-summary pairs. 6) Aspect hierarchy: features -> sub-features (camera -> image quality, zoom, video). Implementation pipeline: 1) Preprocess reviews. 2) ABSA (BERT-based). 3) Cluster aspect terms to canonical features. 4) Aggregate sentiment per feature. 5) Select key quotes (extractive) or generate text (abstractive). Metrics: 1) Aspect coverage (% of reviews with extracted aspects). 2) Sentiment accuracy per aspect. 3) Summary quality (ROUGE, human evaluation). Use for: e-commerce product pages, competitive analysis, voice of customer programs.
**Code:**
```python
aggregate = {"camera": {"pos": 24, "neg": 3, "neu": 3},
             "battery": {"pos": 20, "neg": 5, "neu": 5}}
for f, s in aggregate.items():
    print(f, round(s["pos"] / sum(s.values()), 0))
```

## Q72: How do you implement BERT for sentiment with progressive loading (streaming)?
**A:** Streaming sentiment: process text as it arrives (not wait for full text). Approaches: 1) Segment-level: process chunks, aggregate (weighted by position). 2) BERT on each sentence, combine with temporal decay (recent sentences matter more). 3) Streaming BERT: maintain running state of seen tokens (not standard BERT, uses prefix attention). 4) Sliding window: last 512 tokens, updated as new tokens arrive. 5) Live sentiment: initial prediction based on first sentence, update as each new sentence arrives. 6) Event-driven: emit sentiment events (on significant change). For real-time: 1) Process first 100 tokens -> initial sentiment. 2) Add tokens as they arrive (re-inference every N tokens). 3) If sentiment changes > threshold, emit update. Latency: initial sentiment in < 100ms (first tokens), updates every 50ms. Tradeoff: more frequent updates = more compute. Best for: live chat monitoring, real-time social media, streaming audio transcription sentiment.
**Code:**
```python
segs = ["great product", "but support is bad", "overall ok"]
prev, score = None, 0.0
for s in segs:
    prev = s[:20]  # incremental context window
    print("live window:", prev)
```

## Q73: How do you implement BERT for multi-label aspect-sentiment with label correlation?
**A:** Aspect-sentiment multi-label: each aspect (food, service) has a sentiment (positive, negative). Labels = {food_pos, food_neg, food_neu, service_pos, ...}. Label correlations: 1) food_pos and service_neg may co-occur (mixed review). 2) food_neg and food_pos cannot both be true (mutually exclusive). Architecture: 1) BERT encoder. 2) N heads (one per aspect). 3) Each head: linear(768, 3) -> softmax (pos/neg/neu per aspect). 4) Label correlation: add a label correlation layer (bilinear or graph network) that models interactions between aspect heads. 5) Loss: sum of cross-entropy per aspect. Inference: 1) Run BERT. 2) Per aspect, argmax over pos/neg/neu. 3) Output: {food: positive, service: negative, ambiance: neutral}. Performance: label correlation modeling improves multi-label F1 by 2-3% over independent heads. The main benefit: if food is positive, service is more likely to be positive (correlation), but model should learn not to over-rely on this.
**Code:**
```python
heads = {"food": [0.9, 0.1, 0.0], "service": [0.1, 0.9, 0.0]}
print({k: ["pos", "neg", "neu"][v.index(max(v))] for k, v in heads.items()})
```

## Q74: How do you implement a sentiment analysis system that explains predictions using counterfactuals?
**A:** Counterfactual explanations: "If the text said 'good' instead of 'bad', the prediction would change from negative to positive." Approaches: 1) Minimum edit: find minimal word changes that flip prediction. 2) BERT-based: replace words with BERT-suggested alternatives, find those that flip prediction. 3) Polyjuice: fine-tuned GPT model that generates counterfactuals given original text + target label. 4) Feature attribution: identify tokens whose removal/replacement changes prediction (via SHAP/Integrated Gradients). 5) Example-based: find nearest training example with different label. Implementation: 1) Given input text and prediction. 2) Search for minimum word changes that change prediction to target class. 3) Return: "If we change 'terrible' to 'great', the sentiment changes from negative to positive." Benefits: 1) Human-understandable explanations. 2) Reveals model's decision boundaries. 3) Useful for debugging (model focusing on wrong words). Performance: counterfactual generation takes 1-5 seconds per instance (iterative search). Use for: high-stakes sentiment (content moderation, financial analysis) where explainability is critical.
**Code:**
```python
from transformers import pipeline
mlm = pipeline("fill-mask", model="distilbert-base-uncased")
for r in mlm("the movie was [MASK]", top_k=3):
    print(r["token_str"], "->", "flips to positive" if r["token_str"].startswith(("great", "good")) else "stays negative")
```

## Q75: How do you implement BERT for sentiment analysis with integrated commonsense knowledge?
**A:** Commonsense for sentiment: "The car won't start" -> negative (commonsense: not starting = bad). Approaches: 1) COMET (commonsense transformer): generate commonsense inferences from text. Concatenate with BERT. 2) ConceptNet: retrieve related concepts, inject embeddings. 3) ATOMIC: event-effect knowledge (If X happens, Y feels). 4) BERT + knowledge graph attention: attend to relevant knowledge graph nodes. Implementation: 1) Encode text with BERT. 2) Retrieve relevant commonsense (COMET generates "won't start" -> effect: "feels frustrated"). 3) Encode commonsense with separate BERT/encoder. 4) Fuse with cross-attention. 5) Classify. Benefits: 1) Handles implicit sentiment better (sentiment implied by situation). 2) Improves low-resource performance. 3) More robust. Performance: BERT + COMET improves implicit sentiment accuracy by 3-5%. The cost is additional latency (COMET forward pass) and complexity. For most sentiment tasks, BERT alone captures enough implicit sentiment from pre-training.
**Code:**
```python
cs = {"car_wont_start": "feels frustrated", "win_lottery": "feels happy"}
text = "The car won't start."
print("inferred effect:", cs.get(text.replace(".", ""), "neutral"))
```
## Q76: How do you implement a BERT sentiment model with dynamic class weighting?
**A:** Dynamic weighting adjusts class weights during training: 1) Start with uniform weights. 2) Track class accuracy during training. 3) Increase weight for classes with lower accuracy. 4) Formula: `weight_c = (1 - accuracy_c) / sum(1 - accuracy_i)`. 5) Update every N steps (e.g., 100). Benefits: 1) Adapts to class difficulty (not just frequency). 2) Focuses training on hard classes. 3) Handles both imbalance AND difficulty. For sentiment: 1) Neutral class often has lower accuracy (harder). 2) Dynamic weighting increases neutral weight. 3) Improves neutral F1 by 2-4%. Implementation: 1) Maintain running accuracy per class. 2) Compute weights after each epoch. 3) Apply weights to cross-entropy loss. 4) Option: combine with frequency-based weighting for initialization. Dynamic weighting is more robust than fixed weighting because it responds to actual model performance.
**Code:**
```python
acc = {"pos": 0.95, "neg": 0.93, "neu": 0.80}
weights = {c: (1 - a) / sum(1 - x for x in acc.values()) for c, a in acc.items()}
print(weights)
```

## Q77: How do you implement BERT for sentiment with contrastive learning on sentence-pair tasks?
**A:** Sentence-pair sentiment (e.g., review helpfulness, contradiction): 1) Two sentences input (separated by [SEP]). 2) BERT encodes pair. 3) [CLS] -> pair classification. 4) Contrastive learning: a) Positive pairs: same label (both positive reviews). b) Negative pairs: different labels. c) Same BERT encodes both. d) Contrastive loss: pull same-label pairs together, push different apart. Use for: 1) Review helpfulness: does sentence A describe same aspect as sentence B? 2) Sentiment consistency: do two reviews about same product have same sentiment? 3) Contradiction detection: two reviews contradict each other? Benefits: 1) Learns better pair representations. 2) 1-2% improvement on pair classification tasks. Performance: BERT + contrastive achieves 85% F1 on sentiment contradiction detection (SNLI-based sentiment). Implementation: 1) Batch construction: within batch, create pairs by combining sentences with same/different labels. 2) Contrastive loss + classification loss. 3) Joint training.
**Code:**
```python
import torch
a = torch.randn(3, 4, requires_grad=True)
y = torch.tensor([0, 0, 1])
sim = a @ a.T
L = torch.stack([-sim[i][y == y[i] and i != j].mean() for i in range(3)
                 for j in range(3) if y[i] == y[j] and i != j]).mean()
print("pair contrastive loss:", round(float(L), 3))
```

## Q78: How do you implement sentiment with weak supervision using multiple heuristics?
**A:** Weak supervision combines multiple noisy label sources: 1) Heuristics: VADER, sentiment lexicons, rule patterns ("excellent" -> positive), emoji-based. 2) Labeling functions: functions that return label or abstain. 3) Snorkel: model labeling function accuracies and correlations (generative model). 4) Probabilistic training labels from the generative model. 5) Train BERT on probabilistic labels. Example labeling functions: 1) If compound > 0.5: positive. 2) If "not" + "good": negative. 3) If contains "bad": negative. 4) If ratio of positive to negative lexicon words > 2: positive. 5) If emoji in ["😂", "😡"]: negative. Snorkel learns: 1) Accuracy of each labeling function. 2) Correlations between functions. 3) Outputs: probabilistic labels for unlabeled data. Results: BERT trained on Snorkel labels achieves ~85% of supervised accuracy (vs ~75% for single heuristic). Weak supervision enables sentiment model training without manual labels.
**Code:**
```python
import snorkel.labeling.options as opt
def lf_vader(x): return 1 if x["compound"] > 0.5 else 0
def lf_bad(x): return 0 if "bad" in x["text"] else opt.ABSTAIN
print("labeling functions -> Snorkel generative model -> BERT training labels")
```

## Q79: How do you handle sentiment for languages with complex morphology (Arabic, Finnish)?
**A:** Complex morphology: words have many forms (Arabic: root + pattern, Finnish: 15+ cases). Challenges: 1) Tokenization splits verbs/adjectives into morphemes, losing sentiment. 2) One word may encode negation, tense, subject. 3) Root-based sentiment: root K-T-B (write) may appear in "kitab" (book), "maktab" (office), "kataba" (he wrote). Approaches: 1) Morphologically-aware tokenization: keep meaningful morphemes together. 2) Stemming/lemmatization: reduce to root, apply sentiment at root level. 3) mBERT/XLM-R: subword tokenization handles morphology to some extent. 4) Language-specific BERT: AraBERT (Arabic), FinBERT (Finnish) - pre-trained on morphological data. 5) Character-level: bypass morphology entirely (less effective). For Arabic: AraBERTv2 achieves ~90% on Arabic sentiment benchmarks. mBERT achieves ~85%. For Finnish: FinBERT ~88% vs mBERT ~80%. Use language-specific BERT for best results on morphologically complex languages.
**Code:**
```python
root = {"ktb": ["kitab (book)", "maktab (office)", "kataba (wrote)"]}
print("root K-B-T:", root["ktb"])
```

## Q80: How do you implement a BERT model that predicts both sentiment and its intensity?
**A:** Joint sentiment + intensity: 1) Multi-task: sentiment class (3-class) + intensity regression (continuous, e.g., 0.0-1.0). 2) Ordinal: intensity as ordered categories (very negative, negative, neutral, positive, very positive). 3) Multi-head: BERT encoder + class head (softmax 3) + intensity head (sigmoid 1). 4) Loss: `L = CE(class) + MSE(intensity)`. 5) Constraint: if class = positive, intensity should be > 0.5. If neutral, intensity = 0.5. Data: some datasets include intensity (SST-5, VADER scores). Performance: joint model improves intensity prediction by 5-10% over two-stage (classify then predict intensity). The shared representation learns that intensity correlates with class confidence. Use for: nuanced sentiment analysis where both direction and strength matter (surveys, social media monitoring). Inference: class determines direction, intensity determines strength.
**Code:**
```python
import torch
hidden = torch.randn(1, 768)
cls = torch.softmax(torch.nn.Linear(768, 3)(hidden), dim=1)
intensity = torch.sigmoid(torch.nn.Linear(768, 1)(hidden))
print("class:", cls.argmax().item() - 1, "| intensity:", round(float(intensity), 2))
```

## Q81: How do you implement BERT for sentiment with attention-based document representation?
**A:** Attention-based document representation: 1) Encode each sentence with BERT. 2) Sentence-level attention: learn which sentences are most important for document sentiment. 3) Attended sentence sum -> document embedding -> classifier. 4) Position-aware attention: first and last sentences often carry more weight. Architecture: 1) BERT per sentence: [CLS] sentence_i = sent_emb_i. 2) Sentence attention: `alpha_i = softmax(W * tanh(sent_emb_i * V + b))`. 3) `doc_emb = sum(alpha_i * sent_emb_i)`. 4) Classification. Benefits: 1) Handles arbitrary-length documents. 2) Attention shows which sentences drive sentiment. 3) Better than mean pooling or truncation. Performance: hierarchical attention BERT improves long document sentiment by 3-5% over truncated BERT. The attention mechanism typically assigns higher weight to first and last sentences (where main opinion often appears).
**Code:**
```python
import torch
embs = torch.randn(4, 768).view(4, 768)
V = torch.randn(1024, 768); w = torch.randn(1024); b = torch.randn(1024)
scores = (torch.tanh(embs @ V.T + b) @ w)
attn = torch.softmax(scores, dim=0)
print("sentence attention:", [round(float(a), 3) for a in attn])
```

## Q82: How do you implement BERT for cross-lingual sentiment without parallel data?
**A:** Cross-lingual without parallel data: 1) Sentence embedding alignment: use unsupervised alignment (VecMap, MUSE) to map sentiment embeddings across languages. 2) Adversarial training: train BERT to produce language-invariant sentiment representations. Domain-adversarial loss: language classifier tries to predict language, BERT tries to fool it. 3) Self-training: predict on target language with high confidence, add as pseudo-labels. 4) Cross-lingual contrastive: pull same-sentiment examples together across languages (requires only sentiment labels, not parallel data). 5) Initialize with XLM-R (multilingual pre-trained). 6) Iterative refinement: alternately train on source labels + refine target pseudo-labels. Performance: XLM-R + unsupervised alignment achieves ~80% of supervised cross-lingual performance. Best for: language pairs where no parallel data or target labels exist. The adversarial approach reduces language bias in sentiment representations.
**Code:**
```python
import torch
class GradReverse(torch.autograd.Function):
    @staticmethod
    def forward(ctx, x): return x
    @staticmethod
    def backward(ctx, g): return -g
loss = torch.nn.functional.cross_entropy(
    torch.nn.Linear(768, 2)(GradReverse.apply(torch.randn(4, 768))),
    torch.tensor([0, 1, 0, 1]))
print("adversarial language loss:", round(float(loss), 3))
```

## Q83: How do you implement BERT for sentiment analysis with hierarchical label taxonomy?
**A:** Hierarchical labels: 1) Level 1: positive/negative/neutral. 2) Level 2 (under positive): joy, love, surprise. Level 2 (under negative): anger, sadness, fear. 3) Level 3: fine-grained emotions. Architecture: 1) BERT encoder. 2) Level 1 classifier. 3) For each Level 1 class, separate Level 2 classifier (or single multi-task with 6 outputs). 4) Hierarchical loss: `L = L_level1 + L_level2`. 5) During inference: Level 1 prediction determines which Level 2 classifier to use. Benefits: 1) Coarse classes have more training data. 2) Fine-grained classes benefit from coarse class information. 3) More interpretable than flat 7-class classification. 4) Handles class imbalance (rare fine emotions share data with common coarse). Performance: hierarchical BERT improves fine-grained emotion F1 by 3-5% over flat classification. The hierarchy provides inductive bias that coarse sentiment helps fine-grained.
**Code:**
```python
def infer(l1, l2_head):
    return "negative -> " + ["anger", "sadness", "fear"][l2_head]
print(infer("negative", 1))
```

## Q84: How do you implement sentiment with BERT-inspired feature extraction for rule-based systems?
**A:** BERT as feature extractor for rule systems: 1) Extract BERT embeddings as features. 2) Use interpretable models on top (logistic regression, decision tree). 3) SHAP on the interpretable model to explain predictions. 4) Combine BERT features with hand-crafted features (lexicon scores, negation flags, POS tags). 5) Rule extraction: train a decision tree on BERT embeddings, extract rules. Process: 1) Encode text with BERT (get [CLS] embedding). 2) Reduce dimension (PCA to 50 dims). 3) Train logistic regression. 4) Extract top weighted features. 5) Map feature weights back to words (via influence on [CLS]). Benefits: 1) More interpretable than pure BERT. 2) Maintains BERT's accuracy. 3) Rule extraction provides explicit decision logic. Performance: BERT + logistic regression achieves ~90% of pure BERT accuracy but is fully interpretable. Best for: regulated industries (finance, healthcare) requiring explainable AI.
**Code:**
```python
from sklearn.linear_model import LogisticRegression
import numpy as np
X = np.random.randn(100, 50); y = (X[:, 0] > 0).astype(int)
clf = LogisticRegression().fit(X, y)
print("top weighted feature:", int(np.argmax(clf.coef_[0])))
```

## Q85: How do you implement BERT for sentiment with Bayesian optimization for hyperparameters?
**A:** Hyperparameter optimization for BERT sentiment: 1) Parameters: learning_rate (1e-5 to 5e-5), batch_size (8-64), warmup_ratio (0.0-0.2), weight_decay (0.0-0.1), dropout (0.1-0.3), num_epochs (2-5). 2) Bayesian optimization (Optuna, Hyperopt): a) Define search space. b) Sample hyperparameters. c) Train BERT. d) Evaluate on validation F1. e) Fit surrogate model (Gaussian Process). f) Acquisition function (EI, UCB) selects next parameters. g) Repeat for 20-50 trials. 3) Pruning: stop poor trials early (median pruner). Results: 1) Bayesian optimization finds parameters 2-3% better than default BERT settings for specific domains. 2) Learning rate and batch size are most important. 3) Optimal: lr=3e-5, batch=32, warmup=0.1, weight_decay=0.01, dropout=0.1, epochs=3. Bayesian optimization is more efficient than grid search (20 trials vs 100+ for grid).
**Code:**
```python
import optuna
def objective(trial):
    lr = trial.suggest_float("lr", 1e-5, 5e-5, log=True)
    bs = trial.suggest_int("batch_size", 8, 64, log=True)
    return -(0.91 + 0.05 * (lr / 5e-5) - 0.01 * (1 - bs / 64))
study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=5)
print("best trial:", study.best_trial.params)
```

## Q86: How do you implement BERT for sentiment with data deduplication?
**A:** Deduplication prevents overfitting from repeated data: 1) Exact dedup: remove identical texts (common in scraped data). 2) Near-dedup: remove very similar texts (MinHash LSH, SimHash). 3) Conflict detection: if same text has different labels, investigate (noise flag). 4) Source dedup: if same review appears on multiple sites. 5) Template dedup: reviews from the same template (e.g., Amazon Vine). Impact: 1) Removing duplicates prevents overfitting (2-3% validation accuracy improvement). 2) Reduces training time (less data). 3) Better generalization. Implementation: 1) MinHash: create signature per text. 2) LSH: bucket similar signatures. 3) Within bucket: keep one sample per near-identical group. 4) For sentiment: aggressive dedup helps (reviews often auto-generated, spammed). Remove: 1) Exact duplicates. 2) >90% cosine similarity in BERT embedding space. 3) Reviews with same text but different ratings (label noise).
**Code:**
```python
texts = ["Great product", "Great product", "Great prduct", "Terrible."]
norm = [t.lower() for t in texts]
keep = list(dict.fromkeys(norm))
print("dedup size:", "texts:", len(texts), "-> kept:", len(keep))
```

## Q87: How do you implement BERT for sentiment in a federated learning setting?
**A:** Federated sentiment: train across devices without centralizing data. 1) Server distributes BERT model to devices. 2) Devices fine-tune on local data (local reviews). 3) Devices send model updates (gradients), not raw data. 4) Server aggregates updates (FedAvg, FedProx). 5) Repeat rounds. Challenges: 1) Communication cost: BERT is large (440MB). Use DistilBERT (200MB) or FedML compression. 2) Data heterogeneity: device data is non-IID (one device may have only positive reviews). 3) Stragglers: slow devices delay training. 4) Privacy: gradients may leak information (use differential privacy). Implementation: 1) Use Flower or TensorFlow Federated. 2) DistilBERT on-device (smaller, faster). 3) FedProx for heterogeneous data. 4) Differential privacy (clip gradients, add noise). Performance: federated BERT achieves ~90% of centralized accuracy after 100 rounds. Best for: privacy-sensitive sentiment (personal messages, healthcare feedback). Gradient inversion attacks can reconstruct data from BERT gradients - always add DP noise.
**Code:**
```python
import numpy as np
def fedavg(grads):
    return [np.mean([g[i] for g in grads], axis=0) for i in range(len(grads[0]))]
print("aggregated update shape:", np.array(fedavg([np.random.randn(10)
                                                   for _ in range(3)])).shape)
```

## Q88: How do you implement a BERT-based question-answering system for sentiment insights?
**A:** Sentiment QA: ask questions about sentiment in text. "What did the customer say about the battery?" -> "The battery life is amazing." Approaches: 1) Extractive QA: BERT QA model (SQuAD variant) trained on sentiment QA data. Input = question + review. Output = answer span. 2) Abstractive QA: T5 generates answer. 3) Aspect-specific: filter text to aspect-related sentences, then QA. 4) Multi-hop: "Why did the customer give 1 star?" -> Answer spans showing specific complaints. 5) Aggregative: "What do customers say about the camera?" -> Generate summary from multiple reviews. Performance: BERT QA achieves ~80% F1 on sentiment QA with limited training data. Use for: interactive sentiment analysis, analyst tools, customer feedback exploration. The key challenge is creating QA training data (question-answer pairs from reviews). Generate automatically: for each aspect in review, create Q/A pair.
**Code:**
```python
from transformers import pipeline
qa = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")
ans = qa({"question": "What about the battery?",
          "context": "The battery life is amazing but it is heavy."})
print("answer:", ans["answer"])
```

## Q89: How do you implement BERT for sentiment with curriculum learning?
**A:** Curriculum learning: train on easy examples first, gradually increase difficulty. For sentiment: 1) Easy: short text, explicit sentiment words (good, bad). 2) Medium: longer text, some negation, no sarcasm. 3) Hard: sarcasm, complex negation, mixed sentiment, long context. 4) Train BERT sequentially on easy, then easy+medium, then all data. 5) Difficulty scoring: a) Text length (shorter = easier). b) Sentiment intensity (stronger = easier). c) Model confidence (high confidence = easier). d) Manual difficulty labels. Benefits: 1) Faster convergence (starts with clean signal). 2) Better final accuracy (1-2% improvement). 3) Reduces catastrophic forgetting. Implementation: 1) Score each training example for difficulty. 2) Sort by difficulty. 3) Train: epochs 1-2 on top 30% (easy). Epochs 3-4 on top 60%. Epochs 5-6 on all data. 4) Alternatively: increase difficulty within each epoch (batch sampling from easy to hard). Curriculum BERT learns sentiment patterns more systematically.
**Code:**
```python
def difficulty(text):
    return 3 if "not good" in text else 1
data = ["great", "not good", "ok"]
print(sorted(data, key=difficulty))
```

## Q90: How do you handle sentiment analysis for hate speech detection (binary classification)?
**A:** Hate speech detection: classify text as hate speech or not. Challenges: 1) Hate speech vs offensive vs free speech boundaries. 2) Sarcastic hate speech. 3) Code words (dog whistles). 4) Context-dependent. Approaches: 1) BERT fine-tuned on hate speech datasets (HateXplain, Founta, Davidson). 2) Multi-task: hate speech + target group + severity. 3) Counter-narrative generation: generate non-hateful alternatives. 4) Explainable hate detection: highlight words contributing to classification (SHAP, Integrated Gradients). 5) Bias mitigation: ensure model doesn't flag dialect-specific terms (AAVE) as hate speech. Performance: BERT-base achieves ~90% F1 on hate speech benchmarks. Challenges: 1) Low agreement between annotators (0.6 kappa). 2) Concept drift (new hate speech patterns emerge). 3) Over-sensitivity (false positives on dialect). Best practice: 1) Use multiple datasets for training. 2) Regular evaluation on diverse groups. 3) Human-in-the-loop for edge cases.
**Code:**
```python
def classify(text, shape):
    # shape: (n,) hate logits
    print("hate" if shape.mean() > 0.5 else "non-hate")
    return "evidence via SHAP highlights"
import numpy as np
print(classify("stop calling me that", np.random.randn(5)))
```
## Q91: How do you implement BERT for sentiment with RAG (Retrieval-Augmented Generation)?
**A:** RAG for sentiment: 1) Retrieve relevant documents/examples for input text. 2) Augment BERT input with retrieved context. 3) Classify based on augmented input. Use cases: 1) Cross-domain sentiment: retrieve labeled examples from similar domain, use as context. 2) Sentiment with evidence: retrieve product specs as context for review sentiment. 3) Few-shot: retrieve labeled examples with similar text, predict based on nearest neighbors. Architecture: 1) Encode input with BERT. 2) Retrieve top-K similar examples from labeled database (FAISS). 3) Concatenate retrieved examples: `[CLS] input [SEP] retrieved_example_1 [SEP] retrieved_example_2`. 4) Classify. Benefits: 1) Dynamic adaptation without retraining. 2) Handles rare/novel patterns (retrieves similar known cases). 3) More robust. Performance: RAG-BERT improves sentiment accuracy by 2-5% on cross-domain tasks. For in-domain: marginal improvement. Best for: domain adaptation, handling edge cases, providing evidence for predictions.
**Code:**
```python
import faiss
emb = faiss.IndexFlatIP(384)
emb.add(__import__("numpy").random.randn(1000, 384))
retrieved = emb.search(__import__("numpy").random.randn(1, 384), k=3)
print("retrieved indices:", retrieved[1][0])
```

## Q92: How do you implement BERT for sentiment in low-resource settings with multi-task learning and auxiliary tasks?
**A:** Multi-task with auxiliary tasks for low-resource sentiment: 1) Main task: sentiment classification (few labels). 2) Auxiliary tasks (more data available): a) Language modeling (MLM): unlabeled text is abundant. b) Emotion classification (if some emotion labels exist). c) Polarity detection (lexicon-based noisy labels). d) Aspect extraction (if aspect labels exist). e) Sarcasm detection (if sarcasm labels exist). 3) Shared BERT encoder. 4) Task-specific heads. 5) Joint training: aim to improve main task via shared representations. Benefits: 1) Auxiliary tasks provide additional training signal. 2) MLM prevents overfitting to small labeled set. 3) Related tasks (emotion) improve sentiment understanding. Performance: with 100 sentiment-labeled examples + 10K unlabeled examples (MLM), multi-task BERT achieves ~85% accuracy (vs ~78% for sentiment-only). Best auxiliary task: MLM (easy to get unlabeled data). For domain-specific: domain-adaptive MLM is most effective.
**Code:**
```python
def joint_loss(sent, mlm, emotion):
    return sent + 0.5 * mlm + 0.3 * emotion
print("multi-task low-resource loss:", round(float(joint_loss(1.0, 0.6, 0.8)), 3))
```

## Q93: How do you implement BERT for sentiment with SHAP model explanations?
**A:** SHAP for BERT sentiment: 1) Input: text. 2) Compute SHAP values for each token. 3) Positive SHAP = pushes toward positive class. 4) Negative SHAP = pushes toward negative class. 5) Aggregation: sum per token SHAP values across embedding dimensions. Implementation: 1) `shap.Explainer(model, tokenizer)` for BERT. 2) Partition SHAP: explains by partitioning input into subsets. 3) Output: token-level SHAP values. 4) Visualization: text highlighting (red for positive, blue for negative). SHAP advantages: 1) Game-theoretically grounded (unique, additive, consistent). 2) Handles feature interactions (BERT's non-linearities). 3) Global explanations: aggregate SHAP values across dataset to find most important words overall. For sentiment: SHAP typically highlights sentiment-bearing words correctly ("great" positive SHAP, "terrible" negative SHAP). Use SHAP for: model debugging, bias detection (are protected attributes influencing predictions?), trust building with stakeholders.
**Code:**
```python
import shap
explainer = shap.Explainer(lambda x: 0.5 * x.mean(1).reshape(-1, 1),
                           np.random.randn(20, 384))
vals = explainer(np.random.randn(3, 384))
print("SHAP shape:", vals.values.shape)
```

## Q94: How do you implement sentiment for multi-modal brand monitoring (text + images)?
**A:** Brand monitoring across modalities: 1) Text: mentions, reviews, comments (BERT sentiment). 2) Images: logo detection (YOLO) + image sentiment (CLIP). 3) Video: transcribe speech (Whisper) -> text sentiment + visual sentiment (frames). 4) Social: emoji sentiment, meme sentiment. 5) Fusion: weighted combination of modality-specific sentiment scores. Pipeline: 1) Crawl: collect mentions from social media, news, forums. 2) Process per modality: a) Text: BERT sentiment. b) Image: CLIP zero-shot sentiment for brand-related content. c) Emoji: emoji sentiment lexicon. 3) Brand entity linking: ensure sentiment is about the brand (not just mention). 4) Aggregate: overall brand sentiment per day. 5) Alert: sentiment spikes (positive or negative). Challenges: 1) Entity disambiguation (Apple the company vs Apple the fruit). 2) Cross-modal sarcasm (image has positive brand, text is sarcastic). 3) Scale (billions of posts/day requires distributed processing). Use: Klarna, Sprout Social, Brandwatch platforms.
**Code:**
```python
txt = 0.7; img = -0.3; video = 0.4
fusion = 0.6 * txt + 0.3 * img + 0.1 * video
print("brand sentiment:", round(float(fusion), 2), "(spike alert if > 0.5)")
```

## Q95: How do you implement BERT for sentiment with one-class learning (only positive data)?
**A:** One-class sentiment: only have positive examples (no negative labels). Approaches: 1) One-class SVM on BERT embeddings. 2) Deep SVDD (Deep Support Vector Data Description): minimize hypersphere volume around normal (positive) embeddings. 3) Autoencoder + reconstruction error: positive data reconstructs well, negative data reconstructs poorly. 4) Self-supervised: create negative data via corruption (shuffle words, replace sentiment words with antonyms). 5) VADER: use pre-defined lexicon (no training needed). 6) Zero-shot: use NLI-based sentiment without training data. For one-class BERT: 1) Extract [CLS] embeddings from positive data. 2) Compute mean embedding (prototype). 3) Score = cosine similarity to prototype + threshold. 4) Negative = score < threshold. 5) Alternatively: train autoencoder on positive data, reconstruction error = anomaly score. Performance: one-class BERT achieves ~75% F1 on sentiment detection (vs ~92% for supervised). Useful when labeling negative data is expensive (all reviews are positive, need to detect fake/harmful reviews).
**Code:**
```python
import torch.nn.functional as F
import torch
pos = torch.randn(100, 384); proto = pos.mean(dim=0)
for text in ["great product", "this is a scam"]:
    score = F.cosine_similarity(torch.randn(384), proto, dim=0)
    print(text, "->", round(float(score), 2),
          "anomaly" if score < 0.5 else "normal")
```

## Q96: How do you implement BERT for sentiment with neural architecture search (NAS)?
**A:** NAS for sentiment BERT: search for optimal architecture variations. Search space: 1) Number of transformer layers (6, 12). 2) Hidden size (512, 768). 3) Attention heads (8, 12). 4) FFN intermediate size (1024, 2048, 3072). 5) Dropout rate (0.1, 0.2). 6) Classification head architecture (1-layer vs 2-layer). Search method: 1) Weight-sharing NAS (ENAS, DARTS): train super-network of all architectures, derive best. 2) Evolutionary: population of architectures, mutate/crossover, evaluate. 3) Bayesian optimization: sample architectures, train, fit surrogate model. Results for sentiment: 1) DistilBERT (6 layers, 768 dim) is near-optimal for accuracy/speed. 2) Reducing to 384-dim drops accuracy by 2%. 3) 3-layer TinyBERT is optimal for edge. NAS suggests: for sentiment, 8 attention heads suffice (not 12). FFN 2048 (not 3072). This gives 30% speedup with <0.5% accuracy loss. NAS is overkill for most sentiment projects (use off-the-shelf BERT variants).
**Code:**
```python
configs = [(6, 768, 8), (12, 768, 12), (4, 384, 8)]
best = max(configs, key=lambda c: 0.5 * c[1] / 768 - 0.1 * c[0])
print("chosen arch (layers, hidden, heads):", best)
```

## Q97: How do you implement BERT for sentiment with robust training against label noise?
**A:** Label noise robustness: 1) Label smoothing: prevents overfitting to wrong labels. 2) Bootstrapping: use model's own predictions to correct labels. Soft bootstrapping: weighted average of label and prediction. Hard bootstrapping: use prediction if confident. 3) Loss correction: estimate noise transition matrix. 4) Sample selection: identify clean vs noisy samples, train only on clean. 5) MentorNet: learn to weight training samples (clean = high weight, noisy = low weight). 6) Mixup: interpolation reduces impact of individual noisy labels. 7) SELFIE: use small-loss samples for training (clean labels have lower loss). For BERT: bootstrapping + sample selection is most effective. 1) Train BERT for 1 epoch on full data. 2) For each sample, compute loss. 3) Keep top 80% of samples (lowest loss). 4) Retrain on selected samples. Repeat. Results: reduces impact of 20% label noise from 10% accuracy drop to 3% drop. BERT is relatively robust to label noise (pre-training knowledge corrects some wrong labels).
**Code:**
```python
import numpy as np
loss = np.random.randn(1000)
keep = np.argsort(loss)[:800]  # clean samples (lowest loss)
print("selected clean samples:", len(keep), "/", len(loss))
```

## Q98: How do you implement BERT for sentiment with constrained decoding for safety?
**A:** Safety-constrained sentiment: don't misclassify hate speech as positive. Approaches: 1) Rule-based override: if text matches hate speech patterns, override BERT's prediction to negative. 2) Constrained loss: add penalty for misclassifying known harmful content. 3) Safety head: separate BERT output for safety classification. 4) Debiasing: ensure model doesn't associate specific groups with negative sentiment. 5) Human-in-loop: if safety score < threshold, route to human. 6) Asymmetric cost: higher cost for false negatives (missed hate speech) than false positives. Implementation: 1) Standard BERT sentiment head. 2) Safety head: sigmoid output for "contains hate speech." 3) Final prediction: if safety > 0.5, override sentiment to negative. 4) Training: 2-task loss (sentiment + safety). 5) Safety dataset: HateXplain, Davidson for explicit, hard negative mining for subtle. Constrained BERT reduces hate speech misclassification as positive by 80% with only 2% accuracy drop on clean data.
**Code:**
```python
def constrained(sent, safety):
    return "negative (safety override)" if safety > 0.5 else sent
print(constrained("positive", 0.9))
```
## Q99: How do you implement BERT for sentiment with parametric efficiency (parameter-efficient fine-tuning)?
**A:** Parameter-efficient fine-tuning (PEFT) for BERT sentiment: 1) LoRA (Low-Rank Adaptation): add low-rank matrices to attention layers (Q, K, V, O). Train only LoRA weights (~0.5% of parameters). 2) Adapters: small bottleneck layers in each transformer layer. 3) Prefix tuning: learn continuous prompts (virtual tokens prepended to input). 4) Prompt tuning: learn soft prompt embeddings. 5) BitFit: only train bias terms. Results: 1) LoRA (rank=8): 0.5% of parameters trained, achieves 99% of full fine-tuning accuracy on sentiment. 2) Adapters (bottleneck=64): 3% parameters, 99.5% of full fine-tuning. 3) Prefix tuning (20 tokens): 0.1% parameters, 95% of full fine-tuning. Benefits: 1) Much lower memory for training (store only small delta weights). 2) Fast adaptation: switch between domains by swapping LoRA weights. 3) Mitigates catastrophic forgetting. For multi-domain sentiment: train one LoRA per domain (~2MB each). Deploy all LoRAs with one base BERT model.
**Code:**
```python
from peft import LoraConfig, get_peft_model
config = LoraConfig(r=8, lora_alpha=32, target_modules=["q_lin", "v_lin"])
print("trainable:", round(0.5, 1), "% of params, ~2MB per LoRA per domain")
```

## Q100: Design a comprehensive production sentiment analysis pipeline for a global e-commerce platform.
**A:** Production pipeline: 1) Ingestion: Kafka processes 100M reviews/day from 50 countries. 2) Preprocessing: language detection (langid), text normalization, HTML stripping, emoji-to-text, spam detection (duplicate removal). 3) Language-specific routing: 50 language models (DistilBERT ONNX INT8 per language). 4) Multi-tier inference: a) Fast path (VADER) for simple cases (70% of traffic, <1ms). b) Normal path (DistilBERT) for ambiguous cases (25%, ~8ms CPU). c) Deep path (XLM-R) for complex cases (sarcasm, mixed sentiment, 5%, ~20ms GPU). 5) Aspect extraction: BERT-CRF per review for aspect-sentiment tuples. 6) Aggregation: per product, per category, per brand, per language. 7) Time-series: hourly/daily sentiment trends with drift detection. 8) Alerts: p95 latency > 50ms, sentiment anomalies > 3std, concept drift detected. 9) Feedback loop: sample 1% of predictions for human review. Add reviewed data to weekly retraining. 10) Model registry: track 50 language models + versions. A/B test new models vs current. 11) Cost: DistilBERT on CPU (AWS C7g) = $0.001/1000 inferences. Total: $100/day for 100M reviews. 12) Accuracy: ~92% overall (varies by language: English 94%, low-resource 82%). Aspect extraction: 88% F1.
**Code:**
```python
def pipeline(text, lang):
    if is_simple(text):
        return vader_fast_path(text)        # 70% traffic, <1ms
    if is_ambiguous(text):
        return distilbert_norm(text)        # 25% traffic, ~8ms CPU
    return xlmr_deep(text)                  # 5% traffic, ~20ms GPU
print("100M reviews/day: $100/day, p95 < 50ms, 92% accuracy")
```