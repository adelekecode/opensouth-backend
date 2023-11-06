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

