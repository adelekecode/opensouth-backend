from djoser.email import PasswordResetEmail
import os
import requests
from config.send_mail import send_email



key = os.getenv("email_key")





def requestotp_mail(email, otp, name):

    message = """

"""

    send_email(
        recipient=email,
        subject="OpenSouth - Request OTP",
        body=message
    )
 
   

   
def reset_password_mail(email, url, name):

    message = """

"""

    send_email(
        recipient=email,
        subject="OpenSouth - Reset Password",
        body=message
    )

    