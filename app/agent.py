from langchain.agents import initialize_agent, Tool
from app.models.llm import get_llm
from app.memory import get_memory

from app.tools.rag_tool import rag_tool
from app.tools.web_tool import web_tool
from app.tools.legal_tool import legal_tool

def create_agent(vectorstore):

    llm = get_llm()
    memory = get_memory()

    tools = [
        Tool(
            name="Legal RAG",
            func=lambda q: rag_tool(q, vectorstore),
            description="Use this for answering questions from uploaded legal documents"
        ),
        Tool(
            name="Web Search",
            func=web_tool,
            description="Use this for latest legal updates or news"
        ),
        Tool(
            name="Legal Explainer",
            func=legal_tool,
            description="Use this to explain legal concepts simply"
        )
    ]

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent="conversational-react-description",
        memory=memory,
        verbose=True
    )

    return agent