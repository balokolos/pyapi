from flask import Flask, request, jsonify
import cx_Oracle

app = Flask(__name__)

# Configure Oracle connection
ORACLE_HOST = 'your_host'
ORACLE_PORT = '1521'
ORACLE_SERVICE_NAME = 'your_service_name'
ORACLE_USER = 'your_username'
ORACLE_PASSWORD = 'your_password'

# Create a connection function
def get_db_connection():
    dsn = cx_Oracle.makedsn(ORACLE_HOST, ORACLE_PORT, service_name=ORACLE_SERVICE_NAME)
    connection = cx_Oracle.connect(user=ORACLE_USER, password=ORACLE_PASSWORD, dsn=dsn)
    return connection

# Define a route to query the database
@app.route('/api/employees', methods=['GET'])
def get_employees():
    department_id = request.args.get('department_id')  # Get query parameter
    if not department_id:
        return jsonify({"error": "department_id is required"}), 400
    
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = "SELECT employee_id, first_name, last_name, department_id FROM employees WHERE department_id = :id"
        cursor.execute(query, id=department_id)
        rows = cursor.fetchall()
        
        # Convert query results to a list of dictionaries
        results = [
            {"employee_id": row[0], "first_name": row[1], "last_name": row[2], "department_id": row[3]}
            for row in rows
        ]
        
        return jsonify(results)
    
    except cx_Oracle.DatabaseError as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
