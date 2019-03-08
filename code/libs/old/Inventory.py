## Inventory List for every shop in shops.shop table

import sqlite3

class Inventory:
    def __init__(self, sid):
        self.sid = sid;
        self.conn = sqlite3.connect('/home/balor/Workspace/Hackathon/db/inventory.db')
        self.curr = self.conn.cursor()

        self.curr.execute(
        f"""
            CREATE TABLE IF NOT EXISTS {self.sid}
            (
                sno INT AUTO_INCREMENT PRIMARY KEY DEFAULT 0,
                item VARCHAR(100) NOT NULL, 
                quantity INT NOT NULL,
                price REAL NOT NULL
            );
        """)

    def add_items(self, item,  quantity, price):
        self.curr.execute(
        f"""
            INSERT INTO {self.sid}
            (item, quantity, price)
            VALUES ("{item}",{quantity},{price});
        """)
        self.conn.commit()
