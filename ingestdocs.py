import pickle
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain.vectorstores.faiss import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import TextLoader, DirectoryLoader, PyPDFLoader
import shutil
import os

def ingest_docs(text_splitter_cls, chunk_size=None, chunk_overlap=None):
    loader = DirectoryLoader('docs', glob="*.pdf", loader_cls=PyPDFLoader)
    docs = loader.load()
    if text_splitter_cls == RecursiveCharacterTextSplitter:
        text_splitter = RecursiveCharacterTextSplitter()
    elif text_splitter_cls == CharacterTextSplitter:
        text_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    else:
        raise ValueError("Invalid text splitter class")
    documents = text_splitter.split_documents(docs)
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(documents, embeddings)
    with open("vectorstore.pkl", "wb") as f:
        pickle.dump(vectorstore, f)

def ingest_new_docs(text_splitter_cls, chunk_size=None, chunk_overlap=None):
    with open("vectorstore.pkl", "rb") as f:
        vectorstore = pickle.load(f)
    loader = DirectoryLoader('new_docs', glob="*.pdf", loader_cls=PyPDFLoader)
    new_docs = loader.load()

    if text_splitter_cls == RecursiveCharacterTextSplitter:
        text_splitter = RecursiveCharacterTextSplitter()
    elif text_splitter_cls == CharacterTextSplitter:
        text_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    else:
        raise ValueError("Invalid text splitter class")
    new_documents = text_splitter.split_documents(new_docs)
    vectorstore.add_documents(new_documents)

    with open("vectorstore.pkl", "wb") as f:
        pickle.dump(vectorstore, f)

    # Move files from new_docs to docs directory
    for filename in os.listdir("new_docs"):
        if filename.endswith(".pdf"):
            shutil.move(os.path.join("new_docs", filename), os.path.join("docs", filename))