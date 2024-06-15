import sqlite3


class SqliteDatabase:
    def __init__(self):
        self.path = './database/database.db'

        self.conn = sqlite3.connect(database=self.path)
        self.cursor = self.conn.cursor()

        # Создаем таблицу, если она не существует
        self.create_table()

    def create_table(self):
        """ Создает таблицу пользователей """
        query = """
        CREATE TABLE IF NOT EXISTS users (
            chat_id INTEGER PRIMARY KEY,
            long_percent INTEGER,
            long_time INTEGER,
            short_percent INTEGER,
            short_time INTEGER,
            pay_time INTEGER,
            is_admin BOOL)
        """
        self.cursor.execute(query)
        self.conn.commit()

    def exists_user(self, chat_id):
        """ Проверить существование пользователя
        Если пользователь существует вернуть True, иначе
        """
        query = "SELECT 1 FROM users WHERE chat_id = ?"
        self.cursor.execute(query, (chat_id,))
        result = self.cursor.fetchone()
        if result:
            return True
        return False

    def new_user(self, chat_id: int):
        """ Добавить пользователя """
        exists_user = self.exists_user(chat_id)
        if exists_user:
            return False

        # Если пользователя нет, добавляем его
        query = "INSERT INTO users (chat_id) VALUES (?)"
        self.cursor.execute(query, (chat_id,))
        self.conn.commit()
        return True

    def update_user(self, chat_id: int, long_percent: int = None, long_time: int = None, short_percent: int = None,
                    short_time: int = None):
        """ Обновить информацию пользователя """

        exists_user = self.exists_user(chat_id)
        if not exists_user:
            return False

        update_params = []
        update_values = []
        if long_percent:
            update_params.append("long_percent = ?")
            update_values.append(long_percent)
        if long_time:
            update_params.append("long_time = ?")
            update_values.append(long_time)
        if short_percent:
            update_params.append("short_percent = ?")
            update_values.append(short_percent)
        if short_time:
            update_params.append("short_time = ?")
            update_values.append(short_time)

        # Формируем запрос
        if update_params:
            query = f"UPDATE users SET {', '.join(update_params)} WHERE chat_id = ?"
            update_values.append(chat_id)
            self.cursor.execute(query, update_values)
            self.conn.commit()
            return True
        else:
            return False

    def get_user(self, chat_id: int):
        """ Получить информацию о пользователе """
        query = "SELECT * FROM users WHERE chat_id = ?"
        self.cursor.execute(query, (chat_id,))
        result = self.cursor.fetchone()
        if result:
            result = {
                'chat_id': chat_id,
                'long_percent': result[1],
                'long_time': result[2],
                'short_percent': result[3],
                'short_time': result[4],
                'pay_time': result[5],
                'is_admin': result[6],
            }
        return result

    def close_connection(self):
        """ Закрыть соединение """
        self.conn.close()
