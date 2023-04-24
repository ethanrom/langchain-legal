import os
import time
import pickle
import spacy
from spacy import displacy
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter

import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_chat import message

from ingest_docs import ingest_docs, ingest_new_docs
from query_data import get_chain
from retrieval_qa import qa_retrive_chain
from similarity import calculate_textual_similarity, calculate_linguistic_similarity, calculate_semantic_similarity, highlight_text_differences
from extract_text import extract_info
from adherance_check import check_agreement
from summarize_doc import summarize_pdf
from default_text import default_text1, default_text2, default_text3, default_text4, default_text5, default_template
from markup import legal_ai_tools_demo, legal_ai_tools_demo_todo, vecstore_into, chatbot_intro, chatbotapi_intro, retrieval_intro
from help_text import HELP_TEXT
from save import save_function


nlp = spacy.load("en_core_web_sm")
os.environ["OPENAI_API_KEY"] = "API-KEY"

def tab1():
    st.header("Legal AI Tools")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("image.jpg", use_column_width=True)
    with col2:
        st.markdown(legal_ai_tools_demo(), unsafe_allow_html=True)
    st.markdown(legal_ai_tools_demo_todo(),unsafe_allow_html=True)   

def tab2():
    st.header("Manage vectorstore")
    st.markdown(vecstore_into())
    col1, col2 = st.columns(2)    
    with col1:
        st.subheader("List of Files")
        files = os.listdir("docs")
        if not files:
            st.write("No files found.")
        for file in files:
            file_col, delete_col = st.columns([8, 1])
            file_col.write("- " + file)
            delete_button = delete_col.button("Delete", key=f"delete_{file}")
            if delete_button:
                os.remove(os.path.join("docs", file))
                st.experimental_rerun()

    with col2:
        st.subheader("Upload Files")
        uploaded_files = st.file_uploader("Select files", type=["pdf"], accept_multiple_files=True)
        if uploaded_files:
            for uploaded_file in uploaded_files:
                file_exists = os.path.isfile(os.path.join("docs", uploaded_file.name))
                if not file_exists:
                    with open(os.path.join("new_docs", uploaded_file.name), "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    st.success(f"File '{uploaded_file.name}' uploaded.")
                else:
                    st.warning(f"File '{uploaded_file.name}' already exists.")
            
    st.write("")
    with st.expander("Advanced"):
        st.subheader("Advanced Options")
        col1, col2 = st.columns([2, 1])

        with col2:
            vectorstore_path = "vectorstore.pkl"
            vectorstore_size = os.path.getsize(vectorstore_path)
            vectorstore_last_updated = os.path.getmtime(vectorstore_path)
            vectorstore_last_updated_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(vectorstore_last_updated))
            st.subheader("Index Info")
            st.write(f"Index size: {vectorstore_size} bytes")
            st.write(f"Index Last updated: {vectorstore_last_updated_str}")
    
        with col1:
            text_splitter_cls = st.radio("Select text splitter", options=[RecursiveCharacterTextSplitter, CharacterTextSplitter], help=HELP_TEXT["Select text splitter"])
            if text_splitter_cls == CharacterTextSplitter:
                chunk_size = st.slider("Chunk size", min_value=100, max_value=10000, step=100, value=1000, help=HELP_TEXT["Chunk size"])
                chunk_overlap = st.slider("Chunk overlap", min_value=0, max_value=500, step=10, value=0, help=HELP_TEXT["Chunk overlap"])
            else:
                chunk_size = None
                chunk_overlap = None
        
            if st.button("Reindex all"):
                st.spinner("Ingesting documents...")
                ingest_docs(text_splitter_cls, chunk_size, chunk_overlap)
                st.success("Documents ingested.")

    if st.button("Ingest New Documents"):
        st.spinner("Ingesting documents...")
        ingest_new_docs(text_splitter_cls, chunk_size, chunk_overlap)
        st.success("Documents ingested.")

if "generated" not in st.session_state:
    st.session_state["generated"] = []

if "past" not in st.session_state:
    st.session_state["past"] = []

def tab3():
    col1, col2 = st.columns([3, 1])
    with col2:
        with st.expander("Model Options"):
            model_list = ["text-davinci-003", "text-davinci-002", "gpt-3.5-turbo", "gpt-3.5-turbo-0301"]
            selected_model = st.selectbox("Select a model", model_list)
            temperature = st.slider("LLM Temperature", 0.0, 1.0, 0.0, 0.1, help=HELP_TEXT["LLM Temperature"])
            max_tokens = st.slider("Max Tokens", 0, 2048, 2048, 100, help=HELP_TEXT["Max Tokens"]) #removed since varies for different models
            frequency_penalty = st.slider("Frequency Penalty", -2.0, 2.0, 0.0, 0.1, help=HELP_TEXT["Frequency Penalty"]) #todo
            presence_penalty = st.slider("Presence Penalty", -2.0, 2.0, 0.0, 0.1, help=HELP_TEXT["Presence Penalty"]) #todo
        with st.expander("AI Options"):
            template = st.text_area("AI Prompt", height=500, value=default_template)
        with st.expander("Create API"):
            st.markdown(chatbotapi_intro())
            save_button = st.button("Generate API")
            if save_button:
                save_function(selected_model, temperature, template)
        with st.expander("Create streamlit demo"):
            stcreate_button = st.button("Generate streamlit app")
    
    with col1:
        with open("vectorstore.pkl", "rb") as f:
            vectorstore = pickle.load(f)
        qa_chain = get_chain(selected_model, vectorstore, temperature, template)
        chat_history = []
        if "past" not in st.session_state:
            st.session_state.past = []
        if "generated" not in st.session_state:
            st.session_state.generated = []
            
        st.header("Contextual chatbot")
        st.markdown(chatbot_intro(), unsafe_allow_html=True)
        question = st.text_input("Ask:")
        submit_button = st.button("Chat")
        if submit_button:
            with st.spinner('Searching for answer...'):
                result = qa_chain({"question": question, "chat_history": chat_history})
                chat_history.append((question, result["answer"]))

                st.session_state.past.append(question)
                st.session_state.generated.append(result)

        if st.session_state["generated"]:
            for i in range(len(st.session_state["generated"]) - 1, -1, -1):
                message(
                    st.session_state["generated"][i]["answer"],
                    key=str(i)
                )
                message(
                    st.session_state["past"][i],
                    is_user=True,
                    key=str(i) + "_user"
                )

        
def tab4():
    st.header("Retrieval Question Answering")
    st.markdown(retrieval_intro())

    query = st.text_input("Question:")
    submit_button = st.button("Submit")
    if submit_button:
        with st.spinner('Searching for answer...'):
            result = qa_retrive_chain({"query": query})
        st.text("answer:")
        st.write(result["result"])
        st.text("source")
        st.write(result["source_documents"])

def tab5():
    st.header("Similarity comparison")
    st.markdown('This can highlight the :green[similarities] and :red[differences] in **wording** across two legal documents.')
    
    text1 = st.text_area("Enter Text 1", height=200, value=default_text1)
    text2 = st.text_area("Enter Text 2", height=200, value=default_text2)

    if st.button("Compare Similarity"):
        textual_similarity = calculate_textual_similarity(text1, text2)
        linguistic_similarity = calculate_linguistic_similarity(text1, text2)
        semantic_similarity = calculate_semantic_similarity(text1, text2)
        highlighted_text1, highlighted_text2 = highlight_text_differences(text1, text2)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(highlighted_text1, unsafe_allow_html=True)
        with col2:
            st.markdown(highlighted_text2, unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader('Textual Similarity')
            st.markdown('measures the similarity based on the *wording* of the two texts.')    
            st.write("Textual Similarity: <span style='font-size: 2em;'>{:.2f}%</span>".format(textual_similarity), unsafe_allow_html=True)

        with col2:
            st.subheader('Linguistic Similarity')
            st.markdown('measures the similarity based on the *linguistic features* of the two texts.')
            st.write("Linguistic Similarity: <span style='font-size: 2em;'>{:.2f}%</span>".format(linguistic_similarity), unsafe_allow_html=True)
        
        with col3:
            st.subheader('Semantic Similarity')
            st.markdown('measures the similarity based on the *meaning* of the two texts.')
            st.write("Semantic Similarity: <span style='font-size: 2em;'>{:.2f}%</span>".format(semantic_similarity), unsafe_allow_html=True)

def tab6():
    st.header("Extract Info")
    st.markdown('Extract key information from legal documents such as dates, names, address, etc.')
  
    input_text = st.text_area("Enter your text here:", height=200, value=default_text3)
    if st.button("Extract Information"):
        info = extract_info(input_text)
        highlighted_text = displacy.render(nlp(input_text), style="ent", options={"ents": [ent[3] for ent in info["names"]+info["addresses"]+info["dates"]], "colors": {"PERSON": "#66c2a5", "ADDRESS": "#fc8d62", "DATE": "#8da0cb"}})
        
        st.markdown(highlighted_text, unsafe_allow_html=True)
        
        st.write("### Extracted Information")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.write("#### Names")        
            for name in info["names"]:
                st.write("- {}: {}".format(name[0], name[3]))
        with col2:
            st.write("#### Addresses")        
            for address in info["addresses"]:
                st.write("- {}: {}".format(address[0], address[3]))
        
        with col3:
            st.write("#### Dates")
            for date in info["dates"]:
                st.write("- {}: {}".format(date[0], date[3]))

def tab7():
    st.header("Summerize")
    st.markdown('Get an overview of any document in straightforward, everyday language.')
    pdf_files = [f for f in os.listdir("docs") if f.endswith(".pdf")]
    selected_file = st.selectbox("Select a PDF file", pdf_files)
    if st.button("Summarize"): #todo
        pdf_path = os.path.join("docs", selected_file)
        summary = summarize_pdf(pdf_path)
        st.write(summary)

def tab8():
    st.header("Policy checker")
    st.markdown("Checks if an Legal agreement follows the company policy")

    policy_text = st.text_area("Enter company policy text:", height=200, value=default_text4)
    agreement_text = st.text_area("Enter legal agreement text:", height=200, value=default_text5)

    col1, col2 = st.columns([3, 1])
    with col1:

        if st.button("Check agreement"):
            with st.spinner('checking the document...'):
                result = check_agreement(policy_text, agreement_text)
            st.write(result)
    
    with col2:
        if st.button("Rewrite agreement"):
            st.write("todo")
    
def main():
    st.set_page_config(page_title="Legal Tools Demo", page_icon=":memo:", layout="wide")
    tabs = ["Intro", "Index", "Chat", "Retrieve", "Similarity", "Extract", "Summerize", "Adherence"]
    
    with st.sidebar:

        current_tab = option_menu("Select a Tab", tabs, menu_icon="cast")
    
    tab_functions = {
    "Intro": tab1,
    "Index": tab2,
    "Chat": tab3,
    "Retrieve": tab4,
    "Similarity": tab5,
    "Extract": tab6,
    "Summerize": tab7,
    "Adherence": tab8,
    }

    if current_tab in tab_functions:
        tab_functions[current_tab]()

if __name__ == "__main__":
    main()
