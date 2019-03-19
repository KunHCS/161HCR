"""
Configuration values for flask
"""
from pathlib import Path

db_name = 'bank_database'


class Config:
    FLASK_ENV = 'development'
    SECRET_KEY = 'dev'
    TEMPLATE_PATH = Path('../client/build')
    STATIC_PATH = Path('../client/build/static')
