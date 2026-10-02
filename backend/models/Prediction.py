import datetime

from extensions import db

CATEGORY_FIELDS = (
    "food",
    "entertainment",
    "sports",
    "shopping",
    "gym",
    "petrol",
    "travel",
    "snacks",
    "misc",
)


class Prediction(db.Model):
    __tablename__ = "predictions"

    id = db.Column(db.Integer, primary_key=True)
    month = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    budget = db.Column(db.Integer, nullable=False)
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
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<Prediction(month={self.month}, year={self.year}, total_expense={self.total_expense})>"

    def category_expenses_dict(self):
        return {
            "Food": self.food,
            "Entertainment": self.entertainment,
            "Sports": self.sports,
            "Shopping": self.shopping,
            "Gym": self.gym,
            "Petrol": self.petrol,
            "Travel": self.travel,
            "Snacks": self.snacks,
            "Misc": self.misc,
        }

    def to_dict(self):
        created = self.created_at.isoformat() if self.created_at else None
        return {
            "id": self.id,
            "month": self.month,
            "year": self.year,
            "budget": self.budget,
            "total_expense": self.total_expense,
            "budget_status": self.budget_status,
            "category_expenses": self.category_expenses_dict(),
            "created_at": created,
        }
