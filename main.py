import gradio as gr
import os
from chat import Chat

# Instantiate chat with system message
chat = Chat(system="You are a helpful assistant.")

# Gradio UI function
def respond(message, chat_history):
    bot_message = chat.prompt(content=message)
    chat_history.append((message, bot_message))
    return "", chat_history

# Gradio UI layout
with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.Button("Clear")

    msg.submit(respond, [msg, chatbot], [msg, chatbot])
    clear.click(lambda: [], None, chatbot, queue=False)

demo.launch(debug=True)
