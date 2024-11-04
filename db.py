import os
import psycopg2


class db:
    def __init__ (self):
        self.conn = psycopg2.connect(
            os.environ["DATABASE_URL"],
            keepalives=1,
            keepalives_idle=60,
            keepalives_interval=10,
            keepalives_count=5
        )
        self.cur = self.conn.cursor()
        self.cache = {
            "chanels": {}
        }

    def balance (self, id: str):
        self.cur.execute("SELECT money FROM users WHERE id = %s", (str(id),))

        return self.cur.fetchone()[0]

    def is_user (self, id: str):
        self.cur.execute("SELECT * FROM users WHERE id = %s", (str(id),))
        
        return self.cur.fetchone() is not None

    def new_user (self, id: str):
        self.cur.execute("INSERT INTO users (id, money, monkeys, inventory) VALUES (%s, %s, %s, %s)", (str(id), 100, [], []))

        self.conn.commit()

    def add_money (self, id: str, amount: int):
        self.cur.execute(f"UPDATE users SET money = money + {amount} WHERE id = %s", (str(id), ))

        self.conn.commit()

    def new_monkey (self, type: str, health: int, damage: int):
        self.cur.execute("INSERT INTO monkeys (type, health, damage) VALUES (%s, %s, %s)", (type, health, damage))

        monkey_id = self.cur.fetchone()[0]

        self.conn.commit()
        return monkey_id