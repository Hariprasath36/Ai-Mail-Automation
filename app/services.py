import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
from openai import OpenAI
import re

# Load environment variables from .env file
load_dotenv()

def get_openai_client():
    token = os.getenv("github_key")
    endpoint = "https://models.inference.ai.azure.com"
    
    if not token:
        raise ValueError("Error: Missing OpenAI API key in environment variables.")
    
    return OpenAI(base_url=endpoint, api_key=token)

def generate_and_send_email(from_address: str, to_address: str, prompt: str):
    client = get_openai_client()

    # Step 1: Generate the email template
    try:
        template_response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are an assistant that generates email templates with placeholders in square brackets.",
                },
                {
                    "role": "user",
                    "content": f"Generate an email template for the following request: {prompt}",
                }
            ],
            model="gpt-4o",
        )
        template = template_response.choices[0].message.content.strip()
    except Exception as e:
        raise Exception(f"Error generating email template: {e}")

    # Step 2: Extract placeholders from the template
    placeholders = re.findall(r"\[([^\]]+)\]", template)

    # Step 3: Ask detailed questions for each placeholder dynamically
    questions = []
    for placeholder in placeholders:
        question = f"Please provide the value for '{placeholder}' (one word only):"
        questions.append(question)

    # Step 4: Collect user responses
    answers = {}
    for question, placeholder in zip(questions, placeholders):
        while True:
            print(question)
            answer = input().strip()
            if len(answer.split()) == 1:  # Ensure one-word answer
                answers[placeholder] = answer
                break
            else:
                print("Please provide a one-word answer.")

    # Step 5: Fill the template with user responses
    filled_template = template
    for placeholder, answer in answers.items():
        filled_template = filled_template.replace(f"[{placeholder}]", answer)

    # Extract subject and body
    try:
        subject, body = filled_template.split('\n\n', 1)
        subject = subject.replace('Subject: ', '')
    except ValueError:
        raise Exception("Error parsing filled template into subject and body.")

    # Step 6: Send email
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
