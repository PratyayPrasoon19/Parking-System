import sqlite3
from datetime import datetime
from datetime import time
conn=sqlite3.connect('Parking.db')
c=conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS ParkingSystem(
Vehicle_number TEXT,
Entry_Time TIME,
Exit_Time TIME,
Duration Integer,
Amount Integer
)""")

choice=0
while(choice<5):
    print("\n\nPlease select your choice:\n1. Vehicle Entry\n2. Vehicle Exit\n3. Show Database\n4. Exit")
    choice=int(input("Enter Value: "))
    if choice==1:
        a=input("Enter Vehicle Number: ")
        now1=datetime.now()
        b=now1.strftime("%H:%M:%S")
        c.execute("INSERT INTO ParkingSystem(Vehicle_number, Entry_Time) VALUES(?,?)",(a,b))
        print("Vehicle entered successfully.")

    if choice==2:
        d=input("Enter Vehicle Number: ")
        now2=datetime.now()
        e=now2.strftime("%H:%M:%S")
        c.execute("SELECT * FROM ParkingSystem where Vehicle_number=?",(d,))
        row=c.fetchone()
        if row:
            entry_time = row[1]
            format="%H:%M:%S"
            f=datetime.strptime(e, format)-datetime.strptime(entry_time, format)
            duration=f.seconds
            amount=duration*10
            c.execute("UPDATE ParkingSystem SET Exit_Time=?, Duration=?, Amount=? WHERE Vehicle_number=?", (e, duration, amount, row[0]))
            print("Vehicle exited successfully.")
            print("Duration:", duration, "seconds")
            print("Amount: Rs.", amount,"/-")
        else:
            print("Vehicle not found.")
      
    if choice==3:
        c.execute("SELECT * FROM ParkingSystem")
        print(c.fetchall())

    if choice==4:
        break
conn.commit()
