from flask import Blueprint, current_app, render_template
from server import db
import pandas as pd
import json
from sqlalchemy import func, case 
from dbObjects.tablesV2 import TeamWatchResult, ScoringRow, MatchWatchResult
from dbObjects.views import MatchPoints, TeamScoringRowView
analysis = Blueprint('analysis', __name__, template_folder='templates')

@analysis.route('/analysis')
def showAnalysis():
    with current_app.app_context():
        result = db.session.query(
            TeamWatchResult.team_number,
            ScoringRow.row_position,
            ScoringRow.scoring_position_1,
            ScoringRow.scoring_position_2,
            ScoringRow.scoring_position_3,
            ScoringRow.scoring_position_4,
            ScoringRow.scoring_position_5,
            ScoringRow.scoring_position_6,
            ScoringRow.scoring_position_7,
            ScoringRow.scoring_position_8,
            ScoringRow.scoring_position_9,
        ).select_from(TeamWatchResult).join(TeamWatchResult.result).join(MatchWatchResult.scoring_rows, isouter=True).all()

        result_json = json.dumps([{
            "team_number": r.team_number,
            "row_position": r.row_position,
            "row_position_1": r.scoring_position_1,
            "row_position_2": r.scoring_position_2,
            "row_position_3": r.scoring_position_3,
            "row_position_4": r.scoring_position_4,
            "row_position_5": r.scoring_position_5,
            "row_position_6": r.scoring_position_6,
            "row_position_7": r.scoring_position_7,
            "row_position_8": r.scoring_position_8,
            "row_position_9": r.scoring_position_9,
        } for r in result])
        avg_scores = db.session.query(
            TeamScoringRowView.team_number,
            func.avg(TeamScoringRowView.top),
            func.std(TeamScoringRowView.top),
            func.avg(TeamScoringRowView.mid),
            func.std(TeamScoringRowView.mid),
            func.avg(TeamScoringRowView.low),
            func.std(TeamScoringRowView.low)
            ).group_by(TeamScoringRowView.team_number).order_by().all()
        rankings_json = json.dumps([{
            "team_number": r.team_number,
            "avg_top": "{:.2f}".format(float(r[1])),
            "std_top": "{:.2f}".format(float(r[2])),
            "avg_mid": "{:.2f}".format(float(r[3])),
            "std_mid": "{:.2f}".format(float(r[4])),
            "avg_low": "{:.2f}".format(float(r[5])),
            "std_low": "{:.2f}".format(float(r[6])),
        }for r in avg_scores])

        
        return render_template('analysis.jinja', score_result=result_json,results=rankings_json)
    
    