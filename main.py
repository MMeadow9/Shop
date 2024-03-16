from flask import Flask, render_template, redirect, abort, request
from data.db_session import global_init, create_session
from data.card import *
from data.user import *
from data.product import *
from data.db_session import *
import os
from wtforms import Label
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from random import randint, choices, choice
from werkzeug.security import generate_password_hash


def load_data():
    if os.path.isfile("db/blogs.db"):
        return
    global_init("db/blogs.db")

    db_sess = create_session()

    db_sess.commit()


load_data()
