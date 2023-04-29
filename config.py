import os
import openai
import pinecone
from dotenv import load_dotenv

load_dotenv()

pinecone.init(
    api_key=os.environ.get("PINECONE_KEY"),
    environment=os.environ.get("PINECONE_ENV"),
)

openai.api_key = os.environ.get("OPENAI_KEY")

EMBEDDING_MODEL = "text-embedding-ada-002"
CHAT_MODEL = "gpt-3.5-turbo"
INDEX_NAME = "openai"
