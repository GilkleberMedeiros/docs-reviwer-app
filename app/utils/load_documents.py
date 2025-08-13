from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    CSVLoader,
    Docx2txtLoader,
)
from langchain_core.documents import Document
from io import BytesIO
from typing import Callable
import os
from pathlib import Path

from confs import PROJECT_DIR


LoaderFuncType = Callable[[str | Path], list[Document]]

LOADERS: dict[str, LoaderFuncType] = {
    ".txt": lambda filepath: TextLoader(filepath).load(),
    ".pdf": lambda filepath: PyPDFLoader(filepath).load(),
    ".csv": lambda filepath: CSVLoader(filepath).load(),
    ".docx": lambda filepath: Docx2txtLoader(filepath).load(),
}

TMP_DIR_PATH = Path(PROJECT_DIR).joinpath("tmp_files/")


def load_document(file: BytesIO) -> list[Document]:
    """
    Load a file into a document using the correct langchain [DocumentLoader] class.

    Args:
        file: BytesIO file object or streamlit UploadedFile object.

    Returns:
        The list of documents loaded from a file, list[Document].

    Raises:
        Exception: if don't find correct loader function in [LOADERS] given file extension.
        Exception: if can't remove temporary file.
    """

    TMP_FILE_PATH = TMP_DIR_PATH.joinpath(file.name)

    content = file.getvalue()
    loaded: list[Document]

    with open(TMP_FILE_PATH, "wb") as f:
        f.write(content)
        f.flush()

        file_ext = "." + file.name.split(".")[-1].lower()
        if not LOADERS.get(file_ext):
            raise Exception(
                f"LOADERS doesn't have a loader function for {file_ext} extension."
            )

        loader = LOADERS[file_ext]
        loaded = loader(TMP_FILE_PATH)

    # Try remove when file used
    try:
        os.remove(TMP_FILE_PATH)
    except Exception as e:
        raise Exception(
            f"Unknow exception when removing temp file {TMP_FILE_PATH}. \n{e}"
        )

    return loaded


def load_documents(files: list[BytesIO]) -> list[list[Document]]:
    """Basic for wrap under [load_document] function."""

    loaded: list[list[Document]] = []
    for file in files:
        loaded.append(load_document(file))

    return loaded
