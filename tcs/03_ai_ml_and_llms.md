# AI, ML, NLP, and LLMs

**Q1. What is RAG (Retrieval-Augmented Generation) and how did you implement it?**
**Answer:** RAG is a framework that improves the quality of LLM-generated responses by grounding the model on external, retrieved information rather than just relying on internal weights. 
In my projects, I implemented RAG by taking user documents, breaking them into chunks, generating embeddings, and storing them in a vector database. When a user queries, the system embeds the query, retrieves the most semantically similar text chunks, and feeds them into the LLM as context to generate an accurate and hallucination-free answer.

**Q2. Explain the role of Word Embeddings in NLP.**
**Answer:** Word embeddings are dense vector representations of words where words with similar meanings have similar vector representations in a continuous vector space. Models like Word2Vec, GloVe, or modern Transformer-based embeddings capture the semantic relationships between text. They handle the drawback of sparse representations like One-Hot Encoding and are crucial for tasks like sentiment analysis and similarity search.

**Q3. How do Transformer architectures differ from older RNNs/LSTMs?**
**Answer:** RNNs and LSTMs process data sequentially, which makes them slow and difficult to parallelize, and they struggle with long-range dependencies over long text sequences.
Transformers use a mechanism called **Self-Attention**, which allows the model to look at all words in a sequence simultaneously and weigh their importance relative to each other. This enables massive parallelization and a much better understanding of context and long-range dependencies, forms the backbone of models like BERT, GPT, and Gemini.

**Q4. You mentioned using BERT and VADER for sentiment analysis in your NullClass internship. Compare them.**
**Answer:** 
- **VADER** is a lexicon and rule-based sentiment analysis tool specifically attuned to sentiments expressed in social media. It relies on a predefined dictionary of words and rules to calculate polarity. It's fast and requires no training but struggles with complex context.
- **BERT** (Bidirectional Encoder Representations from Transformers) is a deep learning model. It understands bidirectional context in text. For sentiment analysis, BERT is fine-tuned on labeled data. It is much more accurate at detecting sarcasm, negation, and complex phrasing compared to VADER, though computationally heavier.

**Q5. What is the LangChain framework, and why use it?**
**Answer:** LangChain is a framework designed to simplify the creation of applications using LLMs. It provides abstractions for chaining together components like prompts, models, output parsers, memory, and external tools/APIs. I use it because it makes developing AI agents much easier—for instance, allowing an LLM to dynamically decide to query a database or surf the web using tool integrations.

**Q6. What is the Agno framework, and what was your open-source contribution to it?**
**Answer:** Agno is a lightweight framework for building multi-agent AI systems. I contributed to the open-source repository by implementing Milvus reranking capabilities (which improves RAG retrieval quality), fixing JSON filter parsing bugs, and adding proxy configurations for the Crawl4AI toolkit, ensuring enterprise environments could use the web crawler securely.

**Q7. Explain Fine-tuning vs. Prompt Engineering.**
**Answer:** 
- **Prompt Engineering:** Structuring the input queries to guide a pre-trained LLM towards the desired output without changing the model's weights. Techniques include zero-shot, few-shot, and chain-of-thought prompting.
- **Fine-Tuning:** Updating the actual weights of a pre-trained model by training it on a specific dataset. It is used when prompt engineering isn't enough, particularly for adopting a highly specific tone, structure, or specialized domain knowledge.
