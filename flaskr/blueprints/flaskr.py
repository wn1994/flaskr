import os
from sqlite3 import dbapi2 as sqlite3
from flask import request, session, g, redirect, url_for, abort, \
    render_template, flash, current_app
from . import bp


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(current_app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db(db_path):
    """Initializes the database."""
    db = sqlite3.connect(db_path)
    db.row_factory = sqlite3.Row
    with open(os.path.join(os.path.dirname(db_path), 'schema.sql'), mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@bp.before_request
def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.db = connect_db()


@bp.route('/')
def show_entries():
    cur = g.db.execute('select title, text from entries order by id desc')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)


@bp.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (title, text) values (?, ?)', [request.form['title'], request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    # print url_for('.add_entry')  #/add
    return redirect(url_for('.show_entries'))


@bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != current_app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != current_app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('.show_entries'))
    return render_template('login.html', error=error)


@bp.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('.show_entries'))
