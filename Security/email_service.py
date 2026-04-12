import smtplib
from email.message import EmailMessage

email_address = "vaultxacc123@gmail.com"
email_app_password = "ykkn gruu atks xtzs" # add your email app-password here

def send_email(to_email, subject, body):
    msg = EmailMessage()
    msg.set_content(body)

    msg['Subject'] = subject
    msg['From'] = email_address
    msg['To'] = to_email

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.ehlo()
            server.starttls()
            server.login(email_address, email_app_password)
            server.send_message(msg)

        return True
    except Exception as e:
        print("Email Error : ", e)
        return False