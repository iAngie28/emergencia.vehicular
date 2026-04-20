from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pathlib import Path
from app.core.config import settings 

mail_conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

async def enviar_correo_recuperacion(email_to: str, token: str):
    # En producción, cambia localhost por tu dominio real
    # Reemplaza con el link real de tu frontend en Render
    url_recuperacion = f"https://emergencia-vehicular-1.onrender.com/reset-password?token={token}"
    
    html = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto;">
        <h2>Recuperación de Contraseña - TallerPro</h2>
        <p>Has solicitado restablecer tu contraseña. Haz clic en el botón de abajo para continuar:</p>
        <div style="text-align: center; margin: 30px 0;">
            <a href="{url_recuperacion}" 
               style="background-color: #007bff; color: white; padding: 12px 25px; text-decoration: none; border-radius: 5px;">
               Restablecer Contraseña
            </a>
        </div>
        <p>Este enlace expirará en 15 minutos.</p>
        <p>Si no solicitaste este cambio, puedes ignorar este correo.</p>
    </div>
    """

    message = MessageSchema(
        subject="Restablecer tu clave de TallerPro",
        recipients=[email_to],
        body=html,
        subtype=MessageType.html
    )

    fm = FastMail(mail_conf)
    await fm.send_message(message)