from datetime import datetime
from extensions import db
import json

class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    source = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.String(20), nullable=False)
    end_date = db.Column(db.String(20), nullable=False)
    budget = db.Column(db.String(50), nullable=False)
    interests = db.Column(db.String(255), nullable=True)
    itinerary = db.Column(db.Text, nullable=True) # Stored as JSON string
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_saved = db.Column(db.Boolean, default=False)

    def set_itinerary(self, itinerary_dict):
        self.itinerary = json.dumps(itinerary_dict)

    def get_itinerary(self):
        if self.itinerary:
            return json.loads(self.itinerary)
        return None

    def __repr__(self):
        return f"Trip('{self.source}' to '{self.destination}')"
