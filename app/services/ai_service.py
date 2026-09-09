# ==========================================================
# BLOCERA AI SERVICE
# Bu dosya yapay zeka bağlantısını yönetir.
#
# Görevleri:
# 1- Groq API bağlantısı kurmak
# 2- BLOCERA bilgi bankasını okumak
# 3- Kullanıcı mesajını AI modeline göndermek
# 4- AI cevabını geri döndürmek
# ==========================================================


# Dış API'lere HTTP isteği göndermek için kullanılır.
import requests


# Dosya işlemleri için kullanılır.
import os


# config.py içindeki ayarları alıyoruz.
#
# Buradan:
# - API anahtarı
# - AI ayarları
# - şirket tanımı
# okunur.
from config import Config



# Yapay zeka sırasında oluşabilecek özel hataları
# ayırmak için kendi hata sınıfımızı oluşturuyoruz.
class AIServiceError(Exception):
    pass





class AIService:


    # ------------------------------------------------------
    # Sistem başlarken çalışan ana bölüm
    # ------------------------------------------------------
    def __init__(self):


        # Groq API anahtarını alıyoruz.
        self.api_key = Config.GROQ_API_KEY


        # Kullanılan AI sağlayıcısı
        self.provider = Config.AI_PROVIDER


        # Groq API adresi
        self.api_url = (
            "https://api.groq.com/openai/v1/chat/completions"
        )





    # ------------------------------------------------------
    # BLOCERA bilgi bankasını okuyan fonksiyon
    #
    # app/knowledge/blocera.txt dosyasını açar.
    #
    # Buraya şirket bilgileri yazılacak.
    # ------------------------------------------------------

    def bilgi_getir(self):


        dosya_yolu = "app/knowledge/blocera.txt"


        try:

            with open(
                dosya_yolu,
                "r",
                encoding="utf-8"
            ) as dosya:


                return dosya.read()



        except Exception:


            return ""







    # ------------------------------------------------------
    # AI karakterini belirleyen sistem mesajı
    #
    # Burada AI'ye kim olduğunu söylüyoruz.
    # ------------------------------------------------------

    def _sistem_talimati(self):


        # Önce BLOCERA bilgi bankasını okuyoruz.

        bilgi = self.bilgi_getir()



        return f"""

Sen BLOCERA şirketinin yapay zeka asistanısın.


Aşağıdaki şirket bilgilerini temel alarak cevap ver.


BLOCERA BİLGİ BANKASI:

{bilgi}


Kurallar:

- Türkçe cevap ver.
- Profesyonel bir şirket temsilcisi gibi konuş.
- Bilmediğin bilgileri uydurma.
- BLOCERA hakkında sadece verilen bilgileri kullan.
- Blockchain, kripto para veya NFT bağlantısı kurma.


"""








    # ------------------------------------------------------
    # Kullanıcı mesajını AI'ye gönderen ana fonksiyon
    # ------------------------------------------------------

    def yanit_uret(
            self,
            mesaj,
            gecmis=None
    ):



        # Eğer geçmiş konuşma yoksa boş liste oluştur.

        if gecmis is None:

            gecmis = []





        # API anahtarı yoksa işlem yapma.

        if not self.api_key:


            return (
                "API anahtarı bulunamadı."
            )





        # AI'ye gönderilecek mesaj listesi

        messages = [


            {


                "role": "system",


                "content": self._sistem_talimati()


            }


        ]





        # Eski konuşmaları ekliyoruz.

        messages.extend(
            gecmis
        )





        # Kullanıcının yeni mesajını ekliyoruz.

        messages.append(

            {

                "role": "user",

                "content": mesaj

            }

        )






        try:



            # API bağlantı bilgileri

            headers = {


                "Authorization":
                f"Bearer {self.api_key}",


                "Content-Type":
                "application/json"


            }





            # Groq'a gönderilecek veri

            payload = {


                # Güncel Groq modeli

                "model":
                "openai/gpt-oss-20b",



                "messages":
                messages


            }





            # API çağrısı

            response = requests.post(


                self.api_url,


                headers=headers,


                json=payload,


                timeout=30


            )





            # Hata kontrolü

            response.raise_for_status()





            # JSON cevabını al

            data = response.json()





            # AI cevabını döndür

            return (
                data["choices"][0]
                ["message"]
                ["content"]
            )





        except requests.RequestException as hata:


            raise AIServiceError(

                f"Groq bağlantı hatası: {hata}"

            )





        except (
            KeyError,
            IndexError,
            ValueError
        ) as hata:



            raise AIServiceError(

                f"AI cevabı okunamadı: {hata}"

            )







# ------------------------------------------------------
# Tek bir AIService nesnesi oluşturuyoruz.
#
# Flask içinde bunu tekrar tekrar oluşturmayacağız.
# ------------------------------------------------------

ai_service = AIService()