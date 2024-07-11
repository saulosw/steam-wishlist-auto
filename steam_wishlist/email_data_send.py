from smtplib import SMTP
from string import Template
from pathlib import Path
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

ROOT_EMAIL = Path(__file__).parent / 'email_model.html'

def send_data_to_email(destinatario, nome, wishlist_data):
    load_dotenv()

    remetente = os.getenv('EMAIL_STEAM', '')

    smtp_server = os.getenv('SMTP_SERVER_GMAIL', '')
    smtp_port = os.getenv('SMTP_SERVER_PORT', '')
    smtp_username = os.getenv('EMAIL_STEAM', '')
    smtp_password = os.getenv('EMAIL_STEAM_PASSWORD', '')

    games_data = {
        'nome': nome,
        'whitelist_data': '<br>'.join(wishlist_data)
    }

    with open(ROOT_EMAIL, 'r', encoding='utf-8') as email_model:
        text_email = email_model.read()
        template_email = Template(text_email)
        email_content = template_email.safe_substitute(games_data)

    email_structure = MIMEMultipart()
    email_structure['From'] = remetente
    email_structure['To'] = destinatario
    email_structure['Subject'] = 'Lista de Desejos da Steam'

    email_structure.attach(MIMEText(email_content, 'html'))

    try:
        with SMTP(smtp_server, smtp_port) as server:
            server.ehlo()
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(remetente, destinatario, email_structure.as_string())
            print('Email enviado com sucesso!')
    except Exception as e:
        print(f"Algo deu errado ao enviar o email! - {e}")