# QR Tracking – Redirección y análisis de escaneos

Este proyecto permite generar códigos QR que redirigen a una URL (por ejemplo, Instagram) y al mismo tiempo registran información del escaneo para su posterior análisis.

## 🚀 Funcionalidad

- Generación de códigos QR personalizados
- Redirección automática del usuario al escanear (ej: Instagram)
- Registro de datos del escaneo:
  - IP del usuario
  - Ubicación aproximada (ciudad, país)
  - Fecha y hora
  - User Agent (dispositivo/navegador)
- Posibilidad de analizar métricas de uso y comportamiento

## 🧠 Objetivo del proyecto

Este proyecto fue desarrollado como una solución para medir la efectividad de campañas físicas (por ejemplo, flyers o packaging) mediante códigos QR, permitiendo obtener datos reales de interacción de usuarios.

## 🛠️ Tecnologías utilizadas

- Python
- Flask (backend)
- APIs externas para geolocalización
- Generación de códigos QR
- JSON / REST

## 📊 Aplicación práctica

Permite responder preguntas como:
- ¿Cuántas personas escanean el QR?
- ¿Desde qué ciudades?
- ¿En qué horarios hay más actividad?
- ¿Qué dispositivos utilizan?

## ▶️ Ejecución

1. Clonar el repositorio:
```bash
git clone https://github.com/tu-usuario/qr-tracking.git
