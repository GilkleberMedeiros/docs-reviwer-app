"""
Llm model handler, guarantees one instance/connection across application and pre-confs.
"""

from langchain_google_genai.llms import ChatGoogleGenerativeAI
from abc import ABC

from app.confs import LLM_MODEL


class __AbstractLlmModel(ABC):
    __instance: ChatGoogleGenerativeAI

    def __init__(self) -> None:
        super().__init__()
        self.__instance = self._init_instance()

    def get_instance(self) -> ChatGoogleGenerativeAI:
        raise NotImplementedError()

    def _init_instance(self) -> ChatGoogleGenerativeAI:
        raise NotImplementedError()


class LlmModel(__AbstractLlmModel):
    __instance: ChatGoogleGenerativeAI

    def __init__(self) -> None:
        super().__init__()

    def get_instance(self) -> ChatGoogleGenerativeAI:
        if self.__instance:
            return self.__instance

        return self._init_instance()

    def _init_instance(self) -> ChatGoogleGenerativeAI:
        llm = ChatGoogleGenerativeAI(model=LLM_MODEL)

        return llm


def get_instance() -> ChatGoogleGenerativeAI:
    return LlmModel().get_instance()
