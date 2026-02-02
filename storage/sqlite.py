import sqlite3
from pathlib import Path

class SQLiteStore:
    def __init__(self, db_path="data/markov.db"):
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(db_path)
        # self.conn.execute("PRAGMA journal_mode=WAL")

    def init_schema(self):
        with open("storage/migrations.sql") as f:
            self.conn.executescript(f.read())

    def record_transition(self, state1, state2, next_word):
        self.conn.execute(
            """
            INSERT INTO transitions (state1, state2, next_word, count)
            VALUES (?, ?, ?, 1)
            ON CONFLICT(state1, state2, next_word)
            DO UPDATE SET count = count + 1
            """,
            (state1, state2, next_word)
        )
        self.conn.commit()

    def get_next_words(self, state1, state2):
        cur = self.conn.execute(
            """
            SELECT next_word, count
            FROM transitions
            WHERE state1 = ? AND state2 = ?
            """,
            (state1, state2)
        )
        return cur.fetchall()

    def get_random_state(self):
        row = self.conn.execute(
            """
            SELECT state1, state2
            FROM transitions
            ORDER BY RANDOM()
            LIMIT 1
            """
        ).fetchone()

        return row if row else (None, None)