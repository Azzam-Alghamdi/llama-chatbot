import groq
from langchain.chains import LLMChain
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.messages import SystemMessage
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq

groq_api_key = ("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")
model = "llama-3.3-70b-versatile"

groq_chat = ChatGroq(
    groq_api_key=groq_api_key,
    model_name=model
)

system_prompt = "You are a friendly conversational chatbot"
conversational_memory_length = 5
memory = ConversationBufferWindowMemory(k=conversational_memory_length, memory_key="chat_history", return_messages=True)

def generate_ai_response(user_message):
    if not groq_api_key:
        return "Error: Groq API key is missing."
    
    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content=system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template("{human_input}"),
        ]
    )

    conversation = LLMChain(
        llm=groq_chat,
        prompt=prompt,
        verbose=False,
        memory=memory,
    )
    
    response = conversation.predict(human_input=user_message)
    return response
