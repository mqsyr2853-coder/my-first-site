from flask import Flask, render_template, url_for, flash, redirect, request
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from models import db, User, Post # استيراد من ملف models.py

app = Flask(__name__)

# --- الإعدادات ---
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245' # مفتاح أمان
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///minigram.db'

# --- ربط قاعدة البيانات ونظام الدخول ---
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login' # يرجع لصفحة اللوجن لو حاول يدخل وهو مش مسجل

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# إنشاء الجداول لأول مرة
with app.app_context():
    db.create_all()

# --- المسارات (Routes) ---

@app.route("/")
@app.route("/login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route("/signup")
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    return render_template('signup.html')

@app.route("/signup_process", methods=['POST'])
def signup_process():
    user_name = request.form.get('username')
    user_pass = request.form.get('password')
    
    user = User.query.filter_by(username=user_name).first()
    if user:
        return "Username exists! <a href='/signup'>Try again</a>"
    
    new_user = User(username=user_name, password=user_pass)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('login'))

@app.route("/login_process", methods=['POST'])
def login_process():
    user_name = request.form.get('username')
    user_pass = request.form.get('password')
    
    user = User.query.filter_by(username=user_name, password=user_pass).first()
    if user:
        login_user(user)
        return redirect(url_for('home'))
    else:
        return "Login Failed! <a href='/'>Try again</a>"

@app.route("/home")
@login_required
def home():
    return render_template('index.html', title='Feed')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)