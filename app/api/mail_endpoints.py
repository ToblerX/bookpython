from fastapi import APIRouter
from app import schemas, mail

mail_router = APIRouter()


@mail_router.post("/send_mail", tags=["Mail"])
async def send_mail(emails: schemas.EmailModel):
    emails = emails.addresses
    html = "<h1>Welcome to the app</h1>"
    message = mail.create_message(
        recipients=emails,
        subject="Welcome",
        body=html,
    )
    await mail.mail_engine.send_message(message)
    return {"message": "Email sent successfully"}
