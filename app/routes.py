# Flask içerisinden ihtiyacımız olan araçları içe aktarıyoruz.
#
# Blueprint:
# Rotaları (URL adreslerini) gruplandırmak için kullanılır.
#
# render_template:
# HTML sayfalarını kullanıcıya göstermek için kullanılır.
#
# request:
# Kullanıcının gönderdiği verileri okumamızı sağlar.
#
# jsonify:
# Python verilerini JSON formatında cevap olarak göndermemizi sağlar.
from flask import Blueprint, render_template, request, jsonify


# database.py dosyasındaki hazır veritabanı fonksiyonlarını çağırıyoruz.
#
# Burada SQL yazmıyoruz.
# SQL işlemleri yalnızca database.py içerisinde kalmalıdır.
from app.database import lead_ekle, tum_leadler


# ai_service.py dosyasındaki hazır yapay zekâ servisini
# ve yapay zekâya özel hata sınıfını içe aktarıyoruz.
#
# Burada Groq API kodu yazmayacağız.
# Yapay zekâ işlemleri sadece ai_service.py içerisinde kalacak.
from app.services.ai_service import ai_service, AIServiceError


# Normal web sayfalarını yönetecek Blueprint'i oluşturuyoruz.
#
# Örneğin:
# /
# /dashboard
#
# adresleri bu Blueprint içerisinde olacak.
pages_bp = Blueprint("pages", __name__)


# API işlemlerini yönetecek ikinci Blueprint'i oluşturuyoruz.
#
# Daha sonra __init__.py içerisinde buna "/api" öneki vereceğiz.
#
# Böylece:
# /sohbet     yerine /api/sohbet
# /leads      yerine /api/leads
#
# şeklinde çalışacak.
api_bp = Blueprint("api", __name__)


# Bu rota, web sitesinin ana karşılama sayfasını gösterir.
#
# Kullanıcı tarayıcıdan "/" adresine geldiğinde
# Flask, templates klasöründeki index.html dosyasını açacaktır.
@pages_bp.route("/")
def ana_sayfa():

    # render_template() fonksiyonu bir HTML dosyasını
    # kullanıcıya web sayfası olarak göndermek için kullanılır.
    return render_template("index.html")


# Bu rota, işletme sahibinin müşteri adaylarını
# göreceği yönetim panelini açmak için kullanılır.
#
# Kullanıcı "/dashboard" adresine geldiğinde
# dashboard.html sayfası gösterilecektir.
@pages_bp.route("/dashboard")
def dashboard():

    # Yönetim panelinin HTML dosyasını kullanıcıya gönderiyoruz.
    return render_template("dashboard.html")


# Bu API rotası, kullanıcının BLOCERA yapay zekâ asistanına
# gönderdiği mesajı alır ve ai_service.py dosyasındaki
# yapay zekâ servisine yönlendirir.
#
# Dikkat:
# Burada doğrudan Groq API kodu YAZMIYORUZ.
# Çünkü hocanın istediği mimaride yapay zekâ işlemleri
# yalnızca ai_service.py dosyasında bulunmalıdır.
@api_bp.route("/sohbet", methods=["POST"])
def sohbet():

    # Kullanıcının gönderdiği JSON verisini okuyoruz.
    #
    # Örneğin Wix Studio bize şöyle bir veri gönderebilir:
    #
    # {
    #     "mesaj": "BLOCERA nedir?",
    #     "gecmis": []
    # }
    veri = request.get_json(silent=True) or {}

    # JSON içerisindeki "mesaj" alanını alıyoruz.
    #
    # Eğer mesaj alanı gönderilmemişse
    # varsayılan olarak boş metin kullanıyoruz.
    mesaj = veri.get("mesaj", "").strip()

    # Daha önce yapılmış konuşmalar varsa onları alıyoruz.
    #
    # Konuşma geçmişi gönderilmemişse boş liste kullanıyoruz.
    gecmis = veri.get("gecmis", [])

    # Kullanıcı boş mesaj göndermişse yapay zekâ servisini
    # gereksiz yere çağırmıyoruz.
    #
    # 400 HTTP durum kodu:
    # Kullanıcının gönderdiği istekte eksik veya hatalı veri
    # bulunduğunu ifade eder.
    if not mesaj:
        return jsonify({
            "basari": False,
            "hata": "Mesaj alanı boş bırakılamaz."
        }), 400

    try:

        # Burada daha önce hazırladığımız ai_service nesnesini çağırıyoruz.
        #
        # Gerçek Groq API işlemi routes.py içinde değil,
        # ai_service.py içerisinde gerçekleşecektir.
        cevap = ai_service.yanit_uret(
            mesaj=mesaj,
            gecmis=gecmis
        )

        # Yapay zekâdan başarılı cevap geldiyse
        # bunu JSON formatında kullanıcıya gönderiyoruz.
        return jsonify({
            "basari": True,
            "cevap": cevap
        })

    # ai_service.py içerisindeki yapay zekâ işlemi sırasında
    # bir hata oluşursa AIServiceError burada yakalanır.
    except AIServiceError as hata:

        # 503 HTTP durum kodu:
        # Sunucu çalışıyor fakat harici servis
        # geçici olarak kullanılamıyor anlamına gelir.
        return jsonify({
            "basari": False,
            "hata": str(hata)
        }), 503


# Bu API rotası, kullanıcının iletişim bilgilerini
# yeni bir müşteri adayı (lead) olarak kaydetmek için kullanılır.
#
# Wix Studio veya başka bir frontend bu adrese
# isim, telefon ve mesaj bilgilerini JSON olarak gönderebilir.
@api_bp.route("/leads", methods=["POST"])
def lead_kaydet():

    # Kullanıcının gönderdiği JSON verisini okuyoruz.
    #
    # Geçersiz veya boş bir JSON gelirse programın
    # doğrudan hata vermemesi için boş sözlük kullanıyoruz.
    veri = request.get_json(silent=True) or {}

    # JSON içerisindeki isim bilgisini alıyoruz.
    # strip() ile baştaki ve sondaki gereksiz boşlukları temizliyoruz.
    isim = veri.get("isim", "").strip()

    # Telefon bilgisini alıyoruz.
    telefon = veri.get("telefon", "").strip()

    # Mesaj alanı zorunlu değildir.
    # Gönderilmemişse boş metin kullanıyoruz.
    mesaj = veri.get("mesaj", "").strip()

    # İsim veya telefon eksikse kayıt işlemi yapmıyoruz.
    #
    # Hocanın istediği şekilde eksik veri durumunda
    # 400 Bad Request durum kodu döndürüyoruz.
    if not isim or not telefon:
        return jsonify({
            "basari": False,
            "hata": "İsim ve telefon alanları zorunludur."
        }), 400

    # Veritabanı işlemini burada SQL yazarak yapmıyoruz.
    #
    # database.py dosyasında daha önce oluşturduğumuz
    # lead_ekle() fonksiyonunu çağırıyoruz.
    lead_ekle(
        isim=isim,
        telefon=telefon,
        mesaj=mesaj
    )

    # Kayıt başarıyla oluşturulduğunda
    # JSON cevap ve 201 Created durum kodu döndürüyoruz.
    return jsonify({
        "basari": True,
        "mesaj": "Müşteri adayı başarıyla kaydedildi."
    }), 201    


# Bu API rotası, veritabanında kayıtlı olan
# bütün müşteri adaylarını listelemek için kullanılır.
#
# Yönetim paneli daha sonra bu adresi kullanarak
# kayıtlı lead bilgilerini ekranda gösterecektir.
@api_bp.route("/leads", methods=["GET"])
def leadleri_getir():

    # Burada doğrudan SQL sorgusu yazmıyoruz.
    #
    # database.py dosyasındaki tum_leadler() fonksiyonunu
    # çağırarak bütün müşteri adaylarını alıyoruz.
    leadler = tum_leadler()

    # Veritabanından gelen müşteri adaylarını
    # JSON formatında frontend'e gönderiyoruz.
    #
    # "basari": True
    # İşlemin başarılı olduğunu belirtir.
    #
    # "leadler":
    # Veritabanından gelen müşteri adaylarının listesidir.
    return jsonify({
        "basari": True,
        "leadler": leadler
    })