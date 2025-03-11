from flask import Flask, request, jsonify, render_template, send_file
import sqlite3
import pandas as pd

app = Flask(__name__)
def get_db_connection():
    return sqlite3.connect("keputusan_pru.db")
    conn.row_factory = sqlite3.Row
    return conn
    def sainte_lague(state):    
     conn = get_db_connection(keputusan_pru)

    df = pd.read_sql_query("SELECT party, votes FROM election_results WHERE state=?", conn, params=(state,))
    

    row = conn.execute("SELECT seats FROM parliament_seats WHERE state=?", (state,)).fetchone()
    seats = row[0] if row else 0
    

    return df, seats

    total_seats = seats[0]
    total_votes = df['votes'].sum()
    threshold = total_votes * 0.03
    df = df[df['votes'] >= threshold]  # Tapis parti yang tidak capai ambang

    df['allocated_seats'] = 0
    divisor = {party: 1 for party in df['party'].tolist()}

    for _ in range(total_seats):
        df['quotient'] = df.apply(lambda row: row['votes'] / divisor[row['party']], axis=1)
        max_index = df['quotient'].idxmax()
        df.loc[max_index, 'allocated_seats'] += 1
        divisor[df.loc[max_index, 'party']] += 2

    return df[['party', 'allocated_seats']].to_dict(orient='records')
@app.route("/results/<state>", methods=["GET"])
def get_results(state):
    results = sainte_lague(state)
    return jsonify(results)
@app.route("/add", methods=["POST"])
def add_data():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO election_results (state, party, votes, registered_voters) VALUES (?, ?, ?, ?)",
                   (data["state"], data["party"], data["votes"], data["registered_voters"]))
    conn.commit()
    conn.close()
    return jsonify({"message": "Data successfully added!"})
    @app.route("/export", methods=["GET"])
    def export_excel():
     conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM election_results", conn)
    conn.close()
    
    file_path = "election_results.xlsx"
    df.to_excel(file_path, index=False)
    return send_file(file_path, as_attachment=True)
  
@app.route("/")  
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
    
    