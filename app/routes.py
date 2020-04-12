from flask import render_template, request, redirect, url_for, flash

from app import app, db
from app.forms import LoginForm, RegistrationForm, EventAddForm, EventEditForm

from flask_login import current_user, login_user, logout_user,  login_required
from app.models import User, Event
from werkzeug.urls import url_parse


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    # Главная cтраница
    events = Event.query.all()
    return render_template('index.html', title='Home', events=events)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/testlogining')
@login_required
def testlogining():
    return render_template('testlogining.html', title='testlogining')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    user_events = user.events.all()
    return render_template('user.html', user=user, events=user_events)


@app.route('/eventadd', methods=['GET', 'POST'])
@login_required
def event_add():
    form = EventAddForm()
    user_id = current_user.get_id()
    user = User.query.get(user_id)
    if form.validate_on_submit():
        event_for_add = Event(
            title = form.title.data,
            body = form.body.data,
            start = form.start.data,
            end = form.end.data,
            author = user
        )
        db.session.add(event_for_add)
        db.session.commit()
        flash('Событие добавленно')
        return redirect(url_for('index'))
    return render_template('eventadd.html', title='Event add', form=form, user=user)


@app.route('/delete/<username>/<event_id>')
@login_required
def event_dlt(username, event_id):
    current_user_id = current_user.get_id()
    user_from_context = User.query.filter_by(username=username).first_or_404()
    if int(current_user_id) == user_from_context.id:
        even_to_del = user_from_context.events.filter_by(id=int(event_id)).first()
        db.session.delete(even_to_del)
        flash('Задача {} удалена успешно'.format(even_to_del.title))
        db.session.commit()
        return redirect(url_for('index'))
    else:
        flash('Отказано в доступе')
        flash('Вы можете удалять только свои задачи')
    return redirect(url_for('user', username=User.query.get(int(current_user_id)).username))


@app.route('/edit_event/<event_id>', methods=['GET', 'POST'])
@login_required
def event_edit(event_id):
    editing_event = Event.query.get(event_id)
    try:
        event_user_id = editing_event.user_id
    except:
        flash('Задача не найдена')
        return redirect(url_for('user', username=User.query.get(int(current_user.get_id())).username))

    if int(current_user.get_id()) == editing_event.user_id:
        form = EventEditForm(obj=editing_event)
        if form.validate_on_submit():
            form.populate_obj(editing_event)
            db.session.commit()
            flash('Событие обновлено')
            return redirect(url_for('user', username=User.query.get(int(current_user.get_id())).username))

        return render_template('event.html', title='Edit {}'.format(editing_event.title), editing_event=editing_event, form=form)
    
    else:
        flash('Отказано в доступе')
        flash('Вы можете редактировать только свои задачи')
        return redirect(url_for('user', username=User.query.get(int(current_user.get_id())).username))


