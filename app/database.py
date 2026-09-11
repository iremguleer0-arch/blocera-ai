import sqlite3


DATABASE = "blocera.db"


def get_db():

    db = sqlite3.connect(DATABASE)

    db.row_factory = sqlite3.Row

    return db



def init_db(app):

    with app.app_context():

        db = get_db()

        db.execute("""
        CREATE TABLE IF NOT EXISTS leads (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            ad_soyad TEXT NOT NULL,

            firma_adi TEXT,

            telefon TEXT,

            e_posta TEXT,

            mesaj TEXT,

            durum TEXT DEFAULT 'Yeni',

            tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
        """)


        db.commit()

        db.close()



def lead_ekle(
    ad_soyad,
    firma_adi,
    telefon,
    e_posta,
    mesaj
):

    db = get_db()


    db.execute("""

    INSERT INTO leads
    (
        ad_soyad,
        firma_adi,
        telefon,
        e_posta,
        mesaj
    )

    VALUES
    (?, ?, ?, ?, ?)

    """,

    (
        ad_soyad,
        firma_adi,
        telefon,
        e_posta,
        mesaj
    ))


    db.commit()

    db.close()



def tum_leadler():

    db = get_db()


    kayitlar = db.execute("""

    SELECT *

    FROM leads

    ORDER BY id DESC

    """).fetchall()



    db.close()


    return [dict(x) for x in kayitlar]