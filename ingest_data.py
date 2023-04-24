from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import ReadTheDocsLoader
from langchain.vectorstores.faiss import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import TextLoader, DirectoryLoader

import pickle
import os
os.environ["OPENAI_API_KEY"] = "API-KEY"

loader = DirectoryLoader('docs', glob="*.txt", loader_cls=TextLoader)
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter()
documents = text_splitter.split_documents(docs)

embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(documents, embeddings)

with open("vectorstore.pkl", "wb") as f:
    pickle.dump(vectorstore, f)
