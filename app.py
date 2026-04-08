from flask import Flask, request, redirect, render_template
import psycopg2
import datetime
import requests
import os
from flask import jsonify

app = Flask(__name__)

@app.route('/track', methods=['POST'])
def track():
    data = request.get_json()

    ip = data.get("ip")
    country = data.get("country")
    city = data.get("city")

    fecha = datetime.datetime.now()

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO scans (ip, user_agent, fecha, ciudad, region, pais, lat, lon)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        ip,
        "worker",
        fecha,
        city,
        None,
        country,
        None,
        None
    ))

    conn.commit()

    return jsonify({"status": "ok"})

app = Flask(__name__)

# 🔌 Conexión a PostgreSQL (Render)
database_url = os.environ.get("DATABASE_URL")

if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

conn = psycopg2.connect(database_url)

def obtener_ubicacion(ip):
    try:
        url = f"http://ip-api.com/json/{ip}"
        data = requests.get(url).json()

        return {
            "ciudad": data.get("city"),
            "region": data.get("regionName"),
            "pais": data.get("country"),
            "lat": data.get("lat"),
            "lon": data.get("lon")
        }
    except:
        return None

@app.route('/qr')
def qr():
    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    fecha = datetime.datetime.now()

    ubicacion = obtener_ubicacion(ip)

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO scans (ip, user_agent, fecha, ciudad, region, pais, lat, lon)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        ip,
        user_agent,
        fecha,
        ubicacion["ciudad"] if ubicacion else None,
        ubicacion["region"] if ubicacion else None,
        ubicacion["pais"] if ubicacion else None,
        ubicacion["lat"] if ubicacion else None,
        ubicacion["lon"] if ubicacion else None
    ))

    conn.commit()

    return redirect("https://instagram.com/mediodiaresuelto")

@app.route('/')
def home():
    return redirect('/qr')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)