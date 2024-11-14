import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv


# Подключаем SMTP SERVER
load_dotenv()
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = os.getenv("SMTP_PORT")
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")


def send_email(to_email, subject, body, image_path):
    msg = MIMEMultipart()
    msg['From'] = SMTP_USER
    msg['To'] = to_email
    msg['Subject'] = subject
    
    # Создаем HTML-контент с измененными стилями
    html = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                font-size: 18px;
                color: #333;
            }}
            .greeting {{
                font-size: 30px;
                color: #28a745; /* Зеленый цвет */
                font-weight: bold;
            }}
            .footer {{
                margin-top: 20px;
                font-size: 16px;
                color: #666;
            }}
            .image {{
                margin-top: 20px;
                width: 150px; /* Увеличенный размер картинки */
                height: 150px;
                border-radius: 50%;
            }}
        </style>
    </head>
    <body>
        <p class="greeting">Привет, друг!</p>
        <p>{body}</p>
        <p class="footer">С уважением,<br>Ваша команда Наблюдатели Бека</p>
        <img src="cid:image1" class="image"/>
    </body>
    </html>
    """
    
    # Прикрепляем HTML-контент
    msg.attach(MIMEText(html, 'html'))

    # Прикрепляем изображение (если указано)
    if image_path and os.path.exists(image_path):
        with open(image_path, 'rb') as img_file:
            img_data = img_file.read()
            image = MIMEImage(img_data, name=os.path.basename(image_path))
            image.add_header('Content-ID', '<image1>')  # Это связывает изображение с ссылкой в HTML
            msg.attach(image)
    
    # Отправка email через SMTP
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(SMTP_USER, SMTP_PASSWORD)
        smtp.send_message(msg)