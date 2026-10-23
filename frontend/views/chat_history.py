import requests
import streamlit as st
import pandas as pd

st.title("Chat History")

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Chat History",
    page_icon="ðŸ’¬",
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

st.title("Chat History")

response = requests.get(
    f"{API_URL}/chat-history",
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

data = response.json().get(
    "chats",
    []
)

if len(data) == 0:

    st.warning(
        "No chat history found."
    )

else:

    st.success(
        f"{len(data)} conversations found"
    )

    df = pd.DataFrame(data)

    csv = df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="â¬‡ï¸ Download Chat History (CSV)",
        data=csv,
        file_name="chat_history.csv",
        mime="text/csv"
    )

    st.divider()

    for chat in data:

        with st.expander(
            f"{chat['question'][:80]}"
        ):

            st.markdown(
                "**Question:**"
            )

            st.write(
                chat["question"]
            )

            st.markdown(
                "**Answer:**"
            )

            st.write(
                chat["answer"]
            )

            st.caption(
                f"Created: {chat['created_at']}"
            )

    st.divider()

    st.subheader(
        "Conversation Table"
    )

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader(
        "Chat Statistics"
    )

    col1, col2 = st.columns(2)

    col1.metric(
        "Total Conversations",
        len(df)
    )

    col2.metric(
        "Average Question Length",
        round(
            df["question"].str.len().mean(),
            1
        )
    )
