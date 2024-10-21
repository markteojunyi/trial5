import json
import logging
from helper_function.tokencounting import count_tokens
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from helper_function.Credentials import embeddings_model, llm
from langchain.chains import LLMChain
from langchain.schema import Document
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain

__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load the scraped data with error handling
def load_scraped_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as json_file:
            scraped_data = json.load(json_file)
        return scraped_data
    except FileNotFoundError:
        logger.error("File not found!")
        return {}
    except json.JSONDecodeError:
        logger.error("Error decoding the JSON file!")
        return {}

# Step 1: Function to split documents
def prepare_documents(scraped_data):
    all_document_texts = []
    
    # Extract all document contents into a list
    for key, docs in scraped_data.items():
        for doc in docs:
            content = doc.get("content")
            if isinstance(content, str):
                all_document_texts.append(content)
            else:
                logger.info(f"Skipped a document from {key} due to non-string content.")
    
    # Initialize text splitter
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1100, chunk_overlap=10, length_function=count_tokens)
    
    # Split each document's content
    splitted_documents = [text_splitter.split_text(doc_content) for doc_content in all_document_texts]
    flat_splitted_docs = [doc for sublist in splitted_documents for doc in sublist]
    
    logger.info(f"Number of documents after splitting: {len(flat_splitted_docs)}")
    
    # Create Document objects for each split text
    splitted_documents_as_docs = [Document(page_content=doc_content) for doc_content in flat_splitted_docs]
    
    return splitted_documents_as_docs

# Step 2: Function to set up the vector database
def setup_vector_db(documents):
    vectordb = Chroma.from_documents(
        documents=documents,  
        embedding=embeddings_model,
        collection_name="naive_splitter",
        persist_directory="./vector_db"
    )
    vectordb.persist()
    return vectordb

# Step 3: Function to create LLM response with a custom prompt
def get_llm_response_with_prompt(vectordb, question):
    # Define a custom prompt template
    custom_prompt = """
    You are an expert about all Housing Development Board matters. Based on the question asked, give the best answer you can.
    If you do not know the answer, say "I am still learning and am unable to give an answer at the moment, please try asking another question."

    Question: {question}

    Answer in a way that even a beginner would understand, and provide additional insights if relevant.
    """

    # Initialize a PromptTemplate
    prompt_template = PromptTemplate(
        input_variables=["question"],
        template=custom_prompt
    )

    # Create a simple LLMChain using the custom prompt
    llm_chain = LLMChain(
        llm=llm,
        prompt=prompt_template
    )

    # Create the full QA chain with the vector retriever and custom LLM chain
    qa_chain = load_qa_chain(llm, chain_type="stuff")  

    # Retrieve relevant documents using vectordb
    retriever = vectordb.as_retriever()
    relevant_docs = retriever.get_relevant_documents(question)

    # Run the custom LLM chain with the prompt and question
    response = qa_chain.run(input_documents=relevant_docs, question=question)

    return response
