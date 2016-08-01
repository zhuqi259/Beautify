# -*- coding: utf-8 -*-
__author__ = 'zhuqi259'

from flask import Flask, jsonify, make_response, url_for, request, abort
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///F:/workspace/python/db/student.db'
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


class Beauty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    star = db.Column(db.Integer)

    user_id = db.Column(db.String(20), db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('users', lazy='dynamic'))

    def __init__(self, _user, _star=1):
        self.user = _user
        self.star = _star

    def __repr__(self):
        return '<Beauty %r>' % self.user.id


__page_number__ = 1
__page_size__ = 10


def make_public_user(_user):
    new_user = {}
    for field in _user:
        if field == 'id':
            new_user['id'] = _user['id']
            new_user['uri'] = url_for('get_user', user_id=_user['id'], _external=True)
            new_user['photo'] = url_for('static', filename='img/' + _user['id'] + '.jpg', _external=True)
        else:
            new_user[field] = _user[field]
    return new_user


@app.route('/api/v1.0/users', methods=['GET'])
def get_users():
    _users = [u.serialize() for u in User.query.all()]
    return jsonify({'users': map(make_public_user, _users)})


@app.route('/api/v1.0/users/<user_id>', methods=['GET'])
def get_user(user_id):
    _user = User.query.get_or_404(user_id)
    return jsonify({'user': make_public_user(_user.serialize())})


@app.route('/api/v1.0/users/random', methods=['GET'])
def get_user_random():
    count = User.query.count()
    random_choice = random.randint(1, count)
    users_one = User.query.paginate(random_choice, 1).items
    _user = users_one[0]
    return jsonify({'user': make_public_user(_user.serialize())})


@app.route('/api/v1.0/users/pages', methods=['GET'])
def get_users_pages():
    page_number = int(request.args.get('page_number', __page_number__))
    page_size = int(request.args.get('page_size', __page_size__))
    _users = [u.serialize() for u in User.query.paginate(page_number, page_size).items]
    return jsonify({'users': map(make_public_user, _users)})


@app.route('/api/v1.0/beauties', methods=['GET'])
def get_beauties():
    _users = [b.user.serialize() for b in Beauty.query.order_by(Beauty.star.desc()).all()]
    return jsonify({'users': map(make_public_user, _users)})


@app.route('/api/v1.0/beauties/pages', methods=['GET'])
def get_beauties_pages():
    page_number = int(request.args.get('page_number', __page_number__))
    page_size = int(request.args.get('page_size', __page_size__))
    _users = [b.user.serialize() for b in
              Beauty.query.order_by(Beauty.star.desc()).paginate(page_number, page_size).items]
    return jsonify({'users': map(make_public_user, _users)})


@app.route('/api/v1.0/beauties', methods=['POST'])
def create_beauty():
    if not request.json or not 'user_id' in request.json:
        abort(400)
    user_id = request.json['user_id']
    _user = User.query.get_or_404(user_id)
    b = Beauty.query.filter_by(user_id=user_id).first()
    if b is None:
        b = Beauty(_user)
        db.session.add(b)
    else:
        b.star += 1
    db.session.commit()
    return jsonify({'status': '200'})


@app.errorhandler(400)
def param_error(error):
    return make_response(jsonify({'error': 'Param Error'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    # 初始化数据库
    db.drop_all()
    db.create_all()

    # 初始化数据
    __storage_file__ = "F:/workspace/python/db/jlu_student.csv"


    def read_data(filename):
        with open(filename, 'rb') as f:
            return f.read()


    data = read_data(__storage_file__).decode('utf-8')

    users = data.splitlines()

    # 第一行是表头
    users = users[1:]

    for user in users:
        attrs = user.split(",")
        if attrs[2] == '1':
            someone = User(attrs[0], attrs[1], attrs[2], attrs[3], attrs[4], attrs[5], attrs[6], attrs[7])
            db.session.add(someone)

    db.session.commit()
