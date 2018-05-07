from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from classes import utility
from classes.sqlite import Sqlite

app = Flask(__name__)
app.debug = True

sq = Sqlite("/Volumes/workspace/Python/SetIt/setit.sqlite")


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title="Home", current_tab="home")


@app.route('/user')
def user():
    users = sq.select_all('user')
    ul = []
    for u in users:
        ul.append({"id": u[0], "first_name": u[1], "last_name": u[2], "email": u[3], "phone": u[4], "active": 1})
    return render_template('user.html', title="User List", current_tab="user", users=ul)


@app.route('/user/create')
def create_user():
    return render_template('forms/_new_user.html', title="New User", current_tab="user")


@app.route('/user/save', methods=['POST'])
def save_user():
    if request.method == 'POST':
        data_str = "('%s','%s','%s','%s','%s',%d,'%s','%s')" % (utility.token(), request.form['first_name'],
                                                                request.form['last_name'], request.form['email'],
                                                                request.form['phone'],
                                                                (1 if request.form['active'] == 'true' else 0),
                                                                request.form['password'], utility.now())
        res = sq.insert("user", data_str)
        if res:
            return redirect("/user")
        else:
            return res
    else:
        return "Error"


@app.route('/user/<string:user_id>')
def get_user(user_id):
        data_str = "SELECT * FROM user WHERE id='%s';" %(user_id)
        rows = sq.select_by(data_str)
        print(rows)
        ud = []
        for u in rows:
            ud.append({"id": u[0], "first_name": u[1], "last_name": u[2], "email": u[3], "phone": u[4], "active": 1})
        return render_template('forms/_user_detail.html', title="User Detail", current_tab="user", user=ud[0])


@app.route('/log')
def log():
    return render_template('log.html', title="Log", current_tab="log")


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


if __name__ == '__main__':
    app.run()
