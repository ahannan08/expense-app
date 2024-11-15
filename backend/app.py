from flask import Flask
from extensions import db
from flask_migrate import Migrate
from config.config import SQLALCHEMY_DATABASE_URI
from routes.catPredictRoute import category_bp  # Import the category route
from routes.expenseRoutes import expense_bp
from models.expense import Expense
from routes.predictionDb import predictions_bp
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will allow all origins by default

# Setup configuration
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize DB and Migrate
db.init_app(app)
migrate = Migrate(app, db)

# Register blueprints
app.register_blueprint(expense_bp, url_prefix="/api")
# app.register_blueprint(category_bp, url_prefix='/api')
app.register_blueprint(predictions_bp, url_prefix='/api/predictions')

# Test route to confirm app is working
@app.route('/')
def hello_world():
    return "Flask app is up and running!"

if __name__ == "__main__":
    # If you don't want to run create_all, remove this part
    with app.app_context():
        db.create_all()

    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
