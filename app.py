from config import openai, pinecone, EMBEDDING_MODEL, CHAT_MODEL, INDEX_NAME
from flask import Flask

app = Flask(__name__)


@app.route("/chat/<prompt>", methods=["POST"])
def chat(prompt):
    xq = openai.Embedding.create(input=prompt, engine=EMBEDDING_MODEL)["data"][0][
        "embedding"
    ]

    index = pinecone.Index(INDEX_NAME)

    res = index.query([xq], top_k=5, include_metadata=True)

    context = ""

    for match in res["matches"]:
        context += f"{match['metadata']['text']}\n"

    chat = openai.ChatCompletion.create(
        model=CHAT_MODEL,
        messages=[
            {
                "role": "system",
                "content": f"Try to answer any questions using the following context. Potentially helpful context: {context}",
            },
            {"role": "user", "content": prompt},
        ],
    )

    return chat["choices"][0]["message"]["content"]
