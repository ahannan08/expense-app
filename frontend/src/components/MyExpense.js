import React, { useState, useEffect } from 'react';
import api from '../api/client';
import Layout from './Layout';
import './styles/shared.css';
import './styles/MyExpense.css';

const MyExpense = () => {
  const [amount, setAmount] = useState('');
  const [category, setCategory] = useState('');
  const [toast, setToast] = useState(null);
  const [predictedExpenses, setPredictedExpenses] = useState({
    total_expense: 0,
    category_expenses: { food: 0, entertainment: 0 },
    budgetStatus: '',
  });

  useEffect(() => {
    const fetchPrediction = async () => {
      const currentMonth = new Date().getMonth() + 1;
      const currentYear = new Date().getFullYear();

      try {
        const response = await api.get('/api/predictions/get-prediction', {
          params: { month: currentMonth, year: currentYear },
        });

        if (response.data && response.data.total_expense !== undefined) {
          const cats = response.data.category_expenses || {};
          setPredictedExpenses({
            total_expense: response.data.total_expense || 0,
            category_expenses: {
              food: cats.Food || 0,
              entertainment: cats.Entertainment || 0,
            },
            budgetStatus: response.data.budget_status || 'No Prediction',
          });
        }
      } catch {
        setPredictedExpenses({
          total_expense: 0,
          category_expenses: { food: 0, entertainment: 0 },
          budgetStatus: 'No prediction for this month',
        });
      }
    };

    fetchPrediction();
  }, []);

  const categories = [
    'Food', 'Sports', 'Shopping', 'Travel', 'Misc', 'Snacks', 'Petrol', 'Gym', 'Entertainment',
  ];

  const showToast = (message) => {
    setToast(message);
    setTimeout(() => setToast(null), 3000);
  };

  const handlePostExpense = async (event) => {
    event.preventDefault();

    const expenseData = {
      amount: parseFloat(amount),
      category,
      month: new Date().getMonth() + 1,
      year: new Date().getFullYear(),
    };

    try {
      await api.post('/api/expenses', expenseData);
      showToast('Expense recorded successfully');
      setAmount('');
      setCategory('');
    } catch (error) {
      console.error('Error posting expense:', error);
      showToast('Error recording expense');
    }
  };

  const monthNames = [
    'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
    'September', 'October', 'November', 'December',
  ];
  const currentMonthName = monthNames[new Date().getMonth()];

  const statusClass =
    predictedExpenses.budgetStatus === 'Over Budget'
      ? 'status-over'
      : predictedExpenses.budgetStatus === 'Under Budget'
        ? 'status-under'
        : '';

  return (
    <Layout title="Log expense" subtitle={`Record spending for ${currentMonthName}`}>
      {toast && <div className="toast" role="status">{toast}</div>}

      <div className="log-expense-grid">
        <section className="card predicted-expenses">
          <h2 className="card-title">Prediction snapshot — {currentMonthName}</h2>
          <ul className="prediction-categories">
            {Object.entries(predictedExpenses.category_expenses).map(([cat, expense]) => (
              <li key={cat}>
                <span>{cat.charAt(0).toUpperCase() + cat.slice(1)}</span>
                <span>Rs {Number(expense).toFixed(2)}</span>
              </li>
            ))}
          </ul>
          <p className="total-line">
            Total: <strong>Rs {predictedExpenses.total_expense.toFixed(2)}</strong>
          </p>
          <p className={`status-line ${statusClass}`}>Status: {predictedExpenses.budgetStatus}</p>
        </section>

        <section className="card expense-form">
          <h2 className="card-title">New expense</h2>
          <form onSubmit={handlePostExpense}>
            <div className="form-group">
              <label htmlFor="amount">Amount (Rs)</label>
              <input
                id="amount"
                type="number"
                min="0"
                step="0.01"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
                required
              />
            </div>

            <div className="form-group">
              <label>Category</label>
              <div className="category-grid">
                {categories.map((cat) => (
                  <label key={cat} className={`category-pill${category === cat ? ' selected' : ''}`}>
                    <input
                      type="radio"
                      name="category"
                      value={cat}
                      onChange={() => setCategory(cat)}
                      checked={category === cat}
                    />
                    {cat}
                  </label>
                ))}
              </div>
            </div>

            <button type="submit" className="btn btn-primary">Post expense</button>
          </form>
        </section>
      </div>
    </Layout>
  );
};

export default MyExpense;
