import os
import psycopg2
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

def get_db_connection():
    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    return conn

@app.route('/api/hello')
def hello():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Create table if it doesn't exist
        cur.execute('CREATE TABLE IF NOT EXISTS timestamps (ts TIMESTAMP);')
        
        # Insert current timestamp
        cur.execute('INSERT INTO timestamps (ts) VALUES (NOW());')
        
        # Retrieve all timestamps
        cur.execute('SELECT ts FROM timestamps;')
        timestamps = cur.fetchall()
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify([ts[0] for ts in timestamps])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Get port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    # Run the app, listening on all interfaces
    app.run(host='0.0.0.0', port=port, debug=True)
