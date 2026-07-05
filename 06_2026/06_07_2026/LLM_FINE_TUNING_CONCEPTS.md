# LLM Fine-Tuning Concepts (June 6–7, 2026)

## Overview

End-to-end LLM fine-tuning pipeline covering three stages: **Non-Instruction (Domain-Adaptive) Fine-Tuning**, **Instruction Fine-Tuning**, and **Preference Tuning** — all applied sequentially on the same model using LoRA/QLoRA adapters.

---

## Stage 1: Non-Instruction Causal LM Fine-Tuning (Domain-Adaptive Continued Pretraining)

- **Goal**: Teach a base model (TinyLlama) domain-specific language from raw pharma PDF text
- **What the model learns**: Drug names, medical terminology, scientific writing style, domain sentence patterns
- **What it does NOT learn**: How to answer questions, follow instructions, or behave as a chatbot
- **Pipeline**: PDF extraction → text cleaning → HF Dataset → tokenization → text packing → LoRA fine-tuning → validation loss → adapter save

### Key Concepts

- **Causal LM**: Predict the next token from left to right (past causes future)
- **Text Cleaning**: Unicode normalization, zero-width char removal, hyphenated line-break fixes, page number removal, space normalization
- **Text Packing**: Join all tokens into one stream, split into fixed-size blocks (e.g., 512 tokens) — avoids padding waste vs. padding each paragraph individually
- **Block Size (512)**: Number of tokens per training example — NOT the embedding dimension
- **DataCollatorForLanguageModeling (mlm=False)**: Batches packed blocks into tensors; `mlm=False` = causal (not BERT-style masked) LM
- **Labels = input_ids**: For causal LM, the target is the same as the input shifted by one position

---

## Stage 2: Instruction Fine-Tuning (IFT)

- **Goal**: Teach the domain-adapted model to follow instructions and answer questions
- **Data Format**: Alpaca-style `### Instruction: ... ### Response: ...` or `instruction/input/output` JSON
- **Continues from Stage 1 LoRA adapter** — not training from scratch
- **Tokenization**: Pad/truncate to `max_length=512`; use `-100` in labels for padding positions so loss ignores them
- **Two approaches for Stage 2**:
  - **Approach 1 (Recommended)**: Continue training the same Stage 1 LoRA adapter on instruction data
  - **Approach 2**: Merge Stage 1 adapter into base model, then add a new LoRA adapter for instruction tuning

---

## Stage 3: Preference Tuning (Planned)

- Uses the merged instruction-tuned model as base
- Trains on chosen/rejected response pairs to align model outputs with human preferences

---

## QLoRA / LoRA Setup

- **4-bit quantization** (`BitsAndBytesConfig`): `load_in_4bit=True`, `nf4` quant type, `float16` compute dtype, double quantization
- **`prepare_model_for_kbit_training`**: Required for stable training with quantized models
- **LoRA targets**: `q_proj`, `k_proj`, `v_proj`, `o_proj`, `gate_proj`, `up_proj`, `down_proj`
- **LoRA trains only adapter parameters** — much cheaper than full fine-tuning

---

## Full 3-Stage Pipeline

```
Base TinyLlama
   ↓ Stage 1: Raw domain text (LoRA)
Domain-adapted LoRA adapter
   ↓ Stage 2: Instruction Q&A data (LoRA)
Instruction-tuned LoRA adapter
   ↓ Merge into base model
Merged instruction-tuned model
   ↓ Stage 3: Preference tuning (chosen/rejected data)
Final aligned model
```

---

## Note: Google Colab

We use **Google Colab** for running these fine-tuning notebooks because it provides free/low-cost access to GPUs (T4, etc.). Fine-tuning LLMs — even small ones like TinyLlama with QLoRA — requires CUDA-capable GPUs for practical training speeds. Colab eliminates the need for local GPU hardware, making it accessible for learning and experimentation.

---

## Fine-Tuning vs. Model Training vs. RAG

### Model Training (Pretraining)
- **What it does**: Trains a model from scratch on massive corpora to learn language
- **Data needed**: Billions of tokens (web, books, code)
- **Model weights**: All weights are learned from random initialization
- **Cost**: Extremely expensive (millions of dollars, weeks of GPU time)
- **When to use**: Building a new foundation model
- **Knowledge source**: Baked into weights during training
- **Example**: Training GPT/LLaMA from scratch

### Fine-Tuning
- **What it does**: Adapts a pretrained model to a specific domain or task by further training on smaller data
- **Data needed**: Hundreds to thousands of domain-specific examples
- **Model weights**: A subset of weights are updated (or adapters added via LoRA)
- **Cost**: Moderate (hours to days on a single GPU with LoRA/QLoRA)
- **When to use**: Teaching a model new domain knowledge, style, or instruction-following ability
- **Knowledge source**: Baked into weights during fine-tuning
- **Example**: Fine-tuning TinyLlama on pharma text (this notebook)

### RAG (Retrieval-Augmented Generation)
- **What it does**: Retrieves relevant documents at inference time and feeds them as context to a pretrained/fine-tuned model
- **Data needed**: A searchable knowledge base (vector store, database)
- **Model weights**: No weights are changed — the model stays frozen
- **Cost**: Low (no training needed; cost is in retrieval infrastructure)
- **When to use**: Giving a model access to up-to-date or private data without retraining
- **Knowledge source**: Provided dynamically at query time via retrieved context
- **Example**: Querying a pharma vector DB and passing results to an LLM for answering
