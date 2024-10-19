#lcCredentials mean LangChain credentials
import os
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
import openai
import streamlit as st

openai.api_key = st.secrets["OPENAI_API_KEY"]

# embedding model that we will use for the session
embeddings_model = OpenAIEmbeddings(model='text-embedding-3-small')

# llm to be used in RAG pipeplines in this notebook
llm = ChatOpenAI(model='gpt-4o-mini', temperature=0, seed=42)

print('Setup completed')