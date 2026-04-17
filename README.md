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

```bash primary_key=True ```→ Her kullanıcıya otomatik sıra numarası ver (1, 2, 3...)
```bash nullable=False ```→ Bu alan boş bırakılamaz, zorunlu
```bash unique=True ```→ Aynı email iki kez kayıt edilemez

**5. to_dict fonksiyonu**

```bash
def to_dict(self):
    return {"id": self.id, "name": self.name, "email": self.email}
```

Veritabanından gelen kullanıcıyı tarayıcının anlayacağı formata çeviriyor. Yani şunu üretiyor:

```json
{"id": 1, "name": "Sevval", "email": "sevval@test.com"}
```

**6. tabloyu oluştur**

```bash
with app.app_context():
    db.create_all()
```

"Uygulama başlarken, eğer ```bash users.db ``` dosyası yoksa oluştur" demek. Zaten varsa dokunma.

**7. Tüm kullanıcıları listele (GET)**

```bash
@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users])
```

```bash @app.route("/users", methods=["GET"]) ``` → Biri ```bash http://127.0.0.1:5000/users ``` adresine girince bu fonksiyonu çalıştır

```bash User.query.all() ``` → Veritabanındaki tüm kullanıcıları getir

```bash [u.to_dict() for u in users] ``` → Her kullanıcıyı JSON'a çevir ve liste yap

**8. Tek kullanıcıyı getir (GET)**

```bash
@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = db.get_or_404(User, user_id)
    return jsonify(user.to_dict())
```

```bash  <int:user_id> ``` → URL'deki sayıyı al. Örn: ```bash /users/3 ``` → ```bash user_id = 3 ``` 

```bash get_or_404 ``` → Kullanıcı varsa getir, yoksa "bulunamadı" hatası ver

**9. Yeni kullanıcı ekle (POST)**

```bash
@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data or not data.get("name") or not data.get("email"):
        return jsonify({"error": "name ve email zorunludur"}), 400

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Bu email zaten kullanımda"}), 409

    user = User(name=data["name"], email=data["email"])
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201
```

```bash request.get_json() ``` → Gelen isteğin içindeki veriyi oku (```bash{"name": "Sevval", ...}```)

İlk ```bash if ``` → Name veya email boşsa hata ver (```bash 400 ``` = "yanlış istek")

İkinci ```bash if ``` → Aynı email zaten varsa hata ver (```bash 409 ``` = "çakışma")

```bash db.session.add() ``` → Yeni kullanıcıyı veritabanına eklemek için hazırla

```bash db.session.commit() ``` → Kaydet! (commit = "tamam, yaz artık")

```bash 201 ``` → "Başarıyla oluşturuldu" anlamına gelen kod

**10. Kullanıcıyı güncelle (PUT)**

```bash
@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = db.get_or_404(User, user_id)
    data = request.get_json()

    if "name" in data:
        user.name = data["name"]
    if "email" in data:
        if User.query.filter(...).first():
            return jsonify({"error": "Bu email zaten kullanımda"}), 409
        user.email = data["email"]

    db.session.commit()
    return jsonify(user.to_dict())
```

Önce kullanıcıyı bul, sonra gelen verideki alanları güncelle

Sadece gönderilen alanları günceller — name göndermediysen name'e dokunmaz

Yine ```bash commit() ``` ile kaydeder

**11. Kullanıcıyı sil (DELETE)**

```bash
@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = db.get_or_404(User, user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": f"Kullanıcı {user_id} silindi"})
```

Bul → Silmek için işaretle → Kaydet

**12. Sunucuyu Başlat**

```bash
if __name__ == "__main__":
    app.run(debug=True)
```

```bash if __name__ == "__main__" ``` → "Bu dosya direkt çalıştırılıyorsa" demek. Başka bir dosya import ederse çalışmaz.

**Kısaca**
Kütüphaneler → Uygulama kurulumu → Tablo tanımı → 5 endpoint (GET/POST/PUT/DELETE) → Sunucu başlat
```bash debug=True ``` → Kodda değişiklik yapınca sunucu otomatik yeniden başlar. Geliştirme kolaylığı.
