import openai
import boto3
import os
import openai
from bs4 import BeautifulSoup
import requests, json
import weaviate
from weaviate.classes.config import Configure
from weaviate.exceptions import WeaviateBaseError

# The OpenAI API key is stored in AWS Secrets Manager
# This function retrieves the key from AWS Secrets Manager
# and returns it as a string
# def get_openai_key():
#     # Create a session with SSL verification disabled
#     session = boto3.Session()
#     client = session.client('secretsmanager', verify=False)
#     response = client.get_secret_value(SecretId='openai/apiKey')
#     return response['SecretString']

print("Starting RAG Pipeline Ingestion")

client = weaviate.connect_to_local()
print(client.is_ready())  # Should print: `True`

collection_name = "Question"

try:
    # Try to retrieve; if found, nothing more to do
    _ = client.collections.get(collection_name)
    print(f"✔ Collection '{collection_name}' already exists.")
except WeaviateBaseError:
    # If any error (e.g. 404/422), assume it’s missing and create it
    print(f"⚠ Collection '{collection_name}' not found — creating it now.")
    questions = client.collections.create(
    name="Question",
    vectorizer_config=Configure.Vectorizer.text2vec_ollama(     # Configure the Ollama embedding integration
        api_endpoint="http://host.docker.internal:11434",       # Allow Weaviate from within a Docker container to contact your Ollama instance
        model="nomic-embed-text",                               # The model to use
    ),
    generative_config=Configure.Generative.ollama(              # Configure the Ollama generative integration
        api_endpoint="http://host.docker.internal:11434",       # Allow Weaviate from within a Docker container to contact your Ollama instance
        model="llama3.2",                                       # The model to use
    ))
    print(f"✔ Collection '{collection_name}' created.")


# We will start with some demo data

resp = requests.get(
   "https://raw.githubusercontent.com/weaviate-tutorials/quickstart/main/data/jeopardy_tiny.json"
)
data = json.loads(resp.text)

questions = client.collections.get("Question")

with questions.batch.fixed_size(batch_size=200) as batch:
   for d in data:
       batch.add_object(
           {
               "answer": d["Answer"],
               "question": d["Question"],
               "category": d["Category"],
           }
       )
       if batch.number_errors > 10:
           print("Batch import stopped due to excessive errors.")
           break

failed_objects = questions.batch.failed_objects
if failed_objects:
   print(f"Number of failed imports: {len(failed_objects)}")
   print(f"First failed object: {failed_objects[0]}")


client.close()

# Get the OpenAI API key from AWS Secrets Manager
# OPENAI_API_KEY=get_openai_key()
# print("A key was read of length", len(OPENAI_API_KEY))

# os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
# openai.api_key = os.getenv("OPENAI_API_KEY")

# Open the file and read the first 20 lines
# with open('llm.txt', 'r', encoding='utf-8') as file:
#     lines = file.readlines()
#     # Print the first 20 lines
#     for line in lines[:20]:
#         print(line.strip())

#     with open('llm.txt', 'r') as f:
#         text = f.read()

# Chunk the text into 1000 character chunks
# CHUNK_SIZE = 1000
# chunked_text = [text[i:i+CHUNK_SIZE] for i in range(0,len(text), CHUNK_SIZE)]

# Print the first 20 lines
# for line in chunked_text[:20]:
#         print(line.strip())

# vector_store_path = "hub://nickbaynham/space_exploration_v1"
# try:
    # Attempt to load the vector store
    # vector_store = VectorStore(path=vector_store_path)
#     print("Vector store exists")
# except FileNotFoundError:
#     print("Vector store does not exist. You can create it.")
    # Code to create the vector store goes here
    # create_vector_store=True

# Read llm.txt and chunk into 1000 character pieces
# with open('llm.txt', 'r', encoding='utf-8') as f:
    # text = f.read()
# chunks = [text[i:i+CHUNK_SIZE] for i in range(0, len(text), CHUNK_SIZE)]


# Add the chunks as a text column
# (Assume Deep Lake auto-creates columns as needed)
