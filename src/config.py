# config.py
import os
from dotenv import load_dotenv

# Load variables from .env into os.environ
load_dotenv()  

# Fetch — with defaults if you like
WEAVIATE_HOST      = os.getenv("WEAVIATE_HOST", "localhost")
WEAVIATE_PORT      = int(os.getenv("WEAVIATE_PORT", "8080"))
WEAVIATE_GRPC_PORT = int(os.getenv("WEAVIATE_GRPC_PORT", "50051"))
PROJECT_NAME       = os.getenv("PROJECT_NAME", "Question")
