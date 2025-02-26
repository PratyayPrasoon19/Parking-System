import sqlite3
from datetime import datetime
import cv2
import pytesseract

pytesseract.pytesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

plate_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_russian_plate_number.xml')

def extract_number(image):
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(img_gray, lang='eng')
    return text.strip()

def detect_number_plate_from_video():
    cap = cv2.VideoCapture(0) 

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to capture video frame.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        plates = plate_cascade.detectMultiScale(gray, 1.1, 10)

        for (x, y, w, h) in plates:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Draw bounding box
            plate_img = frame[y:y+h, x:x+w]
            number = extract_number(plate_img)

            if number:
                print(f"✅ Detected Number Plate: {number}")
                cap.release()
                cv2.destroyAllWindows()
                return number

        cv2.imshow("Live Camera - Detecting Number Plate", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return None


conn = sqlite3.connect('Parking.db')
c = conn.cursor()


choice = 0
while choice < 5:
    print("\n\nPlease select your choice:\n1. Vehicle Entry\n2. Vehicle Exit\n3. Show Database\n4. Exit")
    choice = int(input("Enter Value: "))

    if choice == 1:
        print("📷 Capturing vehicle number from live camera...")
        vehicle_number = detect_number_plate_from_video()

        if vehicle_number:
            now = datetime.now().strftime("%H:%M:%S")
            c.execute("INSERT INTO ParkingSystem (Vehicle_number, Entry_Time) VALUES (?, ?)", (vehicle_number, now))
            conn.commit()
            print(f"✅ Vehicle {vehicle_number} entered at {now}")
        else:
            print("❌ Number plate could not be detected.")

    if choice == 2:
        print("📷 Capturing vehicle exit from live camera...")
        vehicle_number = detect_number_plate_from_video()

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

