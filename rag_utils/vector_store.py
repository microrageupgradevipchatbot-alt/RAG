import os
from langchain_community.document_loaders import TextLoader, UnstructuredMarkdownLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from .setup import (DB_DIR, DOC_DIR, get_gemini_llm, get_gemini_embeddings, logger)
from .prompt import build_prompt, build_prompt_v7, build_prompt_v3, build_prompt_v4, build_prompt_v5, build_prompt_v6

embeddings = get_gemini_embeddings()

FAISS_INDEX_DIR = str(DB_DIR / "faiss_index")

class DatasetEmptyError(Exception):
    pass

def load_documents(folder_path):
    documents = []

    if not os.path.exists(folder_path):
        logger.warning(f"⚠️ Documents folder does not exist: {folder_path}")
        raise DatasetEmptyError(f"No documents folder found: {folder_path}")

    files = os.listdir(folder_path)
    if not files:
        logger.warning(f"⚠️ No files found in documents folder: {folder_path}")
        raise DatasetEmptyError(f"No files found in documents folder: {folder_path}")

    for filename in files:
        file_path = os.path.join(folder_path, filename)
        logger.info(f"🚩full filename {file_path}")

        if filename.endswith('.md'):
            loader = UnstructuredMarkdownLoader(file_path)
            logger.info(f"📄 loaded {filename}")
        elif filename.endswith('.txt'):
            loader = TextLoader(file_path)
            logger.info(f"📄 loaded {filename}")
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

def create_faiss_db(text_chunks):
    '''Index Documents (store embeddings) in FAISS vector store'''
    logger.info(f"✅ Indexing {len(text_chunks)} chunks into FAISS vector store...")
    try:
        faiss_db = FAISS.from_documents(text_chunks, embeddings)
        faiss_db.save_local(FAISS_INDEX_DIR)
        logger.info("✅ FAISS vector store created and saved successfully.")
        return faiss_db
    except Exception as e:
        logger.error(f"❌ Error creating FAISS vector store: {type(e).__name__}: {e}", exc_info=True)
        print(f"❌ Error creating FAISS vector store: {type(e).__name__}: {e}")
        raise

def load_faiss_db():
    '''Load FAISS vector store from disk'''
    try:
        faiss_db = FAISS.load_local(FAISS_INDEX_DIR, embeddings, allow_dangerous_deserialization=True)
        logger.info("✅ FAISS vector store loaded from disk.")
        return faiss_db
    except Exception as e:
        logger.error(f"❌ Error loading FAISS vector store: {type(e).__name__}: {e}", exc_info=True)
        print(f"❌ Error loading FAISS vector store: {type(e).__name__}: {e}")
        raise

def checking_vector_store():
    '''Check if FAISS vector store exists, if not create it'''
    if (DB_DIR / "faiss_index").exists():
        logger.info("✅ Existing FAISS vector store found. Loading it...")
        return load_faiss_db()
    else:
        logger.info("🛑 No existing FAISS vector store found. Creating a new one...")
        documents = load_documents(DOC_DIR)
        text_chunks = create_chunks(documents)
        return create_faiss_db(text_chunks)

def get_gemini_response(query, context, chat_history):
    prompt = build_prompt_v3(query, context, chat_history)
    llm = get_gemini_llm()
    return llm.invoke(prompt).content

def get_gemini_response_v2(query, context, chat_history):
    prompt = build_prompt_v4(query, context, chat_history)
    llm = get_gemini_llm()
    return llm.invoke(prompt).content

def get_gemini_response_v3(query, context, chat_history):
    logger.info(f"Chat history in vector_store.py: {chat_history}")
    prompt = build_prompt_v5(query, context, chat_history)
    llm = get_gemini_llm()
    return llm.invoke(prompt).content

def get_gemini_response_v4(query, context, chat_history):
    logger.info(f"Chat history in vector_store.py: {chat_history}")
    prompt = build_prompt_v6(query, context, chat_history)
    llm = get_gemini_llm()
    return llm.invoke(prompt).content

def get_gemini_response_v5(query, context, chat_history):
    logger.info(f"Chat history in vector_store.py: {chat_history}")
    prompt = build_prompt_v7(query, context, chat_history)
    llm = get_gemini_llm()
    return llm.invoke(prompt).content

#---- New functions for button operations ----
