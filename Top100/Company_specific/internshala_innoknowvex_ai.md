# Innoknowvex — 100 AI Internship Interview Q&A

> Based on Innoknowvex — AI Internship (ML/DL model building, NLP, deployment, edtech)  > Candidate: Aayush Gid (Python/TensorFlow/Keras/BERT/NLP/LLM agents/RAG/Milvus/FAISS/OpenAI API background)

---

## 1. Data Collection & Preparation (Q1–Q14)

**Q1: What are the common sources for collecting datasets in an AI project?**  
A: Public repositories (Kaggle, UCI ML Repository, Google Dataset Search), government APIs, web scraping (BeautifulSoup, Scrapy), company databases, and third-party APIs (Twitter, YouTube, Google Drive). In my Marketing AI Agent project, I pulled data from Gmail, Twitter, and YouTube APIs simultaneously.

**Q2: What is data preprocessing and why is it critical?**  
A: Preprocessing transforms raw data into a clean, model-ready format. It includes handling missing values, encoding categoricals, scaling features, and removing duplicates. Without it, models learn from noise, not signal. My NullClass chatbot required preprocessing text data before feeding it into BERT.

**Q3: How do you handle missing values in a dataset?**  
A: Strategies depend on context: drop rows (if few missing), impute with mean/median (numerical), mode (categorical), use KNN imputation, or forward/backward fill for time series. Pandas makes this straightforward:
```python
df.fillna(df.median(), inplace=True)        # numerical
df['col'].fillna(df['col'].mode()[0])        # categorical
```

**Q4: What is feature normalization and what are the main techniques?**  
A: Normalization scales features to comparable ranges so no single feature dominates. Min-Max scaling maps to [0,1]; StandardScaler zero-centers and unit-variances. NumPy/Pandas + scikit-learn handle this:
```python
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
```

**Q5: What is one-hot encoding and when do you use it?**  
A: One-hot encoding converts categorical variables into binary vectors (one column per category) so ML algorithms don't assume ordinal relationships. Use it for nominal data with low cardinality. For high-cardinality features, target encoding or embeddings are better.

**Q6: How do you handle outliers in a dataset?**  
A: Detect with box plots, Z-scores (|z| > 3), or IQR method. Then decide: remove them, cap at a percentile (winsorize), or log-transform the feature. In NLP datasets, outlier sentences can be length-based (remove extremely short/long).

**Q7: What is the difference between structured, semi-structured, and unstructured data?**  
A: Structured data fits neatly into tables (SQL databases, CSVs). Semi-structured has tags or keys but no rigid schema (JSON, XML). Unstructured is free-form (text, images, audio). My ScriptVector project processes unstructured Hindi text and stores metadata in structured SQLite.

**Q8: How do you handle categorical data with many unique values (high cardinality)?**  
A: Avoid one-hot encoding (creates sparse, high-dim data). Instead use: label encoding, target encoding, frequency encoding, or learned embeddings. For NLP, tokenization + embedding layers handle this naturally.

**Q9: What is the difference between data cleaning and data transformation?**  
A: Cleaning fixes quality issues (missing values, duplicates, typos, inconsistent formats). Transformation reshapes data for modeling (scaling, encoding, feature engineering, dimensionality reduction). Both are sequential steps in a preprocessing pipeline.

**Q10: How do you split data into training, validation, and test sets?**  
A: Typical split is 70/15/15 or 80/10/10. Use stratified splitting for classification to preserve class ratios:
```python
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
```
Never touch test data until final evaluation.

**Q11: What is feature engineering? Give examples relevant to AI/ML.**  
A: Creating new input features from raw data. Examples: TF-IDF vectors from text, polynomial features, rolling averages for time series, word count/character count from documents. In my NLP sentiment pipeline, I engineered features like sentence length and sentiment polarity scores before classification.

**Q12: How do you deal with imbalanced datasets?**  
A: Use resampling (SMOTE for oversampling minority, random undersampling for majority), class weights in model training (`class_weight='balanced'`), or evaluation metrics that account for imbalance (F1, ROC-AUC) instead of accuracy.

**Q13: What is a data pipeline and why build one?**  
A: A data pipeline automates the flow from raw data ingestion → cleaning → transformation → feature extraction → model input. It ensures reproducibility and scalability. Tools: Pandas scripts, scikit-learn Pipelines, or Airflow for orchestration.

**Q14: Describe your experience using Pandas and NumPy for data preparation.**  
A: I use Pandas for tabular data manipulation (filtering, grouping, merging, handling NaNs) and NumPy for numerical array operations and vectorized math. In my NullClass internship, I cleaned NLP datasets with `pandas.read_csv()`, applied `.dropna()`, `.fillna()`, `.apply()` for text preprocessing, and NumPy for feature array construction.

---

## 2. Research & Exploration (Q15–Q25)

**Q15: What is Exploratory Data Analysis (EDA) and why do it before modeling?**  
A: EDA uses statistics and visualizations (histograms, scatter plots, correlation heatmaps) to understand distributions, relationships, and anomalies in data. It reveals which features matter and what transformations are needed before building models. I use Matplotlib/Seaborn for this.

**Q16: What are the key libraries you use for data visualization?**  
A: Matplotlib for foundational plots (line, bar, scatter, histogram), Seaborn for statistical visualizations (heatmaps, pair plots, box plots), and Plotly for interactive dashboards. My Marketing AI Agent used Streamlit + Matplotlib for a live analytics dashboard.

**Q17: How do you read a correlation matrix and use it in feature selection?**  
A: A correlation matrix shows Pearson/Spearman correlation between every pair of features. Values near ±1 indicate strong linear relationships. Drop one of two highly correlated features (>0.9) to reduce multicollinearity. Use `df.corr()` in Pandas and `sns.heatmap()` to visualize.

**Q18: What is a literature review in the context of AI projects?**  
A: Reviewing published papers (arXiv, IEEE, ACL), blog posts, and GitHub repos to understand state-of-the-art approaches for a given problem. It prevents reinventing the wheel and helps choose proven architectures. For my face mask detection project, I reviewed CNN-based approaches before implementing.

**Q19: How do you define an AI solution for a business problem?**  
A: Start with the business objective, identify what data is available, determine if it's a classification/regression/clustering/generation problem, select candidate algorithms, define success metrics, and prototype. The key is translating business language into technical requirements.

**Q20: What is the difference between supervised, unsupervised, and reinforcement learning?**  
A: Supervised: labeled data, learn input→output mapping (classification, regression). Unsupervised: no labels, find structure (clustering, dimensionality reduction). Reinforcement: agent learns by trial-and-error in an environment via rewards. Most edtech applications (recommendation, prediction) use supervised learning.

**Q21: What is transfer learning and why is it powerful?**  
A: Transfer learning reuses a pre-trained model (trained on a large dataset) and fine-tunes it on a smaller, task-specific dataset. It saves time and compute. I applied this with BERT for sentiment analysis at NullClass — fine-tuning a pre-trained BERT on our text classification task.

**Q22: How do you decide which ML approach to use for a given problem?**  
A: Consider: data type (tabular/text/image), data size, problem type (classification/regression/clustering), interpretability needs, latency requirements, and available compute. Start simple (logistic regression, random forest), then escalate to deep learning only if justified.

**Q23: What is a dataset's "cardinality" and why does it matter?**  
A: Cardinality refers to the number of unique values in a column or the number of rows in a dataset. High-cardinality categorical features need special encoding. Small datasets risk overfitting with complex models. Understanding cardinality guides preprocessing and model complexity choices.

**Q24: How do you handle text data for AI tasks?**  
A: Tokenization (split into tokens), lowercasing, stopword removal, lemmatization/stemming, then vectorization (TF-IDF, Word2Vec, or transformer embeddings like BERT). My NullClass chatbot pipeline: raw text → clean → tokenize → BERT embeddings → sentiment classifier.

**Q25: What tools do you use for data exploration in practice?**  
A: Jupyter notebooks for interactive EDA, Pandas `.describe()`, `.info()`, `.value_counts()`, Seaborn/Matplotlib for plots, and `pandas-profiling` (ydata-profiling) for automated reports. I combine these with git-tracked notebooks for version control.

---

## 3. Model Development & Training: Core ML (Q26–Q42)

**Q26: What is a loss function and why does it matter?**  
A: A loss function quantifies the difference between predicted and actual values. The optimizer minimizes it during training. Common losses: cross-entropy (classification), MSE/MAE (regression). Choosing the wrong loss misguides learning.

**Q27: What is gradient descent and how does it work?**  
A: Gradient descent iteratively adjusts model weights in the direction that reduces the loss. It computes partial derivatives of the loss w.r.t. each weight and takes a step proportional to the learning rate. Variants: batch, stochastic (SGD), and mini-batch gradient descent.

**Q28: What is the learning rate and how do you choose it?**  
A: The learning rate controls step size during optimization. Too high → diverges; too low → slow convergence or stuck in local minima. Common starting points: 1e-3 for Adam, 1e-2 for SGD. Use learning rate schedulers (cosine annealing, ReduceLROnPlateau) for fine-tuning.

**Q29: What is the difference between Adam and SGD optimizers?**  
A: SGD updates weights using only the gradient. Adam combines momentum (past gradients) and RMSprop (adaptive per-parameter learning rates), converging faster with less tuning. Adam is the default for most deep learning; SGD with momentum sometimes generalizes better on vision tasks.

**Q30: What is overfitting and how do you prevent it?**  
A: Overfitting is when a model memorizes training data but fails on unseen data. Prevention: regularization (L1/L2), dropout, early stopping, data augmentation, cross-validation, reducing model complexity, and using more training data.

**Q31: What is underfitting?**  
A: Underfitting occurs when a model is too simple to capture the underlying patterns — it performs poorly on both training and test data. Fix: increase model complexity, add features, train longer, or reduce regularization.

**Q32: What is regularization? Explain L1 vs L2.**  
A: Regularization adds a penalty to the loss to discourage complex models. L1 (Lasso) adds absolute weight values, driving some weights to zero (feature selection). L2 (Ridge) adds squared weights, shrinking all weights toward zero (prevents large weights). In Keras:
```python
from keras.regularizers import l2
model.add(Dense(64, activation='relu', kernel_regularizer=l2(0.01)))
```

**Q33: What is dropout and when do you use it?**  
A: Dropout randomly deactivates a fraction of neurons during each training step, forcing the network to learn redundant representations. It's a strong regularizer for dense and convolutional layers. Typical rate: 0.2–0.5. Disable during inference.

**Q34: What is a decision tree and how does it differ from a random forest?**  
A: A decision tree splits data on feature thresholds to make predictions — easy to interpret but prone to overfitting. A random forest is an ensemble of many decision trees trained on random subsets of data and features, reducing variance and overfitting significantly.

**Q35: Explain the bias-variance tradeoff.**  
A: High bias = underfitting (model too simple). High variance = overfitting (model too complex, sensitive to training data). The goal is finding the sweet spot where total error (bias² + variance + noise) is minimized. Regularization and ensemble methods help navigate this tradeoff.

**Q36: What is cross-validation and why use it?**  
A: Cross-validation (e.g., 5-fold) splits data into K folds, trains on K-1, validates on the remaining, and rotates. It gives a more reliable performance estimate than a single train/val split and maximizes data usage.
```python
from sklearn.model_selection import cross_val_score
scores = cross_val_score(model, X, y, cv=5, scoring='f1')
```

**Q37: What is a confusion matrix?**  
A: A confusion matrix summarizes predictions vs actuals: TP, TN, FP, FN. From it, you derive accuracy, precision, recall, and F1. It reveals where the model is confused (e.g., which classes it misclassifies).

**Q38: When would you choose precision over recall?**  
A: When false positives are costly (e.g., spam detection — don't want legitimate emails marked spam), optimize for precision. When false negatives are costly (e.g., disease detection — don't want to miss cases), optimize for recall. F1 balances both.

**Q39: What is ROC-AUC and when is it useful?**  
A: ROC-AUC measures a model's ability to distinguish between classes across all threshold settings. AUC = 1.0 is perfect; 0.5 is random. It's especially useful for imbalanced datasets where accuracy is misleading. Plot the ROC curve with `sklearn.metrics.roc_curve`.

**Q40: What is scikit-learn and what are its key components?**  
A: scikit-learn is Python's standard ML library providing: classifiers/regressors (SVM, Random Forest, KNN), preprocessing (StandardScaler, OneHotEncoder), model selection (GridSearchCV, cross_val_score), and metrics. I use it extensively for classical ML baselines before deep learning.

**Q41: How do you perform hyperparameter tuning?**  
A: Use GridSearchCV (exhaustive), RandomizedSearchCV (sampled), or Bayesian optimization (Optuna). Define a parameter grid, specify a metric, and let cross-validation find the best combo:
```python
from sklearn.model_selection import GridSearchCV
grid = GridSearchCV(estimator, param_grid, cv=5, scoring='f1')
grid.fit(X_train, y_train)
```

**Q42: Describe a complete model training workflow from your experience.**  
A: (1) Load/clean data with Pandas, (2) split into train/val/test, (3) preprocess and vectorize, (4) train baseline model (e.g., LogisticRegression), (5) train complex model (e.g., neural network), (6) tune hyperparameters, (7) evaluate on test set, (8) save model. I followed this pattern for my NullClass sentiment analysis project.

---

## 4. Deep Learning & Neural Networks (Q43–Q58)

**Q43: What is a neural network and how does it learn?**  
A: A neural network is a stack of layers of interconnected neurons that learn weight parameters via backpropagation. Each neuron computes a weighted sum + bias, applies an activation, and passes the output forward. The loss is propagated backward to update weights via gradient descent.

**Q44: What is TensorFlow and how have you used it?**  
A: TensorFlow is Google's open-source deep learning framework for building and training neural networks. I used TensorFlow + Keras for my IEEE face mask detection project — building a CNN to classify masked/unmasked faces. It provides eager execution, `tf.data` for pipelines, and `tf.keras` for high-level model building.

**Q45: What is Keras and how does it relate to TensorFlow?**  
A: Keras is a high-level API (now part of TensorFlow as `tf.keras`) for building neural networks with simple, readable code. It offers Sequential and Functional APIs for defining layers, compile/train/evaluate workflows, and callbacks like EarlyStopping. Most of my DL work uses `tf.keras`.

**Q46: What is a Convolutional Neural Network (CNN) and when do you use it?**  
A: CNNs use convolutional filters to extract spatial features from images. Key layers: Conv2D (feature extraction), MaxPooling2D (downsampling), Flatten/Dense (classification). Used for image classification, object detection, and face recognition. My face mask detection model was a CNN.

**Q47: What is a Recurrent Neural Network (RNN) and what are its limitations?**  
A: RNNs process sequential data by maintaining a hidden state across time steps. Limitations: vanishing/exploding gradients, difficulty learning long-range dependencies. LSTMs and GRUs address this with gating mechanisms. Transformers have largely replaced RNNs for NLP.

**Q48: What is an LSTM and how does it improve over vanilla RNNs?**  
A: LSTM (Long Short-Term Memory) adds three gates — forget, input, output — that regulate what information to retain or discard over long sequences. This solves the vanishing gradient problem and enables learning long-range dependencies in text, time series, and speech.

**Q49: What is a Transformer architecture?**  
A: Transformers process all tokens in parallel using self-attention, which computes relationships between every pair of tokens. This eliminates recurrence, enabling faster training and better long-range dependency capture. BERT, GPT, and Gemini are all Transformer-based.

**Q50: What is the difference between BERT and GPT?**  
A: BERT is bidirectional (reads context from both left and right), pre-trained with masked language modeling — great for classification, NER, and Q&A. GPT is autoregressive (left-to-right), pre-trained with next-token prediction — great for text generation. I fine-tuned BERT for sentiment classification at NullClass.

**Q51: What is batch normalization and why use it?**  
A: Batch normalization normalizes layer inputs per mini-batch, stabilizing and accelerating training. It reduces internal covariate shift, allows higher learning rates, and acts as mild regularization. In Keras:
```python
model.add(tf.keras.layers.BatchNormalization())
```

**Q52: What is the difference between the Sequential and Functional APIs in Keras?**  
A: Sequential is a linear stack of layers (simple models). Functional API supports multi-input/multi-output, shared layers, and complex architectures (e.g., residual connections). Use Functional for anything beyond a simple pipeline.

**Q53: What are activation functions and why are they needed?**  
A: Activations introduce non-linearity so the network can learn complex patterns. Common ones: ReLU (hidden layers, fast), Sigmoid (binary output), Softmax (multi-class output), Tanh (zero-centered). Without them, a multi-layer network collapses to a single linear transformation.

**Q54: What is early stopping and how do you implement it?**  
A: Early stopping monitors a validation metric (e.g., val_loss) and halts training when it stops improving, preventing overfitting. In Keras:
```python
callback = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
model.fit(X_train, y_train, validation_split=0.15, callbacks=[callback], epochs=100)
```

**Q55: What is a loss function for multi-class classification?**  
A: Use `categorical_crossentropy` when labels are one-hot encoded, or `sparse_categorical_crossentropy` when labels are integers. Both measure the distance between predicted probability distributions and true labels.

**Q56: What is data augmentation and how does it help?**  
A: Data augmentation artificially increases training data diversity by applying transformations (rotation, flip, crop for images; synonym replacement, back-translation for text). It reduces overfitting and improves generalization without collecting more real data.

**Q57: How do you save and load a trained model?**  
A: In TensorFlow/Keras:
```python
model.save('model.keras')                    # save
model = tf.keras.models.load_model('model.keras')  # load
```
For scikit-learn, use `joblib.dump(model, 'model.pkl')`. This is essential for deployment — I saved BERT models after fine-tuning at NullClass.

**Q58: What is the purpose of an embedding layer in deep learning?**  
A: An embedding layer maps discrete tokens (words, categories) to dense, continuous vectors of fixed dimension. It learns semantic relationships during training. In NLP, word embeddings capture that "king" - "man" + "woman" ≈ "queen". Pre-trained embeddings (Word2Vec, GloVe, BERT) are often used.

---

## 5. NLP, LLMs & Intelligent Agents (Q59–Q72)

**Q59: What is NLP and what are its core subtasks?**  
A: NLP (Natural Language Processing) enables machines to understand and generate human language. Subtasks: tokenization, named entity recognition, sentiment analysis, text classification, machine translation, summarization, question answering, and text generation. My NullClass chatbot covered sentiment analysis and text classification.

**Q60: What is tokenization and why is it the first step in NLP?**  
A: Tokenization splits text into smaller units (words, subwords, characters) for model processing. Subword tokenizers (BPE, WordPiece used by BERT) handle out-of-vocabulary words gracefully. You can't feed raw strings into a model.

**Q61: What is TF-IDF and when would you use it over word embeddings?**  
A: TF-IDF (Term Frequency-Inverse Document Frequency) weights words by their importance in a document relative to a corpus. Use it for fast, interpretable baselines on smaller datasets. Use embeddings (BERT, Word2Vec) when semantic meaning and context matter more than frequency.

**Q62: How does BERT-based sentiment analysis work?**  
A: Pass text through BERT tokenizer → feed token IDs + attention mask into pre-trained BERT → extract `[CLS]` token embedding → pass through a classification head (Dense layer + Softmax). Fine-tune on your labeled dataset. This is exactly what I built at NullClass for sentiment analysis with BERT and VADER.

**Q63: What is VADER and how does it differ from BERT for sentiment?**  
A: VADER (Valence Aware Dictionary and sEntiment Reasoner) is a rule-based, lexicon-driven sentiment analyzer — fast, no training needed, good for social media text. BERT is a deep learning model that captures context — more accurate but slower and requires training. I used both: VADER for quick baseline, BERT for production accuracy.

**Q64: What are Large Language Models (LLMs)?**  
A: LLMs are Transformer-based models trained on massive text corpora (billions of parameters) that can generate, summarize, translate, and reason about text. Examples: GPT-4, Gemini, Claude. I've worked with OpenAI API and Gemini API for building AI agents.

**Q65: How do you use the OpenAI API effectively?**  
A: Structure prompts clearly with system/user/assistant roles, use `temperature` to control randomness (0 = deterministic, 1+ = creative), leverage function calling for structured outputs, and handle rate limits with retries. I integrated OpenAI in MigratorGen for LLM-based library upgrade parsing and in multiple Agno agent projects.

**Q66: What is RAG (Retrieval-Augmented Generation)?**  
A: RAG combines a retrieval step (fetching relevant documents from a vector store) with a generation step (LLM answers using that context). It grounds LLM responses in real data, reducing hallucinations. I built RAG pipelines using FAISS and Milvus for vector storage, with OpenAI/Gemini embeddings.

**Q67: What are vector embeddings and how are they used in AI?**  
A: Vector embeddings are dense numerical representations of data (text, images) where similar items are close in vector space. They power semantic search, recommendation systems, and RAG. I used OpenAI embeddings stored in Milvus (production) and FAISS (local) for similarity search in my projects.

**Q68: What is the difference between Milvus and FAISS?**  
A: FAISS (Facebook AI) is a lightweight, in-memory library for similarity search — great for prototyping and local use. Milvus is a distributed, scalable vector database with persistence, filtering, and hybrid search — better for production. I used FAISS for local RAG experiments and Milvus for deployed pipelines.

**Q69: What are AI agents and how do they differ from simple chatbots?**  
A: AI agents perceive their environment, reason about goals, and take actions (calling APIs, writing files, searching the web) autonomously. Simple chatbots just generate text responses. My projects demonstrate this: Agno agents that autonomously manage Google Drive, post to social media, and process emails (Marketing AI Agent).

**Q70: What is LangChain and how does it simplify LLM app development?**  
A: LangChain is a framework for building LLM-powered applications. It provides abstractions for chains (sequential prompt→LLM pipelines), agents (tool-using decision makers), memory (conversation history), and retrieval (RAG). I've used it alongside Agno and LangGraph for complex agent workflows.

**Q71: What is a prompt and how do you engineer it for better results?**  
A: A prompt is the input instruction to an LLM. Good prompt engineering: be specific, provide examples (few-shot), define output format, use system messages for role-setting, and iterate. In MigratorGen, I engineered prompts to parse changelogs into structured JSON for code migration.

**Q72: How do you handle LLM hallucinations in production?**  
A: Mitigation strategies: RAG with verified knowledge bases, low temperature for factual tasks, output validation/format enforcement, human-in-the-loop review, chain-of-thought prompting, and grounding responses with retrieved context. Never trust LLM output blindly in production.

---

## 6. Model Evaluation & Experiment Tracking (Q73–Q84)

**Q73: What is the difference between accuracy, precision, recall, and F1?**  
A: Accuracy = (TP+TN)/(all). Precision = TP/(TP+FP) — how many predicted positives are correct. Recall = TP/(TP+FN) — how many actual positives are found. F1 = 2×(precision×recall)/(precision+recall) — harmonic mean balancing both. Use F1 for imbalanced data; accuracy is misleading.

**Q74: When is accuracy a misleading metric?**  
A: With imbalanced classes (99% negative, 1% positive), a model predicting all-negative gets 99% accuracy but is useless. Use precision, recall, F1, ROC-AUC, or PR-AUC instead. Always check the confusion matrix for a full picture.

**Q75: How do you choose the right evaluation metric for a project?**  
A: Match metric to business goal: accuracy for balanced classification, F1 for imbalanced, ROC-AUC for ranking/threshold flexibility, precision when FP are costly, recall when FN are costly, MSE/RMSE for regression, BLEU/ROUGE for text generation. At NullClass, I used F1 for sentiment classification.

**Q76: What is a validation set vs a test set?**  
A: The validation set tunes hyperparameters during development (you see its results and adjust). The test set is held out until the very end for a final, unbiased estimate of real-world performance. Never use test data for training decisions — it leads to overfitting to the test set.

**Q77: How do you compare multiple models fairly?**  
A: Use the same train/val/test splits, same preprocessing pipeline, same evaluation metrics, and run each model multiple times with different seeds. Report mean ± std. Use paired statistical tests (t-test, McNemar's) for significance. Document everything for reproducibility.

**Q78: What is a ROC curve and how do you interpret it?**  
A: ROC curve plots True Positive Rate vs False Positive Rate across all classification thresholds. A curve hugging the top-left corner is excellent (high AUC). A diagonal line means random guessing (AUC = 0.5). Use `sklearn.metrics.roc_curve` and `auc` to compute.

**Q79: What is a precision-recall curve?**  
A: It plots precision vs recall at different thresholds. Useful for imbalanced datasets where ROC can be overly optimistic. A curve close to the top-right is ideal. Area Under PR Curve (AUPRC) summarizes overall performance.

**Q80: What is the Matthews Correlation Coefficient (MCC)?**  
A: MCC is a correlation coefficient between observed and predicted classifications. It returns a value between -1 (total disagreement) and +1 (perfect prediction), and is considered more informative than F1 for imbalanced datasets because it accounts for all four confusion matrix quadrants.

**Q81: How do you evaluate regression model performance?**  
A: Key metrics: MSE (penalizes large errors), RMSE (same scale as target), MAE (robust to outliers), R² (proportion of variance explained). Use MSE/RMSE when large errors are especially undesirable; MAE for robust evaluation.

**Q82: What is experiment tracking and why is it important?**  
A: Experiment tracking logs parameters, metrics, code versions, and artifacts for each training run. It enables comparison, reproducibility, and debugging. Tools: MLflow, Weights & Biases, TensorBoard. Even simple CSV logging beats "I forgot which hyperparameters gave the best result."

**Q83: How do you document an AI project for handoff?**  
A: Document: (1) problem statement and success criteria, (2) data sources and preprocessing steps, (3) model architecture and hyperparameters, (4) training procedure, (5) evaluation results with metrics/plots, (6) known limitations, (7) inference instructions. I use markdown READMEs and inline comments in my repos.

**Q84: What is the difference between offline and online evaluation?**  
A: Offline evaluation tests on held-out data (static metrics). Online evaluation measures real-world performance via A/B testing, user engagement, or live metrics. A model that scores well offline may underperform online due to distribution shift — always validate in production.

---

## 7. Deployment, Integration & MLOps (Q85–Q94)

**Q85: How do you deploy a trained ML model for inference?**  
A: Save the model (`.keras` or `.pkl`), wrap it in a REST API (FastAPI is my go-to), containerize with Docker, and deploy to a cloud platform. For simple demos, Streamlit works well. I deployed BERT sentiment models via FastAPI at NullClass and AI agent services at Krip AI.

**Q86: What is FastAPI and why is it popular for ML model serving?**  
A: FastAPI is an async Python web framework with automatic OpenAPI docs, Pydantic validation, and high performance (comparable to Node.js/Go). It's ideal for ML serving because: native async, easy request/response typing, fast development, and simple model endpoint creation:
```python
from fastapi import FastAPI
app = FastAPI()
@app.post("/predict")
async def predict(text: str):
    return {"sentiment": model.predict([text])}
```

**Q87: What is Docker and how do you use it for AI projects?**  
A: Docker packages an application with all its dependencies into a container, ensuring consistent environments across development and production. For AI: containerize the model, API, and dependencies. I use Docker in all my projects — from CI/CD pipelines at Krip AI to local development for ScriptVector.

**Q88: What is CI/CD and how does it apply to ML projects?**  
A: CI (Continuous Integration) automates testing on every commit. CD (Continuous Delivery) automates deployment. For ML: CI runs unit tests + model validation tests; CD deploys updated models. I set up GitHub Actions for CI/CD at Krip AI, running pytest and Docker builds automatically.

**Q89: What is model monitoring and why is it necessary?**  
A: After deployment, monitor for: data drift (input distribution changes), concept drift (relationship between input/output changes), latency degradation, and error rates. Without monitoring, a model silently degrades. Log predictions, set alerts, and schedule periodic retraining.

**Q90: What is a chatbot and how do you build one with modern AI?**  
A: A chatbot processes user messages and generates responses. Modern approach: LLM-based with RAG for knowledge grounding, conversation memory for context, and tool use for actions. At NullClass, I built an AI chatbot with BERT + VADER; now I'd build it with OpenAI/Gemini + RAG + FastAPI.

**Q91: What is a recommendation engine and what are the main approaches?**  
A: Approaches: (1) Collaborative filtering — recommend based on similar users' preferences, (2) Content-based — recommend similar items based on features, (3) Hybrid — combines both. Deep learning approaches use embeddings for user/item representations. Edtech platforms use these to suggest courses/internships.

**Q92: How do you handle API keys and secrets in deployed AI applications?**  
A: Never hardcode secrets. Use environment variables, secret managers (AWS Secrets Manager, GCP Secret Manager), or platform-specific env vars. In Docker: pass via `docker run -e API_KEY=...` or `.env` files (never committed). I use `.env` + `python-dotenv` in development and platform secrets in production.

**Q93: What is the difference between batch inference and real-time inference?**  
A: Batch inference processes data in bulk on a schedule (e.g., nightly predictions). Real-time inference responds to individual requests instantly (e.g., live chatbot). Batch is cheaper and handles larger volumes; real-time requires low-latency serving infrastructure.

**Q94: How do you ensure a model's predictions are explainable?**  
A: Use SHAP (SHapley Additive exPlanations) for feature importance, LIME for local explanations, attention visualization for Transformers, or simpler surrogate models. Explainability builds trust and is critical in regulated domains. For NLP, attention weights show which words influenced the prediction.

---

## 8. Behavioral, AI Vision & Innoknowvex Fit (Q95–Q100)

**Q95: Why do you want to intern at Innoknowvex?**  
A: Innoknowvex connects students with meaningful internships and mentorship — solving a problem I've personally experienced. Contributing AI models (recommendation engines, predictive systems, chatbots) to an edtech platform directly impacts student outcomes. The AI intern role aligns perfectly with my NLP, LLM agent, and ML deployment experience.

**Q96: Tell us about a challenging AI project you've worked on and what you learned.**  
A: MigratorGen (Code Migration Platform) was the most challenging. I built a Python CLI that uses LLM-based parsing to read changelog files and automatically upgrade library imports via LibCST. The hardest part was handling edge cases in changelog formats — I solved it by designing structured JSON schemas and validating with pytest. It taught me that robust data validation is as important as the model itself.

**Q97: How do you approach learning a new AI technique or framework quickly?**  
A: I follow a hands-on loop: read the official docs/tutorials, run the provided examples, then immediately apply it to a mini-project. For example, when I learned LangChain and Agno, I built ScriptVector (Hindi content generator) within days. The best way to learn AI is to build something, hit errors, and debug.

**Q98: How would you handle a situation where your model's performance is poor and you don't know why?**  
A: Systematic debugging: (1) Check data quality — are labels correct? Is there leakage? (2) Check the pipeline — is preprocessing consistent between train/test? (3) Try a simpler baseline to sanity-check. (4) Visualize errors — what patterns does the model get wrong? (5) Check for overfitting (train vs val gap). (6) Review literature for similar problems. Never assume — diagnose.

**Q99: Where do you see AI in edtech heading in the next 2–3 years?**  
A: Personalized learning paths powered by AI tutors (LLM-based, like my RAG agents), automated assessment with detailed feedback, real-time student engagement prediction, and intelligent internship/course recommendation engines. Innoknowvex is well-positioned to integrate these to better connect students with opportunities.

**Q100: What unique value do you bring to this AI internship?**  
A: Three things: (1) Hands-on production experience — I've deployed AI services (FastAPI + Docker + CI/CD) in real companies, not just notebooks. (2) End-to-end NLP expertise — from BERT fine-tuning to RAG pipelines with vector databases to LLM agent orchestration. (3) Ship-fast mindset — my open-source contributions to Agno and projects like ScriptVector show I learn and deliver quickly. I can contribute meaningfully from week one.
