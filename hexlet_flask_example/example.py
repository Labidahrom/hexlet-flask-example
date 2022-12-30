from flask import Flask
from flask import render_template, request, redirect, url_for, flash, get_flashed_messages
import json
import random
users = ['mike', 'mishel', 'adel', 'keks', 'kamila']


# Это уже нам знакомое callable WSGI-приложение
app = Flask(__name__)
app.secret_key = "secret_key"

def read_json_file():
    with open('repo.json', 'r') as json_file:
        data = json_file.read()
        if not data:
            return []
        return json.loads(data)

def write_json_file(data, data_to_add):
    if not data:
        data = []
    data.extend(data_to_add)
    with open('repo.json', 'w') as json_file:
        json.dump(data, json_file)


def change_json_file(id, user_data):
    data = read_json_file()
    for i in data:
        if i['id'] == id:
            user_data['id'] = id
            data[data.index(i)] = user_data
    with open('repo.json', 'w') as json_file:
        json.dump(data, json_file)


def find_user(id):
    with open('repo.json', 'r') as json_file:
        data = json_file.read()
        data = json.loads(data)
        print(type(data))
        for i in data:
            if i['id'] == str(id):
                return i


def delete_user(id):
    data = read_json_file()
    for i in data:
        if i['id'] == id:
            data.remove(i)
    with open('repo.json', 'w') as json_file:
        json.dump(data, json_file)


def generate_id():
    return str(random.randint(10, 99)) + str(random.randint(10, 99)) + str(random.randint(10, 99))


def filter_users(user_list, term):
    output = []
    term = str(term)
    for i in user_list:
        if term in i:
            output.append(i)
    return output


# @app.route('/')
# def hello_world():
#     return [233, 322, 55]


def validate(user):
    errors = {}
    if not user['name'].isalpha():
        errors['name'] = "only letters allowed"
    if 'gmail.com' not in user['email'] and 'yandex.ru' not in user['email']:
        errors['email'] = "wrong email"
    return errors

#
# @app.route('/users')
# def users_list():
#
#     return render_template(
#         '/users/index.html',
#         users=users,
#     )

# @app.route('/users')
# def filter_users_list():
#     term = request.args.get('term')
#     filtered_users = filter_users(users, term)
#
#     return render_template(
#         '/users/index.html',
#         search=term,
#         users=filtered_users,
#     )


# @app.post('/users')
# def users_post():
#     return 'Users', 302
    

@app.route('/users/<id>')
def users1(id):
    user = find_user(id)
    if not user:
        return 'page not found', 404

    return render_template(
        '/users/show.html',
        user=user
    )

@app.route('/')
def index():

    return render_template(
        'index.html'
    )

#
#
# @app.route('/users/<id>')
# def users1(id):
#
#     return render_template(
#         '/users/show.html',
#         id=id,
#     )


@app.post('/users/user_list')
def users_post():
    user = request.form.to_dict()
    errors = validate(user)
    if errors:
        return render_template(
          'users/new.html',
          user=user,
          errors=errors,
        )
    initial_data = read_json_file()
    user['id'] = generate_id()
    user = [user]
    write_json_file(initial_data, user)
    flash('Спасибки за регистрацию!', 'success')
    return redirect(url_for('users_post'), code=302)


@app.route('/users/user_list')
def ut():
    user_data = read_json_file()
    messages = get_flashed_messages(with_categories=True)
    return render_template(
            '/users/user_list.html',
            users=user_data,
            messages=messages
        )


@app.route('/users/new')
def users_new():
    user = {}
    errors = {}

    return render_template(
        'users/new.html',
        user=user,
        errors=errors
        )


@app.route('/users/<id>/edit')
def users11(id):
    user = find_user(id)
    errors = {}

    return render_template(
        'users/edit.html',
        user=user,
        errors=errors
        )


@app.route('/users/<id>/patch', methods=['POST'])
def patch_school(id):
    user = request.form.to_dict()

    errors = validate(user)
    if errors:
        return render_template(
            'user/edit.html',
            user=user,
            errors=errors,
        ), 422

    change_json_file(id, user)
    flash('User had been changed', 'success')
    return redirect(url_for('users_post'), code=302)


@app.route('/users/<id>/delete', methods=['GET'])
def ask_delete(id):
    user = find_user(id)
    return render_template(
        'users/delete.html',
        user=user)


@app.route('/users/<id>/delete', methods=['POST'])
def delete_user1(id):
    delete_user(id)
    flash('User had been deleted', 'success')
    return redirect(url_for('users_post'), code=302)
