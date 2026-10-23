from app.chat.database import (
    get_all_chats
)

from app.feedback.service import (
    get_all_feedback
)

from app.rag.document_manager import (
    get_document_summary
)

from app.auth.database import (
    get_all_users,
    delete_user
)


def get_admin_stats():

    documents = get_document_summary()

    feedbacks = get_all_feedback()

    chats = get_all_chats()

    users = get_all_users()

    total_documents = len(documents)

    total_chunks = sum(
        doc["chunks"]
        for doc in documents
    )

    thumbs_up = 0

    for feedback in feedbacks:

        if feedback[3] == "thumbs_up":

            thumbs_up += 1

    helpful_percentage = 0

    if len(feedbacks) > 0:

        helpful_percentage = round(
            (
                thumbs_up
                / len(feedbacks)
            ) * 100,
            2
        )

    return {
        "total_users": len(users),
        "total_documents": total_documents,
        "total_chunks": total_chunks,
        "total_chats": len(chats),
        "total_feedback": len(feedbacks),
        "helpful_percentage": helpful_percentage
    }


def get_admin_users():

    rows = get_all_users()

    users = []

    for row in rows:

        users.append(
            {
                "id": row[0],
                "username": row[1],
                "created_at": row[3]
            }
        )

    return users


def remove_user(
    username
):

    return delete_user(
        username
    )