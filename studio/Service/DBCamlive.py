import sqlite3

class DatabaseManager:

    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def create_table(self):
        try:
            create_table_sql = """
    
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    password TEXT NOT NULL
                );

                --DROP TABLE IF EXISTS sessions;
                CREATE TABLE IF NOT EXISTS sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                    name TEXT NOT NULL,
                    created_at Date DEFAULT CURRENT_DATE,
                    update_at Date DEFAULT CURRENT_DATE,
                    fk_user INTEGER NOT NULL,
                    FOREIGN KEY(fk_user) REFERENCES users(id) ON DELETE CASCADE
                );

                --DROP TABLE IF EXISTS configs;
                CREATE TABLE IF NOT EXISTS configs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                    name TEXT DEFAULT NULL,
                    reference TEXT DEFAULT NULL,
                    fk_session INTEGER NOT NULL,
                    FOREIGN KEY(fk_session) REFERENCES sessions(id) ON DELETE CASCADE
                );

                --DROP TABLE IF EXISTS camlists;
                CREATE TABLE IF NOT EXISTS camlists (
                    id INTEGER DEFAULT NULL,
                    tab_id TEXT PRIMARY KEY,
                    cam_label TEXT DEFAULT NULL,
                    save BOOLEAN DEFAULT FALSE,
                    format TEXT DEFAULT NULL,
                    fk_session INTEGER NOT NULL,
                    FOREIGN KEY(fk_session) REFERENCES sessions(id) ON DELETE CASCADE
                );

                --DROP TABLE IF EXISTS traitements;
                CREATE TABLE IF NOT EXISTS traitements (
                    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                    type_objet TEXT DEFAULT 'personne',
                    detect_path TEXT DEFAULT NULL,
                    face REAL DEFAULT 0,
                    profile REAL DEFAULT 0,
                    eye REAL DEFAULT 0,
                    fk_cam TEXT NOT NULL,
                    fk_session INTEGER NOT NULL,
                    FOREIGN KEY(fk_cam) REFERENCES camlists(tab_id) ON DELETE CASCADE,
                    FOREIGN KEY(fk_session) REFERENCES sessions(id) ON DELETE CASCADE
                );
                """
            self.cursor.execute("""
			    PRAGMA foreign_keys = ON
			""")
            self.cursor.executescript(create_table_sql)
            print('create db')
        except sqlite3.Error as e:
            print(e)

    def insert_data(self, insert_sql, data):
        try:
            self.cursor.execute(insert_sql, data)
            self.connection.commit()
        except sqlite3.Error as e:
            print(e)

    def update_data(self, update_sql, data):
        try:
            self.cursor.execute(update_sql, data)
            self.connection.commit()
        except sqlite3.Error as e:
            print(e)

    def fetch_data(self, select_sql=None, data=None):
        try:
            if data:
                self.cursor.execute(select_sql, data)
            else:   
                self.cursor.execute(select_sql)
            rows = self.cursor.fetchall()
            return rows
        except sqlite3.Error as e:
            print(e)
            return None

    def close_connection(self):
        self.connection.close()

# if __name__ == "__main__":
#     db_manager = DatabaseManager("example.db")
    
#     create_table_sql = """
#     CREATE TABLE IF NOT EXISTS users (
#         id INTEGER PRIMARY KEY,
#         name TEXT NOT NULL,
#         age INTEGER
#     );
#     """
#     db_manager.create_table(create_table_sql)

#     insert_sql = "INSERT INTO users (name, age) VALUES (?, ?)"
#     db_manager.insert_data(insert_sql, ("Alice", 30))
#     db_manager.insert_data(insert_sql, ("Bob", 25))

#     update_sql = "UPDATE users SET age = ? WHERE name = ?"
#     db_manager.update_data(update_sql, (31, "Alice"))

#     select_sql = "SELECT * FROM users"
#     rows = db_manager.fetch_data(select_sql)
#     for row in rows:
#         print(row)

#     db_manager.close_connection()
