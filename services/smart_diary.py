import mysql.connector
from datetime import datetime

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="krishisathi"
    )
def save_yield_history(data):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO yield_history 
            (date, crop_name, region, year, temperature, rainfall, humidity, soil_nitrogen, soil_ph, predicted_yield)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            data["date"],
            data["crop_name"],
            data.get("region", None),
            data.get("year", None),
            data.get("temperature", None),
            data.get("rainfall", None),
            data.get("humidity", None),
            data.get("soil_nitrogen", None),
            data.get("soil_ph", None),
            data["predicted_yield"]
        ))

        conn.commit()
        conn.close()
        print("✅ Yield forecast saved successfully!")

    except Exception as e:
        print(f"❌ Error saving yield forecast: {e}")

# SAVE CROP HISTORY
def save_crop_history(data):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        INSERT INTO crop_history 
        (date, nitrogen, phosphorus, potassium, pH, rainfall, temperature, humidity, prediction)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    values = (
        data["date"],
        data["nitrogen"],
        data["phosphorus"],
        data["potassium"],
        data["pH"],
        data["rainfall"],
        data["temperature"],
        data["humidity"],
        data["prediction"]
    )

    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()


# SAVE FERTILIZER HISTORY
def save_fertilizer_history(data):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        INSERT INTO fertilizer_history
        (date, crop_name, soil_type, nitrogen, phosphorus, potassium, recommendation)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """

    values = (
        data["date"],
        data["crop_name"],
        data["soil_type"],
        data["nitrogen"],
        data["phosphorus"],
        data["potassium"],
        data["recommendation"]
    )

    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()


# GET ALL HISTORY
def get_diary_history():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Crop & Fertilizer
    cursor.execute("SELECT * FROM crop_history ORDER BY date DESC")
    crop = cursor.fetchall()

    cursor.execute("SELECT * FROM fertilizer_history ORDER BY date DESC")
    fertilizer = cursor.fetchall()

    # Disease & Yiel

    cursor.execute("SELECT * FROM yield_history ORDER BY date DESC")
    yield_data = cursor.fetchall()

    cursor.close()
    conn.close()

    return {
        "crop": crop,
        "fertilizer": fertilizer,
        "yield": yield_data
    }
