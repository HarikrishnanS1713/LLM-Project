# 🤖 AI Code Companion

An AI-powered programming assistant built using Python, Streamlit, Ollama, and the Qwen 2.5 Large Language Model.

## 📌 About the Project

AI Code Companion is a Generative AI application designed to help users understand, generate, and debug Python code.

It uses a locally running Large Language Model through Ollama to provide programming assistance.

The application also uses SQLite to store conversation history permanently.

## 🚀 Features

* **Code Explanation:** Understand Python code with step-by-step explanations.
* **Code Generation:** Generate Python programs based on user requirements.
* **Code Debugging:** Identify programming errors and suggest corrections.
* **File Upload:** Upload Python and text files for AI analysis.
* **Instant AI Responses:** Display generated answers immediately.
* **Chat History:** Store and retrieve previous conversations.
* **SQLite Database:** Permanently save conversations.
* **Download Responses:** Download individual AI answers or complete chat history.
* **Error Handling:** Display understandable messages for common application errors.

## 🛠️ Technologies Used

* Python
* Generative AI
* Large Language Models (LLM)
* Qwen 2.5 3B
* Ollama
* Streamlit
* SQLite
* python-dotenv

## 📂 Project Structure

```text
AI-Code-Companion/
│
├── app.py
├── database.py
├── requirements.txt
├── README.md
├── .env
├── .gitignore
│
└── chat_history.db
```

The `.env`, `.venv`, and database files should not be uploaded to GitHub.

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Open the project folder

```bash
cd AI-Code-Companion
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Install Ollama

Download and install Ollama.

### 7. Download the AI model

```bash
ollama pull qwen2.5:3b
```

### 8. Configure environment variables

Create a `.env` file:

```text
OLLAMA_MODEL=qwen2.5:3b
```

### 9. Run the application

```bash
python -m streamlit run app.py
```

## 🎯 Project Objective

The main objective of this project is to explore the practical implementation of Generative AI and Large Language Models by developing an interactive programming assistant.

## 👨‍💻 Author

GenAI Learner
