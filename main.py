import threading
import resend
from flask import Flask, render_template , request
from api_client import get_blog_posts
import smtplib
import os
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
load_dotenv()

@app.route('/')
def home():
    posts_from_api = get_blog_posts(tag="python", limit=3)
    formatted_for_home = []
    for post in posts_from_api:
        formatted_for_home.append({
            "topic": "Python & Data",      # HTML'deki rozet (badge) kısmı
            "title": post["title"],     # HTML'deki kart ana başlığı (h5)
            "body": post["summary"],     # HTML'deki {% for x in post.body %} döngüsü için listeye çevrildi
            "url": post["url"] ,             # "Read More" linki için (ileride HTML'e eklenebilir)
            "cover_image": post["image"] ,
            "date": post["date"]   
        })
    return render_template('index.html', all_posts=formatted_for_home)

@app.route('/about')
def about():
    return render_template('about.html')

resend.api_key = os.getenv("RESEND_API_KEY")

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        received_name = request.form.get('name')
        received_email = request.form.get('email')
        received_message = request.form.get('message')
        received_subject = request.form.get('subject')

        try:
            # Resend ile mail gönderme işlemi
            params = {
                "from": "onboarding@resend.dev", # Domain onaylatana kadar bu kalmalı
                "to": os.getenv("MY_EMAIL"),    # Kendi mail adresin (Render'da tanımlı olmalı)
                "subject": f"Portfolyo: {received_name} sana ulaştı!",
                "reply_to": received_email,      # Yanıtla dediğinde formu doldurana gitsin
                "html": f"""
                    <h3>Yeni Mesaj Bildirimi</h3>
                    <p><strong>Gönderen:</strong> {received_name} ({received_email})</p>
                    <p><strong>Konu:</strong> {received_subject}</p>
                    <hr>
                    <p><strong>Mesaj:</strong></p>
                    <p>{received_message}</p>
                """
            }

            # Maili gönderiyoruz
            resend.Emails.send(params)

            return render_template('contact.html', basari_mesaji="Mesajın başarıyla bize ulaştı. En kısa sürede döneceğiz.")

        except Exception as e:
            # Hata oluşursa loglara yazdırıyoruz
            print(f"Resend hatası: {e}")
            return render_template('contact.html', basari_mesaji="Maalesef bir hata oluştu, lütfen sonra tekrar dene.")

    return render_template('contact.html')

@app.route('/blog')
def blog():
    posts = get_blog_posts(tag="python", limit=9)
    return render_template('blog.html', posts=posts)

@app.route('/project')
def project():
    return render_template('project.html')


if __name__ == "__main__":
    app.run(debug=True)
    


