import streamlit as st

from confs import ACCEPT_DOCS_FORMATS
from services.llm import get_instance as get_llm_instance
from services.logging import Log, LEVEL
from utils.single_query_docs import single_query_docs
from dto.UI.chat_state import ChatState


LOG_ORIGIN = "app.pages.home"

# App persistent states
if "state" not in st.session_state:
    stt: ChatState = {
        "label": "",
        "state": "complete",
        "query_tasks": [],
        "messages": [],
    }
    st.session_state.state = stt

st.title("Docs Reviewer 📙📖 😀")

status_container = st.empty()

chat_input = st.chat_input(
    placeholder="Review/query these docs for me...",
    accept_file="multiple",
    file_type=ACCEPT_DOCS_FORMATS,
)

if st.session_state.state["label"]:
    label = st.session_state.state["label"]
    state = st.session_state.state["state"]
    query_tasks = st.session_state.state["query_tasks"]
    status = status_container.status(label=label, state=state)

    for task in query_tasks:
        status.write(task)

if st.session_state.state["messages"]:
    for msg in st.session_state.state["messages"]:
        with st.chat_message("assistant"):
            st.write(msg)

if chat_input:
    files = chat_input.files
    query = chat_input.text

    log = Log(LEVEL.INFO, "Processing query request.", LOG_ORIGIN)
    print(log)

    query_tasks: list[str] = []
    status = status_container.status(
        label="Processing request...",
        state="running",
    )
    status.write("Got chat inputs...")
    query_tasks.append("Got chat inputs. ✅")

    results = []
    if files:
        log1 = Log(
            LEVEL.INFO, "Processing query request using input files.", LOG_ORIGIN
        )
        print(log1)
        results = single_query_docs(query, files)
        status.write("Got relevant docs...")
        query_tasks.append("Got relevant docs. ✅")

    # mount prompt
    log2 = Log(LEVEL.INFO, "Mounting full llm prompt.", LOG_ORIGIN)
    print(log2)
    status.write("Assembling prompt...")
    query_tasks.append("Assembling prompt. ✅")
    docs_str = ""
    if results:
        for doc in results:
            docs_str += doc.page_content + "\n"

    prompt = f"context: \n{docs_str}\n\nquestion: {query}"

    status.write("Invoked llm...")
    query_tasks.append("Invoked llm. ✅")
    llm = get_llm_instance()
    res = llm.invoke(prompt)
    log4 = Log(LEVEL.INFO, f"Invoked llm with prompt: {prompt[:45]}.", LOG_ORIGIN)

    messages = st.session_state.state["messages"]
    if res.content:  # type: ignore
        log3 = Log(LEVEL.INFO, f"Got llm response: {res.text()[:40]}", LOG_ORIGIN)
        print(log3)
        messages = [res.text()]  # Use only the previous message

    st.session_state.state = {
        "label": "Completed",
        "state": "complete",
        "query_tasks": query_tasks,
        "messages": messages,
    }
    st.rerun()
