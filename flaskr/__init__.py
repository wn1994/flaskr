# -*- coding: utf-8 -*-
"""
    Flaskr
    ~~~~~~

    A microblog example application written as Flask tutorial with
    Flask and sqlite3.

    :copyright: © 2010 by the Pallets team.
    :license: BSD, see LICENSE for more details.
"""

import os
from flask import Flask, g, render_template
from blueprints.flaskr import init_db
from blueprints import bp

default_config = dict(
        DATABASE=os.path.join(os.path.dirname(__file__), 'flaskr.db'),
        DEBUG=True,
        SECRET_KEY=b'_5#y2L"F4Q8z\n\xec]/',
        USERNAME='admin',
        PASSWORD='admin'
    )


def create_app(config=None, is_initdb=False):
    app = Flask(__name__)
    app.config.update(default_config)
    app.config.update(config or {})
    app.config.from_envvar('FLASKR_SETTINGS', silent=True)
    register_blueprints(app)
    if is_initdb:
        init_db(app.config['DATABASE'])
    # with app.app_context():
    #     init_db()
    # register_cli(app)
    register_teardowns(app)
    register_404(app)

    return app


def register_blueprints(app):
    """Register all blueprint modules"""
    app.register_blueprint(bp)
    return None


# def register_cli(app):
#     @app.cli.command('initdb')
#     def initdb_command():
#         """Creates the database tables."""
#         init_db()
#         print('Initialized the database.')


def register_teardowns(app):
    @app.teardown_appcontext
    def close_db(error=None):
        """Closes the database again at the end of the request."""
        if hasattr(g, 'sqlite_db'):
            g.sqlite_db.close()


def register_404(app):
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404
