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
    
#Route for entry deletion from database
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

#Route for database insertion modal
@views.route("/modal_insert", methods=['GET','POST'])
def modal_insert():
    #check request method, go on with request processing only if POST received
    if request.method == 'POST':
        try:
            #Initialize variables from request object
            newEntry = request.get_json()
            master = newEntry['master']
            #define user and check if master password is correct
            user = User.query.filter_by(id=current_user.id).first()
            if check_password_hash(user.password, master):
                #encrypt password entry and insert into database
                passw = pass_encrypt(newEntry['password'].encode(),master)
                #Create database entry object and commit data to database
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
            else:
                return "wrongPass"
        except json.JSONDecodeError:
            flash('Empty response', category='error')

    return render_template("modal_insert.html", user=current_user)

#Route for "Show Password" modal
@views.route("/modal_passCheck", methods=['GET', 'POST'])
def modal_passCheck():
    #check request method, go on with request processing only if POST received
    if request.method == 'POST':
        try:
            #Initialize variables from request object
            newData = request.get_json()
            passphrase = newData['password']
            entryID = newData['entryID']
            user = User.query.filter_by(id=current_user.id).first()
            #Check if users input hash == MASTER passwords hash
            if check_password_hash(user.password, passphrase):
                #Get stored encrypted password from Vault and use it for decryption
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
