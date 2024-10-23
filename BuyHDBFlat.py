import streamlit as st
from langchain_community.vectorstores import Chroma
from helper_function.Credentials import embeddings_model, llm
# from RAGFunctions import prepare_documents, setup_vector_db, get_llm_response_with_prompt, load_scraped_data
from RAGFunctions_Janice import prepare_documents, setup_vector_db, get_llm_response_with_prompt, load_scraped_data
import hmac
import openai  
from helper_function.stpassword import check_password  

if not check_password():  
    st.stop()
    
# Create an expander for the disclaimer
with st.expander("IMPORTANT NOTICE: Click to expand/disclose", expanded=False):
    st.write("""
    This web application is a prototype developed for educational purposes only. 
    The information provided here is NOT intended for real-world usage and should not be relied upon for making any decisions, 
    especially those related to financial, legal, or healthcare matters.

    Furthermore, please be aware that the LLM may generate inaccurate or incorrect information. 
    You assume full responsibility for how you use any generated output.

    Always consult with qualified professionals for accurate and personalized advice.
    """)


# Show a spinner until the page is fully loaded
with st.spinner('Loading the application, we ask for your patience...'):
    
    # Streamlit app title and introduction
    st.title('🏠 Ask any policy related questions regarding buying a HDB or EC 🏠')
    st.write('🏘️🏡🏚️ This is applicable to Executive Condos (ECs), new flats, resale flats 🏚️🏡🏘️')
    st.write('💰 You can ask about loan options and HDB Flat Eligibility too 💰')
    st.write('Examples include: What is the income ceiling to buy an EC/ I am single, can i buy a HDB?')

    # Step 1: Load the scraped data from the JSON file with a spinner
    @st.cache_data(show_spinner=False)
    def load_scraped_data_cache():
        return load_scraped_data('scraped_data_buyingflat.json')

    # Step 2: Prepare documents and set up vector database
    @st.cache_resource(show_spinner=False)
    def load_vector_db(scraped_data):
        splitted_documents_as_docs = prepare_documents(scraped_data)
        vectordb = setup_vector_db(splitted_documents_as_docs)
        return vectordb

    # Load the scraped data and vector database
    scraped_data = load_scraped_data_cache()
    vectordb = load_vector_db(scraped_data)

# Step 3: Input question and submit button
question = st.text_input("Enter your question here:")
button_clicked = st.button("Get Answer")

# Step 4: Handle user interaction and response generation
if question or button_clicked:
    with st.spinner(f'Processing your question: "{question}"...'):
        response = get_llm_response_with_prompt(vectordb, question)

        # Display the response
        st.text_area("Answer", value=response, height=200)
