from flask import Blueprint, render_template
from flask_login import login_required

core_bp = Blueprint("core", __name__)

@core_bp.route("/")
#@login_required
def home():
    #msg = Message('Hello', sender='balagrivine@gmail.com', recepient=current_user)
    #msg.body = "Hello Flask message end from AlumniCRM"
    #mail.send(msg)
    return render_template("core/index.html")

