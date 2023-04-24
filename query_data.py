from langchain.prompts.prompt import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import ChatVectorDBChain

def get_chain(model, vectorstore, temperature, template):
    _template = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question.
    you can assume the question is about the document.

    Chat History:
    {chat_history}
    Follow Up Input: {question}
    Standalone question:"""
    CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(_template)

    QA_PROMPT = PromptTemplate(template=template, input_variables=["question", "context"])

    llm = OpenAI(model=model, temperature=temperature)
    qa_chain = ChatVectorDBChain.from_llm(
        llm,
        vectorstore,
        qa_prompt=QA_PROMPT,
        condense_question_prompt=CONDENSE_QUESTION_PROMPT,
    )
    return qa_chain
