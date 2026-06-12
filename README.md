# LangChain AI Agents Hub

This repository contains two Streamlit-based AI applications built with LangChain and Groq:
1. **Text-to-Math Solver**: An intelligent chatbot that can solve direct math expressions instantly or use a ReAct agent to solve complex, logic-based word problems.
2. **Chat with SQL Database**: A natural language database assistant that connects to SQLite or MySQL databases and queries them directly using natural language.

---

## 🔒 Security & API Key Setup

This application requires a **Groq API Key** to run. To prevent incurring unexpected costs on other users' accounts, **never share or commit your API keys**. 

### How to use your own Groq API Key:

1. **Option A (Environment Variable - Recommended):**
   Create a `.env` file in the root directory of this project and add your Groq API key:
   ```env
   GROQ_API_KEY=gsk_your_actual_api_key_here
   ```
   *Note: `.env` is already configured in `.gitignore` so your key will never be committed to Git.*

2. **Option B (Streamlit Sidebar Input):**
   When you run the app, you can paste your API key directly into the secure password input field in the left sidebar.
   
You can get your own free/tier API key directly from the [Groq Console](https://console.groq.com/).

---

## 🚀 Applications

### 1. Text-to-Math Solver (`maths.py`)
A fast, robust math chatbot that solves equations and answers math word problems.
* **Instant Evaluation:** Direct arithmetic expressions (e.g. `2 + 34 * 4`) bypass LLM generation entirely and evaluate instantly using python's `numexpr` library for 100% accuracy and zero latency.
* **Agent Fallback:** Complex questions use a ReAct agent equipped with a Reasoning tool and Wikipedia access to query the web and logically break down word problems.

#### Run the Math Solver:
```bash
streamlit run maths.py
```

### 2. Chat with SQL Database (`app.py`)
Allows you to query data from structured databases without writing SQL commands.
* **Dialect support:** Toggle easily between a local SQLite3 database and a remote MySQL database directly in the interface.
* **Local Database Setup:** Run `sqlite.py` first to generate a sample student table (`agents.db`) to test the agent immediately.

#### Initialize Local DB:
```bash
python sqlite.py
```

#### Run the SQL Assistant:
```bash
streamlit run app.py
```

---

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/dharmender12/text-to-math-solver-groq.git
   cd text-to-math-solver-groq
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment:**
   Create your `.env` file as described in the API Key Setup section above.
