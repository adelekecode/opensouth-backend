import requests
import os


key = os.getenv("email_key")












   
def organisation_add_users(user, organisation):

    requests.post(

        url="https://api.useplunk.com/v1/send",

        headers = {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"

        },

        json={
            "to": user.email,
            "subject": "Open South - Organisation Invitation",
            "body": f"""
            <html> <body> <p>Dear {str(user.first_name).capitalize()},</p>

<p>You have been invited  into the organisation {str(organisation.name).capitalize()} to become a colaborator.</p>

<p>If you encounter any issues during the process or have any questions about our platform,
please don't hesitate to reach out to our friendly support team at support@opensouth.io</p>

<p>Best regards,</p>
<p>Open South.</p> 
</body> </html>
            """
        }
    )
    




   
def organisation_delete_users(user, organisation):

    requests.post(

        url="https://api.useplunk.com/v1/send",

        headers = {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"

        },

        json={
            "to": user.email,
            "subject": "Open South - Organisation Removal",
            "body": f"""
            <html> <body> <p>Dear {str(user.first_name).capitalize()},</p>

<p>You have been removed from the organisation {str(organisation.name).capitalize()}.</p>
<p>If you think this was an error or unintended, feel free to reach out to our support team.</p>

<p>If you encounter any issues during the process or have any questions about our platform,
please don't hesitate to reach out to our friendly support team at support@opensouth.io</p>

<p>Best regards,</p>
<p>Open South.</p> 
</body> </html>
            """
        }
    )




def organisation_verification_email(email, user, organization, pin):

    
    requests.post(
        url="https://api.useplunk.com/v1/send",
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"
        },
        json={
            "to": email,
            "subject": "Open South - Organization Verification",
            "body": f"""
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
        }
    )






def dataset_created_mail(email, user, message):

    
    requests.post(
        url="https://api.useplunk.com/v1/send",
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"
        },
        json={
            "to": email,
            "subject": "Open South - Dataset Created",
            "body": f"""
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
        }
    )






    
