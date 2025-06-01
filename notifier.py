import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_notification(permit_id):
    from database import get_all_requests   # Import here to avoid circular import
    
    permits = get_all_requests()
    permit = next((p for p in permits if p[0] == permit_id), None)

    if not permit:
        print("Permit not found.")
        return

    name, flight_no, country, email, status = permit[1], permit[2], permit[3], permit[4], permit[5]

    sender_email = "kclpk2024@gmail.com"
    sender_password = "rtwfxtpkuxqhvzjp"  # App password if using Gmail with 2FA
    subject = f"Flight Permit Status Updated for {flight_no}"
    body = f"""
    Dear {name},

    Your permit request for flight {flight_no} to {country} has been updated.
    Current status: {status}

    Regards,
    Smart Permit Team
    """

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email, msg.as_string())
        server.quit()
        print("Email sent successfully.")
    except Exception as e:
        print("Failed to send email:", e)
