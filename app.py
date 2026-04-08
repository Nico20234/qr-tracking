from flask import Flask, request, jsonify, redirect
import psycopg2
import os
import datetime

app = Flask(__name__)

database_url = os.environ.get("DATABASE_URL")

if not database_url:
    raise ValueError("No se encontró DATABASE_URL")

if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

def get_connection():
    return psycopg2.connect(database_url)

@app.route('/track', methods=['POST'])
def track():
    data = request.get_json(silent=True) or {}

    ip = data.get("ip")
    user_agent = data.get("user_agent")
    city = data.get("city")
    region = data.get("region")
    country = data.get("country")
    lat = data.get("lat")
    lon = data.get("lon")

    fecha_str = data.get("fecha")
    if fecha_str:
        try:
            fecha = datetime.datetime.fromisoformat(fecha_str.replace("Z", "+00:00"))
        except Exception:
            fecha = datetime.datetime.utcnow()
    else:
        fecha = datetime.datetime.utcnow()

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO scans (ip, user_agent, fecha, ciudad, region, pais, lat, lon)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            ip,
            user_agent,
            fecha,
            city,
            region,
            country,
            lat,
            lon
        ))

        conn.commit()

        return jsonify({"status": "ok"}), 200

    except Exception as e:
        if conn:
            conn.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/')
def home():
    return jsonify({"status": "running"}), 200

@app.route('/qr')
def qr():
    return redirect("https://instagram.com/mediodiaresuelto", code=302)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)