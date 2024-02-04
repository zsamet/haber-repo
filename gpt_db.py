import mysql.connector
from openai import OpenAI
import time

# Veritabanı bağlantı bilgileriniz
db_config = {
    'host': 'host_name',
    'port': 'port',
    'user': 'user',
    'password': 'password',
    'database': 'database'
}

# OpenAI API anahtarınız
OPEN_AI_API_KEY = "OPENAI_API_KEY"
ASSISTANT_ID = "ASST_ID"
client = OpenAI(api_key=OPEN_AI_API_KEY)


def translate_and_update():
    # Veritabanına bağlanmak için gerekli konfigürasyon ile bağlantıyı kur
    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor()

    while True:
        # 'news_turk' sütunu boş olan ve dolayısıyla çevrilmemiş haberleri seç
        cursor.execute("SELECT id, news_eng FROM news WHERE news_turk IS NULL ORDER BY id")
        rows = cursor.fetchall()

        if rows:
            for row in rows:
                if row[1] is not None:  # Eğer haber metni (news_eng) boş değilse
                    id, text = row
                    print(f"Çevrilecek metin: {text}")

                    # Çeviri talimatı eklenerek OpenAI API'ye çeviri için gönderilir
                    text += " \n Bu haber metnini kurallara bağlı kalarak Türkçe olacak şekilde ve başlığın sadece ilk harfi büyük olacak şekilde yeniden yaz."

                    # OpenAI API aracılığıyla çeviri işlemi yapılır (API çağrısı örneğe göre kurgusal)
                    thread = client.beta.threads.create(
                        messages=[
                            {"role": "user", "content": text}
                        ]
                    )
                    run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=ASSISTANT_ID)
                    
                    # Çeviri işlemi tamamlanana kadar döngüde bekler
                    while run.status != "completed":
                        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
                        time.sleep(50)  # API sonucunu beklerken bekleme
                    
                    # Çeviri sonucunu alır
                    message_response = client.beta.threads.messages.list(thread_id=thread.id)
                    messages = message_response.data
                    translated_text = messages[0].content[0].text.value  # Çeviri sonucu

                    print(f"Çevrilen metin: {translated_text}")

                    # Çeviri sonucunu veritabanında ilgili haberin 'news_turk' sütunu altında günceller
                    update_query = "UPDATE news SET news_turk = %s WHERE id = %s"
                    cursor.execute(update_query, (translated_text, id))
                    cnx.commit()

                    print("Çeviri tamamlandı ve veritabanına kaydedildi.")
                else:
                    print("Çevrilecek uygun metin yok...")

        else:
            print("Tüm veriler işlendi, yeni veri bekleniyor...")
            time.sleep(60)  # İşlenecek yeni veri gelene kadar bekler

        # Veritabanı bağlantısını yeniden kurmak için mevcut bağlantıyı kapatır ve yeniden açar
        cursor.close()
        cnx.close()
        time.sleep(10)  # Kısa bir mola ver
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()

if __name__ == "__main__":
    translate_and_update()

