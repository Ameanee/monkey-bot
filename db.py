import os
import time
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
        self.cur.execute("INSERT INTO users (id, money, monkeys, inventory, lineup) VALUES (%s, %s, %s, %s, %s)", (str(id), 100, [], [], []))

        self.conn.commit()

    def add_money (self, id: str, amount: int):
        self.cur.execute(f"UPDATE users SET money = money + {amount} WHERE id = %s", (str(id), ))

        self.conn.commit()

    def new_monkey (self, type: str, health: int, damage: int, id: str):
        self.cur.execute("INSERT INTO monkeys (type, health, base_health, attack, discovery_id, discovery_date) VALUES (%s, %s, %s, %s, %s, %s)", (type, health, health, damage, id, int(time.time())))

        self.conn.commit()
  
        self.cur.execute("SELECT last_value FROM monkeys_id_seq")
        id = self.cur.fetchone()[0]

        return id

    def add_monkey (self, id: str, monkey_id: int):
        self.cur.execute("UPDATE users SET monkeys = array_append(monkeys, %s) WHERE id = %s", (monkey_id, str(id)))

        self.conn.commit()

    def remove_monkey (self, id: str, monkey_id: int, perm: bool = False):
        self.cur.execute("UPDATE users SET monkeys = array_remove(monkeys, %s) WHERE id = %s", (monkey_id, str(id)))

        if perm:
            self.cur.execute("DELETE FROM monkeys WHERE id = %s", (monkey_id,))

        self.conn.commit()
    
    def get_monkeys (self, id: str):
        self.cur.execute("SELECT monkeys FROM users WHERE id = %s", (str(id),))

        return self.cur.fetchone()[0]

    def get_monkey (self, id: str):
        self.cur.execute("SELECT * FROM monkeys WHERE id = %s", (str(id),)) 
        # (None, 'cyborg monkey', 200, 75, 2, "🐈's server", 1731113365, 200)
        return self.cur.fetchone()