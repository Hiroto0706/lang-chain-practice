from typing import Set
from backend.core import run_llm
import streamlit as st


st.header("LangChain Udemy Course- Documentation Helper Bot")
st.subheader("Main Page")

prompt = st.text_input("Prompt", placeholder="Enter your prompt here...")


if (
    "chat_answer_history" not in st.session_state
    and "user_prompt_history" not in st.session_state
    and "chat_history" not in st.session_state
):
    st.session_state["chat_answers_history"] = []
    st.session_state["user_prompt_history"] = []
    st.session_state["chat_history"] = []


def created_source_string(source_urls: Set[str]) -> str:
    if not source_urls:
        return ""
    sources_list = list(source_urls)
    sources_list.sort()
    sources_string = "sources:\n"
    for i, source in enumerate(sources_list, 1):
        sources_string += f"{i}. {source}\n"
    return sources_string


if prompt:
    with st.spinner("Generating response..."):
        generated_response = run_llm(
            query=prompt, chat_history=st.session_state["chat_history"]
        )
        sources = set([
            doc.metadata["sourceURL"]  # doc.metadata["sourceURL"]
            for doc in generated_response["source_documents"]
        ])

        formatted_response = f"{generated_response['result']} \n\n {created_source_string(sources)}"

        st.session_state["user_prompt_history"].append(prompt)
        st.session_state["chat_answers_history"].append(formatted_response)
        st.session_state["chat_history"].append(("human", prompt))
        st.session_state["chat_history"].append(
            ("ai", generated_response["result"]))
        prompt = ""

if st.session_state["chat_answers_history"]:
    for user_query, generatted_response in zip(st.session_state["user_prompt_history"], st.session_state["chat_answers_history"]):
        st.chat_message("user").write(user_query)
        st.chat_message("assistant").write(generatted_response)

custom_css = """
<style>
.stChatMessage {
    overflow-wrap: break-word;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)
