from server import db 
from flask import Blueprint, abort, current_app, render_template, request
from wtforms import Form, BooleanField, StringField, validators, IntegerField, SubmitField, TextAreaField, SelectField
from dbObjects.tables import Settings
from dbObjects.tablesV2 import MatchWatchResult, TeamWatchResult, ScoringRow
import json

scouting = Blueprint('scouting',__name__,template_folder='templates')

@scouting.route('/matches', methods=['GET', 'POST'])
def scoutmatch():
    
    if request.method == 'POST' :
        settings = db.session.query(Settings).filter(Settings.oid ==1).first()
        print (request.json)
        try:
            match_result = json.loads(request.json)# type: ignore    
            team = TeamWatchResult(
                
            )
            match_data = MatchWatchResult(

            )
            row_high = ScoringRow()
            row_mid = ScoringRow()
            row_low = ScoringRow()
            
        except:
            print("insert Failed ")
            db.rollback()
        return render_template('match_form.jinja',valdation_error='')
    elif request.method == 'POST':
        error = 'Form Error :('
        return render_template('match_form.jinja',valdation_error=error)
    return render_template('match_form.jinja',valdation_error='')