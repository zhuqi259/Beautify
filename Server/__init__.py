# -*- coding: utf-8 -*-
__author__ = 'zhuqi259'

from flask import Flask, jsonify, make_response

__storage_file__ = "E:/DATA/INPUT/jlu_student.csv"


def read_data(filename):
    with open(filename, 'rb') as f:
        return f.read()


app = Flask(__name__)

data = read_data(__storage_file__).decode('utf-8')

users = data.splitlines()

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})


@app.route('/api/v1.0/users', methods=['GET'])
def get_users():
    return jsonify({'users': users})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(debug=True)
