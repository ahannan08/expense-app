import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import axios from 'axios';
import './styles/MyExpense.css';  // Custom styles for MyExpense component

const MyExpense = () => {
  const [amount, setAmount] = useState('');
  const [category, setCategory] = useState('');
  const [predictedExpenses, setPredictedExpenses] = useState({
    total_expense: 0,
    category_expenses: {
      entertainment: 0,
      food: 0,
    },
    budgetStatus: '',
  });

  const { state } = useLocation(); // Retrieve the prediction data passed via navigate

  useEffect(() => {
    // Fetch prediction data from the server for the current month and year
    const fetchPrediction = async () => {
      const currentMonth = new Date().getMonth() + 1; // Current month (1-based)
      const currentYear = new Date().getFullYear(); // Current year

      try {
        const response = await axios.get(
          `http://127.0.0.1:5000/api/predictions/get-prediction?month=${currentMonth}&year=${currentYear}`
        );

        if (response.data) {
          setPredictedExpenses({
            total_expense: response.data.total_expense || 0,
            category_expenses: {
              food: response.data.category_expenses.Food || 0,
              entertainment: response.data.category_expenses.Entertainment || 0,
            },
            budgetStatus: response.data.budget_status || 'No Prediction',
          });
        } else {
          setPredictedExpenses({
            total_expense: 0,
            category_expenses: {
              food: 0,
              entertainment: 0,
            },
            budgetStatus: 'No Prediction',
          });
        }
      } catch (error) {
        console.error('Error fetching prediction data:', error);
        setPredictedExpenses({
          total_expense: 0,
          category_expenses: {
            food: 0,
            entertainment: 0,
          },
          budgetStatus: 'Error fetching prediction',
        });
      }
    };

    fetchPrediction();
  }, []); // Empty dependency array to fetch prediction on mount

  const categories = [
    'Food', 'Sports', 'Shopping', 'Travel', 'Misc', 'Snacks', 'Petrol', 'Gym', 'Entertainment'
  ];

  const handleCategoryChange = (event) => {
    setCategory(event.target.value); // Single selection, no array
  };

  const handlePostExpense = async (event) => {
    event.preventDefault();

    const expenseData = {
      amount: parseFloat(amount),
      category: category,  // Use the selected category (single value)
      month: new Date().getMonth() + 1, // Current month (1-based)
      year: new Date().getFullYear(),   // Current year
    };
    console.log("expense data", expenseData); // Ensure the data is correctly structured

    try {
      await axios.post('http://127.0.0.1:5000/api/expenses', expenseData);  // Ensure the correct endpoint
      alert('Expense recorded successfully!');
      // Reset the form fields after submission
      setAmount('');
      setCategory('');
    } catch (error) {
      console.error('Error posting expense:', error);
      alert('Error recording expense.');
    }
  };

  // Array of month names for better formatting
  const monthNames = [
    "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"
  ];

  // Current month name
  const currentMonthName = monthNames[new Date().getMonth()];

  // Conditional styling for budget status
  const budgetStatusStyle = predictedExpenses.budgetStatus === 'Over Budget' 
    ? { color: 'red' }
    : predictedExpenses.budgetStatus === 'Under Budget'
    ? { color: 'green' }
    : {};

  return (
    <div className="my-expense-container">
      {/* Navbar */}
      <div className="navbar">
      <Link to="/prediction" className="nav-link">Prediction</Link>
        <Link to="/get-expenses" className="nav-link">My Expenses</Link>
        <Link to="/summary" className="nav-link">Summary</Link>
      </div>

      {/* Predicted Expenses Section */}
      <div className="predicted-expenses">
        <h2>Predicted Expenses for {currentMonthName}</h2> {/* Display current month */}
        <ul>
          {Object.entries(predictedExpenses.category_expenses).map(([category, expense]) => (
            <li key={category}>
              <strong>{category.charAt(0).toUpperCase() + category.slice(1)}:</strong> Rs {expense.toFixed(2)}
            </li>
          ))}
        </ul>
        <h3 className="total-expense">Total Expense: Rs {predictedExpenses.total_expense.toFixed(2)}</h3> {/* Larger font size */}
        <h3 style={budgetStatusStyle}>Status: {predictedExpenses.budgetStatus}</h3>  {/* Display budget status with conditional color */}
      </div>

      {/* Expense Form */}
      <div className="expense-form">
        <h2>Post an Expense</h2>
        <form onSubmit={handlePostExpense}>
          <div className="form-group">
            <label>Amount</label>
            <input
              type="number"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
              required
            />
          </div>

          <div className="form-group">
            <label>Category</label>
            <div className="category-radio-group">
              {categories.map((cat) => (
                <div key={cat}>
                  <input
                    type="radio"
                    id={cat}
                    name="category"
                    value={cat}
                    onChange={handleCategoryChange}
                    checked={category === cat}
                  />
                  <label htmlFor={cat}>{cat}</label>
                </div>
              ))}
            </div>
          </div>

          <button type="submit">Post Expense</button>
        </form>
      </div>
    </div>
  );
};

export default MyExpense;
