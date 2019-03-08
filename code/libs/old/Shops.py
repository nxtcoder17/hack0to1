# Inventory System 

import sqlite3;
from Inventory import Inventory

class Shops:
    def __init__(self):
        self.table = "shop"
        self.conn = sqlite3.connect("/home/balor/Workspace/Hackathon/db/shops.db");
        self.curr = self.conn.cursor();

        # Shop columns: SHOPNAME LONGITUDE LATITUDE
        self.curr.execute(
        f"""
            CREATE TABLE IF NOT EXISTS {self.table} (
                sno int NOT NULL,
                sid varchar(20) PRIMARY KEY,
                name varchar(100) NOT NULL,
                long varchar(20) NOT NULL,
                lat varchar(20) NOT NULL 
            );
        """)

    def add(self, sno, sid, name, long, lat):
            # (name,long,lat) 
        self.curr.execute(
        f"""
            INSERT INTO {self.table} 
            (sno,sid,name,long,lat)
            VALUES ( {sno},"{sid}","{name}", "{long}", "{lat}");
        """)
        self.conn.commit();
        Inventory(sid);


    def rm(self, sid):
        self.curr.execute(
        f"""
            DELETE FROM {self.table} 
                where sid = "{sid}";
        """)
        self.conn.commit()


if __name__ == '__main__':
    a = Shops()
    a.add(1, 'SH123', 'Shop ABC', '74', '120');

    inv = Inventory("SH123")
    inv.add_items("ToothBrush", 10, 112.50);
    inv.add_items("ToothPaste", 10, 100);
    # a.rm('SH123')
