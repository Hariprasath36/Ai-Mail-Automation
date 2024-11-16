from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from .services import send_email, generate_ai_content

app = FastAPI()

class EmailGenerateAndSendRequest(BaseModel):
    from_address: EmailStr
    to_address: EmailStr
    prompt: str

@app.post("/generate_and_send_email/")
async def generate_and_send_email(request: EmailGenerateAndSendRequest):
    try:
        # Generate email content
        ai_response = generate_ai_content(f"Generate a professional email with subject and body based on this prompt: {request.prompt}")
        
        # Parse AI response
        lines = ai_response.split('\n', 2)
        if len(lines) < 3:
            raise ValueError("AI response format is incorrect")
        
        subject = lines[0].replace("Subject: ", "").strip()
        body = lines[2].strip()
        
        # Send email
        send_email(request.from_address, request.to_address, subject, body)
        
        return {
            "message": "Email generated and sent successfully",
            "subject": subject,
            "body": body
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))