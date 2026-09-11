from flask import Blueprint, render_template, request, jsonify

from app.database import lead_ekle, tum_leadler

from app.services.ai_service import ai_service, AIServiceError



# Sayfa rotaları
pages_bp = Blueprint("pages", __name__)


# API rotaları
api_bp = Blueprint("api", __name__)




# ==========================
# ANA SAYFA
# ==========================

@pages_bp.route("/")
def ana_sayfa():

    return render_template("index.html")




# ==========================
# YÖNETİM PANELİ
# ==========================

@pages_bp.route("/dashboard")
def dashboard():

    return render_template("dashboard.html")




# ==========================
# BLOCERA AI SOHBET API
# ==========================

@api_bp.route("/sohbet", methods=["POST"])
def sohbet():

    veri = request.get_json(silent=True) or {}


    mesaj = veri.get("mesaj", "").strip()

    gecmis = veri.get("gecmis", [])



    if not mesaj:

        return jsonify({

            "basari": False,

            "hata": "Mesaj alanı boş bırakılamaz."

        }), 400



    try:

        cevap = ai_service.yanit_uret(

            mesaj=mesaj,

            gecmis=gecmis

        )


        return jsonify({

            "basari": True,

            "cevap": cevap

        })



    except AIServiceError as hata:


        return jsonify({

            "basari": False,

            "hata": str(hata)

        }), 503





# ==========================
# İLETİŞİM FORMU KAYDETME
# ==========================

@api_bp.route("/leads", methods=["POST"])
def lead_kaydet():


    veri = request.get_json(silent=True) or {}



    ad_soyad = veri.get("ad_soyad", "").strip()

    firma_adi = veri.get("firma_adi", "").strip()

    telefon = veri.get("telefon", "").strip()

    e_posta = veri.get("e_posta", "").strip()

    mesaj = veri.get("mesaj", "").strip()




    if not ad_soyad or not telefon:


        return jsonify({

            "basari": False,

            "hata": "Ad soyad ve telefon zorunludur."

        }), 400





    lead_ekle(

        ad_soyad=ad_soyad,

        firma_adi=firma_adi,

        telefon=telefon,

        e_posta=e_posta,

        mesaj=mesaj

    )




    return jsonify({

        "basari": True,

        "mesaj": "İletişim talebi kaydedildi."

    }), 201






# ==========================
# TÜM TALEPLERİ GETİR
# YÖNETİM PANELİ İÇİN
# ==========================

@api_bp.route("/leads", methods=["GET"])
def leadleri_getir():


    leadler = tum_leadler()



    return jsonify({

        "basari": True,

        "leadler": leadler

    })