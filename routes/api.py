from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models.trip import Trip
from extensions import db
import os
import json

api_bp = Blueprint('api', __name__)

# Stub for AI service
def generate_ai_itinerary(data):
    # This will be replaced with actual Gemini API call
    source = data.get('source')
    destination = data.get('destination')
    days = 3 # calculate from dates
    
    # Mock itinerary format
    itinerary = []
    for i in range(1, days + 1):
        itinerary.append({
            "day": i,
            "title": f"Day {i} in {destination}",
            "activities": [
                {"time": "09:00 AM", "activity": "Breakfast at local cafe", "description": "Enjoy local cuisine to start your day."},
                {"time": "11:00 AM", "activity": f"Visit popular attraction in {destination}", "description": "Explore the most famous landmark."},
                {"time": "02:00 PM", "activity": "Lunch", "description": "Try the street food."},
                {"time": "04:00 PM", "activity": "Relax at park/beach", "description": "Unwind and enjoy the view."},
                {"time": "07:00 PM", "activity": "Dinner", "description": "Fine dining experience."}
            ]
        })
    
    return {
        "summary": f"A wonderful {days}-day trip from {source} to {destination}.",
        "budget_breakdown": {
            "flights/travel": "30%",
            "accommodation": "40%",
            "food": "20%",
            "activities": "10%"
        },
        "itinerary": itinerary
    }


@api_bp.route('/generate-itinerary', methods=['POST'])
@login_required
def generate_itinerary():
    data = request.json
    
    # In a real app, call AI here
    ai_response = generate_ai_itinerary(data)
    
    # Create trip in DB, not saved yet
    trip = Trip(
        user_id=current_user.id,
        source=data.get('source'),
        destination=data.get('destination'),
        start_date=data.get('start_date'),
        end_date=data.get('end_date'),
        budget=data.get('budget'),
        interests=data.get('interests'),
        is_saved=False
    )
    trip.set_itinerary(ai_response)
    db.session.add(trip)
    db.session.commit()
    
    return jsonify({
        "status": "success",
        "trip_id": trip.id,
        "data": ai_response
    })

@api_bp.route('/save-trip/<int:trip_id>', methods=['POST'])
@login_required
def save_trip(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    if trip.user_id != current_user.id:
        return jsonify({"status": "error", "message": "Unauthorized"}), 403
        
    trip.is_saved = True
    db.session.commit()
    return jsonify({"status": "success", "message": "Trip saved successfully!"})

@api_bp.route('/chat', methods=['POST'])
@login_required
def chat():
    data = request.json
    message = data.get('message')
    # Stub for AI chatbot
    reply = f"AI Assistant (Mock): You asked about '{message}'. In the future, I will connect to Gemini to give you a real answer!"
    return jsonify({"reply": reply})
