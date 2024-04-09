from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

DATABASE = 'todos.db'

def create_table():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            todo_title TEXT NOT NULL,
            todo_description TEXT NOT NULL
        );
    ''')
    conn.commit()
    conn.close()

create_table()

# Define a common prefix for all routes
common_prefix = '/v1'

@app.route(f'{common_prefix}/addtodo', methods=['POST'])
def add_todo():
    todo_title = request.json.get('todo_title')
    todo_description = request.json.get('todo_description')

    if not todo_title or not todo_description:
        return jsonify({'error': 'Both todo title and description are required'}), 400

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO todos (todo_title, todo_description) VALUES (?, ?)', (todo_title, todo_description))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Todo added successfully'}), 201

@app.route(f'{common_prefix}/todos', methods=['GET'])
def get_todos():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM todos')
    todos = cursor.fetchall()
    conn.close()
    return jsonify(todos)

if __name__ == '__main__':
    app.run(debug=True)
