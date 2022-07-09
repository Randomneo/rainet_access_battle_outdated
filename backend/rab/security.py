from bcrypt import checkpw
from bcrypt import gensalt
from bcrypt import hashpw


def hash_password(password):
    return hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')


def check_password(password, hashed):
    return checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
