# Encoding & Text Feature Engineering - Concepts Covered

## 1) Goal of the Notebooks
Three notebooks cover text-to-numerical-feature conversion, progressing from basic encoding techniques to a full real-world text feature engineering pipeline with sentiment classification.

---

## 2) Notebooks Summary

### encoding.ipynb
A hands-on walkthrough of three classical encoding techniques:
- **One-Hot Encoding** using `sklearn.preprocessing.OneHotEncoder`
- **Bag of Words (BoW)** using `sklearn.feature_extraction.text.CountVectorizer`
- **TF-IDF** using `sklearn.feature_extraction.text.TfidfVectorizer`

Includes exploration of sparse matrices, out-of-vocabulary behavior, and scikit-learn documentation links.

### text_feature_engineering.ipynb
A comprehensive assignment-style notebook that builds a full text processing pipeline on a product reviews dataset (110 reviews). Covers:
- Data collection (synthetic reviews with positive/negative/neutral labels)
- Text preprocessing (lowercase, punctuation removal, tokenization, stopword removal, lemmatization)
- Vocabulary creation and frequency analysis
- One-Hot Encoding, BoW, and TF-IDF implementations
- Sparse matrix analysis
- Sentiment classification using Logistic Regression and Naive Bayes
- Feature importance analysis with visualizations

### classical_word_embedding.ipynb
An empty/placeholder notebook — likely intended for Word2Vec or GloVe content (covered in later sessions).

---

## 3) Core Libraries Used
- `sklearn.preprocessing.OneHotEncoder`: binary one-hot vectors per word
- `sklearn.feature_extraction.text.CountVectorizer`: Bag of Words representation
- `sklearn.feature_extraction.text.TfidfVectorizer`: TF-IDF weighted representation
- `nltk`: tokenization (`word_tokenize`), stopwords, lemmatization (`WordNetLemmatizer`)
- `pandas`, `numpy`: data manipulation
- `matplotlib`, `seaborn`: visualizations
- `sklearn.linear_model.LogisticRegression`, `sklearn.naive_bayes.MultinomialNB`: classifiers
- `sklearn.metrics`: accuracy, classification report, confusion matrix

---

## 4) One-Hot Encoding

### Pipeline
1. Define documents (sentences).
2. Tokenize via `.lower().split()`.
3. Reshape tokens into `[[word]]` format for the encoder.
4. Fit `OneHotEncoder(sparse_output=False)` on all words.
5. Transform each sentence's words into one-hot vectors.

### Key Detail
- `sparse_output=False`: returns a dense NumPy array instead of a sparse matrix.

### Characteristics
- Binary (0/1) — word is present or not.
- No word frequency captured.
- High-dimensional and very sparse for large vocabularies.

---

## 5) Bag of Words (BoW)

### Pipeline
1. Create `CountVectorizer()`.
2. `fit_transform(documents)` to learn vocabulary and produce count matrix.
3. Inspect vocabulary via `get_feature_names_out()`.
4. View matrix via `.toarray()`.

### Key Observations
- Repeated words get higher counts.
- `fit()` learns vocabulary; `transform()` applies it to new data.
- Out-of-vocabulary words are silently ignored during `transform()`.
- Demonstrated with example: `"lion is the king of jungle"` transformed against a movie/cricket vocabulary produces all zeros.

### Limitations
- Ignores word order.
- Common words dominate.
- No semantic understanding.

---

## 6) TF-IDF (Term Frequency - Inverse Document Frequency)

### Pipeline
1. Create `TfidfVectorizer()`.
2. `fit_transform(documents)` to produce weighted matrix.
3. Inspect vocabulary and matrix.

### How It Works
- **TF**: how often a word appears in a document.
- **IDF**: penalizes words appearing across many documents.
- **TF-IDF = TF × IDF**: highlights words unique to a document; down-weights common words.

### Advantage over BoW
- Reduces impact of frequently occurring but non-informative words (e.g., "people", "and").

---

## 7) Comparison Table

| Feature | One-Hot Encoding | Bag of Words | TF-IDF |
|---------|-----------------|--------------|--------|
| Unit of encoding | Individual word | Document-level | Document-level |
| Output values | Binary (0/1) | Integer counts | Float weights (0–1) |
| Word frequency captured | No | Yes | Yes (normalized) |
| Penalizes common words | No | No | Yes |
| Word order preserved | No | No | No |
| Semantic meaning | No | No | No |
| Sparsity | ~95%+ | ~92% | ~94% |
| Best paired classifier | Any | Naive Bayes | Logistic Regression |

---

## 8) Text Preprocessing Pipeline (TextPreprocessor class)

The `text_feature_engineering.ipynb` implements a reusable `TextPreprocessor` class:

1. **Lowercase conversion** — standardize text
2. **Punctuation removal** — `str.maketrans` + `string.punctuation`
3. **Tokenization** — `nltk.word_tokenize()`
4. **Stopword removal** — `nltk.corpus.stopwords`
5. **Lemmatization** — `nltk.stem.WordNetLemmatizer`

Impact: vocabulary reduced from ~500 to ~200 unique tokens (~60% reduction).

---

## 9) Sparse Matrix Analysis

All three methods produce highly sparse matrices (>90% zeros).

### Why Sparsity Is Problematic
1. **Memory waste**: most storage holds zeros.
2. **Computational inefficiency**: operations on zeros waste CPU.
3. **Scalability**: vocabulary grows with corpus → impractical at scale.

### Solutions
- Sparse storage formats (CSR, CSC) to store only non-zero values.
- Dense embeddings (Word2Vec, GloVe, BERT) — typically 100–768 dimensions.
- Dimensionality reduction (PCA, SVD).
- Feature selection (top-k informative features).

---

## 10) Sentiment Classification Mini Use Case

### Dataset
- 110 synthetic product reviews: 60 positive, 50 negative (10 neutral labeled positive).
- Saved as `product_reviews.csv`.

### Models Trained
| Model | Accuracy |
|-------|----------|
| Logistic Regression + BoW | ~95–100% |
| Naive Bayes + BoW | ~95–100% |
| Logistic Regression + TF-IDF | ~95–100% (best) |
| Naive Bayes + TF-IDF | ~95–100% |

### Key Finding
- TF-IDF + Logistic Regression generally performs best.
- Feature importance analysis reveals top positive indicators (excellent, amazing, great) and top negative indicators (terrible, poor, waste).

---

## 11) Real-World Questions Addressed

### Why BoW fails at semantic meaning:
- Ignores word order ("not good" ≈ "good")
- No context understanding ("bank" in river vs finance)
- Misses synonyms ("happy" ≠ "joyful" in BoW)
- Cannot handle negation

### When to use BoW vs TF-IDF:
- **BoW**: short texts, small vocabulary, frequency is a signal (e.g., spam detection, tweets)
- **TF-IDF**: long documents, search/retrieval, large corpus, keyword extraction (e.g., search engines, recommendation systems)

### TF-IDF limitations:
- No semantic understanding
- Ignores word order
- High dimensionality
- Out-of-vocabulary problem
- Document length bias
- Domain dependency

---

## 12) Practical Takeaways

- Start with TF-IDF as a baseline for text classification tasks.
- Use Logistic Regression for interpretable results; Naive Bayes for fast baselines.
- All classical methods lose word order and semantics — this motivates word embeddings (Word2Vec, GloVe) and contextual embeddings (BERT, GPT) covered in later sessions.
- For production systems, consider BERT-based models for better accuracy.
- The `fit()`/`transform()` pattern in scikit-learn ensures consistent vocabulary between training and inference.
