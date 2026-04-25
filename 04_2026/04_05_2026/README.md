# Text Feature Engineering Assignment

## 📋 Project Overview

This project implements a comprehensive text processing pipeline for analyzing product reviews using classical NLP feature engineering techniques. It demonstrates the implementation and comparison of One Hot Encoding, Bag of Words, and TF-IDF for sentiment classification.

## 🎯 Objectives

- Build a complete text preprocessing pipeline
- Implement multiple feature engineering techniques
- Compare classical NLP methods (OHE, BoW, TF-IDF)
- Analyze sparse matrix efficiency
- Build and evaluate sentiment classification models
- Understand real-world applications and limitations

## 📁 Project Structure

```
04_11_2026/
│
├── text_feature_engineering.ipynb    # Main Jupyter notebook with all implementations
├── product_reviews.csv               # Dataset (110 product reviews)
├── REPORT.md                         # Comprehensive 2-page report with findings
└── README.md                         # This file
```

## 🚀 Quick Start

### Prerequisites

```bash
# Required libraries
pip install pandas numpy nltk scikit-learn matplotlib seaborn jupyter
```

### Running the Project

1. **Open the Jupyter Notebook:**
   ```bash
   jupyter notebook text_feature_engineering.ipynb
   ```

2. **Run all cells sequentially** - The notebook is organized in logical sections:
   - Data collection and loading
   - Text preprocessing
   - Vocabulary building
   - Feature engineering (OHE, BoW, TF-IDF)
   - Comparison analysis
   - Sparse matrix analysis
   - Sentiment classification
   - Results and conclusions

3. **View the Report:**
   - Open `REPORT.md` for detailed findings and analysis

## 📊 Dataset

- **Source:** Synthetic product reviews (simulating e-commerce data)
- **Size:** 110 reviews
- **Distribution:** 60 positive, 50 negative
- **Format:** CSV with columns: `review_text`, `sentiment`
- **Note:** In production, replace with actual scraped data using Selenium/BeautifulSoup

## 🔧 Implementation Details

### Task 1: Text Preprocessing
- Lowercase conversion
- Tokenization using NLTK
- Punctuation removal
- Stopword removal
- Lemmatization

### Task 2: Vocabulary Creation
- Built vocabulary from preprocessed tokens
- Analyzed word frequency distribution
- Identified top frequent words
- Vocabulary size: ~200 unique words

### Task 3: Feature Engineering

#### One Hot Encoding (OHE)
- Binary vector representation (word presence/absence)
- Matrix shape: 110 × 200
- Sparsity: >95%
- Use case: Simple document classification

#### Bag of Words (BoW)
- Count-based word frequency vectors
- Matrix shape: 110 × 100 (top features)
- Sparsity: ~92%
- Use case: Short text classification, spam detection

#### TF-IDF
- Weighted representation balancing frequency and importance
- Matrix shape: 110 × 100
- Sparsity: ~94%
- Use case: Document retrieval, search engines

### Task 4: Comparison Analysis
- Created comprehensive comparison table
- Analyzed feature importance in TF-IDF
- Visualized differences between methods
- Explained why common words receive lower weight in TF-IDF

### Task 5: Sparse Matrix Analysis
- Calculated sparsity percentages
- Analyzed memory inefficiency
- Discussed scalability challenges
- Proposed solutions (sparse formats, dense embeddings)

### Task 6: Real-world Questions

**Q1: Why does BoW fail in understanding semantic meaning?**
- Ignores word order
- No context understanding
- Misses synonyms and related words
- Cannot handle negation

**Q2: When to use BoW vs TF-IDF in industry?**
- BoW: Short texts, small vocabulary, frequency matters
- TF-IDF: Long documents, search/retrieval, keyword extraction

**Q3: Limitations of TF-IDF**
- No semantic understanding
- Ignores word order
- High dimensionality & sparsity
- Out-of-vocabulary problem
- Domain dependency

### Task 7: Sentiment Classification

**Models Tested:**
1. Logistic Regression + BoW
2. Logistic Regression + TF-IDF
3. Naive Bayes + BoW
4. Naive Bayes + TF-IDF

**Best Performance:** 🏆 Logistic Regression + TF-IDF (95-100% accuracy)

## 📈 Key Results

| Metric | Value |
|--------|-------|
| Best Accuracy | 95-100% |
| Vocabulary Size | ~200 words |
| Average Sparsity | >93% |
| Training Time | <5 seconds |
| Best Feature Method | TF-IDF |
| Best Classifier | Logistic Regression |

## 🎓 Key Learnings

### Strengths
✅ Simple and interpretable methods  
✅ Fast training and inference  
✅ Good baseline performance  
✅ Works well for sentiment analysis  

### Limitations
❌ No semantic understanding  
❌ Word order ignored  
❌ High sparsity (memory inefficient)  
❌ Cannot handle negation  
❌ Treats synonyms as different words  

### Future Improvements
🔮 Word embeddings (Word2Vec, GloVe)  
🔮 Contextual embeddings (BERT, RoBERTa)  
🔮 N-grams for phrase capture  
🔮 Deep learning models (CNN, LSTM)  
🔮 Ensemble methods  

## 📚 Technologies Used

- **Python 3.11+**
- **pandas** - Data manipulation
- **numpy** - Numerical computing
- **nltk** - Natural language processing
- **scikit-learn** - Machine learning and feature engineering
- **matplotlib & seaborn** - Data visualization
- **Jupyter Notebook** - Interactive development

## 📖 How to Use This Project

### For Learning
1. Study the notebook section by section
2. Experiment with different parameters
3. Try your own review text
4. Modify preprocessing steps
5. Test different classifiers

### For Production
1. Replace synthetic data with real scraped reviews
2. Increase dataset size to 10,000+ reviews
3. Tune hyperparameters using GridSearchCV
4. Add error handling and validation
5. Deploy as REST API using Flask/FastAPI
6. Monitor model performance over time

### For Research
1. Compare with modern embeddings (BERT)
2. Analyze different domains (movies, restaurants, electronics)
3. Experiment with multilingual reviews
4. Study impact of preprocessing steps
5. Investigate ensemble methods

## 🔬 Experimental Settings

- **Train/Test Split:** 80/20
- **Random Seed:** 42 (for reproducibility)
- **Max Features:** 100-500 (dimensionality control)
- **Stopwords:** English (NLTK)
- **Preprocessing:** Full pipeline (lowercase, tokenize, remove stopwords, lemmatize)

## 📝 Deliverables

✅ **Jupyter Notebook** (`text_feature_engineering.ipynb`)
- Clean, modular, well-documented code
- All 7 tasks implemented
- Comprehensive visualizations
- Detailed explanations

✅ **Dataset** (`product_reviews.csv`)
- 110 product reviews
- Balanced sentiment distribution
- Clean and readable format

✅ **Report** (`REPORT.md`)
- 2-page comprehensive analysis
- Key findings and observations
- Comparison tables
- Real-world recommendations
- Mathematical foundations

✅ **Documentation** (`README.md`)
- Project overview and structure
- Quick start guide
- Implementation details
- Usage instructions

## 🎯 Assignment Completion Checklist

- [x] Task 1: Text preprocessing (lowercase, tokenization, stopwords, lemmatization)
- [x] Task 2: Vocabulary creation and frequency analysis
- [x] Task 3: Feature engineering (OHE, BoW, TF-IDF)
- [x] Task 4: Comparison analysis with visualizations
- [x] Task 5: Sparse matrix analysis
- [x] Task 6: Real-world questions answered
- [x] Task 7: Sentiment classification with model comparison
- [x] Deliverable: Jupyter notebook (.ipynb)
- [x] Deliverable: Clean and modular code
- [x] Deliverable: Dataset (CSV)
- [x] Deliverable: Comprehensive report (1-2 pages)

## 🤝 Contributing

This is an educational project. Feel free to:
- Experiment with the code
- Add new features
- Try different datasets
- Share insights and improvements

## 📧 Contact

For questions or discussions about this project, please refer to the course materials or instructor.

## 📄 License

This project is created for educational purposes as part of the Gen AI & Agentic AI course.

---

**Project Status:** ✅ Complete  
**Date:** April 11, 2026  
**Version:** 1.0

---

## 🌟 Highlights

> "This project demonstrates the fundamentals of classical NLP feature engineering, providing a solid foundation before transitioning to modern deep learning approaches."

### What Makes This Project Special?

1. **Comprehensive Coverage:** All classical NLP techniques in one place
2. **Real-world Focus:** Practical industry insights and use cases
3. **Clear Comparisons:** Direct performance comparison of different methods
4. **Production-Ready:** Modular code ready for extension
5. **Educational Value:** Detailed explanations and visualizations

### Key Takeaways

💡 **TF-IDF outperforms BoW** for most text classification tasks  
💡 **Sparse matrices** are inefficient for large-scale systems  
💡 **Classical methods** provide good baselines but have limitations  
💡 **Modern embeddings** (BERT, Word2Vec) address many limitations  
💡 **Feature engineering** remains important even in the deep learning era  

---

*Happy Learning! 🚀*
