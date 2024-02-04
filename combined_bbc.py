import asyncio
import aiohttp
from bs4 import BeautifulSoup
import mysql.connector

# MySQL veritabanı bağlantısı kurulması
connection_config = {
    "host": "host_name",
    "port": "port",
    "user": "user",
    "password": "password",
    "database": "database"
}

# BUSINESS


async def fetch_and_save_links_business(session, new_links_business):
    # Hedef URL
    url = "https://www.bbc.com/news/business"

    try:
        # Asenkron olarak URL'den içerik çekme işlemi
        async with session.get(url, timeout=10) as response:
            # HTTP yanıtının başarılı olup olmadığını kontrol et
            if response.status == 200:
                # Yanıttan alınan HTML içeriğini ayrıştır
                soup = BeautifulSoup(await response.text(), 'html.parser')
                # "Latest Updates" başlığını bul
                latest_updates_heading = soup.find(lambda tag: tag.name == "h2" and "Latest Updates" in tag.string)

                if latest_updates_heading:
                    # "Latest Updates" bölümünü bul
                    latest_updates_section = latest_updates_heading.find_next_sibling('div')

                    if latest_updates_section:
                        # Bölüm içindeki tüm 'a' etiketlerini (linkleri) bul
                        links = latest_updates_section.find_all('a', href=True)
                        
                        # Linklerden tam URL'yi oluştur ve filtrele
                        new_links = set(link['href'] if link['href'].startswith("https://www.bbc.com") else "https://www.bbc.com" + link['href'] for link in links if "https://www.bbc.co.uk/usingthebbc/terms/can-i-share-things-from-the-bbc" not in link['href'] and "{assetUri}" not in link['href'])
                        
                        # Veritabanındaki mevcut linklerle karşılaştırma yap
                        existing_links = get_existing_links()  # Bu fonksiyonun ayrıca tanımlanması gerekiyor
                        new_links_business = [link for link in new_links if link not in existing_links]
                                
                        # Yeni linkler varsa veritabanına kaydet
                        if new_links_business:
                            print(f"Yeni linkler bulundu: {new_links_business}")
                            save_links_to_database(new_links_business)  # Bu fonksiyonun ayrıca tanımlanması gerekiyor

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
    url = "https://www.bbc.com/news/topics/cmj34zmwm1zt"  # İklim haberlerinin çekileceği sayfa URL'si

    try:
        # Asenkron bir GET isteği yapılıyor ve yanıt bekleniyor
        async with session.get(url, timeout=10) as response:
            # HTTP isteğinin başarılı olup olmadığı kontrol ediliyor
            if response.status == 200:
                # Sayfanın HTML içeriğini BeautifulSoup ile ayrıştırılıyor
                soup = BeautifulSoup(await response.text(), 'html.parser')

                # Belirtilen sayfadaki makaleleri bulma
                articles = soup.find_all('div', class_='ssrcss-10i168z-LinkPost edn7j850')

                for article in articles:
                    # Makalenin başlığını, linkini ve zaman damgasını çekme
                    headline = article.find('h3', class_='ssrcss-17h8shz-StyledHeading e10rt3ze0')
                    link = article.find('a')['href']
                    timestamp = article.find('span', class_='ssrcss-dyweam-Timestamp ej9ium93')

                    # Belirli filtreleme kriterlerine göre linkin geçerliliğini kontrol etme
                    if link and not link.startswith("https://www.bbc.co.uk/usingthebbc/terms/can-i-share-things-from-the-bbc") and "{assetUri}" not in link:
                        # Linkin tam URL'sini oluşturma
                        full_link = link if link.startswith("https://www.bbc.com") else "https://www.bbc.com" + link
                        new_links_climate.add(full_link)

                # Veritabanındaki mevcut linklerle yeni bulunan linklerin karşılaştırılması
                existing_links = get_existing_links()
                new_links_climate = [link for link in new_links_climate if link not in existing_links]
                        
                # Yeni bulunan linkler varsa, bunların veritabanına kaydedilmesi
                if new_links_climate:
                    print(f"Yeni linkler bulundu: {new_links_climate}")
                    save_links_to_database(new_links_climate)
            else:
                # HTTP isteği başarısız olursa, hata mesajı yazdırma
                print(f"Sayfa yüklenemedi. Durum Kodu: {response.status}")
    except Exception as e:
        # Bağlantı hatası gibi genel hataların yakalanması ve yazdırılması
        print(f"Bağlantı hatası: {e}")



# ENTERTAINMENT

# Belirli bir URL'den eğlence ve sanatla ilgili makale linklerini asenkron bir şekilde çekip kaydeden fonksiyon
async def fetch_and_save_links_entertainment(session, new_links_enter):
    url = "https://www.bbc.com/news/entertainment_and_arts"  # Veri çekilecek olan web sayfasının URL'si

    try:
        # Asenkron bir GET isteği ile belirtilen URL'deki içeriği çekme
        async with session.get(url, timeout=10) as response:
            if response.status == 200:  # HTTP isteğinin başarılı olduğunu kontrol etme
                soup = BeautifulSoup(await response.text(), 'html.parser')  # Sayfa içeriğini parse etme

                # Sayfada belirtilen CSS sınıfına sahip div elementlerini (makaleleri) bulma
                articles = soup.find_all('div', class_='ssrcss-10i168z-LinkPost edn7j850')

                for article in articles:
                    # Her makale için başlık, link ve zaman damgasını bulma
                    headline = article.find('h3', class_='ssrcss-17h8shz-StyledHeading e10rt3ze0')
                    link = article.find('a')['href']
                    timestamp = article.find('span', class_='ssrcss-dyweam-Timestamp ej9ium93')

                    # Belirli koşulları karşılayan linkleri filtreleme ve düzeltme
                    if link and not link.startswith("https://www.bbc.co.uk/usingthebbc/terms/can-i-share-things-from-the-bbc") and "{assetUri}" not in link:
                        full_link = link if link.startswith("https://www.bbc.com") else "https://www.bbc.com" + link  # Gerekirse URL ön ekini ekleme
                        new_links_enter.add(full_link)  # Yeni linkleri sete ekleme

                # Veritabanındaki mevcut linklerle yeni linklerin kesişimini bulma ve yalnızca yeni olanları kaydetme
                existing_links = get_existing_links()
                new_links_enter = [link for link in new_links_enter if link not in existing_links]
                        
                if new_links_enter:
                    print(f"Yeni linkler bulundu: {new_links_enter}")
                    save_links_to_database(new_links_enter)  # Yeni linkleri veritabanına kaydetme

            else:
                print(f"Sayfa yüklenemedi. Durum Kodu: {response.status}")  # HTTP isteği başarısız olduysa hata mesajı
    except Exception as e:
        print(f"Bağlantı hatası: {e}")  # Genel bir hata oluşursa hata mesajı




# SCIENCE


async def fetch_and_save_links_science(session, new_links_science):
    # Hedef web sayfasının URL'si.
    url = "https://www.bbc.com/news/science_and_environment"

    try:
        # Asenkron olarak web sayfasından veri çekme işlemi başlatılır.
        async with session.get(url, timeout=10) as response:
            # HTTP yanıtı başarılıysa (200 durum kodu), içerik işlenir.
            if response.status == 200:
                # BeautifulSoup ile HTML içeriği ayrıştırılır.
                soup = BeautifulSoup(await response.text(), 'html.parser')
                # Belirli bir CSS sınıfına sahip div etiketleri bulunur (makaleler için).
                articles = soup.find_all('div', class_='ssrcss-10i168z-LinkPost edn7j850')

                # Eğer makaleler bulunursa, her bir makale için işlem yapılır.
                if articles:
                    for article in articles:
                        # Her makale içindeki ilk 'a' etiketi (link) bulunur.
                        link_tag = article.find('a', href=True)
                        # Eğer link geçerliyse (href attribute'u varsa) ve '/news/' ile başlıyorsa:
                        if link_tag and link_tag['href'].startswith('/news/'):
                            # Linkin tam URL'si oluşturulur. Eğer zaten tam URL değilse, başına 'https://www.bbc.com' eklenir.
                            full_link = "https://www.bbc.com" + link_tag['href'] if not link_tag['href'].startswith("https://www.bbc.com") else link_tag['href']
                            # Oluşturulan tam link, yeni linkler kümesine eklenir.
                            new_links_science.add(full_link)

                    # Veritabanındaki mevcut linklerle yeni çekilen linkler karşılaştırılır.
                    existing_links = get_existing_links()
                    new_links_science = [link for link in new_links_science if link not in existing_links]
                            
                    # Eğer yeni ve benzersiz linkler varsa, bunlar kaydedilir.
                    if new_links_science:
                        print(f"Yeni linkler bulundu: {new_links_science}")
                        save_links_to_database(new_links_science)
                    
                else:
                    # Makale bulunamazsa, bir uyarı mesajı yazdırılır.
                    print("Makale bulunamadı.")
            else:
                # HTTP yanıtı başarısızsa, bir hata mesajı yazdırılır.
                print(f"Sayfa yüklenemedi. Durum Kodu: {response.status}")
    except Exception as e:
        # Herhangi bir bağlantı hatası olursa, hata mesajı yazdırılır.
        print(f"Bağlantı hatası: {e}")



# TECHNOLOGY

async def fetch_and_save_links_tech(session, new_links_tech):
    url = "https://www.bbc.com/news/technology"  # Teknoloji haberlerinin çekileceği sayfa URL'si

    try:
        # Asenkron bir GET isteği yapılıyor ve yanıt bekleniyor
        async with session.get(url, timeout=10) as response:
            # HTTP isteğinin başarılı olup olmadığı kontrol ediliyor
            if response.status == 200:
                # Sayfanın HTML içeriğini BeautifulSoup ile ayrıştırılıyor
                soup = BeautifulSoup(await response.text(), 'html.parser')

                # Belirtilen sayfadaki makaleleri bulma
                articles = soup.find_all('div', class_='ssrcss-10i168z-LinkPost edn7j850')

                for article in articles:
                    # Her makale için başlık, link ve zaman damgasını çekme
                    headline = article.find('h3', class_='ssrcss-17h8shz-StyledHeading e10rt3ze0')
                    link = article.find('a')['href']
                    timestamp = article.find('span', class_='ssrcss-dyweam-Timestamp ej9ium93')

                    # Belirli filtreleme kriterlerine göre linkin geçerliliğini kontrol etme
                    if link and not link.startswith("https://www.bbc.co.uk/usingthebbc/terms/can-i-share-things-from-the-bbc") and "{assetUri}" not in link:
                        # Linkin tam URL'sini oluşturma
                        full_link = link if link.startswith("https://www.bbc.com") else "https://www.bbc.com" + link
                        new_links_tech.add(full_link)

                # Veritabanındaki mevcut linklerle yeni bulunan linklerin karşılaştırılması
                existing_links = get_existing_links()
                new_links_tech = [link for link in new_links_tech if link not in existing_links]
                        
                # Yeni bulunan linkler varsa, bunların veritabanına kaydedilmesi
                if new_links_tech:
                    print(f"Yeni linkler bulundu: {new_links_tech}")
                    save_links_to_database(new_links_tech)
            else:
                # HTTP isteği başarısız olursa, hata mesajı yazdırma
                print(f"Sayfa yüklenemedi. Durum Kodu: {response.status}")
    except Exception as e:
        # Bağlantı hatası gibi genel hataların yakalanması ve yazdırılması
        print(f"Bağlantı hatası: {e}")




# BBC World sayfasından "Latest Updates" bölümündeki linkleri çeken ve kaydeden asenkron fonksiyon
async def fetch_and_save_links_world(session, new_links_world):
    url = "https://www.bbc.com/news/world"  # Veri çekilecek olan web sayfasının URL'si

    try:
        # Asenkron bir GET isteği ile belirtilen URL'deki içeriği çekme
        async with session.get(url, timeout=10) as response:
            if response.status == 200:  # HTTP isteğinin başarılı olduğunu kontrol etme
                soup = BeautifulSoup(await response.text(), 'html.parser')  # Sayfa içeriğini parse etme

                # "Latest Updates" başlığını içeren h2 tag'ini bulma
                latest_updates_heading = soup.find(lambda tag: tag.name == "h2" and "Latest Updates" in tag.string)

                if latest_updates_heading:
                    # "Latest Updates" başlığının hemen sonrasında gelen div'i bulma (içerik bölümü)
                    latest_updates_section = latest_updates_heading.find_next_sibling('div')

                    if latest_updates_section:
                        # Bu bölümdeki tüm 'a' tag'lerini (linkleri) bulma
                        links = latest_updates_section.find_all('a', href=True)
                        
                        # Linkleri filtreleyerek ve gerekirse URL ön ekini ekleyerek yeni linkler listesini güncelleme
                        new_links_world.update(set(link['href'] if link['href'].startswith("https://www.bbc.com") else "https://www.bbc.com" + link['href'] for link in links if "https://www.bbc.co.uk/usingthebbc/terms/can-i-share-things-from-the-bbc" not in link['href'] and "{assetUri}" not in link['href']))
                        
                        # Veritabanındaki mevcut linklerle yeni linklerin kesişimini bulma ve yalnızca yeni olanları seçme
                        existing_links = get_existing_links()
                        new_links_world = {link for link in new_links_world if link not in existing_links}
                                
                        if new_links_world:
                            print(f"Yeni linkler bulundu: {new_links_world}")
                            save_links_to_database(new_links_world)  # Yeni linkleri veritabanına kaydetme

                    else:
                        print("Latest Updates altındaki içerik bulunamadı.")  # İlgili bölüm bulunamazsa hata mesajı
                else:
                    print("Latest Updates başlığı bulunamadı.")  # İlgili başlık bulunamazsa hata mesajı
            else:
                print(f"Sayfa yüklenemedi. Durum Kodu: {response.status}")  # HTTP isteği başarısız olduysa hata mesajı
    except Exception as e:
        print(f"Bağlantı hatası: {e}")  # Genel bir hata oluşursa hata mesajı




def get_existing_links():
    try:
        # Veritabanı bağlantısı kurulumu.
        conn = mysql.connector.connect(**connection_config)
        cursor = conn.cursor()

        # Veritabanından mevcut linkleri çekmek için SQL sorgusu.
        select_query = "SELECT news_link FROM news"
        cursor.execute(select_query)

        # Sorgu sonucunu bir set olarak alır, bu, tekrar eden linklerin olmamasını sağlar.
        existing_links = {row[0] for row in cursor.fetchall()}

        # Cursor ve bağlantıyı kapatır.
        cursor.close()
        conn.close()

        return existing_links
    except Exception as e:
        # Hata durumunda hata mesajı yazdırılır ve boş bir set döndürülür.
        print(f"Hata: {e}")
        return set()


def save_links_to_database(links):
    try:
        # Veritabanı bağlantısı kurulumu.
        conn = mysql.connector.connect(**connection_config)
        cursor = conn.cursor()

        for link in links:
            # Veritabanına yeni bir link eklemek için SQL sorgusu.
            insert_query = "INSERT INTO news (news_link) VALUES (%s)"
            data = (link,)

            cursor.execute(insert_query, data)

        # Yapılan değişiklikleri veritabanına kaydeder.
        conn.commit()
        cursor.close()
        conn.close()

        print("Linkler veritabanına kaydedildi.")
    except Exception as e:
        # Hata durumunda hata mesajı yazdırılır.
        print(f"Hata: {e}")



async def main():
    async with aiohttp.ClientSession() as session:
        while True:
            # Her kategori için yeni linklerin bir setini oluşturur.
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
