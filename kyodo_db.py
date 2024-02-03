import asyncio
import aiohttp
from bs4 import BeautifulSoup
import mysql.connector

# MySQL veritabanı bağlantısı kurulması
connection_config = {
    "host": "172.21.54.148",
    "port": "3306",
    "user": "NYP23-11",
    "password": "Uludag9512357.",
    "database": "neis_news"
}

async def fetch_and_save_links_kyodonews(session):
    url = "https://english.kyodonews.net/news"
    new_links_kyodo = set()

    try:
        async with session.get(url, timeout=10) as response:
            if response.status == 200:
                soup = BeautifulSoup(await response.text(), 'html.parser')
                sec_latest = soup.find("div", class_="sec-latest")

                if sec_latest:
                    news_blocks = sec_latest.find_all("div", class_="row")

                    for news_block in news_blocks:
                        news_contents = news_block.find_all("article", class_="col-md-3")

                        for news_content in news_contents:
                            link = news_content.a.get("href")
                            full_news_url = f"https://english.kyodonews.net{link}"
                            new_links_kyodo.add(full_news_url)

    except Exception as e:
        print(f"Bağlantı hatası: {e}")

    if new_links_kyodo:
        existing_links = get_existing_links()
        unique_links = new_links_kyodo - existing_links
        if unique_links:
            save_links_to_database(unique_links)

def get_existing_links():
    try:
        conn = mysql.connector.connect(**connection_config)
        cursor = conn.cursor()
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
        insert_query = "INSERT INTO news (news_link) VALUES (%s)"
        for link in links:
            cursor.execute(insert_query, (link,))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Linkler veritabanına kaydedildi: {len(links)} adet")
    except Exception as e:
        print(f"Hata: {e}")

async def main():
    async with aiohttp.ClientSession() as session:
        await fetch_and_save_links_kyodonews(session)

# Asenkron ana döngüyü başlat
if __name__ == "__main__":
    asyncio.run(main())
