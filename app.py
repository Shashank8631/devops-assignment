from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import os

app = Flask(__name__)
@app.route("/")
def home():
    return "Flask API Running ✅ Use /health to check status"


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///items.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

# ✅ New initialization
with app.app_context():
    db.create_all()

@app.route("/health")
def health():
    return {"status": "ok"}

@app.route("/items", methods=["POST"])
def create_item():
    data = request.json
    item = Item(name=data["name"], description=data.get("description"))
    db.session.add(item)
    db.session.commit()
    return {"message": "Item created"}, 201

@app.route("/items", methods=["GET"])
def get_items():
    items = Item.query.all()
    return jsonify([{"id": i.id, "name": i.name, "description": i.description} for i in items])

@app.route("/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = Item.query.get(item_id)
    return {"id": item.id, "name": item.name, "description": item.description}

@app.route("/items/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    data = request.json
    item = Item.query.get(item_id)
    item.name = data["name"]
    item.description = data.get("description")
    db.session.commit()
    return {"message": "Item updated"}

@app.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    item = Item.query.get(item_id)
    db.session.delete(item)
    db.session.commit()
    return {"message": "Item deleted"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
