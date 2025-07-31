# 🔍 QueryGPT — Chat with Your SQLite Database using LLMs

QueryGPT is a Streamlit-based AI assistant that allows you to interact with your SQLite database using natural language. It leverages LLMs like **Ollama (Mistral)** or **OpenAI GPT-4** via LangChain to translate your questions into SQL queries and display meaningful answers.

---

## 📦 Features

- 🔗 Connects to a local SQLite database (`products.db`)
- 🤖 Uses either:
  - `Ollama` (default) — lightweight LLM via local inference
  - `OpenAI GPT-4` — via API key
- 🧠 Translates natural language into SQL using LangChain's SQL agent
- 📊 Automatically renders query results in table format (if applicable)
- 🧾 Handles plain-text responses and extracts structured data when possible

---

## 🚀 How It Works

1. You ask a question (e.g., _"Show me the top 5 most expensive products"_).
2. The app uses a selected LLM to generate a SQL query.
3. If it's a `SELECT` query:
   - Executes it on `products.db`
   - Displays results in a table
4. If not, it tries to parse and display the response cleanly.

---

## 🧰 Tech Stack

- **Python**
- **Streamlit**
- **LangChain**
- **Ollama / OpenAI**
- **SQLite**
- **Pandas**

---

## ⚙️ Setup Instructions

1. **Clone the Repository**

```bash
git clone https://github.com/your-username/query-gpt.git
cd query-gpt