// fetch.js

import axios from 'axios';

// Function to fetch the expenses for a specific month and year
export const fetchExpenses = async (month, year) => {
  try {
    const response = await axios.get(`http://127.0.0.1:5000/api/x?month=${month}&year=${year}`);
    return response.data;  // Return the expenses data
  } catch (error) {
    console.error('Error fetching current expenses:', error);
    return [];  // Return an empty array in case of error
  }
};
