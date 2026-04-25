# Consolidated Notes: Transformers, Embeddings & Modern NLP

---

## 1. Evolution of NLP Models

### Early Models

- **RNN → LSTM → GRU**
- Designed for sequence data but suffered from **vanishing gradients**, slow training, and poor long-context handling

### Encoder–Decoder with Attention (2015–2016)

- Introduced **attention** to improve sequence-to-sequence tasks like machine translation

### Transformer (2017 – "Attention Is All You Need")

- Removed recurrence entirely
- Enabled **parallel processing**, better scalability, and strong long-context modeling

### Pretrained Language Models

| Model / Family | Type | Key Feature |
|---|---|---|
| **ULMFiT** | Transfer learning | Pioneered transfer learning for NLP |
| **BERT** (2018, Google) | Encoder-only | Masked Language Modeling (MLM), bidirectional |
| **GPT family** | Decoder-only | Autoregressive next-token prediction |
| **Modern LLMs** | Various | GPT, LLaMA, Mistral, Qwen, Gemini, Claude, DeepSeek |

---

## 2. Transformer Architecture (Core Understanding)

### Encoder

1. Input Embedding
2. Positional Encoding
3. Multi-Head Self-Attention
4. Add & Layer Normalization
5. Feed-Forward Network
6. Residual Connections
7. **Repeated N times**

### Decoder

1. Shifted-right output embeddings
2. Positional Encoding
3. Masked Multi-Head Self-Attention
4. Cross Attention (Encoder–Decoder interaction, except GPT)
5. Feed-Forward Network
6. Linear + Softmax → Output probabilities

### Key Properties

- **Parallel processing** (unlike RNNs)
- Handles **long-term dependencies** well
- **Context-aware** representations

---

## 3. Self-Attention Explained

- Self-attention allows each word to look at **all other words** in the sentence to understand meaning
- Uses **Query (Q)**, **Key (K)**, **Value (V)** matrices
- Produces **dynamic embeddings**:
  - Same word → different vectors in different contexts
  - Example: *bank* (money vs river)
- Transformer embeddings are **context-dependent**, unlike Word2Vec

---

## 4. Embeddings: From Encoding to Semantics

| Technique | Characteristics |
|---|---|
| **One-hot / TF-IDF** | Sparse, frequency-based, no semantics |
| **Word2Vec / GloVe** | Dense, static embeddings |
| **Sentence Transformers** | Context-aware embeddings |
| **Transformer embeddings** (OpenAI, Gemini) | Deep contextual semantics |

> **Key Takeaway:** Encoding captures frequency, embeddings capture meaning, transformers capture context.

---

## 5. Types of Data for Embeddings

- Text (word, paragraph, document)
- Image
- Audio
- Video
- Modern SOTA embedding models support **multi-modal** inputs

---

## 6. How to Select the Best Embedding Model

### Embedding Quality (Most Important)

- **Benchmarks:**
  - MTEB leaderboard
  - BEIR benchmark

### Dimensionality

| Dimension | Trade-off |
|---|---|
| **384** | Lightweight |
| **768** | Balanced |
| **1536** | High quality, higher cost |

### Cost

| Source | Quality | Cost |
|---|---|---|
| **Closed source** (OpenAI, Gemini) | High quality | API cost |
| **Open source** (Sentence Transformers) | Free | Infrastructure cost |

### Domain Suitability

- General: `all-MiniLM`, OpenAI embeddings, Gemini embeddings

---

## 7. Similarity Search Techniques (Used in RAG)

- Dot Product
- **Cosine Similarity** ✅ (most commonly used)
- Euclidean Distance

---

## 8. RAG (Retrieval-Augmented Generation)

### Combines

- Embeddings
- Similarity search
- LLMs

### Workflow

1. Convert data to embeddings
2. Store in vector database
3. Retrieve relevant chunks
4. Inject into prompt

> Improves **factual accuracy** and **grounding**.

---

## 9. Pretraining vs Fine-Tuning

| Aspect | Pretraining | Fine-Tuning (FT) |
|---|---|---|
| **Data** | Large-scale unlabeled data | Task-specific data |
| **Objective** | Next-token or masked token prediction | Task-specific adaptation |
| **GPT** | Autoregressive | — |
| **BERT** | Masked Language Modeling (MLM) | — |

---

## 10. RNN vs Transformer (High-Level Comparison)

| Aspect | RNN / LSTM | Transformer |
|---|---|---|
| **Processing** | Sequential | Parallel |
| **Speed** | Slow | Fast |
| **Long context** | Weak | Strong |
| **Architecture** | Gated memory | Self-attention |
| **Scalability** | Limited | Highly scalable |

---

## 11. Key Resources Mentioned

- Sentence Transformers (HuggingFace): https://huggingface.co/sentence-transformers

- Sentence Transformer Models: https://huggingface.co/models?library=sentence-transformers&sort=downloads

- OpenAI API: https://developers.openai.com/api/docs/quickstart

- Gemini API Key: https://aistudio.google.com/api-keys

- HuggingFace Tokens: https://huggingface.co/settings/tokens

- MeshAPI: https://meshapi.ai/

- **Original Papers:**
  - Encoder–Decoder: https://arxiv.org/pdf/1409.3215

  - Attention with Encoder–Decoder: https://arxiv.org/pdf/1409.0473

  - ULMFiT: https://arxiv.org/pdf/1801.06146

  - Transformer ("Attention Is All You Need"): https://arxiv.org/pdf/1706.03762

- Jay Alammar's Illustrated Transformer Blog: https://jalammar.github.io/illustrated-transformer/
