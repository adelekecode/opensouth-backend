import requests
import os
from config.send_mail import send_email















   
def organisation_add_users(user, organisation):

    message = f"""
 <html> <body> <p>Dear {str(user.first_name).capitalize()},</p>

<p>You have been invited  into the organisation {str(organisation.name).capitalize()} to become a colaborator.</p>

<p>If you encounter any issues during the process or have any questions about our platform,
please don't hesitate to reach out to our friendly support team at support@opensouth.io</p>

<p>Best regards,</p>
<p>Open South.</p> 

"""

    send_email(
        email=user.email,
        subject="Open South - Organisation Invitation",
        body=message
    )

   
def organisation_delete_users(user, organisation):

    message = f"""
 <html> <body> <p>Dear {str(user.first_name).capitalize()},</p>

<p>You have been removed from the organisation {str(organisation.name).capitalize()}.</p>
<p>If you think this was an error or unintended, feel free to reach out to our support team.</p>

<p>If you encounter any issues during the process or have any questions about our platform,
please don't hesitate to reach out to our friendly support team at support@opensouth.io</p>

<p>Best regards,</p>
<p>Open South.</p> 
</body> </html>

"""

    send_email(
        email=user.email,
        subject="Open South - Organisation Removal",
        body=message
    )


def organisation_reject_users(user, organisation):

    message = f"""

<html> <body> <p>Dear {str(user.first_name).capitalize()},</p>

<p>Your request to join the organisation {str(organisation.name).capitalize()} as been rejected.</p>
<p>If you think this was an error or unintended, feel free to reach out to our support team.</p>

<p>If you encounter any issues during the process or have any questions about our platform,
please don't hesitate to reach out to our friendly support team at support@opensouth.io</p>

<p>Best regards,</p>
<p>Open South.</p> 
</body> </html>

"""

    send_email(
        email=user.email,
        subject="Open South - Organisation Request Declined",
        body=message
    )


def organisation_verification_email(email, user, organization, pin):

    message = f"""
<html>
    <body>
        <p>Dear {str(user.first_name).capitalize()},</p>

        <p>A new organization, {str(organization.name).capitalize()}, has been created.</p>
        <p>Please use the following verification pin to verify your ownership:</p>

        <p>Verification Pin: {pin}</p>
        <p>If you have any questions or need assistance, please contact our support team at support@opensouth.io.</p>
        <p>Best regards,</p>
        <p>Open South.</p>
    </body>
</html>


"""
    
    send_email(
        email=email,
        subject="Open South - New Organisation Created",
        body=message
    )






def dataset_created_mail(email, user, message):

    message = f"""
 <html>
    <body>
        <p>Dear {str(user.first_name).capitalize()},</p>

        <p> {message}</p>

        <p>If you have any questions or need assistance, please contact our support team at support@opensouth.io.</p>
        <p>Best regards,</p>
        <p>Open South.</p>
    </body>
</html>

"""
    
    send_email(
        email=email,
        subject="Open South - New Dataset Created",
        body=message
    )







   
def public_support_mail(to, name, message, address):

    body = f"""
 <html> <body> <p>Hello Admin,</p>

<p>A new public support mail.</p>

<p style="font-style: italic;">From: {str(name).capitalize()}</p>

<p style="font-style: italic;">Address: {str(address).capitalize()}</p>

<p style="font-style: italic;">Message: {str(message).capitalize()}</p>


<p">Best regards,</p>
<p>Open South.</p> 
</body> 
</html>
"""
    send_email(
        email=to,
        subject="Open South - New Public Support Mail",
        body=body
    )
    
