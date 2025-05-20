from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False
    
    def get_id(self):
        return str(self.id)
    
    @staticmethod
    def get(user_id):
        users = {
            "1": User("1", "admin", generate_password_hash("admin123")),
            "2": User("2", "doctor", generate_password_hash("doctor123"))
        }
        return users.get(user_id)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = None
        for u in User.get_all_users():
            if u.username == username:
                user = u
                break
        
        if not user or not check_password_hash(user.password, password):
            flash('Invalid username or password', 'error')
            return redirect(url_for('auth.login'))
        
        login_user(user)
        return redirect(url_for('dashboard.index'))
    
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

def get_all_users():
    return [
        User("1", "admin", generate_password_hash("admin123")),
        User("2", "doctor", generate_password_hash("doctor123"))
    ]

User.get_all_users = staticmethod(get_all_users)