 Elimizde bir defter olduğunu düşünelim. Bu deftere isim ve e-posta yazarak kişi kaydedebiliyorsunuz. İstediğiniz kişiyi bulabiliyorsunuz, bilgilerini değiştirebiliyorsunuz ya da silebiliyorsunuz.

  Burada tam olarak bunu yaptım — ama bu defteri internet üzerinden çalışır hale getirdim.

  Yani başka bir uygulama (mesela bir web sitesi veya telefon uygulaması) bize şunu diyebilir:

   - "Bana tüm kişilerin listesini ver."
   - "Şu kişiyi ekle."
   - "Şunun adını güncelle."
   - "Şu kişiyi sil."

  Buna göre cevap veririz.

  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

  Kullandığımız araçlar ne işe yarıyor?

   - Python → Talimatları yazdığımız dil.
   - Flask → "İnternet üzerinden gelen istekleri dinle" dememizi sağlıyor. Kapıda bekleyen bir görevli gibi.
   - SQLite → Kişilerin kaydedildiği defter. Bilgisayarda küçük bir dosya olarak duruyor.

  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

  Kısacası: "İnternetten erişilebilen, kişi bilgilerini saklayan bir sistem" yaptık. Bu da = API.


## Satır satır kodu inceleyelim

```python
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
```

```bash Flask ``` → Sunucuyu kuran ana araç

```bash request ``` → "Şu kullanıcıyı ekle" gibi gelen istekleri okur

```bash jsonify ``` → Cevabı JSON formatına çevirir (bu tarayıcının anlayacağı dildir)

```bash SQLAlchemy ``` → Veritabanıyla konuşmamızı sağlar
