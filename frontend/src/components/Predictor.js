import React, { useState, useEffect, useCallback } from 'react';
import api from '../api/client';
import Layout from './Layout';
import ManagePrediction from './ManagePrediction';
import './styles/shared.css';
import './styles/Predictor.css';

const Predictor = () => {
  const [budget, setBudget] = useState('');
  const [foodLevel, setFoodLevel] = useState('High');
  const [entertainmentLevel, setEntertainmentLevel] = useState('Low');
  const [month, setMonth] = useState(new Date().getMonth() + 1);
  const [year, setYear] = useState(new Date().getFullYear());
  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState(null);
  const [predictionExists, setPredictionExists] = useState(false);

  const checkIfPredictionExists = useCallback(async () => {
    try {
      const response = await api.get('/api/predictions/get-prediction', {
        params: { month, year },
      });
      setPredictionExists(response.status === 200 && response.data?.month != null);
    } catch {
      setPredictionExists(false);
    }
  }, [month, year]);

  useEffect(() => {
    checkIfPredictionExists();
  }, [checkIfPredictionExists]);

  const handleSubmit = async (event) => {
    event.preventDefault();

    const payload = {
      budget: parseInt(budget, 10),
      month: parseInt(month, 10),
      food_level: foodLevel,
      entertainment_level: entertainmentLevel,
    };

    try {
      const response = await api.post('/api/predict-category', payload);
      const { total_expense, category_expenses } = response.data;
      setPrediction({
        totalExpense: total_expense,
        categoryExpenses: category_expenses,
      });
      setError(null);
      checkIfPredictionExists();
    } catch {
      setError('An error occurred while fetching the prediction.');
      setPrediction(null);
    }
  };

  const budgetStatus =
    prediction && budget
      ? prediction.totalExpense > parseFloat(budget)
        ? 'Over Budget'
        : 'Under Budget'
      : '';

  return (
    <Layout title="Expense prediction" subtitle="ML forecast by category for your budget">
      {error && <div className="error-banner">{error}</div>}

      <div className="predictor-grid">
        <section className="card">
          <h2 className="card-title">Your inputs</h2>
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="budget">Monthly budget (Rs)</label>
              <input
                id="budget"
                type="number"
                min="1"
                value={budget}
                onChange={(e) => setBudget(e.target.value)}
                placeholder="Enter budget"
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="food-level">Food level</label>
              <select
                id="food-level"
                value={foodLevel}
                onChange={(e) => setFoodLevel(e.target.value)}
                required
              >
                <option value="Low">Low</option>
                <option value="Medium">Medium</option>
                <option value="High">High</option>
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="entertainment-level">Entertainment level</label>
              <select
                id="entertainment-level"
                value={entertainmentLevel}
                onChange={(e) => setEntertainmentLevel(e.target.value)}
                required
              >
                <option value="Low">Low</option>
                <option value="High">High</option>
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="pred-month">Month</label>
              <select
                id="pred-month"
                value={month}
                onChange={(e) => setMonth(Number(e.target.value))}
                required
              >
                {Array.from({ length: 12 }, (_, i) => (
                  <option key={i + 1} value={i + 1}>
                    {new Date(0, i).toLocaleString('en', { month: 'long' })}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="pred-year">Year</label>
              <input
                id="pred-year"
                type="number"
                value={year}
                onChange={(e) => setYear(Number(e.target.value))}
                required
              />
            </div>

            <button type="submit" className="btn btn-primary">Get prediction</button>
          </form>
        </section>

        {prediction && (
          <section className="card prediction-results">
            <h2 className="card-title">Forecast</h2>
            <ul className="forecast-list">
              {Object.entries(prediction.categoryExpenses).map(([category, expense]) => (
                <li key={category}>
                  <span>{category}</span>
                  <span>Rs {Number(expense).toFixed(2)}</span>
                </li>
              ))}
            </ul>
            <p className="forecast-total">
              Total: <strong>Rs {prediction.totalExpense.toFixed(2)}</strong>
            </p>
            <p
              className={`forecast-status ${
                budgetStatus === 'Over Budget' ? 'status-over' : 'status-under'
              }`}
            >
              Status: {budgetStatus}
            </p>
            <ManagePrediction
              prediction={prediction}
              budget={budget}
              month={month}
              year={year}
              predictionExists={predictionExists}
              onSaved={checkIfPredictionExists}
            />
          </section>
        )}
      </div>
    </Layout>
  );
};

export default Predictor;
