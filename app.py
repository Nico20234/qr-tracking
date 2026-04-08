from flask import Flask, request, jsonify, redirect
import psycopg2
import os
import datetime

app = Flask(__name__)

# =========================
# Config DB
# =========================
database_url = os.environ.get("DATABASE_URL")

if not database_url:
    raise ValueError("No se encontró DATABASE_URL en las variables de entorno")

if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)


def get_connection():
    return psycopg2.connect(database_url)


# =========================
# Endpoint principal para tracking
# =========================
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

    # Si el worker no manda fecha, usamos la del servidor
    fecha = data.get("fecha")
    if not fecha:
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

        return jsonify({
            "status": "ok",
            "guardado": {
                "ip": ip,
                "user_agent": user_agent,
                "city": city,
                "region": region,
                "country": country,
                "lat": lat,
                "lon": lon
            }
        }), 200

    except Exception as e:
        if conn:
            conn.rollback()
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# =========================
# Endpoint opcional de prueba
# =========================
@app.route('/qr')
def qr():
    return redirect("https://instagram.com/mediodiaresuelto", code=302)


# =========================
# Health check
# =========================
@app.route('/')
def home():
    return jsonify({
        "status": "running",
        "message": "Backend de tracking activo"
    })


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)