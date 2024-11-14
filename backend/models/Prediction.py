from extensions import db

class Prediction(db.Model):
    __tablename__ = 'predictions'

    id = db.Column(db.Integer, primary_key=True)
    month = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    budget = db.Column(db.Integer, nullable=False)  # Added budget field
    food = db.Column(db.Float, nullable=False)
    entertainment = db.Column(db.Float, nullable=False)
    sports = db.Column(db.Float, nullable=False)
    shopping = db.Column(db.Float, nullable=False)
    travel = db.Column(db.Float, nullable=False)
    misc = db.Column(db.Float, nullable=False)
    snacks = db.Column(db.Float, nullable=False)
    petrol = db.Column(db.Float, nullable=False)
    gym = db.Column(db.Float, nullable=False)
    total_expense = db.Column(db.Float, nullable=False)
    budget_status = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Prediction(month={self.month}, year={self.year}, total_expense={self.total_expense})>"
