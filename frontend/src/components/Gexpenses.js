import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom'; // Import useNavigate hook for navigation
import axios from 'axios';
import './styles/Gexpenses.css';  // Make sure to include the CSS for styling

const Gexpenses = () => {
  const [expenses, setExpenses] = useState([]);
  const navigate = useNavigate();
   // Initialize the navigate function

   const API_URL = process.env.REACT_APP_API_URL;  // Default to local URL for development


  useEffect(() => {
    // Fetch past expenses from the backend
    const fetchExpenses = async () => {
      try {
        const response = await axios.get(`${API_URL}/api/x`);
        setExpenses(response.data); // Set the expenses data from the backend response
      } catch (error) {
        console.error('Error fetching expenses:', error);
        alert('Error retrieving expenses.');
      }
    };

    fetchExpenses();
  }, []);

  const handleBackClick = () => {
    navigate('/'); // Navigate back to the MyExpense component
  };

  return (
    <div className="get-expenses-container">
      {/* Back Button */}
      <button className="back-button" onClick={handleBackClick}>Back to My Expenses</button>

      <h2>My Past Expenses</h2>
      {expenses.length === 0 ? (
        <div className="no-expenses-message">
          <p>No expenses recorded yet.</p>
        </div>
      ) : (
        <div className="table-container">
          <table className="expenses-table">
            <thead>
              <tr>
                <th>Category</th>
                <th>Amount</th>
                <th>Month</th>
                <th>Year</th>
              </tr>
            </thead>
            <tbody>
              {expenses.map((expense, index) => (
                <tr key={index}>
                  <td>{expense.category}</td>
                  <td>Rs {expense.amount}</td>
                  <td>{expense.month}</td>
                  <td>{expense.year}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default Gexpenses;
