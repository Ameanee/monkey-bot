import os
import psycopg2


class db:
    def __init__(self):
        self.conn = psycopg2.connect(os.environ["DATABASE_URL"])
        self.cur = self.conn.cursor()
        self.cache = {
            "chanels": {}
        }

    def balance(self, id: str):
        self.cur.execute("SELECT money FROM users WHERE id = %s", (str(id),))

        return self.cur.fetchone()[0]

    def is_user(self, id: str):
        self.cur.execute("SELECT * FROM users WHERE id = %s", (str(id),))
        
        return self.cur.fetchone() is not None

    def new_user(self, id: str):
        self.cur.execute("INSERT INTO users (id, money, monkeys) VALUES (%s, %s, %s)", (str(id), 100, []))

        self.conn.commit()

    def add_money(self, id: str, amount: int):
        self.cur.execute(f"UPDATE users SET money = money + {amount} WHERE id = %s", (str(id), ))

        self.conn.commit()