from flask import Flask, render_template, url_for, flash, redirect
from flask_migrate import Migrate
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "abc"
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///site.db'

    db = SQLAlchemy(app)

    class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(20), unique=True, nullable=False)
        email = db.Column(db.String(120), unique=True, nullable=False)
        image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
        password = db.Column(db.String(60), nullable=False)
        posts = db.relationship('Post', backref='author', lazy=True)

        def __repr__(self):
            return f"User('{self.username}', '{self.email}', '{self.image_file}')"
        
    class Post(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(100), nullable=False)
        date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
        content = db.Column(db.Text, nullable=False)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

        
    # Create the database
    with app.app_context():
      db.create_all()     

    @app.route("/")
    def home():
        return render_template('index.html')

    @app.route("/register", methods=['GET', 'POST'])
    def register():
        form = RegistrationForm()
        if form.validate_on_submit():
            flash(f'Account created for {form.username.data}!', 'success')
            return redirect(url_for('home'))
        return render_template('register.html', title='Register', form=form)

    @app.route("/login", methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            if form.email.data == 'jai23@gmail.com' and form.password.data == '1234':
                flash('You have been logged in!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Login Unsuccessful. Please recheck your credentials', 'danger')
        return render_template('login.html', title='Login', form=form)
       

    return app

# App instance
app = create_app()


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
