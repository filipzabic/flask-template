from flask import Flask
from flask import render_template as template


app = Flask(__name__, template_folder='templates', static_folder='static')
route = app.route


@route('/')
def index():
    return template('index.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
 