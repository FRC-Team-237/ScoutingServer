from server import db 
from flask import Blueprint, abort, current_app, render_template, request
from wtforms import Form, BooleanField, StringField, validators, IntegerField, SubmitField, TextAreaField, SelectField

from dbObjects.tablesV2 import MatchWatchResult, TeamWatchResult, ScoringRow, Settings
import json

scouting = Blueprint('scouting',__name__,template_folder='templates')

@scouting.route('/upload',methods=['POST'])
def uploadResults():
    if request.method != 'POST':
        abort(404)
    if not request.json:
        abort(500)
    match_result_list = {}
    match_result_list = request.json
    settings = db.session.query(Settings).first()
    try: 
        for result in match_result_list: 
            for team in result['teamData']:
                watch_data = MatchWatchResult(
                    auto_mobility = team['autonomous']['mobility'],
                    auto_charge = team['autonomous']['charge'],
                    end_charge = team['endgame']['charge']
                ) 
                team_data = TeamWatchResult(
                    competition_id = settings.scouting_app_comp_key,
                    alliance_color = result['alliance'],
                    match_number = result['matchNumber'],
                    team_number = team['teamNumber'],
                    notes = team['notes'],
                    win = result['win'],
                    result = watch_data
                )
                row_high = ScoringRow(
                    row_position = 'top',
                    scoring_position_1 = team['scoreMatrix']['high'][0],
                    scoring_position_2 = team['scoreMatrix']['high'][1],
                    scoring_position_3 = team['scoreMatrix']['high'][2],
                    scoring_position_4 = team['scoreMatrix']['high'][3],
                    scoring_position_5 = team['scoreMatrix']['high'][4],
                    scoring_position_6 = team['scoreMatrix']['high'][5],
                    scoring_position_7 = team['scoreMatrix']['high'][6],
                    scoring_position_8 = team['scoreMatrix']['high'][7],
                    scoring_position_9 = team['scoreMatrix']['high'][8],
                    match_result = watch_data
                    )
                row_mid = ScoringRow(
                    row_position = 'mid',
                    scoring_position_1 = team['scoreMatrix']['mid'][0],
                    scoring_position_2 = team['scoreMatrix']['mid'][1],
                    scoring_position_3 = team['scoreMatrix']['mid'][2],
                    scoring_position_4 = team['scoreMatrix']['mid'][3],
                    scoring_position_5 = team['scoreMatrix']['mid'][4],
                    scoring_position_6 = team['scoreMatrix']['mid'][5],
                    scoring_position_7 = team['scoreMatrix']['mid'][6],
                    scoring_position_8 = team['scoreMatrix']['mid'][7],
                    scoring_position_9 = team['scoreMatrix']['mid'][8],
                    match_result = watch_data
                    )
                row_low = ScoringRow(
                    row_position = 'low',
                    scoring_position_1 = team['scoreMatrix']['low'][0],
                    scoring_position_2 = team['scoreMatrix']['low'][1],
                    scoring_position_3 = team['scoreMatrix']['low'][2],
                    scoring_position_4 = team['scoreMatrix']['low'][3],
                    scoring_position_5 = team['scoreMatrix']['low'][4],
                    scoring_position_6 = team['scoreMatrix']['low'][5],
                    scoring_position_7 = team['scoreMatrix']['low'][6],
                    scoring_position_8 = team['scoreMatrix']['low'][7],
                    scoring_position_9 = team['scoreMatrix']['low'][8],
                    match_result = watch_data
                )
                watch_data.watch_result = [team_data]
                row_high.match_result = watch_data
                row_mid.match_result = watch_data
                row_low.match_result = watch_data
                db.session.add(watch_data)
        db.session.commit()
    except:
        db.rollback()
        return 'Failure', 500
    return "Sucess", 200

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
                team_number = match_result['teamData']['teamNumber'],
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