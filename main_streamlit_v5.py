import streamlit as st
from rag_utils.vector_store import DOC_DIR, get_gemini_response, DatasetEmptyError, checking_vector_store,get_gemini_response_v2,get_gemini_response_v3,get_gemini_response_v4,get_gemini_response_v5
from rag_utils.retriever import retrieve_docs, get_context
from rag_utils.prompt import build_prompt
from rag_utils.setup import eval_logger, logger

def submit_on_enter():
    st.session_state._submitted = True

st.set_page_config(page_title="UpgradeVIP RAG Chatbot Version: 5.0", layout="wide")
st.title("UpgradeVIP RAG Chatbot Version: 5.0")

# Custom CSS for orange button with white text
st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #ff8800;
        color: white;
        height: 2em;
        width: 4em;
        font-size: 1.1em;
        font-weight: bold;
        border-radius: 8px;
        border: none;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_chroma_db():
    try:
        return checking_vector_store()
    except DatasetEmptyError as e:
        st.warning(str(e))
        return None

chromaDB = get_chroma_db()

# --- Chat history logic ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # List of dicts: [{"user": "...", "assistant": "..."}]

if chromaDB is None:
    st.error("⚠️ No documents available. Please upload documents to DATA/Docs and create the vector store.")
    st.info("👉 Steps:\n1. Add .txt or .md files to the DATA/Docs folder\n2. Restart the app or recreate the vector store")
else:
    query = st.text_input(
    "Welcome to the Upgarde Vip AI powered chatbot. Ask any query related to Upgrade vip:",
    key="query_input",
    on_change=submit_on_enter,
    autocomplete="off"  # <--- add this line
)
    # Place ASK button on the left below the text field
    col1, col2 = st.columns([1, 5])
    with col1:
       ask = st.button("ASK")
    with col2:
       pass

    if (query and ask) or st.session_state.get("_submitted", False):
        st.session_state._submitted = False  # reset flag
        if query.lower() in ["exit", "quit"]:
            st.info("👋 Exiting RAG pipeline.")

        else:
            try:# Use last 4 exchanges (8 messages) as chat history
                recent_history = st.session_state.chat_history[-4:] if len(st.session_state.chat_history) > 0 else None
                logger.info(f"Recent chat history: {recent_history}")
                retrieved_docs = retrieve_docs(query, chromaDB)
                context = "\n\n".join([doc.page_content for doc in retrieved_docs])
                with st.spinner("Generating answer..."):
                    answer = get_gemini_response_v5(query, context, chat_history=recent_history)
                st.markdown(f"**Assistant:** {answer}")

                # Store conversation
                st.session_state.chat_history.append({"user": query, "assistant": answer})

                eval_logger.info(
                    f"\n\n\n\nmain_streamlit_v5\n**Query:** {query}\n"
                    f"**Context:** {context}\n"
                    f"**Answer:** {answer}\n"
                    "----------------------------------------"
                )

                with st.expander("Show retrieved chunks"):
                    for i, doc in enumerate(retrieved_docs):
                        st.write(f"**Chunk {i+1}:** {doc.page_content}")
            except Exception as e:
                st.error(f"An error occurred while processing your request: {e}")
    # Optional: Show chat history in the UI
    if st.session_state.chat_history:
        with st.expander("🕑 Chat History"):
            for i, turn in enumerate(st.session_state.chat_history[-8:]):
                st.markdown(f"**You:** {turn['user']}")
                st.markdown(f"**Assistant:** {turn['assistant']}")