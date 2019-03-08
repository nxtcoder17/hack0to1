from Calc_Distance import distance_between
import pymysql

# Assuming we get to read the user's current geo coordinates
# cur_long, cur_lat = map(float, open('geo_coordinates', 'rt').read().split())
cur_long, cur_lat = 0, 0

conn = pymysql.connect('localhost', 'root', '', 'Hackathon')
curr = conn.cursor()
