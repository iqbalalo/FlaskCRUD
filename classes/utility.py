import secrets as sc
import datetime


def token():
    return sc.token_hex(16)


def now():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')