from flask import Flask, render_template, Response
import sqlite3
from datetime import datetime
from pyzbar.pyzbar import decode
import cv2
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# Initialize SQLite database
def init_db():
    with sqlite3.connect('school.db') as conn:
        c = conn.cursor()
        c.executescript('''
            CREATE TABLE IF NOT EXISTS students (
                usn TEXT PRIMARY KEY,
                name TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usn TEXT NOT NULL,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                status TEXT NOT NULL,
                FOREIGN KEY (usn) REFERENCES students(usn)
            );
        ''')
        conn.commit()

init_db()

# Function to decode barcode
def decode_barcode(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    barcodes = decode(gray)
    for barcode in barcodes:
        barcode_data = barcode.data.decode('utf-8')
        return barcode_data
    return None

# Route to display camera feed
@app.route('/')
def index():
    return render_template('index.html')

# Generator function for video streaming with barcode scanning
def generate_frames():
    camera = cv2.VideoCapture(0)
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            barcode_data = decode_barcode(frame)
            if barcode_data:
                record_attendance(barcode_data)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Function to record attendance in the database
def record_attendance(usn):
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")
    with sqlite3.connect('school.db') as conn:
        c = conn.cursor()
        c.execute("INSERT INTO attendance (usn, date, time, status) VALUES (?, ?, ?, ?)",
                  (usn, date_str, time_str, "Present"))
        conn.commit()

# Route for video feed with barcode scanning
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Route to display attendance records and graph
@app.route('/attendance')
def attendance():
    conn = sqlite3.connect('school.db')
    c = conn.cursor()
    c.execute("SELECT * FROM attendance")
    rows = c.fetchall()
    conn.close()

    # Generate graph
    usns = [row[1] for row in rows]
    dates = [row[2] for row in rows]
    plt.figure(figsize=(10, 6))
    plt.bar(dates, usns, color='blue')
    plt.xlabel('Date')
    plt.ylabel('USN')
    plt.title('Attendance Records')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save graph to a string buffer
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()

    return render_template('attendance.html', rows=rows, graph_url=graph_url)

if __name__ == '__main__':
    app.run(debug=True)
