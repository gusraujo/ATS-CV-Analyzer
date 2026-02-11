# 🚀 ATS Resume Optimizer API

An AI-powered ATS resume optimizer built with **FastAPI**, designed to:

- 📄 Extract CV data from PDF  
- 🧠 Parse structured job descriptions  
- 🎯 Match CV against job requirements  
- ✍ Rewrite resume to improve ATS score  
- 🖨 Generate optimized PDF output  

---



### Main Flow

1. Upload CV (PDF)
2. Send structured Job JSON
3. Extract CV → Validate → Match → Rewrite
4. Generate optimized PDF
5. Return optimized file

---

# 📦 Requirements

## ✅ Python Version

Python **3.11+ recommended**  
(3.11 is the most stable for ecosystem compatibility)

Check your version:

```bash
python --version
```

📥 Installation
1️⃣ Create Virtual Environment (Recommended)
```bash
python -m venv venv
```

## Activate

### Windows
```bash
venv\Scripts\activate
```

### Mac/Linux
```bash
source venv/bin/activate
```

## 2️⃣ Install Dependencies
```bash
pip install fastapi
pip install uvicorn
pip install python-multipart
pip install pydantic
pip install reportlab
pip install PyPDF2
pip install openai
pip install python-dotenv
```


# 🔐 Environment Variables

## Create a .env file in the root of the project:

```bash
OPENAI_API_KEY=your_openai_key_here
```
Make sure your LLM client loads it:

```bash

from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
```


## ▶ Running the Application

Run the FastAPI server using:
```bash
uvicorn app.main:app --reload
```

If your main file is different, adjust accordingly:
```bash
uvicorn main:app --reload
```

Server will run at:
```bash
http://127.0.0.1:8000
```


# 📘 API Documentation

Once running, access interactive documentation:

Swagger UI:

http://127.0.0.1:8000/docs


Redoc:

http://127.0.0.1:8000/redoc