import api from '../api/client';

export const fetchExpenses = async (month, year) => {
  try {
    const params = {};
    if (month != null) params.month = month;
    if (year != null) params.year = year;
    const response = await api.get('/api/expenses', { params });
    return response.data;
  } catch (error) {
    console.error('Error fetching current expenses:', error);
    return [];
  }
};
