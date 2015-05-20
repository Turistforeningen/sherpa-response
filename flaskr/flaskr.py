import os
import pickle

from flask import Flask, render_template

import redis
from raven.contrib.flask import Sentry

from udp import Listener

app = Flask(__name__)
if os.environ.get('CONFIGURATION', 'prod').lower() == 'prod':
    app.config['DEBUG'] = False
else:
    app.config['DEBUG'] = True

sentry = Sentry(app)

# Paths are stored in the 'paths' redis hash.
# Keys are the paths with query string, and the value is (response time, count)
r = redis.StrictRedis(host='redis', port=6379, db=0)

def add_measure(path, new_measure):
    result = r.hget('paths', path)
    if result is None:
        r.hset('paths', path, pickle.dumps((new_measure, 1)))
    else:
        old_measure, count = pickle.loads(result)
        r.hset('paths', path, pickle.dumps((
            calc_new_value(old_measure, new_measure, count),
            count + 1,
        )))

def calc_new_value(old_measure, new_measure, count):
    """
    Factor the total count in to the difference of the new value.
    E.g. for a value of 100ms with 50 measurements, a new measure of 150ms would add 1 ms to the total
    """
    return (old_measure + (old_measure + (new_measure - old_measure) * (1.0 / count))) / 2.0

def sort_paths(paths):
    paths_parsed = []
    for path, s in paths.items():
        value, count = pickle.loads(s)
        paths_parsed.append((path.decode('utf-8'), value, count))

    return reversed(sorted(paths_parsed, key=lambda p: p[1])[-100:])

@app.route('/')
def index():
    paths = r.hgetall('paths')
    return render_template('index.html', paths=sort_paths(paths))

if __name__ == '__main__':
    # Start the UDP listener thread
    if not app.config['DEBUG']:
        listener = Listener(callback=add_measure)
        listener.start()

    # Start the Flask app
    app.run(host=os.environ['APP_HOST'], port=int(os.environ['APP_PORT']))
