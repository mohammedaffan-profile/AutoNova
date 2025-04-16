from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Correct: Load from DATABASE_URL and assign to SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default_secret')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize DB
db = SQLAlchemy(app)

# Dummy room data
available_rooms = {
    "101": {"status": "available"},
    "102": {"status": "booked"},
    "103": {"status": "available"}
}

# --- Routes ---
@app.route("/")
def index():
    return jsonify({"message": "Welcome to AutoNova!"})

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok", "message": "AutoNova backend is running"}), 200

@app.route('/rooms', methods=['GET'])
def get_rooms():
    return jsonify(available_rooms)

@app.route('/book', methods=['POST'])
def book_room():
    data = request.get_json()
    room_id = data.get("room_id")
    guests = data.get("guests")
    if available_rooms.get(room_id) and available_rooms[room_id]['status'] == 'available':
        available_rooms[room_id]['status'] = 'booked'
        return jsonify({"message": "Room booked!", "pin": "1234", "guests": guests})
    return jsonify({"error": "Room unavailable"}), 400

@app.route('/upload-id', methods=['POST'])
def upload_id():
    return jsonify({"message": "ID verified successfully"})

@app.route('/pay', methods=['POST'])
def payment():
    return jsonify({"message": "Payment successful (via UPI)", "upi_id": "upi@autonova"})

@app.route('/guests', methods=['GET'])
def show_guests():
    guests = Guest.query.all()
    return jsonify([{"id": g.id, "name": g.name} for g in guests])

# --- Models ---
class Guest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

# --- Entry Point ---
if __name__ == "__main__":
    app.run(debug=True)
