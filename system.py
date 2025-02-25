import sqlite3
from datetime import datetime
from datetime import time
from box import detect_number_plate 
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
    if choice == 1:
        image_path = input("Enter the path of the vehicle image: ")
        vehicle_number = detect_number_plate(image_path)

        if vehicle_number:
            now = datetime.now().strftime("%H:%M:%S")
            c.execute("INSERT INTO ParkingSystem (Vehicle_number, Entry_Time) VALUES (?, ?)", (vehicle_number, now))
            conn.commit()
            print(f"✅ Vehicle {vehicle_number} entered at {now}")
        else:
            print("❌ Number plate could not be detected.")

    if choice == 2:
        image_path = input("Enter the path of the vehicle image: ")
        vehicle_number = detect_number_plate(image_path)

        if vehicle_number:
            now = datetime.now().strftime("%H:%M:%S")
            c.execute("SELECT Entry_Time FROM ParkingSystem WHERE Vehicle_number=?", (vehicle_number,))
            row = c.fetchone()

            if row:
                entry_time = row[0]
                format = "%H:%M:%S"
                duration = (datetime.strptime(now, format) - datetime.strptime(entry_time, format)).seconds
                amount = duration * 10  # Adjust pricing logic if needed

                c.execute("UPDATE ParkingSystem SET Exit_Time=?, Duration=?, Amount=? WHERE Vehicle_number=?", 
                          (now, duration, amount, vehicle_number))
                conn.commit()

                print(f"✅ Vehicle {vehicle_number} exited.")
                print(f"⏳ Duration: {duration} seconds")
                print(f"💰 Amount: Rs. {amount}/-")
            else:
                print("❌ Vehicle not found.")
        else:
            print("❌ Number plate could not be detected.")

    if choice == 3:
        c.execute("SELECT * FROM ParkingSystem")
        print(c.fetchall())

    if choice == 4:
        break

conn.commit()
conn.close()
