import sqlite3

conn=sqlite3.connect('Parking.db')
c=conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS ParkingSystem(
Vehicle_number TEXT,
Entry_Time TIME,
Exit_Time TIME,
Duration Integer,
Amount Integer
)""")

conn.commit()
