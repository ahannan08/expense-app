import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom'; // Import useNavigate for back button functionality
import axios from 'axios';
import './styles/Summary.css';  // Custom styles for Summary component

const Summary = () => {
  const [totalExpense, setTotalExpense] = useState(0);
  const [categoryExpenses, setCategoryExpenses] = useState({
    Food: 0,
    Sports: 0,
    Shopping: 0,
    Travel: 0,
    Misc: 0,
    Snacks: 0,
    Petrol: 0,
    Gym: 0,
    Entertainment: 0,
  });
  const [selectedMonth, setSelectedMonth] = useState(new Date().getMonth() + 1);
  const [selectedYear, setSelectedYear] = useState(new Date().getFullYear());
  const [isDataAvailable, setIsDataAvailable] = useState(true);
  const navigate = useNavigate(); // Initialize the navigate function

  useEffect(() => {
    const fetchMonthlyExpenses = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/expenses/monthly-summary', {
          params: { month: selectedMonth, year: selectedYear }
        });

        const data = response.data;

        if (data && data.total_expense > 0) {
          setTotalExpense(data.total_expense);

          const updatedCategoryExpenses = { ...categoryExpenses };
          Object.entries(data.category_expenses).forEach(([category, amount]) => {
            if (updatedCategoryExpenses.hasOwnProperty(category)) {
              updatedCategoryExpenses[category] = amount;
            }
          });

          setCategoryExpenses(updatedCategoryExpenses);
          setIsDataAvailable(true);
        } else {
          setIsDataAvailable(false);  // No data for the selected month/year
        }
      } catch (error) {
        console.error('Error fetching monthly expenses:', error);
        setIsDataAvailable(false);
      }
    };

    fetchMonthlyExpenses();
  }, [selectedMonth, selectedYear]); // Dependency on selected month/year

  const handleBackClick = () => {
    navigate('/'); // Navigate back to the MyExpense component
  };

  return (
    <div className="summary-container">
      {/* Back Button */}
      <button className="back-button" onClick={handleBackClick}>Back</button>

      <div className="filter-container">
        <label>
          <span>Month:</span>
          <select value={selectedMonth} onChange={(e) => setSelectedMonth(e.target.value)}>
            {Array.from({ length: 12 }, (_, index) => (
              <option key={index} value={index + 1}>
                {new Date(0, index).toLocaleString('en', { month: 'long' })}
              </option>
            ))}
          </select>
        </label>

        <label>
          <span>Year:</span>
          <input
            type="number"
            value={selectedYear}
            onChange={(e) => setSelectedYear(e.target.value)}
            min="2020"
          />
        </label>
      </div>

      {isDataAvailable ? (
        <div className="summary-content">
          <h2>Expense Summary for {new Date(selectedYear, selectedMonth - 1).toLocaleString('en', { month: 'long' })} {selectedYear}</h2>

          {/* Category-wise Expenses Section */}
          <div className="category-summary">
            <h3>Category-wise Expenses</h3>
            <div className="category-list">
              {Object.entries(categoryExpenses).map(([category, expense]) => (
                <div key={category} className="category-item">
                  <strong>{category}:</strong> Rs {expense.toFixed(2)}
                </div>
              ))}
            </div>
          </div>

          {/* Total Expense Section */}
          <div className="total-expense">
            <h3>Total Expense</h3>
            <p>Rs {totalExpense.toFixed(2)}</p>
          </div>
        </div>
      ) : (
        <div className="no-expenses">
          <p>No expenses found for {new Date(selectedYear, selectedMonth - 1).toLocaleString('en', { month: 'long' })} {selectedYear}.</p>
        </div>
      )}
    </div>
  );
};

export default Summary;
