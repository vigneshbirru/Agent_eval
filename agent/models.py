from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()
model = init_chat_model( model="groq:openai/gpt-oss-120b",)

response = model.invoke("tell me about agent eval")
# print(response.content)