# Embeddings Demonstration

This project provides a comprehensive Jupyter notebook demonstrating the use of embeddings for natural language processing tasks.

## What's Included

The `embeddings_demo.ipynb` notebook covers:

1. **Introduction to Embeddings** - Understanding what embeddings are and their applications
2. **Creating Embeddings** - Using pre-trained models to generate text embeddings
3. **Semantic Similarity** - Measuring how similar different texts are
4. **Visualization** - Using PCA to visualize high-dimensional embeddings in 2D
5. **Semantic Search** - Building a simple search engine that understands meaning
6. **Document Clustering** - Grouping similar documents together
7. **Practical Examples** - Finding outliers and understanding similarity scores

## Installation

1. Install dependencies using uv (recommended):
```bash
uv sync
```

2. Add the kernel to the notebook 
```bash
uv run main.py
```


3. Open `embeddings_demo.ipynb` and run the cells!

## Requirements

- Python 3.13+
- sentence-transformers
- numpy
- matplotlib
- seaborn
- scikit-learn
- jupyter

## Key Concepts Demonstrated

- **Text Embeddings**: Converting text to numerical vectors
- **Cosine Similarity**: Measuring semantic similarity between texts
- **Dimensionality Reduction**: Visualizing high-dimensional data
- **Semantic Search**: Finding relevant content by meaning, not just keywords
- **Clustering**: Grouping similar items together

## Use Cases

- Search engines
- Recommendation systems
- Chatbots and virtual assistants
- Document classification
- Duplicate detection
- Question answering systems

## Model Used

The notebook uses the `all-MiniLM-L6-v2` model from Sentence Transformers, which:
- Produces 384-dimensional embeddings
- Is fast and lightweight
- Works well for general-purpose tasks

Feel free to experiment with other models from the [Sentence Transformers library](https://www.sbert.net/)!

