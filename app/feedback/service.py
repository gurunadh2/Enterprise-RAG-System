import sqlite3

DATABASE_NAME = "feedback.db"


def get_all_feedback():

    conn = sqlite3.connect(
        DATABASE_NAME
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            question,
            answer,
            rating,
            created_at
        FROM feedback
        ORDER BY id DESC
        """
    )

    rows = cursor.fetchall()

    conn.close()

    return rows