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

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        received_name = request.form.get('name')
        received_email = request.form.get('email')
        received_message = request.form.get('message')
        received_subject = request.form.get('subject')
        
        # --- MAİL GÖNDERME AYARLARI ---
        my_mail = os.getenv("MY_EMAIL")
        my_app_password = os.getenv("MY_APP_PASSWORD")

        # Mail paketini hazırlıyoruz
        msg = MIMEMultipart()
        msg['From'] = received_email
        msg['To'] = my_mail 
        msg['Subject'] = f"Portfolyo: {received_name} sana ulaştı!"

        # Mailin içindeki metin
        body = f"You get a new message from your portfolio website.\n\nFrom: {received_name}\nE-mail: {received_email}\nSubject: {received_subject}\n\nMessage:\n{received_message}"
        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP('smtp.gmail.com', 465)
            server.starttls() 
            server.login(my_mail, my_app_password) 
            server.send_message(msg) 
            server.quit() 
            
            return render_template('contact.html', basari_mesaji="we received your message we will get back to you soon.")
            
        except Exception as e:
            # İnternet kopsa veya şifre yanlış olsa bile site çökmesin diye hatayı yakalıyoruz
            print(f"Mail gönderilirken hata oluştu: {e}")
            return render_template('contact.html', basari_mesaji="Bir hata oluştu, lütfen daha sonra tekrar deneyin.")

    # Sadece sayfayı görüntüleyenler için boş formu göster
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
    


