from djoser.email import PasswordResetEmail
import os
import requests


class CustomPasswordResetEmail(PasswordResetEmail):
    template_name = "email/password_reset.html"

    def get_context_data(self):
        # PasswordResetEmail can be deleted
        context = super().get_context_data()

        user = context.get("user")
        
            
        context["domain"] = self.request.META.get('HTTP_REFERER')
            
        
        return context

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
            <html> <body> <p>Hi {name},</p> <p>Click on the link below to reset your password.</p> <p><a href="{url}">Reset Password</a></p>
            <p>
If you encounter any issues during the verification process or have any questions about our platform,
please don't hesitate to reach out to our friendly support team at support@opensouth.io</p>
<p>Best regards,</p>
<p>Open South.</p> 
</body> </html>
            """
        }
    )
    
