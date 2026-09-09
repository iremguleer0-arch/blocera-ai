# Flask:
# BLOCERA web uygulamasını oluşturmak için kullanılır.
#
# jsonify:
# /health gibi API cevaplarını JSON formatında döndürmemizi sağlar.
from flask import Flask, jsonify


# CORS:
# Wix Studio gibi farklı bir internet adresinde çalışan
# frontend'in Python backend'imize istek gönderebilmesini sağlar.
from flask_cors import CORS


# config.py dosyasında oluşturduğumuz
# development ve production ayarlarını buraya aktarıyoruz.
from config import config


# database.py içerisindeki init_db() fonksiyonunu çağırıyoruz.
# Bu fonksiyon gerekli SQLite tablolarını oluşturur.
from app.database import init_db


# create_app() fonksiyonu BLOCERA Flask uygulamasını
# oluşturan ana fabrika (Application Factory) fonksiyonudur.
#
# Hocanın istediği mimaride uygulamanın bütün parçaları
# burada bir araya getirilir.
def create_app():

    # Flask uygulamasını oluşturuyoruz.
    app = Flask(__name__)


    # Şimdilik geliştirme ortamında çalıştığımız için
    # config.py içerisindeki "development" ayarlarını yüklüyoruz.
    #
    # Daha sonra sunucuya yayınladığımızda
    # "production" ayarını kullanabileceğiz.
    app.config.from_object(config["development"])


    # CORS'u aktif ediyoruz.
    #
    # Böylece Wix Studio gibi farklı bir kaynaktan
    # BLOCERA API'ye HTTP isteği gönderilebilir.
    CORS(
        app,
        origins=app.config.get("CORS_ORIGINS", "*")
    )


    # Uygulama bağlamı (app context) içerisinde
    # veritabanını başlatıyoruz.
    #
    # init_db() leads tablosu yoksa oluşturacaktır.
    with app.app_context():
        init_db(app)


    # routes.py dosyasındaki iki Blueprint'i
    # uygulamayı oluşturduktan sonra içe aktarıyoruz.
    #
    # pages_bp -> normal web sayfaları
    # api_bp   -> API işlemleri
    from app.routes import pages_bp, api_bp


    # Normal sayfaları uygulamaya kaydediyoruz.
    #
    # Örneğin:
    # /
    # /dashboard
    app.register_blueprint(pages_bp)


    # API Blueprint'ini "/api" önekiyle kaydediyoruz.
    #
    # routes.py içerisinde "/sohbet" yazmıştık.
    # Buradaki url_prefix sayesinde gerçek adres:
    #
    # /api/sohbet
    #
    # olacaktır.
    app.register_blueprint(
        api_bp,
        url_prefix="/api"
    )


    # Bu rota sunucunun çalışıp çalışmadığını
    # hızlı şekilde kontrol etmek için kullanılır.
    #
    # Tarayıcıdan /health adresine gidildiğinde
    # aşağıdaki JSON cevabını görmeliyiz.
    @app.route("/health")
    def health():

        return jsonify({
            "basari": True,
            "durum": "BLOCERA backend çalışıyor"
        })


    # Hazırladığımız Flask uygulamasını
    # run.py dosyasının kullanabilmesi için geri döndürüyoruz.
    return app