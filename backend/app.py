from flask import Flask, request, jsonify

app = Flask(__name__)

# Dummy room data
available_rooms = {
    "101": {"status": "available"},
    "102": {"status": "booked"},
    "103": {"status": "available"}
}

# Health check route
@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok", "message": "AutoNova backend is running"}), 200

# View available rooms
@app.route('/rooms', methods=['GET'])
def get_rooms():
    return jsonify(available_rooms)

# Book a room
@app.route('/book', methods=['POST'])
def book_room():
    data = request.get_json()
    room_id = data.get("room_id")
    guests = data.get("guests")
    if available_rooms.get(room_id) and available_rooms[room_id]['status'] == 'available':
        available_rooms[room_id]['status'] = 'booked'
        return jsonify({"message": "Room booked!", "pin": "1234", "guests": guests})
    return jsonify({"error": "Room unavailable"}), 400

# Upload ID verification
@app.route('/upload-id', methods=['POST'])
def upload_id():
    return jsonify({"message": "ID verified successfully"})

# Payment simulation
@app.route('/pay', methods=['POST'])
def payment():
    return jsonify({"message": "Payment successful (via UPI)", "upi_id": "upi@autonova"})

if __name__ == '__main__':
    app.run(debug=True)
