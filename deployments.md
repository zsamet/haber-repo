******Dağıtım Kılavuzu******

Bu kılavuz, BBC ve Kyodo News web sitelerinden haber içeriği çekme ve işleme için Python betiklerinin nasıl dağıtılacağı ve çalıştırılacağına dair adımları özetlemektedir. Ayrıca OpenAI aracılığıyla içerik çevirisi de dahildir.

Sistem Gereksinimleri

Python 3.7 veya daha yüksek
pip (Python paket yükleyici)
MySQL Server (Tavsiye edilen 5.7 veya daha yüksek)
API çağrıları ve haber içeriği çekme işlemleri için internet erişimi

Gerekli Python Paketleri:
aiohttp
asyncio
beautifulsoup4
mysql-connector-python
requests
requests_html
openai (gpt_db_main.py için)
Bu paketleri pip kullanarak yükleyin:

pip install aiohttp asyncio beautifulsoup4 mysql-connector-python requests requests_html openai

Veritabanı Yapılandırması
Her betik, bir MySQL veritabanına erişim gerektirir. Çalışır ve erişilebilir bir MySQL örneğiniz olduğundan emin olun. Betiklerde kullanılan varsayılan yapılandırma şu şekildedir:

Host: host_name
Port: port
User: user
Password: password
Database: database

Önemli: Her bir betikteki veritabanı yapılandırmasını kendi ortamınıza uyacak şekilde değiştirin. Biz okulun sunucusunu kullandığımız için bilgileri paylaşamıyoruz.

OpenAI API Anahtarı
gpt_db_main.py için bir OpenAI API anahtarınızın olması gerekmektedir. API anahtarınızı betikte belirtin:
OPEN_AI_API_KEY = "openai_api_anahtarınız_buraya"

Betikleri Çalıştırma
MySQL sunucunuzu başlatın ve verilen kimlik bilgileri ile erişilebilir olduğundan emin olun.
Her bir betiği, MySQL bağlantı detaylarınız ve gerekliyse OpenAI API anahtarınız ile güncelleyin.
Her bir betiği ayrı ayrı çalıştırın. 
İlk olarak combined_bbc.py ve kyodo_db.py dosyaları çalıştırılmalı ardından bbc_context_db.py dosyası çalıştırılmalı ve en son gpt_db.py dosyası çalıştırılmalıdır.

Sorun Giderme
Tüm Python bağımlılıklarının yüklendiğinden emin olun.
MySQL sunucunuzun çalıştığını ve erişilebilir olduğunu doğrulayın.
gpt_db_main.py için OpenAI API anahtarının doğru şekilde ayarlandığından emin olun.
