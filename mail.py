import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# SMTP server details
smtp_server = "smtp.office365.com"
port = 587  # For TLS

# Sender's and receiver's email addresses
sender_email = "kiryugaming99@outlook.com"
receiver_email = "dsteyn431@gmail.com"
app_password = "password"  # Use the App Password

# Email content
subject = "Test Email"
body = "This is a test email sent from a Python script."

# Create a multipart email
msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = receiver_email
msg['Subject'] = subject

# Attach the body text to the email
msg.attach(MIMEText(body, 'example mail'))

# Sending the email
try:
    # Connect to the server
    server = smtplib.SMTP(smtp_server, port)
    server.starttls()  # Secure the connection
    
    # Log in to the SMTP server
    server.login(sender_email, app_password)
    
    # Send the email
    server.sendmail(sender_email, receiver_email, msg.as_string())
    
    print("Email sent successfully!")
    
except Exception as e:
    print(f"Error: {e}")
    
finally:
    # Terminate the SMTP session
    server.quit()
