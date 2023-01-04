from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Vault
from . import db
import json
from .crypto import pass_encrypt, pass_decrypt

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

@views.route("/modal_insert", methods=['GET','POST'])
def modal_insert():
    if request.method == 'POST':
        try:
            newEntry = request.get_json()
            master = newEntry['master']
            newEntry = Vault(
                service = newEntry['service'],
                username = newEntry['username'],
                passw = pass_encrypt(newEntry['password'].encode(),master),
                userID = current_user.id,
            )
            db.session.add(newEntry)
            db.session.commit()
            flash('Success', category='success')
            return "success"
        except json.JSONDecodeError:
            flash('Empty response', category='error')
    return render_template("modal_insert.html", user=current_user)

@views.route("/modal_passCheck", methods=['GET', 'POST'])
def modal_passCheck():
    if request.method == 'POST':
        try:
            newData = request.get_json()
            print(newData)
            passphrase = newData['password']
            service = newData['service']
            user = newData['username']
            token = db.select([Vault.columns.passw]).where(Vault.columns.service == service, Vault.columns.username == user)
            return pass_decrypt(token,passphrase)

        except json.JSONDecodeError:
            flash('Empty response', category='error')

    return render_template("modal_passCheck.html", user=current_user)