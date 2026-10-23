import requests
import streamlit as st
import pandas as pd

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Document Manager",
    page_icon=None,
    layout="wide"
)

# Authentication Check

if (
    "token" not in st.session_state
    or not st.session_state.token
):

    st.error(
        "Please login first."
    )

    st.stop()

st.title("My Documents")

response = requests.get(
    f"{API_URL}/documents",
    headers={
        "Authorization":
        f"Bearer {st.session_state.token}"
    }
)

if response.status_code != 200:

    st.error(
        response.text
    )

    st.stop()

documents = response.json().get(
    "documents",
    []
)

if len(documents) == 0:

    st.warning(
        "No documents uploaded."
    )

else:

    df = pd.DataFrame(
        documents
    )

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader(
        "Delete Document"
    )

    selected_doc = st.selectbox(
        "Choose Document",
        options=[
            doc["filename"]
            for doc in documents
        ]
    )

    if st.button(
        "Delete Document"
    ):

        delete_response = requests.delete(
            f"{API_URL}/documents/{selected_doc}",
            headers={
                "Authorization":
                f"Bearer {st.session_state.token}"
            }
        )

        if delete_response.status_code == 200:

            st.success(
                delete_response.json()["message"]
            )

            st.rerun()
