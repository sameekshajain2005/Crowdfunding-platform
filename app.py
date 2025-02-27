from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy 
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crowdfunding.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    goal = db.Column(db.Float, nullable=False)
    raised = db.Column(db.Float, default=0)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@app.route('/')
def index():
    campaigns = Campaign.query.all()
    return render_template('index.html', campaigns=campaigns)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

@app.route('/create_campaign', methods=['GET', 'POST'])
def create_campaign():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        goal = float(request.form['goal'])
        campaign = Campaign(title=title, description=description, goal=goal, creator_id=session['user_id'])
        db.session.add(campaign)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create_campaign.html')

@app.route('/donate/<int:campaign_id>', methods=['POST'])
def donate(campaign_id):
    amount = float(request.form['amount'])
    campaign = Campaign.query.get(campaign_id)
    if campaign:
        campaign.raised += amount
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

admin = Admin(app)
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Campaign, db.session))

app = Flask(__name__, template_folder="path_to_templates")
app = Flask(__name__, template_folder="templates")

