from flask import Flask, render_template, request, abort
import smtplib
import requests

app = Flask(__name__)

posts = requests.get("https://api.npoint.io/c790b4d5cab58020d391").json()

OWN_EMAIL = "your_email@gmail.com"
OWN_PASSWORD = "your_app_password"

@app.route("/")
def get_all_posts():
    return render_template("index.html", all_posts=posts)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        data = request.form
        send_email(
            data["name"],
            data["email"],
            data["phone"],
            data["message"]
        )
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)

def send_email(name, email, phone, message):
    email_message = f"""Subject:New Message

Name: {name}
Email: {email}
Phone: {phone}
Message: {message}
"""
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(OWN_EMAIL, OWN_PASSWORD)
        connection.sendmail(OWN_EMAIL, OWN_EMAIL, email_message)

@app.route("/post/<int:index>")
def show_post(index):
    requested_post = next(
        (post for post in posts if post["id"] == index),
        None
    )
    if requested_post is None:
        abort(404)
    return render_template("post.html", post=requested_post)

if __name__ == "__main__":
    app.run(debug=True)
