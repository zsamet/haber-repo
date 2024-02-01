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

# BUSINESS

async def fetch_and_save_links_business(session, new_links_business):
    url = "https://www.bbc.com/news/business"

    try:
        async with session.get(url, timeout=10) as response:
            if response.status == 200:
                soup = BeautifulSoup(await response.text(), 'html.parser')
                latest_updates_heading = soup.find(lambda tag: tag.name == "h2" and "Latest Updates" in tag.string)

                if latest_updates_heading:
                    latest_updates_section = latest_updates_heading.find_next_sibling('div')

                    if latest_updates_section:
                        links = latest_updates_section.find_all('a', href=True)
                        
                        new_links = set(link['href'] if link['href'].startswith("https://www.bbc.com") else "https://www.bbc.com" + link['href'] for link in links if "https://www.bbc.co.uk/usingthebbc/terms/can-i-share-things-from-the-bbc" not in link['href'] and "{assetUri}" not in link['href'])
                        
                        # Veritabanındaki linklerin kontrolü
                        existing_links = get_existing_links()
                        new_links_business = [link for link in new_links if link not in existing_links]
                                
                        if new_links_business:
                            print(f"Yeni linkler bulundu: {new_links_business}")
                            save_links_to_database(new_links_business)

                    else:
                        print("Latest Updates altındaki içerik bulunamadı.")
                else:
                    print("Latest Updates başlığı bulunamadı.")
            else:
                print(f"Sayfa yüklenemedi. Durum Kodu: {response.status}")
    except Exception as e:
        print(f"Bağlantı hatası: {e}")

# CLIMATE
async def fetch_and_save_links_climate(session, new_links_climate):
    url = "https://www.bbc.com/news/topics/cmj34zmwm1zt"

    try:
        async with session.get(url, timeout=10) as response:
            if response.status == 200:
                soup = BeautifulSoup(await response.text(), 'html.parser')

                # Belirtilen sayfadaki makaleleri bulma
                articles = soup.find_all('div', class_='ssrcss-10i168z-LinkPost edn7j850')

                for article in articles:
                    headline = article.find('h3', class_='ssrcss-17h8shz-StyledHeading e10rt3ze0')
                    link = article.find('a')['href']
                    timestamp = article.find('span', class_='ssrcss-dyweam-Timestamp ej9ium93')

                    if link and not link.startswith("https://www.bbc.co.uk/usingthebbc/terms/can-i-share-things-from-the-bbc") and "{assetUri}" not in link:
                        # Linkin başında "https://www.bbc.com" olup olmadığını kontrol ederek gerektiğinde ekleyin
                        full_link = link if link.startswith("https://www.bbc.com") else "https://www.bbc.com" + link
                        new_links_climate.add(full_link)

                # Veritabanındaki linklerin kontrolü
                existing_links = get_existing_links()
                new_links_climate = [link for link in new_links_climate if link not in existing_links]
                        
                if new_links_climate:
                    print(f"Yeni linkler bulundu: {new_links_climate}")
                    save_links_to_database(new_links_climate)

            else:
                print(f"Sayfa yüklenemedi. Durum Kodu: {response.status}")
    except Exception as e:
        print(f"Bağlantı hatası: {e}")


# ENTERTAINMENT

# ENTERTAINMENT
async def fetch_and_save_links_entertainment(session, new_links_enter):
    url = "https://www.bbc.com/news/entertainment_and_arts"

    try:
        async with session.get(url, timeout=10) as response:
            if response.status == 200:
                soup = BeautifulSoup(await response.text(), 'html.parser')

                # Belirtilen sayfadaki makaleleri bulma
                articles = soup.find_all('div', class_='ssrcss-10i168z-LinkPost edn7j850')

                for article in articles:
                    headline = article.find('h3', class_='ssrcss-17h8shz-StyledHeading e10rt3ze0')
                    link = article.find('a')['href']
                    timestamp = article.find('span', class_='ssrcss-dyweam-Timestamp ej9ium93')

                    if link and not link.startswith("https://www.bbc.co.uk/usingthebbc/terms/can-i-share-things-from-the-bbc") and "{assetUri}" not in link:
                        # Linkin başında "https://www.bbc.com" olup olmadığını kontrol ederek gerektiğinde ekleyin
                        full_link = link if link.startswith("https://www.bbc.com") else "https://www.bbc.com" + link
                        new_links_enter.add(full_link)

                # Veritabanındaki linklerin kontrolü
                existing_links = get_existing_links()
                new_links_enter = [link for link in new_links_enter if link not in existing_links]
                        
                if new_links_enter:
                    print(f"Yeni linkler bulundu: {new_links_enter}")
                    save_links_to_database(new_links_enter)

            else:
                print(f"Sayfa yüklenemedi. Durum Kodu: {response.status}")
    except Exception as e:
        print(f"Bağlantı hatası: {e}")



# SCIENCE

# SCIENCE
async def fetch_and_save_links_science(session, new_links_science):
    url = "https://www.bbc.com/news/science_and_environment"

    try:
        async with session.get(url, timeout=10) as response:
            if response.status == 200:
                soup = BeautifulSoup(await response.text(), 'html.parser')
                articles = soup.find_all('div', class_='ssrcss-10i168z-LinkPost edn7j850')

                if articles:
                    for article in articles:
                        link_tag = article.find('a', href=True)
                        if link_tag and link_tag['href'].startswith('/news/'):
                            # Linkin başında "https://www.bbc.com" olup olmadığını kontrol ederek gerektiğinde ekleyin
                            full_link = "https://www.bbc.com" + link_tag['href'] if not link_tag['href'].startswith("https://www.bbc.com") else link_tag['href']
                            new_links_science.add(full_link)

                    # Veritabanındaki linklerin kontrolü
                    existing_links = get_existing_links()
                    new_links_science = [link for link in new_links_science if link not in existing_links]
                            
                    if new_links_science:
                        print(f"Yeni linkler bulundu: {new_links_science}")
                        save_links_to_database(new_links_science)
                    
                else:
                    print("Makale bulunamadı.")
            else:
                print(f"Sayfa yüklenemedi. Durum Kodu: {response.status}")
    except Exception as e:
        print(f"Bağlantı hatası: {e}")


# TECHNOLOGY

# TECHNOLOGY
async def fetch_and_save_links_tech(session, new_links_tech):
    url = "https://www.bbc.com/news/technology"

    try:
        async with session.get(url, timeout=10) as response:
            if response.status == 200:
                soup = BeautifulSoup(await response.text(), 'html.parser')

                # Belirtilen sayfadaki makaleleri bulma
                articles = soup.find_all('div', class_='ssrcss-10i168z-LinkPost edn7j850')

                for article in articles:
                    headline = article.find('h3', class_='ssrcss-17h8shz-StyledHeading e10rt3ze0')
                    link = article.find('a')['href']
                    timestamp = article.find('span', class_='ssrcss-dyweam-Timestamp ej9ium93')

                    if link and not link.startswith("https://www.bbc.co.uk/usingthebbc/terms/can-i-share-things-from-the-bbc") and "{assetUri}" not in link:
                        # Linkin başında "https://www.bbc.com" olup olmadığını kontrol ederek gerektiğinde ekleyin
                        full_link = link if link.startswith("https://www.bbc.com") else "https://www.bbc.com" + link
                        new_links_tech.add(full_link)

                # Veritabanındaki linklerin kontrolü
                existing_links = get_existing_links()
                new_links_tech = [link for link in new_links_tech if link not in existing_links]
                        
                if new_links_tech:
                    print(f"Yeni linkler bulundu: {new_links_tech}")
                    save_links_to_database(new_links_tech)

            else:
                print(f"Sayfa yüklenemedi. Durum Kodu: {response.status}")
    except Exception as e:
        print(f"Bağlantı hatası: {e}")



# WORLD

# WORLD
async def fetch_and_save_links_world(session, new_links_world):
    url = "https://www.bbc.com/news/world"

    try:
        async with session.get(url, timeout=10) as response:
            if response.status == 200:
                soup = BeautifulSoup(await response.text(), 'html.parser')
                latest_updates_heading = soup.find(lambda tag: tag.name == "h2" and "Latest Updates" in tag.string)

                if latest_updates_heading:
                    latest_updates_section = latest_updates_heading.find_next_sibling('div')

                    if latest_updates_section:
                        links = latest_updates_section.find_all('a', href=True)
                        
                        # Linkin başında "https://www.bbc.com" olup olmadığını kontrol ederek gerektiğinde ekleyin
                        new_links_world.update(set(link['href'] if link['href'].startswith("https://www.bbc.com") else "https://www.bbc.com" + link['href'] for link in links if "https://www.bbc.co.uk/usingthebbc/terms/can-i-share-things-from-the-bbc" not in link['href'] and "{assetUri}" not in link['href']))
                        
                        # Veritabanındaki linklerin kontrolü
                        existing_links = get_existing_links()
                        new_links_world = {link for link in new_links_world if link not in existing_links}
                                
                        if new_links_world:
                            print(f"Yeni linkler bulundu: {new_links_world}")
                            save_links_to_database(new_links_world)

                    else:
                        print("Latest Updates altındaki içerik bulunamadı.")
                else:
                    print("Latest Updates başlığı bulunamadı.")
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
            new_links_business = set()
            await fetch_and_save_links_business(session, new_links_business)
            await asyncio.sleep(30)
            
            new_links_climate = set()
            await fetch_and_save_links_climate(session, new_links_climate)
            await asyncio.sleep(30)
            
            new_links_enter = set()
            await fetch_and_save_links_entertainment(session, new_links_enter)
            await asyncio.sleep(30)
            
            new_links_science = set()
            await fetch_and_save_links_science(session, new_links_science)
            await asyncio.sleep(30)
            
            new_links_tech = set()
            await fetch_and_save_links_tech(session, new_links_tech)
            await asyncio.sleep(30)
            
            new_links_world = set()
            await fetch_and_save_links_world(session, new_links_world)
            await asyncio.sleep(30)

# Asenkron ana döngüyü başlat
if __name__ == "__main__":
    asyncio.run(main())
