from flask import Blueprint, abort, current_app, render_template, jsonify
from jinja2 import TemplateNotFound
from sqlalchemy import func
from dbObjects.tables import MoneyBall
from dbObjects.tablesV2 import TeamWatchResult, MatchWatchResult, ScoringRow
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

@stats.route('/matches/<match_no>')
def match(match_no): # type: ignore
    with current_app.app_context():
        team_data = db.session.query(TeamWatchResult).filter(TeamWatchResult.match_number == match_no).all()
        match_dict = {
            'red' : {
                'auto' : {
                    'charge' : 0,
                    'mobility' : 0,
                    'placement' : 0    
                },
                'tele' : {
                    'placement' : 0 
                },
                'end' : {
                    'charge' : 0
                },
                'links' : 0,
                'win': False
            },
            'blue' : {
                'auto' : {
                    'charge' : 0,
                    'mobility' : 0,
                    'placement' : 0    
                },
                'tele' : {
                    'placement' : 0 
                },
                'end' : {
                    'charge' : 0
                },
                'links' : 0,
                'win': False
            }
        }  
        for team in team_data:
            match_dict[team.alliance_color]['win'] = team.win
            match_data:MatchWatchResult = team.result
            if match_dict[team.alliance_color]['auto'] == 0: 
                match_dict[team.alliance_color]['auto'] = 8 if match_data.auto_charge == 1 else 12
            if match_data.auto_mobility:
                match_dict[team.alliance_color]['auto']['mobility']+=3
            if match_data.end_charge == 1:
                match_dict[team.alliance_color]['end']['charge'] +=6
            elif match_data.end_charge == 2:
                match_dict[team.alliance_color]['end']['charge'] +=10
            for row in match_data.scoring_rows:
                score_inc = 0
                if row.row_position == 'top':
                    score_inc = 5
                elif row.row_position == 'mid':
                    score_inc = 3
                else:    
                    score_inc = 2
                for x in range(1,9):
                    #if pos obj < 0 : scored in auto 
                    #if pos obj > 0 : scored in tele 
                    pos_obj = row.__dict__[f'scoring_position_{x}']
                    if pos_obj < 0:
                        match_dict[team.alliance_color]['auto']['placement'] += (score_inc+1)
                    elif pos_obj > 0:
                        match_dict[team.alliance_color]['tele']['placement'] += score_inc
        linkCalc(match_no=match_no,alliance_color='blue')
        return jsonify(match_dict), 200 
    
def linkCalc(match_no,alliance_color):
    with current_app.app_context():
        alliance_score_grid = db.session.query(
            func.sum(ScoringRow.scoring_position_1),
            func.sum(ScoringRow.scoring_position_2),
            func.sum(ScoringRow.scoring_position_3),
            func.sum(ScoringRow.scoring_position_4),
            func.sum(ScoringRow.scoring_position_5),
            func.sum(ScoringRow.scoring_position_6),
            func.sum(ScoringRow.scoring_position_7),
            func.sum(ScoringRow.scoring_position_8),
            func.sum(ScoringRow.scoring_position_9)
            ).select_from(TeamWatchResult).join(TeamWatchResult.result).join(MatchWatchResult.scoring_rows, isouter=True).filter(TeamWatchResult.match_number == match_no).filter(TeamWatchResult.alliance_color == alliance_color).group_by(ScoringRow.row_position).all()
        link_count = 0;
        for row in alliance_score_grid:
            