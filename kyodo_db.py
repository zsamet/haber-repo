import asyncio
import aiohttp
from bs4 import BeautifulSoup
import mysql.connector
import requests

# MySQL veritabanı bağlantısı kurulması
connection_config = {
    "host": "172.21.54.148",
    "port": "3306",
    "user": "NYP23-11",
    "password": "Uludag9512357.",
    "database": "neis_news"
}

async def fetch_and_save_links_kyodonews(session, new_links_kyodo):
    url = "https://english.kyodonews.net/news"

    try:
        async with session.get(url, timeout=10) as response:
            if response.status == 200:
                soup = BeautifulSoup(await response.text(), 'html.parser')

                # Ana içerik bölümünü belirle
                sec_latest = soup.find("div", class_="sec-latest")

                if sec_latest:
                    # Her bir haber bloğunu seç
                    news_blocks = sec_latest.find_all("div", class_="row")

                    for news_block in news_blocks:
                        news_contents = news_block.find_all("article", class_="col-md-3")

                        for news_content in news_contents:
                            link = news_content.a.get("href")
                            full_news_url = f"https://english.kyodonews.net{link}"

                            # İlgili haber başlığını çek
                            title = news_content.h3.get_text(strip=True)

                            # İlgili haber içeriğini çek
                            response_content = requests.get(full_news_url)

                            if response_content.status_code == 200:
                                soup_content = BeautifulSoup(response_content.content, "html.parser")
                                news_content_text = "\n".join(paragraph.get_text(strip=True) for paragraph in soup_content.select("div.article-body p"))
                            else:
                                print("İçerik bulunamadı")

                    # Veritabanındaki linklerin kontrolü
                    existing_links = get_existing_links()
                    new_links_kyodo = [link for link in new_links_kyodo if link not in existing_links]

                    if new_links_kyodo:
                        print(f"Yeni linkler bulundu: {new_links_kyodo}")
                        save_links_to_database(new_links_kyodo)

                else:
                    print(f"Sayfa yüklenemedi. Durum Kodu: {response.status}")

    except Exception as e:
        print(f"Bağlantı hatası: {e}")


def get_existing_links():
    try:
        conn = mysql.connector.connect(**connection_config)
        cursor = conn.cursor()

        # Veritabanından mevcut linkleri çekme
        select_query = "SELECT news_link FROM news"
        cursor.execute(select_query)

        existing_links = {row[0] for row in cursor.fetchall()}

        cursor.close()
        conn.close()

        return existing_links
    except Exception as e:
        print(f"Hata: {e}")
        return set()

def save_links_to_database(links):
    try:
        conn = mysql.connector.connect(**connection_config)
        cursor = conn.cursor()

        for link in links:
            # Her linki "news_link" sütununa eklemek için SQL sorgusu
            insert_query = "INSERT INTO news (news_link) VALUES (%s)"
            data = (link,)

            cursor.execute(insert_query, data)

        conn.commit()
        cursor.close()
        conn.close()

        print("Linkler veritabanına kaydedildi.")
    except Exception as e:
        print(f"Hata: {e}")


async def main():
    async with aiohttp.ClientSession() as session:
        while True:
            new_links_world = set()
            await fetch_and_save_links_kyodonews(session, new_links_kyodo)
            await asyncio.sleep(30)

# Asenkron ana döngüyü başlat
if __name__ == "__main__":
    asyncio.run(main())