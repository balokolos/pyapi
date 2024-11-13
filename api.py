from flask import Flask, jsonify, request
from flasgger import Swagger

app = Flask(__name__)
tasks = []
swagger = Swagger(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/time')
def get_current_time():
    from datetime import datetime
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route('/tasks', methods=['POST'])
def add_task():
    task = request.json.get('task', '')
    tasks.append(task)
    return jsonify({'task': task}), 201

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    tasks.pop(task_id)

@app.route('/api/data')
def data_api():
    """
    This is an example API endpoint.
    ---
    responses:
      200:
        description: A list of data items.
    """
    return "Data list"


if __name__ == '__main__':
    app.run(debug=True)