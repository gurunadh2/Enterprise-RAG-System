import sqlite3


DATABASE_NAME = "feedback.db"


def initialize_database():

    conn = sqlite3.connect(
        DATABASE_NAME
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            rating TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    conn.commit()

    conn.close()


def save_feedback(
    question,
    answer,
    rating
):

    conn = sqlite3.connect(
        DATABASE_NAME
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO feedback (
            question,
            answer,
            rating
        )
        VALUES (?, ?, ?)
        """,
        (
            question,
            answer,
            rating
        )
    )

    conn.commit()

    conn.close()