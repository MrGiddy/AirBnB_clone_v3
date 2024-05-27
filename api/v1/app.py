#!/usr/bin/python3
"""Instantiates the HBNB flask application"""
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def call_storage_dot_close(exception=None):
    """Closes the storage connection"""
    storage.close()


if __name__ == "__main__":
    if getenv('HBNB_API_HOST'):
        app.run(
            host=getenv('HBNB_API_HOST'),
            port=getenv('HBNB_API_PORT'),
            threaded=True)
    else:
        app.run(host='0.0.0.0', port=5000, threaded=True)
