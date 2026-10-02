import React, { useState, useEffect } from 'react';
import api from '../api/client';
import Layout from './Layout';
import './styles/shared.css';
import './styles/Summary.css';

const EMPTY_CATEGORIES = {
  Food: 0,
  Sports: 0,
  Shopping: 0,
  Travel: 0,
  Misc: 0,
  Snacks: 0,
  Petrol: 0,
  Gym: 0,
  Entertainment: 0,
};

const Summary = () => {
  const [totalExpense, setTotalExpense] = useState(0);
  const [categoryExpenses, setCategoryExpenses] = useState(EMPTY_CATEGORIES);
  const [selectedMonth, setSelectedMonth] = useState(new Date().getMonth() + 1);
  const [selectedYear, setSelectedYear] = useState(new Date().getFullYear());
  const [isDataAvailable, setIsDataAvailable] = useState(true);

  useEffect(() => {
    const fetchMonthlyExpenses = async () => {
      try {
        const response = await api.get('/api/expenses/monthly-summary', {
          params: { month: selectedMonth, year: selectedYear },
        });

        const data = response.data;

        if (data && data.total_expense > 0) {
          setTotalExpense(data.total_expense);
          const updated = { ...EMPTY_CATEGORIES };
          Object.entries(data.category_expenses).forEach(([category, amount]) => {
            if (updated.hasOwnProperty(category)) {
              updated[category] = amount;
            }
          });
          setCategoryExpenses(updated);
          setIsDataAvailable(true);
        } else {
          setCategoryExpenses(EMPTY_CATEGORIES);
          setTotalExpense(0);
          setIsDataAvailable(false);
        }
      } catch (error) {
        console.error('Error fetching monthly expenses:', error);
        setIsDataAvailable(false);
      }
    };

    fetchMonthlyExpenses();
  }, [selectedMonth, selectedYear]);

  const periodLabel = new Date(selectedYear, selectedMonth - 1).toLocaleString('en', {
    month: 'long',
    year: 'numeric',
  });

  return (
    <Layout title="Monthly summary" subtitle="Spending breakdown by category">
      <section className="card">
        <div className="filter-container">
          <div className="form-group">
            <label htmlFor="summary-month">Month</label>
            <select
              id="summary-month"
              value={selectedMonth}
              onChange={(e) => setSelectedMonth(Number(e.target.value))}
            >
              {Array.from({ length: 12 }, (_, index) => (
                <option key={index} value={index + 1}>
                  {new Date(0, index).toLocaleString('en', { month: 'long' })}
                </option>
              ))}
            </select>
          </div>
          <div className="form-group">
            <label htmlFor="summary-year">Year</label>
            <input
              id="summary-year"
              type="number"
              value={selectedYear}
              onChange={(e) => setSelectedYear(Number(e.target.value))}
              min="2020"
            />
          </div>
        </div>

        {isDataAvailable ? (
          <div className="summary-content">
            <h2 className="card-title">Expenses for {periodLabel}</h2>
            <div className="category-list">
              {Object.entries(categoryExpenses).map(([category, expense]) => (
                <div key={category} className="category-item">
                  <span>{category}</span>
                  <span>Rs {expense.toFixed(2)}</span>
                </div>
              ))}
            </div>
            <div className="total-expense">
              <span>Total</span>
              <strong>Rs {totalExpense.toFixed(2)}</strong>
            </div>
          </div>
        ) : (
          <div className="empty-state">
            <p>No expenses found for {periodLabel}.</p>
          </div>
        )}
      </section>
    </Layout>
  );
};

export default Summary;
