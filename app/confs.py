"""
Static settings app file. Put your static at runtime settings here.
"""

from pathlib import Path


__PROJECT_DIR_OBJ_PATH = Path(__file__).parent.parent.absolute()
PROJECT_DIR = str(__PROJECT_DIR_OBJ_PATH)

# App confs
ACCEPT_DOCS_FORMATS = [".pdf", ".csv", ".txt", ".docx"]

# LLM model confs
LLM_MODEL = "gemini-2.5-flash"
LLM_API_KEY_NAME = "GOOGLE_AISTUDIO_API_KEY"

# Embeddings confs
EMBEDDINGS_API_KEY_NAME = "GOOGLE_AISTUDIO_API_KEY"
EMBEDDINGS_MODEL = "models/gemini-embedding-001"

# VectorDB confs
COLLECTION_NAME = "docs"
PERSIST_DIR = str(__PROJECT_DIR_OBJ_PATH.joinpath("/vectordata/").absolute())
