# Text Preprocessing — NLP Pipeline for Recommendation Systems

## 1. Overview of Text in Recommendation Systems

### 1.1 Text Data Sources

| Data Source | Example | Volume | Use Case |
|------------|---------|--------|----------|
| Item Title | "Sony WH-1000XM5 Wireless Noise Canceling Headphones" | 1 field per item | Item similarity, search matching |
| Item Description | Long-form product description | 1 field per item | Content-based features, embedding generation |
| User Reviews | "Great sound quality, comfortable for long sessions" | Millions per day | Sentiment features, aspect extraction |
| Search Queries | "wireless headphones under $200" | Millions per day | Query understanding, intent classification |
| Category/Tags | "Electronics > Audio > Headphones > Over-Ear" | Hierarchical | Taxonomy-based features, category embeddings |
| User-Generated Content | Playlist titles, collection names, notes | Millions | Interest extraction, collaborative signals |

### 1.2 Why Text Preprocessing Matters

- **Noise Reduction**: Raw text contains noise (HTML, special characters, stopwords) that degrades model performance.
- **Normalization**: Different representations of the same concept ("iPhone 15", "Apple iPhone 15", "iPhone15") must be normalized.
- **Dimensionality Reduction**: Raw text has thousands of unique tokens; processed text has a manageable vocabulary.
- **Semantic Preservation**: Good preprocessing preserves the meaning of the text while removing noise.

---

## 2. Tokenization

### 2.1 Word-Level Tokenization

Split text into individual words based on whitespace and punctuation.

- **Simple Split**: `text.split()` — fast but naive. Does not handle contractions ("don't" → "do" + "n't"), hyphens ("state-of-the-art" → "state" + "of" + "the" + "art"), or special characters.
- **Regex Tokenization**: Use regular expressions to define more sophisticated splitting rules. NLTK's `word_tokenize` uses the Penn Treebank tokenizer, which handles contractions and punctuation correctly.
- **Whitespace + Lowercase + Strip**: The most common preprocessing pipeline: lowercase, strip punctuation, split on whitespace.

### 2.2 Subword Tokenization

Split text into subword units that balance between character-level and word-level representations.

- **Byte-Pair Encoding (BPE)**: Iteratively merges the most frequent pair of adjacent tokens. Used by GPT models. Handles out-of-vocabulary (OOV) words gracefully.
- **WordPiece**: Similar to BPE but uses a likelihood-based merging criterion rather than frequency. Used by BERT.
- **SentencePiece**: Language-agnostic tokenization that works directly on raw text without pre-tokenization. Used by multilingual models (mBERT, XLM-R).

**Advantages of Subword Tokenization**: Handles rare words and misspellings (common in user-generated content); vocabulary is fixed size; works across languages without language-specific tokenizers.

### 2.3 Tokenization for Recommendation Text

| Text Type | Recommended Tokenizer | Rationale |
|-----------|----------------------|-----------|
| Product Titles | Regex + Lowercase | Short, structured, domain-specific terms |
| Product Descriptions | BPE/WordPiece | Longer text with diverse vocabulary |
| User Reviews | Subword (SentencePiece) | Noisy, informal, contains misspellings |
| Search Queries | Subword + Domain Rules | Short, intent-driven, contains abbreviations |
| Category Hierarchy | Split on Delimiter | Structured, predictable format |

---

## 3. Stop Word Removal

### 3.1 What Are Stop Words?

Stop words are common words that appear frequently across all documents but carry little semantic meaning for the specific task. Examples: "the", "is", "at", "which", "on", "a", "an".

### 3.2 Stop Word Lists

- **NLTK Default**: 179 English stop words. Conservative list that removes only the most common words.
- **spaCy Default**: 326 stop words. More aggressive than NLTK.
- **Custom Domain-Specific**: Recommendation systems often need custom stop word lists that include domain-specific noise:
  - E-commerce: "buy", "shop", "free", "shipping", "click", "save" (common in product titles but not meaningful for similarity)
  - Media: "watch", "listen", "stream", "play" (common across all content)
  - Generic: "new", "best", "top", "review" (marketing noise)

### 3.3 When NOT to Remove Stop Words

- **Sentence Embeddings**: Modern transformer models (BERT, SBERT) are pre-trained with stop words included. Removing them degrades the quality of sentence embeddings because the model expects grammatically complete sentences.
- **Short Text**: In short texts (titles, queries), stop words may carry important context. Removing "not" from "not good" destroys the sentiment.
- **Sentiment Analysis**: Stop words like "not", "very", "really" carry sentiment intensity. Removing them weakens sentiment signals.

---

## 4. Stemming and Lemmatization

### 4.1 Stemming

Reduces words to their root form by removing suffixes using rule-based heuristics.

- **Porter Stemmer**: The most widely used stemmer. Applies a series of suffix-stripping rules. Example: "running" → "run", "better" → "better" (fails to reduce to "good"), "studies" → "studi" (not a real word).
- **Snowball Stemmer**: An improved version of Porter with better handling of irregular words and support for multiple languages.
- **Lancaster Stemmer**: More aggressive than Porter; produces shorter stems but may over-stem.

**Properties**: Fast (O(n) per word); produces non-dictionary stems; may over-stem (different words mapped to same stem) or under-stem (same word mapped to different stems).

### 4.2 Lemmatization

Reduces words to their dictionary form (lemma) using vocabulary and morphological analysis.

- **WordNet Lemmatizer**: Uses WordNet dictionary to find the lemma. Requires part-of-speech (POS) tagging to determine the correct form. Example: "better" → "good" (requires POS tag: adjective), "running" → "run" (requires POS tag: verb).
- **spaCy Lemmatizer**: Uses a statistical model for POS tagging + rule-based lemmatization. Fast and accurate for English.
- **spaCy + Contextual Lemmatizer**: Uses transformer-based POS tagging for more accurate lemmatization in context.

**Properties**: Produces real dictionary words; slower than stemming (requires POS tagging); more accurate than stemming; language-dependent.

### 4.3 Stemming vs Lemmatization for Recommendation Systems

| Criterion | Stemming | Lemmatization |
|-----------|----------|--------------|
| Speed | Fast | Slower (3–10×) |
| Output Quality | Non-dictionary stems | Dictionary words |
| Accuracy | Lower (over-stems, under-stems) | Higher (context-aware) |
| Multilingual Support | Limited | Better with spaCy |
| Use Case | High-volume batch processing | Quality-sensitive applications |
| Recommendation | Use Snowball for batch; lemmatize for embeddings | |

---

## 5. TF-IDF Vectorization

### 5.1 Standard TF-IDF

Converts a collection of text documents into a matrix of TF-IDF features.

- **Vocabulary Construction**: Build vocabulary from training corpus. Limit size by frequency thresholds (min_df, max_df) or max_features.
- **TF-IDF Computation**: For each document, compute TF-IDF scores for each vocabulary term.
- **Output**: Sparse matrix of shape (n_documents × vocabulary_size).

### 5.2 TF-IDF Hyperparameter Tuning for Recommendation Text

| Parameter | Recommended Range | Effect |
|-----------|------------------|--------|
| max_features | 10,000–50,000 | Vocabulary size; larger captures more terms but increases dimensionality |
| ngram_range | (1, 2) | Include bigrams to capture phrases like "wireless headphones" |
| min_df | 3–10 | Ignore very rare terms (appearing in < N documents) |
| max_df | 0.8–0.95 | Ignore very common terms (appearing in > X% of documents) |
| sublinear_tf | True | Apply log normalization to TF: 1 + log(TF) instead of raw TF |
| norm | "l2" | L2-normalize each document vector |

### 5.3 TF-IDF for Similarity Computation

TF-IDF vectors are commonly used for item-to-item similarity in recommendation systems:

1. Compute TF-IDF vectors for all items.
2. Compute cosine similarity between item TF-IDF vectors.
3. For each item, retrieve the K most similar items.
4. Use these similarities as features in the recommendation model or as a standalone similarity-based recommender.

---

## 6. Word Embeddings

### 6.1 Pre-trained Word Embeddings

| Model | Dimensions | Vocabulary | Training Corpus | File Size |
|-------|-----------|-----------|-----------------|-----------|
| Word2Vec (Google News) | 300 | 3M | Google News (100B words) | 1.6 GB |
| GloVe (6B) | 300 | 400K | Wikipedia + Gigaword | 822 MB |
| GloVe (840B) | 300 | 2.2M | Common Crawl | 5.4 GB |
| FastText (English) | 300 | 1M | Wikipedia | 1.2 GB |

### 6.2 Document Embedding from Word Embeddings

To represent an item description or review as a single vector:

- **Average Pooling**: Average all word embeddings in the document. Simple, fast, but loses word order information.
- **TF-IDF Weighted Average**: Weight each word embedding by its TF-IDF score before averaging. Gives more importance to semantically significant words.
- **SIF Embedding (Smooth Inverse Frequency)**: Weight word embeddings by 1/frequency, subtract the first principal component, and average. Produces higher-quality sentence embeddings than simple averaging.

### 6.3 Contextual Word Embeddings

Modern NLP uses contextual embeddings where the same word has different representations based on context:

- **BERT (Bidirectional Encoder Representations from Transformers)**: Produces a 768-dimensional contextual embedding for each token. The [CLS] token embedding represents the full document.
- **RoBERTa**: An optimized BERT variant with better performance on downstream tasks.
- **DistilBERT**: A distilled version of BERT (66M parameters vs 110M) with 97% of BERT's performance but 60% faster inference.

---

## 7. Sentence and Document Embeddings

### 7.1 Sentence-BERT (SBERT)

Fine-tuned BERT model specifically optimized for producing semantically meaningful sentence embeddings.

- **Architecture**: Siamese network that takes two sentences and produces cosine similarity predictions.
- **Output**: 384-dimensional or 768-dimensional sentence embedding.
- **Performance**: Significantly outperforms BERT [CLS] embedding, average word embedding, and SIF for semantic similarity tasks.
- **Use in Recommendation Systems**: Generate item description embeddings → compute cosine similarity → similar items retrieval.

### 7.2 Universal Sentence Encoder (USE)

Google's pre-trained model for computing universal sentence embeddings.

- **Architecture**: DAN (Deep Averaging Network) or Transformer-based.
- **Output**: 512-dimensional sentence embedding.
- **Advantage**: Fast inference; available as a TensorFlow Hub module.
- **Use Case**: Quick, high-quality sentence embeddings for item descriptions and reviews.

### 7.3 Multilingual Sentence Embeddings

For recommendation systems operating across languages:

- **LaBSE (Language-agnostic BERT Sentence Embedding)**: Trained on 6 billion sentence pairs across 109 languages. Produces aligned embeddings across languages — "wireless headphones" (English) and "casque sans fil" (French) have similar embeddings.
- **Multilingual Sentence Transformers**: Fine-tuned multilingual models that produce aligned embeddings for 50+ languages.
- **Cross-Lingual Similarity**: Enable cross-lingual item similarity — an English product description can be matched with a French product description in the same embedding space.

---

## 8. Multilingual Preprocessing

### 8.1 Language Detection

Before language-specific preprocessing, detect the language of each text document:

- **FastText Language Identification**: Facebook's language identification model, classifying text into 176 languages. Fast and accurate for short texts.
- **langdetect / langid**: Python libraries for language detection. Less accurate than FastText for short texts.
- **spaCy Language Detection**: Integrated into spaCy's pipeline for languages it supports.

### 8.2 Language-Specific Preprocessing

| Language | Challenges | Recommended Pipeline |
|----------|-----------|---------------------|
| English | Contractions, phrasal verbs | Standard English pipeline (NLTK/spaCy) |
| Chinese | No whitespace; word segmentation required | jieba or HanLP for segmentation; then standard NLP |
| Japanese | Mixed scripts (hiragana, katakana, kanji); no spaces | MeCab/Janome for segmentation; language-specific stop words |
| Korean | Agglutinative morphology; no spaces | KoNLPy for segmentation |
| Arabic | Right-to-left; complex morphology; diacritics | CamelTools for preprocessing; AraBERT for embeddings |
| Hindi | Devanagari script; compound words | Hindi stemmer; IndicNLP library |

### 8.3 Cross-Lingual Normalization

- **Transliteration**: Convert text from one script to another (e.g., Cyrillic to Latin) to enable cross-lingual matching.
- **Translation**: For high-value items, translate descriptions to a common language (typically English) for cross-lingual similarity computation.
- **Unicode Normalization**: Apply NFC or NFD Unicode normalization to handle different representations of the same characters (e.g., é as a single character vs. e + combining accent).

---

## 9. Text Preprocessing Pipeline Summary

### 9.1 End-to-End Pipeline

```
Raw Text
    ↓
Language Detection
    ↓
HTML/XML Tag Removal
    ↓
Unicode Normalization
    ↓
Lowercasing
    ↓
Special Character Removal / Normalization
    ↓
Tokenization (language-appropriate)
    ↓
Stop Word Removal (if applicable)
    ↓
Stemming or Lemmatization
    ↓
Vocabulary Filtering (min/max frequency)
    ↓
Feature Extraction:
    ├── TF-IDF (for non-neural models)
    ├── Word Embeddings (average/SIF for simple models)
    └── Sentence Embeddings (SBERT/USE for deep learning)
    ↓
Output: Numerical Feature Vector
```

### 9.2 Preprocessing for Different Model Types

| Model Type | Text Preprocessing Level | Feature Extraction |
|-----------|------------------------|-------------------|
| Logistic Regression / XGBoost | Full pipeline (clean, tokenize, remove stops, lemmatize) | TF-IDF with bigrams |
| Neural Network (DNN) | Minimal pipeline (lowercase, basic cleanup) | Pre-trained word embeddings (averaged) |
| Transformer (BERT/SBERT) | Minimal pipeline (tokenize only) | Model-native tokenization + embeddings |
| Hybrid (CF + Content) | Full pipeline for content features | TF-IDF or embeddings depending on integration |
