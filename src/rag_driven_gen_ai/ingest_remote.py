from bs4 import BeautifulSoup
import boto3
import requests, json
import weaviate
from weaviate.classes.config import Configure
from weaviate.exceptions import WeaviateBaseError
from weaviate.auth import AuthApiKey

# The Weaviate API key is stored in AWS Secrets Manager
# This function retrieves the key from AWS Secrets Manager
# and returns it as a string
def get_weaviate_key():
    # Create a session with SSL verification disabled
    session = boto3.Session()
    client = session.client('secretsmanager', verify=False)
    try:
        response = client.get_secret_value(SecretId='weaviate/apiKey')
        secret_string = response['SecretString']
        
        # Try to parse as JSON in case it's stored as a JSON object
        try:
            import json
            secret_data = json.loads(secret_string)
            # If it's a JSON object, look for common key names
            if isinstance(secret_data, dict):
                # Try common key names for API keys
                for key in ['api_key', 'apikey', 'key', 'token', 'weaviate_key']:
                    if key in secret_data:
                        return secret_data[key]
                # If no common key found, return the first string value
                for value in secret_data.values():
                    if isinstance(value, str):
                        return value
                # If still no string found, return the original
                return secret_string
            else:
                return secret_string
        except json.JSONDecodeError:
            # Not JSON, return as is
            return secret_string
            
    except Exception as e:
        print(f"Error retrieving API key from AWS Secrets Manager: {e}")
        # For testing, you can return a placeholder or use environment variable
        import os
        return os.getenv('WEAVIATE_API_KEY', 'your-api-key-here')

print("Starting RAG Pipeline Ingestion")

# ToDo: Load this from an .env file

WEAVIATE_HOST = "weaviate.calgentik.com"
WEAVIATE_PORT = 443
GRPC_PORT = 50051
api_key = get_weaviate_key()
print(f"API Key retrieved: {api_key[:10]}..." if len(api_key) > 10 else f"API Key retrieved: {api_key}")
print(f"API Key length: {len(api_key)}")
print(f"API Key type: {type(api_key)}")

client = weaviate.connect_to_custom(
    http_host=WEAVIATE_HOST,
    http_port=WEAVIATE_PORT,
    http_secure=True,
    grpc_host=WEAVIATE_HOST, 
    grpc_port=GRPC_PORT,
    grpc_secure=False,  # Try without SSL for gRPC
    auth_credentials=AuthApiKey(api_key),
    skip_init_checks=True)  # Skip gRPC health check

print(client.is_ready())

collection_name = "Question"

# try:
#     # Try to retrieve; if found, nothing more to do
#     _ = client.collections.get(collection_name)
#     print(f"✔ Collection '{collection_name}' already exists.")
# except WeaviateBaseError:
#     # If any error (e.g. 404/422), assume it’s missing and create it
#     print(f"⚠ Collection '{collection_name}' not found — creating it now.")
#     questions = client.collections.create(
#     name="Question",
#     vectorizer_config=Configure.Vectorizer.text2vec_ollama(     # Configure the Ollama embedding integration
#         api_endpoint="http://host.docker.internal:11434",       # Allow Weaviate from within a Docker container to contact your Ollama instance
#         model="nomic-embed-text",                               # The model to use
#     ),
#     generative_config=Configure.Generative.ollama(              # Configure the Ollama generative integration
#         api_endpoint="http://host.docker.internal:11434",       # Allow Weaviate from within a Docker container to contact your Ollama instance
#         model="llama3.2",                                       # The model to use
#     ))
#     print(f"✔ Collection '{collection_name}' created.")


# We will start with some demo data

# resp = requests.get(
#    "https://raw.githubusercontent.com/weaviate-tutorials/quickstart/main/data/jeopardy_tiny.json"
# )
# data = json.loads(resp.text)

# questions = client.collections.get("Question")

# with questions.batch.fixed_size(batch_size=200) as batch:
#    for d in data:
#        batch.add_object(
#            {
#                "answer": d["Answer"],
#                "question": d["Question"],
#                "category": d["Category"],
#            }
#        )
#        if batch.number_errors > 10:
#            print("Batch import stopped due to excessive errors.")
#            break

# failed_objects = questions.batch.failed_objects
# if failed_objects:
#    print(f"Number of failed imports: {len(failed_objects)}")
#    print(f"First failed object: {failed_objects[0]}")

client.close()

