from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Vault
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET','POST'])
@login_required
def home():

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
        try:
            newEntry = request.get_json()
            newEntry = Vault(
                service = newEntry['service'],
                username = newEntry['username'],
                passw = newEntry['password'],
                userID = current_user.id
            )
            db.session.add(newEntry)
            db.session.commit()
            flash('Success', category='success')
            return "success"
        except json.JSONDecodeError:
            flash('Empty response', category='error')
    return render_template("modal.html", user=current_user)
