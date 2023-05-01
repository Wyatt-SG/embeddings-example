# Embeddings App

Complete example of using OpenAI's [Embeddings API](https://beta.openai.com/docs/engines/embeddings) with [Pinecone](https://www.pinecone.io/) to complete a chat prompt

## Getting started

1. Get an OpenAI API key [here](https://platform.openai.com/account/api-keys) and a Pinecone API key [here](https://docs.pinecone.io/docs/quickstart)

2. Create `.env` file and set environment variables
    ```bash
    echo "OPENAI_KEY=\nPINECONE_KEY=\nPINECONE_ENV=" >.env

This project uses a [Python virtual environment](https://docs.python.org/3/library/venv.html)

3. Create virtual environment
    ```bash
    python3 -m venv .venv
    ```

4. Active environment
    ```bash
    . .venv/bin/activate
    ```

5. Install dependencies
    ```bash
    pip install -r requirements.txt
    ```

## Seed data

Populate the index with the seed data
```bash
python3 scripts/populate_index.py
```

## Start app


```bash
flask --app app run
```

The server will be running at [http://127.0.0.1:5000/](http://127.0.0.1:5000/)