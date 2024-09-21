CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usn VARCHAR(255),
    date TEXT,
    time TEXT,
    status TEXT
);