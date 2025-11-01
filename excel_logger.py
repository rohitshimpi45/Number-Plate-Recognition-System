import pandas as pd
import os

csv_file = "detected_plates.csv"

# Create file if missing
def setup_csv():
    if not os.path.exists(csv_file):
        df = pd.DataFrame(columns=["Plate_Number", "Timestamp"])
        df.to_csv(csv_file, index=False)

def save_plate_to_csv(plate, timestamp):
    df = pd.DataFrame([[plate, timestamp]], columns=["Plate_Number", "Timestamp"])
    df.to_csv(csv_file, mode='a', header=False, index=False)
