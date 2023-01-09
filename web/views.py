from flask import Blueprint, render_template, request, flash, jsonify,redirect,url_for
from flask_login import login_required, current_user
from sqlalchemy import select
from werkzeug.security import check_password_hash
from .models import User,Vault
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
            passw = pass_encrypt(newEntry['password'].encode(),master)
            newEntry = Vault(
                service = newEntry['service'],
                username = newEntry['username'],
                passw = passw.decode(),
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
            passphrase = newData['password']
            entryID = newData['entryID']
            user = User.query.filter_by(id=current_user.id).first()
            if check_password_hash(user.password, passphrase):
                stmt = select(Vault.passw).where(Vault.id == entryID)
                for row in db.session.execute(stmt):
                    token = str(row)        
                password = pass_decrypt(token,passphrase).decode()

                return password
            else:
                return "wrongPass"
        except json.JSONDecodeError:
            flash('Empty response', category='error')


    if request.method == 'GET':
        entryID = request.args.get('entryID', None)
        return render_template("modal_passCheck.html", user=current_user, entryID=entryID)
