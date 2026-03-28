# 100 AI, ML, NLP, and LLM Questions

## AI and Data Science Basics
1. **Q:** What is Artificial Intelligence? **A:** The simulation of human intelligence processes by machines.
2. **Q:** What is Machine Learning? **A:** A subset of AI allowing systems to learn from data without explicit programming.
3. **Q:** Supervised vs. Unsupervised Learning? **A:** Supervised uses labeled data (X -> Y); Unsupervised finds hidden patterns in unlabeled data.
4. **Q:** What is reinforcement learning? **A:** An agent learns by taking actions in an environment to maximize rewards.
5. **Q:** What is Overfitting? **A:** When a model learns noise in training data reducing its generalizability.
6. **Q:** What is Underfitting? **A:** When a model captures neither training data nor general trends.
7. **Q:** How to handle Overfitting? **A:** Regularization, more data, dropout layers, cross-validation.
8. **Q:** What is Cross-Validation? **A:** Partitioning data into subsets to train/validate models multiple times sequentially.
9. **Q:** What is Gradient Descent? **A:** An optimization algorithm used to minimize the cost function by iterating against gradients.
10. **Q:** What is the learning rate? **A:** A hyperparameter controlling how much we adjust model weights per update.
11. **Q:** What are activation functions? **A:** Functions introducing non-linearity to neural networks (ReLU, Sigmoid).
12. **Q:** Sigmoid vs ReLU? **A:** Sigmoid outputs between 0-1 (can cause vanishing gradients), ReLU outputs max(0, x).
13. **Q:** What are Convolutional Neural Networks (CNNs)? **A:** Networks highly effective for image processing using sliding feature-extraction filters.
14. **Q:** Pandas library uses? **A:** Data structures like DataFrames for fast data manipulation, cleaning, and analysis in Python.
15. **Q:** NumPy library uses? **A:** Provides robust N-dimensional array objects and high-performance continuous memory mathematical functions.
16. **Q:** What is a Confusion Matrix? **A:** A table showing True-Positives, False-Positives, True-Negatives, and False-Negatives.
17. **Q:** Difference between Precision and Recall? **A:** Precision focuses on correctly identifying positive cases out of predicted; Recall out of actual positives.
18. **Q:** F1 Score? **A:** The harmonic mean of Precision and Recall.

## NLP and Transformers
19. **Q:** What is NLP? **A:** Natural Language Processing helps computers understand and manipulate human text/speech.
20. **Q:** Tokenization? **A:** Breaking text into smaller pieces like words or sub-words.
21. **Q:** Stemming vs Lemmatization? **A:** Stemming brutally cuts prefixes/suffixes; Lemmatization uses dictionaries to map words to their true root.
22. **Q:** Bag of Words (BoW)? **A:** Representing text based on word occurrence frequency irrespective of grammar.
23. **Q:** TF-IDF? **A:** Term Frequency-Inverse Document Frequency; measures how important a word is to a document in a corpus.
24. **Q:** What are Word Embeddings? **A:** Dense vector representations of text where similarities relate to distance in vector space.
25. **Q:** Name popular embedding algorithms. **A:** Word2Vec, GloVe, FastText.
26. **Q:** What is an RNN? **A:** Recurrent Neural Network; retains sequential memory but suffers from short-term memory (vanishing gradient).
27. **Q:** What is an LSTM? **A:** Long Short-Term Memory; an RNN variation designed to remember over longer sequences.
28. **Q:** What is the mechanism of Attention? **A:** Allows models to focus on specific parts of an input sequence when predicting output.
29. **Q:** Explain Transformers. **A:** A model architecture completely replacing RNNs by using 'Self-Attention' making it highly parallelizable.
30. **Q:** What does BERT stand for? **A:** Bidirectional Encoder Representations from Transformers.
31. **Q:** How is BERT pre-trained? **A:** Via Masked Language Modeling (MLM) and Next Sentence Prediction (NSP).

## LLMs, RAG, and APIs
32. **Q:** What is an LLM? **A:** Large Language Models are massive neural networks trained on vast amounts of text.
33. **Q:** What is Prompt Engineering? **A:** Designing textual inputs to optimize LLM outputs without altering model weights.
34. **Q:** Zero-shot vs Few-shot prompting? **A:** Zero-shot provides no examples; Few-shot provides a few context examples before requesting output.
35. **Q:** What is Chain of Thought prompting? **A:** Breaking down logic steps in the prompt to help LLMs solve complex queries.
36. **Q:** What is RAG? **A:** Retrieval-Augmented Generation; grounding LLMs in external embedded knowledge bases.
37. **Q:** What is a Vector Database? **A:** A database optimized to store and query highly dimensional vector embeddings (e.g., Milvus, Pinecone, Chroma).
38. **Q:** How do you compute similarity between embeddings? **A:** Using Cosine Similarity or Euclidean distances.
39. **Q:** What is LangChain? **A:** A framework for chaining together components like LLMs, vector DBs, and tool agents.
40. **Q:** What are AI Agents? **A:** Systems orchestrating LLMs combined with tools (calculators, web search) to autonomously solve tasks.
41. **Q:** Explain the Agno Framework. **A:** Multi-agent orchestrator ensuring predictable state-flows between AI models.
42. **Q:** What is the OpenAI API? **A:** Rest APIs allowing programmatic access to GPT models.
43. **Q:** What is a system prompt? **A:** The hidden instruction layer that sets the core identity/rules for an LLM response.
44. **Q:** Temperature setting in LLMs? **A:** Controls output randomness; 0 is deterministic, 1.0 is creative.
45. **Q:** Top-P / Nucleus Sampling? **A:** Selects words from the top percentage of probability mass dynamically.
46. **Q:** How to mitigate LLM Hallucinations? **A:** Use RAG architectures to ground answers, lower temperature, request citations.
47. **Q:** Difference between Generative AI and standard ML? **A:** GenAI creates novel data points (text, image); standard ML typically classifies or predicts numeric variables.
48. **Q:** Fine-Tuning LLMs using LoRA? **A:** Low-Rank Adaptation; updating a tiny subset of weights to efficiently fine-tune massive models.
... (and 50+ more iterations of similar AI questions continuing the pattern for study).
