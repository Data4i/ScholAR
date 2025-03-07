from langchain.chat_models import init_chat_model
from dotenv import load_dotenv, find_dotenv
from langchain_together import ChatTogether

load_dotenv(find_dotenv())

llm = ChatTogether(
    model="meta-llama/Llama-3-70b-chat-hf",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)





# llm = init_chat_model("meta-llama/Llama-3.3-70B-Instruct-Turbo", model_provider="together", temperature=0)