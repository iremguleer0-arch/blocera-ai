# SQLite veritabanı ile çalışabilmek için sqlite3 kütüphanesini içe aktarıyoruz
import sqlite3


# Veritabanına bağlanmak için kullanılan fonksiyon
def get_db():

    # blocera.db isimli SQLite veritabanı dosyasına bağlantı açıyoruz
    db = sqlite3.connect("blocera.db")

    # Veritabanından gelen satırlara sütun isimleriyle erişebilmemizi sağlar
    db.row_factory = sqlite3.Row

    # Oluşturduğumuz veritabanı bağlantısını geri döndürüyoruz
    return db


# Veritabanında gerekli tabloları ilk kez oluşturmak için kullanılan fonksiyon
def init_db(app):

    # Flask uygulamasının bağlamı içerisinde veritabanı işlemi yapıyoruz
    with app.app_context():

        # get_db() fonksiyonunu kullanarak veritabanına bağlanıyoruz
        db = get_db()

        # leads tablosu yoksa oluşturuyoruz
        db.execute("""
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                isim TEXT NOT NULL,
                telefon TEXT NOT NULL,
                mesaj TEXT,
                tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Yaptığımız değişiklikleri veritabanına kaydediyoruz
        db.commit()

        # Veritabanı bağlantısını kapatıyoruz
        db.close()

        # Bu fonksiyon, BLOCERA ile iletişime geçen yeni bir müşteri adayını
# "leads" tablosuna kaydetmek için kullanılır.
#
# Fonksiyon dışarıdan 3 bilgi alır:
# isim    -> müşteri adayının adı
# telefon -> müşteri adayının telefon numarası
# mesaj   -> müşterinin yazdığı mesaj (zorunlu değildir)
def lead_ekle(isim, telefon, mesaj=None):

    # Daha önce oluşturduğumuz get_db() fonksiyonunu çağırıyoruz.
    # Böylece blocera.db isimli SQLite veritabanına bağlantı açıyoruz.
    db = get_db()

    # INSERT INTO komutu veritabanına yeni bir kayıt eklemek için kullanılır.
    #
    # Burada kullanıcıdan gelen isim, telefon ve mesaj bilgilerini
    # SQL cümlesinin içine doğrudan yazmıyoruz.
    #
    # Bunun yerine "?" yer tutucularını kullanıyoruz.
    # Bu yöntem SQL Injection saldırılarına karşı daha güvenlidir
    # ve hocanın yönergesinde özellikle istenmektedir.
    db.execute(
        """
        INSERT INTO leads (isim, telefon, mesaj)
        VALUES (?, ?, ?)
        """,
        (isim, telefon, mesaj)
    )

    # INSERT işlemini veritabanına kalıcı olarak kaydediyoruz.
    # commit() yapılmazsa eklediğimiz kayıt kalıcı olmayabilir.
    db.commit()

    # Veritabanı işlemi tamamlandığı için açık bağlantıyı kapatıyoruz.
    db.close()


    # Bu fonksiyon, veritabanında kayıtlı olan bütün müşteri adaylarını
# listelemek için kullanılır.
#
# Yönetim panelinde müşteri adaylarını göstereceğimiz zaman
# routes.py dosyası bu fonksiyonu çağıracak.
def tum_leadler():

    # get_db() fonksiyonunu çağırarak
    # blocera.db SQLite veritabanına bağlantı açıyoruz.
    db = get_db()

    # SELECT komutu veritabanından veri okumak için kullanılır.
    #
    # Burada leads tablosundaki bütün kayıtları alıyoruz.
    #
    # ORDER BY tarih DESC:
    # Kayıtları tarihe göre sıralar.
    #
    # DESC = azalan sıralama anlamına gelir.
    # Böylece en yeni müşteri adayı listenin en üstünde görünür.
    kayitlar = db.execute("""
        SELECT id, isim, telefon, mesaj, tarih
        FROM leads
        ORDER BY tarih DESC, id DESC
    """).fetchall()

    # Veritabanından gelen kayıtlar sqlite3.Row tipindedir.
    # Bunları JSON olarak gönderebilmek için
    # her satırı Python sözlüğüne (dictionary) çeviriyoruz.
    lead_listesi = [dict(kayit) for kayit in kayitlar]

    # Veritabanından gerekli bilgileri aldığımız için
    # açık bağlantıyı kapatıyoruz.
    db.close()

    # Hazırladığımız müşteri adayı listesini
    # bu fonksiyonu çağıran yere geri gönderiyoruz.
    return lead_listesi