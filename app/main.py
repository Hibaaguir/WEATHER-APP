from flask import Flask, render_template, jsonify
import random
from datetime import datetime

app = Flask(__name__)

# Données météo simulées
cities_weather = {
    "Paris": {"temp": random.randint(15, 25), "condition": "Ensoleillé"},
    "London": {"temp": random.randint(10, 18), "condition": "Nuageux"},
    "New York": {"temp": random.randint(20, 30), "condition": "Pluvieux"},
    "Tokyo": {"temp": random.randint(18, 28), "condition": "Partiellement nuageux"}
}

@app.route('/')
def index():
    return render_template('index.html', cities=cities_weather)

@app.route('/api/weather/<city>')
def get_weather(city):
    weather = cities_weather.get(city)
    if weather:
        return jsonify({
            "city": city,
            "temperature": weather["temp"],
            "condition": weather["condition"],
            "timestamp": datetime.now().isoformat()
        })
    return jsonify({"error": "City not found"}), 404

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)