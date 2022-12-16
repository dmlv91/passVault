from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from .models import Vault
from . import db

views = Blueprint('views', __name__)

@views.route('/', methods=['GET','POST'])
@login_required
def home():
    if request.method == 'POST':
        passEntry = request.form.get('Vault')

        if len(passEntry) < 1:
            flash('error', category='error')
        else:
            newEntry = Vault(passw=passEntry, user_id=current_user.id)
            db.session.add(newEntry)
            db.session.commit()
            flash('Success', category='success')

    return render_template("home.html", user=current_user)
