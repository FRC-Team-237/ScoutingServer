from sqlalchemy import (BOOLEAN, VARCHAR, Column, Integer, String,
                        UniqueConstraint)

from server import db


class MatchResult(db.Model):  # type: ignore 
    __tablename__ = "match_results"
    __table_args__ = {
        'autoload':True,
        'autoload_with': db.engine,
        'schema' : 'scouting_db'
    }
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
    notes = Column(String)
    comp_loc = Column(VARCHAR(45))
    UniqueConstraint('match_number','team_number','comp_loc') 

class MoneyBall(db.Model): # type: ignore 
    __tablename__ = "money_ball_vw"
    __table_args__ = {
        'autoload':True,
        'autoload_with': db.engine,
        'schema' : 'scouting_db'   
    }
    team_number = Column(Integer,primary_key='true')

class Settings(db.Model): # type: ignore 
    __tablename__ = "server_settings_table"
    __table_args__ = {
        'autoload':True,
        'autoload_with': db.engine,
        'schema' : 'scouting_db'  
    }
    oid = Column(Integer,primary_key=True)
    scouting_app_comp_key = Column(String)
    blue_alliance_comp_key = Column(String)