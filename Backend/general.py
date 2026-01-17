from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
groq_client = Groq()

def generalchat(query, chat_history):
    # 1. Define the System Persona
    # It is best to put instructions in the 'system' role so they persist 
    # even as the conversation gets longer.
    system_instruction = """You are a helpful food delivery app assistant. 
    Answer the following question based on your general knowledge and chat history.
    Don't mention any work which you cannot do, just answer the question to the best of your ability."""

    # 2. Start building the message list
    messages = [
        {
            'role': 'system',
            'content': system_instruction
        }
    ]

    # 3. Add the Chat History
    # We loop through the history passed from Streamlit and append it.
    # We explicitly extract only 'role' and 'content' to avoid passing any 
    # extra Streamlit metadata to the API.
    for message in chat_history:
        messages.append({
            'role': message['role'],
            'content': message['content']
        })

    # 4. Add the Current Query
    messages.append({
        'role': 'user',
        'content': query
    })

    # 5. Make the API Call with the full context
    completion = groq_client.chat.completions.create(
        model=os.environ['GROQ_MODEL'],
        messages=messages
    )

    return completion.choices[0].message.content