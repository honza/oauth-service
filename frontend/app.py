from flask import Flask, request, session, redirect, url_for
from api import get_color, authenticate


app = Flask(__name__)
app.secret_key = 'jldfkjs'


@app.route('/')
def index():
    if "token" not in session:
        return redirect(url_for('login'))

    user = {
        'access_token': session.get('token'),
        'access_token_secret': session.get('secret')
    }

    data = get_color(user)

    if not data:
        return ('Forbidden', 403)

    return """
    <html>
    <head>
    <style>
        body {
            background: %s;
        }
    </style>
    </head>
    <body>
    <h1>Hello there</h1>
    <p>Your favorite color is %s.  We've also colored the background as such.</p>
    <p><a href="/logout">Logout</a></p>
    </body>
    </html>
    """ % (data['favorite_color'], data['favorite_color'])


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        token, secret = authenticate(request.form['username'],
            request.form['password'])
        if token and secret:
            session['token'] = token
            session['secret'] = secret
        return redirect(url_for('index'))
    return """
        <form action="" method="post">
            <p>Username: <input type="text" name="username"></p>
            <p>Password: <input type="password" name="password"></p>
            <p><input type="submit" value="Login"></p>
        </form>
        <p><a href="/logout">Logout</a></p>
    """


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(port=4444, debug=True)
