from flask import Flask, request, render_template, redirect, url_for, session, send_from_directory
from datetime import datetime
import os

app = Flask(__name__)

# সিক্রেট কী এবং আপলোড ফোল্ডার সেটআপ
app.secret_key = "your_secret_key"
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# পাসওয়ার্ড
PASSWORD = "mypassword"

# আপলোড করা ফাইল, টেক্সট এবং নাম সেভ করার জন্য
posts = []

@app.route("/", methods=["GET", "POST"])
def login():
    """লগইন পৃষ্ঠা"""
    if request.method == "POST":
        if request.form["password"] == PASSWORD:
            session["logged_in"] = True
            session["name"] = request.form["name"]
            return redirect(url_for("upload"))
        else:
            return render_template("login.html", error="Incorrect password! Please try again.")
    return render_template("login.html")

@app.route("/upload", methods=["GET", "POST"])
def upload():
    """ফাইল আপলোড এবং টেক্সট যুক্ত করার পৃষ্ঠা"""
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    if request.method == "POST":
        files = request.files.getlist("files")
        text = request.form.get("text")
        name = session.get("name", "Anonymous")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        uploaded_files = []

        for file in files:
            if file:
                file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
                file.save(file_path)
                uploaded_files.append(url_for("uploaded_file", filename=file.filename))

        if uploaded_files or text:
            posts.append({"files": uploaded_files, "text": text, "name": name, "timestamp": timestamp})

    return render_template("upload.html", posts=posts)

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    """আপলোড হওয়া ফাইল দেখানোর জন্য"""
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

@app.route("/logout")
def logout():
    """লগআউট ফাংশন"""
    session.pop("logged_in", None)
    session.pop("name", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
