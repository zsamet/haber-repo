import asyncio
import aiohttp
from bs4 import BeautifulSoup
import mysql.connector
import requests

# MySQL veritabanı bağlantısı kurulması
connection_config = {
    "host": "host_name",
    "port": "port",
    "user": "user",
    "password": "password",
    "database": "database"
}

# Gerekli kütüphaneler ve modüllerin içe aktarılması
from aiohttp import ClientSession
from bs4 import BeautifulSoup

# Kyodo News İngilizce haberler sayfasından son haberlerin linklerini ve içeriklerini çeken asenkron fonksiyon
async def fetch_and_save_links_kyodonews(session, new_links_kyodo):
    url = "https://english.kyodonews.net/news"  # Veri çekilecek olan web sayfasının URL'si

    try:
        # Asenkron bir GET isteği ile belirtilen URL'deki içeriği çekme
        async with session.get(url, timeout=10) as response:
            if response.status == 200:  # HTTP isteğinin başarılı olduğunu kontrol etme
                soup = BeautifulSoup(await response.text(), 'html.parser')  # Sayfa içeriğini parse etme

                sec_latest = soup.find("div", class_="sec-latest")  # 'sec-latest' sınıfına sahip div'i bulma

                if sec_latest:
                    news_blocks = sec_latest.find_all("div", class_="row")  # Her bir haber bloğunu içeren div'leri bulma

                    for news_block in news_blocks:
                        news_contents = news_block.find_all("article", class_="col-md-3")  # Her bir haber içeriğini temsil eden article'ları bulma

                        for news_content in news_contents:
                            link = news_content.a.get("href")  # Haberin linkini alma
                            full_news_url = f"https://english.kyodonews.net{link}"  # Tam URL'yi oluşturma
                            title = news_content.h3.get_text(strip=True)  # Haberin başlığını alma

                            # İlgili haberin tam metnini çekmek için asenkron bir GET isteği
                            async with session.get(full_news_url) as response_content:
                                if response_content.status == 200:
                                    soup_content = BeautifulSoup(await response_content.text(), "html.parser")
                                    # Haber metnini paragraflar halinde birleştirme
                                    news_content_text = "\n".join(paragraph.get_text(strip=True) for paragraph in soup_content.select("div.article-body p"))
                                else:
                                    print("İçerik bulunamadı")
                else:
                    print(f"Sayfa yüklenemedi. Durum Kodu: {response.status}")

    except Exception as e:
        print(f"Bağlantı hatası: {e}")  # Genel bir hata oluşursa hata mesajı




def get_existing_links():
    try:
        # Veritabanı bağlantısı kuruluyor
        conn = mysql.connector.connect(**connection_config)
        cursor = conn.cursor()

        # Mevcut tüm haber linklerini çekmek için SQL sorgusu çalıştırılıyor
        select_query = "SELECT news_link FROM news"
        cursor.execute(select_query)

        # Çekilen linkler bir set olarak kaydediliyor, böylece benzersiz linkler elde ediliyor
        existing_links = {row[0] for row in cursor.fetchall()}

        # Kaynakların kapatılması
        cursor.close()
        conn.close()

        return existing_links
    except Exception as e:
        # Hata durumunda bilgilendirme yapılıyor ve boş bir set döndürülüyor
        print(f"Hata: {e}")
        return set()

def save_links_to_database(links):
    try:
        # Veritabanı bağlantısı kuruluyor
        conn = mysql.connector.connect(**connection_config)
        cursor = conn.cursor()

        for link in links:
            # Veritabanına yeni bir link eklemek için SQL sorgusu hazırlanıyor
            insert_query = "INSERT INTO news (news_link) VALUES (%s)"
            data = (link,)

            # Sorgu çalıştırılıyor ve link veritabanına kaydediliyor
            cursor.execute(insert_query, data)

        # Tüm değişikliklerin veritabanına kaydedilmesi
        conn.commit()

        # Kaynakların kapatılması
        cursor.close()
        conn.close()

        print("Linkler veritabanına kaydedildi.")
    except Exception as e:
        # Hata durumunda bilgilendirme yapılıyor
        print(f"Hata: {e}")

async def main():
    # aiohttp ile asenkron bir HTTP istemci oturumu başlatılıyor
    async with aiohttp.ClientSession() as session:
        while True:
            # Yeni haber linkleri için boş bir set oluşturuluyor
            new_links_world = set()
            # Belirli bir haber kaynağından yeni linklerin çekilip kaydedilmesi
            await fetch_and_save_links_kyodonews(session, new_links_world)
            # Belirli bir süre bekleniyor (örneğin, her 30 saniyede bir)
            await asyncio.sleep(30)

# Asenkron ana döngüyü başlat
if __name__ == "__main__":
    asyncio.run(main())