import smtplib as smt
from email.mime.text import MIMEText as mt
import random as rd


def sendOTP(email):
    try:
        sender = 'found404at404notfound@gmail.com'
        receiver = email
        password = 'hxth xobb hlzd jmrx'  
        otp = rd.randint(10000, 99999)

       
        msg = mt(f'Your OTP is: {otp}\n\nKindly do not reply to this email.', "plain")
        msg["Subject"] = "Your OTP Code"
        msg["From"] = sender
        msg["To"] = receiver
        msg["Reply-To"] = "noreply@example.com"

        
        with smt.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender, password)
            server.sendmail(sender, [receiver], msg.as_string())  
            print(f"OTP sent successfully to {receiver} {otp}")
            return otp

    except Exception as E:
        print('Exception Raised:', E)
        
