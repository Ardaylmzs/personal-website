import requests

def get_blog_posts(tag="python", limit=6):
    url = "https://dev.to/api/articles"
    
    # API'ye göndereceğimiz parametreler
    params = {
        "tag": tag,
        "per_page": limit
    }

    try:
        # API'ye GET isteği atıyoruz. Timeout eklemek sitenin donmasını engeller.
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status() # Eğer 200 OK dönmezse hata fırlatır
        
        # Gelen JSON verisini Python sözlüğüne (dictionary) çeviriyoruz
        articles = response.json()
        
        # Jinja şablonumuzda kullanacağımız yapıya (title, summary, url) uygun bir liste oluşturuyoruz
        formatted_posts = []
        for article in articles:
            formatted_posts.append({
                "title": article.get("title"),
                "summary": article.get("description"), # DEV.to özeti 'description' olarak verir
                "url": article.get("url"),
                "image": article.get("cover_image"),
                "date": article.get("readable_publish_date") # Ekstra: İleride Bootstrap kartlarına resim eklemek istersen
            })
            
        return formatted_posts

    # İnternet kopsa veya API çökse bile sitemiz çalışmaya devam etsin diye hatayı yakalıyoruz
    except requests.exceptions.RequestException as e:
        print(f"Veri çekilirken hata oluştu: {e}")
        return [] # Hata durumunda boş liste döner, böylece Jinja'daki "if posts" bloğumuz hata mesajını gösterir