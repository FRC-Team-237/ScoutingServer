from flask import Blueprint, current_app, render_template

analysis = Blueprint('analysis', __name__, template_folder='templates')

@analysis.route('/analysis')
def showAnalysis():
	with current_app.app_context():
		return render_template('analysis.jinja')