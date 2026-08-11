# 01 — NLP Sentiment Pipeline

## Purpose
Turn headlines into a structured sentiment signal, self-hosted, transparent,
and auditable — without sending data to third-party black-box APIs.

## Approach (dependency-minimized)
1. **Lexicon-based scoring** (start): a curated financial word list with
   positive/negative weights. Fast, interpretable, no model training.
2. **Manual rules** for negations ("not", "misses"), intensifiers, and domain
   phrases ("beats estimates", "downgrade", "recall").
3. **Optional learned model** (later, behind an interface): a small classifier
   trained on labeled headlines; must be validated and versioned like any model.

## Pipeline steps
1. Text cleaning: lowercase, strip URLs, expand common contractions.
2. Tokenize (simple whitespace/punctuation for MVP).
3. Score: sum weights of matched terms, apply negation window.
4. Tag symbols (dictionary + capitalization heuristics).
5. Aggregate: per symbol per minute/hour sentiment = mean/sum of event scores.

## Pseudo-code: lexicon scorer
```
def score(text):
    s = 0
    tokens = tokenize(text)
    neg = False
    for tok in tokens:
        if tok in NEGATIONS: neg = True; continue
        w = LEXICON.get(tok, 0)
        if w and neg: w = -w; neg = False
        s += w
    return s
```

## Validation
- Build a small labeled test set; track precision/recall against a baseline
  (random / constant). Reject the component if it adds no measured value.
- Sanity-check aggregate sentiment against price moves post-event (directional
  correlation) and report it honestly.

## Usage guidance
- Sentiment is a *context feature*: combine with price reaction, never alone.
- Prices already reflect most public news; edge is in *unexpected* deviation.

## Rules
- The sentiment engine is deterministic (same text → same score) and logged.
- Never auto-execute on sentiment alone; it is one weak signal among many.
- Publish sentiment as a feature with its score, count, and window.
