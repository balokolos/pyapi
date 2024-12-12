from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Configure MySQL connection
MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_DATABASE = 'world'
MYSQL_USER = '<wuhoo>'
MYSQL_PASSWORD = '<wuhoo>'

# Create a connection function
def get_db_connection():
    connection = mysql.connector.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        database=MYSQL_DATABASE,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD
    )
    return connection

# Define a route to query the database
@app.route('/api/country', methods=['GET'])
def get_employees():
    country_id = request.args.get('country_id')  # Get query parameter
    if not country_id:
        return jsonify({"error": "country_id is required"}), 400
    
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = "SELECT Name, CountryCode, District, Population FROM city WHERE CountryCode = %s"
        cursor.execute(query, (country_id,))
        rows = cursor.fetchall()
        
        # Convert query results to a list of dictionaries
        results = [
            {"Name": row[0], "CountryCode": row[1], "District": row[2], "Population": row[3]}
            for row in rows
        ]
        
        return jsonify(results)
    
    except mysql.connector.Error as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
