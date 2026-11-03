import sqlite3

DATABASE_NAME = "chat_history.db"


# Connect to database and create table
def create_database():

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            feature TEXT NOT NULL,

            question TEXT NOT NULL,

            answer TEXT NOT NULL,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
    """)

    connection.commit()

    connection.close()


# Save conversation
def save_conversation(feature, question, answer):

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO conversations (feature, question, answer)

        VALUES (?, ?, ?)
    """, (feature, question, answer))

    connection.commit()

    connection.close()


# Retrieve all conversations
def get_conversations():

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, feature, question, answer, created_at

        FROM conversations

        ORDER BY id DESC
    """)

    conversations = cursor.fetchall()

    connection.close()

    return conversations


# Delete all conversations
def delete_all_conversations():

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("DELETE FROM conversations")

    connection.commit()

    connection.close()