import RPi.GPIO as GPIO
from flask import Flask, render_template,redirect, \
    url_for, request, session, flash, g, abort
from flask_login import UserMixin, login_user, logout_user, login_required, LoginManager, current_user
from flask_sqlalchemy import sqlalchemy, SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

database = "credientals.db"


app = Flask( __name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{db}'.format(db=database)
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "You can't touch what you can't see"

db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100), unique = True, nullable = False)
    password_hashed = db.Column(db.String(100), nullable = False)

def create_db():
    db.create_all()


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#def login_required(f):
#    @wraps(f)
#    def wrap(*args, **kwargs):
#        if 'username' in session:
#            return f(*args, **kwargs)
#        else:
#            flash('You need to login first.')
#            return redirect(url_for('login'))
#    return wrap

@app.route("/signup", methods = ["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        if not (username and password):
            flash('cannot signup: credentials empty!')
            return redirect(url_for('signup'))
        else:
            username = username.strip()
            password = password.strip()

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
        new = User(username = username, password_hashed = hashed_password)
        db.session.add(new)

        try:
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            flash("User {u} already taken!".format(u=username))
            return redirect(url_for("signup"))
        flash("Account has been created!")
        return redirect(url_for("login"))
    return render_template("signup.html")

@app.route("/")
@app.route("/login", methods=["GET","POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password_hashed, password):
        flash("Check your login details please!")
        return render_template("login.html")
    
    login_user(user, remember = remember)
    return redirect(url_for("profile", username=username))

GPIO.setmode(GPIO.BCM)

pins = {
        2: {"name" : "GREEN LED", "state" : GPIO.LOW },
        3: {"name" : "RED LED", "state" : GPIO.LOW},
        14: {"name" : "BLUE LED", "state" : GPIO.LOW }
        }
for p in pins:
    GPIO.setup(p, GPIO.OUT) # set pin as an output
    GPIO.output(p, GPIO.LOW) # set pin low

@app.route("/user")
@login_required
def profile():
    return render_template("user.html", username=current_user.username)

@app.route("/led_control")
@login_required
def led_control():

    for p in pins:
        pins[p]["state"] = GPIO.input(p)

    template = { "pins" : pins}
    return render_template("led_control.html", **template)

@app.route("/<activate>/<action>") # request url with pin number
def action(activate, action):
    change = int(activate) # convert pin from url into int
    device = pins[change]["name"]

    if action ==  "on":
        GPIO.output(change, GPIO.HIGH)
        text = device + "is on"

    if action == "off":
        GPIO.output(change, GPIO.LOW)
        text = device + "is off"

    for p in pins:
        pins[p]["state"] = GPIO.input(p)

    template = {"pins" : pins}

    return render_template("led_control.html", **template)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out!")
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 5000, debug = True)
