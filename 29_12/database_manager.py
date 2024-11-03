import sqlite3

class DatabaseManager:
    def __init__(self, db_filename="books.db"):
        self.db_filename = db_filename
        self.create_db()

    def create_db(self):
        conn = sqlite3.connect(self.db_filename)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                author TEXT NOT NULL,
                title TEXT NOT NULL,
                year INTEGER NOT NULL
            );
        """)
        conn.commit()
        conn.close()

    def add_book(self, author, title, year):
        conn = sqlite3.connect(self.db_filename)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO books (author, title, year) VALUES (?, ?, ?);", (author, title, year))
        conn.commit()
        conn.close()

    def find_books(self, author=None, title=None, start_year=None, end_year=None):
        conn = sqlite3.connect(self.db_filename)
        cursor = conn.cursor()
        query = "SELECT author, title, year FROM books WHERE 1=1"
        params = []
        if author:
            query += " AND author LIKE ?"
            params.append(f"%{author}%")
        if title:
            query += " AND title LIKE ?"
            params.append(f"%{title}%")
        if start_year:
            query += " AND year >= ?"
            params.append(start_year)
        if end_year:
            query += " AND year <= ?"
            params.append(end_year)

        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        return results
