from tqdm.auto import tqdm
import os
import openai
import pinecone
from dotenv import load_dotenv
import json

load_dotenv()

pinecone.init(
    api_key=os.environ.get("PINECONE_KEY"),
    environment=os.environ.get("PINECONE_ENV"),
)

openai.api_key = os.environ.get("OPENAI_KEY")

EMBEDDING_MODEL = "text-embedding-ada-002"
CHAT_MODEL = "gpt-3.5-turbo"
INDEX_NAME = "sales-gpt"


def populate_index():
    with open("scripts/example-data.json", "r") as file:
        data = json.load(file)

    text_array = data["text"]

    res = openai.Embedding.create(
        input=[
            "Sample document text goes here",
            "there will be several phrases in each batch",
        ],
        engine=EMBEDDING_MODEL,
    )

    embeds = [record["embedding"] for record in res["data"]]

    # check if 'openai' index already exists (only create index if not)
    if INDEX_NAME not in pinecone.list_indexes():
        pinecone.create_index(INDEX_NAME, dimension=len(embeds[0]))

    # connect to index
    index = pinecone.Index(INDEX_NAME)

    batch_size = 32  # process everything in batches of 32
    for i in tqdm(range(0, len(text_array), batch_size)):
        # set end position of batch
        i_end = min(i + batch_size, len(text_array))
        # get batch of lines and IDs
        lines_batch = text_array[i : i + batch_size]
        ids_batch = [str(n) for n in range(i, i_end)]
        # create embeddings
        res = openai.Embedding.create(input=lines_batch, engine=EMBEDDING_MODEL)
        embeds = [record["embedding"] for record in res["data"]]
        # prep metadata and upsert batch
        meta = [{"text": line} for line in lines_batch]
        to_upsert = zip(ids_batch, embeds, meta)
        # upsert to Pinecone
        index.upsert(vectors=list(to_upsert))


populate_index()
