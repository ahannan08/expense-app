import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './styles/Predictor.css';
import ManagePrediction from './ManagePrediction';

const Predictor = () => {
  const [budget, setBudget] = useState('');
  const [foodLevel, setFoodLevel] = useState('High');
  const [entertainmentLevel, setEntertainmentLevel] = useState('Low');
  const [month, setMonth] = useState(3); // Default to March
  const [year, setYear] = useState(2024); // Default to 2024
  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState(null);
  const [predictionExists, setPredictionExists] = useState(false);
  const API_URL = process.env.REACT_APP_API_BASE_URL;  
  const navigate = useNavigate();

  // Check if prediction exists when month or year changes
  useEffect(() => {
    checkIfPredictionExists();
  }, [month, year]);

  const handleSubmit = async (event) => {
    event.preventDefault();

    const payload = {
      budget: parseInt(budget),
      month: parseInt(month),
      year: parseInt(year),
      food_level: foodLevel,
      entertainment_level: entertainmentLevel,
    };

    try {
      const response = await axios.post(`${API_URL}/api/predict-category`, payload);
      const { total_expense, category_expenses } = response.data;
      setPrediction({
        totalExpense: total_expense,
        categoryExpenses: category_expenses,
      });
      setError(null);

      // After receiving prediction, check if it already exists
      checkIfPredictionExists();
    } catch (error) {
      setError('An error occurred while fetching the prediction.');
      setPrediction(null);
    }
  };

  const checkIfPredictionExists = async () => {
    try {
      const response = await axios.get(`http://127.0.0.1:5000/api/predictions/get-prediction?month=${month}&year=${year}`);
      // If a prediction is found, set predictionExists to true; otherwise, false
      setPredictionExists(response.data !== null && response.data !== undefined);
    } catch (error) {
      console.error('Error checking existing prediction:', error);
      setPredictionExists(false);
    }
  };

  const handleNavigateToMyExpenses = () => {
    if (prediction) {
      const budgetStatus = prediction.totalExpense > parseFloat(budget) ? 'Over Budget' : 'Under Budget';
      navigate('/my-expenses', {
        state: {
          totalExpense: prediction.totalExpense,
          categoryExpenses: prediction.categoryExpenses,
          budgetStatus: budgetStatus,
        },
      });
    }
  };

  const handleBackClick = () => {
    navigate('/'); // Navigate back to the MyExpense component
  };

  return (
    <div className="predictor-container">
      <h1>Expense Prediction</h1>

      <button className="back-button" onClick={handleBackClick}>Back</button>

      <div className="form-container">
        <h2>Enter Your Budget for the Month </h2>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Budget for the Month</label>
            <input
              type="number"
              value={budget}
              onChange={(e) => setBudget(e.target.value)}
              placeholder="Enter budget"
              required
            />
          </div>

          <div className="form-group">
            <label>Food Level</label>
            <select
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
            <label>Entertainment Level</label>
            <select
              value={entertainmentLevel}
              onChange={(e) => setEntertainmentLevel(e.target.value)}
              required
            >
              <option value="Low">Low</option>
              <option value="High">High</option>
            </select>
          </div>

          <div className="form-group month-selector">
            <label>Month</label>
            <select
              value={month}
              onChange={(e) => setMonth(e.target.value)}
              required
            >
              <option value={1}>January</option>
              <option value={2}>February</option>
              <option value={3}>March</option>
              <option value={4}>April</option>
              <option value={5}>May</option>
              <option value={6}>June</option>
              <option value={7}>July</option>
              <option value={8}>August</option>
              <option value={9}>September</option>
              <option value={10}>October</option>
              <option value={11}>November</option>
              <option value={12}>December</option>
            </select>
          </div>

          <div className="form-group">
            <label>Year</label>
            <input
              type="number"
              value={year}
              onChange={(e) => setYear(e.target.value)}
              placeholder="Enter year"
              required
            />
          </div>

          <button type="submit">Get Prediction</button>
        </form>
      </div>

      {/* Display Prediction */}
      {prediction && (
        <div className="prediction-container">
          <h2>Expected Prediction for Expense</h2>
          <ul>
            {Object.entries(prediction.categoryExpenses).map(([category, expense]) => (
              <li key={category}>
                <strong>{category}:</strong> Rs {expense.toFixed(2)}
              </li>
            ))}
          </ul>
          <h3>Total Expense: Rs {prediction.totalExpense.toFixed(2)}</h3>
          <h3>Status: {prediction.totalExpense > parseFloat(budget) ? 'Over Budget' : 'Under Budget'}</h3>
          
          {/* Save/Update Prediction */}
          <ManagePrediction
            prediction={prediction}
            budget={budget}
            month={month}
            year={year}
            predictionExists={predictionExists}
          />
        </div>
      )}


      {/* Error handling */}
      {error && <div className="error">{error}</div>}
    </div>
  );
};

export default Predictor;
