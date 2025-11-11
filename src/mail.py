import os
import resend
import base64

resend.api_key = os.getenv("RESEND_API_KEY")

def send_qr_email(file_id: str, qr_path: str, download_url: str):
    """
    Sends an email via Resend with QR code attachment and inline display.
    """
    # read QR code bytes
    with open(qr_path, "rb") as f:
        qr_image_bytes = f.read()

    # base64 encode for inline display
    qr_image_base64 = base64.b64encode(qr_image_bytes).decode("utf-8")

    # base64 encode for attachment (required by Resend)
    qr_image_attachment = base64.b64encode(qr_image_bytes).decode("utf-8")

    # HTML body with inline QR
    html_body = f"""
    <p>Hi there!</p>
    <p>Your file <strong>{file_id}</strong> is now ready for download.</p>
    <p><a href="{download_url}">Click to download your PDF</a></p>
    <p>Or scan the QR code below:</p>
    <img src="data:image/png;base64,{qr_image_base64}" alt="QR Code" />
    """

    # Send email via Resend
    response = resend.Emails.send({
        "from": "onboarding@resend.dev",
        "to": "resend.unfailing273@passmail.com",
        "subject": f"Your converted file is ready — {file_id}",
        "html": html_body,
        "attachments": [
            {
                "name": f"{file_id}_qr.png",
                "content": qr_image_attachment,
                "type": "image/png"
            }
        ]
    })

    return response

