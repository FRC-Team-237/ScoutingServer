from server import db 
from flask import Blueprint, abort, current_app, render_template, request
from wtforms import Form, BooleanField, StringField, validators, IntegerField, SubmitField, TextAreaField, SelectField

from dbObjects.tablesV2 import MatchWatchResult, TeamWatchResult, ScoringRow, Settings
import json

scouting = Blueprint('scouting',__name__,template_folder='templates')

@scouting.route('/matches', methods=['GET', 'POST'])
def scoutmatch():
    
    if request.method == 'POST' :
        settings = db.session.query(Settings).first()
        
        print (request.json)
        try:
            match_result = {}
            if request.json:
                match_result = request.json 
            
            
            match_data = MatchWatchResult(
                auto_mobility = match_result['autonomous']['mobility'],
                auto_charge = match_result['autonomous']['charge'],
                end_charge = match_result['endgame']['charge']

            )
            team = TeamWatchResult(
                competition_id = settings.scouting_app_comp_key,
                alliance_color = match_result['alliance'],
                match_number = match_result['matchNumber'],
                team_number = match_result['teamNumber'],
                notes = match_result['notes'],
                win = match_result['win'],
                result = match_data

            )
            row_high = ScoringRow(
                row_position = 'top',
                scoring_position_1 = match_result['scoreMatrix']['high'][0],
                scoring_position_2 = match_result['scoreMatrix']['high'][1],
                scoring_position_3 = match_result['scoreMatrix']['high'][2],
                scoring_position_4 = match_result['scoreMatrix']['high'][3],
                scoring_position_5 = match_result['scoreMatrix']['high'][4],
                scoring_position_6 = match_result['scoreMatrix']['high'][5],
                scoring_position_7 = match_result['scoreMatrix']['high'][6],
                scoring_position_8 = match_result['scoreMatrix']['high'][7],
                scoring_position_9 = match_result['scoreMatrix']['high'][8],
                match_result = match_data
                )
            row_mid = ScoringRow(
                row_position = 'mid',
                scoring_position_1 = match_result['scoreMatrix']['mid'][0],
                scoring_position_2 = match_result['scoreMatrix']['mid'][1],
                scoring_position_3 = match_result['scoreMatrix']['mid'][2],
                scoring_position_4 = match_result['scoreMatrix']['mid'][3],
                scoring_position_5 = match_result['scoreMatrix']['mid'][4],
                scoring_position_6 = match_result['scoreMatrix']['mid'][5],
                scoring_position_7 = match_result['scoreMatrix']['mid'][6],
                scoring_position_8 = match_result['scoreMatrix']['mid'][7],
                scoring_position_9 = match_result['scoreMatrix']['mid'][8],
                match_result = match_data
                )
            row_low = ScoringRow(
                row_position = 'low',
                scoring_position_1 = match_result['scoreMatrix']['low'][0],
                scoring_position_2 = match_result['scoreMatrix']['low'][1],
                scoring_position_3 = match_result['scoreMatrix']['low'][2],
                scoring_position_4 = match_result['scoreMatrix']['low'][3],
                scoring_position_5 = match_result['scoreMatrix']['low'][4],
                scoring_position_6 = match_result['scoreMatrix']['low'][5],
                scoring_position_7 = match_result['scoreMatrix']['low'][6],
                scoring_position_8 = match_result['scoreMatrix']['low'][7],
                scoring_position_9 = match_result['scoreMatrix']['low'][8],
                match_result = match_data
            )
            match_data.watch_result = [team]
            row_high.match_result = match_data
            row_mid.match_result = match_data
            row_low.match_result = match_data
            db.session.add(match_data)
            db.session.commit()
            return render_template('match_form.jinja',submit_msg='Match Submitted!')
        except:
            print("insert Failed ")
            db.rollback()
            return render_template('match_form.jinja',validation_error='Submission Failed')
        return render_template('match_form.jinja',valdation_error='')
    elif request.method == 'POST':
        error = 'Form Error :('
        return render_template('match_form.jinja',valdation_error=error)
    return render_template('match_form.jinja',valdation_error='')