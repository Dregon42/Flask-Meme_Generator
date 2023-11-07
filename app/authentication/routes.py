from forms import UserLoginForm, UserSignupForm
from models import User, db
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, LoginManager, current_user, login_required

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = UserSignupForm()

    if request.method == 'POST' and form.validate_on_submit():
        first = form.first.data
        last = form.last.data
        email = form.email.data
        password = form.password.data

        user = User(first, last, email, password)

        db.session.add(user)
        db.session.commit()

        flash(f'You have successfully created a user account {email}', 'User-created')
        return redirect(url_for('site.home'))
    else:
        flash(f'Error creating user account. Please check your form and try again.', 'auth-failed')

    return render_template('signup.html', form=form)


@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    form = UserLoginForm()
    
    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data.lower()
            password = form.password.data
            print(email, password)
            logged_user = db.session.execute(db.select(User).where(User.email == email)).scalar()
            # logged_user = User.query.filter_by(email = email).first()
            print(logged_user)
            if logged_user is not None and logged_user.check_hash_password(logged_user.password, password):
                login_user(logged_user)
                flash('You were successful in your initiation. Congratulations, and welcome!', 'auth-sucess')
                return redirect(url_for('site.profile'))
            else:
                flash('You have failed in your attempt to access this content.', 'auth-failed')
                return redirect(url_for('auth.signin'))
    except:
        raise Exception('Invalid Form Data: Please Check your Form')
    return render_template('signin.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('site.home'))