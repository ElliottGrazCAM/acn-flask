from flask import Flask, render_template, redirect, url_for, flash, request, session
from models.user import db, User
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('profile'))
        else:
            error = "Invalid credentials."
    return render_template('login.html', error=error)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

# Admin Blueprint for separation (short version in main file for demo)
from flask import Blueprint

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
@login_required
def dashboard():
    if not current_user.is_admin:
        return redirect(url_for('index'))
    return render_template('admin/dashboard.html')

@admin_bp.route('/members')
@login_required
def members():
    if not current_user.is_admin:
        return redirect(url_for('index'))
    members = User.query.all()
    return render_template('admin/members.html', members=members)

app.register_blueprint(admin_bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
