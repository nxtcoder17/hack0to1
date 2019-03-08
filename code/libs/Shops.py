import pymysql
import sys
from Inventory import Inventory

class Shops:
    def __init__(self):
        self.conn = pymysql.connect('localhost', 'root', '', 'hackathon');
        self.curr = self.conn.cursor()
        self.table = 'shop'

        self.curr.execute(
                f"""
                    CREATE TABLE IF NOT EXISTS {self.table}
                    (
                        sno INT NOT NULL,
                        sid VARCHAR(20) PRIMARY KEY,
                        name VARCHAR(100),
                        longitude VARCHAR(20),
                        latitude VARCHAR(20)
                    );
                """)

    def add(self, sid, name, long, lat):
        self.curr.execute(
                f"""
                    SELECT * from {self.table};
                """)
        print(f"Row Count: ", self.curr.rowcount)
        sno = int(self.curr.rowcount) + 1;
        print(f"Sno: {sno}")
        try: 
            self.curr.execute(
                    f"""
                        INSERT INTO {self.table}
                        (sno,sid,name,longitude,latitude)
                        VALUES (
                            {sno},
                            "{sid}",
                            "{name}",
                            "{long}",
                            "{lat}"
                        );
                    """)
            self.conn.commit();
            Inventory(sid);
        except Exception as e:
            print('Duplicate Entry begin made')


if __name__ == '__main__':
    a = Shops()
    # a.add('SH123', 'Kirana Dukan', '74', '120');
    a.add(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]);

 
