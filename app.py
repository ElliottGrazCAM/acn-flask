from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'this-should-be-a-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///members.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120))
    password = db.Column(db.String(200), nullable=False)
    membership_level = db.Column(db.String(40), default="Basic")
    is_admin = db.Column(db.Boolean, default=False)

    def get_id(self):
        return str(self.id)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def home():
    return "Welcome to the ACN Members Backend! Go to /register or /login."

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        password = request.form['password']
        if User.query.filter_by(email=email).first():
            return "Email already registered."
        user = User(email=email, name=name, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return '''
        <form method="post">
            Name: <input name="name"><br>
            Email: <input name="email"><br>
            Password: <input name="password" type="password"><br>
            <button type="submit">Register</button>
        </form>
    '''

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('profile'))
        else:
            return "Login failed."
    return '''
        <form method="post">
            Email: <input name="email"><br>
            Password: <input name="password" type="password"><br>
            <button type="submit">Login</button>
        </form>
    '''

@app.route('/profile')
@login_required
def profile():
    return f'''
        <h2>Welcome, {current_user.name}!</h2>
        <p>Email: {current_user.email}</p>
        <p>Membership level: {current_user.membership_level}</p>
        <a href="/logout">Logout</a>
    '''

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Create database if it doesn't exist
@app.before_request
def create_tables_once():
    if not hasattr(app, 'db_created'):
        db.create_all()
        app.db_created = True

if __name__ == '__main__':
    app.run(debug=True)
