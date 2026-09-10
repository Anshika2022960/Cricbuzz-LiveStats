import sqlite3


def get_connection():
    connection = sqlite3.connect(
        "database/cricket.db",
        check_same_thread=False
    )

    return connection