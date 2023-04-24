import PyPDF2
from langchain import OpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document

def summarize_pdf2(pdf_path, summary_length=200):
    pdf_file = open(pdf_path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ''
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    chunk_size = 1000
    text_chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    docs = [Document(page_content=chunk) for chunk in text_chunks]
    llm = OpenAI(temperature=0)
    chain = load_summarize_chain(llm, chain_type="map_reduce")
    summary = ''
    for doc in docs:
        doc_summary = chain.run([doc])[0].get_summary(summary_length)
        summary += doc_summary + ' '
    return summary

def summarize_pdf(pdf_path):
    return "todo"
