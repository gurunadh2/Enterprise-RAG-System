import requests
import streamlit as st
import pandas as pd
import plotly.express as px

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Admin Dashboard",
    page_icon="ðŸ“ˆ",
    layout="wide"
)

# -------------------------
# Authentication Check
# -------------------------

# Authentication Check

if (
    "token" not in st.session_state
    or not st.session_state.token
):

    st.error(
        "Please login first."
    )

    st.stop()

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
        "â›” Access Denied"
    )

    st.warning(
        "You are not authorized to access the Admin Dashboard."
    )

    st.stop()

# -------------------------
# Dashboard
# -------------------------

st.title(
    "Enterprise RAG Admin Dashboard"
)

response = requests.get(
    f"{API_URL}/admin/stats"
)

stats = response.json()

# KPI Cards

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Documents",
    stats["total_documents"]
)

col2.metric(
    "Chunks",
    stats["total_chunks"]
)

col3.metric(
    "Chats",
    stats["total_chats"]
)

col4.metric(
    "Feedback",
    stats["total_feedback"]
)

col5.metric(
    "â­ Helpful %",
    f"{stats['helpful_percentage']}%"
)

st.divider()

# Overview Chart

chart_df = pd.DataFrame(
    {
        "Metric": [
            "Documents",
            "Chunks",
            "Chats",
            "Feedback"
        ],
        "Count": [
            stats["total_documents"],
            stats["total_chunks"],
            stats["total_chats"],
            stats["total_feedback"]
        ]
    }
)

fig = px.bar(
    chart_df,
    x="Metric",
    y="Count",
    title="System Overview"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# System Health

st.subheader(
    "âš™ï¸ System Health"
)

health_df = pd.DataFrame(
    {
        "Component": [
            "LLM",
            "Vector Database",
            "Retrieval",
            "Chat History",
            "Feedback System"
        ],
        "Status": [
            "Active",
            "Active",
            "Hybrid",
            "Active",
            "Active"
        ]
    }
)

st.dataframe(
    health_df,
    use_container_width=True,
    hide_index=True
)

st.divider()

st.subheader(
    "Registered Users"
)

users_response = requests.get(
    f"{API_URL}/admin/users"
)

users_df = pd.DataFrame(
    users_response.json()["users"]
)

st.dataframe(
    users_df,
    use_container_width=True,
    hide_index=True
)

st.divider()

st.subheader(
    "Active Users"
)

active_response = requests.get(
    f"{API_URL}/admin/active-users"
)

active_df = pd.DataFrame(
    active_response.json()["users"]
)

st.dataframe(
    active_df,
    use_container_width=True,
    hide_index=True
)
