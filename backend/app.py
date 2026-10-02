import os

from flask import Flask, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from sqlalchemy import text

from config.config import FRONTEND_URL, SQLALCHEMY_DATABASE_URI
from extensions import db
from models.Prediction import Prediction  # noqa: F401 — register with metadata
from models.budget import Budget  # noqa: F401
from models.expense import Expense  # noqa: F401
from routes.catPredictRoute import category_bp
from routes.expenseRoutes import expense_bp
from routes.predictionDb import predictions_bp

app = Flask(__name__)

_frontend_origins = [FRONTEND_URL]
if os.environ.get("FLASK_ENV") == "development" or os.environ.get("CORS_PERMISSIVE") == "1":
    CORS(app)
else:
    CORS(app, origins=_frontend_origins, supports_credentials=True)

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(expense_bp, url_prefix="/api")
app.register_blueprint(category_bp, url_prefix="/api")
app.register_blueprint(predictions_bp, url_prefix="/api/predictions")


def init_db():
    with app.app_context():
        db.create_all()


init_db()


@app.route("/")
def hello_world():
    return "Flask app is up and running!"


@app.route("/api/health")
def health():
    db_status = "connected"
    try:
        db.session.execute(text("SELECT 1"))
    except Exception:
        db_status = "disconnected"
    status = "ok" if db_status == "connected" else "degraded"
    return jsonify({"status": status, "db": db_status})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
