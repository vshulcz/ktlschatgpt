import sqlite3


class ChatUser:
    def __init__(
        self,
        user_id: int,
    ) -> None:
        self.user_id = user_id
        self.chat_history = []


class ChatMessage:
    def __init__(
        self,
        role: str,
        content: str,
    ) -> None:
        self.role = role
        self.content = content


class ChatDatabase:
    """SQL database for users chat history."""

    def __init__(
        self,
        db_name: str,
    ) -> None:
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.cursor.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY
            );

            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER REFERENCES users(id),
                role TEXT,
                content TEXT
            );
            """
        )
        self.conn.commit()

    def add_message(
        self,
        user: ChatUser,
        role: str,
        content: str,
    ) -> str:
        self.cursor.execute(
            "INSERT INTO messages (user_id, role, content) VALUES(?, ?, ?)",
            (user.user_id, role, content),
        )
        self.conn.commit()
        message_id = self.cursor.lastrowid
        message = ChatMessage(role, content)
        user.chat_history.append(message)

        return message

    def get_or_create_user(
        self,
        user_id: int,
    ) -> ChatUser:
        self.cursor.execute(f"SELECT id FROM users WHERE id = {user_id}")
        user_data = self.cursor.fetchone()

        if user_data:
            user_id = user_data[0]
            return ChatUser(user_id)
        else:
            self.cursor.execute(f"INSERT INTO users (id) VALUES ({user_id})")
            self.conn.commit()
            return ChatUser(user_id)

    def set_user_history(
        self,
        user: ChatUser,
    ) -> None:
        self.cursor.execute(f"DELETE FROM messages WHERE user_id = {user.user_id}")
        self.conn.commit()

    def get_user_history(
        self,
        user: ChatUser,
    ) -> list:
        self.cursor.execute(
            f"SELECT role, content FROM messages WHERE user_id = {user.user_id}"
        )
        rows = self.cursor.fetchall()
        user.chat_history = [
            {"role": role, "content": content} for role, content in rows
        ]

        return user.chat_history

    def close(
        self,
    ) -> None:
        self.conn.close()
