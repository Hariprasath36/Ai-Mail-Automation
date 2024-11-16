import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from openai import ChatCompletion


from dotenv import load_dotenv
load_dotenv()
import os


# Email Sending Service
def send_email(recipient: str, subject: str, body: str):
    sender_email = os.environ.get('sender_email')
    sender_password = os.environ.get('sender_password')
    smtp_server = "smtp.gmail.com"
    port = 587

    try:
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = recipient
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP(smtp_server, port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient, message.as_string())
        server.quit()
        print("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")

# AI Content Generator
def generate_ai_content(prompt: str) -> str:
    import openai
    openai.api_key = "your_openai_api_key"
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=500
    )
    return response.choices[0].text.strip()
