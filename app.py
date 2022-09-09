from functools import wraps
from flask import Flask, request, abort, redirect, url_for, make_response, send_from_directory
from flask import render_template as template
import os


app = Flask(__name__, template_folder='templates', static_folder='static')
route = app.route


@route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


def authorize(f):
    @wraps(f)
    def decorated_function(*args, **kws):

        if request.cookies.get('access'):
            return f(*args, **kws)
        else:
            return redirect(url_for('login'))      
     
    return decorated_function


@route('/')
@authorize
def index():
    return template('index.html')


@route('/logout')
def logout():
    resp = make_response(redirect('/login'))
    resp.set_cookie('access', '', expires=0)

    return resp


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            resp = make_response(redirect('/'))
            resp.set_cookie('access', 'granted')

            return resp

    return template('login.html', error=error)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
