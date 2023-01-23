import pytest
from server import create_app , register_V2_blueprints
from flask_sqlalchemy import SQLAlchemy
@pytest.fixture(scope='module')
def test_client():
    #Set Up 
    app = create_app('test.cfg')
    with app.test_client() as test_client:
        with app.app_context():
            from server import db
            register_V2_blueprints(app)
            from dbObjects import tablesV2
            db.create_all()
            comp = tablesV2.Competition(competition_name='test')
            db.session.add(comp)
            db.session.add(tablesV2.Settings(scouting_app_comp_key=comp.id))
            db.session.commit()
            yield test_client
            #tear down 
            db.drop_all()


