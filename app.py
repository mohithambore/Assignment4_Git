from flask import Flask, request, jsonify, render_template, redirect, url_for
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["assignment_db"]
todo_collection = db["todo_items"]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api")
def api():
    try:
        with open("data.txt", "r") as file:
            data_list = [line.strip() for line in file.readlines()]
        return jsonify(data_list)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name")
    email = request.form.get("email")

    try:
        client = MongoClient(MONGO_URI)
        db = client["assignment_db"]
        collection = db["students"]

        collection.insert_one({
            "name": name,
            "email": email
        })

        return redirect(url_for("success"))
    except Exception as e:
        return render_template("index.html", error=str(e))

@app.route("/success")
def success():
    return render_template("success.html")

@app.route("/submittodoitem", methods=["POST"])
def submit_todo_item():
    item_name = request.form.get("itemName")
    item_description = request.form.get("itemDescription")

    todo_data = {
        "itemName": item_name,
        "itemDescription": item_description
    }

    todo_collection.insert_one(todo_data)

    return "To-Do item submitted successfully!"

@app.route("/todo")
def todo():
    return render_template("todo.html")

if __name__ == "__main__":
    app.run(debug=True)