from sqlalchemy import (BOOLEAN, VARCHAR, Column, Integer, String, Float, FLOAT, 
                        UniqueConstraint, ForeignKey)

from server import db

class MatchPoints(db.Model): # type: ignore 
    __tablename__ = 'scoring_avg_vw'
    id = Column(Integer, primary_key=True)
    team_number = Column(Integer)
    row_position = Column(String(3))
    tele_op_avg = Column(Integer)
    auto_avg = Column(Integer)

class TeamScoringRowView(db.Model): # type: ignore 
    __tablename__ = 'team_row_scores_vw'
    id = Column(Integer, primary_key=True)
    team_number = Column(Integer)
    top = Column(Integer)
    mid = Column(Integer)
    low = Column(Integer)

class MatchResult(db.Model):  # type: ignore 
    __tablename__ = "match_results"
    
    result_oid = Column(Integer,primary_key=True)
    match_number = Column(Integer)
    team_number = Column(Integer)
    alliance_station = Column(VARCHAR(45))
    auto_low = Column(Integer)
    auto_high = Column(Integer)
    tele_op_low = Column(Integer)
    tele_op_high = Column(Integer)
    auto_line = Column(BOOLEAN)
    hang_1 = Column(BOOLEAN)
    hang_2 = Column(BOOLEAN)
    hang_3 = Column(BOOLEAN)
    hang_4 = Column(BOOLEAN)
    played_defence = Column(BOOLEAN)
    won_match = Column(BOOLEAN)
    notes = Column(String(255))
    comp_loc = Column(VARCHAR(45))
    UniqueConstraint('match_number','team_number','comp_loc') 

class MoneyBall(db.Model): # type: ignore 
    __tablename__ = "money_ball_vw"
    team_number = Column(Integer,primary_key='true')
    avg_auto_score = Column(Float)
    std_auto = Column(Float)
    avg_tele_score = Column(Float) 
    std_tele = Column(Float)
    avg_hang_4_pts   = Column(Float) 
    avg_hang_3_pts   = Column(Float) 
    avg_hang_2_pts   = Column(Float) 
    avg_end_game     = Column(Float)
    std_end_game     = Column(Float)
    avg_total_points = Column(Float)
    std_total_points = Column(Float)