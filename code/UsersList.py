import sqlite3

class UsersList:
    def __init__(self):
        self.conn = sqlite3.connect("localhost", "root", "", "hackathon")
        self.curr = conn.cursor()
        self.table = "users"

        self.curr.execute(
        f""" 
            CREATE TABLE IF NOT EXISTS {self.table}
            (
                item_name VARCHAR(100) PRIMARY KEY,
                brand_name VARCHAR(100), 
                quantity INT
            );
        """)

    def add(self, item, brand, quantity):
        self.curr.execute(
        f"""
            INSERT INTO {self.table} 
            (item, brand, quantity)
            VALUES (
                "{item}",
                "{brand}",
                {quantity}
            );
        """)
        self.conn.commit();

    def ls(self):
        self.curr.execute(
        f"""
            SELECT * from {self.table};
        """)
        return render_template('./view_lists.html', item_list = self.curr.fetchall())
