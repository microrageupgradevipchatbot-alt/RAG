from .setup import logger
def retrieve_docs(query,faiss_db):
  '''Retrieve Docs from Vector Store using similarity search'''
  retrieveDocs = faiss_db.similarity_search(query, k=2)

  return retrieveDocs
def get_context_from_docs(documents):
  '''Get pag_content from documents to create context'''
                          
  context = "\n\n".join([doc.page_content for doc in documents])
  for i, doc in enumerate(documents):
      logger.info(f"📋 Chunk {i+1}: {doc.page_content}")
  return context

def get_context(query,faiss_db):
    retrieved_docs = retrieve_docs(query,faiss_db)
    context= get_context_from_docs(retrieved_docs)
    return context
