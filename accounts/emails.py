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
            <html>
                <body>
                    <img src="https://d1cc9gva10xzzu.cloudfront.net/dataset_files/opensouth.jpg" alt="Open South" width="200" height="200">
                    <p>Hi {name},</p>
                    <p>Need to change your password, No problem. Let us give you a new one.</p>
                    <p><a href="{url}">RESET PASSWORD</a></p>
                    <p>If you did not initiate this password reset or feel that your account may have been accessed by someone else,
                    please reach out to support@opensouth.io.</p>
                    <p>Best regards,</p>
                    <p>Open South.</p>
                </body>
            </html>
            """
        }
    )

