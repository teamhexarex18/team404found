import React,{useState} from 'react';
import axios from 'axios';
import {useNavigate} from 'react-router-dom';
import './otp.css';
function OtpPage() {
    const [otp, setOtp]=useState('');
    const [error, setError]=useState('');
    const [message, setMessage]=useState('');
    const navigate=useNavigate();
    const handleOtpSubmit =async(e)=>{
        e.preventDefault();
        try {
            const userEmail = localStorage.getItem('userEmail');
            if (!userEmail) {
                setError('Email not found. Please register again.');
                return;
            }
            const response = await axios.post(
                'https://heavily-blonde-coming-destroy.trycloudflare.com/verify-otp',
                {
                    email: userEmail,
                    otp: otp,
                });
        
            localStorage.setItem('token',response.data.token);
            navigate('/'); 
        } catch (err) {
            setError('Invalid OTP. Please try again.');
            console.error(err);
        }
    };
    return (
        <div className="otp-container">
            <form className="otp-form" onSubmit={handleOtpSubmit}>
                <h1>Enter OTP</h1>
                <label htmlFor="otp">OTP sent to your email. Enter OTP:</label>
                <input
                    type="text"
                    id="otp"
                    name="otp"
                    maxLength="5"
                    pattern="\d{5}"
                    placeholder="Enter OTP"
                    value={otp}
                    onChange={(e) => setOtp(e.target.value.replace(/[^0-9]/g, ''))}
                    required
                />
                <button type="submit">Submit</button>
            </form>
        </div>
    );
}
export default OtpPage;
