from rag_utils.vector_store import checking_vector_store
from rag_utils.vector_store import DOC_DIR, get_gemini_response
from rag_utils.retriever import retrieve_docs, get_context
from rag_utils.prompt import build_prompt
from rag_utils.setup import logger, eval_logger

print("🚀 RAG pipeline started...")
faiss_db = checking_vector_store()

chat_history = []  # Store as list of dicts: [{"user": "...", "assistant": "..."}]

while True:
    try:
        query = input("----> You: ")
        
        if query.lower() in ["exit", "quit"]:
            print("👋 Exiting RAG pipeline.")
            logger.info("👋 Exiting RAG pipeline.")
            break
        
        logger.info(f"Processing query: {query}")
        context = get_context(query, faiss_db)
        
        # Pass last 4 exchanges (8 messages)
        recent_history = chat_history[-4:] if len(chat_history) > 0 else None
        
        answer = get_gemini_response(query, context, chat_history=recent_history)
        print(f"\n----> Assistant: {answer}\n")
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
    
    except KeyboardInterrupt:
        print("\n\n👋 Exiting RAG pipeline (interrupted by user).")
        logger.info("👋 Exiting RAG pipeline (interrupted by user).")
        break
    except Exception as e:
        error_msg = f"❌ Error occurred: {type(e).__name__}: {str(e)}"
        print(f"\n{error_msg}\n")
        logger.error(error_msg, exc_info=True)
        print("Please try again or type 'exit' to quit.\n")
