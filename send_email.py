import contextlib
import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(subject, sender, recipient, body, filename=""):
    """Sends an email to one or more recipients with an optional attachment.

    Args:
        subject (str): Subject of the email to be sent.
        sender (str): Email address of sender.
        recipient (str or list of strings): Single recipient email address as    string, multiple recipients as bracketed list of strings.
        body (str): Body of the email
        filename (str, optional): Email attachment filename. Defaults to ''.
    """
    port = 25
    smtp_server = os.getenv("SMTP_SERVER")
    login = os.getenv("SMTP_LOGIN")
    password = os.getenv("SMTP_PASS")
    subject = subject
    sender_email = sender
    recipient_email = recipient
    message = MIMEMultipart()
    message["FROM"] = sender_email
    message["TO"] = ", ".join(recipient_email)
    message["SUBJECT"] = subject
    body = body
    message.attach(MIMEText(body, "plain"))

    with contextlib.suppress(FileNotFoundError):
        with open(filename, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        encoders.encode_base64(part)

        part.add_header(
            "Content-Disposition",
            f"attachment; filename={filename}",
        )

        message.attach(part)

    text = message.as_string()

    with smtplib.SMTP(smtp_server, port) as server:  # type: ignore
        server.starttls()
        server.login(login, password)  # type: ignore
        server.sendmail(sender_email, recipient_email, text)
