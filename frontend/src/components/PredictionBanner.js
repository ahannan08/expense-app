import React from 'react';
import { Link } from 'react-router-dom';
import './styles/PredictionBanner.css';

function PredictionBanner() {
  return (
    <aside className="prediction-banner" aria-labelledby="prediction-banner-title">
      <div className="prediction-banner-content">
        <p className="prediction-banner-eyebrow">How it works</p>
        <h2 id="prediction-banner-title" className="prediction-banner-title">
          Smart expense forecasting
        </h2>
        <p className="prediction-banner-lead">
          We estimate your monthly spending across nine categories using machine learning
          models trained on historical expense patterns—not a single guess, but one
          tailored forecast per category.
        </p>
        <ol className="prediction-banner-steps">
          <li>
            <strong>You share context</strong> — monthly budget, target month, and lifestyle
            signals (food and entertainment levels).
          </li>
          <li>
            <strong>Models run per category</strong> — separate regressors predict Food,
            Travel, Petrol, Gym, and the rest from those inputs.
          </li>
          <li>
            <strong>We sum and compare</strong> — predicted totals are stacked and checked
            against your budget so you see under or over before you spend.
          </li>
        </ol>
        <Link to="/prediction" className="btn btn-primary prediction-banner-cta">
          Try a prediction
        </Link>
      </div>
      <div className="prediction-banner-visual" aria-hidden="true">
        <div className="prediction-flow">
          <span className="flow-node">Budget &amp; habits</span>
          <span className="flow-arrow">→</span>
          <span className="flow-node flow-node-accent">9 category models</span>
          <span className="flow-arrow">→</span>
          <span className="flow-node">Forecast &amp; status</span>
        </div>
      </div>
    </aside>
  );
}

export default PredictionBanner;
