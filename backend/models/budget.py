from extensions import db

class Budget(db.Model):
    __tablename__ = 'budgets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)

    # Define the relationship to Expense
    # expenses = db.relationship('Expense', backref='budget', lazy=True)

    def __repr__(self):
        return f"<Budget(name={self.name}, amount={self.amount})>"
