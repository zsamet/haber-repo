import asyncio
from mysql.connector import connect, Error
from requests_html import AsyncHTMLSession


async def fetch_news_content(news_link, retries=3, delay=5):
    # Asenkron HTML oturumu başlat
    session = AsyncHTMLSession()
    try:
        # Belirtilen URL'ye asenkron GET isteği yap
        response = await session.get(news_link, timeout=10)
        
        # Sayfanın HTML'inden 'h1' etiketine sahip ilk öğeyi al
        # Eğer 'h1' etiketi bulunamazsa "No headline found" mesajını döndür
        headline = response.html.find('h1', first=True)
        headline_text = headline.text if headline else "No headline found"
        
        # Sayfadaki tüm 'p' etiketlerini bul ve metinlerini birleştir
        paragraphs = ' '.join([p.text for p in response.html.find('p')])
        
        # Başlık ve paragraf metinlerini birleştirerek içeriği oluştur
        content = headline_text + ' ' + paragraphs
        return content
    except Exception as e:
        # Hata durumunda yeniden deneme mekanizması
        if retries > 0:
            print(f"Retry {retries} for {news_link} after delay {delay}s due to error: {e}")
            await asyncio.sleep(delay) # Belirlenen gecikme süresi kadar bekle
            return await fetch_news_content(news_link, retries-1, delay) # Fonksiyonu yeniden çağır
        else:
            # Tüm yeniden denemeler başarısız olursa, hata mesajını yazdır
            print(f"Final error fetching news content for {news_link}: {e}")
            return None # Hata durumunda None döndür

async def update_news_content():
    while True:  # Sürekli haber içeriklerini güncellemek için sonsuz döngü
        try:
            # Veritabanı bağlantısını kur
            connection = connect(
                host="host_name",
                port="port",
                user="user",
                password="password",
                database="database"
            )

            # Veritabanı üzerinde işlem yapabilmek için bir imleç(cursor) oluştur
            cursor = connection.cursor()
            # İngilizce içeriği boş olan veya hiç eklenmemiş haberlerin ID ve linklerini seç
            cursor.execute("SELECT ID, news_link FROM news WHERE news_eng IS NULL OR news_eng = ''")
            news_records = cursor.fetchall()  # Sorgu sonucunu al

            # Her bir haber kaydı için döngü
            for news_id, news_link in news_records:
                content = await fetch_news_content(news_link)  # Haber içeriğini asenkron olarak çek
                if content:
                    # Haber içeriğini veritabanında güncelle
                    update_query = "UPDATE news SET news_eng = %s WHERE ID = %s"
                    cursor.execute(update_query, (content, news_id))
                    connection.commit()  # Güncellemeyi veritabanına işle
                    print(f"News ID {news_id} updated")  # Güncelleme bilgisini yazdır

        except Error as e:
            # Veritabanı ile ilgili bir hata oluşursa yazdır
            print(f"Database error: {e}")
        finally:
            # İşlemler bittiğinde veritabanı bağlantısını kapat
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed")

        await asyncio.sleep(30)  # Her döngü arasında 30 saniye bekle


asyncio.run(update_news_content())
