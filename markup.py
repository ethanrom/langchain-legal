def legal_ai_tools_demo():
    return """
    <h3 style='text-align: center;'>About</h3>
            
    <ul>
    <li><b>Ingest multiple documents into a vector store:</b> <span style="color:lightgray;">This demo can take multiple documents and store them permanently in a vector store, allowing for efficient and easy access to the data.</span></li>
    <li><b>Chat with the vector store:</b> <span style="color:lightgray;">Chatbot can interact with the vector store, using its memory and predefined identity to facilitate more effective and personalized communication.</span></li>
    <li><b>Question answering with source retrieval:</b> <span style="color:lightgray;">This demo can answer questions by retrieving relevant information from a variety of sources, providing accurate and comprehensive answers.</span></li>
    <li><b>Compare wording similarities of multiple legal documents:</b> <span style="color:lightgray;">This demo can compare the wording of multiple legal documents, highlighting similarities and differences to help identify potential issues or discrepancies.</span></li>
    <li><b>Extract key information from legal documents:</b> <span style="color:lightgray;">This demo can analyze legal documents and extract key information, making it easier to understand the content and identify important details.</span></li>
    <li><b>Summarize long legal documents into everyday language:</b> <span style="color:lightgray;">This demo can take complex legal documents and summarize them into clear and concise language, making the information more accessible and easier to understand.</span></li>
    <li><b>Compare multiple documents to identify policy adherence:</b> <span style="color:lightgray;">This demo can compare multiple documents, such as a company policy and an agreement, to determine if the agreement follows the policy and identify any potential conflicts or discrepancies.</span></li>
    </ul>          
    """

def legal_ai_tools_demo_todo():
    return """
    <div style='text-align: center;'>
    <h3 style='text-align: center;'>todo / tofix </h3>
    <p> index loads at the statup. changes to vectstore does not apply until restart, summerize, chatbot reaches token limits. Semantic Similarity </p>
            
    </div>
    """

def vecstore_into():
    return "Effortlessly upload one or several documents and have them ingested into a durable vectorstore for rapid access. system utilizes **openai** embeddings and **faiss** vectorstore by default, but can be tailored to meet specific needs." 

def chatbot_intro():
    return """chatbot designed with a contextual approach and utilizes the vector store as its knowledge base. It possesses a memory and a distinct personality. Scope is limited to answering queries pertaining only to legal documents.
    <p> You can customize the chatbot to your likening on the go using the settings on the left, and save the custom API script once done. </P>
    """

def chatbotapi_intro():
    return """After configuring the chatbot's custom settings to your satisfaction, simply click the "Generate API" button to create a downloadable Python script for setting up a FastAPI server with an API endpoint."""

def retrieval_intro():
    return """This feature enables users to perform question answering across an index of multiple documents and receive the corresponding **source documents** as results. This approach is generally more **efficient** and **accurate** than the standard vectordb chat function."""