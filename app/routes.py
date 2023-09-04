from datetime import datetime
from datetime import date, timedelta
from flask import render_template, redirect, url_for, request, flash
from app.forms import LoginForm, ChildForm, PostForm, RegistrationForm, EmptyForm, EditProfileForm, EditChildForm, DeleteChildForm, AddActivityForm, AssignGroupForm
from app import app, db
from app.models import User
from app.models import Child, Activity
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
# @login_required
def index():
    form = PostForm()
    return render_template('index.html', title='Home', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
         return redirect(url_for('user', username=current_user.username))
    form = LoginForm()
    if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user is None or not user.check_password(form.password.data):
                flash('Ungültiger Benutzername oder Passwort')
                return redirect(url_for('login'))
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
               next_page = url_for('user', username=current_user.username)
            return redirect(next_page)
    return render_template('login.html', title='Anmelden', form=form)

@app.route('/all_users', methods=['GET', 'POST'])
def all_users():
    all_users = User.query.all()

    group_forms = {}
    for user in all_users:
        form = AssignGroupForm(prefix=str(user.id))
        group_forms[user.id] = form

        if form.validate_on_submit() and form.user_id.data == str(user.id):
            print("Form submitted:", form.validate_on_submit())
            print("User ID:", form.user_id.data)
            print("Current User ID:", user.id)
            user_to_update = User.query.get(int(form.user_id.data))
            user_to_update.group = form.new_group.data
            user.group = form.new_group.data
            db.session.commit()
            flash(f"Gruppenzugehörigkeit von {user_to_update.username} wurde aktualisiert.", "success")
            return redirect(url_for('all_users'))
        else:             
            print("Form submitted:", form.validate_on_submit())
            print("User ID:", form.user_id.data)
            print("Current User ID:", user.id)
            print("Updating user group to:", form.new_group.data)
        if form.is_submitted():
            print("Form errors:", form.errors)

    return render_template('all_users.html', users=all_users, group_forms=group_forms)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/children')
def children():
    children = Child.query.all()
    return render_template('children.html', children=children)
   

@app.route('/add_child', methods=['GET', 'POST'])
def add_child():
    form = ChildForm()
    if form.validate_on_submit():
        child = Child(first_name=form.first_name.data, last_name=form.last_name.data, age=form.age.data, group=form.group.data)
        db.session.add(child)
        db.session.commit()
        flash('Kind erfolgreich hinzugefügt!')
        return redirect(url_for('add_child'))
    return render_template('add_child.html', form=form)

@app.route('/edit_child/<int:child_id>', methods=['GET', 'POST'])
def edit_child(child_id):
    child = Child.query.get(child_id)
    form = EditChildForm(obj=child)

    if form.validate_on_submit():
        child.first_name = form.first_name.data
        child.last_name = form.last_name.data
        child.age = form.age.data
        child.group = form.group.data

        db.session.commit()
        flash('Kind erfolgreich Bearbeitet!')
        return redirect(url_for('edit_child', child_id=child.id))

    elif request.method == 'GET':
        form.first_name.data = child.first_name
        form.last_name.data = child.last_name
        form.age.data = child.age
        form.group.data = child.group

    return render_template('edit_child.html', form=form, child=child)


@app.route('/delete_child/<int:child_id>', methods=['GET', 'POST'])
def delete_child(child_id):
    child = Child.query.get(child_id)
    if not child:
        flash("Kind nicht gefunden!")
        return redirect(url_for("index"))

    form = DeleteChildForm()
    
    if request.method == "POST":
        if form.validate_on_submit():
            db.session.delete(child)
            db.session.commit()
            flash("Kind erfolgreich gelöscht!")
            return redirect(url_for("children"))
        else:
            flash("Es gab ein Problem beim Löschen des Kindes.")
            return redirect(url_for("index"))
    else:
        return render_template("delete_child.html", form=form, child=child)

@app.route('/perform_activity/<int:child_id>')
def perform_activity(child_id):
    child = Child.query.get(child_id)
    db.session.commit()
    flash('Aktivität durchgeführt!')
    return redirect(url_for('children'))

@app.route('/child_details/<int:child_id>')
def child_details(child_id):
    child = Child.query.get_or_404(child_id)
    return render_template('child_details.html', child=child)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, group=form.group.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Benutzer wurde erfasst!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)


@app.route('/user/<username>')
# @login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = EmptyForm()
    return render_template('user.html', user=user, form=form)


@app.route('/edit_profile', methods=['GET', 'POST'])
# @login_required
def edit_profile():
    form = EditProfileForm(current_user.username) 
    if form.validate_on_submit():
        current_user.username = form.username.data
    if form.validate_on_submit():
            if user is None or not user.check_password(form.password.data):
                flash('Ungültiger Benutzername oder Passwort')
            db.session.commit()
            flash('Your changes have been saved.')
            return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)

@app.route('/add_activity/<int:child_id>', methods=['GET', 'POST'])
@login_required
def add_activity(child_id):
    form = AddActivityForm()
    child = Child.query.get(child_id)
    if request.method == 'POST':
        print("Form is a POST request")

        if form.sleep_end_button.data:
            last_sleep_start = Activity.query.filter_by(
                child_id=child.id, 
                activity_type="sleep", 
                sleep_end=None
            ).order_by(Activity.timestamp.desc()).first()

            if last_sleep_start:
                last_sleep_start.sleep_end = datetime.utcnow()
                db.session.commit()
                flash('Kind ist aufgewacht!', 'success')
                flash('Aktivität erfolgreich hinzugefügt!', 'success')
                return redirect(url_for('add_activity', child_id=child.id))
            else:
                flash('Kind ist noch nicht eingeschlafen!', 'error')
                return redirect(url_for('add_activity', child_id=child.id))
        else:
            if form.sleep_start_button.data:
                existing_sleep_start = Activity.query.filter_by(
                    child_id=child.id, 
                    activity_type="sleep", 
                    sleep_end=None
                ).order_by(Activity.timestamp.desc()).first()
                if existing_sleep_start:
                    flash('Kind schläft schon!', 'error')
                    return redirect(url_for('add_activity', child_id=child.id))

            activity = Activity(child_id=child.id)

            if form.food_choices.data == 'Andere':
                activity.activity_type = "food"
                activity.food = form.other_food.data
                activity.description = "Essen"
            elif form.food_choices.data in ['Apfel', 'Birne']:
                activity.activity_type = "food"
                activity.food = form.food_choices.data
                activity.description = "Essen"
            
            if form.sleep_start_button.data:
                activity.activity_type = "sleep"
                activity.description = "Schlaf gestartet"
                activity.sleep_start = datetime.utcnow()
                flash('Kind ist eingeschlafen!', 'success')

            if form.change_type.data:
                activity.activity_type = "diaper"
                change_type = form.change_type.data
                if change_type == 'gross':
                    activity.description = "Windel gewechselt - groß"
                    activity.diaper_change_large = datetime.utcnow()
                elif change_type == 'klein':
                    activity.description = "Windel gewechselt - klein"
                    activity.diaper_change_small = datetime.utcnow()

            db.session.add(activity)
            db.session.commit()
            print("Data committed to the database")
            flash('Aktivität erfolgreich hinzugefügt!', 'success')
            return redirect(url_for('add_activity', child_id=child.id))

    if request.method == 'GET':
        latest_activity = Activity.query.filter_by(child_id=child.id).order_by(Activity.timestamp.desc()).first()
        if latest_activity:
            if latest_activity.food in ['Apfel', 'Birne']:
                form.food_choices.data = latest_activity.food
            else:
                form.food_choices.data = 'andere'
                form.other_food.data = latest_activity.food

    return render_template('add_activity.html', form=form, child=child)

@app.route('/day_review/<int:child_id>', methods=['GET'])
@login_required
def day_review(child_id):
    child = Child.query.get_or_404(child_id)
    activities = Activity.query.filter_by(child_id=child.id).all()
    print(activities)
    return render_template('day_review.html', child=child, activities=activities)

@app.route('/group_children/<group_name>', methods=['GET'])
@login_required
def group_children(group_name):
    if group_name not in ['A', 'B', 'C']:
        flash('Ungültige Gruppenbezeichnung')
        return redirect(url_for('all_users'))
    
    children = Child.query.filter_by(group=group_name).all()
    return render_template('group_children.html', children=children, group_name=group_name)

@app.route('/update_user_group', methods=['POST'])
@login_required
def update_user_group():
    form = AssignGroupForm()
    if form.validate_on_submit():
        user = User.query.get(form.user_id.data)
        user.group = form.new_group.data
        db.session.commit()
        flash('Die Gruppe des Benutzers wurde aktualisiert.')
    return redirect(url_for('all_users'))


