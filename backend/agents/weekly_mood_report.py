import smtplib
import ssl
import asyncio
import pynliner
import os
from jinja2 import Environment, FileSystemLoader
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from sqlalchemy.future import select

from db.database import AsyncSessionFactory
from db.models import User, MoodEntry
from sqlalchemy.orm import selectinload
from core.config import settings

# E-posta gönderimi için SMTP ayarları config'den okunur
SMTP_SERVER = "smtp.gmail.com"  # Genellikle sabit kalır
SMTP_PORT = 587  # Genellikle sabit kalır
SENDER_EMAIL = settings.SENDER_EMAIL
SENDER_PASSWORD = settings.SENDER_PASSWORD

# Jinja2 Environment'ını ayarla
template_loader = FileSystemLoader(searchpath=os.path.dirname(__file__))
template_env = Environment(loader=template_loader)

async def get_active_users_last_week(db: AsyncSession):
    """
    Son 7 gün içinde en az bir duygu girişi yapmış olan kullanıcıları döndürür.
    """
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    subquery = select(MoodEntry.user_id).filter(MoodEntry.created_at >= seven_days_ago).distinct()
    result = await db.execute(select(User).filter(User.id.in_(subquery)))
    return result.scalars().all()

async def get_dominant_mood_for_user(db: AsyncSession, user_id: int):
    """
    Bir kullanıcının son 7 gündeki en baskın duygu durumunu döndürür.
    """
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    dominant_mood_query = (
        select(MoodEntry.mood_label, func.count(MoodEntry.mood_label).label('mood_count'))
        .filter(MoodEntry.user_id == user_id, MoodEntry.created_at >= seven_days_ago)
        .group_by(MoodEntry.mood_label)
        .order_by(func.count(MoodEntry.mood_label).desc())
        .limit(1)
    )
    result = await db.execute(dominant_mood_query)
    mood = result.first()
    return mood[0] if mood else None

def send_email(receiver_email: str, subject: str, html_content: str):
    """
    Belirtilen alıcıya HTML içerikli bir e-posta gönderir.
    """
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = SENDER_EMAIL
    message["To"] = receiver_email
    
    # Pynliner ile CSS'i inline yap
    p = pynliner.Pynliner()
    inlined_html = p.from_string(html_content).run()
    
    message.attach(MIMEText(inlined_html, "html"))

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls(context=context)
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, receiver_email, message.as_string())
        print(f"E-posta başarıyla gönderildi: {receiver_email}")
    except Exception as e:
        print(f"E-posta gönderilirken hata oluştu: {e}")

def render_email_template(username: str, dominant_mood: str, content: dict) -> str:
    """
    Verilen bilgilerle e-posta HTML şablonunu doldurur ve CSS'i inline hale getirir.
    """
    template = template_env.get_template("email_template.html")
    
    # Renk paletini HTML'e uygun hale getir
    colors = [color.strip() for color in content['color_palette'].split(',')]
    
    html_content = template.render(
        username=username,
        dominant_mood=dominant_mood.capitalize(),
        quote=content['quote'],
        spotify_url=content['spotify_url'],
        colors=colors
    )
    return html_content

async def send_weekly_mood_reports():
    """
    Ana asenkron fonksiyon: Aktif kullanıcıları bulur, içerik üretir ve e-posta gönderir.
    """
    print("Haftalık rapor gönderim süreci başlatıldı...")
    async with AsyncSessionFactory() as session:
        try:
            active_users = await get_active_users_last_week(session)
            print(f"Bu hafta {len(active_users)} aktif kullanıcı bulundu.")
            
            for user in active_users:
                dominant_mood = await get_dominant_mood_for_user(session, user.id)
                
                if dominant_mood:
                    print(f"Kullanıcı: {user.username}, Baskın Duygu: {dominant_mood}")
                    
                    generated_content = await generate_content_for_mood(dominant_mood)
                    
                    email_html = render_email_template(user.username, dominant_mood, generated_content)
                    
                    send_email(user.email, "Bu Haftaki Duygu Raporun Hazır!", email_html)
                else:
                    print(f"Kullanıcı {user.username} için baskın duygu bulunamadı.")
                    
        except Exception as e:
            print(f"Raporlama sürecinde bir hata oluştu: {e}")
        finally:
            print("Haftalık rapor gönderim süreci tamamlandı.")

if __name__ == "__main__":
    asyncio.run(send_weekly_mood_reports())
