import React from 'react';
import axios from 'axios';

const ManagePrediction = ({ prediction, budget, month, year, predictionExists }) => {

  const API_URL = process.env.REACT_APP_API_BASE_URL;  // Default to local URL for development

  const handleSaveOrUpdatePrediction = async () => {
    const payload = {
      month: parseInt(month),
      year: parseInt(year),
      budget: parseInt(budget),
      total_expense: prediction.totalExpense,
      budget_status: prediction.totalExpense > parseFloat(budget) ? 'Over Budget' : 'Under Budget',
      category_expenses: prediction.categoryExpenses,
    };

    try {
      if (predictionExists) {
        const confirmUpdate = window.confirm('Prediction for this month already exists. Do you want to update it?');
        if (confirmUpdate) {
          payload.confirm = true;  // Adding confirm flag to payload
          await axios.post(`${API_URL}/api/predictions/update-all-predictions`, [payload]);
          alert('Prediction updated successfully.');
        }
      } else {
        // Save new prediction
        const response = await axios.post(`${API_URL}/api/predictions/save-prediction`, payload);
        if (response.status === 200) {
          alert('Prediction saved successfully.');
        } else {
          alert('Error saving prediction.');
        }
      }
    } catch (error) {
      console.error('Error saving/updating prediction:', error);
      alert('An error occurred while processing the prediction.');
    }
  };

  return (
    <button onClick={handleSaveOrUpdatePrediction}>
      {predictionExists ? 'Update Prediction' : 'Save Prediction'}
    </button>
  );
};

export default ManagePrediction;
