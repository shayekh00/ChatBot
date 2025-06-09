# chatbot.py  –  simple, bullet-proof version
from typing import Dict, List
from langchain_openai import ChatOpenAI                     
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage,
)
from config import MODEL_NAME, SYSTEM_PROMPT

# ── 1.  Create a single ChatOpenAI instance  ────────────────────────────────────
llm = ChatOpenAI(model=MODEL_NAME) # ChatOpenAI expects List[BaseMessage] :contentReference[oaicite:2]{index=2}

# ── 2.  In-memory store:  session-id ➜ list[BaseMessage]  ─────────────────────—
_history: Dict[str, List] = {}

from retriever import retrieve

def chat(session_id: str, user_text: str) -> str:
    """
    1) Retrieve context.
    2) Build RAG prompt: system + retrieved docs + user.
    3) Call LLM, save reply.
    """
    # ensure history initialised … (same as before)
    if session_id not in _history:
        _history[session_id] = [SystemMessage(content=SYSTEM_PROMPT)]

    # 1. RAG step
    context = retrieve(user_text)          # top-k docs as a big string

    # 2. Build one *synthetic* assistant message that injects the context
    context_msg = AIMessage(
        content=f"Here are relevant reference materials:\n{context}"
    )

    # 3. Append both context (as if assistant provided it) + user question
    _history[session_id].extend([context_msg, HumanMessage(content=user_text)])

    # 4. LLM call
    assistant_msg: AIMessage = llm.invoke(_history[session_id])

    _history[session_id].append(assistant_msg)
    return assistant_msg.content

# def chat(session_id: str, user_text: str) -> str:
#     """
#     Add the user's text to the running history for `session_id`,
#     call the model with the *full* message list,
#     append the assistant reply to history,
#     and return the reply's text.
#     """
#     # initialise history once per session with the system prompt
#     if session_id not in _history:
#         _history[session_id] = [SystemMessage(content=SYSTEM_PROMPT)]

#     # 2a. append the new user message
#     _history[session_id].append(HumanMessage(content=user_text))

#     # 2b. call the model with the entire message list
#     assistant_msg: AIMessage = llm.invoke(_history[session_id])  # invoke = sync call :contentReference[oaicite:3]{index=3}

#     # 2c. append model response to history
#     _history[session_id].append(assistant_msg)

#     # 2d. return the text content for your UI
#     return assistant_msg.content
