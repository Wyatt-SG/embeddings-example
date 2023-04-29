from config import openai, pinecone, EMBEDDING_MODEL, INDEX_NAME
from datasets import load_dataset
from tqdm.auto import tqdm


def populate_index():
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

    trec = load_dataset("trec", split="train[:1000]")

    batch_size = 32  # process everything in batches of 32
    for i in tqdm(range(0, len(trec["text"]), batch_size)):
        # set end position of batch
        i_end = min(i + batch_size, len(trec["text"]))
        # get batch of lines and IDs
        lines_batch = trec["text"][i : i + batch_size]
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
