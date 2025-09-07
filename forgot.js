import React,{useState} from 'react';
import axios from 'axios';
import {Link} from 'react-router-dom';
import './forgot.css';
function ForgotPasswordPage() {
    const [email,setEmail] = useState('');
    const [message,setMessage] = useState('');
    const [isError,setIsError] = useState(false);
    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await axios.post('https://heavily-blonde-coming-destroy.trycloudflare.com/forgot-password', { email });
            setMessage('If a matching email was found, a password reset link has been sent.');
            setIsError(false);
        } catch (error) {
            setMessage('Failed to send reset link. Please try again later.');
            setIsError(true);
        }
    };
    return (
        <div className="forgot-password-container">
            <form className="forgot-password-form" onSubmit={handleSubmit}>
                <h1>Forgot Password</h1>
                <p>Please enter your registered email</p>
                {message && <p className={isError ? "error-message":"success-message"}>{message}</p>}
                <input
                    type="email"
                    name="email"
                    placeholder="Enter your email"
                    value={email}
                    onChange={(e)=>etEmail(e.target.value)}
                    required
                />
                <input type="submit" value="Send OTP" />
                <Link to="/" className="link">Back to Login</Link>
            </form>
        </div>
    );
}


export default ForgotPasswordPage;
