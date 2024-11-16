import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Email Sending Service
def send_email(from_address: str, to_address: str, subject: str, body: str):
    smtp_server = "smtp.gmail.com"
    port = 587
    sender_password = os.getenv('sender_password')

    if not sender_password:
        raise ValueError("Error: Missing email password in environment variables.")

    try:
        # Prepare email message
        message = MIMEMultipart()
        message["From"] = from_address
        message["To"] = to_address
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        # Send email using SMTP server
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()  # Start TLS encryption
            server.login(from_address, sender_password)
            server.sendmail(from_address, to_address, message.as_string())
        
        print("Email sent successfully.")
    except Exception as e:
        raise Exception(f"Error sending email: {e}")

# AI Content Generator
def generate_ai_content(prompt: str) -> str:
    token = os.getenv("github_key")
    endpoint = "https://models.inference.ai.azure.com"
    model_name = "gpt-4o"

    if not token:
        raise ValueError("Error: Missing OpenAI API key in environment variables.")

    client = OpenAI(
        base_url=endpoint,
        api_key=token,
    )
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant to generate professional emails. Provide the email in the following format:\nSubject: [Email Subject]\n\n[Email Body]",
            },
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model=model_name,
    )

    return response.choices[0].message.content