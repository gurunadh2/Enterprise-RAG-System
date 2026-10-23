
import os

import requests
import streamlit as st
from dotenv import load_dotenv
from streamlit_cookies_manager import EncryptedCookieManager

load_dotenv()

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

COOKIE_PASSWORD = os.getenv("COOKIE_PASSWORD", "")
if not COOKIE_PASSWORD:
    raise RuntimeError("COOKIE_PASSWORD environment variable is required")

cookies = EncryptedCookieManager(
    prefix="enterprise_rag_",
    password=COOKIE_PASSWORD
)


if not cookies.ready():

    st.stop()

# Normalize cookies

saved_token = cookies.get(
    "token"
)

saved_username = cookies.get(
    "username"
)

if saved_token == "":

    saved_token = None

if saved_username == "":

    saved_username = None

st.set_page_config(
    page_title="Enterprise RAG",
    page_icon=None,
    layout="wide"
)

# Session State

if "token" not in st.session_state:

    st.session_state.token = saved_token

if "username" not in st.session_state:

    st.session_state.username = saved_username

if "messages" not in st.session_state:

    st.session_state.messages = []

# Verify stored token

if st.session_state.token:

    try:

        verify_response = requests.post(
            f"{API_URL}/verify-token",
            params={
                "token": st.session_state.token
            }
        )

        if verify_response.status_code != 200:

            cookies["token"] = ""

            cookies["username"] = ""

            cookies.save()

            st.session_state.token = None

            st.session_state.username = None

            st.session_state.messages = []

            st.rerun()

    except Exception:

        pass

# Login / Register Screen

if not st.session_state.token:

    st.title("Enterprise RAG")

    login_tab, register_tab, forgot_tab = st.tabs(
        [
            "Login",
            "Register",
            "Forgot Password"
        ]
    )

    # Login Tab

    with login_tab:

        username = st.text_input(
            "Username",
            key="login_username"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button(
            "Login",
            key="login_button"
        ):

            response = requests.post(
                f"{API_URL}/login",
                json={
                    "username": username,
                    "password": password
                }
            )

            result = response.json()

            token = result.get(
                "access_token"
            )

            if token:

                st.session_state.token = token

                me_response = requests.get(
                    f"{API_URL}/me",
                    headers={
                        "Authorization":
                        f"Bearer {token}"
                    }
                )

                if me_response.status_code == 200:

                    st.session_state.username = (
                        me_response.json()["username"]
                    )

                    cookies["token"] = token

                    cookies["username"] = (
                        st.session_state.username
                    )

                    cookies.save()

                st.success(
                    "Login successful"
                )

                st.rerun()

            else:

                st.error(
                    "Invalid credentials"
                )

    # Register Tab

    with register_tab:

        new_username = st.text_input(
            "Username",
            key="register_username"
        )

        new_password = st.text_input(
            "Password",
            type="password",
            key="register_password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            key="register_confirm_password"
        )

        if st.button(
            "Create Account",
            key="register_button"
        ):

            if not new_username:

                st.error(
                    "Username is required"
                )

            elif not new_password:

                st.error(
                    "Password is required"
                )

            elif new_password != confirm_password:

                st.error(
                    "Passwords do not match"
                )

            else:

                response = requests.post(
                    f"{API_URL}/register",
                    json={
                        "username": new_username,
                        "password": new_password
                    }
                )

                result = response.json()

                if result["message"] == "User registered successfully":

                    st.success(
                        "Account created successfully. Please login."
                    )

                else:

                    st.error(
                        result["message"]
                    )

    # Forgot Password Tab

    with forgot_tab:

        st.subheader(
            "Forgot Password"
        )

        st.info(
            """
            This feature is coming soon.

            Future version will support:

            â€¢ Email verification
            â€¢ OTP reset
            â€¢ Secure password recovery
            """
        )

        st.warning(
            "For now, contact the administrator if you forget your password."
        )

    st.stop()

# Sidebar

with st.sidebar:

    st.title("Enterprise RAG")

    if st.session_state.username:

        st.success(
            f"Logged in as: {st.session_state.username}"
        )

    if st.button("Logout"):

        cookies["token"] = ""

        cookies["username"] = ""

        cookies.save()

        st.session_state.token = None

        st.session_state.username = None

        st.session_state.messages = []

        st.rerun()

    st.markdown("---")

    ADMIN_USERS = ["guru"]

    menu = [
        "Chat",
        "Chat History",
        "Document Manager",
        "Analytics"
    ]

    if st.session_state.username in ADMIN_USERS:

        menu.extend(
            [
                "Admin Dashboard",
                "Admin Chats"
            ]
        )

    selected_page = st.radio(
        "Navigation",
        menu
    )

    st.markdown("---")

    st.subheader("System Info")

    st.write("LLM: llama3")
    st.write("Vector DB: Qdrant")
    st.write("Retrieval: Hybrid")
    st.write("Top-K: 5")

    st.markdown("---")

    if (
        st.session_state.username
        in ADMIN_USERS
    ):

        st.markdown("---")

        st.subheader(
            "Admin Dashboard"
        )

        stats_response = requests.get(
            f"{API_URL}/admin/stats"
        )

        users_response = requests.get(
            f"{API_URL}/admin/active-users"
        )

        if (
            stats_response.status_code == 200
            and users_response.status_code == 200
        ):

            stats = stats_response.json()

            active_users = (
                users_response.json()["users"]
            )

            st.metric(
                "Users",
                stats["total_users"]
            )

            st.metric(
                "Documents",
                stats["total_documents"]
            )

            st.metric(
                "Chats",
                stats["total_chats"]
            )

            st.metric(
                "Feedback %",
                stats["helpful_percentage"]
            )

            with st.expander(
                "Most Active Users"
            ):

                for user in active_users:

                    st.write(
                        f"{user['username']} "
                        f"({user['total_chats']} chats)"
                    )

    st.markdown("---")

    st.subheader("Document Filter")

    try:

        docs_response = requests.get(
            f"{API_URL}/documents",
            headers={
                "Authorization":
                f"Bearer {st.session_state.token}"
            }
        )

        if docs_response.status_code == 200:

            documents = docs_response.json()[
                "documents"
            ]

            document_names = [
                doc["filename"]
                for doc in documents
            ]

        else:

            document_names = []

    except Exception:

        document_names = []

    selected_documents = st.multiselect(
        "Choose documents",
        options=document_names,
        default=document_names
    )

    st.markdown("---")

    st.subheader("Upload PDF")

    uploaded_file = st.file_uploader(
        "Choose PDF",
        type=["pdf"]
    )

    if st.button("Upload"):

        if uploaded_file:

            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file,
                    "application/pdf"
                )
            }

            response = requests.post(
                f"{API_URL}/upload",
                headers={
                    "Authorization":
                    f"Bearer {st.session_state.token}"
                },
                files=files
            )

            if response.status_code == 200:

                st.success(
                    response.json()["message"]
                )

                st.rerun()

            else:

                st.error(
                    response.text
                )

if selected_page == "Chat":

    st.title(
        "Enterprise RAG Assistant"
    )

    for message in st.session_state.messages:

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )

    question = st.chat_input(
        "Ask anything about your documents..."
    )

    if question:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message("user"):

            st.markdown(question)

        response = requests.post(
            f"{API_URL}/query",
            headers={
                "Authorization":
                f"Bearer {st.session_state.token}"
            },
            json={
                "question": question,
                "source_filter": selected_documents
            }
        )

        if response.status_code != 200:

            st.error(
                response.text
            )

            st.stop()

        result = response.json()

        answer = result["answer"]

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        st.rerun()

# Page Navigation

if selected_page == "Chat":

    pass

elif selected_page == "Chat History":

    with open(
        "frontend/views/chat_history.py",
        encoding="utf-8"
    ) as f:

        exec(f.read())

elif selected_page == "Document Manager":

    with open(
        "frontend/views/document_manager.py",
        encoding="utf-8"
    ) as f:

        exec(f.read())

elif selected_page == "Analytics":

    with open(
        "frontend/views/analytics.py",
        encoding="utf-8"
    ) as f:

        exec(f.read())

elif selected_page == "Admin Dashboard":

    with open(
        "frontend/views/admin_dashboard.py",
        encoding="utf-8"
    ) as f:

        exec(f.read())

elif selected_page == "Admin Chats":

    with open(
        "frontend/views/admin_chats.py",
        encoding="utf-8"
    ) as f:

        exec(f.read())