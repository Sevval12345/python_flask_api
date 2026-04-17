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

**1. Kütüphaneleri içe aktarma**

```python
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
```

```bash Flask ``` → Sunucuyu kuran ana araç

```bash request ``` → "Şu kullanıcıyı ekle" gibi gelen istekleri okur

```bash jsonify ``` → Cevabı JSON formatına çevirir (bu tarayıcının anlayacağı dildir)

```bash SQLAlchemy ``` → Veritabanıyla konuşmamızı sağlar

**2. Uygulamayı kurma**

```python
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
```

```bash app = Flask(__name__) ``` → "Bir Flask uygulaması başlat" demek. ```bash app ``` artık bizim sunucumuzun adı.

```bash SQLALCHEMY_DATABASE_URI ``` → Veritabanının nerede olduğunu söylüyoruz. ```bash sqlite:///users.db ``` → "Aynı klasörde ```bash users.db ``` adında bir dosya kullan" demek.

```bash TRACK_MODIFICATIONS ``` = False → Gereksiz uyarıları kapat. Performans için.

**3. Veritabanını bağlama**

```python
db = SQLAlchemy(app)
```

Flask uygulamasını (```bash app ```) veritabanı aracına (```bash SQLAlchemy```) bağlıyoruz. Artık ```bash db ``` diyerek veritabanına erişebiliriz.

**4. Kullanıcı tablosunu tanımla**

```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
```

Bu, veritabanındaki tablonun şablonudur. Örneğin:


| id | name | email | 
| -------- | -------- | -------- |
| 1 | Sevval | sevval@test.com |
| 2 | Zeynep | zeynep@test.com |
