import React, { useState } from 'react';
import api from '../api/client';

const ManagePrediction = ({
  prediction,
  budget,
  month,
  year,
  predictionExists,
  onSaved,
}) => {
  const [saving, setSaving] = useState(false);

  const handleSaveOrUpdatePrediction = async () => {
    const payload = {
      month: parseInt(month, 10),
      year: parseInt(year, 10),
      budget: parseInt(budget, 10),
      total_expense: prediction.totalExpense,
      budget_status:
        prediction.totalExpense > parseFloat(budget) ? 'Over Budget' : 'Under Budget',
      category_expenses: prediction.categoryExpenses,
    };

    setSaving(true);
    try {
      if (predictionExists) {
        const confirmUpdate = window.confirm(
          'Prediction for this month already exists. Do you want to update it?'
        );
        if (confirmUpdate) {
          payload.confirm = true;
          await api.post('/api/predictions/update-all-predictions', [payload]);
          onSaved?.();
        }
      } else {
        await api.post('/api/predictions/save-prediction', payload);
        onSaved?.();
      }
    } catch (error) {
      console.error('Error saving/updating prediction:', error);
    } finally {
      setSaving(false);
    }
  };

  return (
    <button
      type="button"
      className="btn btn-primary"
      onClick={handleSaveOrUpdatePrediction}
      disabled={saving}
    >
      {saving ? 'Saving…' : predictionExists ? 'Update prediction' : 'Save prediction'}
    </button>
  );
};

export default ManagePrediction;
