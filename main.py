from rag_utils.vector_store import checking_vector_store
from rag_utils.vector_store import DOC_DIR, get_gemini_response,delete_vector_store
from rag_utils.retriever import retrieve_docs, get_context
from rag_utils.prompt import build_prompt
from rag_utils.setup import logger, eval_logger

print("🚀 RAG pipeline started...")
chromaDB = checking_vector_store()

chat_history = []  # Store as list of dicts: [{"user": "...", "assistant": "..."}]

while True:
    query = input("----> You: ")
    
    if query.lower() in ["exit", "quit"]:
        print("👋 Exiting RAG pipeline.")
        logger.info("👋 Exiting RAG pipeline.")
        break
    context = get_context(query, chromaDB)
    
    # Pass last 4 exchanges (8 messages)
    recent_history = chat_history[-4:] if len(chat_history) > 0 else None
    
    answer = get_gemini_response(query, context, chat_history=recent_history)
    logger.info(f"\n----> Assistant: {answer}")

    # Store conversation
    chat_history.append({"user": query, "assistant": answer})
    

    eval_logger.info(
            f"checking build prompt v3 on hamza dataset\n\n"
            f"**Query:** {query}\n"
            f"**Context:** {context}\n"
            f"**Answer:** {answer}\n"
            "----------------------------------------------------------------------\n"
            "----------------------------------------------------------------------\n"
            "----------------------------------------------------------------------\n"
            "----------------------------------------------------------------------\n"
            "----------------------------------------------------------------------\n"
    )