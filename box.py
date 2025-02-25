import cv2
import os
import pandas as pd
from pytesseract import pytesseract 
path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
pytesseract.tesseract_cmd = path_to_tesseract 
def extract_number(image):
   img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
   text = pytesseract.image_to_string(img_gray, lang='eng')
   return text

# Create a directory to save images with bounding boxes
if not os.path.exists("annotated_images"):
    os.makedirs("annotated_images")

# Load the Haar Cascade classifier for number plate detection (you can find pre-trained classifiers online)
plate_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_russian_plate_number.xml')

# Function to detect number plate and draw bounding box
def detect_number_plate(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect plates
    plates = plate_cascade.detectMultiScale(gray, 1.1, 10)
    img_new, number = None, None
    # Draw bounding boxes
    for (x, y, w, h) in plates:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Green box
        img_new = image[y:y+h,x:x+w]
        cv2.imwrite(f"annotated_images/{image_path}", img_new)
        number = extract_number(img_new)
        print(number)

    return img_new, number

# Load dataset images
image_folder = r"datatset\images\train"  # Update this path with the directory where your images are stored
images = os.listdir(image_folder)

# Process each image in the dataset
numbers = []
for image_name in images:
    image_path = os.path.join(image_folder, image_name)
    annotated_image, number = detect_number_plate(image_path)
    # Save the annotated image
    # cv2.imwrite(f"annotated_images/{image_name}", annotated_image)
    # Prepare annotations for YOLO format (class_id, x_center, y_center, width, height)
    try:
            for vehicle_number in number:
                numbers.append({
                    'vehicle_number': vehicle_number,
                })
    except:
         numbers.append("plate not detected")

# Save annotations to a CSV file
df = pd.DataFrame(numbers)
df.to_csv("numbers.csv", index=False)

print("Vehicle numbers saved to numbers.csv")
