from langchain import PromptTemplate, LLMChain
from langchain.llms import OpenAI
import openai
import os
os.environ["OPENAI_API_KEY"] = "API-KEY"

template = """Does the following agreement follow the company policy fully? 
give a detailed answer with a through analysis. 
if there are any conflicting points at all, quote them.

Policy:
{policy_text}

Agreement:
{agreement_text}

Answer in Markdown:"""

prompt = PromptTemplate(template=template, input_variables=["policy_text", "agreement_text"])

llm = OpenAI(temperature=0)

llm_chain = LLMChain(prompt=prompt, llm=llm)

def check_agreement(policy_text, agreement_text):
    response = llm_chain.run(policy_text=policy_text, agreement_text=agreement_text)
    return response
