from djoser.email import PasswordResetEmail
import os
import requests



key = os.getenv("email_key")


def signup_mail(email, otp, name):
 
    requests.post(
        "https://api.useplunk.com/v1/track",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}" 
        },
        json={
            "event": 'activation',
            "email": email,
            "data": {
                "code": otp,
                "name": name
                }
            }
    )


def signup_mail(email, otp, name):
 
    requests.post(
        "https://api.useplunk.com/v1/track",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}" 
        },
        json={
            "event": 'activation',
            "email": email,
            "data": {
                "code": otp,
                "name": name
                }
            }
    )



def requestotp_mail(email, otp, name):
 
    requests.post(
        "https://api.useplunk.com/v1/track",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}" 
        },
        json={
            "event": 'request_otp',
            "email": email,
            "data": {
                "code": otp,
                "name": name
                }
            }
    )



def welcome_mail(email, name):
 
    requests.post(
        "https://api.useplunk.com/v1/track",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}" 
        },
        json={
            "event": 'welcome',
            "email": email,
            "data": {
                "name": name
                }
            }
    )




   
def reset_password_mail(email, url, name):

    requests.post(

        url="https://api.useplunk.com/v1/send",

        headers = {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"

        },

        json={
            "to": email,
            "subject": "Reset Password",
            "body": f"""
            <html> <body>
                <src="https://open-south-frontend.vercel.app/assets/logo-1ab2b399.svg" alt="Open South" width="200" height="200">
             
               <p>Hi {name},</p> <p>Click on the link below to reset your password.</p> <p><a href="{url}">Reset Password</a></p>
            <p>
If you encounter any issues during the verification process or have any questions about our platform,
please don't hesitate to reach out to our friendly support team at support@opensouth.io</p>
<p>Best regards,</p>
<p>Open South.</p> 
</body> </html>
            """
        }
    )
    


