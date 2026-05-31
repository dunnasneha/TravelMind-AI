from flask import Blueprint, render_template
from flask_login import current_user, login_required
from models.trip import Trip

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('index.html', title='Home')
    return render_template('index.html', title='Home')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    saved_trips = Trip.query.filter_by(user_id=current_user.id, is_saved=True).order_by(Trip.created_at.desc()).all()
    recent_trips = Trip.query.filter_by(user_id=current_user.id).order_by(Trip.created_at.desc()).limit(3).all()
    return render_template('dashboard.html', title='Dashboard', saved_trips=saved_trips, recent_trips=recent_trips)

@main_bp.route('/planner')
@login_required
def planner():
    return render_template('planner.html', title='AI Travel Planner')

@main_bp.route('/chatbot')
@login_required
def chatbot():
    return render_template('chatbot.html', title='AI Travel Chatbot')

@main_bp.route('/saved-trips')
@login_required
def saved_trips():
    trips = Trip.query.filter_by(user_id=current_user.id, is_saved=True).order_by(Trip.created_at.desc()).all()
    return render_template('saved_trips.html', title='Saved Trips', trips=trips)

@main_bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html', title='Profile')
