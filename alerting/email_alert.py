import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email_alert(subject, body, to_email):
    from_email = "anjali00878@gmail.com"  # Replace with your email
    from_password = "rigu jrjz hqfa bstx"     # Replace with your email password or app password

    # Set up the server
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, from_password)

        # Create the email
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject

        # Attach the body with the msg instance
        msg.attach(MIMEText(body, 'plain'))

        # Send the email
        server.sendmail(from_email, to_email, msg.as_string())
        print(f"Alert email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
    finally:
        server.quit()
