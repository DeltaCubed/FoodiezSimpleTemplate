from flask import Blueprint, redirect, url_for, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required,logout_user, current_user

User_Pages = Blueprint("User_Pages", __name__, static_folder='static', template_folder="templates")

@User_Pages.route('/user')
@login_required
def user():
    return render_template('inner/profile.html', user=current_user)

@User_Pages.route("/friends")
@login_required
def friends():
    # TODO Make a list of your friends
    # Query the current user's name into an actual list, then pushes the list into html
    _temp = []
    for friend in current_user.Ufriends:
        _temp.append(friend.fri_name)
    return render_template('inner/friends.html', friends=_temp)


@User_Pages.route("/view/<user>")
@login_required
def view(user):
    # TODO Create a nice page to view, add and report a user
    return "This will show the user's profile!"


@User_Pages.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out successfully!")
    return redirect(url_for('login'))