

from ultralytics import YOLO
import easyocr
import cv2
import time

from database import connect_db, save_plate_to_db
from excel_logger import setup_csv, save_plate_to_csv
from preprocess_black_text import preprocess_black_text



db, cursor = connect_db()
setup_csv()

model = YOLO("D:/number plate/best.pt")
reader = easyocr.Reader(['en'])

detected_plates = {}
DETECTION_INTERVAL = 3
DUPLICATE_THRESHOLD = 10
last_detection = time.time()

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    current = time.time()

    if current - last_detection >= DETECTION_INTERVAL:
        results = model(frame)

        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                crop = frame[y1:y2, x1:x2]

                if crop.size > 0:
                    processed = preprocess_black_text(crop)
                    ocr_results = reader.readtext(processed)

                    for (_, text, prob) in ocr_results:
                        if prob > 0.4:
                            plate = text.strip()
                            last_seen = detected_plates.get(plate, 0)

                            if current - last_seen > DUPLICATE_THRESHOLD:
                                detected_plates[plate] = current
                                timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

                                print(f" Plate detected: {plate}")

                                save_plate_to_csv(plate, timestamp)
                                save_plate_to_db(cursor, db, plate, timestamp)

                            cv2.putText(frame, plate, (x1, y1 - 10),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)

        last_detection = current

    cv2.imshow("Number Plate Detection System", frame)
    print(f"Unique Plates: {len(detected_plates)}", end="\r")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
cursor.close()
db.close()
