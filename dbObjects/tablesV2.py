from sqlalchemy import (BOOLEAN, VARCHAR, Column, Integer, String,
                        UniqueConstraint, ForeignKey)

from server import db

class Competition(db.Model): # type: ignore
    __tablename__ = "competition_tb"
    
    id  = db.Column('id',db.Integer, primary_key = True)
    competition_name = db.Column('competiton_name',db.String(4))

class MatchWatchResult(db.Model): # type: ignore
    __tablename__ = 'match_watch_result_tb'
    
    id  = db.Column('id',db.Integer, primary_key = True)
    auto_mobility = db.Column('auto_mobility',db.BOOLEAN)
    auto_charge = db.Column('auto_charge', db.String(6))
    end_charge = db.Column('end_charge', db.String(6))
    end_parked = db.Column('end_parked',db.BOOLEAN)
    scoring_rows = db.relationship('ScoringRow',back_populates='id')
    watch_result = db.relationship('TeamWatchResult',back_populates='result_id')    

class TeamWatchResult(db.Model): # type: ignore
    __tablename__ = "team_watch_tb"
    id  = db.Column('id',db.Integer, primary_key = True)
    competition_id = db.Column('competition_id',db.Integer,ForeignKey('competition_tb.id'))
    alliance_color = db.Column('alliance_color', db.String(4))
    match_number = db.Column('match_number',db.Integer)
    team_number = db.Column('team_number',db.Integer)
    notes = db.Column('notes', db.String(240))
    win = db.Column('win',db.BOOLEAN)
    result_id = db.Column('result_id',db.Integer, ForeignKey(MatchWatchResult.id))
    
class ScoringRow(db.Model): # type: ignore
    __tablename__ = 'scoring_row_tb'
    
    id  = db.Column('id',db.Integer, primary_key = True)
    match_result_id = db.Column('match_result_id',ForeignKey(MatchWatchResult.id))
    row_position = db.Column('row_position', db.String(3))
    scoring_position_1 = db.Column('row_position_1', db.BOOLEAN)
    scoring_position_2 = db.Column('row_position_2', db.BOOLEAN)
    scoring_position_3 = db.Column('row_position_3', db.BOOLEAN)
    scoring_position_4 = db.Column('row_position_4', db.BOOLEAN)
    scoring_position_5 = db.Column('row_position_5', db.BOOLEAN)
    scoring_position_6 = db.Column('row_position_6', db.BOOLEAN)
    scoring_position_7 = db.Column('row_position_7', db.BOOLEAN)
    scoring_position_8 = db.Column('row_position_8', db.BOOLEAN)
    scoring_position_9 = db.Column('row_position_9', db.BOOLEAN)
    match_result = db.relationship('MatchWatchResult',back_populates='scoring_rows')
    UniqueConstraint('match_result_id','row_position')