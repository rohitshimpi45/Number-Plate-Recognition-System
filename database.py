import mysql.connector

def connect_db():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Hit@man45",
        database="number_plate_system_indian"
    )
    cursor = db.cursor()

    # Table create if not exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS plates (
            id INT AUTO_INCREMENT PRIMARY KEY,
            plate_number VARCHAR(50),
            timestamp VARCHAR(50)
        )
    """)
    db.commit()
    return db, cursor


def save_plate_to_db(cursor, db, plate, timestamp):
    query = "INSERT INTO plates (plate_number, timestamp) VALUES (%s, %s)"
    cursor.execute(query, (plate, timestamp))
    db.commit()
