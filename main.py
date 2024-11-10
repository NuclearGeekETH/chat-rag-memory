import gradio as gr
from modules.get_openai_response import chat_response


with gr.Blocks(theme=gr.themes.Soft(), title="LLM with Memory Demo") as demo:
    gr.Markdown(f"<h1 style='text-align: center; display:block'>{'LLM with Memory Demo'}</h1>")
    bot = gr.Chatbot(render=False)

    dropdown = gr.Dropdown(
        ["gpt-4o-2024-08-06", "gpt-4o", "gpt-4o-mini", "chatgpt-4o-latest", "gpt-4-0125-preview", "gpt-4-turbo", "gpt-4-1106-preview", "gpt-4"],
        label = "Model",
        value = "gpt-4o-mini",
        render = False
    )

    system = gr.Textbox(
        lines = 2,
        label = "System Message",
    value="You are ChatGPT, a large language model trained by OpenAI based on the GPT-4 architecture. " +
          "You have the ability to store, delete and retrieve memories. " +
          "Save anything of value and attempt to retrieve a memory when needed or asked. " +
          "Delete memories on request using the memory_id. " +
          "Always use memory_id when referencing or managing memories. " +
          "Make it clear when a memory is being stored, retrieved, or deleted and use the associated memory ID.",
        render = False
        )

    chat = gr.ChatInterface(
        fn = chat_response,
        chatbot = bot,
        additional_inputs = [dropdown, system]
    )

if __name__ == "__main__":
    demo.queue()
    # # Toggle this on if you want to share your app, change the username and password
    # demo.launch(share=True, auth=("admin", "password"))

    # Toggle this on if you want to only run local
    demo.launch()