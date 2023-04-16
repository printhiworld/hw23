import os
from flask import Flask, request
from werkzeug.exceptions import BadRequest

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

def limit(it, value):
    d = 0
    for i in it:
        if i < value:
            yield i
        else:
            break
        d += 1

def apply_cmd(it, cmd, value):
    if cmd == 'filter':
        return filter(lambda x: value in x, it)
    if cmd == 'map':
        return map(lambda x: x.split()[int(value)], it)
    if cmd == 'unique':
        return iter(set(it))
    if cmd == 'sort':
        return sorted(it, reverse=(value=='desc'))
    if cmd == 'limit':
        return limit(it, int(value))
def build_query(it, cmd1, value1, cmd2, value2):
    it = apply_cmd(it, cmd1, value1)
    it = apply_cmd(it, cmd2, value2)
    return it
@app.route("/perform_query")
def perform_query():
    # получить параметры query и file_name из request.args, при ошибке вернуть ошибку 400
    try:
        file_name = request.json['file_name']
        cmd1 = request.json['cmd1']
        value1 = request.json['value1']
        cmd2 = request.json['cmd2']
        value2 = request.json['value2']
    except :
        raise BadRequest
    # проверить, что файла file_name существует в папке DATA_DIR, при ошибке вернуть ошибку 400
    file_path = os.path.join(DATA_DIR, file_name)
    if not os.path.exists(file_path):
        return BadRequest
    # с помощью функционального программирования (функций filter, map), итераторов/генераторов сконструировать запрос
    with open(file_path) as file:
        res = build_query(file, cmd1, value1, cmd2, value2)
        data = '\n'.join(res)
    # вернуть пользователю сформированный результат
    return app.response_class(data, content_type="text/plain")

app.run()
