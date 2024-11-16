from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from .services import send_email, generate_ai_content

app = FastAPI()

class EmailRequest(BaseModel):
    recipient: EmailStr
    subject: str
    body: str

@app.post("/send_email/")
async def send_email_api(email_request: EmailRequest):
    try:
        send_email(email_request.recipient, email_request.subject, email_request.body)
        return {"message": "Email sent successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate_email/")
async def generate_email(prompt: str):
    try:
        content = generate_ai_content(prompt)
        return {"generated_content": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
