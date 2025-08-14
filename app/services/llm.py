"""
Llm model handler, guarantees one instance/connection across application and pre-confs.
"""

from langchain_google_genai.llms import ChatGoogleGenerativeAI
from abc import ABC

from confs import LLM_MODEL, LLM_API_KEY_NAME
from utils.get_secret import get_secret
from .logging import Log, LEVEL


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
        self.__instance = self._init_instance()

    def get_instance(self) -> ChatGoogleGenerativeAI:
        if self.__instance:
            log = Log(
                LEVEL.WARNING,
                "LlmModel.get_instance returned same instance!",
                "services.llm.LlmModel",
            )
            print(log)
            return self.__instance

        log = Log(
            LEVEL.WARNING,
            "LlmModel.get_instance returned new instance!",
            "services.llm.LlmModel",
        )
        print(log)
        return self._init_instance()

    def _init_instance(self) -> ChatGoogleGenerativeAI:
        llm = ChatGoogleGenerativeAI(
            model=LLM_MODEL, google_api_key=get_secret(LLM_API_KEY_NAME)
        )

        return llm


def get_instance() -> ChatGoogleGenerativeAI:
    return LlmModel().get_instance()
