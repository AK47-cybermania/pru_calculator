import sqlite3
conn = sqlite3.connect("election_results.db")
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS election_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    state TEXT NOT NULL,
    party TEXT NOT NULL,
    votes INTEGER NOT NULL,
    registered_voters INTEGER NOT NULL
)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS parliament_seats (
    state TEXT PRIMARY KEY,
    seats INTEGER NOT NULL
)''')
seats_data = [
    ("PERLIS", 3), ("KEDAH", 15), ("KELANTAN", 14), ("TERENGGANU", 8),
    ("PULAU PINANG", 13), ("PERAK", 24), ("PAHANG", 14), ("SELANGOR", 22),
    ("WILAYAH PERSEKUTUAN KUALA LUMPUR", 11), ("WILAYAH PERSEKUTUAN PUTRAJAYA", 1),
    ("NEGERI SEMBILAN", 8), ("MELAKA", 6), ("JOHOR", 26), ("WILAYAH PERSEKUTUAN LABUAN", 1),
    ("SABAH", 25), ("SARAWAK", 31)
]
cursor.executemany("INSERT OR IGNORE INTO parliament_seats (state, seats) VALUES (?, ?)", seats_data)

conn.commit()
conn.close()
print("Pangkalan data telah disediakan.")