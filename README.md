# Mini RAG (Retrieval-Augmented Generation) App

A lightweight implementation of a Retrieval-Augmented Generation system that combines document retrieval with language generation for enhanced question-answering capabilities.

## 🚀 Features

- **Document Processing**: Extract and process text from various document formats
- **Vector Embeddings**: Generate embeddings for semantic search
- **Vector Database**: Store and retrieve document embeddings efficiently
- **Question Answering**: Answer questions based on retrieved document context
- **Web Interface**: Simple and intuitive user interface for interaction

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## 🛠️ Installation

1. **Clone the repository**

   ```bash
   git clone <your-repo-url>
   cd mini-rag
   ```

2. **Create and activate virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Quick Start

1. **Activate your virtual environment**

   ```bash
   source venv/bin/activate
   ```

2. **Run the application**

   ```bash
   python app.py
   ```

3. **Open your browser** and navigate to `http://localhost:5000`

## 📁 Project Structure

```
mini-rag/
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── venv/                 # Virtual environment
├── data/                 # Document storage
├── models/               # Saved models and embeddings
└── static/               # Static web assets
```

## 🔧 Configuration

Create a `.env` file in the root directory with your configuration:

```env
OPENAI_API_KEY=your_openai_api_key_here
EMBEDDING_MODEL=text-embedding-ada-002
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
```

## 📖 Usage

### Adding Documents

1. Upload documents through the web interface
2. Documents are automatically processed and embedded
3. Vector embeddings are stored for fast retrieval

### Asking Questions

1. Type your question in the search box
2. The system retrieves relevant document chunks
3. An answer is generated based on the retrieved context

## 🧪 API Endpoints

- `POST /upload` - Upload documents
- `POST /process` - process documents
- `POST /query` - Ask questions and get answers
- `GET /documents` - List all processed documents
- `DELETE /documents/<id>` - Remove a document

## 📦 Dependencies

- **Flask**: Web framework
- **OpenAI**: Language model API
- **QdrantDB**: Vector database
- **LangChain**: Document processing and retrieval
- **Pandas**: Data manipulation
- **NumPy**: Numerical computing

## 🙏 Acknowledgments

- OpenAI for providing the language models
- QdrantDB for vector storage capabilities
- LangChain for the RAG framework

**Happy RAG-ing! 🎉**
