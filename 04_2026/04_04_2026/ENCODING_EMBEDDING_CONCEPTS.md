# Text Encoding & Embedding - Concepts Covered

## 1) Goal of the Notebooks
The notebooks demonstrate how to convert raw text into numerical representations using classical encoding and vectorization techniques from scikit-learn. Four notebook variants cover the same core concepts with slightly different example data.

## 2) Core Libraries Used
- `sklearn.preprocessing.OneHotEncoder`: converts individual words into binary one-hot vectors
- `sklearn.feature_extraction.text.CountVectorizer`: Bag of Words (BoW) representation
- `sklearn.feature_extraction.text.TfidfVectorizer`: TF-IDF weighted representation
- `numpy`: numerical array operations

## 3) Fundamental Aim
Convert text data into numbers so machine learning models can process it.
> AIM: Convert Data → Numbers

## 4) One-Hot Encoding

### Pipeline
1. Define a list of documents (sentences).
2. Tokenize: split each sentence into lowercase words using `.lower().split()`.
3. Reshape tokens into `[[word]]` format (each word wrapped in its own list) for the encoder.
4. Fit `OneHotEncoder(sparse_output=False)` on all words to learn the vocabulary.
5. Transform each sentence's words into one-hot vectors.

### Key Parameter
- `sparse_output=False`: returns a dense NumPy array instead of a sparse matrix, making the output easier to read and inspect.

### What It Produces
Each word becomes a binary vector of length equal to the vocabulary size, with exactly one `1` at the position corresponding to that word.

### Limitations
- Produces high-dimensional vectors for large vocabularies.
- No notion of word frequency or semantic similarity.
- Each word is equidistant from every other word.

## 5) Bag of Words (BoW)

### Pipeline
1. Define a list of documents.
2. Create a `CountVectorizer()` instance.
3. Call `fit_transform(documents)` to learn vocabulary and produce the BoW matrix.
4. Inspect vocabulary with `get_feature_names_out()`.
5. View the count matrix with `.toarray()`.

### What It Produces
A matrix where each row is a document and each column is a word from the vocabulary. Cell values are the count of how many times that word appears in that document.

### Key Observations from the Notebooks
- Words that appear multiple times get higher counts (e.g., "watch movie and watch movie again" → "watch" gets count 2, "movie" gets count 2).
- `fit()` learns the vocabulary; `transform()` converts new documents using only that learned vocabulary.
- Words not in the learned vocabulary are ignored during transform (demonstrated with `"lion is the king of jungle"` against a vocabulary learned from people/movie/cricket sentences).

### Limitations
- Ignores word order (hence "bag" of words).
- High-frequency common words can dominate.
- No notion of semantic similarity.

## 6) TF-IDF (Term Frequency - Inverse Document Frequency)

### Pipeline
1. Define a list of documents.
2. Create a `TfidfVectorizer()` instance.
3. Call `fit_transform(documents)` to produce the TF-IDF matrix.
4. Inspect vocabulary with `get_feature_names_out()`.
5. View the weighted matrix with `.toarray()`.

### What It Produces
A matrix similar to BoW, but instead of raw counts, each cell contains a TF-IDF weight:
- **TF (Term Frequency)**: how often a word appears in a document.
- **IDF (Inverse Document Frequency)**: penalizes words that appear across many documents (common words get lower weight).
- **TF-IDF = TF × IDF**: words unique to a document get higher scores; common words across all documents get lower scores.

### Advantage over BoW
- Down-weights common/shared words (e.g., "people", "and").
- Highlights discriminative/important words per document.

## 7) Comparison of the Three Techniques

| Feature | One-Hot Encoding | Bag of Words | TF-IDF |
|---------|-----------------|--------------|--------|
| Unit of encoding | Individual word | Document-level | Document-level |
| Output values | Binary (0 or 1) | Integer counts | Float weights |
| Word frequency captured | No | Yes | Yes (weighted) |
| Penalizes common words | No | No | Yes |
| Word order preserved | No | No | No |
| Semantic meaning captured | No | No | No |
| Typical use | Categorical features | Text classification baseline | Text classification, search |

## 8) Notebook Variants Summary
- **encoding-embedding.ipynb**: Clean consolidated version covering all three techniques (One-Hot, BoW, TF-IDF) with markdown section headers.
- **encoding.ipynb**: Detailed walkthrough with extra exploration steps — includes scikit-learn documentation links, additional test with out-of-vocabulary words, and intermediate inspection of sparse matrices.
- **encoding1.ipynb**: Practice version using different example data (shows, basketball, plays) — covers One-Hot Encoding and begins BoW with CountVectorizer import.
- **encoding2.ipynb**: Similar to encoding.ipynb with minor variations in example text — covers One-Hot Encoding and BoW.

## 9) Key scikit-learn API Patterns Demonstrated
- **fit / transform / fit_transform** workflow:
  - `fit()`: learn vocabulary from training data
  - `transform()`: apply learned vocabulary to new data
  - `fit_transform()`: do both in one step
- **Sparse vs dense output**: `.toarray()` converts sparse matrices to dense NumPy arrays
- **Vocabulary inspection**: `encoder.categories_[0]` for OneHotEncoder, `vectorizer.get_feature_names_out()` for CountVectorizer/TfidfVectorizer
- **Out-of-vocabulary handling**: words not seen during `fit()` are silently ignored during `transform()`

## 10) Practical Takeaways
- One-Hot Encoding is useful for individual categorical features but not practical for large text vocabularies.
- Bag of Words is the simplest document-level representation — good baseline for text classification.
- TF-IDF improves upon BoW by reducing the impact of common words — preferred for most classical NLP tasks.
- All three methods lose word order and semantic meaning — this motivates the use of word embeddings (Word2Vec, GloVe) and contextual embeddings (BERT, GPT) covered in later sessions.
