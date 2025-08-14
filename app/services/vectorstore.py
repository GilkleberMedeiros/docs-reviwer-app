"""
VectorDB handler, guarantees one instance/connection to vectorDB across application and
exposition of only needed interface.
"""

from langchain_community.vectorstores.chroma import Chroma
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from abc import ABC
import asyncio

from confs import (
    EMBEDDINGS_API_KEY_NAME,
    EMBEDDINGS_MODEL,
    PERSIST_DIR,
    COLLECTION_NAME,
)
from utils.get_secret import get_secret
from .logging import Log, LEVEL


class __AbstractVectorDB(ABC):
    __instance: Chroma

    def __init__(self):
        super().__init__()
        self.__instance = self._init_instance()

    def get_instance(self) -> Chroma:
        raise NotImplementedError

    def _init_instance(self) -> Chroma:
        raise NotImplementedError


class VectorDB(__AbstractVectorDB):
    __instance: Chroma

    def __init__(self):
        super().__init__()
        self.__instance = self._init_instance()

    def get_instance(self) -> Chroma:
        if self.__instance:
            log = Log(
                LEVEL.WARNING,
                "VectorDB.get_instance returned same instance!",
                "services.vectorstore.VectorDB",
            )
            print(log)
            return self.__instance

        log = Log(
            LEVEL.WARNING,
            "VectorDB.get_instance returned new instance!",
            "services.vectorstore.VectorDB",
        )
        print(log)
        return self._init_instance()

    def _init_instance(self):
        # Get or set an event loop. Needed By embeddings creation
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            asyncio.set_event_loop(asyncio.new_event_loop())

        embeddings = GoogleGenerativeAIEmbeddings(
            model=EMBEDDINGS_MODEL, google_api_key=get_secret(EMBEDDINGS_API_KEY_NAME)
        )

        vectorstore = Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=embeddings,
            persist_directory=PERSIST_DIR,
        )

        return vectorstore


def get_instance() -> Chroma:
    return VectorDB().get_instance()
