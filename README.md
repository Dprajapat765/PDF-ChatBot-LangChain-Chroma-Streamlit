# 📄 PDF Chatbot (LangChain + Chroma + Streamlit)

This project lets you upload any PDF and chat with it like ChatGPT!  
It uses LangChain, OpenAI Embeddings, ChromaDB, and Streamlit UI.

---

## 🔧 Features

- Upload PDF and extract text
- Chunk + embed into Chroma vector DB
- Ask questions and get contextual answers
- Clean chat interface with history

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/Dprajapat765/pdf-chatbot.git
cd pdf-chatbot
```

### 2. Create virtual environment
```
python -m venv genai_env
source genai_env/bin/activate  # or `.\genai_env\Scripts\activate` on Windows
```

### 3. Install dependencies
```
pip install -r requirements.txt
```

### 4. Set your OpenAI API key
Create a .env file or export:
```
export OPENAI_API_KEY=your_key_here
```


### 5. Run the app
```
streamlit run app.py
```


