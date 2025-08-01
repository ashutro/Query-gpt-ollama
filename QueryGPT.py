import streamlit as st
from langchain_community.llms import Ollama
from langchain.chat_models import ChatOpenAI
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
import pandas as pd
import re
import os
import sqlite3

# === CONFIGURATION ===
USE_OPENAI = False  # Set to True to use OpenAI GPT-4, False to use Ollama
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OLLAMA_MODEL = "mistral"
OPENAI_MODEL = "gpt-4"

# === DB SETUP ===
db = SQLDatabase.from_uri("sqlite:///products.db")

# === LLM SELECTION ===
if USE_OPENAI:
    llm = ChatOpenAI(model=OPENAI_MODEL, temperature=0, api_key=OPENAI_API_KEY)
else:
    llm = Ollama(model=OLLAMA_MODEL)

# === SQL Agent Setup ===
agent = create_sql_agent(
    llm=llm,
    toolkit=SQLDatabaseToolkit(db=db, llm=llm),
    verbose=False,
    handle_parsing_errors=True
)

# === Streamlit Frontend ===
st.set_page_config(page_title="QueryGPT - SQLite Agent", page_icon="🔍")
st.title("🔍 QueryGPT: Chat with Your Product DB")
st.markdown("Ask a question about your database (e.g. top 3 expensive products):")

user_input = st.text_input("Your question")

if st.button("Ask") and user_input:
    with st.spinner("Thinking..."):
        try:
            response = agent.run(user_input)

            if "SELECT" in response.upper():
                try:
                    conn = sqlite3.connect("products.db")
                    cursor = conn.cursor()
                    sql_query = response.strip().strip('`')
                    st.code(sql_query, language="sql")
                    if not sql_query.lower().startswith("select"):
                        raise ValueError("Only SELECT queries are allowed.")
                    cursor.execute(sql_query)
                    rows = cursor.fetchall()
                    columns = [desc[0] for desc in cursor.description]
                    conn.close()

                    df = pd.DataFrame(rows, columns=columns)
                    st.success("Result from Query:")
                    st.dataframe(df)

                except Exception as sql_error:
                    st.error(f"⚠️ Query Execution Failed: {sql_error}")
            else:
                price_matches = re.findall(r'([A-Za-z0-9\s]+?)\s+with\s+a\s+price\s+of\s+\$?(\d+\.\d+)', response)
                if price_matches:
                    df = pd.DataFrame(price_matches, columns=["Product", "Price"])
                    df["Price"] = df["Price"].astype(float)
                    st.success("Answer in Table Format:")
                    st.dataframe(df)
                else:
                    st.success("Answer:")
                    st.write(response)

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")