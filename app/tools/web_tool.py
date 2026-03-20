from app.utils.web_utils import search_web

def web_tool(query):
    try:
        return search_web(query)
    except Exception as e:
        return f"Web search error: {str(e)}"