from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import smtplib
# import resend
import base64

# get the SMTP credentials from environment variables
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))  # Make sure the port is an integer
FROM_ADDRESS = os.getenv("FROM_ADDRESS")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

def send_qr_email(file_id: str, qr_path: str, download_url: str, recipient: str):
    """
    Sends an email with QR code attachment and inline display.
    """
    # read QR code bytes
    with open(qr_path, "rb") as f:
        qr_image_bytes = f.read()

    # base64 encode for inline display
    qr_image_base64 = base64.b64encode(qr_image_bytes).decode("utf-8")

    # base64 encode for attachment (required by Resend)
    # qr_image_attachment = base64.b64encode(qr_image_bytes).decode("utf-8")

    # html body with inline QR
    html_body = f"""
    <p>Hi there!</p>
    <p>Your file <strong>{file_id}</strong> is now ready for download.</p>
    <p><a href="{download_url}">Click to download your PDF</a></p>
    <p>Or scan the QR code below:</p>
    <img src="data:image/png;base64,{qr_image_base64}" alt="QR Code" />
    """

     # create message container
    msg = MIMEMultipart()
    msg['From'] = FROM_ADDRESS
    msg['To'] = recipient
    msg['Subject'] = f"Your converted file is ready — {file_id}"

    # attach the HTML body to the email
    msg.attach(MIMEText(html_body, 'html'))

    # attach the QR image (as an attachment and inline image)
    image_attachment = MIMEImage(qr_image_bytes)
    image_attachment.add_header('Content-Disposition', 'attachment', filename=f"{file_id}_qr.png")
    image_attachment.add_header('Content-ID', '<qr_code_image>')
    msg.attach(image_attachment)

    try:
        # send the email via Gmail SMTP server
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  
            server.login(FROM_ADDRESS, SMTP_PASSWORD)  
            server.sendmail(FROM_ADDRESS, recipient, msg.as_string()) 
            print("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")

