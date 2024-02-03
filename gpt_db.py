import mysql.connector
from openai import OpenAI
import time

# Veritabanı bağlantı bilgileriniz
db_config = {
    'host': '172.21.54.148',
    'port': '3306',
    'user': 'NYP23-11',
    'password': 'Uludag9512357.',
    'database': 'neis_news'
}

# OpenAI API anahtarınız
OPEN_AI_API_KEY = "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"
ASSISTANT_ID = "asst_tagNB2jgTLfgg8bGQTJ9QLD2"
client = OpenAI(api_key=OPEN_AI_API_KEY)

def translate_and_update():
    # Veritabanına bağlan
    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor()

    while True:
        # Tüm 'news_eng' sütununu işlenecek şekilde kontrol et
        cursor.execute("SELECT id, news_eng FROM news WHERE news_turk IS NULL ORDER BY id")
        rows = cursor.fetchall()

        if rows:
            for row in rows:
                if row[1] is not None:  # row[1] news_eng'e karşılık gelir ve None kontrolü yapılır
                    id, text = row
                    print(f"Çevrilecek metin: {text}")

                    text += " \n Bu haber metnini kurallara bağlı kalarak Türkçe olacak şekilde ve başlığın sadece ilk harfi büyük olacak şekilde yeniden yaz."

                    # OpenAI API ile çeviri yap
                    thread = client.beta.threads.create(
                        messages=[
                            {"role": "user", "content": text}
                        ]
                    )
                    run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=ASSISTANT_ID)
                    
                    while run.status != "completed":
                        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
                        time.sleep(50)  # API sorguları arasında bekleme süresi
                    
                    message_response = client.beta.threads.messages.list(thread_id=thread.id)
                    messages = message_response.data
                    translated_text = messages[0].content[0].text.value  # Çeviri sonucunu al
                    print(f"Çevrilen metin: {translated_text}")

                    # Çeviri sonucunu 'news_turk' sütununa yaz
                    update_query = "UPDATE news SET news_turk = %s WHERE id = %s"
                    cursor.execute(update_query, (translated_text, id))
                    cnx.commit()

                    print("Çeviri tamamlandı ve veritabanına kaydedildi.")

                else:
                    print("Çevrilecek uygun metin yok...")
                    # time.sleep(30)  
        else:
            print("Tüm veriler işlendi, yeni veri bekleniyor...")
            time.sleep(60)  # 1 dakika sonra tekrar kontrol et

        # Veritabanı bağlantısını sürekli açık tutmak yerine, her iterasyonda yeniden bağlanabilirsiniz
        cursor.close()
        cnx.close()
        time.sleep(10)  # Kısa bir mola ver
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()

if __name__ == "__main__":
    translate_and_update()
