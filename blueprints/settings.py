from server import db 
from flask import Blueprint, abort, current_app, render_template, request
from wtforms import Form, BooleanField, StringField, validators, IntegerField, SubmitField, TextAreaField, SelectField
from dbObjects.tables import MatchResult, Settings
from dbObjects.tablesV2 import Competition

class SettingsForm(Form):
    competition_location = StringField(u'Add Comp Location', [validators.length(max=4)])
    submit = SubmitField("Save Settings")

settings = Blueprint('settings',__name__,template_folder='templates')

@settings.route('/settings', methods=['GET', 'POST'])
def scoutmatch():
    
    form = SettingsForm()
    if request.method == 'POST' and form.validate():
        comp_loc = request.form['competition_location']
        try :
            db.session.add(Competition(competition_name=comp_loc))
            db.session.commit()
        except:
            print("Update Failed")
            db.rollback()
    elif request.method == 'POST' and not form.validate():
        error = 'Form Error :('
        return render_template('serversettings.jinja',form=form,valdation_error=error)
    return render_template('serversettings.jinja',form=form,valdation_error='')
