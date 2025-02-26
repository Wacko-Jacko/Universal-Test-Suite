from flask import Flask, request, jsonify, send_from_directory
from flask_mysqldb import MySQL
import os
import datetime
import subprocess

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'test_suite'
mysql = MySQL(app)

# Directory for storing screenshots
SCREENSHOT_DIR = "screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

@app.route('/test_cases', methods=['GET', 'POST'])
def test_cases():
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM test_cases")
        test_cases = cur.fetchall()
        cur.close()
        return jsonify([{ "id": row[0], "name": row[1], "description": row[2] } for row in test_cases])
    
    elif request.method == 'POST':
        data = request.json
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO test_cases (name, description) VALUES (%s, %s)", (data['name'], data['description']))
        mysql.connection.commit()
        cur.close()
        return jsonify({"message": "Test case added"}), 201

@app.route('/execute_test/<int:test_id>', methods=['POST'])
def execute_test(test_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT name FROM test_cases WHERE id = %s", (test_id,))
    test = cur.fetchone()
    if not test:
        return jsonify({"error": "Test case not found"}), 404
    
    test_name = test[0]
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = os.path.join(SCREENSHOT_DIR, f"{test_name}_{timestamp}.png")
    
    # Simulating test execution with Selenium
    try:
        subprocess.run(["python", "run_selenium_test.py", test_name, screenshot_path], check=True)
        status = "Passed"
    except subprocess.CalledProcessError:
        status = "Failed"
    
    cur.execute("INSERT INTO test_results (test_name, status, executed_at, screenshot) VALUES (%s, %s, NOW(), %s)",
                (test_name, status, screenshot_path))
    mysql.connection.commit()
    cur.close()
    
    return jsonify({"message": "Test executed", "status": status})

@app.route('/test_results', methods=['GET'])
def test_results():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM test_results")
    results = cur.fetchall()
    cur.close()
    return jsonify([{
        "id": row[0], "test_name": row[1], "status": row[2], "executed_at": row[3].strftime("%Y-%m-%d %H:%M:%S"), "screenshot": row[4]
    } for row in results])

@app.route('/screenshots/<path:filename>')
def get_screenshot(filename):
    return send_from_directory(SCREENSHOT_DIR, filename)

if __name__ == '__main__':
    app.run(debug=True)
