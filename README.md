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

- `POST /upload` - Upload and process documents
- `POST /query` - Ask questions and get answers
- `GET /documents` - List all processed documents
- `DELETE /documents/<id>` - Remove a document

## 🛠️ Development

### Running in Development Mode

```bash
export FLASK_ENV=development
python app.py
```

### Running Tests

```bash
python -m pytest tests/
```

## 📦 Dependencies

- **Flask**: Web framework
- **OpenAI**: Language model API
- **ChromaDB**: Vector database
- **LangChain**: Document processing and retrieval
- **Pandas**: Data manipulation
- **NumPy**: Numerical computing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for providing the language models
- ChromaDB for vector storage capabilities
- LangChain for the RAG framework

## 📞 Support

If you encounter any issues or have questions, please:

1. Check the [Issues](https://github.com/yourusername/mini-rag/issues) page
2. Create a new issue with detailed information
3. Contact the maintainers

---

**Happy RAG-ing! 🎉**
