import React, { useState, useEffect } from 'react';
import api from '../api/client';
import Layout from './Layout';
import './styles/shared.css';

const MONTH_NAMES = [
  'January', 'February', 'March', 'April', 'May', 'June',
  'July', 'August', 'September', 'October', 'November', 'December',
];

const Gexpenses = () => {
  const [expenses, setExpenses] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchExpenses = async () => {
      try {
        const response = await api.get('/api/expenses');
        setExpenses(response.data);
      } catch (error) {
        console.error('Error fetching expenses:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchExpenses();
  }, []);

  return (
    <Layout title="All expenses" subtitle="Complete history of logged spending">
      <section className="card">
        {loading ? (
          <div className="loading-block">Loading expenses…</div>
        ) : expenses.length === 0 ? (
          <div className="empty-state">
            <p>No expenses recorded yet.</p>
          </div>
        ) : (
          <div className="table-wrap">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Category</th>
                  <th>Amount</th>
                  <th>Month</th>
                  <th>Year</th>
                </tr>
              </thead>
              <tbody>
                {expenses.map((expense) => (
                  <tr key={expense.id}>
                    <td>{expense.category}</td>
                    <td>Rs {Number(expense.amount).toFixed(2)}</td>
                    <td>{MONTH_NAMES[expense.month - 1] || expense.month}</td>
                    <td>{expense.year}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>
    </Layout>
  );
};

export default Gexpenses;
