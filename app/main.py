from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from .services import send_email, generate_ai_content
from apscheduler.schedulers.background import BackgroundScheduler
import datetime

app = FastAPI()
scheduler = BackgroundScheduler()
scheduler.start()

class EmailRequest(BaseModel):
    recipient: EmailStr
    subject: str
    body: str
    send_at: datetime.datetime = None

@app.post("/send_email/")
async def send_email_api(email_request: EmailRequest):
    if email_request.send_at:
        scheduler.add_job(
            send_email, 
            'date', 
            run_date=email_request.send_at, 
            args=[email_request.recipient, email_request.subject, email_request.body]
        )
        return {"message": "Email scheduled successfully."}
    else:
        send_email(email_request.recipient, email_request.subject, email_request.body)
        return {"message": "Email sent successfully."}

@app.post("/generate_email/")
async def generate_email(prompt: str):
    try:
        content = generate_ai_content(prompt)
        return {"generated_content": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
