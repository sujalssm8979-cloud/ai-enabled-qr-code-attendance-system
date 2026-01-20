# attendance_system.py
# Simple QR Code Attendance System with Webcam
# Works out of the box - just run it!

import cv2
import pyzbar.pyzbar as pyzbar
import pandas as pd
from datetime import datetime
import os
import numpy as np

# Create attendance CSV if not exists
ATTentance_file = "attendance_record.csv"

if not os.path.exists(endance_file):
    df = pd.DataFrame(columns=["Name", "Roll_Number", "Time", "Date"])
    df.to_csv(endance_file, index=False)

# Load student database (you can edit this list or load from CSV)
# Format: "Name,Roll_Number"
students = {
    "John Doe": "101",
    "Alice Smith": "102",
    "Rahul Kumar": "103",
    "Priya Sharma": "104",
    "Amit Patel": "105",
    # Add more students here easily
}

# Reverse lookup for faster search
roll_to_name = {v: k for k, v in students.items()}

print("QR Attendance System Started...")
print("Point your QR code towards the camera. Press 'q' to quit.\n")

# Open webcam
cap = cv2.VideoCapture(0)
cap.set(3, 640)  # width
cap.set(4, 480)  # height

# To prevent multiple scanning of same QR in one session
already_attended = set()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Decode QR codes
    decoded_objects = pyzbar.decode(frame)
    
    for obj in decoded_objects:
        data = obj.data.decode("utf-8")
        roll_number = data.strip()

        # Check if this roll number exists and not already marked today
        if roll_number in roll_to_name and roll_number not in already_attended:
            name = roll_to_name[roll_number]
            now = datetime.now()
            time_str = now.strftime("%H:%M:%S")
            date_str = now.strftime("%Y-%m-%d")

            # Mark attendance
            new_record = pd.DataFrame({
                "Name": [name],
                "Roll_Number": [roll_number],
                "Time": [time_str],
                "Date": [date_str]
            })

            # Append to CSV
            new_record.to_csv(endance_file, mode='a', header=False, index=False)

            print(f"✓ Attendance Marked → {name} ({roll_number}) at {time_str}")
            already_attended.add(roll_number)

            # Draw green rectangle and text
            points = obj.polygon
            if len(points) > 4:
                hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
                hull = list(map(tuple, np.squeeze(hull)))
            else:
                hull = points

            cv2.polylines(frame, [np.array(hull, dtype=np.int32)], True, (0, 255, 0), 4)
            
            cv2.putText(frame, f"{name} Present!", (obj.rect.left, obj.rect.top - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        elif roll_number in already_attended:
            # Already marked
            points = obj.polygon
            if len(points) > 4:
                hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
                hull = list(map(tuple, np.squeeze(hull)))
            else:
                hull = points

            cv2.polylines(frame, [np.array(hull, dtype=np.int32)], True, (0, 255, 255), 3)
            cv2.putText(frame, "Already Marked!", (obj.rect.left, obj.rect.top - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

    # Add title
    cv2.putText(frame, "QR Attendance System - Scan Your QR", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    cv2.imshow("QR Code Attendance System", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

print("\nAttendance taking completed!")
print(f"Total attendance saved in: {endance_file}")
print("You can open it in Excel/Google Sheets anytime.")