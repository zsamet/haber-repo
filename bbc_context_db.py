import asyncio
from mysql.connector import connect, Error
from requests_html import AsyncHTMLSession

async def fetch_news_content(news_link, retries=3, delay=5):
    session = AsyncHTMLSession()
    try:
        response = await session.get(news_link, timeout=10)
        # h1 etiketine sahip classı al
        headline = response.html.find('h1', first=True)
        headline_text = headline.text if headline else "No headline found"
        # Paragrafları al
        paragraphs = ' '.join([p.text for p in response.html.find('p')])
        # Başlık ve paragrafları birleştir
        content = headline_text + ' ' + paragraphs
        return content
    except Exception as e:
        if retries > 0:
            print(f"Retry {retries} for {news_link} after delay {delay}s due to error: {e}")
            await asyncio.sleep(delay)
            return await fetch_news_content(news_link, retries-1, delay)
        else:
            print(f"Final error fetching news content for {news_link}: {e}")
            return None

async def update_news_content():
    while True:  # Sonsuz döngü
        try:
            connection = connect(
                host="172.21.54.148",
                port="3306",
                user="NYP23-11",
                password="Uludag9512357.",
                database="neis_news"
            )

            cursor = connection.cursor()
            cursor.execute("SELECT ID, news_link FROM news WHERE news_eng IS NULL OR news_eng = ''")
            news_records = cursor.fetchall()

            for news_id, news_link in news_records:
                content = await fetch_news_content(news_link)
                if content:
                    update_query = "UPDATE news SET news_eng = %s WHERE ID = %s"
                    cursor.execute(update_query, (content, news_id))
                    connection.commit()
                    print(f"News ID {news_id} updated")

        except Error as e:
            print(f"Database error: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed")

        await asyncio.sleep(30)  # 30 saniye bekle


asyncio.run(update_news_content())
