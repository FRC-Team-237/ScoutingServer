from server import db 
from flask import Blueprint, abort, current_app, render_template, request
from wtforms import Form, BooleanField, StringField, validators, IntegerField, SubmitField, TextAreaField, SelectField
from dbObjects.tables import MatchResult, Settings

class MatchForm(Form):
    match_number = IntegerField('Match Number',[validators.NumberRange(min=1, max=100)])
    alliance_station = SelectField('Alliance Station',choices=['Red 1', 'Red 2', 'Red 3', 'Blue 1', 'Blue 2', 'Blue 3'])
    team_number = IntegerField('Team Number',[validators.NumberRange(min=1,max=99999)])
    auto_high_score = IntegerField('Auto High Score',[validators.InputRequired()])
    auto_low_score = IntegerField('Auto Low Score',[validators.InputRequired()])
    tele_op_high_score = IntegerField('Tele Op High Score',[validators.InputRequired()])
    tele_op_low_score = IntegerField('Tele Op Low Score',[validators.InputRequired()])
    hang_lvl_1 = BooleanField('Hang Level 1')
    hang_lvl_2 = BooleanField('Hang Level 2')
    hang_lvl_3 = BooleanField('Hang Level 3')
    hang_lvl_4 = BooleanField('Hang Level 4')
    played_defence = BooleanField('Played Defence')
    won_match = BooleanField('Won Match')
    notes = TextAreaField('Notes')
    submit = SubmitField("Submit Match")

scouting = Blueprint('scouting',__name__,template_folder='templates')

@scouting.route('/matches', methods=['GET', 'POST'])
def scoutmatch():
    
    form = MatchForm()
    if request.method == 'POST' and form.validate():
        settings = db.session.query(Settings).filter(Settings.oid ==1).first()
        result = MatchResult(
            match_number= request.form['match_number'],
            alliance_station= request.form['alliance_station'],
            team_number= request.form['team_number'],
            auto_high_score= request.form['auto_high_score'],
            auto_low_score= request.form['auto_low_score'],
            tele_op_high_score= request.form['tele_op_high_score'],
            tele_op_low_score= request.form['tele_op_low_score'],
            hang_lvl_1= request.form['hang_lvl_1'],
            hang_lvl_2= request.form['hang_lvl_2'],
            hang_lvl_3= request.form['hang_lvl_3'],
            hang_lvl_4= request.form['hang_lvl_4'],
            notes= request.form['notes'],
            played_defence= request.form['played_defence'],
            won_match= request.form['won_match'],
            auto_line= True,
            comp_loc = settings.scouting_app_comp_key
            )
        try:
            db.session.add(result)
            db.session.commit()
        except:
            print("insert Failed ")
            db.rollback()
        return render_template('match_scouting.jinja',form=form,valdation_error='')
    elif request.method == 'POST' and not form.validate():
        error = 'Form Error :('
        return render_template('match_scouting.jinja',form=form,valdation_error=error)
    return render_template('match_scouting.jinja',form=form,valdation_error='')
    return "", 200