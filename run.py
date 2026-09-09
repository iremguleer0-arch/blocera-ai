# app klasöründeki __init__.py dosyasında oluşturduğumuz
# create_app() fonksiyonunu buraya aktarıyoruz.
#
# create_app() fonksiyonunun görevi:
# Flask uygulamasını, ayarları, veritabanını,
# CORS sistemini ve rotaları tek yerde birleştirmektir.
from app import create_app


# create_app() fonksiyonunu çalıştırarak
# gerçek BLOCERA Flask uygulamasını oluşturuyoruz.
#
# Oluşan uygulamayı "app" isimli değişkende tutuyoruz.
app = create_app()


# Bu kontrol, run.py dosyası doğrudan çalıştırıldığında
# aşağıdaki sunucunun başlatılmasını sağlar.
#
# Eğer bu dosya başka bir Python dosyasından import edilirse
# app.run() otomatik olarak çalışmaz.
if __name__ == "__main__":

    # Flask geliştirme sunucusunu başlatıyoruz.
    #
    # debug=True:
    # Kodda değişiklik yaptığımızda sunucunun otomatik yeniden başlamasını ve geliştirme hatalarını görmemizi sağlar.
    # port=5000:
    # BLOCERA backend'inin bilgisayarımızdaki
    # 5000 numaralı port üzerinden çalışmasını sağlar.
    app.run(
        debug=True,
        port=5000
    )