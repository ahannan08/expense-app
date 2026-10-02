import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Home from './components/Home';
import Predictor from './components/Predictor';
import MyExpense from './components/MyExpense';
import Gexpenses from './components/Gexpenses';
import Summary from './components/Summary';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/log-expense" element={<MyExpense />} />
        <Route path="/prediction" element={<Predictor />} />
        <Route path="/expenses" element={<Gexpenses />} />
        <Route path="/get-expenses" element={<Navigate to="/expenses" replace />} />
        <Route path="/summary" element={<Summary />} />
      </Routes>
    </Router>
  );
}

export default App;
