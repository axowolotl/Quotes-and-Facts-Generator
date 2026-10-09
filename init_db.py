import sqlite3

def init_db():
    # Connect to database (creates bot_data.db if it doesn't exist)
    conn = sqlite3.connect("bot_data.db")
    cursor = conn.cursor()

    # Create tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS facts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            author TEXT NOT NULL
        )
    """)

    # Seed initial data if tables are empty
    cursor.execute("SELECT COUNT(*) FROM facts")
    if cursor.fetchone()[0] == 0:
        initial_facts = [
            ("Honey never spoils. You could theoretically eat 3,000-year-old honey.",),
            ("Bananas are berries, but strawberries aren't.",),
            ("Wombat poop is cube-shaped, which stops it from rolling away.",)
        ]
        cursor.executemany("INSERT INTO facts (content) VALUES (?)", initial_facts)

    cursor.execute("SELECT COUNT(*) FROM quotes")
    if cursor.fetchone()[0] == 0:
        initial_quotes = [
            ("The only true wisdom is in knowing you know nothing.", "Socrates"),
            ("An unexamined life is not worth living.", "Socrates"),
            ("It always seems impossible until it's done.", "Nelson Mandela")
        ]
        cursor.executemany("INSERT INTO quotes (content, author) VALUES (?, ?)", initial_quotes)

    conn.commit()
    conn.close()
    print("Database initialized and seeded successfully!")

if __name__ == "__main__":
    init_db()
