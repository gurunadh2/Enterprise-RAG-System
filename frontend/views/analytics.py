import requests
import streamlit as st
import pandas as pd
import plotly.express as px

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Analytics",
    page_icon=None,
    layout="wide"
)

st.title("Enterprise RAG Analytics")

# Fetch system stats

stats_response = requests.get(
    f"{API_URL}/stats"
)



stats = stats_response.json()



# Fetch feedback data

feedback_response = requests.get(
    f"{API_URL}/feedbacks"
)

data = feedback_response.json()["feedbacks"]

# System Metrics

st.subheader("System Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Feedback",
    stats["total_feedback"]
)

col2.metric(
    "Helpful %",
    f"{stats['helpful_percentage']}%"
)

col3.metric(
    "Model",
    stats["model"]
)

col4.metric(
    "Vector DB",
    stats["vector_db"]
)

st.divider()

# Feedback Analytics

st.subheader("Feedback Analytics")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Helpful",
    stats["thumbs_up"]
)

col2.metric(
    "Not Helpful",
    stats["thumbs_down"]
)

col3.metric(
    "Retrieval",
    stats["retrieval"]
)

st.divider()

if len(data) == 0:

    st.warning(
        "No feedback available yet."
    )

else:

    df = pd.DataFrame(data)

    chart_df = pd.DataFrame(
        {
            "Rating": [
                "Helpful",
                "Not Helpful"
            ],
            "Count": [
                stats["thumbs_up"],
                stats["thumbs_down"]
            ]
        }
    )

    fig = px.pie(
        chart_df,
        names="Rating",
        values="Count",
        title="Feedback Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    st.subheader(
        "Recent Feedback"
    )

    st.dataframe(
        df,
        use_container_width=True
    )

    st.divider()

    st.subheader(
        "Feedback Summary"
    )

    summary_df = pd.DataFrame(
        {
            "Metric": [
                "Total Feedback",
                "Helpful",
                "Not Helpful",
                "Helpful Percentage"
            ],
            "Value": [
                stats["total_feedback"],
                stats["thumbs_up"],
                stats["thumbs_down"],
                f"{stats['helpful_percentage']}%"
            ]
        }
    )

    st.dataframe(
        summary_df,
        use_container_width=True,
        hide_index=True
    )
