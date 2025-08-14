import streamlit as st

from confs import ACCEPT_DOCS_FORMATS
from services.llm import get_instance as get_llm_instance
from services.logging import Log, LEVEL
from utils.single_query_docs import single_query_docs


LOG_ORIGIN = "app.pages.home"

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

    log = Log(LEVEL.INFO, "Processing query request.", LOG_ORIGIN)
    print(log)

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
        log1 = Log(
            LEVEL.INFO, "Processing query request using input files.", LOG_ORIGIN
        )
        print(log1)
        results = single_query_docs(query, files)
        status.write("Got relevant docs...")

    # mount prompt
    log2 = Log(LEVEL.INFO, "Mounting full llm prompt.", LOG_ORIGIN)
    print(log2)
    status.write("Assembling prompt...")
    docs_str = ""
    if results:
        for doc in results:
            docs_str += doc.page_content + "\n"

    prompt = f"context: \n{docs_str}\n\nquestion: {query}"

    status.write("Invoked llm...")
    llm = get_llm_instance()
    res = llm.invoke(prompt)
    log4 = Log(LEVEL.INFO, f"Invoked llm with prompt: {prompt[:45]}.", LOG_ORIGIN)

    if res.content:  # type: ignore
        with st.chat_message("assistant"):
            log3 = Log(LEVEL.INFO, f"Got llm response: {res.text()[:40]}", LOG_ORIGIN)
            st.write(res.text())

    st.session_state["is_req_processing"] = False
    st.session_state["prev_chat_msg"] = res.text()
    st.rerun()
