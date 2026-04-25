# Workshop Concepts - Global Summary

> **Auto-generated index of all `*CONCEPTS*.md` files across workshop folders.**

---

## 03_29_2026

### ENCODING_EMBEDDING_CONCEPTS.md
Minimal environment check notebook. Verifies the Jupyter kernel is active and Python execution works before starting NLP encoding/embedding experiments. Covers the "smoke test" pattern commonly used as the first cell in training notebooks.

### EXAMPLE_COMPARISON_CONCEPTS.md
Interactive experimentation with reusable utility functions from `text_utils.py` (`clean_text`, `count_words`, `get_text_stats`). Demonstrates the module + notebook pattern: keep logic in `.py` files for reuse, use `.ipynb` for exploration. Covers basic text normalization, word counting, and descriptive text statistics.

---

## 04_04_2026

### ENCODING_EMBEDDING_CONCEPTS.md
Four notebook variants covering classical text-to-number encoding techniques using scikit-learn:
- **One-Hot Encoding** (`OneHotEncoder`): binary word vectors, `sparse_output=False` parameter
- **Bag of Words** (`CountVectorizer`): document-level word counts, `fit`/`transform` workflow, out-of-vocabulary handling
- **TF-IDF** (`TfidfVectorizer`): frequency weighted by importance, down-weights common words

Includes comparison table (OHE vs BoW vs TF-IDF), key scikit-learn API patterns (`fit`/`transform`/`fit_transform`), and practical takeaways on when each method is appropriate.

---

## 04_05_2026

### ENCODING_AND_TEXT_FEATURE_ENGINEERING_CONCEPTS.md
Three notebooks progressing from basic encoding to a full real-world pipeline:
- **encoding.ipynb**: One-Hot, BoW, TF-IDF walkthrough with sparse matrix exploration
- **text_feature_engineering.ipynb**: End-to-end assignment on 110 product reviews — text preprocessing (`TextPreprocessor` class with tokenization, stopword removal, lemmatization), vocabulary analysis, sparse matrix analysis (>90% sparsity), sentiment classification (Logistic Regression + Naive Bayes), feature importance visualization
- **classical_word_embedding.ipynb**: Empty placeholder

Key results: TF-IDF + Logistic Regression performed best. Real-world Q&A on BoW vs TF-IDF trade-offs, TF-IDF limitations, and why classical methods fail at semantic meaning.

---

## 04_11_2026

### CLASSICAL_WORD_EMBEDDING_CONCEPTS.md
Using a pre-trained Word2Vec model (`word2vec-google-news-300`, 300-d, Skip-gram) via gensim:
- Word vector retrieval and similarity (`most_similar`, `similarity`)
- Odd-one-out detection (`doesnt_match`)
- Word analogy via vector arithmetic (king - man + woman ≈ queen)
- **Average Word2Vec**: sentence-level embedding by averaging word vectors

Highlights that Word2Vec is case-sensitive, cannot handle multi-word inputs directly, and that Average Word2Vec is an older technique superseded by Transformer-based models.

---

## 04_12_2026

### CUSTOM_WORD2VEC_CONCEPTS.md
Training a custom Word2Vec model from scratch on local text files using gensim + nltk:
- Data pipeline: raw text files → `sent_tokenize` → `simple_preprocess` → `List[List[str]]`
- Architectures: CBOW (`sg=0`) vs Skip-gram (`sg=1`)
- Hyperparameters: `window=10`, `min_count=1`, `vector_size=150`, `epochs=10`
- Embedding inspection: retrieve vectors, `most_similar`, `doesnt_match`, `similarity`
- Vocabulary and corpus count analysis

Practical notes: small corpus limits quality, low `min_count` may add noise, model can be saved via `model.save()` for reuse.

---

## 04_25_2026

### TRANSFORMER_ARCHITECTURE_CONCEPTS_04_25_2026.md
Deep dive into the **Transformer architecture** from motivation to math, based on handwritten class notes. Covers the full pipeline: tokenization → embedding → positional encoding → self-attention (Q, K, V) → multi-head attention → feed-forward network → output (softmax). Explains why Transformers replace RNNs (parallelism, long-range context), the attention formula $\text{softmax}(QK^T / \sqrt{d_k}) \times V$, residual connections (skip connections inspired by ResNet), layer normalization, and FFN non-linearity.

Key architectural details: original Transformer uses 6 encoder + 6 decoder layers (hyperparameter — BERT uses 12/24, GPT uses 12–96+), 512-d embeddings expanded to 2048 in FFN. Covers encoder vs decoder differences (masked self-attention, cross-attention), stacking for hierarchical representation (word → phrase → sentence → context), and interview-ready recap topics.

---

## Learning Progression

```
03_29 → Environment setup & text utility patterns
04_04 → Classical encoding: One-Hot, BoW, TF-IDF
04_05 → Full text feature engineering pipeline + sentiment classification
04_11 → Pre-trained Word2Vec (Google News) + Average Word2Vec
04_12 → Custom Word2Vec training on domain-specific data
04_25 → Transformer architecture: attention, Q/K/V, encoder-decoder, residual connections
  ↓
Next  → SOTA embeddings (Sentence Transformers, OpenAI, Gemini) & RAG pipelines
```
