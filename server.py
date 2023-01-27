from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS



def create_app(config=None):
    global db
    app = Flask(__name__ ,instance_relative_config=True)
    if not config:
        app.config.from_pyfile('devel.cfg')
    else:
        app.config.from_pyfile(config)
    db = SQLAlchemy(app)
    CORS(app)
    with app.app_context():
        register_bluprints(app)
        from dbObjects import tablesV2
        db.create_all()
    return app

def register_bluprints(app):
    from blueprints.stats import stats
    from blueprints.scouting import scouting
    from blueprints.settings import settings
    app.register_blueprint(settings)
    app.register_blueprint(stats)
    app.register_blueprint(scouting)
    return
def register_V2_blueprints(app):
    from blueprints.scouting import scouting
    app.register_blueprint(scouting)



    