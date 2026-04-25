# Classical Word Embedding (Word2Vec) - Concepts Covered

## 1) Goal of the Notebook
Demonstrates how to use a pre-trained Word2Vec model (Google News) to explore word embeddings, perform semantic operations, and create sentence-level representations using Average Word2Vec.

---

## 2) Core Libraries Used
- `gensim.models.Word2Vec`, `gensim.models.KeyedVectors`: Word2Vec model handling
- `gensim.downloader`: downloading pre-trained models
- `numpy`: computing average vectors

---

## 3) Pre-trained Model Used

**Model:** `word2vec-google-news-300`
- Trained on Google News dataset
- Embedding dimension: **300** (number of neurons in hidden layer)
- Architecture: **Skip-gram**
- Contains vectors for millions of words/phrases

Loaded via:
```python
model = api.load("word2vec-google-news-300")
```

---

## 4) Word Vector Operations Demonstrated

### Retrieving a Word Vector
```python
model["sunny"]       # returns a 300-dimensional numpy array
len(model["sunny"])   # 300
```

### Key Limitation
- Multi-word phrases like `"i am sunny"` cause a `KeyError` — Word2Vec maps **individual words**, not sentences.

---

## 5) Semantic Similarity

### `most_similar(word)`
Finds the top 10 words closest in vector space:
```python
model.most_similar("man")    # returns words like woman, boy, person...
model.most_similar("golf")   # returns words like golfer, PGA, tee...
```

### `similarity(word1, word2)`
Returns cosine similarity (float between -1 and 1):

| Word Pair | Relationship | Expected Similarity |
|-----------|-------------|-------------------|
| man, woman | Gendered pair | High (~0.76) |
| man, python | Unrelated | Low |
| man, men | Singular/plural | Very high |
| delighted, ecstatic | Synonyms | High |
| python, snake | Polysemy | Moderate-high |
| overcast, cloudy | Synonyms | High |
| sunny, Sunny | Case-sensitive | May differ |

**Note:** Word2Vec is case-sensitive — `"sunny"` and `"Sunny"` may have different vectors.

---

## 6) Odd-One-Out Detection

### `doesnt_match(word_list)`
Identifies the word least similar to the others:
```python
model.doesnt_match(["PHP", "FOOD", "India", "JAVA", "DOG", "C++", "NBA"])
```
The model identifies which word doesn't belong based on vector distances.

---

## 7) Word Analogy (Vector Arithmetic)

The classic Word2Vec analogy test:
```python
vec = model['king'] - model['man'] + model['woman']
model.most_similar([vec])  # → "queen" (ideally)
```

This demonstrates that Word2Vec captures semantic relationships as vector directions:
- king - man + woman ≈ queen
- The "royalty" direction is preserved while swapping gender.

---

## 8) Average Word2Vec (Sentence Embedding)

### Problem
Word2Vec produces a vector per **word**, but many tasks need a vector per **sentence** or **document**.

### Solution: Average Word2Vec
1. Tokenize the sentence into words.
2. Look up each word's vector from the model.
3. Compute the element-wise mean of all word vectors.

```python
sentence = "I loVe Machine leaRning"
words = sentence.lower().split()

word_vectors = []
for word in words:
    word_vectors.append(model[word])

sentence_vector = np.mean(word_vectors, axis=0)
# sentence_vector.shape → (300,)
```

### Result
- Each sentence becomes a single 300-dimensional dense vector.
- Can be used as input to ML classifiers.

### Limitations
- Ignores word order.
- All words weighted equally (no importance weighting).
- Out-of-vocabulary words cause errors.

---

## 9) Key Concepts Summarized

| Concept | Level | Output |
|---------|-------|--------|
| Word2Vec | Word-level | One vector per word (300-d) |
| Average Word2Vec | Sentence-level | One vector per sentence (300-d) |
| Transformers (next class) | Contextual | Context-aware vectors per token |

---

## 10) Practical Takeaways

- Word2Vec captures **semantic meaning** — similar words have similar vectors.
- **Vector arithmetic** encodes relationships (king - man + woman = queen).
- **Average Word2Vec** is a simple way to get sentence embeddings, but it's an older technique.
- Modern alternatives: **Transformer-based models** (BERT, GPT) provide context-aware embeddings and are state-of-the-art (covered in next class).
- Pre-trained models like `word2vec-google-news-300` are useful for general-purpose tasks without training your own embeddings.
