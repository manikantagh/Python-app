from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("app.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/messages", methods=["GET"])
def get_messages():
    conn = get_db()
    messages = conn.execute(
        "SELECT * FROM messages ORDER BY id DESC"
    ).fetchall()
    conn.close()

    return jsonify([dict(message) for message in messages])

@app.route("/api/messages", methods=["POST"])
def add_message():
    data = request.get_json()
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"error": "Message is required"}), 400

    conn = get_db()
    conn.execute(
        "INSERT INTO messages (message) VALUES (?)",
        (message,)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": message}), 201

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
