from flask import Flask, jsonify
import cx_Oracle
import json
from pymemcache.client import base

app = Flask(__name__)

# Memcached connection
memcache_client = base.Client(('127.0.0.1', 11211))

# Oracle DB connection details
ORACLE_USERNAME = "HR"
ORACLE_PASSWORD = "your_password"
ORACLE_DSN = "your_oracle_host:1521/your_service_name"

def get_db_connection():
    """Establish a connection to Oracle DB."""
    try:
        connection = cx_Oracle.connect(ORACLE_USERNAME, ORACLE_PASSWORD, ORACLE_DSN)
        return connection
    except cx_Oracle.DatabaseError as e:
        print(f"Error connecting to Oracle DB: {e}")
        return None

def fetch_employee(employee_id):
    """Fetch employee details from Oracle DB with Memcached caching."""
    cache_key = f"employee:{employee_id}"

    # Check if data is cached
    cached_data = memcache_client.get(cache_key)
    if cached_data:
        print("Cache HIT! Returning cached result.")
        return json.loads(cached_data)

    # Cache MISS: Query Oracle DB
    print("Cache MISS! Fetching from Oracle DB...")
    conn = get_db_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT employee_id, first_name, last_name, email, job_id, salary FROM HR.EMPLOYEES WHERE employee_id = :id", {"id": employee_id})
        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if row:
            result = {
                "employee_id": row[0],
                "first_name": row[1],
                "last_name": row[2],
                "email": row[3],
                "job_id": row[4],
                "salary": row[5]
            }

            # Store in Memcached for 5 minutes
            memcache_client.set(cache_key, json.dumps(result), expire=300)
            return result
        else:
            return {"error": "Employee not found"}

    except cx_Oracle.DatabaseError as e:
        print(f"Error executing query: {e}")
        return None

@app.route('/employee/<int:employee_id>', methods=['GET'])
def get_employee(employee_id):
    """API endpoint to get employee details"""
    result = fetch_employee(employee_id)
    if result:
        return jsonify(result)
    else:
        return jsonify({"error": "Unable to retrieve data"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
