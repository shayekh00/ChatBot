# main.py
import gradio as gr
from langchain_core.messages import HumanMessage
from chatbot import chat                


def respond(user_text, history, session_id="main"):
    """
    1) Call the chat() helper (adds msg to LLM + memory, gets reply).
    2) Convert BOTH messages into {'role', 'content'} dicts.
    3) Append to history list expected by gr.Chatbot(type="messages").
    """
    assistant_text = chat(session_id, user_text)

    # Gradio wants dict objects, not tuples
    history.append({"role": "user",      "content": user_text})
    history.append({"role": "assistant", "content": assistant_text})

    # return "" to clear the input box, and new history
    return "", history


with gr.Blocks() as demo:
    chatbot = gr.Chatbot(type="messages")
    input_box = gr.Textbox(placeholder="Ask me anything…")
    clear_btn = gr.Button("Clear")

    input_box.submit(respond, [input_box, chatbot], [input_box, chatbot])
    clear_btn.click(lambda: [], None, chatbot, queue=False)

demo.launch()
