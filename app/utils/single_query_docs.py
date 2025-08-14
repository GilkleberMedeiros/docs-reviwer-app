from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from streamlit.runtime.uploaded_file_manager import UploadedFile
from io import BytesIO

from services.vectorstore import get_instance
from services.logging import Log, LEVEL
from utils.load_documents import load_document
from confs import DEFAULT_K, DEFAULT_CHUNK_SIZE, DEFAULT_CHUNK_OVERLAP


def single_query_doc(
    query: str,
    file: BytesIO | UploadedFile,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
    num_results: int = DEFAULT_K,
) -> list[Document]:
    """
    Does similarity search on documents that will last only one search.

    Args:
        query: query string to use on similarity search.
        file: file to load and get results.
        chunk_size: chunk_size param to text splitters, defaults to app [DEFAULT_CHUNK_SIZE].
        chunk_overlap: chunk_overlap param to text splitters, defaults to app [DEFAULT_CHUNK_OVERLAP].
        num_results: number of results to return from similarity search, defaults to app [DEFAULT_K].

    Retuns:
        The list of results from similarity search.
    """
    try:
        vectorstore = get_instance()

        documents = load_document(file)
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

        splitted = splitter.split_documents(documents)

        doc_ids = vectorstore.add_documents(splitted)

        results = vectorstore.similarity_search(query, k=num_results)

        vectorstore.delete(doc_ids)
    except Exception as e:
        raise Exception(
            f"Unknow exception when managing single query docs!\nException: \n{e}"
        )

    return results


def single_query_docs(
    query: str,
    files: list[BytesIO] | list[UploadedFile],
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
    num_results: int = DEFAULT_K,
) -> list[list[Document]]:
    """
    Does similarity search on documents that will last only one search.
    This is basically a for around [single_query_doc]. see [single_query_doc] docs
    to see more details on params, returns, raises, etc...
    """
    results: list[list[Document]] = []
    for file in files:
        results.append(
            single_query_doc(query, file, chunk_size, chunk_overlap, num_results)
        )

    log = Log(
        LEVEL.INFO,
        f"Got {len([item for sublist in results for item in sublist])}",
        "utils.single_query_docs.single_query_docs",
    )
    print(log)

    return results
