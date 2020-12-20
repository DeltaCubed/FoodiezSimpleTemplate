""" 
TODO:
Create a many-to-many relationship between friends, restaurants and user
build UI
 """
from flask import Flask, redirect, url_for, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required,logout_user, current_user
from User_Pages import User_Pages

app = Flask(__name__)
app.register_blueprint(User_Pages, url_prefix="")

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///login.db'
app.config['SECRET_KEY']= 'this is secret UWU'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"

# TODO Create 2 tables, 1 for Friends and 1 for Restaurants
# Link between User and Friend
friends = db.Table(
    'friends',  
    db.Column('id', db.Integer, db.ForeignKey('user.id')),
    db.Column('fri_id', db.Integer, db.ForeignKey('friend.fri_id')),
)

# Link between User and restaurants
restaurants = db.Table(
    'restaurants',
    db.Column('id', db.Integer, db.ForeignKey('user.id')),
    db.Column('res_id', db.Integer, db.ForeignKey('restaurant.res_id'))
)

# Link between Friends and restaurants
f_restaurants = db.Table(
    'f_restaurants',
    db.Column('fri_id', db.Integer, db.ForeignKey('friend.fri_id')),
    db.Column('res_id', db.Integer, db.ForeignKey('restaurant.res_id'))
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    # TODO Connect both Restaurant and Friend database
    Urestaurant = db.relationship('Restaurant', secondary=restaurants, backref=db.backref('Liked_Restaurants'), lazy='dynamic')
    Ufriends = db.relationship('Friend', secondary=friends, backref=db.backref('Your_Friends'), lazy='dynamic')

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

class Restaurant(db.Model):
    res_id = db.Column(db.Integer, primary_key=True)  # Prime key
    res_name = db.Column(db.String(30))  # Name of restaurant
    res_des = db.Column(db.String(300))  # Restaurant Description
    res_score = db.Column(db.Integer)  # The rank of the restaurant

class Friend(db.Model):
    fri_id = db.Column(db.Integer, primary_key=True)  # Prime key
    fri_name = db.Column(db.String(30))
    # TODO Create a way to pull restaurant ranking info
    # Frestaurant = db.relationship('f_restaurants', secondary=f_restaurants, backref=db.backref('Their_restaurants'), lazy='dynamic')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def frontPage():
    return render_template("frontpage.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('User_Pages.user'))
    if request.method == 'POST':
        # TODO add signin functionality
        _user = request.form['uname']
        _password = request.form["pwd"]
        _found_user = User.query.filter_by(username=_user, password=_password).first()
        if _found_user:
            login_user(_found_user)
        else:
            flash("Incorrect Username or Password")
            return redirect(url_for('login'))
        # flash("Log in was successful!")
        return redirect(url_for('User_Pages.user'))
    else:
        return render_template('login.html')
    
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('User_Pages.user'))
    if request.method == "POST":
        _user = request.form['uname']
        if request.form['pwd'] != request.form['pwd2']:
            flash('The password does not match')
            return redirect(url_for("signup"))
        else:
            _password = request.form['pwd']
        _email = request.form['email']
        taken_login = User.query.filter_by(username=_user, email=_email).first()
        if taken_login:
            flash("Username and/or email are taken")
            return redirect(url_for('signup'))
        else:
            new_user = User(_user, _password, _email)
            db.session.add(new_user)
            db.session.commit()
        created_user = User.query.filter_by(username=_user, email=_email).first()
        login_user(created_user)
        return redirect(url_for('User_Pages.user'))
    else:
        return render_template('signup.html')


@app.route('/people')
@login_required
def people():
    _people = User.query.order_by(User.id).all()
    _curr_friends = []
    for friend in current_user.Ufriends:
        _curr_friends.append(friend.fri_name)
    
    return render_template(
        'inner/people.html', 
        people=_people, 
        curr_friends=_curr_friends, 
        cur_name=current_user.username
    )


@app.route("/add/<user>")
@login_required
def add(user):
    # TODO Make a confirm friend request
    # TODO Fix duplication assignment
    new_friend = Friend(fri_name=user)
    current_user.Ufriends.append(new_friend)
    db.session.commit()
    other_user = User.query.filter_by(username=user).first()
    next_friend = Friend(fri_name=current_user.username)
    other_user.Ufriends.append(next_friend)
    db.session.commit()
    return redirect(url_for('User_Pages.friends'))
    

@app.route('/remove/<user>')
@login_required
def remove(user):
    # TODO Make a remove user remember it needs to remove on both sides
    # TODO Work on deleting on the other end
    Friend.query.filter_by(fri_name=user).delete()
    db.session.commit()
    return redirect(url_for('User_Pages.friends'))

@app.route('/restaurants')
@login_required
def restaurants():
    # TODO Connect with Geolocation API and Yelp API
    # TODO Create a ranking algorithm for individual
    # TODO Build tinder html interface
    ...


if __name__ == '__main__':
    app.run(debug=True, ssl_context="adhoc")