# -*- coding: utf-8 -*-
__author__ = 'zhuqi259'

from flask import Flask, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/hadoop/db/student.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    username = db.Column(db.String(80))
    gender = db.Column(db.Integer)
    department = db.Column(db.String(80))
    major = db.Column(db.String(80))
    teacher = db.Column(db.String(80))
    telephone = db.Column(db.String(80))
    email = db.Column(db.String(80))

    def __init__(self, _id, _username, _gender, _department, _major, _teacher, _telephone, _email):
        self.id = _id
        self.username = _username
        self.gender = _gender
        self.department = _department
        self.major = _major
        self.teacher = _teacher
        self.telephone = _telephone
        self.email = _email

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'gender': self.gender,
            'department': self.department,
            'major': self.major,
            'teacher': self.teacher,
            'telephone': self.telephone,
            'email': self.email
        }


@app.route('/api/v1.0/users', methods=['GET'])
def get_users():
    _users = [u.serialize() for u in User.query.all()]
    return jsonify({'users': _users})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    # 初始化数据库
    db.drop_all()
    db.create_all()

    # 初始化数据
    __storage_file__ = "/home/hadoop/db/jlu_student.csv"


    def read_data(filename):
        with open(filename, 'rb') as f:
            return f.read()


    data = read_data(__storage_file__).decode('utf-8')

    users = data.splitlines()

    # 第一行是表头
    users = users[1:]

    for user in users:
        attrs = user.split(",")
        someone = User(attrs[0], attrs[1], attrs[2], attrs[3], attrs[4], attrs[5], attrs[6], attrs[7])
        db.session.add(someone)

    db.session.commit()
