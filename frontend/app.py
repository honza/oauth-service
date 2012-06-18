from flask import Flask, request, session, redirect, url_for
from api import get_greeting, authenticate


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

    data = get_greeting(user)

    if not data:
        return ('Forbidden', 403)

    return "Your greeting: %s" % data['greeting']


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
    """


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(port=4444, debug=True)
