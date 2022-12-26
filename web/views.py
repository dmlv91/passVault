from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Vault
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET','POST'])
@login_required
def home():
    # if request.method == 'POST':
    #     newEntry = Vault(
    #         service = request.form['service-name'],
    #         username = request.form['username'],
    #         passw = request.form['password']
    #     )
    #     if len(newEntry.service,newEntry.username,newEntry.passw) < 1:
    #         flash('error', category='error')
    #     else:
    #         db.session.add(newEntry)
    #         db.session.commit()
    #         flash('Success', category='success')
    #     if len(service) < 1:
    #        flash('error', category='error')
    #     else:            
    #        newEntry = Vault(service = service,username=username,passw=passw, userID=current_user.id)
    #        db.session.add(newEntry)
    #        db.session.commit()
    #        flash('Success', category='success')

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

@views.route("/modal", methods=['GET','POST'])
def modal():
    if request.method == 'POST':
        newEntry = json.loads(request.data)
        service = newEntry['service']
        username = newEntry['username']
        passw = newEntry['password']
        print(newEntry)
        newEntry = Vault(
            service = service,
            username = username,
            passw = passw
        )
        if len(str(service)) < 1:
            flash('error', category='error')
        else:
            db.session.add(newEntry)
            db.session.commit()
            flash('Success', category='success')

    return render_template("modal.html", user=current_user)
