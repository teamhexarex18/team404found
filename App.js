import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import LoginPage from './components/login';
import SignupPage from './components/signup';
import OtpPage from './components/otp';
import HomePage from './components/homepage';
import ForgotPasswordPage from './components/forgot';

function App() {
  return (
    <Router>
      <div className="app-container">
        <nav>
          <Link to="/">Login</Link>
          <Link to="/signup">Sign Up</Link>
          <Link to="/home">Home</Link>
          <Link to="/forgot-password">Forgot Password</Link>
        </nav>
        <Routes>
          <Route path="/" element={<LoginPage />} />
          <Route path="/signup" element={<SignupPage />} />
          <Route path="/otp" element={<OtpPage />} />
          <Route path="/home" element={<HomePage />} />
          <Route path="/forgot-password" element={<ForgotPasswordPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;