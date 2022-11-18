from flask import Blueprint, abort, current_app, render_template
from jinja2 import TemplateNotFound

from dbObjects.tables import MoneyBall
from server import db

stats = Blueprint('stats',__name__,template_folder='templates')

@stats.route('/moneyball')
def showMoneyBall():
    with current_app.app_context():
        results = db.session.query(MoneyBall).all()
        try:
            return render_template('money_ball.jinja',results=results)
        except TemplateNotFound:
            abort(404)