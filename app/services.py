import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import openai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Email Sending Service
def send_email(recipient: str, subject: str, body: str):
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PASSWORD')
    smtp_server = "smtp.gmail.com"
    port = 587

    if not sender_email or not sender_password:
        print("Error: Missing email credentials.")
        return

    try:
        # Prepare email message
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = recipient
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        # Send email using SMTP server
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()  # Start TLS encryption
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient, message.as_string())
        
        print("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")

# AI Content Generator
def generate_ai_content(prompt: str) -> str:
    from openai import OpenAI

    token = os.getenv("github_key")
    endpoint = "https://models.inference.ai.azure.com"
    model_name = "gpt-4o"

    client = OpenAI(
        base_url=endpoint,
        api_key=token,
    )
    response = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You are an  helpful assistant to generate emails",
        },
        {
            "role": "user",
            "content": prompt,
        }
    ],
    model=model_name,
)

    data=response.choices[0].message.content
    return data

