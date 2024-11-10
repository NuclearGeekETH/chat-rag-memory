import openai
import os
import json
from dotenv import load_dotenv
from datetime import date
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document

load_dotenv()

key = os.getenv("OPENAI_API_KEY")

openai.api_key = key

embedding_function = OpenAIEmbeddings()
vector_store = Chroma(embedding_function=embedding_function, persist_directory="./db_memories")

vector_store.persist()

def create_memory(memory, memory_id):
    print(f"creating memory: {memory}\nmemory_id: {memory_id}")
    try:
        memory_1 = Document(
            page_content=memory,
            metadata={
                "source": "user",
                "memory_id": memory_id
                }
        )

        print(f"memory data: {memory_1}")

        documents = [memory_1]
        
        vector_store.add_documents(documents=documents, ids=[memory_id])

        return("Memory created")

    except Exception as e:
        return(f"Creating Memory Error: {e}")

def delete_memory(memory_id):
    print(f"deleting memory with id: {memory_id}")
    try:      
        vector_store.delete(memory_id)

        return("Memory deleted")
        
    except Exception as e:
        return(f"Deleting Memory Error: {e}")

def search_memory(query):
    print(f"Searching memory for: {query}")
    try:
        matched_docs = vector_store.similarity_search(query)

        print("Matched Documents:", matched_docs)

        if not matched_docs:
            return("No matching memories.")
        
        injected_docs_content = ""

        for doc in matched_docs:
            # Assuming doc is an object with 'metadata' and 'page_content' attributes
            memory_id = doc.metadata.get('memory_id', 'Unknown memory_id')
            source = doc.metadata.get('source', 'Unknown source')

            # Print for debugging
            print(f"Memory with id: {memory_id} from source: {source}")

            # Construct content for each document
            doc_content = f"memory_id: {memory_id}\nsource: {source}\ncontents: {doc.page_content}"
            injected_docs_content += doc_content 

        # Print for verification and debugging
        print("Injected Docs Content:")
        print(injected_docs_content)

        return injected_docs_content
    
    except Exception as e:
        return(f"Searching Memory Error: {e}")

def execute_function_call(tool_call):
    function_name = tool_call.function.name
    if function_name == "create_memory":
        arguments = tool_call.function.arguments
        arguments_contents = json.loads(arguments)
        memory = arguments_contents["memory"]
        memory_id = arguments_contents["memory_id"]
        results = create_memory(memory, memory_id)
        return results
    elif function_name == "delete_memory":
        arguments = tool_call.function.arguments
        arguments_contents = json.loads(arguments)
        memory_id = arguments_contents["memory_id"]
        results = delete_memory(memory_id)
        return results
    elif function_name == "search_memory":
        arguments = tool_call.function.arguments
        arguments_contents = json.loads(arguments)
        query = arguments_contents["query"]
        results = search_memory(query)
        return results

    else:
        return f"Error: function {function_name} does not exist"

def chat_response(message, history, model, system):
    print(history)

    tools = [
        {
            "type": "function",
            "function": {
                "name": "create_memory",
                "description": "Create a saved memory.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "memory": {
                            "type": "string",
                            "description": "The memory you are saving.",
                        },
                        "memory_id": {
                            "type": "string",
                            "description": "A unique string representing the id of the memory.",
                        },
                    },
                    "required": ["memory", "memory_id"]
                },
            }
        },
        {
            "type": "function",
            "function": {
                "name": "delete_memory",
                "description": "Delete a saved memory using the memory_id. Ensure you use the memory_id from the conversation context.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "memory_id": {
                            "type": "string",
                            "description": "The unique string representing the id of the memory.",
                        },
                    },
                    "required": ["memory_id"]
                },
            }
        },
        {
            "type": "function",
            "function": {
                "name": "search_memory",
                "description": "Search for a saved memory using a query, returns the memory and memory_id.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The text of the memory you are searching for.",
                        },
                    },
                    "required": ["query"]
                },
            }
        },
    ]

    try:
        history_response = []

        history_response.append({"role": "system", "content": f"{system} Current Date: {date.today()}"})

        for human, assistant in history:
            history_response.append({"role": "user", "content": human})
            history_response.append({"role": "assistant", "content": assistant})

        history_response.append({"role": "user", "content": message})
              
        completion = openai.chat.completions.create(
            model = model,
            messages = history_response,
            tools=tools,
            tool_choice='auto',
        )

        print(completion)

        assistant_message = completion.choices[0].message

        # history_response.append({"role": "assistant", "content": assistant_message})

        print(assistant_message)

        if hasattr(assistant_message, 'tool_calls') and assistant_message.tool_calls:
            for tool_call in assistant_message.tool_calls:
                # print(tool_call)
                function_response_content = execute_function_call(tool_call)
                # print(function_response_content)

                # Extend the conversation with the actual function response
                history_response.append({
                    "tool_call_id": tool_call.id, # Link response to the call
                    "role": "system",
                    "content": function_response_content
                })

                print(history_response)

        completion = openai.chat.completions.create(
            model = model,
            messages = history_response,
            stream=True
        )

        # Stream Response
        partial_message = ""
        for chunk in completion:
            if chunk.choices[0].delta.content != None:
                partial_message = partial_message + str(chunk.choices[0].delta.content)
                if partial_message:
                    yield partial_message

    except Exception as e:
        return(f"OpenAI API returned an API Error: {e}")
    

