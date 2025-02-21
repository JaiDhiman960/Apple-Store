
## view.py
from flask import render_template, request, redirect, session
from models import User, Contact
from app import app, db

@app.route('/')
def home():
    user = session.get('user')
    return render_template('index.html', username=user)




@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user'] = user.username
            return redirect('/')
        else:
            return render_template('login.html', error="Invalid credentials!")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            return render_template('register.html', error="Username already taken!")
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')


@app.route('/delete', methods=['POST'])
def delete_account():
    if 'user' not in session:
        return redirect('/login')

    user = User.query.filter_by(username=session['user']).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        session.pop('user', None)
        return redirect('/register')

    return redirect('/')