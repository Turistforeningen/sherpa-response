import os

from flask import Flask, render_template

app = Flask(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host=os.environ['APP_HOST'], port=int(os.environ['APP_PORT']))
