### UpgradeVIP RAG Chatbot

**Introduction**

A conversational AI assistant built to provide intelligent customer support for UpgradeVIP's premium airport services. This chatbot leverages Retrieval-Augmented Generation (RAG) to answer user queries accurately while maintaining context across conversations.

---
### Flow:
Input->user_input embedding->vector store creation/reload -> chroma db search for answer -> similar chunks top 2 ->llm (chunks,input,chat history)->llm generate answer.


---
**Tech Stack**

- AI Model: Google Gemini 2.5 Flash (via LangChain) &  gemini-embedding-001 for embeddings.
- Vector Database: ChromaDB for semantic search and embeddings
- Frontend: Streamlit for rapid UI prototyping
- Document Processing: LangChain document loaders and text splitters
- Context Management: In-memory chat history for conversational   context
- Logging: Comprehensive logging system for debugging and evaluation

---


**How It Works**
User Input → Query entered in Streamlit interface
Vector Search → retrieve_docs fetches relevant chunks from ChromaDB
Context Assembly → Top chunks combined into unified context
Prompt Building → Query + Context + Chat History → Structured prompt
LLM Generation → Gemini 2.5 Flash generates response via get_gemini_response
Chat History Update → Conversation stored for next turn context
Response Display → Answer shown with optional chunk transparency

**Key Features**
- RAG
- conversational history
- Only one time document embeddings to save tokens
- chroma DB as vector db for storing vectors
- Multiple versioning of prompts
- Validate vector store existance and reload/re-create it.

---
**Prompt Engineering Evolution**
- Version 1 - Base RAG (build_prompt_v3)
First-person perspective: "I can help you with..."
Context-aware contact sharing: Only when relevant
Greeting detection: Professional mirroring of user tone
Clean output: Strips internal metadata

- Version 2 - Intent Matching (build_prompt_v4)
Luxury-concierge tone: Refined, sophisticated language
Minimal-first approach: Core info upfront, expand on request
Structured presentation: Organized service lists
Smart context use: Avoids overwhelming users

- Version 3 - Elite Conversational (build_prompt_v5)
Natural phrasing: Avoids robotic repetition
Engagement words: "perfect", "absolutely", "delighted"
Paraphrasing intelligence: Varies responses dynamically
Enhanced UX: Warm, premium customer experience

- Version 4 - Structured Clarity (build_prompt_v6)
Numbered service format: Easy scanning and reference
Sophisticated vocabulary: Refined, warm, professional
Natural follow-ups: Based on query type and chat history
Progressive disclosure: Expands info only when needed

- Version 5 - Human-Centric (build_prompt_v7)
No robot vibes: Genuine conversational persona
Energy matching: Mirrors user's excitement/formality level
Scenic route: Engages unmotivated users naturally
Rapport over push: Builds trust before booking suggestions
---

**Data Curation Strategy**
Document Structure (upgradevip_details.txt)
Keyword-Rich Headers: Each section starts with comprehensive search terms
Example: "This section answers: mission, guarantee, satisfaction, company promise..."
Semantic Chunking: Content split into meaningful segments using RecursiveCharacterTextSplitter
Metadata Preservation: Flight details, pricing, contact info structured for easy retrieval
Multi-Format Support: Text and Markdown files for flexibility
---

**Vector Store (chroma.sqlite3)**
Embeddings: Google Generative AI embeddings via get_gemini_embeddings
Persistent Storage: ChromaDB with SQLite backend
Semantic Search: Retrieves top-K relevant chunks using retrieve_docs
Context Assembly: Combines retrieved chunks into coherent context for LLM
