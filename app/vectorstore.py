"""
VectorDB handler, guarantees one instance/connection to vectorDB across application and
exposition of only needed interface.
"""

from langchain_community.vectorstores.chroma import Chroma
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from abc import ABC

from .confs import (
    EMBEDDINGS_API_KEY_NAME,
    EMBEDDINGS_MODEL,
    PERSIST_DIR,
    COLLECTION_NAME,
)
from .utils.get_secret import get_secret


embeddings = GoogleGenerativeAIEmbeddings(
    model=EMBEDDINGS_MODEL, google_api_key=get_secret(EMBEDDINGS_API_KEY_NAME)
)

vectorstore = Chroma(
    collection_name=COLLECTION_NAME,
    embedding_function=embeddings,
    persist_directory=PERSIST_DIR,
)


class __AbstractVectorDB(ABC):
    __instance: Chroma

    def __init__(self):
        super().__init__()
        self.__instance = self._init_instance()

    def get_instance(self) -> Chroma:
        raise NotImplementedError

    def _init_instance(self) -> Chroma:
        raise NotImplementedError


class __VectorDB(__AbstractVectorDB):
    __instance: Chroma

    def __init__(self):
        super().__init__()

    def get_instance(self) -> Chroma:
        if self.__instance:
            return self.__instance

        return self._init_instance()

    def _init_instance(self):
        vectorstore = Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=embeddings,
            persist_directory=PERSIST_DIR,
        )

        return vectorstore


def get_instance() -> Chroma:
    return __VectorDB().get_instance()
