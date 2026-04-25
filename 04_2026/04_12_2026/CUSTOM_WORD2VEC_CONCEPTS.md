# Custom Word2Vec Training - Concepts Covered

## 1) Goal of the Notebook
The notebook demonstrates how to train a custom Word2Vec model on local text files and inspect learned word embeddings.

## 2) Core Libraries Used
- `nltk`: sentence tokenization (`sent_tokenize`)
- `gensim`: Word2Vec model creation, vocabulary building, training, and vector operations
- `os`: reading multiple files from a data folder
- `numpy`, `pandas`: imported (not central to the final training flow here)

## 3) Data Preparation Pipeline
The notebook follows this practical NLP pipeline:

1. Read raw text files from a local `data` directory.
2. Split raw text into sentences using `sent_tokenize`.
3. Convert each sentence into cleaned tokens using `simple_preprocess`.
4. Build a training corpus (`story`) as a list of tokenized sentences.

Conceptually, training data shape is:
- Input: list of documents/files
- After preprocessing: list of sentences
- Final training format: `List[List[str]]` (tokens per sentence)

## 4) Word2Vec Fundamentals Covered
The notebook touches both major Word2Vec architectures:
- CBOW (`sg=0`): predicts target word from surrounding context words
- Skip-gram (`sg=1`): predicts surrounding words from a target word

Only one model is trained in the notebook, but comments explain CBOW vs Skip-gram configuration.

## 5) Hyperparameters Discussed and Used
The custom model is initialized with:
- `window=10`: size of context window around each target word
- `min_count=1`: keep even very rare words in vocabulary
- `vector_size=150`: embedding dimension for each word vector

Additional training setup:
- `build_vocab(story)`: scans corpus and creates vocabulary
- `train(..., total_examples=corpus_count, epochs=10)`: trains embeddings for 10 epochs

## 6) Vocabulary and Corpus Concepts
The notebook checks:
- `corpus_count`: number of training sentences/examples
- vocabulary size (number of unique words learned)

Important distinction:
- More corpus examples generally improve semantic quality.
- Larger vocabulary with very rare words may add noise if corpus is small.

## 7) Embedding Inspection and Semantic Queries
The notebook demonstrates major embedding operations:

- Retrieve vector for a word:
  - `model.wv["arjun"]`
- Check embedding dimension:
  - `len(model.wv["arjun"])` (matches `vector_size`)
- Find semantically similar words:
  - `model.wv.most_similar("ai")`
- Find odd one out from a list:
  - `model.wv.doesnt_match([...])`
- Compute cosine similarity between words:
  - `model.wv.similarity("ai", "technology")`

These operations validate whether embeddings capture semantic relationships in the training corpus.

## 8) Practical Learning Outcome
By the end of the notebook, the learner understands how to:
- create a custom corpus
- train Word2Vec from scratch on domain text
- tune key hyperparameters
- evaluate embeddings qualitatively via similarity and analogy-like checks

## 9) Limitations Noted Implicitly
From the notebook flow, the main practical constraints are:
- Small corpus can limit embedding quality.
- Very low `min_count` may include noisy tokens.
- Results are sensitive to tokenization quality and training epochs.

## 10) Assignment / Next Experiments Mentioned
The notebook suggests experimentation with:
- adding more data
- increasing training epochs
- checking model quality/accuracy
- trying different embedding dimensions
- broadly tuning all hyperparameters

## 11) Suggested Cleaned Workflow (Best Practice)
For stronger results in future runs:
- use relative paths instead of machine-specific absolute paths
- avoid `nltk.download('all')`; install only required resources
- split train/validation for downstream task-based evaluation
- save model after training for reuse

Example:
- `custom_model.save("custom_word2vec.model")`
