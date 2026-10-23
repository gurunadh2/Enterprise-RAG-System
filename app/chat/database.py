import sqlite3

DATABASE_NAME = "chat_history.db"


def initialize_chat_database():

    conn = sqlite3.connect(
        DATABASE_NAME
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    conn.commit()

    conn.close()


def save_chat(
    username,
    question,
    answer
):

    conn = sqlite3.connect(
        DATABASE_NAME
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO chat_history (
            username,
            question,
            answer
        )
        VALUES (?, ?, ?)
        """,
        (
            username,
            question,
            answer
        )
    )

    conn.commit()

    conn.close()


def get_user_chats(
    username
):

    conn = sqlite3.connect(
        DATABASE_NAME
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM chat_history
        WHERE username = ?
        ORDER BY created_at DESC
        """,
        (
            username,
        )
    )

    rows = cursor.fetchall()

    conn.close()

    return rows


def get_all_chats():

    conn = sqlite3.connect(
        DATABASE_NAME
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM chat_history
        ORDER BY created_at DESC
        """
    )

    rows = cursor.fetchall()

    conn.close()

    return rows


def get_most_active_users():

    conn = sqlite3.connect(
        DATABASE_NAME
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            username,
            COUNT(*) as total_chats
        FROM chat_history
        GROUP BY username
        ORDER BY total_chats DESC
        """
    )

    rows = cursor.fetchall()

    conn.close()

    return rows