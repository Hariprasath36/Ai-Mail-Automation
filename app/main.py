from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from .services import generate_and_send_email

app = FastAPI()

class EmailRequest(BaseModel):
    from_address: EmailStr
    to_address: EmailStr
    email_type: str

@app.post("/generate_and_send_email/")
async def api_generate_and_send_email(request: EmailRequest):
    try:
        result = generate_and_send_email(request.from_address, request.to_address, request.email_type)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))