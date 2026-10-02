import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../api/client';
import { DUMMY_DASHBOARD } from '../data/dummyDashboard';
import Layout from './Layout';
import PredictionBanner from './PredictionBanner';
import './styles/shared.css';
import './styles/Home.css';

const MONTH_NAMES = [
  'January', 'February', 'March', 'April', 'May', 'June',
  'July', 'August', 'September', 'October', 'November', 'December',
];

function formatMonthYear(month, year) {
  const name = MONTH_NAMES[month - 1] || month;
  return `${name} ${year}`;
}

function Home() {
  const [data, setData] = useState({ recent_expenses: [], recent_predictions: [] });
  const [loading, setLoading] = useState(true);
  const [usingSampleData, setUsingSampleData] = useState(false);

  useEffect(() => {
    const load = async () => {
      try {
        const response = await api.get('/api/dashboard');
        const expenses = response.data.recent_expenses || [];
        const predictions = response.data.recent_predictions || [];

        if (expenses.length === 0 && predictions.length === 0) {
          setData(DUMMY_DASHBOARD);
          setUsingSampleData(true);
        } else {
          setData(response.data);
          setUsingSampleData(false);
        }
      } catch (err) {
        console.error(err);
        setData(DUMMY_DASHBOARD);
        setUsingSampleData(true);
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  const { recent_expenses, recent_predictions } = data;

  return (
    <Layout
      title="Welcome back"
      subtitle="Your recent expenses and saved monthly predictions"
    >
      <PredictionBanner />

      {usingSampleData && (
        <p className="sample-data-notice" role="status">
          <span className="chip chip-sample">Sample data</span>
          Showing example history until your backend is connected and you log real activity.
        </p>
      )}

      <div className="home-actions">
        <Link to="/prediction" className="btn btn-primary">Run prediction</Link>
        <Link to="/log-expense" className="btn btn-secondary">Log an expense</Link>
      </div>

      {loading ? (
        <div className="loading-block">Loading history…</div>
      ) : (
        <div className="grid-2">
          <section className="card">
            <h2 className="card-title">Recent expenses</h2>
            {recent_expenses.length === 0 ? (
              <div className="empty-state">
                <p>No expenses logged yet.</p>
                <Link to="/log-expense" className="btn btn-primary">Log your first expense</Link>
              </div>
            ) : (
              <div className="table-wrap">
                <table className="data-table">
                  <thead>
                    <tr>
                      <th>Category</th>
                      <th>Amount</th>
                      <th>When</th>
                    </tr>
                  </thead>
                  <tbody>
                    {recent_expenses.map((exp) => (
                      <tr key={exp.id}>
                        <td>{exp.category}</td>
                        <td>Rs {Number(exp.amount).toFixed(2)}</td>
                        <td>{formatMonthYear(exp.month, exp.year)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
            {recent_expenses.length > 0 && (
              <Link to="/expenses" className="card-footer-link">View all expenses →</Link>
            )}
          </section>

          <section className="card">
            <h2 className="card-title">Saved predictions</h2>
            {recent_predictions.length === 0 ? (
              <div className="empty-state">
                <p>No predictions saved yet.</p>
                <Link to="/prediction" className="btn btn-primary">Create a prediction</Link>
              </div>
            ) : (
              <ul className="prediction-list">
                {recent_predictions.map((pred) => (
                  <li key={pred.id} className="prediction-item">
                    <div className="prediction-item-head">
                      <strong>{formatMonthYear(pred.month, pred.year)}</strong>
                      <span
                        className={`chip ${
                          pred.budget_status === 'Over Budget' ? 'chip-danger' : 'chip-success'
                        }`}
                      >
                        {pred.budget_status}
                      </span>
                    </div>
                    <div className="prediction-item-meta">
                      <span>Budget: Rs {Number(pred.budget).toLocaleString()}</span>
                      <span>Total: Rs {Number(pred.total_expense).toFixed(2)}</span>
                    </div>
                  </li>
                ))}
              </ul>
            )}
          </section>
        </div>
      )}
    </Layout>
  );
}

export default Home;
