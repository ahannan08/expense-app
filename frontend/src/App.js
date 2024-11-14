import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Predictor from './components/Predictor';
import MyExpense from './components/MyExpense';  // Import MyExpense component
import Gexpenses from './components/Gexpenses';
import Summary from './components/Summary'; // Import Summary component

function App() {
  return (
    <Router>
     

      <Routes>
        <Route path="/prediction" element={<Predictor />} />
        <Route path="/" element={<MyExpense />} />
        <Route path="/get-expenses" element={<Gexpenses />} /> 
        <Route path="/summary" element={<Summary />} />
      </Routes>
    </Router>
  );
}

export default App;
