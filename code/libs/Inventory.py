import sys
import pymysql

class Inventory:
    def __init__(self, sid):
        self.conn = pymysql.connect('localhost', 'root', '', 'hackathon');
        self.curr = self.conn.cursor()
        self.sid = sid;

        self.curr.execute(
        f"""
            CREATE TABLE IF NOT EXISTS {self.sid} (
                sno INT ,
                item VARCHAR(100) PRIMARY KEY,
                quantity INT,
                price FLOAT
            );
        """)

        print(f'Table ({self.sid}) successfully created.')

    def add_item(self, item, quantity, price):
        self.curr.execute(
                f"""
                    SELECT * from {self.sid};
                """)
        sno = int(self.curr.rowcount) + 1;
        self.curr.execute(
        f"""
            INSERT INTO {self.sid}
            (sno,item,quantity,price)
            VALUES (
                {sno},
                "{item}",
                {quantity},
                {price}
            );
        """)
        self.conn.commit()
        print('Items successfully added to {self.sid} table')

if __name__ == '__main__':
    Inventory(sys.argv[1]).add_item(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]));
    # a.add_item('Toothbrush', 10, 115.90);
