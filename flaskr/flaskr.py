import os

from flask import Flask

app = Flask(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

if __name__ == '__main__':
    app.run(host=os.environ['APP_HOST'], port=int(os.environ['APP_PORT']))
