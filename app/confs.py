"""
Static settings app file. Put your static at runtime settings here.
"""
import os

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


# Embeddings confs
EMBEDDINGS_API_KEY_NAME="GOOGLE_AISTUDIO_API_KEY"
EMBEDDINGS_MODEL="models/gemini-embedding-001"

# VectorDB confs
COLLECTION_NAME="docs"
PERSIST_DIR=os.path.join(PROJECT_DIR, "/vectordata/")
