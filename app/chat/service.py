from app.chat.database import (
    get_all_chats,
    get_user_chats,
    get_most_active_users
)


def fetch_chat_history():

    rows = get_all_chats()

    chats = []

    for row in rows:

        chats.append(
            {
                "id": row[0],
                "username": row[1],
                "question": row[2],
                "answer": row[3],
                "created_at": row[4]
            }
        )

    return chats


def fetch_user_chat_history(
    username
):

    rows = get_user_chats(
        username
    )

    chats = []

    for row in rows:

        chats.append(
            {
                "id": row[0],
                "username": row[1],
                "question": row[2],
                "answer": row[3],
                "created_at": row[4]
            }
        )

    return chats


def fetch_all_chat_history():

    rows = get_all_chats()

    chats = []

    for row in rows:

        chats.append(
            {
                "id": row[0],
                "username": row[1],
                "question": row[2],
                "answer": row[3],
                "created_at": row[4]
            }
        )

    return chats


def fetch_most_active_users():

    rows = get_most_active_users()

    users = []

    for row in rows:

        users.append(
            {
                "username": row[0],
                "total_chats": row[1]
            }
        )

    return users