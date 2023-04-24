import streamlit as st
from datetime import datetime
import base64

TEMPLATE = """from langchain.prompts.prompt import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import ChatVectorDBChain

import os
import pickle
from fastapi import FastAPI, Request

os.environ["OPENAI_API_KEY"] = "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"

model = '{model}'
temperature = {temperature}
template = '''{template}'''

_template = '''Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question.
you can assume the question is about the document.

Chat History:
{chat_history}
Follow Up Input: {question}
Standalone question:'''

CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(_template)

QA_PROMPT = PromptTemplate(template=template, input_variables=['question', 'context'])

with open("vectorstore.pkl", "rb") as f:
   vectorstore = pickle.load(f)

app = FastAPI()
llm = OpenAI(model=model, temperature=temperature)
qa_chain = ChatVectorDBChain.from_llm(
        llm,
        vectorstore,
        qa_prompt=QA_PROMPT,
        condense_question_prompt=CONDENSE_QUESTION_PROMPT,
    )

@app.post("/api")
async def get_answer(request: Request):
    body = await request.json()
    question = body.get("question")
    chat_history = body.get("chat_history", [])
    result = qa_chain({"question": question, "chat_history": chat_history})
    chat_history.append((question, result["answer"]))
    return {"answer": result["answer"]}
"""

def save_function(model, temperature, template):
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"api_{model}_{current_time}.py"
    script = TEMPLATE.format(model=model, temperature=temperature, template=template, chat_history="{chat_history}", question="{question}")
    with open(filename, "w") as f:
        f.write(script)
    st.success(f"Custom API created as {filename}")
    with open(f"{filename}", 'rb') as f:
        bytes = f.read()
    b64 = base64.b64encode(bytes).decode()
    href = f'<a href="data:file/{filename};base64,{b64}" download="{filename}">Download custom API</a>'
    st.markdown(href, unsafe_allow_html=True)
