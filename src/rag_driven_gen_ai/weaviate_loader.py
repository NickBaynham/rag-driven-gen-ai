import requests, json
import weaviate
from weaviate.classes.config import Property, Configure
from config import WEAVIATE_HOST, WEAVIATE_PORT, WEAVIATE_GRPC_PORT, PROJECT_NAME
from weaviate.exceptions import WeaviateBaseError

client = weaviate.connect_to_local(host = WEAVIATE_HOST, port=WEAVIATE_PORT, grpc_port=WEAVIATE_GRPC_PORT)

try:
    print(client.is_ready())

    collection_name = PROJECT_NAME

    try:
        # Try to retrieve; if found, nothing more to do
        _ = client.collections.get(collection_name)
        print(f"✔ Collection '{collection_name}' already exists.")
    except WeaviateBaseError:
        # If any error (e.g. 404/422), assume it’s missing and create it
        print(f"⚠ Collection '{collection_name}' not found — creating it now.")
        collection = client.collections.create(
        name=collection_name,
        vectorizer_config=Configure.Vectorizer.text2vec_ollama(     # Configure the Ollama embedding integration
            api_endpoint="http://host.docker.internal:11434",       # Allow Weaviate from within a Docker container to contact your Ollama instance
            model="nomic-embed-text",                               # The model to use
        ),
        generative_config=Configure.Generative.ollama(              # Configure the Ollama generative integration
            api_endpoint="http://host.docker.internal:11434",       # Allow Weaviate from within a Docker container to contact your Ollama instance
            model="llama3.2",                                       # The model to use
        ))
        print(f"✔ Collection '{collection_name}' created.")

    resp = requests.get("https://raw.githubusercontent.com/weaviate-tutorials/quickstart/main/data/jeopardy_tiny.json")
    data = json.loads(resp.text)
    print(data)

finally:
    client.close()