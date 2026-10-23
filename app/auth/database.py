import sqlite3

DATABASE_NAME = "users.db"


def initialize_user_database():

    conn = sqlite3.connect(
        DATABASE_NAME
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    conn.commit()

    conn.close()


def create_user(
    username,
    password_hash
):

    try:

        conn = sqlite3.connect(
            DATABASE_NAME
        )

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO users (
                username,
                password_hash
            )
            VALUES (?, ?)
            """,
            (
                username,
                password_hash
            )
        )

        conn.commit()

        conn.close()

        return True

    except sqlite3.IntegrityError:

        return False


def get_user_by_username(
    username
):

    conn = sqlite3.connect(
        DATABASE_NAME
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE username = ?
        """,
        (
            username,
        )
    )

    user = cursor.fetchone()

    conn.close()

    return user


def get_all_users():

    conn = sqlite3.connect(
        DATABASE_NAME
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM users
        ORDER BY created_at DESC
        """
    )

    rows = cursor.fetchall()

    conn.close()

    return rows


def delete_user(
    username
):

    conn = sqlite3.connect(
        DATABASE_NAME
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM users
        WHERE username = ?
        """,
        (
            username,
        )
    )

    deleted = cursor.rowcount

    conn.commit()

    conn.close()

    return deleted > 0