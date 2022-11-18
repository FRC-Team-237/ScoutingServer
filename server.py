from flask import Flask
from flask_sqlalchemy import SQLAlchemy




def create_app(config: str):
    app = Flask(__name__ ,instance_relative_config=True)
    app.config.from_pyfile(config)
    return app

def register_bluprints(app):
    from blueprints.stats import stats
    app.register_blueprint(stats)
    return


app = create_app('devel.cfg')
db = SQLAlchemy(app)
with app.app_context():
    register_bluprints(app)
        