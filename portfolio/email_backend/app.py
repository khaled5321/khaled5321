import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, BaseSettings, EmailStr
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from jinja2 import Environment, select_autoescape, FileSystemLoader


class Settings(BaseSettings):
    EMAIL_HOST: str
    EMAIL_PORT: int
    EMAIL_USERNAME: str
    EMAIL_PASSWORD: str
    EMAIL_FROM: EmailStr
    EMAIL_TO: EmailStr

    class Config:
        env_file = "./.env"


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

env = Environment(
    loader=FileSystemLoader(searchpath="./template"),
    autoescape=select_autoescape(["html", "xml"]),
)


settings = Settings()


async def send(name, email, subject, content):
    # Define the config
    config = ConnectionConfig(
        MAIL_USERNAME=settings.EMAIL_FROM,
        MAIL_PASSWORD=settings.EMAIL_PASSWORD,
        MAIL_FROM=settings.EMAIL_FROM,
        MAIL_PORT=settings.EMAIL_PORT,
        MAIL_SERVER=settings.EMAIL_HOST,
        MAIL_STARTTLS=True,
        MAIL_SSL_TLS=False,
        USE_CREDENTIALS=True,
        VALIDATE_CERTS=True,
    )
    # Generate the HTML template base on the template name
    template = env.get_template("email.html")

    html = template.render(name=name, email=email, subject=subject, content=content)

    # Define the message options
    message = MessageSchema(
        subject=subject, recipients=[settings.EMAIL_TO], body=html, subtype="html"
    )

    # Send the email
    fm = FastMail(config)
    await fm.send_message(message)


class Data(BaseModel):
    name: str
    email: EmailStr
    subject: str
    content: str


@app.post("/send")
async def send_email(data: Data):
    try:
        await send(data.name, data.email, data.subject, data.content)
    except Exception as e:
        return {"msg": str(e)}

    return {"msg": "Email sent successfully"}


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
