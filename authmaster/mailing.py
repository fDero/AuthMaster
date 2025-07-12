import smtplib
from exceptions import *
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def setup_smtp_info(args) -> dict:
    return {
        "server": args.smtp_server,
        "port": args.smtp_port,
        "email": args.smtp_email,
        "creds": args.smtp_passw
    }


def send_email(smtp_info: dict, recipient_email: str, subject: str, body: str):
    smtp_server = smtp_info["server"]
    smtp_port = smtp_info["port"]
    sender_email = smtp_info["email"]
    sender_password = smtp_info["creds"]

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, message.as_string())
        server.quit()
    except Exception:
        raise SmtpConnectionException()


def send_verification_email(smtp_info: dict, account: dict):
    send_email(
        smtp_info,
        account["email"],
        "Account Verification",
        "Here is your verification code: {otp}".format(otp=account["state"]["email-otp"])
    )
