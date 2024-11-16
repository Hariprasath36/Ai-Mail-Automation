import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

def get_openai_client():
    token = os.getenv("github_key")
    endpoint = "https://models.inference.ai.azure.com"
    
    if not token:
        raise ValueError("Error: Missing OpenAI API key in environment variables.")
    
    return OpenAI(base_url=endpoint, api_key=token)

def generate_and_send_email(from_address: str, to_address: str, email_type: str):
    client = get_openai_client()

    # Generate questions
    questions_response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are an assistant that generates questions to fill in an email template. Provide a list of questions max 5, one per line.",
            },
            {
                "role": "user",
                "content": f"Generate questions to fill in a {email_type} email template.",
            }
        ],
        model="gpt-4o",
    )
    questions = questions_response.choices[0].message.content.strip().split('\n')

    # Collect answers from the user
    answers = []
    for question in questions:
        answer = input(f"{question}: ")
        answers.append(answer)

    # Generate email content
    content_response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are an assistant that generates professional emails based on user inputs. Provide the email in the following format:\nSubject: [Email Subject]\n\n[Email Body]",
            },
            {
                "role": "user",
                "content": f"Generate a {email_type} email using these answers: {', '.join(answers)}",
            }
        ],
        model="gpt-4o",
    )
    content = content_response.choices[0].message.content.strip()
    subject, body = content.split('\n\n', 1)
    subject = subject.replace('Subject: ', '')

    # Send email
    smtp_server = "smtp.gmail.com"
    port = 587
    sender_password = os.getenv('sender_password')

    if not sender_password:
        raise ValueError("Error: Missing email password in environment variables.")

    try:
        message = MIMEMultipart()
        message["From"] = from_address
        message["To"] = to_address
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()
            server.login(from_address, sender_password)
            server.sendmail(from_address, to_address, message.as_string())
        
        print("Email sent successfully.")
        return {
            "message": "Email generated and sent successfully",
            "subject": subject,
            "body": body
        }
    except Exception as e:
        raise Exception(f"Error sending email: {e}")