import streamlit as st
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from confs import ACCEPT_DOCS_FORMATS
from services.vectorstore import get_instance as get_vs_instance
from services.llm import get_instance as get_llm_instance
from utils import load_documents as ld


is_processing: bool = False
st.container(
    horizontal_alignment="center",
    vertical_alignment="center",
).title("Docs Reviewer 📙📖 😀")

chat_input = st.chat_input(
    placeholder="Review/query these docs for me...",
    accept_file="multiple",
    file_type=ACCEPT_DOCS_FORMATS,
)

if chat_input:
    status = st.status(
        "Processing request...", state="complete" if is_processing else "running"
    )
    files = chat_input.files
    query = chat_input.text
    status.write("Got chat inputs...")

    documents = ld.load_documents(files)  # type: ignore
    status.write("Loaded files into documents...")

    splitted: list[list[Document]] = []
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=200,
    )

    for doc in documents:
        splitted.append(splitter.split_documents(doc))
    status.write("Splitted documents...")

    vectorstore = get_vs_instance()
    llm = get_llm_instance()

    doc_ids = [vectorstore.add_documents(doc) for doc in splitted]

    results: list[Document] = vectorstore.similarity_search(query, k=8)
    status.write("Got relevant documents...")

    # mount prompt
    status.write("Assembling prompt...")
    docs_str = ""
    for doc in results:
        docs_str += doc.page_content + "\n"

    prompt = f"context: \n{docs_str}\n\nquestion: {query}"

    status.write("Invoked llm...")
    res = llm.invoke(prompt)

    if res.content: # type: ignore
        with st.chat_message("assistant"):
            st.write(res.content) # type: ignore

    [vectorstore.delete(docs_id) for docs_id in doc_ids]
    is_processing = True
