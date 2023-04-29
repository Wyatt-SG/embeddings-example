# Embeddings App

## Getting started

1. Get an OpenAI API key [here](https://platform.openai.com/account/api-keys)

1. Create `.env` file and set environment variables
    ```bash
    echo 'OPENAI_KEY=[YOUR KEY HERE]' >.env
    ```

2. Active environment <br />
    This project uses a [Python virtual environment](https://docs.python.org/3/library/venv.html). To get started, run the following command:

    ```bash
    . venv/bin/activate
    ```

3. Start server
    ```bash
    flask app run
    ```
    The server will be running at [http://127.0.0.1:5000/](http://127.0.0.1:5000/)