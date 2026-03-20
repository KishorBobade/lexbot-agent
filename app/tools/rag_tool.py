def rag_tool(query, vectorstore):
    try:
        if vectorstore is None:
            return "No document uploaded."

        docs = vectorstore.similarity_search(query, k=3)
        return "\n".join([doc.page_content for doc in docs])

    except Exception as e:
        return f"RAG Error: {str(e)}"