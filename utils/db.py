import sqlite3


class BotDB:
    def __init__(self, db_file_name) -> None:
        self.db_file_name = db_file_name
    
    def open(self):
        self.conn = sqlite3.connect(self.db_file_name)
        self.cursor = self.conn.cursor()

    def update(self, data_name, new_data, user_id):
        if new_data != None or 'None':
            self.cursor.execute(f'''
                UPDATE users
                SET {data_name} = (?)
                WHERE id = (?)
            ''', (new_data, user_id))
            self.conn.commit()
        else:
            print('None')

    def get_user_by_id(self, user_id):
        self.cursor.execute("""
            SELECT *
            FROM users
            WHERE id = ?
        """, (user_id,))
        user_data = self.cursor.fetchone()
        if user_data:
            user_id, first_name, last_name, user_name = user_data
            return f"ID: {user_data[0]}\nFirst Name: {first_name}\nLast Name: {last_name}\nUser Name: {user_name} @{user_name}"
        else:
            return "Користувача не знайдено"
        
    def get_user_by_name(self, first_name):
        self.cursor.execute("""
            SELECT *
            FROM users
            WHERE LOWER(first_name) = LOWER(?)
        """, (first_name,))
        users = self.cursor.fetchall()
        if users:
            result = ""
            for user_id, first_name, last_name, user_name in users:
                result += f"ID: {user_id}\nFirst Name: {first_name}\nLast Name: {last_name}\nUser Name: {user_name} @{user_name}\n\n"
            return result
        else:
            return "Користувача не знайдено"
    
    def user_exists(self, user_id):
        self.cursor.execute("""
        SELECT COUNT(*)
        FROM users
        WHERE id = ?
        """, (user_id, ))
        is_user_exists = self.cursor.fetchone()[0]
        return bool(is_user_exists)
    
    def add_user_to_db(self, user_id, first_name, last_name, username):
        self.cursor.execute("""
            INSERT INTO users (id, first_name, last_name, user_name)
            VALUES (?, ?, ?, ?)
        """, (user_id, first_name, last_name, username))
        self.conn.commit()

    def remove_user_from_db(self, user_id):
        self.cursor.execute("""
            DELETE FROM users WHERE id = ?
        """, (user_id, ))
        self.conn.commit()


    def create_default_table(self):
        """ Creating default table users with fields id, first_name, last_name, user_name"""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                first_name VARCHAR(255),
                last_name VARCHAR(255),
                user_name VARCHAR(255)
            );
        """)
        return self.conn.commit()


    def close(self):
        if hasattr(self, 'conn'):
            self.conn.close()