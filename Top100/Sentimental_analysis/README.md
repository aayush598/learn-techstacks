# Sentiment Analysis Interview Questions and Answers

## Q1: What is sentiment analysis?
**A:** Sentiment analysis (also called opinion mining) is a Natural Language Processing technique that identifies, extracts, and quantifies the emotional tone, attitude, or opinion expressed in text. It classifies text as positive, negative, or neutral, and can detect more fine-grained emotions or sentiment intensity.
**Code:**
```python
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()
for text in ["I love this product", "This movie was terrible", "Fine."]:
    c = sia.polarity_scores(text)["compound"]
    label = "positive" if c > 0.05 else "negative" if c < -0.05 else "neutral"
    print(text, "->", label)
```

## Q2: What are the different levels of sentiment analysis?
**A:** 1) Document-level: assigns sentiment to the entire document. 2) Sentence-level: classifies the sentiment of each sentence. 3) Aspect-based: identifies sentiment toward specific entities/aspects mentioned (e.g., "The food was great but service was slow"). 4) Entity-level: sentiment toward a specific entity.
**Code:**
```python
from textblob import TextBlob
doc = "The food was great but the service was slow."
blob = TextBlob(doc)
print("document polarity:", round(blob.sentiment.polarity, 2))
for sent in blob.sentences:
    print("sentence:", sent.string, round(sent.sentiment.polarity, 2))
aspects = {"food": "great", "service": "slow"}
print("aspect food ->", round(TextBlob("great").sentiment.polarity, 2),
      "| aspect service ->", round(TextBlob("slow").sentiment.polarity, 2))
```

## Q3: What are the main approaches to sentiment analysis?
**A:** 1) Rule-based/Lexicon-based (VADER, TextBlob, SentiWordNet). 2) Machine learning (Naive Bayes, SVM, Logistic Regression with features like n-grams and TF-IDF). 3) Deep learning (LSTM, CNN, Transformer models like BERT, RoBERTa). 4) Hybrid approaches combining multiple methods.
**Code:**
```python
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
sia = SentimentIntensityAnalyzer()
print("lexicon:", sia.polarity_scores("great movie")["compound"])
texts = ["great movie", "terrible movie"]
X = TfidfVectorizer().fit_transform(texts)
clf = LogisticRegression().fit(X, [1, 0])
print("trained ML classifier:", clf.predict(X))
```

## Q4: What is the difference between polarity and subjectivity in sentiment analysis?
**A:** Polarity measures the direction of sentiment (positive, negative, neutral) and often its intensity. Subjectivity measures whether text is factual (objective) or opinion-based (subjective). "The Earth orbits the Sun" is objective; "The sunset was beautiful" is subjective.
**Code:**
```python
from textblob import TextBlob
examples = ["The Earth orbits the Sun.", "The sunset was beautiful."]
for t in examples:
    blob = TextBlob(t)
    print(t, "| polarity:", round(blob.polarity, 2),
          "| subjectivity:", round(blob.subjectivity, 2))
```

## Q5: What are the common challenges in sentiment analysis?
**A:** 1) Sarcasm and irony. 2) Negation handling ("not bad" is positive). 3) Context-dependency ("This is sick!" can be positive or negative). 4) Polysemy (words with multiple meanings). 5) Domain-dependent sentiment. 6) Emoji and slang. 7) Code-switching (multiple languages).
**Code:**
```python
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()
print("sarcasm-ish:", sia.polarity_scores("Oh great, I lost my job")["compound"])
print("sick in slang:", sia.polarity_scores("That trick was sick!")["compound"])
```

## Q6: How do you handle sarcasm in sentiment analysis?
**A:** Sarcasm detection requires understanding context beyond literal words. Approaches include: 1) Using contextual models like BERT that capture nuanced patterns. 2) Adding punctuation/emoticon features. 3) Contrast-based features (positive words in negative context). 4) Transformer models fine-tuned on sarcasm datasets.
**Code:**
```python
from transformers import pipeline
sarcasm = pipeline("text-classification",
                   model="mishkin/bert-base-uncased-sarcasm")
print(sarcasm("Oh great, another power outage.")[0])
```

## Q7: What is aspect-based sentiment analysis (ABSA)?
**A:** ABSA identifies sentiment toward specific aspects or features of an entity. For "The camera quality is amazing but the battery life is poor," ABSA identifies: camera quality -> positive, battery life -> negative. It involves two subtasks: aspect extraction and aspect sentiment classification.
**Code:**
```python
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()
aspects = [("camera quality", "The camera quality is amazing"),
           ("battery life", "The battery life is poor")]
for aspect, text in aspects:
    c = sia.polarity_scores(text)["compound"]
    print(aspect, "->", "positive" if c > 0.05 else "negative")
```

## Q8: How does domain affect sentiment analysis?
**A:** The same word can have different sentiment across domains. "Unpredictable" is negative for a car but positive for a movie. "Sterile" is positive for a hospital but negative for a restaurant. Domain adaptation or domain-specific training is essential.
**Code:**
```python
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()
for domain in ["car", "movie"]:
    print(domain, "->",
          round(sia.polarity_scores(f"this {domain} is unpredictable")["compound"], 2))
```

## Q9: What is the difference between fine-grained and coarse-grained sentiment?
**A:** Coarse-grained uses broad categories (positive, negative, neutral). Fine-grained uses more granular classes such as 5-point scales (1-5 stars) or specific emotions. Fine-grained provides more nuance but is harder to classify.
**Code:**
```python
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()
def fine(s):
    c = sia.polarity_scores(s)["compound"]
    if c > 0.6: return "very positive"
    if c > 0.05: return "positive"
    if c < -0.6: return "very negative"
    if c < -0.05: return "negative"
    return "neutral"
for s in ["absolutely loved it", "it was okay", "utterly dreadful"]:
    print(s, "->", fine(s))
```

## Q10: What is emotion detection and how is it different from sentiment?
**A:** Emotion detection identifies specific emotions (joy, anger, sadness, fear, disgust, surprise) rather than just polarity. Sentiment is simpler (positive/negative), while emotion detection is more nuanced, often following models like Ekman's six basic emotions.
**Code:**
```python
emotions = {"joy": ["happy", "love"], "anger": ["angry", "hate"],
            "sadness": ["sad", "cry"], "fear": ["afraid", "scary"]}
text = "I am so happy and in love today!"
hits = {e: sum(w in text for w in ws) for e, ws in emotions.items()}
print(max(hits, key=hits.get))
```

## Q11: What are the common datasets for sentiment analysis?
**A:** 1) IMDb Reviews (movie reviews, binary). 2) SST (Stanford Sentiment Treebank, fine-grained). 3) Amazon Reviews (1-5 stars). 4) SemEval Twitter datasets. 5) Yelp Reviews. 6) Sentiment140 (tweets). 7) GoEmotions (emotion classification). 8) Multi-Domain Sentiment Dataset.
**Code:**
```python
from datasets import load_dataset
imdb = load_dataset("imdb", split="test[:5]")
print([(imdb[i]["label"], imdb[i]["text"][:20]) for i in range(5)])
```

## Q12: What is the Stanford Sentiment Treebank (SST)?
**A:** SST is a dataset of 11,855 movie review sentences with fine-grained sentiment labels (very negative, negative, neutral, positive, very positive). Each sentence is parsed into a binary tree with sentiment labels at every node, useful for compositional sentiment analysis.
**Code:**
```python
from datasets import load_dataset
sst2 = load_dataset("glue", "sst2", split="validation[:5]")
for row in sst2:
    print(row["label"], "|", row["sentence"])
```

## Q13: What is the difference between SST-1 and SST-2?
**A:** SST-1 has 5 classes: very negative, negative, neutral, positive, very positive. SST-2 is binary: it removes neutral and merges very negative/negative into negative, very positive/positive into positive.
**Code:**
```python
sst1 = {0: "very negative", 1: "negative", 2: "neutral", 3: "positive", 4: "very positive"}
for c, name in sst1.items():
    print(f"{name:14} -> SST-2: {('positive' if c >= 3 else 'negative')}")
```

## Q14: What is the SemEval sentiment analysis task?
**A:** SemEval (Semantic Evaluation) is a series of workshops with shared tasks including sentiment analysis. Notable tasks include SemEval-2014 Task 4 (ABSA), SemEval-2015 Task 12, and SemEval-2016 Task 5. They provide benchmark datasets and evaluation frameworks.
**Code:**
```python
semeval = [("pizza", "positive"), ("service", "negative")]
text = "The pizza was delicious, but the service was slow."
for aspect, label in semeval:
    print(f"text: {text} | {aspect} -> {label}")
```

## Q15: What are evaluation metrics for sentiment analysis?
**A:** Common metrics: 1) Accuracy. 2) Precision, Recall, F1-score. 3) Macro-F1 (average F1 across classes). 4) Weighted-F1 (weighted by class support). 5) Confusion Matrix. 6) ROC-AUC for binary. 7) MAE and RMSE for fine-grained/regression.
**Code:**
```python
from sklearn.metrics import precision_score, recall_score, f1_score
y_true = [1, 0, 1, 1, 0]
y_pred = [1, 0, 0, 1, 0]
print("precision:", round(precision_score(y_true, y_pred), 2))
print("recall   :", round(recall_score(y_true, y_pred), 2))
print("f1       :", round(f1_score(y_true, y_pred), 2))
```

## Q16: How do you handle class imbalance in sentiment analysis?
**A:** Techniques: 1) Resampling (oversample minority, undersample majority). 2) Weighted loss function. 3) Focal Loss (focus on hard examples). 4) Synthetic data generation (SMOTE, back-translation). 5) Ensemble methods. 6) Threshold tuning.
**Code:**
```python
import numpy as np
y = np.array([1, 1, 1, 0, 0, 0, 0])
weights = {int(c): len(y) / (len(set(y)) * int((y == c).sum())) for c in set(y)}
print(weights)
```

## Q17: What is the role of negation in sentiment analysis?
**A:** Negation flips sentiment polarity (e.g., "good" -> "not good" = negative). Approaches: 1) Negation scope detection. 2) Adding "NOT_" prefix to negated words. 3) Rule-based handling (like VADER). 4) Contextual models (BERT learns negation patterns). 5) Dependency parsing for negation scope.
**Code:**
```python
def add_negation(tokens):
    out, negate = [], False
    for t in tokens:
        if t in {"not", "never", "no"}:
            negate = True
            out.append("NOT_" + t)
        else:
            out.append("NOT_" + t if negate else t)
    return out
print(add_negation("the movie is not good".split()))
```

## Q18: How do you handle negations like "not bad"?
**A:** "Not bad" expresses positive sentiment despite containing negative words. Approaches: 1) Lexicon-based: treat as negation + negative -> positive. 2) Machine learning: models learn "not bad" pattern correlates with positive. 3) BERT captures this from context. 4) N-gram features like "not_bad" bigram.
**Code:**
```python
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()
for s in ["The movie is bad.", "The movie is not bad."]:
    print(s, "->", round(sia.polarity_scores(s)["compound"], 2))
```

## Q19: What are n-grams and how are they used in sentiment analysis?
**A:** N-grams are contiguous sequences of n items (words or characters). Unigrams (n=1), bigrams (n=2), trigrams (n=3). In sentiment analysis, n-grams capture word patterns: "not good" (bigram) signals negative better than individual words.
**Code:**
```python
from sklearn.feature_extraction.text import CountVectorizer
texts = ["not good", "very good", "good"]
vec = CountVectorizer(ngram_range=(1, 2)).fit(texts)
print(vec.get_feature_names_out())
```

## Q20: What is TF-IDF and how is it used in sentiment analysis?
**A:** TF-IDF (Term Frequency-Inverse Document Frequency) weights words by importance in a document relative to a corpus. It reduces the impact of common words and highlights distinctive words. Used as features for ML classifiers (SVM, Logistic Regression).
**Code:**
```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
vec = TfidfVectorizer()
X = vec.fit_transform(["this movie is great", "this movie is boring"])
clf = LogisticRegression().fit(X, [1, 0])
print(clf.predict(vec.transform(["what a great movie"])))
```

## Q21: What are word embeddings in sentiment analysis?
**A:** Word embeddings are dense vector representations of words capturing semantic meaning. Word2Vec, GloVe, and FastText generate static embeddings. Contextual embeddings (BERT, ELMo) produce different vectors based on context, improving sentiment analysis.
**Code:**
```python
from gensim.models import Word2Vec
sents = [["i", "love", "this", "movie"], ["the", "plot", "was", "boring"]]
model = Word2Vec(sents, vector_size=5, min_count=1, seed=1)
print("love ~ exciting:", model.wv.similarity("love", "movie"))
print("love ~ boring  :", model.wv.similarity("love", "boring"))
```

## Q22: What is the difference between static and contextual embeddings?
**A:** Static embeddings (Word2Vec, GloVe) produce the same vector regardless of context - "bank" in "river bank" and "money bank" have the same vector. Contextual embeddings (BERT, ELMo) produce different vectors based on surrounding words, capturing polysemy.
**Code:**
```python
from transformers import AutoTokenizer, BertModel
tok = AutoTokenizer.from_pretrained("bert-base-uncased")
model = BertModel.from_pretrained("bert-base-uncased")
for ctx in ["The river bank is pretty.", "The bank closes at 5."]:
    enc = tok(ctx, return_tensors="pt")
    out = model(**enc)
    i = enc["input_ids"][0].tolist().index(tok.convert_tokens_to_ids("bank"))
    print(ctx.split()[1], "bank ->", out.last_hidden_state[0, i, :4].tolist())
```

## Q23: How do you perform sentiment analysis on social media text?
**A:** Social media has unique challenges: slang, hashtags, emoji, irregular grammar. Approaches: 1) Use VADER (designed for social media). 2) Fine-tune BERT on social media data (BERTweet). 3) Preprocess: normalize slang, handle URLs/mentions. 4) Emoji sentiment mapping.
**Code:**
```python
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
def clean_tweet(t):
    t = re.sub(r"https?://\S+", "", t)
    t = re.sub(r"@\w+|#\w+", "", t)
    return re.sub(r"\s+", " ", t).strip()
sia = SentimentIntensityAnalyzer()
tweet = "Just had an amazing day!! #blessed @friend http://x.com"
print(clean_tweet(tweet), "->", round(sia.polarity_scores(clean_tweet(tweet))["compound"], 2))
```

## Q24: What is BERTweet?
**A:** BERTweet is a pre-trained language model for English tweets based on RoBERTa, trained on 850 million tweets. It outperforms general BERT on social media NLP tasks including sentiment analysis due to domain-specific training.
**Code:**
```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification
tok = AutoTokenizer.from_pretrained("vinai/bertweet-base", normalization=True)
model = AutoModelForSequenceClassification.from_pretrained("vinai/bertweet-base",
                                                           num_labels=3)
enc = tok("Was literally the BEST day ever 😂", truncation=True,
          max_length=128, return_tensors="pt")
print(model(**enc).logits.shape)
```

## Q25: How do you handle emoji in sentiment analysis?
**A:** Approaches: 1) Emoji sentiment lexicons (mapping emojis to scores). 2) Convert emoji to text descriptions or special tokens. 3) Keep emoji as unicode and let the model learn embeddings. 4) Use pre-trained models that saw emoji during training.
**Code:**
```python
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()
emoji_text = "wow great news 😍"
print("scores with emoji:", sia.polarity_scores(emoji_text))
print("emoji word only :", sia.polarity_scores("😍"))
```
## Q26: What is the role of hashtags in sentiment analysis?
**A:** Hashtags (#happy, #fail) often explicitly express sentiment. Approaches: 1) Extract sentiment from hashtag words. 2) Segment hashtags (#HavingABadDay -> "having a bad day"). 3) Use hashtags as features or labels.
**Code:**
```python
import re
def segment(hashtag):
    return re.sub(r"([A-Z])", r" \1", hashtag).lower().strip()
hashtags = re.findall(r"#(\w+)", "Complete disaster #HavingABadDay")
print(hashtags)
print(segment(hashtags[0]))
```

## Q27: How do you build a real-time sentiment analysis system?
**A:** Architecture: 1) Data ingestion (Kafka, Kinesis). 2) Preprocessing pipeline (Flink, Spark Streaming). 3) Sentiment model (VADER for speed, optimized BERT for accuracy). 4) Storage (Elasticsearch). 5) Visualization (Grafana, Kibana). 6) Alerting on negative sentiment spikes.
**Code:**
```python
import queue
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()
q = queue.Queue()
for tweet in ["peak sales!", "server down again", "great update"]:
    q.put(tweet)
while not q.empty():
    t = q.get()
    print(t, "->", round(sia.polarity_scores(t)["compound"], 2))
```

## Q28: What is the difference between batch and streaming sentiment analysis?
**A:** Batch analysis processes large volumes of historical data at scheduled intervals (e.g., daily review analysis). Streaming analysis processes data in real-time as it arrives (e.g., monitoring social media). Streaming requires low-latency and fault-tolerant architecture.
**Code:**
```python
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()
def batch(texts):
    return [sia.polarity_scores(t) for t in texts]
def stream(texts):
    for t in texts:
        yield sia.polarity_scores(t)
texts = ["good film", "bad film", "meh film"]
print("batch comp:", [r["compound"] for r in batch(texts)])
print("stream comp:", [r["compound"] for r in stream(texts)])
```

## Q29: How do you handle multilingual sentiment analysis?
**A:** Approaches: 1) Multilingual models (mBERT, XLM-RoBERTa). 2) Translate to English then analyze (introduces errors). 3) Language-specific models. 4) Cross-lingual zero-shot transfer. 5) Character-level models that work across languages.
**Code:**
```python
from transformers import pipeline
clf = pipeline("text-classification",
               model="nlptown/bert-base-multilingual-uncased-sentiment")
for text in ["I love this", "真好", "Je déteste ça"]:
    print(text, "->", clf(text)[0]["label"], clf(text)[0]["score"])
```

## Q30: What is cross-lingual sentiment analysis?
**A:** Cross-lingual sentiment analysis trains on one language (source) and applies to another (target) without target-language training data. Achieved through: 1) Multilingual BERT (shared embedding space). 2) Adapter-based approaches. 3) Machine translation + sentiment. 4) Zero-shot transfer.
**Code:**
```python
from transformers import pipeline
clf = pipeline("zero-shot-classification", model="joeddav/xlm-roberta-large-xnli")
text = "La comida aquí es increíble."
print(clf(text, candidate_labels=["positive", "negative", "neutral"]))
```

## Q31: What is zero-shot sentiment analysis?
**A:** Zero-shot sentiment analysis classifies sentiment for classes unseen during training. Using models like BART or T5, you can formulate it as a natural language inference task. Hugging Face's pipeline supports zero-shot classification natively.
**Code:**
```python
from transformers import pipeline
clf = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
text = "This plugin made everything much slower."
print(clf(text, candidate_labels=["positive", "negative", "neutral"]))
```

## Q32: What is few-shot sentiment analysis?
**A:** Few-shot learning trains with very few labeled examples (e.g., 5-50 per class). Approaches: 1) Fine-tune pre-trained model with strong regularization. 2) Pattern-exploiting training (PET). 3) In-context learning with LLMs (GPT-3, Llama). 4) SetFit (efficient few-shot fine-tuning).
**Code:**
```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
vec = TfidfVectorizer()
X = vec.fit_transform(["love it", "hate it", "amazing", "awful"])
clf = LogisticRegression().fit(X, ["pos", "neg", "pos", "neg"])
print(clf.predict(vec.transform(["I love this product"])))
```

## Q33: What is SetFit?
**A:** SetFit (Sentence Transformer Fine-tuning) is an efficient few-shot learning method for text classification. It uses sentence transformers to generate embeddings and trains a classifier head with contrastive learning, achieving high accuracy with as few as 8-64 examples per class.
**Code:**
```python
from setfit import SetFitModel, SetFitTrainer
from datasets import Dataset
model = SetFitModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
trainer = SetFitTrainer(model=model,
                        train_dataset=Dataset.from_dict(
                            {"text": ["love it", "hate it", "amazing", "awful"],
                             "label": [1, 0, 1, 0]}))
trainer.train()
print(model(["wonderful", "boring"]))
```

## Q34: What is in-context learning for sentiment analysis?
**A:** In-context learning uses large language models by providing examples in the prompt. For example: "Classify as positive, negative, or neutral: 'I love this product' -> Positive". The model infers the task from examples without weight updates.
**Code:**
```python
import openai
client = openai.OpenAI()
out = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "Label sentiment: positive, neutral, or negative."},
        {"role": "user", "content": "I love the new update!"}])
print(out.choices[0].message.content)
```

## Q35: What is the difference between generative and discriminative approaches?
**A:** Generative approaches model joint probability of text and sentiment (can generate text). Discriminative approaches model conditional probability of sentiment given text (classify only). Most sentiment models (BERT, SVM) are discriminative. GPT models are generative.
**Code:**
```python
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import pipeline
sia = SentimentIntensityAnalyzer()
print("discriminative:", round(sia.polarity_scores("okay film")["compound"], 2))
gen = pipeline("text-generation", model="gpt2")
print("generative:", gen("The movie was absolutely", max_new_tokens=5)[0]["generated_text"])
```

## Q36: What is supervised sentiment analysis?
**A:** Supervised sentiment analysis trains a model on a labeled dataset where each text has an associated sentiment label. The model learns patterns correlating with labels. Requires sufficient labeled data but achieves the highest accuracy.
**Code:**
```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
texts = ["love this phone", "hate this phone", "quite good", "really bad", "decent", "awful"]
labels = [1, 0, 1, 0, 1, 0]
vec = TfidfVectorizer()
X = vec.fit_transform(texts)
clf = MultinomialNB().fit(X, labels)
print(clf.predict(vec.transform(["this phone is amazing"])))
```

## Q37: What is unsupervised sentiment analysis?
**A:** Unsupervised sentiment analysis uses no labeled data. Approaches: 1) Lexicon-based (VADER, SentiWordNet). 2) Embedding clustering (infer sentiment from cluster characteristics). 3) Rule-based patterns. Less accurate but requires no training data.
**Code:**
```python
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()
for t in ["love it", "hate it", "meh"]:
    print(t, "->", round(sia.polarity_scores(t)["compound"], 2))
```

## Q38: What is semi-supervised sentiment analysis?
**A:** Semi-supervised learning uses a small labeled dataset and a large unlabeled dataset. The model is trained on labeled data, then pseudo-labels unlabeled data iteratively. Self-training and co-training are common approaches.
**Code:**
```python
from sklearn.semi_supervised import SelfTrainingClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
texts = ["great movie", "bad movie", "amazing film", "awful film", "superb", "horrible"]
y = [1, 0, 1, 0, -1, -1]
vec = TfidfVectorizer()
clf = SelfTrainingClassifier(MultinomialNB()).fit(vec.fit_transform(texts), y)
print(clf.predict(vec.transform(["wonderful", "disgusting"])))
```

## Q39: What is weak supervision in sentiment analysis?
**A:** Weak supervision uses heuristic rules or distant supervision to generate noisy labels automatically. For example, using star ratings as sentiment labels. Snorkel combines multiple noisy label sources into probabilistic training labels.
**Code:**
```python
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()
def heuristic_label(text):
    c = sia.polarity_scores(text)["compound"]
    if text.startswith("WOW"): return 1
    if c > 0.5: return 1
    if c < -0.3: return 0
    return None
for t in ["WOW this update!!", "this update is bad", "the update shipped"]:
    print(t, "->", heuristic_label(t))
```

## Q40: How do you perform distant supervision for sentiment?
**A:** Distant supervision uses existing data as noisy labels: 1) Emoticons in tweets (:)=positive, :(=negative). 2) Star ratings as labels. 3) Hashtags (#happy, #angry). Labels are noisy but allow training without manual annotation.
**Code:**
```python
def distant_label(tweet):
    return 1 if ":)" in tweet else 0 if ":(" in tweet else None
tweets = ["just won tickets :)", "service was a joke :(", "neutral post"]
X, y = tweets, [distant_label(t) for t in tweets]
print(list(zip(X, y)))
```

## Q41: What is the role of preprocessing in sentiment analysis?
**A:** Steps include: lowercasing, removing HTML/URLs, expanding contractions, punctuation handling, stemming/lemmatization, stop word removal, spell correction. The right preprocessing depends on the approach. Over-processing can harm VADER but help traditional ML.
**Code:**
```python
import re, html
def clean(text):
    text = html.unescape(text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"https?://\S+", "", text)
    text = re.sub(r"@\w+", "", text)
    return re.sub(r"\s+", " ", text.lower()).strip()
print(clean("Check <b>THIS</b> out!!! http://x.com 😀"))
```

## Q42: What is the impact of stop word removal?
**A:** Stop word removal can harm sentiment analysis because: 1) Negation words ("not", "no") are stop words but crucial. 2) Intensifiers ("very", "extremely") are short but significant. 3) Sentiment words can be short ("good", "bad"). Keep stop words or remove selectively.
**Code:**
```python
from nltk.corpus import stopwords
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()
text = "this movie is not good"
cleaned = " ".join(w for w in text.split() if w not in stopwords.words("english"))
print("with stopwords:", round(sia.polarity_scores(text)["compound"], 2))
print("after removal :", round(sia.polarity_scores(cleaned)["compound"], 2))
```

## Q43: What is stemming and lemmatization in sentiment analysis?
**A:** Stemming removes suffixes ("running" -> "run"). Lemmatization returns dictionary form ("better" -> "good"). Lemmatization is more accurate but slower. Both reduce sparsity in traditional ML. Not needed for BERT (uses subword tokenization).
**Code:**
```python
from nltk.stem import PorterStemmer, WordNetLemmatizer
stem, lemm = PorterStemmer(), WordNetLemmatizer()
for w in ["running", "better", "amazing"]:
    print(w, "->", stem.stem(w), "/", lemm.lemmatize(w))
```

## Q44: What are sentiment lexicons?
**A:** Sentiment lexicons map words to sentiment scores/classes. Examples: 1) VADER lexicon (social media). 2) AFINN (-5 to +5). 3) SentiWordNet (WordNet synsets). 4) MPQA Subjectivity Lexicon. 5) Bing Liu Opinion Lexicon. 6) Loughran-McDonald (financial).
**Code:**
```python
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
lex = SentimentIntensityAnalyzer().lexicon
print({w: lex[w] for w in ["good", "terrible", "love", "hate"]})
```

## Q45: What is SentiWordNet?
**A:** SentiWordNet assigns each WordNet synset three scores: positivity, negativity, and objectivity (summing to 1). Covers over 117,000 synsets. Used for lexicon-based sentiment analysis, especially when no domain-specific lexicon is available.
**Code:**
```python
from nltk.corpus import sentiwordnet as swn
syn = swn.senti_synset("good.a.01")
print("pos:", round(syn.pos_score(), 3), "neg:", round(syn.neg_score(), 3),
      "obj:", round(syn.obj_score(), 3))
```

## Q46: What is the difference between SentiWordNet and VADER?
**A:** SentiWordNet covers more words (117K synsets) but is not domain-optimized. VADER has fewer words (~7,500) but is specifically tuned for social media with heuristics for intensifiers, negation, and emoticons. VADER outperforms on informal text.
**Code:**
```python
from nltk.corpus import sentiwordnet as swn
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
print("SentiWordNet good.a.01 pos:", round(swn.senti_synset("good.a.01").pos_score(), 3))
print("VADER 'good' compound:", SentimentIntensityAnalyzer().polarity_scores("good")["compound"])
```

## Q47: How do you handle code-mixed text (Hinglish, Spanglish)?
**A:** Approaches: 1) Normalize each language variant. 2) Character-level models (handle unknown words). 3) Multilingual BERT. 4) Train on code-mixed datasets. 5) Transliteration. 6) Specialized models like HingBERT.
**Code:**
```python
from transformers import pipeline
clf = pipeline("zero-shot-classification", model="joeddav/xlm-roberta-large-xnli")
for text in ["ye movie bahut ganda hai", "phone ka battery achha hai"]:
    print(text, "->", clf(text, candidate_labels=["positive", "negative", "neutral"])["labels"][0])
```

## Q48: What is HingBERT?
**A:** HingBERT is a BERT model trained on Hinglish (Hindi-English code-mixed text). It handles unique patterns of code-mixed text and outperforms multilingual BERT on Hinglish NLP tasks including sentiment analysis.
**Code:**
```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification
tok = AutoTokenizer.from_pretrained("ai4bharat/indic-bert")
model = AutoModelForSequenceClassification.from_pretrained("ai4bharat/indic-bert",
                                                           num_labels=3)
enc = tok("ye movie bahut badhiya hai", return_tensors="pt")
print(model(**enc).logits.shape)
```

## Q49: How do you handle sentiment analysis for long documents?
**A:** Challenges: model input limits, varying sentiment across sections. Approaches: 1) Truncation (keep most relevant part). 2) Sentence-level with aggregation (average, majority vote). 3) Hierarchical models (encode sentences, then document). 4) Longformer/BigBird (long-context).
**Code:**
```python
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()
sents = ["First part was great.", "Second half dragged.", "Ending was perfect."]
compounds = [sia.polarity_scores(s)["compound"] for s in sents]
avg = sum(compounds) / len(compounds)
print([round(c, 2) for c in compounds], "document:", "positive" if avg > 0.05 else "negative")
```

## Q50: How do you handle sentiment analysis for customer reviews?
**A:** For product/service reviews: 1) Aspect-based sentiment analysis per feature. 2) Handle comparative statements. 3) Handle hyperbole and review-specific language. 4) Detect fake/spam reviews. 5) Temporal sentiment trends. 6) Combine with ratings.
**Code:**
```python
from collections import Counter
aspect_kw = {"camera": ["camera"], "battery": ["battery"]}
reviews = [("Great camera", "camera"), ("Battery drains fast", "battery"),
           ("Camera is superb", "camera")]
counts = Counter()
for text, aspect in reviews:
    positive = any(w in text.lower() for w in ["great", "superb", "love"])
    counts[(aspect, "pos" if positive else "neg")] += 1
print(counts)
```
## Q51: What is opinion summarization?
**A:** Opinion summarization generates a concise summary of sentiments from multiple reviews. It identifies key aspects and associated sentiment distribution. Example: "80% of reviews praise battery life, 60% complain about camera quality."
**Code:**
```python
from collections import defaultdict
review_sents = [("camera", 1), ("camera", 1), ("camera", 0),
                ("battery", 1), ("battery", 0)]
agg = defaultdict(list)
for aspect, s in review_sents:
    agg[aspect].append(s)
for aspect, votes in agg.items():
    print(aspect, "pos:", round(votes.count(1) / len(votes), 2),
          "neg:", round(votes.count(0) / len(votes), 2))
```

## Q52: How do you detect fake reviews?
**A:** Approaches: 1) Anomaly detection in sentiment patterns. 2) Review metadata analysis (timing, user behavior). 3) Text patterns (repetition, generic language). 4) Sentiment vs rating inconsistency. 5) Stylometric analysis. 6) Graph-based methods.
**Code:**
```python
import re
def spam_score(review):
    repeated = len(re.findall(r"\b(\w+)\b(?:\s+\1){2,}", review))
    generic = sum(review.lower().count(w) for w in ["must buy", "amazing", "best ever"])
    return repeated + generic
print(spam_score("best ever amazing must buy must buy must buy amazing"))
```

## Q53: What is the relationship between sentiment analysis and opinion mining?
**A:** Often used interchangeably. Opinion mining is broader: it includes sentiment analysis plus opinion holder identification, target extraction, and opinion summarization.
**Code:**
```python
import re
text = "Critics said the movie was brilliant."
print(re.findall(r"(\w+) (?:said|praised|revealed)", text))
```

## Q54: What is opinion target extraction?
**A:** Identifying the specific entity or aspect being evaluated. In "The battery life is amazing," the target is "battery life." Approached as sequence labeling (NER-like) task.
**Code:**
```python
import spacy
nlp = spacy.load("en_core_web_sm")
doc = nlp("The battery life is amazing.")
print([c.text for c in doc.noun_chunks])
```

## Q55: What is the role of dependency parsing in sentiment analysis?
**A:** Dependency parsing reveals grammatical relationships, helping identify: 1) Word modifications ("very" modifies "good"). 2) Negation scope. 3) Relations between opinion words and targets. 4) Long-distance dependencies.
**Code:**
```python
import spacy
nlp = spacy.load("en_core_web_sm")
doc = nlp("I did not think this movie was good.")
for tok in doc:
    if tok.dep_ == "neg":
        print(tok.text, "negates:", tok.head.text,
              "| modified words:", [c.text for c in tok.head.children])
```

## Q56: What is a dependency tree-based sentiment model?
**A:** Models using dependency trees to capture sentiment flow. Tree-LSTM applies recurrent networks over dependency trees, propagating sentiment from words to parents, capturing composition (e.g., "not" flips child's sentiment).
**Code:**
```python
import spacy
nlp = spacy.load("en_core_web_sm")
doc = nlp("The movie was not good.")
neg = [t for t in doc if t.dep_ == "neg"][0]
print("syntax path:", neg.head.text, "<--neg--", neg.text,
      "=> sentiment of 'good' flips to negative")
```

## Q57: What are attention mechanisms in sentiment analysis?
**A:** Attention allows the model to focus on relevant input parts when predicting. It learns to give higher weight to sentiment-bearing words. Self-attention (in BERT) captures relationships between all token pairs.
**Code:**
```python
from transformers import AutoTokenizer, BertModel
tok = AutoTokenizer.from_pretrained("bert-base-uncased")
model = BertModel.from_pretrained("bert-base-uncased", output_attentions=True)
enc = tok("the food was amazing", return_tensors="pt")
att = model(**enc).attentions[-1][0].mean(0).mean(0)
for t, a in zip(tok.convert_ids_to_tokens(enc.input_ids[0]), att):
    print(t, round(float(a), 3))
```

## Q58: What is aspect-level attention?
**A:** Aspect-level attention focuses on text segments relevant to a specific aspect. For "The food was great but service was slow," different attention is assigned to "great" for food sentiment and "slow" for service sentiment.
**Code:**
```python
import numpy as np
aspect_attn = {"food": np.array([0.9, 0.2, 0.5]),
               "service": np.array([0.1, 0.8, 0.6])}
ctx = np.array([1.0, 0.2, 0.5])
for a, w in aspect_attn.items():
    print(a, "score:", round(float(np.dot(w, ctx)), 2))
```

## Q59: What is the difference between global and local attention?
**A:** Global attention considers all input tokens. Local attention focuses on positions near a target. Local attention is more efficient for aspect-based sentiment where local context is most relevant.
**Code:**
```python
import numpy as np
tokens = np.array([0.1, 0.5, 0.9])
global_attn = np.ones(3) / 3
local_attn = np.array([0.1, 0.3, 0.6])
print("global:", round(float(tokens @ global_attn), 2))
print("local :", round(float(tokens @ local_attn), 2))
```

## Q60: How do traditional ML and deep learning compare for sentiment?
**A:** Traditional ML (SVM, NB, with TF-IDF): fast, interpretable, works with small data, limited accuracy. Deep learning (LSTM, BERT): higher accuracy, handles context and nuance, requires more data and compute. BERT now dominates benchmarks.
**Code:**
```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
texts = ["great film", "bad film", "funny movie", "dull movie"]
y = [1, 0, 1, 0]
X = TfidfVectorizer().fit_transform(texts)
print("linear:", LogisticRegression().fit(X, y).predict(X).tolist())
print("MLP   :", MLPClassifier(hidden_layer_sizes=(8,), max_iter=500).fit(X, y).predict(X).tolist())
```

## Q61: What are advantages of transformer models for sentiment?
**A:** 1) Bidirectional context. 2) Pre-trained on massive text. 3) Transfer learning (fine-tune with moderate data). 4) Self-attention captures long-range dependencies. 5) State-of-the-art on most benchmarks.
**Code:**
```python
from transformers import pipeline
clf = pipeline("text-classification",
               model="distilbert-base-uncased-finetuned-sst-2-english")
print(clf("The movie is absolutely wonderful.")[0])
```

## Q62: What is the performance of different models on benchmarks?
**A:** On SST-2: Logistic Regression ~82%, LSTM ~87%, ELMo ~90%, BERT-base ~93%, BERT-large ~94.5%, RoBERTa-large ~96.4%. On SST-5: BERT-base ~54%, RoBERTa-large ~57%.
**Code:**
```python
bench = {"LogReg": 82.0, "LSTM": 87.0, "ELMo": 90.0, "BERT-base": 93.0,
         "BERT-large": 94.5, "RoBERTa-large": 96.4}
for m, a in bench.items():
    print(f"{m:14} {a}% SST-2")
```

## Q63: How do you choose between simple and complex models?
**A:** Consider: 1) Data size: small -> simpler or few-shot. 2) Latency: real-time -> VADER, distilled BERT. 3) Accuracy: high stakes -> BERT-level. 4) Resources: limited -> VADER, abundant -> BERT.
**Code:**
```python
def choose(data_size, latency_ms, gpu):
    if data_size < 1000:
        return "VADER or zero-shot"
    if latency_ms < 10:
        return "DistilBERT"
    if gpu:
        return "BERT-large"
    return "TF-IDF + LogisticRegression"
print(choose(200, 50, True))
print(choose(100000, 5, False))
```

## Q64: What is the cold start problem?
**A:** The cold start problem occurs when launching sentiment analysis for a new domain without labeled data. Solutions: 1) Pre-trained models/lexicons (zero-shot). 2) Transfer learning. 3) Active learning. 4) Weak supervision with heuristics.
**Code:**
```python
from transformers import pipeline
zs = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
new_domain = "the lane-keep assist finally works as advertised"
print(zs(new_domain, candidate_labels=["positive", "negative", "neutral"]))
```

## Q65: What is active learning for sentiment analysis?
**A:** Active learning reduces labeling effort by selecting the most informative examples for annotation. Strategies: 1) Uncertainty sampling. 2) Diversity sampling. 3) Query-by-committee. Significantly reduces labeled data needed.
**Code:**
```python
import numpy as np
probs = np.array([[0.40, 0.30, 0.30], [0.90, 0.05, 0.05], [0.41, 0.50, 0.09]])
uncertainty = 1 - probs.max(axis=1)
for i in np.argsort(uncertainty)[::-1]:
    print("sample", i, "uncertainty", round(uncertainty[i], 2))
```

## Q66: How do you handle temporal drift?
**A:** Language evolves over time. Mitigation: 1) Regular retraining on recent data. 2) Online learning. 3) Monitor performance drift. 4) Maintain up-to-date lexicons. 5) Use recently pre-trained models.
**Code:**
```python
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.linear_model import SGDClassifier
vec = HashingVectorizer(n_features=1000)
clf = SGDClassifier(loss="log_loss")
for month_texts in [["great deal", "epic win"], ["sick deal", "fire sale"]]:
    clf.partial_fit(vec.transform(month_texts), [1, 1], classes=[0, 1])
print("online model sees 'current deal is sick' ->",
      clf.predict(vec.transform(["current deal is sick"]))[0])
```

## Q67: What is data drift in sentiment analysis?
**A:** Data drift occurs when input data distribution changes, degrading performance. Examples: new slang emerges, new products discussed. Monitor by comparing current data statistics with training data; retrain when drift is detected.
**Code:**
```python
import numpy as np
train_stats = np.array([0.8, 0.1, 0.1])   # pos/neg/neu proportion at train time
new_stats = np.array([0.3, 0.4, 0.3])     # current traffic
kl = (train_stats * np.log(train_stats / new_stats)).sum()
print("KL drift signal:", round(kl, 4))
```

## Q68: What is concept drift in sentiment analysis?
**A:** Concept drift occurs when the relationship between features and sentiment changes. "Sick" meant negative but became positive slang. Requires model retraining or adaptation.
**Code:**
```python
def sentiment_with_lexicon(text, lexicon):
    return sum(lexicon.get(w, 0.0) for w in text.split())
old = {"sick": -1.0}
new = {"sick": +1.0}
print("2010 model:", sentiment_with_lexicon("that beat is sick", old))
print("2026 model:", sentiment_with_lexicon("that beat is sick", new))
```

## Q69: How do you deploy a sentiment analysis model?
**A:** Options: 1) REST API (FastAPI, Flask). 2) Batch pipeline (Spark). 3) Edge deployment (TensorFlow Lite). 4) Serverless (Lambda). 5) ML serving (SageMaker, TorchServe). 6) Optimized models (quantization, ONNX) for production.
**Code:**
```python
from fastapi import FastAPI
from pydantic import BaseModel
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
app = FastAPI()
sia = SentimentIntensityAnalyzer()
class Text(BaseModel):
    text: str
@app.post("/sentiment")
def predict(payload: Text):
    c = sia.polarity_scores(payload.text)["compound"]
    return {"compound": c, "class": "pos" if c > 0.05 else "neg" if c < -0.05 else "neu"}
```

## Q70: How do you handle sentiment analysis at scale?
**A:** Strategies: 1) Distributed processing (Spark). 2) Load balancing. 3) Caching results. 4) Asynchronous processing (queues). 5) Model optimization (distillation, quantization). 6) Tiered models (fast filter + accurate model).
**Code:**
```python
from multiprocessing import Pool
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
def score(t):
    return SentimentIntensityAnalyzer().polarity_scores(t)["compound"]
texts = [f"review {i} is great" for i in range(8)]
with Pool(4) as pool:
    results = pool.map(score, texts)
print([round(r, 2) for r in results])
```

## Q71: What is the role of confidence scores?
**A:** Confidence scores indicate prediction certainty. Uses: 1) Filter low-confidence predictions for human review. 2) Calibrate model. 3) Build reject options. 4) Weighted aggregation. 5) Uncertainty estimation.
**Code:**
```python
from transformers import pipeline
clf = pipeline("text-classification",
               model="distilbert-base-uncased-finetuned-sst-2-english")
for t in ["loved it", "hated it", "maybe fine"]:
    label, conf = clf(t)[0]["label"], clf(t)[0]["score"]
    verdict = "auto" if conf >= 0.9 else "send to human review"
    print(t, label, round(conf, 3), "->", verdict)
```

## Q72: How do you calibrate probabilities?
**A:** Methods: 1) Platt scaling (logistic regression on outputs). 2) Isotonic regression. 3) Temperature scaling (softmax parameter). 4) Histogram binning. BERT models benefit from calibration as they tend to be overconfident.
**Code:**
```python
from sklearn.calibration import CalibratedClassifierCV
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
texts = ["love", "hate", "amazing", "bad", "great", "awful"]
y = [1, 0, 1, 0, 1, 0]
vec = TfidfVectorizer()
X = vec.fit_transform(texts)
cal = CalibratedClassifierCV(MultinomialNB(), method="sigmoid").fit(X, y)
print(cal.predict_proba(vec.transform(["cannot believe how good this is"])))
```

## Q73: What is model ensembling for sentiment?
**A:** Ensembling combines multiple models. Approaches: 1) Voting (majority). 2) Weighted averaging. 3) Stacking (meta-model). 4) Bagging. 5) Boosting. Ensembles reduce variance and improve robustness.
**Code:**
```python
from sklearn.ensemble import VotingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
texts = ["great movie", "bad movie", "nice film", "awful film", "lovely", "dreadful"]
y = [1, 0, 1, 0, 1, 0]
X = TfidfVectorizer().fit_transform(texts)
v = VotingClassifier([("lr", LogisticRegression()), ("nb", MultinomialNB()),
                      ("rf", RandomForestClassifier(n_estimators=50))])
v.fit(X, y)
print(v.predict(X[:1]))
```

## Q74: How do you perform error analysis?
**A:** Steps: 1) Build confusion matrix. 2) Analyze misclassified examples for patterns (sarcasm, negation). 3) Slice analysis by length, domain, intensity. 4) Identify systematic errors. 5) Use explainability tools.
**Code:**
```python
import numpy as np
from sklearn.metrics import confusion_matrix
y_true = np.array([1, 0, 1, 1, 0, 1])
y_pred = np.array([1, 0, 0, 1, 1, 0])
print(confusion_matrix(y_true, y_pred))
for i, (t, p) in enumerate(zip(y_true, y_pred)):
    if t != p:
        print("misclassified sample", i, "label", t, "pred", p)
```

## Q75: What is slice-based evaluation?
**A:** Measures performance across data subgroups (slices) to identify bias. Slices: text length, product category, demographic group, language variant. A model may perform well overall but poorly on a critical slice.
**Code:**
```python
texts = [("short and bad", "short"),
         ("a very long review that is honestly just terrible overall", "long")]
for text, bucket in texts:
    print(bucket, "->", "negative")
```

## Q76: What is gender bias in sentiment models?
**A:** Models can learn gender biases from training data (e.g., associating "nurse" with female sentiment differently). Mitigation: 1) Balanced data. 2) Counterfactual augmentation. 3) Debiasing embeddings. 4) Adversarial debiasing. 5) Fairness evaluation.
**Code:**
```python
def sentiment(text):
    return "positive" if "great" in text or "professional" in text else "negative"
for text in ["The nurse was very professional.", "The engineer was very professional."]:
    print(text, "->", sentiment(text))
```

## Q77: How do you audit for bias?
**A:** Steps: 1) Evaluation datasets with protected attributes. 2) Measure performance disparities. 3) Counterfactual testing (swap gender/race terms). 4) Analyze false positive/negative rates across groups. 5) Report and mitigate disparities.
**Code:**
```python
def audit(model, texts):
    return {t: model(t) for t in texts}
model = lambda t: "positive" if "great" in t else "negative"
print(audit(model, ["a great nurse", "a great engineer",
                    "an awful nurse", "an awful engineer"]))
```

## Q78: What is the GDPR impact on sentiment analysis?
**A:** GDPR affects processing of personal data. Requirements: 1) Legal basis for processing. 2) Data minimization. 3) Right to explanation (automated decisions). 4) Data subject rights. 5) Anonymization/pseudonymization.
**Code:**
```python
import re
def pseudonymize(text):
    return re.sub(r"[A-Z][a-z]+ [A-Z][a-z]+", "CONTACT_HOLDER", text)
print(pseudonymize("Jane Doe wrote: I am unhappy with my order."))
```

## Q79: How do you handle privacy in sentiment analysis?
**A:** Measures: 1) Anonymize personal information. 2) Differential privacy. 3) On-device processing. 4) Data retention policies. 5) Consent management. 6) Federated learning.
**Code:**
```python
import hashlib
def deidentify(user_id):
    return hashlib.sha256(user_id.encode()).hexdigest()[:10]
reviews = [("alice@x.com", "I love this"), ("bob@x.com", "I hate this")]
print([(deidentify(u), s) for u, s in reviews], "raw emails removed")
```

## Q80: What is federated learning for sentiment?
**A:** Federated learning trains models across decentralized devices without raw data leaving the device. Model updates (gradients) are aggregated centrally. Useful for privacy-sensitive applications (personal messages).
**Code:**
```python
import numpy as np
clients = [np.array([0.01, 0.02, 0.01]), np.array([0.03, 0.01, 0.02])]
global_model = np.mean(clients, axis=0)
print("FedAvg aggregate:", global_model)
```

## Q81: How do you handle financial sentiment analysis?
**A:** Challenges: domain-specific terms, regulatory language, numerical data. Approaches: 1) FinBERT (pre-trained on financial text). 2) Loughran-McDonald dictionary. 3) Incorporate numerical data. 4) Handle earnings calls, SEC filings.
**Code:**
```python
from transformers import pipeline
fin = pipeline("text-classification", model="ProsusAI/finbert")
for t in ["The company beat earnings estimates.", "Profits sank 20%."]:
    print(t, "->", fin(t)[0]["label"])
```

## Q82: What is FinBERT?
**A:** FinBERT is pre-trained on financial text (SEC filings, earnings reports) and fine-tuned for financial sentiment. It outperforms general BERT on financial tasks, handling terms like "bearish," "volatility," "EPS."
**Code:**
```python
from transformers import pipeline
print(pipeline("text-classification", model="ProsusAI/finbert")(
    "The sector turned bullish on EPS growth.")[0])
```

## Q83: How do you handle healthcare sentiment?
**A:** Healthcare involves medical terminology and patient narratives. Approaches: 1) BioBERT/PubMedBERT. 2) Handle negation carefully (critical in medical). 3) Address HIPAA/privacy. 4) Analyze patient feedback, clinical notes.
**Code:**
```python
from transformers import pipeline
clf = pipeline("zero-shot-classification", model="UWB-AIR/BioBERT-MNLI")
print(clf("Patient reports feeling much better today.",
          candidate_labels=["positive", "negative", "neutral"]))
```

## Q84: How do you handle legal document sentiment?
**A:** Legal text has complex language and nuanced tone. Approaches: 1) Legal-BERT. 2) Hierarchical approaches for long documents. 3) Aspect-based analysis. 4) Fine-grained sentiment for subtle tones.
**Code:**
```python
from transformers import pipeline
clf = pipeline("zero-shot-classification", model="lexlms/legal-roberta-base")
print(clf("The ruling strongly favors the plaintiff.",
          candidate_labels=["positive", "negative", "neutral"]))
```

## Q85: What is aspect-category sentiment analysis?
**A:** Predicts sentiment toward predefined aspect categories (food, service, ambiance, price) rather than extracting specific terms. The model predicts sentiment for each category present.
**Code:**
```python
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()
text = "The food was delicious. The service was rude."
for cat, part in [("food", text[:20]), ("service", text[21:])]:
    print(cat, "->", round(sia.polarity_scores(part)["compound"], 2))
```

## Q86: What is targeted sentiment analysis?
**A:** Identifies sentiment toward a specific target entity. "Apple's new iPhone is amazing but customer service is terrible" -> iPhone: positive, customer service: negative.
**Code:**
```python
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()
pairs = {"iPhone": "Apple's new iPhone is amazing",
         "customer service": "customer service is terrible"}
for t, s in pairs.items():
    print(t, "->", round(sia.polarity_scores(s)["compound"], 2))
```

## Q87: How do you handle comparative sentences?
**A:** Comparative sentences compare entities ("X is better than Y"). Approaches: 1) Identify comparative structure via dependency parsing. 2) Extract comparative preference. 3) Separate into two sentiment statements.
**Code:**
```python
import re
m = re.search(r"(\w+) is better than (\w+)", "Product A is better than Product B.")
print("preference:", m.group(1), "over", m.group(2))
```

## Q88: What is conditional sentiment analysis?
**A:** Handles sentiment dependent on conditions. "If the battery lasted longer, it would be perfect" expresses conditional negative sentiment about current battery. Requires understanding hypotheticals.
**Code:**
```python
import re
sent = "If the battery lasted longer, it would be perfect."
m = re.match(r"If (.+?), it would be (.+)", sent)
print("condition:", m.group(1), "| current-state sentiment: negative")
```

## Q89: How do you handle low-resource languages?
**A:** Approaches: 1) Cross-lingual transfer (mBERT, XLM-R). 2) Zero-shot. 3) Data augmentation (back-translation). 4) Lexicon translation. 5) Active learning. 6) Character-level models.
**Code:**
```python
from transformers import pipeline
clf = pipeline("zero-shot-classification", model="joeddav/xlm-roberta-large-xnli")
print(clf("کھانا بہت مزیدار ہے",
          candidate_labels=["positive", "negative", "neutral"]))
```

## Q90: What is the role of data annotation?
**A:** High-quality annotation is critical for supervised models. Best practices: 1) Clear guidelines with examples. 2) Multiple annotators. 3) Calculate inter-annotator agreement. 4) Resolve disagreements. 5) Ongoing quality checks.
**Code:**
```python
from sklearn.metrics import cohen_kappa_score
a1 = [1, 0, 1, -1, 0, 1, -1, -1, 0, 1]
a2 = [1, 1, 1, -1, 0, 0, -1, -1, 1, 1]
print("Cohen's kappa:", round(cohen_kappa_score(a1, a2), 3))
```

## Q91: What is inter-annotator agreement?
**A:** Measures how consistently annotators label data. Cohen's kappa (2 annotators) or Fleiss' kappa (3+) corrects for chance agreement. >0.8 is strong, 0.6-0.8 moderate. Low agreement indicates ambiguous task.
**Code:**
```python
from sklearn.metrics import cohen_kappa_score
a1 = [1, 0, 1, 0, 1]
a2 = [1, 0, 0, 0, 1]
a3 = [1, 1, 1, 0, 1]
pair_k = [cohen_kappa_score(x, y) for x, y in [(a1, a2), (a1, a3), (a2, a3)]]
print("mean kappa:", round(sum(pair_k) / len(pair_k), 3))
```

## Q92: How do you handle ambiguous or neutral texts?
**A:** Neutral texts are challenging. Approaches: 1) Include neutral as a class. 2) Confidence thresholding (classify only high-confidence). 3) Multi-label (both positive and negative). 4) Regression output.
**Code:**
```python
from transformers import pipeline
clf = pipeline("text-classification",
               model="distilbert-base-uncased-finetuned-sst-2-english")
for t in ["It is okay I guess", "It arrived on Tuesday"]:
    r = clf(t)[0]
    print(t, "->", r["label"] if r["score"] > 0.9 else "neutral / low confidence",
          round(r["score"], 2))
```

## Q93: How do you handle sentiment intensity?
**A:** Intensity measures how strong the sentiment is. Approaches: 1) Fine-grained classification (1-5 stars). 2) Regression (continuous score). 3) Ordinal regression (preserves order). 4) VADER compound score (normalized -1 to +1).
**Code:**
```python
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()
for t in ["Excellent!", "Good.", "Meh.", "Terrible!"]:
    c = sia.polarity_scores(t)["compound"]
    band = "very positive" if c > 0.6 else "positive" if c > 0.05 else \
           "very negative" if c < -0.6 else "negative" if c < -0.05 else "neutral"
    print(t, round(c, 2), "->", band)
```

## Q94: What is multimodal sentiment analysis?
**A:** Combines text with other modalities (audio, video, images) for richer sentiment understanding. For example, analyzing facial expressions, tone of voice, and text together. Models like MERT and Video-Audio-Text transformers.
**Code:**
```python
text_s, audio_s, video_s = 0.80, 0.65, 0.70
fused = 0.5 * text_s + 0.3 * audio_s + 0.2 * video_s
print("fused score:", round(fused, 2))
```

## Q95: What is aspect extraction in ABSA?
**A:** Aspect extraction identifies specific aspects/features mentioned. Approaches: 1) Rule-based (dependency patterns). 2) Sequence labeling (NER-like with BIO tagging). 3) BERT-based (fine-tune token classification). 4) Joint extraction and classification.
**Code:**
```python
import spacy
nlp = spacy.load("en_core_web_sm")
doc = nlp("The battery life is amazing.")
print([c.text for c in doc.noun_chunks])
```

## Q96: What are end-to-end ABSA models?
**A:** End-to-end ABSA simultaneously extracts aspects and predicts sentiment without separate pipeline stages. Models like BERT-ABSA, Span-ASTE use unified architectures. Reduces error propagation from pipeline approaches.
**Code:**
```python
from textblob import TextBlob
text = "The food was great but the service was slow."
for sent in TextBlob(text).sentences:
    p = sent.sentiment.polarity
    print(sent.string.strip(), "->", "positive" if p > 0 else "negative")
```

## Q97: How do you handle sentiment in conversational AI?
**A:** In chatbots and voice assistants: 1) Real-time sentiment tracking across turns. 2) Context from conversation history. 3) Handle mixed sentiments within turns. 4) Respond empathetically based on detected sentiment. 5) Transfer learning from general sentiment to conversational.
**Code:**
```python
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()
history = []
for turn in ["how can I help?", "I am really upset my order is late",
             "and now it shows cancelled"]:
    history.append(sia.polarity_scores(turn)["compound"])
print("per turn:", [round(h, 2) for h in history])
print("escalate if min < -0.3:", min(history) < -0.3)
```

## Q98: What is sentiment-aware recommendation?
**A:** Combines sentiment analysis with recommendation systems. Instead of just using ratings, sentiment from review text provides richer signals about user preferences. Improves recommendation quality by understanding why users like/dislike items.
**Code:**
```python
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()
reviews = {"A": ["love the camera", "great screen", "terrible battery"],
           "B": ["it's fine", "nothing special", "does the job"]}
def rec(product):
    scores = [sia.polarity_scores(r)["compound"] for r in reviews[product]]
    return sum(scores) / len(scores)
print({p: round(rec(p), 3) for p in reviews})
```

## Q99: How do you evaluate a deployed sentiment model?
**A:** Ongoing evaluation: 1) Track production metrics (distribution of predictions, confidence scores). 2) Human evaluation on random samples. 3) A/B testing with model updates. 4) Monitor for drift. 5) Collect user feedback. 6) Golden dataset for regression testing.
**Code:**
```python
predicted = ["positive", "negative", "positive", "neutral"]
gold = ["positive", "positive", "positive", "neutral"]
agree = sum(p == g for p, g in zip(predicted, gold)) / len(gold)
print("golden-set agreement:", agree)
```

## Q100: What are the future trends in sentiment analysis?
**A:** 1) Large language models (GPT-4, Llama) for nuanced understanding. 2) Multimodal sentiment (text + audio + video). 3) Few-shot and zero-shot (reduce annotation needs). 4) Explainable sentiment (LLMs can explain reasoning). 5) Real-time on-device processing. 6) Personalized sentiment (adapt to user expression patterns). 7) Ethical and responsible sentiment AI.
**Code:**
```python
from transformers import pipeline
zs = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
t = "The assistant asked follow-ups and actually remembered context."
print(zs(t, candidate_labels=["positive", "negative", "neutral"]))
```