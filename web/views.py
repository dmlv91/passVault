from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Vault
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET','POST'])
@login_required
def home():
    if request.method == 'POST':
        newEntry = request.form.get('newEntry').split(",")
        service = str(newEntry[0])
        username = str(newEntry[1])
        passw = str(newEntry[2])
        if len(str(newEntry)) < 1:
            flash('error', category='error')
        else:            
            newEntry = Vault(service = service,username=username,passw=passw, userID=current_user.id)
            db.session.add(newEntry)
            db.session.commit()
            flash('Success', category='success')

    return render_template("home.html", user=current_user)

@views.route('/delete-entry', methods=['POST'])
def deleteEntry():
    entry = json.loads(request.data)
    entryID = entry['entryID']
    entry = Vault.query.get(entryID)
    if entry:
        if entry.userID == current_user.id:
            db.session.delete(entry)
            db.session.commit()
        
    return jsonify({})
