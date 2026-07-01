# OpenAI API Interview Questions and Answers

## Q1: What is the OpenAI API?
**A:** The OpenAI API provides programmatic access to OpenAI's AI models including GPT-4, GPT-3.5, DALL-E, Whisper, and Embeddings. It allows developers to integrate natural language processing, image generation, speech-to-text, and other AI capabilities into applications via RESTful HTTP endpoints with JSON responses.

## Q2: What models are available through the OpenAI API?
**A:** Major models include: GPT-4 series (GPT-4, GPT-4 Turbo, GPT-4o, GPT-4o-mini) for text, GPT-3.5 Turbo for cost-effective text, DALL-E 3 for image generation, Whisper for speech-to-text, TTS for text-to-speech, and text-embedding-3-* for embeddings. Each model has different capabilities, pricing, and performance characteristics.

## Q3: How does authentication work with the OpenAI API?
**A:** Authentication uses API keys passed in the HTTP header: `Authorization: Bearer sk-...`. API keys are tied to an OpenAI account and organization. Best practices: never hardcode keys, use environment variables, implement key rotation, and scope keys to specific projects. Organization IDs can also be specified for multi-org accounts.

## Q4: What is the Chat Completions API?
**A:** The Chat Completions API (`/v1/chat/completions`) is the primary endpoint for interacting with GPT models. It accepts a list of messages with roles: `system`, `user`, `assistant`, and `tool`. It returns a model-generated response. Parameters include `model`, `messages`, `temperature`, `max_tokens`, `top_p`, `frequency_penalty`, `presence_penalty`, and `stream`.

## Q5: What is the difference between Chat Completions and Completions endpoints?
**A:** The Completions endpoint (`/v1/completions`) is the legacy endpoint that takes a single text prompt and returns text. The Chat Completions endpoint (`/v1/chat/completions`) is the modern replacement that uses a message-based interface with role annotations. Chat Completions supports all current GPT models and features (function calling, multi-turn, structured output). The legacy Completions endpoint is deprecated.

## Q6: What are the message roles in Chat Completions?
**A:** Four roles: `system` — sets behavior and context for the assistant; `user` — represents the end user's input; `assistant` — previous responses from the model (including tool calls); `tool` — results from function/tool calls. The order of messages matters for context. System messages are most influential for setting behavior.

## Q7: How do you structure a system message effectively?
**A:** System messages should be clear, specific, and structured. Best practices: define the persona (e.g., "You are a helpful coding assistant"), specify constraints (response format, length, tone), provide rules (e.g., "don't make up information"), include context, and use delimiters for clarity. The system message has a strong influence on model behavior.

## Q8: What parameters control the randomness of model outputs?
**A:** `temperature` (0–2) controls randomness — lower values (0.1–0.3) produce deterministic, focused outputs; higher values (0.8–1.5) produce more creative, diverse outputs. `top_p` (0–1, nucleus sampling) controls the cumulative probability threshold for token selection. Use `temperature` OR `top_p`, not both. `frequency_penalty` reduces repetition of frequent tokens; `presence_penalty` encourages new topics.

## Q9: What is `max_tokens` and how does it work?
**A:** `max_tokens` limits the maximum number of tokens the model can generate in a single response. It controls output length and costs. Setting it too low may truncate responses. The model stops generating when it reaches the limit or a stop sequence. Note: `max_tokens` includes both input and output tokens in some newer models; check model-specific docs.

## Q10: What are stop sequences?
**A:** Stop sequences are strings that cause the model to stop generating when encountered. Multiple stop sequences can be provided as an array. Common uses: stopping at newlines, specific delimiters, or end-of-response markers. The stop sequence itself is not included in the output. Useful for controlled generation and parsing structured outputs.

## Q11: What is streaming in the OpenAI API?
**A:** Streaming (`stream: true`) returns responses token-by-token as Server-Sent Events (SSE) instead of waiting for the full response. Each chunk contains a `choices[0].delta` with the incremental token. The final chunk has `finish_reason`. Streaming enables real-time display of model output, improving user experience for longer responses.

## Q12: How do you handle streaming responses in code?
**A:** Set `stream=True` in the request. Iterate over the response object. Each chunk contains `choices[0].delta.content` (for text) or `delta.tool_calls` (for function calls). Accumulate tokens for the full response. Handle `finish_reason` to detect completion. Example in Python: `for chunk in client.chat.completions.create(..., stream=True): print(chunk.choices[0].delta.content or "", end="")`.

## Q13: What is function calling (tool calling) in the OpenAI API?
**A:** Function calling allows the model to intelligently choose to call external functions. You define functions/tools with JSON Schema descriptions of their parameters. The model returns a `tool_calls` object instead of text when it decides a function should be called. Your code executes the function and sends the result back as a `tool` message. Available in GPT-4 and GPT-3.5 Turbo.

## Q14: How do you define a tool/function for the API?
**A:** Pass a `tools` array in the request. Each tool has: `type` ("function"), `function` object with: `name` (unique identifier), `description` (helps model decide when to use it), `parameters` (JSON Schema describing arguments). Example: `{"type": "function", "function": {"name": "get_weather", "description": "Get weather for a location", "parameters": {"type": "object", "properties": {"location": {"type": "string"}}}}}`.

## Q15: What is `tool_choice` parameter?
**A:** `tool_choice` controls when the model calls functions: "none" (never call), "auto" (model decides), or `{"type": "function", "function": {"name": "my_function"}}` (force a specific function). "auto" is the default. Forcing a function is useful for classification or structured extraction workflows.

## Q16: What is `parallel_tool_calls`?
**A:** `parallel_tool_calls` (default true) allows the model to call multiple functions in a single response when they are independent. This reduces latency and round trips. When multiple tool calls are returned, execute them concurrently and send all results back as tool messages.

## Q17: How does the model handle multi-turn function calling?
**A:** The pattern: 1) user message → 2) model responds with `tool_calls` → 3) your code executes the function(s) → 4) append `tool` messages with results (matching `tool_call_id`) → 5) model continues with text or another function call. This loop continues until the model produces `content` (final answer) or a stop condition.

## Q18: What is structured output / JSON mode?
**A:** JSON mode instructs the model to always output valid JSON. Set `response_format={"type": "json_object"}` or `response_format={"type": "json_schema", "json_schema": {...}}` (for structured outputs with schema enforcement). JSON schema mode constrains the model to output matching a specific schema, enabling reliable structured data extraction.

## Q19: What is `response_format` with JSON Schema?
**A:** Passing `response_format={"type": "json_schema", "json_schema": {"name": "schema_name", "schema": {"type": "object", "properties": {...}}}}` enforces the model output to strictly follow the provided JSON Schema. The model will always produce valid JSON matching the schema. This is more reliable than prompting for JSON and parsing afterward.

## Q20: What is the seed parameter?
**A:** The `seed` parameter enables deterministic outputs. When set to the same integer value across requests, the model will attempt to return the same response (with some caveats for different system load). Useful for reproducibility, testing, and caching. Works by seeding the random sampling process deterministically.

## Q21: What are logprobs in the API?
**A:** `logprobs` returns the log probabilities of each output token. Set `logprobs=True` with optional `top_logprobs=N` to get the top N most likely tokens and their probabilities at each position. Useful for: confidence scoring, output validation, analyzing model uncertainty, and building custom sampling strategies.

## Q22: What is the Embeddings API?
**A:** The Embeddings API (`/v1/embeddings`) converts text into vector representations (embeddings) — arrays of floating-point numbers capturing semantic meaning. Models: `text-embedding-3-small` (cost-effective), `text-embedding-3-large` (high quality). Use cases: semantic search, clustering, recommendation systems, RAG, and classification.

## Q23: What are the differences between text-embedding-3-small and text-embedding-3-large?
**A:** `text-embedding-3-large` produces 3072-dimension vectors with higher accuracy on benchmarks like MTEB. `text-embedding-3-small` produces 1536-dimension vectors, is 5x cheaper, and still performs well. Both support `dimensions` parameter to truncate vectors for faster comparisons. Newer models generally outperform older ones at lower dimensions.

## Q24: What is the `dimensions` parameter for embeddings?
**A:** The `dimensions` parameter (`text-embedding-3+`) allows shortening embeddings to fewer dimensions without losing proportionally as much performance. For example, reducing a 3072-dim vector to 256 dims retains more performance than using a natively 256-dim model. This enables faster vector comparisons and lower storage costs with manageable quality loss.

## Q25: What is the Images API (DALL-E)?
**A:** The Images API (`/v1/images/generations`) generates images from text descriptions using DALL-E 3 (or DALL-E 2). Parameters: `prompt`, `model` ("dall-e-3"), `n` (1), `quality` ("standard" or "hd"), `size` ("1024x1024", "1792x1024", "1024x1792"), `style` ("vivid" or "natural"). DALL-E 3 has improved prompt following, detail, and safety.

## Q26: How does image generation prompting differ from text prompting?
**A:** Image prompts should be descriptive about: subject, setting, lighting, composition, style (photorealistic, oil painting, 3D render), colors, mood, and perspective. DALL-E 3 excels at following complex prompts. Avoid negative prompting. Use "vivid" style for hyper-realistic, "natural" for less stylized. Longer prompts generally produce better results.

## Q27: What is the Vision API (GPT-4 Vision)?
**A:** GPT-4 Vision (GPT-4o) allows the model to process images. Images can be provided as URLs or base64-encoded data in user messages. The model can: describe images, extract text (OCR), analyze diagrams, read charts, identify objects, and reason about visual content. Supported formats: PNG, JPEG, GIF, WebP.

## Q28: How do you send images to the Chat Completions API?
**A:** Include an image_url in a user message: `{"role": "user", "content": [{"type": "text", "text": "Describe this image"}, {"type": "image_url", "image_url": {"url": "https://..."}}]}`. For local images, base64-encode and use `data:image/jpeg;base64,...`. Optional `detail` parameter: "low" (faster, cheaper), "high" (more detail), "auto" (default).

## Q29: What is the Whisper API?
**A:** Whisper API (`/v1/audio/transcriptions` or `/v1/audio/translations`) converts speech to text. Supports multiple languages. `transcriptions` transcribes in the original language; `translations` translates to English. Parameters: `file` (audio file), `model` ("whisper-1"), `language`, `response_format` ("json", "text", "srt", "vtt"), `temperature`.

## Q30: What is the TTS (Text-to-Speech) API?
**A:** The TTS API (`/v1/audio/speech`) converts text to spoken audio. Models: `tts-1` (lower latency, lower quality), `tts-1-hd` (higher quality, higher latency). Voices: alloy, echo, fable, onyx, nova, shimmer. Parameters: `model`, `input` (text), `voice`, `response_format` ("mp3", "opus", "aac", "flac"), `speed` (0.25–4.0).

## Q31: What is the Moderation API?
**A:** The Moderation API (`/v1/moderations`) checks content against OpenAI's content policy. It classifies text into categories: hate, harassment, self-harm, sexual, violence, and their subcategories. Returns category scores. Use to filter user inputs and model outputs for safety. Free to use. Latest model: `text-moderation-latest`.

## Q32: How do you handle rate limits in the OpenAI API?
**A:** Rate limits are per organization: RPM (requests per minute) and TPM (tokens per minute). Responses include headers: `x-ratelimit-remaining-requests`, `x-ratelimit-remaining-tokens`, `x-ratelimit-reset-*`. Handle `429` (Too Many Requests) with exponential backoff + jitter. Use the `max_retries` parameter or a retry library (tenacity). Consider request batching and queuing.

## Q33: What error codes does the OpenAI API return?
**A:** Common codes: 400 (Bad Request — invalid params), 401 (Authentication — invalid key), 403 (Permission denied), 404 (Not Found), 429 (Rate limit exceeded or quota exhausted), 500 (Server Error), 503 (Service Unavailable — overloaded). Always handle these gracefully with appropriate user feedback and retry logic.

## Q34: How does token counting work for API billing?
**A:** Billing is per token (roughly 0.75 words per token for English). Input tokens (prompt) and output tokens (completion) are charged separately at different rates. Use `tiktoken` library to count tokens locally. The API response includes `usage.prompt_tokens` and `usage.completion_tokens`. Costs vary by model (GPT-4 is more expensive than GPT-3.5).

## Q35: What is tiktoken?
**A:** `tiktoken` is OpenAI's tokenizer library for counting tokens in text. It uses BPE (Byte Pair Encoding). Use `tiktoken.encoding_for_model("gpt-4")` to get the correct encoder, then `len(encoder.encode(text))` to count tokens. Essential for managing context windows and estimating costs before API calls.

## Q36: What is the context window and why does it matter?
**A:** The context window is the maximum input + output tokens a model can handle in a single request. GPT-4 has 8K/32K/128K variants; GPT-4o has 128K. Exceeding the limit causes truncation or errors. Manage context by: trimming conversation history, summarizing old messages, using sliding windows, and prioritizing recent/relevant content.

## Q37: How do you implement conversation memory with the API?
**A:** Maintain a list of messages (user + assistant) and append to it with each turn. For long conversations: use a sliding window (keep last N turns), summarize old messages, or use retrieval-augmented approaches. The system message stays at position 0. Truncate from the oldest non-system messages when approaching token limits.

## Q38: What is the Assistants API?
**A:** The Assistants API (`/v1/assistants`) is a higher-level abstraction for building AI assistants. It manages: threads (conversation sessions), runs (execution of an assistant on a thread), message history, and tools (code interpreter, file search, function calling). Assistants have persistent state, instructions, and file attachments.

## Q39: What is a Thread in the Assistants API?
**A:** A Thread represents a conversation session between a user and an assistant. Messages are added to threads. The Thread manages context and history automatically. Creating a thread: `client.beta.threads.create()`. Messages are added with `client.beta.threads.messages.create()`. Runs execute the assistant on the thread.

## Q40: What is a Run in the Assistants API?
**A:** A Run is an execution of an Assistant on a Thread. When you create a run, the assistant processes the thread messages and generates responses (or calls tools). Run statuses: `queued`, `in_progress`, `requires_action` (needs function call results), `completed`, `failed`, `cancelled`, `expired`. Poll or use streaming to track progress.

## Q41: What tools does the Assistants API support?
**A:** Three built-in tools: `code_interpreter` (executes Python code in a sandbox, handles data analysis), `file_search` (RAG over uploaded files — handles chunking, embedding, retrieval), and `function_calling` (custom functions you define). Tools are specified when creating the assistant.

## Q42: How does the file_search tool work?
**A:** Upload files, attach to the assistant, enable file_search tool. The API automatically: chunks files, generates embeddings, builds a vector store, and retrieves relevant chunks at query time. Supports filtering by file/vector store. Handles most file types (PDF, DOCX, CSV, etc.). Uses `max_num_results` to control retrieval count.

## Q43: What is a Vector Store in the Assistants API?
**A:** A Vector Store is a managed search index for file chunks. Files are added to a vector store, which handles chunking, embedding, and indexing. Vector stores can be attached to assistants (for file_search) or to threads (for temporary context). Expiration policies auto-clean unused stores. Supports metadata filtering.

## Q44: How does the code_interpreter tool work?
**A:** The code_interpreter tool allows the assistant to write and execute Python code in a sandboxed environment. It can: analyze data, create visualizations (matplotlib), process files, and perform computations. Results include text output and file references (images, CSVs). The environment has common libraries (numpy, pandas, matplotlib). Execution has time limits.

## Q45: What are the differences between Chat Completions and Assistants API?
**A:** Chat Completions is lower-level — you manage messages, context, and tool orchestration yourself. Assistants API is higher-level — it manages threads, runs, context window, and tool execution for you. Assistants API is better for complex assistants with state; Chat Completions gives more control for simpler or custom orchestration.

## Q46: What is the Batch API?
**A:** The Batch API (`/v1/chat/completions` with `batch`) allows sending up to 50,000 requests (or 100M tokens) as a batch for 50% cost reduction. Results are returned within 24 hours (usually ~3 hours). Batch jobs submit a file of requests, processing happens asynchronously, and results are downloadable. Good for offline evaluation, data processing, backfilling.

## Q47: What is the fine-tuning API?
**A:** Fine-tuning creates custom models by training on your dataset. Prepare a training file of example conversations (ChatML format). Upload via Files API, create a fine-tuning job (`/v1/fine_tuning/jobs`). The resulting model can be used like any other model via the Chat Completions API. Benefits: improved performance on specific tasks, reduced prompt length, lower latency.

## Q48: What data format is required for fine-tuning?
**A:** Training data is a JSONL file where each line is a conversation in ChatML format: `{"messages": [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]}`. For function calling fine-tuning, include `tool_calls` and `tool_call_id` in messages. Minimum ~50-100 high-quality examples recommended.

## Q49: What hyperparameters can be configured for fine-tuning?
**A:** Key hyperparameters: `n_epochs` (number of training epochs — default auto-calculated), `learning_rate_multiplier`, `batch_size`. The API uses default values that work well for most cases. You can also configure `validation_file` for evaluation, `suffix` for model name, and `seed` for reproducibility.

## Q50: How does fine-tuning compare to prompt engineering and RAG?
**A:** Prompt engineering: no training, works with any model, easy to iterate but limited by context. RAG: adds external knowledge retrieval, no training required, good for factual Q&A. Fine-tuning: trains the model on examples, best for learning style/format/behavior patterns, requires data collection. Often used together: RAG for knowledge + fine-tuning for style.

## Q51: What is prompt injection and how do you prevent it?
**A:** Prompt injection is an attack where user input overrides the system prompt, causing the model to ignore instructions. Prevention: validate and sanitize user input, use delimiters, place user input after instructions, use the moderation API, implement output validation, restrict tool access, and use the most recent models with better instruction following.

## Q52: How do you handle PII (Personally Identifiable Information) with the API?
**A:** Options: use the Moderation API to detect sensitive content, implement client-side PII detection/redaction before sending to the API, use data retention policies (`retention` header), avoid sending PII in prompts when possible. The API has SOC 2 compliance and data privacy options (no training on API data by default for API customers).

## Q53: What data privacy guarantees does OpenAI offer?
**A:** For API customers: data is not used for training by default (since March 2023). Data is retained for 30 days for abuse monitoring, then deleted. Zero Data Retention (ZDR) available for eligible customers. API traffic is encrypted in transit (TLS) and at rest. SOC 2 Type 2 certified. ChatGPT and other consumer products have different policies.

## Q54: How do you handle model deprecation and versioning?
**A:** Models have deprecation timelines (usually 3-6 months after replacement). Monitor OpenAI status page and emails. Use model aliases (e.g., `gpt-4o` instead of specific date-stamped versions) to auto-upgrade. Test against new models before cutoff dates. Pin specific versions (`gpt-4o-2024-08-06`) in production after validation.

## Q55: What is the difference between `gpt-4`, `gpt-4-turbo`, and `gpt-4o`?
**A:** `gpt-4` (8K/32K context) — original, most capable, slower, more expensive. `gpt-4-turbo` (128K context) — updated knowledge cutoff, cheaper, faster, supports vision and function calling. `gpt-4o` (128K context) — "omni" model, multimodal (text+vision+audio), fastest, most cost-effective, best performance for most tasks. `gpt-4o-mini` — smaller, cheaper, faster version.

## Q56: How do you choose between GPT-4o and GPT-4o-mini?
**A:** Use GPT-4o for: complex reasoning, nuanced tasks, vision processing, high-quality output requirements. Use GPT-4o-mini for: high-volume applications, simple tasks, classification, extraction, cost-sensitive workloads, where slightly lower quality is acceptable. GPT-4o-mini costs ~20x less than GPT-4o while handling most routine tasks well.

## Q57: What is the maximum context length for GPT-4o?
**A:** GPT-4o supports up to 128,000 tokens of context (about 96,000 words). This allows processing entire books, long documents, or extensive conversation histories. However, performance can degrade on information in the middle of very long contexts — consider recency bias and use retrieval for precise information.

## Q58: How do you implement a RAG system using the OpenAI API?
**A:** 1) Chunk documents → 2) Generate embeddings via Embeddings API → 3) Store in vector DB (Pinecone, Weaviate, etc.) → 4) On query, embed the question → 5) Retrieve top-k similar chunks → 6) Format chunks as context in system/user message → 7) Send to Chat Completions with the user question → 8) Generate answer grounded in retrieved context.

## Q59: What is the cost of different OpenAI API models?
**A:** Costs vary by model and change over time. GPT-4o: ~$5/1M input tokens, ~$15/1M output tokens. GPT-4o-mini: ~$0.15/1M input, ~$0.60/1M output. GPT-3.5 Turbo: ~$0.50/1M input, ~$1.50/1M output. Embeddings: ~$0.02/1M tokens. DALL-E 3: ~$0.04–$0.08 per image. Fine-tuning: training + usage costs. Always check current pricing.

## Q60: How do you estimate API costs before building?
**A:** Estimate average tokens per request (input + output), requests per day/month. Use formula: `monthly_cost = requests_per_month * (input_tokens * input_price + output_tokens * output_price) / 1_000_000`. Account for prompt size (system message, context, conversation history). Add buffer for testing, errors, and variable usage. Use cost tracking via Azure or third-party tools.

## Q61: What is the OpenAI Python client library?
**A:** `openai` Python package (`pip install openai`) provides a Pythonic interface to the API. Features: automatic retry, streaming helpers, async support, type hints, and error handling. Initialize with `client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))`. Methods: `client.chat.completions.create()`, `client.embeddings.create()`, etc.

## Q62: What is the OpenAI Node.js/TypeScript client library?
**A:** The `openai` npm package provides the JavaScript/TypeScript SDK. Similar to Python client: `import OpenAI from 'openai'; const client = new OpenAI();`. Supports ESM and CJS, streaming with `for await`, async/await, and full TypeScript typings. Methods mirror the REST API structure.

## Q63: How do you handle streaming with the Python client?
**A:** Set `stream=True` and iterate: `stream = client.chat.completions.create(model="gpt-4o", messages=[...], stream=True)`. Each chunk: `for chunk in stream: content = chunk.choices[0].delta.content or ""`. For tool calls in streaming: check `chunk.choices[0].delta.tool_calls`. For async: use `async for chunk in await client.chat.completions.create(...)`.

## Q64: What is the Files API?
**A:** The Files API (`/v1/files`) is used to upload files for various purposes: fine-tuning (training/validation data), assistants (file_search, code_interpreter), and batch processing. Upload with `purpose` parameter: "fine-tune", "assistants", "batch", "vision". File types: JSONL for fine-tuning, PDF/DOCX/CSV for assistants.

## Q65: What is the difference between Assistants file_search and vector stores?
**A:** Assistants file_search (legacy) uploaded files directly to the assistant. Vector stores (newer, recommended) are more flexible: files → vector store → attach to assistant or thread. Vector stores support: chunking strategies, metadata filtering, multiple file sources, expiration policies, and sharing across assistants.

## Q66: How do you handle network errors and timeouts?
**A:** Configure `timeout` (default 10 min for completions, lower for embeddings), `max_retries` (default 2), and `http_client` for custom session settings. Use libraries like tenacity for custom retry logic. Expected errors: `APITimeoutError`, `APIConnectionError`, `RateLimitError`, `APIStatusError`. Log errors for debugging.

## Q67: What are logprobs useful for in practice?
**A:** Logprobs enable: confidence scoring for classification tasks (reject low-confidence predictions), detecting out-of-distribution inputs (lower probabilities), analyzing model uncertainty, selective sampling (only use high-confidence responses), and debugging prompt quality (perplexity of expected tokens). Enterprise use: threshold-based output filtering.

## Q68: How do you use the API for classification tasks?
**A:** Three approaches: 1) Prompt-based: ask the model to classify with few-shot examples, 2) Embedding + classifier: use Embeddings API then train a classifier on the vectors, 3) Structured output: use response_format with schema to get structured classification. For high accuracy on specific categories, fine-tuning is best. For general categories, prompt-based works well.

## Q69: How do you use the API for summarization?
**A:** Provide the full text in the user message with a system instruction like "Summarize the following text in 3 bullet points." For long documents exceeding context window: 1) Chunk the document → 2) Summarize each chunk (map) → 3) Summarize the summaries (reduce). Use `map_reduce` pattern for arbitrary length documents.

## Q70: How do you use the API for extraction/structured data?
**A:** Best approach: use `response_format` with JSON Schema: define the schema for the data to extract (names, dates, amounts, etc.). The model outputs valid JSON matching the schema. For complex extractions: provide examples in the system message, use function calling for multi-step extraction, and validate outputs post-processing.

## Q71: What is the Azure OpenAI Service?
**A:** Azure OpenAI Service provides OpenAI models through Microsoft Azure's platform with: enterprise-grade security (Azure AD, managed identities), regional availability, compliance certifications, private networking (VNet), responsible AI content filtering, and SLA guarantees. Access via `https://{resource}.openai.azure.com`. Uses the same API but with different authentication.

## Q72: How does authentication differ between OpenAI and Azure OpenAI?
**A:** OpenAI: API key in Authorization header. Azure OpenAI: API key OR Azure AD token authentication. Azure AD supports role-based access control (RBAC), managed identities, and conditional access policies. Azure also requires: `api-version` parameter, resource name in URL, and deployment name instead of model name.

## Q73: What is the `user` parameter in the API?
**A:** The `user` parameter is a unique identifier for the end user, used by OpenAI for monitoring and abuse detection. It doesn't affect model behavior. Best practice: pass a hashed user ID to help OpenAI identify patterns across requests from the same user. Useful for rate limit management and debugging.

## Q74: How do you implement caching to reduce API costs?
**A:** Cache strategies: 1) Response cache — cache exact request → response pairs (using Redis, Memcached), keyed by (model, messages, temperature). 2) Semantic cache — cache similar queries using embeddings (retrieve if cosine similarity > threshold). 3) Tiered approach: try cache first, then cheaper model (GPT-4o-mini), then full model (GPT-4o) as fallback.

## Q75: What is semantic caching for LLM APIs?
**A:** Semantic caching caches responses based on meaning rather than exact text. On request: embed the query, compare against cached query embeddings. If a semantically similar query exists (cosine similarity > threshold like 0.92), return cached response. Reduces costs for similar questions, common patterns, and repeated queries in production.

## Q76: How do you evaluate model outputs?
**A:** Methods: 1) Human evaluation (raters score outputs on accuracy, helpfulness, safety), 2) LLM-as-judge (use a strong model like GPT-4o to evaluate outputs), 3) Automated metrics (ROUGE, BLEU for summarization, Exact Match for extraction), 4) Unit tests (assertions on output format, keywords), 5) A/B testing in production.

## Q77: What evaluation metrics are commonly used?
**A:** Task-specific metrics: accuracy (classification), F1 (extraction), ROUGE-L (summarization), BLEU (translation), Exact Match (QA). LLM-specific: faithfulness (does output match context?), relevance (is output on-topic?), coherence, helpfulness, safety score. Use OpenAI Evals framework or LangSmith for systematic evaluation.

## Q78: What is the OpenAI Evals framework?
**A:** OpenAI Evals is an open-source framework for evaluating LLM outputs. It provides: standard evaluation templates, dataset format, model-graded eval, and customization options. Run with `oaieval <eval> <model>`. Includes evals for: factual correctness, toxicity, JSON validity, and custom criteria.

## Q79: How do you deploy an OpenAI API application to production?
**A:** Steps: 1) Implement retry and error handling, 2) Add monitoring (latency, token usage, error rates), 3) Set up caching, 4) Implement rate limiting per user, 5) Add content moderation (input + output), 6) Use environment-specific API keys, 7) Logging for debugging, 8) Gradual rollout with model version pinning, 9) Cost tracking and alerts.

## Q80: What is prompt chaining?
**A:** Prompt chaining breaks a complex task into multiple API calls where each call's output feeds into the next. Example: 1) Generate outline, 2) Expand each section, 3) Polish final output. Benefits: better quality (each step has a focused task), easier debugging, lower cost (fail early), and ability to parallelize independent steps.

## Q81: What is the difference between prompt chaining and function calling?
**A:** Prompt chaining: multiple sequential API calls, each with its own prompt and purpose, orchestrated by your code. Function calling: a single API call where the model decides to call functions mid-response, with the loop managed by your code. Function calling is more dynamic; prompt chaining is more predictable and debuggable.

## Q82: How do you handle hallucination in model outputs?
**A:** Strategies: 1) Ground responses with RAG (provide relevant context in the prompt), 2) Use lower temperature (0.0–0.2), 3) Ask the model to cite sources, 4) Implement fact-checking (verify claims with tools), 5) Use structured output to constrain format, 6) Post-processing validation, 7) Tell the model to say "I don't know" instead of guessing.

## Q83: What is the `temperature` parameter and how does it work technically?
**A:** Temperature controls the probability distribution over tokens. Before sampling, logits are divided by temperature. Lower temperature (→0) makes high-probability tokens even more likely — deterministic, focused output. Higher temperature (→2) flattens the distribution, making low-probability tokens more likely — creative, diverse output. At temperature=1, no scaling.

## Q84: How do you handle JSON parsing from model outputs?
**A:** Options: 1) Use `response_format` with JSON Schema (most reliable — model outputs valid JSON), 2) Use `response_format={"type": "json_object"}` (valid JSON but no schema enforcement), 3) Prompt for JSON and parse with `json.loads()` with try/except for error handling, 4) Use function calling with a function that returns JSON.

## Q85: What is the GPT-4o system card?
**A:** The system card is a document detailing GPT-4o's capabilities, limitations, safety evaluations, and risk mitigations. It covers: model architecture, training data, performance benchmarks, safety testing results, potential failure modes, bias evaluations, and usage guidelines. Published as part of OpenAI's responsible deployment framework.

## Q86: How do you handle user input safety?
**A:** Multi-layered approach: 1) Input validation (length limits, format checks), 2) Moderation API check before sending to model, 3) System prompt reinforcing safety, 4) Output filtering (moderation API on output), 5) Rate limiting per user, 6) Content policy enforcement, 7) Human review for sensitive applications.

## Q87: What are logit biases?
**A:** Logit biases modify the probability of specific tokens appearing in the output. Accepts a dictionary mapping token IDs to bias values (-100 to 100). Positive values increase likelihood; negative values decrease. Use cases: preventing specific words, encouraging certain formats, guiding topic focus. Example: `logit_bias={2435: -100}` to strongly discourage a token.

## Q88: How do you use logit biases to prevent specific words?
**A:** Tokenize the word(s) you want to block, get their token IDs (using tiktoken), and pass `logit_bias={token_id: -100}`. Setting bias to -100 nearly eliminates the token from being chosen. Note: words may be multiple tokens, and blocking one token may produce unexpected alternatives. Test thoroughly as logit biases can affect output quality.

## Q89: What is the difference between `frequency_penalty` and `presence_penalty`?
**A:** `frequency_penalty` (0–2) reduces the likelihood of tokens that have already appeared frequently in the text — penalizes repetition proportional to frequency. `presence_penalty` (0–2) penalizes ALL tokens that have appeared at least once, regardless of frequency — encourages introducing new topics. Both reduce repetition but work differently.

## Q90: How do you implement tool calling effectively?
**A:** Best practices: 1) Write clear, specific tool descriptions (helps model decide when to use), 2) Use descriptive parameter names with good JSON Schema descriptions, 3) Handle the `requires_action` state properly, 4) Return meaningful error messages as tool results, 5) Set tool_choice for deterministic routing, 6) Handle parallel tool calls.

## Q91: What is prompt caching in the API?
**A:** Prompt caching (available for newer models) automatically caches repeated input prefix tokens across API calls, reducing latency and costs. Useful when many requests share a common prefix (system message, few-shot examples, large context). Cache hits have lower per-token cost. Model checks for cacheable tokens automatically.

## Q92: How do you compare LLM outputs from different models?
**A:** Methods: 1) Side-by-side human evaluation (A/B testing), 2) LLM-as-judge (use one model to evaluate another's outputs), 3) Task-specific benchmarks (e.g., HumanEval for code, MMLU for knowledge), 4) Statistical tests on evaluation scores, 5) Cost-performance analysis (quality vs. price vs. latency tradeoffs).

## Q93: What is the `store` and `metadata` parameters?
**A:** `store` (boolean) when true, stores the conversation for later analysis in the OpenAI dashboard. `metadata` allows tagging requests with custom key-value pairs (e.g., `{"user_id": "abc", "env": "prod"}`) for filtering and analysis in dashboards and logs. Useful for monitoring and debugging production usage.

## Q94: How do you handle long document processing with GPT-4o's 128K context?
**A:** Strategies: 1) Direct: fit entire document in context (if under limit), 2) Sliding window: process overlapping chunks, summarize each, combine, 3) Hierarchical: chunk → summarize each → summarize summaries, 4) Map-reduce: process chunks in parallel, reduce results. With 128K context, many documents fit entirely, but retrieval approaches may still be better for precise Q&A.

## Q95: What are the limitations of the OpenAI API?
**A:** Limitations: knowledge cutoff (models don't know events after training date), hallucination (may produce false info), context window limits, no inherent memory (stateless per request), cost at scale, latency for complex tasks, bias from training data, sensitivity to prompt phrasing, and lack of true reasoning.

## Q96: How do you monitor and debug API calls?
**A:** Use: OpenAI dashboard (usage metrics, latency, error rates), structured logging (request ID, model, tokens, latency), custom metrics (cost per user, feature, endpoint), LangSmith or similar for LLM observability, token tracking, error alerting (429 spikes, error rate thresholds), and request/response logging with PII redaction.

## Q97: What are OpenAI usage tiers?
**A:** Usage tiers (1–5) are determined by account age and cumulative spend. Higher tiers unlock: higher rate limits, access to newer models, priority support, and higher batch sizes. Tier progression: Tier 1 (after $5 spend), Tier 2 ($50), Tier 3 ($100), Tier 4 ($250), Tier 5 ($1000+). Each tier increases RPM and TPM limits.

## Q98: How do you handle multi-language support?
**A:** GPT models natively support 100+ languages. For multi-language: set system message in the target language, provide examples in target language, use language detection before routing to specialized prompts. Whisper API handles 99+ languages for STT. For translation: use Whisper translations endpoint or instruct GPT to translate.

## Q99: How do you implement a feedback loop to improve performance?
**A:** 1) Collect user feedback (thumbs up/down, ratings), 2) Log all interactions (input, output, metadata), 3) Analyze failure patterns (low ratings, high latency, retry counts), 4) Build evaluation datasets from real data, 5) A/B test prompt/system message changes, 6) Use fine-tuning to improve on common failure cases, 7) Monitor improvements over time.

## Q100: What are the emerging trends in the OpenAI API ecosystem?
**A:** Key trends: 1) Agentic workflows (Assistants API, function calling loops), 2) Multi-modal applications (text + vision + audio), 3) Real-time API (WebSocket-based streaming), 4) Model distillation (smaller models trained on larger model outputs), 5) Increased context windows (1M+ tokens), 6) Lower costs and faster inference, 7) Improved structured output reliability, 8) Edge deployment of smaller models via ONNX/GGUF.
