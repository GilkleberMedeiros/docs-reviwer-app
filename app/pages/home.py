import streamlit as st

from confs import ACCEPT_DOCS_FORMATS
from services.llm import get_instance as get_llm_instance
from utils.single_query_docs import single_query_docs


# App persistent states
st.session_state["is_req_processing"] = False
if "prev_chat_msg" not in st.session_state:
    st.session_state["prev_chat_msg"] = ""

st.container(
    horizontal_alignment="center",
    vertical_alignment="center",
).title("Docs Reviewer 📙📖 😀")

chat_input = st.chat_input(
    placeholder="Review/query these docs for me...",
    accept_file="multiple",
    file_type=ACCEPT_DOCS_FORMATS,
)

if st.session_state.get("prev_chat_msg"):
    status = st.status(
        (
            "Processing request..."
            if st.session_state["is_req_processing"]
            else "Completed"
        ),
        state=("running" if st.session_state["is_req_processing"] else "complete"),
    )
    with st.chat_message("assistant"):
        st.write(st.session_state["prev_chat_msg"])

if chat_input:
    files = chat_input.files
    query = chat_input.text

    st.session_state["is_req_processing"] = True
    status = st.status(
        (
            "Processing request..."
            if st.session_state["is_req_processing"]
            else "Waiting queries..."
        ),
        state=("running" if st.session_state["is_req_processing"] else "complete"),
    )
    status.write("Got chat inputs...")

    results = []
    if files:
        results = single_query_docs(query, files)
        status.write("Got relevant docs...")

    # mount prompt
    status.write("Assembling prompt...")
    docs_str = ""
    if results:
        for docs in results:
            for doc in docs:
                docs_str += doc.page_content + "\n"

    prompt = f"context: \n{docs_str}\n\nquestion: {query}"

    status.write("Invoked llm...")
    llm = get_llm_instance()
    res = llm.invoke(prompt)

    if res.content:  # type: ignore
        with st.chat_message("assistant"):
            st.write(res.text())

    st.session_state["is_req_processing"] = False
    st.session_state["prev_chat_msg"] = res.text()
    st.rerun()
