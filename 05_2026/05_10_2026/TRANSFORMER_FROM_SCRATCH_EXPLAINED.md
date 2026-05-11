# Transformer from Scratch — German → English Translation

A complete encoder-decoder Transformer built from scratch in PyTorch for neural machine translation (German → English) using the Multi30k dataset.

---

## Overview

This notebook implements the original Transformer architecture ("Attention Is All You Need", Vaswani et al. 2017) without relying on `nn.Transformer`. Every component — positional encoding, multi-head attention, encoder/decoder layers — is coded manually for educational clarity.

---

## 1. Reproducibility & Device Setup

```python
SEED = 123
random.seed(SEED)
torch.manual_seed(SEED)
torch.backends.cudnn.deterministic = True
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
```

- Sets a fixed random seed across Python and PyTorch for reproducible results.
- Selects GPU if available, otherwise falls back to CPU.

---

## 2. Tokenization (spaCy)

```python
spacy_de = load_spacy_model("de_core_news_sm")
spacy_en = load_spacy_model("en_core_web_sm")
```

- Uses spaCy's language-specific tokenizers for German (`de_core_news_sm`) and English (`en_core_web_sm`).
- Falls back to simple whitespace splitting if spaCy models aren't installed.
- All tokens are lowercased.

---

## 3. Dataset — Multi30k

```python
class Multi30kDataset(Dataset):
```

- Loads parallel German/English sentence pairs from gzip-compressed files.
- Each `__getitem__` returns a dict with `"src"` (German tokens) and `"trg"` (English tokens).
- Source/target transforms (tokenization functions) are applied on the fly.

### Data Download

The notebook auto-downloads the Multi30k dataset from the official GitHub repository into a local `data/` directory using `urllib.request`.

---

## 4. Vocabulary Construction

```python
SPECIAL_TOKENS = ["<pad>", "<sos>", "<eos>", "<unk>"]
```

| Token | Index | Purpose |
|-------|-------|---------|
| `<pad>` | 0 | Padding shorter sequences in a batch |
| `<sos>` | 1 | Start-of-sequence marker |
| `<eos>` | 2 | End-of-sequence marker |
| `<unk>` | 3 | Unknown/out-of-vocabulary words |

- `create_vocab()` counts token frequencies across all training sentences and assigns an integer index to each token that meets `min_freq`.
- Separate vocabularies are built for source (German) and target (English).

---

## 5. Transformer Components

### 5.1 Positional Encoding

```python
class PositionalEncoding(nn.Module):
```

Since Transformers have no recurrence or convolution, positional information is injected via sinusoidal functions:

$$PE_{(pos, 2i)} = \sin\left(\frac{pos}{10000^{2i/d_{model}}}\right)$$

$$PE_{(pos, 2i+1)} = \cos\left(\frac{pos}{10000^{2i/d_{model}}}\right)$$

- Registered as a non-learnable buffer (`register_buffer`).
- Shape: `[1, max_len, d_model]` — broadcasts over the batch dimension.

### 5.2 Multi-Head Attention

```python
class MultiHeadAttention(nn.Module):
```

Core mechanism of the Transformer:

1. **Linear projections**: Input Q, K, V are projected via learned weight matrices $W_Q$, $W_K$, $W_V$.
2. **Split into heads**: Reshaped to `[batch, num_heads, seq_len, d_k]` where $d_k = d_{model} / h$.
3. **Scaled dot-product attention**:

$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$

4. **Mask application**: Padding mask and/or causal mask are applied before softmax by setting masked positions to $-10^9$.
5. **Concatenate & project**: Heads are concatenated and passed through $W_O$.

### 5.3 Position-wise Feed-Forward Network

```python
class PositionwiseFeedForward(nn.Module):
```

A two-layer MLP applied independently to each position:

$$FFN(x) = \text{ReLU}(xW_1 + b_1)W_2 + b_2$$

- Inner dimension (`d_ff`) is typically 2–4× larger than `d_model`.

### 5.4 Encoder Layer

Each encoder layer consists of:
1. Multi-head **self-attention** (with source padding mask)
2. Feed-forward network
3. Residual connections + LayerNorm after each sub-layer

### 5.5 Decoder Layer

Each decoder layer consists of:
1. **Masked self-attention** (causal mask prevents attending to future tokens)
2. **Cross-attention** over encoder output (uses source padding mask)
3. Feed-forward network
4. Residual connections + LayerNorm after each sub-layer

### 5.6 Full Transformer Model

```python
class Transformer(nn.Module):
```

**Encoder path:**
- Source embedding × $\sqrt{d_{model}}$ → Positional encoding → Dropout → N encoder layers

**Decoder path:**
- Target embedding × $\sqrt{d_{model}}$ → Positional encoding → Dropout → N decoder layers → Linear projection to vocab size

**Masks:**
- `make_src_mask`: `[B, 1, 1, src_len]` — masks out `<pad>` positions in source.
- `make_trg_mask`: `[B, 1, trg_len, trg_len]` — combines padding mask with a lower-triangular causal mask.

---

## 6. DataLoader & Training Utilities

### Collate Function

```python
def make_collate_fn(src_vocab, trg_vocab):
```

- Converts token lists to integer IDs (prepends `<sos>`, appends `<eos>`).
- Pads sequences in a batch to equal length using `pad_sequence`.

### Training Loop (`train_epoch`)

1. Teacher forcing: decoder receives `trg[:, :-1]` (everything except last token).
2. Loss computed against `trg[:, 1:]` (everything except `<sos>`).
3. Gradient clipping (`clip_grad_norm_`) prevents exploding gradients.

### Evaluation Loop (`evaluate`)

Same as training but with `torch.no_grad()` and no parameter updates.

---

## 7. Inference / Translation

```python
def translate_sentence(sentence, src_vocab, trg_vocab, model, max_len=50):
```

**Autoregressive decoding** (greedy search):

1. Tokenize the German input sentence.
2. Encode it once through the encoder.
3. Start with `<sos>` token.
4. At each step:
   - Pass all generated tokens so far through the decoder.
   - Take the argmax of the last position's logits as the predicted token.
   - Append to the output sequence.
5. Stop when `<eos>` is predicted or `max_len` is reached.

---

## 8. Main Training Script

### Hyperparameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| `D_MODEL` | 256 | Embedding / hidden dimension |
| `NUM_HEADS` | 8 | Attention heads ($d_k = 32$) |
| `NUM_LAYERS` | 3 | Encoder & decoder depth |
| `D_FF` | 512 | Feed-forward inner dimension |
| `MAX_SEQ_LENGTH` | 100 | Max positional encoding length |
| `DROPOUT` | 0.1 | Dropout rate |
| `BATCH_SIZE` | 32 | Samples per batch |
| `N_EPOCHS` | 1 | Training epochs (demo) |
| `CLIP` | 1.0 | Gradient clipping threshold |
| `lr` | 1e-4 | Adam learning rate |

### Training Flow

1. Build datasets and vocabularies.
2. Initialize model, Adam optimizer (β₁=0.9, β₂=0.98), and CrossEntropyLoss (ignoring `<pad>` index).
3. Train for `N_EPOCHS`, saving the best model by validation loss.
4. Load best checkpoint and print 3 example translations from the test set.

---

## Key Concepts Summary

| Concept | Role in This Code |
|---------|-------------------|
| Self-Attention | Lets each token attend to all other tokens in the same sequence |
| Cross-Attention | Decoder attends to encoder output for source context |
| Causal Mask | Prevents decoder from "seeing" future target tokens during training |
| Padding Mask | Ignores `<pad>` tokens in attention scores |
| Teacher Forcing | Ground-truth target is fed to decoder during training |
| Greedy Decoding | Takes argmax at each step during inference |
| Residual + LayerNorm | Stabilizes deep network training |
| Embedding Scaling | Multiplies embeddings by $\sqrt{d_{model}}$ to balance with positional encoding magnitudes |

---

## Dependencies

- `torch` (PyTorch)
- `spacy` + models (`de_core_news_sm`, `en_core_web_sm`)
- `tqdm` (progress bars)
- Standard library: `gzip`, `math`, `random`, `time`, `collections`, `typing`, `os`, `urllib`
