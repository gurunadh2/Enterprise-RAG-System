import requests
import streamlit as st
import pandas as pd

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Admin Chats",
    page_icon="ðŸ’¬",
    layout="wide"
)

# Authentication Check

if (
    "username" not in st.session_state
    or not st.session_state.username
):

    st.error(
        "Please login first."
    )

    st.stop()

ADMIN_USERS = [
    "guru"
]

if (
    st.session_state.username
    not in ADMIN_USERS
):

    st.error(
        "Access Denied"
    )

    st.stop()

st.title(
    "ðŸ’¬ Admin Chat Monitor"
)

response = requests.get(
    f"{API_URL}/admin/chats"
)

if response.status_code != 200:

    st.error(
        response.text
    )

    st.stop()

data = response.json().get(
    "chats",
    []
)

df = pd.DataFrame(
    data
)

st.metric(
    "Total Chats",
    len(df)
)

st.dataframe(
    df,
    use_container_width=True
)
