from flask import Flask, request, redirect, render_template
import psycopg2
import datetime
import requests

app = Flask(__name__)

# 🔌 Conexión a PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="qr_tracking",
    user="postgres",
    password="nico2023"
)

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

@app.route('/landing')
def landing():
    return render_template("landing.html")

@app.route('/ir-instagram')
def ir_instagram():
    return redirect("https://instagram.com/mediodiaresuelto")

if __name__ == '__main__':
    app.run(debug=True)