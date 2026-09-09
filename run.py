# BLOCERA Flask uygulamasını Render ve yerel bilgisayarda başlatır.

import os

# app klasöründeki create_app() fonksiyonunu çağırıyoruz.
from app import create_app


# Flask uygulamasını oluşturuyoruz.
app = create_app()


# run.py doğrudan çalıştırıldığında bu bölüm devreye girer.
if __name__ == "__main__":

    # Render kendi PORT bilgisini verir.
    # Bilgisayarında çalıştırırsan varsayılan olarak 5000 kullanır.
    port = int(os.environ.get("PORT", 5000))

    # 0.0.0.0 kullanmamızın sebebi:
    # Render uygulamaya internetten erişebilmek için bunu ister.
    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )