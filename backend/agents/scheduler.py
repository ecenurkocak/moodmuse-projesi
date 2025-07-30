import time
import asyncio
from apscheduler.schedulers.background import BackgroundScheduler
from .weekly_mood_report import send_weekly_mood_reports

def run_async_job():
    """
    Asenkron `send_weekly_mood_reports` fonksiyonunu çalıştırmak için bir sarmalayıcı.
    APScheduler senkron bir ortamda çalıştığı için bu gereklidir.
    """
    print("Zamanlanmış görev tetiklendi, asenkron raporlama başlatılıyor...")
    asyncio.run(send_weekly_mood_reports())

def start_scheduler():
    """
    Haftalık rapor gönderimini zamanlamak için bir zamanlayıcı başlatır.
    Görev, her Pazar saat 21:00'de çalışacak şekilde ayarlanmıştır.
    """
    scheduler = BackgroundScheduler(timezone="Europe/Istanbul")
    
    # Görevi her Pazar saat 21:00'de çalışacak şekilde ayarla
    scheduler.add_job(run_async_job, 'interval', seconds=10)

    """scheduler.add_job(
        run_async_job,  # Asenkron işi çalıştıran sarmalayıcıyı çağır
        'cron',
        day_of_week='sun',
        hour=21,
        minute=0
    )
    """
    scheduler.start()
    print("Zamanlayıcı başlatıldı. Haftalık raporlar her Pazar 21:00'de gönderilecek.")

    try:
        # Ana thread'in sonlanmasını engellemek için sonsuz döngü
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print("Zamanlayıcı durduruldu.")

if __name__ == "__main__":
    start_scheduler()
