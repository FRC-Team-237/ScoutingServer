from server import db 
from flask import Blueprint, abort, current_app, render_template, request
from wtforms import Form, BooleanField, StringField, validators, IntegerField, SubmitField, TextAreaField, SelectField
from wtforms_sqlalchemy.orm import QuerySelectField
from dbObjects.tables import MatchResult, Settings
from dbObjects.tablesV2 import Competition
from sqlalchemy import exc
class SettingsForm(Form):
    competition_location = StringField(u'Add Comp Location', [validators.length(max=4)])
    set_comp = QuerySelectField(u"Set Current Comp",
        get_pk=lambda a: a.id,
        get_label=lambda a: a.competition_name,
        allow_blank=True)
    submit = SubmitField("Save Settings")

settings = Blueprint('settings',__name__,template_folder='templates')

@settings.route('/settings', methods=['GET', 'POST'])
def scoutmatch():
    
    form = SettingsForm()
    form.set_comp.query = db.session.query(Competition).all()
    settings  = db.session.query(Settings).first()
    if request.method == 'POST' and form.validate():
        comp_loc = request.form['competition_location']
        try :
            if comp_loc:
                db.session.add(Competition(competition_name=comp_loc))
            if request.form['set_comp']:
                
                if settings:
                    settings.scouting_app_comp_key = request.form['set_comp']
                else:
                    db.session.add(Settings(scouting_app_comp_key=request.form['set_comp'])) 
            db.session.commit()
        except exc.IntegrityError as err:
            print(err)
            db.session.rollback()
            return render_template('serversettings.jinja',form=form,validation_error="This competition already exits!",settings=settings)
        except:
            db.session.rollback()
            return render_template('serversettings.jinja',form=form,validation_error="Form Error!",settings=settings)
    elif request.method == 'POST' and not form.validate():
        error = 'Form Error :('
        return render_template('serversettings.jinja',form=form,validation_error=error)
    return render_template('serversettings.jinja',form=form,valdation_error='',settings=settings)
