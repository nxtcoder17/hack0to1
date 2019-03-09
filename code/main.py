from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

import json

# Classes {{{

# Class: UsersList {{{

import pymysql
from math import radians, sin, cos, asin, acos, sqrt

class UsersList:
    def __init__(self):
        self.conn = pymysql.connect("localhost", "root", "", "hackathon")
        self.curr = self.conn.cursor()
        self.table = "users"

        self.curr.execute(
        f""" 
            CREATE TABLE IF NOT EXISTS {self.table}
            (
                item_name VARCHAR(100) PRIMARY KEY,
                quantity INT
            );
        """)

    def add(self, item, quantity):
        self.curr.execute(
        f"""
            INSERT INTO {self.table} 
            (item_name, quantity)
            VALUES (
                "{item}",
                {quantity}
            );
        """)
        self.conn.commit();

    def ls(self):
        self.curr.execute(
        f"""
            SELECT * from {self.table};
        """)
        return self.curr.fetchall()

# Class: UsersList }}}

def distance_between(lon1, lat1, lon2, lat2):
    lon1 = radians(lon1)
    lat1 = radians(lat1)
    lon2 = radians(lon2)
    lat2 = radians(lat2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1
    temp = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    temp = 2 * asin(sqrt(temp))

    r = 6371

    return (temp * r * 1000)

# class ExtractCloserShops {{{
class ExtractCloserShops:
    def __init__(self):
        self.conn = pymysql.connect("localhost", "root", "", "hackathon")
        self.curr = self.conn.cursor()
        self.table = "shop"

    def extract(self):
        self.curr.execute(f"""
            select * from {self.table};
        """)
        shops = [(x[3], x[4], x[1], x[2]) for x in self.curr.fetchall()]
        long, lat = map(float, open('coords.txt', 'rt').read().split())

        observed = []
        for coords in shops:
            if (distance_between(long, lat, float(coords[0]), float(coords[1])) < 100):
                observed.append(coords)

        # Observed are the A-listed shops,
        items = []
        self.curr.execute(f"""
            SELECT * from users;
        """)
        items = self.curr.fetchall()

        selected = []
        for ids in observed:
            for item in items:
                self.curr.execute(
                f"""
                    SELECT * from {ids[2]} where item = {item[1]};
                """)
                if (self.curr.rowcount  != 0):
                    selected.extend(self.curr.fetchall())

            
        # Notify the user about  selected contents
        f = open('logs.txt', 'wt')
        f.write(str(selected))
        f.close()
        return selected;

# class ExtractCloserShops }}}

# class Inventory {{{
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
                quantity INT
            );
        """)

        print(f'Table ({self.sid}) successfully created.')

    def add_item(self, item, quantity):
        self.curr.execute(
                f"""
                    SELECT * from {self.sid};
                """)
        sno = int(self.curr.rowcount) + 1;
        self.curr.execute(
        f"""
            INSERT INTO {self.sid}
            (sno,item,quantity)
            VALUES (
                {sno},
                "{item}",
                {quantity}
            );
        """)
        self.conn.commit()
        print('Items successfully added to {self.sid} table')

# class Inventory }}}

# class Shops {{{
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

# class Shops }}}


# Classes }}}


@app.route('/')
def default():
    return render_template('index.html');

@app.route('/coords_receiver', methods=['POST'])
def worker():
    json = request.get_json()
    d = dict(request.get_json())

    # console.log(str(json))

    f = open('coords.txt', 'wt')
    # f.write(str(json))
    f.write(str(d['long']) + " " + str(d['lat']))
    f.close()

    return str(json);

@app.route('/add_items.html', methods=['GET'])
def add_items():
    return render_template('add_items.html')

@app.route('/add_items_return', methods=['POST'])
def add_items_return():
    data = dict(request.get_json());
    UsersList().add(
            data['item_name'], data['brand_name'],
            int(data['quantity']))
    return jsonify(request.get_json());


@app.route('/view_item.html')
def view_list():
    return render_template('view_item.html', item_list = UsersList().ls())

@app.route('/result.html')
def find_results():
    return render_template('result.html', choices = ExtractCloserShops().extract());

@app.route('/add_shops.html')
def add_shops():
    return render_template('add_shops.html');

@app.route('/add_shops', methods=['POST'])
def add_shops_post():
    data = dict(request.get_json());
    Shops().add(data['sid'], data['name'], 
            data['long'], data['lat']);
    return jsonify(data)


@app.route('/add_items_in_shop.html')
def add_items_in_the_shop():
    return render_template('add_items_in_shop.html');


@app.route('/add_items_in_shop', methods=['POST'])
def add_items_in_the_shop_json():
    data = dict(request.get_json());
    Inventory(data['sid']).add_item(data['item'], int(data['quantity']));
    return jsonify(data);

if __name__ == '__main__':
    app.run(debug = True)
