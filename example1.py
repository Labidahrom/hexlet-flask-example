from flask import Flask
from flask import render_template, request, redirect, url_for, flash, get_flashed_messages, session
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


@app.route('/', methods=['GET'])
def index():
    cart = json.loads(request.cookies.get('cart', json.dumps({})))
    if session.get('user'):
        user = True
    else:
        user = False
    return render_template('users/index1.html', cart=cart, user=user)


@app.route('/logout', methods=['POST'])
def logout():
    session['user'] = 0
    return redirect('/')


@app.route('/login', methods=['POST'])
def login():
    session['user'] = 1
    return redirect('/')


@app.post('/cart-items')
def add_item():
    cart = json.loads(request.cookies.get('cart', json.dumps({})))

    item = request.form.to_dict()
    if cart.get(item['item_id']):
        count = cart.get(item['item_id']).get('count') + 1
    else:
        count = 1
    item_in_cart_id = item['item_id']
    item_in_cart_name = item['item_name']
    cart[item_in_cart_id] = {
        "name": item_in_cart_name,
        "count": count}

    encoded_сart = json.dumps(cart)
    response = redirect('/')
    response.set_cookie('cart', encoded_сart)
    return response


@app.post('/cart-items/clean')
def clear_item():
    cart = {}
    encoded_сart = json.dumps(cart)
    response = redirect('/')
    response.set_cookie('cart', encoded_сart)
    return response
