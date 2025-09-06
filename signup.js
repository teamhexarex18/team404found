import React, { useState } from 'react';
import axios from 'axios';
import { Link, useNavigate } from 'react-router-dom';
import './signup.css';

function SignupPage() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [cpassword, setCpassword] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const navigate = useNavigate();

  const handleSignup = async (e) => {
    e.preventDefault();
    if (password !== cpassword) {
      setError('Passwords do not match.');
      setSuccess('');
      return;
    }
    try {
      await axios.post(
        'https://heavily-blonde-coming-destroy.trycloudflare.com/register',
        {
          name,
          email,
          password,
        }
      );
      // Save email and redirect to OTP page
      localStorage.setItem('userEmail', email);
      navigate('/otp');
    } catch (err) {
      setError('Registration failed. Please try again.');
      setSuccess('');
      console.error(err);
    }
  };

  return (
    <form onSubmit={handleSignup}>
      <h1>Create an account</h1>
      {error && <p className="error-message">{error}</p>}
      {success && <p className="success-message">{success}</p>}
      <label htmlFor="name">Name:</label>
      <input
        type="text"
        id="name"
        placeholder="Enter Full Name"
        maxLength="20"
        value={name}
        onChange={(e) => setName(e.target.value)}
        required
      /><br /><br />
      <label htmlFor="email">Email:</label>
      <input
        type="email"
        id="email"
        placeholder="Enter Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        required
      /><br /><br />
      <label htmlFor="password">Password:</label>
      <input
        type="password"
        id="password"
        name="password"
        placeholder="Enter Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        required
      /><br /><br />
      <label htmlFor="cpassword">Confirm Password:</label>
      <input
        type="password"
        id="cpassword"
        name="cpassword"
        placeholder="Confirm Password"
        value={cpassword}
        onChange={(e) => setCpassword(e.target.value)}
        required
      /><br /><br />
      <label>
        <Link className="link" to="/">Sign in instead</Link>
      </label>
      <input type="submit" value="Send OTP" />
    </form>
  );
}

export default SignupPage;