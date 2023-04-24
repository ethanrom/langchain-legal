from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
import pickle
import os
os.environ["OPENAI_API_KEY"] = "API-KEY"

with open("vectorstore.pkl", "rb") as f:
        vectorstore = pickle.load(f)

prompt_template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer. Generate a well written detailed answer.

{context}

Question: {question}
Answer:"""
PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)

chain_type_kwargs = {"prompt": PROMPT}
qa_retrive_chain = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=vectorstore.as_retriever(), chain_type_kwargs=chain_type_kwargs, return_source_documents=True)
