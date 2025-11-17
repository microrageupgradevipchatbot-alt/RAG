import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
import logging
load_dotenv()

# ==================================== Chroma db and docs function =========================================

def setup_paths():
    current_dir = Path(__file__).parent.parent
    data_dir = current_dir / "DATA"
    db_dir = data_dir / "DB"
    doc_dir = data_dir / "Docs"
    
    # Create directories if they don't exist
    data_dir.mkdir(exist_ok=True)
    db_dir.mkdir(exist_ok=True)
    doc_dir.mkdir(exist_ok=True)

    return current_dir, db_dir, doc_dir

def setup_logging():
    LOG_FILE = LOGS_DIR / 'RAG_MODULAR_STRUCTURE.log'
    logger = logging.getLogger("Upgrade-Vip")
    logger.setLevel(logging.INFO)
    # replace handlers to avoid duplicates
    logger.handlers = []
    file_handler = logging.FileHandler(str(LOG_FILE), encoding="utf-8")
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(name)s: %(message)s',
                                                '%Y-%m-%d %H:%M:%S'))
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(name)s: %(message)s',
                                                   '%Y-%m-%d %H:%M:%S'))
    logger.addHandler(console_handler)

    logger.propagate = False
    return logger

def setup_evaluation_logger():
    LOG_FILE = LOGS_DIR / 'log_evaluation.log'
    eval_logger = logging.getLogger("EvaluationLogger")
    eval_logger.setLevel(logging.INFO)
    eval_logger.handlers = []
    file_handler = logging.FileHandler(str(LOG_FILE), encoding="utf-8")
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(message)s', '%Y-%m-%d %H:%M:%S'))
    eval_logger.addHandler(file_handler)
    eval_logger.propagate = False
    return eval_logger

CURRENT_DIR, DB_DIR, DOC_DIR = setup_paths()
LOGS_DIR = CURRENT_DIR / 'Logs'   # single logs directory for both files
LOGS_DIR.mkdir(exist_ok=True)

logger = setup_logging()
eval_logger = setup_evaluation_logger()

#
#=================================== Model Gemini =========================================
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if GOOGLE_API_KEY:
    logger.info("GOOGLE_API_KEY loaded successfully.")
else:
    logger.info("GOOGLE_API_KEY not found. Please set it in your environment or .env file.")

def get_gemini_embeddings():
    #api_key = os.getenv("GOOGLE_API_KEY")
    embeddings = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001",
        google_api_key=GOOGLE_API_KEY
    )
    return embeddings
def get_gemini_llm():
    #api_key = os.getenv("GOOGLE_API_KEY")
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=GOOGLE_API_KEY,
        temperature=0.7,  # Add this for more conversational, friendly responses
    )
    return llm

