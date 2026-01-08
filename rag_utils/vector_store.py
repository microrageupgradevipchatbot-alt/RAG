
import gc

import shutil
from langchain_community.document_loaders import TextLoader,UnstructuredMarkdownLoader
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from .setup import (DB_DIR,DOC_DIR,get_gemini_llm,get_gemini_embeddings,logger)
from .prompt import build_prompt, build_prompt_v7,build_prompt_v3,build_prompt_v4,build_prompt_v5,build_prompt_v6
from pathlib import Path

embeddings= get_gemini_embeddings()

class DatasetEmptyError(Exception):
    pass
def load_documents(folder_path):
    documents = []
    
    # Check if folder exists and has files
    if not os.path.exists(folder_path):
        logger.warning(f"⚠️ Documents folder does not exist: {folder_path}")
        raise DatasetEmptyError(f"No documents folder found: {folder_path}")

    files = os.listdir(folder_path)
    if not files:
        logger.warning(f"⚠️ No files found in documents folder: {folder_path}")
        raise DatasetEmptyError(f"No files found in documents folder: {folder_path}")

    
    for filename in files:
        file_path = os.path.join(folder_path, filename)
        logger.info(f"full filename {file_path}")
        
        if filename.endswith('.md'):
            loader = UnstructuredMarkdownLoader(file_path)
            logger.info(f"loaded {filename}")
        elif filename.endswith('.txt'):
            loader = TextLoader(file_path)
            logger.info(f"loaded {filename}")
        else:
            logger.warning(f"unsupported file type : {filename}")
            continue

        documents.extend(loader.load())
    
    return documents

def create_chunks(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=3500,
        chunk_overlap=450
        )
    docs = text_splitter.split_documents(documents)
    logger.info(f"Created {len(docs)} chunks from {len(documents)} documents.")
    return docs

def create_chroma_db(text_chunks):
  '''Index Documents (store embeddings) in vector store'''

  collection_name = "upgrade_collection"
  logger.info(f"✅Indexing {len(text_chunks)} chunks into Chroma vector store '{collection_name}'...")
  chromaDB =  Chroma.from_documents(
      collection_name=collection_name,
      documents=text_chunks,
      embedding=embeddings,
      persist_directory=DB_DIR
  )
  logger.info("✅Chroma vector store created successfully.")
  return chromaDB



#-------
def load_vector_store():
    """Create the Chroma vector store if not present, else load it."""

    chromaDB = Chroma(
        collection_name="upgrade_collection",
        embedding_function=embeddings,
        persist_directory=DB_DIR
    )
    logger.info("✅Chroma vector store loaded from disk.")

    return chromaDB

def create_vector_store():
    """Create the Chroma vector store if not present, else load it."""
  
    documents = load_documents(DOC_DIR)
    text_chunks = create_chunks(documents)
    chromaDB = create_chroma_db(text_chunks)

    return chromaDB

def checking_vector_store():
    '''Check if vector store exists, if not create it'''
    
    if (DB_DIR / "chroma.sqlite3").exists():
        logger.info("✅ Existing vector store found. Loading it...")
        chromaDB = load_vector_store()
    else:
        logger.info("🛑 No existing vector store found. Creating a new one...")
        chromaDB = create_vector_store()    

    return chromaDB

def get_gemini_response(query,context, chat_history):
    #api_key = os.getenv("GOOGLE_API_KEY")
    prompt = build_prompt_v3(query, context, chat_history)
    llm = get_gemini_llm()
    return llm.invoke(prompt).content

def get_gemini_response_v2(query,context, chat_history):
    #api_key = os.getenv("GOOGLE_API_KEY")
    prompt = build_prompt_v4(query, context, chat_history)
    llm = get_gemini_llm()
    return llm.invoke(prompt).content

def get_gemini_response_v3(query,context, chat_history):
    #api_key = os.getenv("GOOGLE_API_KEY")
    logger.info(f"Chat history in vector_store.py: {chat_history}")
    prompt = build_prompt_v5(query, context, chat_history)
    llm = get_gemini_llm()
    return llm.invoke(prompt).content

def get_gemini_response_v4(query,context, chat_history):
    #api_key = os.getenv("GOOGLE_API_KEY")
    logger.info(f"Chat history in vector_store.py: {chat_history}")
    prompt = build_prompt_v6(query, context, chat_history)
    llm = get_gemini_llm()
    return llm.invoke(prompt).content

def get_gemini_response_v5(query,context, chat_history):
    #api_key = os.getenv("GOOGLE_API_KEY")
    logger.info(f"Chat history in vector_store.py: {chat_history}")
    prompt = build_prompt_v7(query, context, chat_history)
    llm = get_gemini_llm()
    return llm.invoke(prompt).content

#---- New functions for button operations ----



