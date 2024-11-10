# LLM with Memory Demo

![Python](https://img.shields.io/badge/python-3.9%2B-yellow.svg)

## Overview

The **LLM with Memory Demo** is a demonstration application that leverages language models with memory capabilities to store, retrieve, and manage information across interactions. The demo application uses OpenAI's models with Gradio for creating an interactive web-based interface. It includes features for creating, deleting, and searching for 'memories' stored as vector embeddings.

## Features

- **Interactive Chat Interface:** Communicate with a chatbot that can remember, forget or search for specific information upon request.
- **Memory Management:** Create, store, retrieve, and delete memories through a structured approach.
- **Model Selection:** Offers choice among various OpenAI models for responses.
- **Customizable System Messages:** Configure the chatbot's behavior with initial system prompts.
- **Persistence of Memory:** Uses Chroma as vector store to persist memory between sessions.

## Installation

To set up the LLM with Memory Demo on your local machine, follow these steps:

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/NuclearGeekETH/chat-rag-demo.git
   cd chat-rag-demo
   ```

2. **Create a Virtual Environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies:**

   Ensure you have [Python 3.9+](https://www.python.org/downloads/) installed, then run:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables:**

   Create a `.env` file and add your OpenAI API key:

   ```plaintext
   OPENAI_API_KEY=your_openai_api_key_here
   ```

5. **Run the Application:**

   ```bash
   python main.py
   ```

   *Toggle the launch options in `main.py` to share your app online or run it locally.*

## Usage

1. Launch the application and open the given local address in your browser.
2. Choose a model from the dropdown.
3. Interact with the chatbot by typing messages. Utilize its memory capabilities by explicitly stating when you want to store or retrieve a memory.

## Directory Structure

- **main.py:** The entry point of the application.
- **modules/get_open_ai_response.py:** Contains functions managing the chatbot's memory operations (create, delete, search).
- **requirements.txt:** Lists the Python packages required to run this demo.

## Dependencies

- [Gradio](https://www.gradio.app/) - For building interactive interfaces.
- [OpenAI](https://beta.openai.com/docs/) - Interface with OpenAI models.
- [LangChain](https://langchain.com/) - Managing and deploying language model applications.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request or report issues.
