from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy  # Requires: pip install flask-sqlalchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "email": self.email}


with app.app_context():
    db.create_all()


# Tüm kullanıcıları listele
@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users])


# Belirli bir kullanıcıyı getir
@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = db.get_or_404(User, user_id)
    return jsonify(user.to_dict())


# Yeni kullanıcı oluştur
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


# Kullanıcıyı güncelle
@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = db.get_or_404(User, user_id)
    data = request.get_json()

    if "name" in data:
        user.name = data["name"]
    if "email" in data:
        if User.query.filter(User.email == data["email"], User.id != user_id).first():
            return jsonify({"error": "Bu email zaten kullanımda"}), 409
        user.email = data["email"]

    db.session.commit()
    return jsonify(user.to_dict())


# Kullanıcıyı sil
@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = db.get_or_404(User, user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": f"Kullanıcı {user_id} silindi"})


if __name__ == "__main__":
    app.run(debug=True)
