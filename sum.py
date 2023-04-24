import streamlit as st
from langchain import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from langchain.chains.summarize import load_summarize_chain
import os
from langchain.document_loaders import PyPDFLoader

os.environ["OPENAI_API_KEY"] = "API-KEY"

llm = OpenAI(temperature=0)
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)


def generate_summary():
    loader = PyPDFLoader("docs/INLAND REVENUE (AMENDMENT) ACT, No. 45 OF 2022.pdf")
    pages = loader.load()
    texts = text_splitter.split_text(pages)
    docs = [Document(page_content=t) for t in texts[:3]]
    chain = load_summarize_chain(llm, chain_type="map_reduce")
    summary = chain.run(docs)
    return summary


st.title("Text Summarization")
if st.button("submit"):
    summary = generate_summary()
    st.header("Summary")
    st.write(summary)
