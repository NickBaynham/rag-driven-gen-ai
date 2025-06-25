import boto3
import urllib3

# Disable SSL warnings and verification for local development
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# The OpenAI API key is stored in AWS Secrets Manager
# This function retrieves the key from AWS Secrets Manager
# and returns it as a string
def get_openai_key():
    # Create a session with SSL verification disabled
    session = boto3.Session()
    client = session.client('secretsmanager', verify=False)
    response = client.get_secret_value(SecretId='openai/apiKey')
    return response['SecretString']

print("Starting RAG Pipeline Retriever")

API_KEY=get_openai_key()
print("A key was read of length", len(API_KEY))
