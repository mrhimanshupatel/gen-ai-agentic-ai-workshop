# Transformer Architecture & Attention Mechanisms

## Session Overview (Based on Handwritten Class Notes – 25 April, 2026)

This document consolidates **all concepts covered in the handwritten lecture notes** from the PDF. It explains Transformers from motivation to architecture, math, and design choices.

---

## 1. Why Transformers?

Traditional sequence models such as **RNNs** and **LSTMs** process tokens sequentially, which leads to:
- Slow training (no parallelism)
- Difficulty learning long-range dependencies

**Transformers solve this by**:
- Removing recurrence
- Processing tokens in parallel
- Using attention to capture relationships between all tokens

---

## 2. High-Level Transformer Pipeline

Text → Tokenization → Embedding Layer → Positional Encoding → Self-Attention → Feed Forward Network → Output

Repeated across **N encoder blocks** and **N decoder blocks**.

---

## 3. Tokenization

- Input text is broken into tokens (words/subwords)
- Losing order during tokenization is a key problem transformers must solve

---

## 4. Embedding Layer

- Converts tokens into dense vectors
- Original Transformer uses **512-dimensional embeddings**
- Similar to Word2Vec, but **not pretrained by default**
- Learns embeddings during training

---

## 5. Positional Encoding

### Why needed?
Transformers process tokens in parallel → **sequence order is lost**.

### Solution
- Add positional encoding to embeddings
- Preserves word order information

Example:
- "You are here" ≠ "Here you are"

---

## 6. Self-Attention (Core Concept)

Self-attention allows each word to:
- Look at all other words
- Decide how much importance (weight) to give them

### Ambiguity Example
Word: **bank**
- river bank
- money bank

Context determines meaning via attention weights.

---

## 7. Query, Key, Value (Q, K, V)

Each token generates:
- **Query (Q):** What am I searching for?
- **Key (K):** What do I contain?
- **Value (V):** What information do I provide?

### Attention Formula

Attention(Q, K, V) = softmax(QKᵀ / √dk) × V

---

## 8. Multi-Head Attention

- Multiple attention heads operate in parallel
- Each head learns different relationships:
  - Syntax
  - Semantics
  - Long vs short context

Heads are concatenated before passing forward.

---

## 9. Encoder Blocks

Original Transformer uses:
- 6 encoder layers
- 6 decoder layers

### Important
- 6 is **not fixed**
- It is a **hyperparameter**

### Why stack encoders?
- Deeper understanding
- Hierarchical representation

Typical progression:
- Layer 1 → Word relations
- Layer 3 → Phrase meaning
- Layer 6 → Sentence meaning
- Deeper layers → Contextual understanding

Modern examples:
- BERT Base → 12 layers
- BERT Large → 24 layers
- GPT → 12–96+ layers

---

## 10. Residual Connections (Skip Connections)

### Problem in deep networks
- Vanishing gradients
- Information loss
- Unstable training

### Solution
Add input directly to output:

Output = x + F(x)

### Benefits
- Better gradient flow
- Faster training
- Preserves original information
- Enables deep stacking

Inspired by **ResNet (CNNs)**.

---

## 11. Layer Normalization

Applied after:
- Self-Attention
- Feed Forward Network

Purpose:
- Stabilizes training
- Prevents exploding/vanishing values

Typically shown as **Add & Norm**.

---

## 12. Feed Forward Neural Network (FFN)

### Why needed?
- Attention captures token relationships
- FFN adds non-linearity per token

### Architecture
512 → 2048 → 512

### Formula
FFN(x) = ReLU(xW₁ + b₁)W₂ + b₂

Adds complexity and expressiveness.

---

## 13. Encoder vs Decoder

### Encoder
- Self-attention only
- Builds contextual embeddings

### Decoder
- Masked self-attention (no future tokens)
- Cross-attention with encoder outputs
- Used for text generation

---

## 14. Output Layer

- Linear transformation
- Softmax
- Produces probability distribution over vocabulary

---

## 15. Why Transformers over RNNs?

- Parallel processing
- Better handling of long context
- Faster training
- Scales to very deep models

---

## 16. Interview & Recap Topics

- Why positional encoding?
- Why residual connections?
- Why FFN is required?
- Why multiple encoder layers?
- Encoder vs Decoder
- Attention vs RNNs

---

## Summary

This session covered **conceptual, mathematical, and architectural foundations of Transformers**, explaining why they power modern models such as **BERT, GPT, and LLaMA**.
