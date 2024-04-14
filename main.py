from flask import Flask, render_template, redirect, abort, request
from requests import get, post, delete, put
from secrets import SECRET_KEY, LOAD_DATA  # Файл доступ к которому имеет только создатель проекта
from random import choices, randint, choice, uniform

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

app.run(port=8880, host='127.0.0.1', debug=True)

