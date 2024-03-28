from .views import core_bp
#from flask_mail import Mail, Message
#from src import app

"""app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'balagrivine@gmail.com'
app.config['MAIL_PASSWORD'] = 'georgebala254'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True"""

#mail = Mail(app)

@core_bp.route("/email")
def index():
    """msg = Message('Hello', sender = 'balagrivine@gmail.com', recipients = ['balagrivine@gmail.com'])
    msg.body = "This is the email body"
    mail.send(msg)"""
    return "Sent"
