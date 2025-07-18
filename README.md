# 📝 AI Text Summarizer using Streamlit & Groq API (Ongoing Project)

A **simple AI-powered text summarizer** built with **Streamlit** and **Groq API**, leveraging **LLaMA-3 models**. Summarize articles, PDFs, or notes into concise summaries with custom tone and format options.

---

## 🚀 Live Demo
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ai-text-summarizer-jesstesting.streamlit.app/)

---

## ✨ Features   
- ✅ **Summarize any text** using **Groq API** with `llama-3.3-70b-versatile`  
- ✅ **Custom Summary Length** – Short, Medium, or Detailed 
- ✅ **Tone Selection** - Neutral, Simple, Professional, Casual, Kid-friendly 
- ✅ **Output Formats** - Bullets, Paragraph, Bullets + Paragraph, TL;DR
- ✅ **File Upload Support** – Upload PDF, DOCX, or TXT files for summarization
- ✅ **Word & Token Count** – Displays before summarization for better control
- ✅ **Download Summary** - – Export summary as a `.txt` file  
- ✅ **Secure API Handling** using `.env` for local and **Streamlit Secrets** for cloud
- ✅ **Clean UI** with **Streamlit**, responsive and user-friendly

---

## 🛠 Tech Stack
- **Frontend:** Streamlit
- **Backend:** Python
- **LLM Provider:** Groq API

---

## 📂 Project Structure
```
├── app.py
├── README.md
├── requirements.txt
└── .env.example
```

---

## 📦 Installation

### 1. Clone the repository
```bash
git clone https://github.com/jessicaagarwal/ai-text-summarizer.git
cd ai-text-summarizer
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate   # On Mac/Linux
.venv\Scripts\activate      # On Windows
```

---


## 🔑 API Setup

### 1. Get Groq API Key
- Visit [Groq Console](https://console.groq.com/keys)
- Copy your API key

### 2. Local Development
Create `.env` file in project root:
```
GROQ_API_KEY=your_api_key_here
```

Install dependencies:
```
pip install -r requirements.txt
```

Run the app:
```
streamlit run app.py
```

### 3. Streamlit Cloud Deployment
- Add your key in **Streamlit Secrets**:
```
GROQ_API_KEY="your_api_key_here"
```

---


## ✅ requirements.txt
```
streamlit
python-dotenv
groq
PyPDF2
python-docx
httpx==0.27.0

```

---

## ▶️ Run the App
```bash
streamlit run app.py
```

The app will be available at:
```
http://localhost:8501
```

---

## 📚 Resources
- [Groq API Docs](https://console.groq.com/docs)
- [Streamlit Docs](https://docs.streamlit.io)

---

## 🔥 Future Enhancements
- Deploy on **custom theme**
- Add Multi-LLM Support (OpenAI, Claude, Gemini)

---

### ⭐ If you like this project, give it a star on GitHub!
