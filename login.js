import React, { useState } from 'react';
import axios from 'axios';
import { Link, useNavigate } from 'react-router-dom';
import './login.css';

function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(
        'https://heavily-blonde-coming-destroy.trycloudflare.com/login',
        {
          email,
          password,
        }
      );
      localStorage.setItem('token', response.data.token);
      navigate('/home');
    } catch (err) {
      setError('Login failed. Please check your credentials.');
      console.error(err);
    }
  };

  return (
    <form onSubmit={handleLogin}>
      <h1>Login into account</h1>
      {error && <p className="error-message">{error}</p>}
      <label htmlFor="email">Email:</label>
      <input
        type="email"
        name="email"
        placeholder="Enter Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        required
      /><br /><br />
      <label htmlFor="password">Password:</label>
      <input
        type="password"
        name="password"
        placeholder="Enter Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        required
      /><br /><br />
      <label>
        <Link className="link" to="/forgot-password">Forgot Password?</Link>
      </label>
      <label>
        <Link className="link" to="/signup">Sign up instead</Link>
      </label>
      <input type="submit" name="login" value="Login" />
    </form>
  );
}

export default LoginPage;