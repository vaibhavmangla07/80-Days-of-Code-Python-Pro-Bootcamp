from flask import Flask, render_template
import random
import datetime
import requests

app = Flask(__name__)


# ---------------- HOME PAGE ----------------
@app.route("/")
def home():
    random_number = random.randint(1, 10)
    current_year = datetime.datetime.now().year
    return render_template(
        "index.html",
        num=random_number,
        year=current_year
    )


# ---------------- GUESS PAGE ----------------
@app.route("/guess/<name>")
def guess(name):
    gender_url = f"https://api.genderize.io?name={name}"
    age_url = f"https://api.agify.io?name={name}"

    gender_response = requests.get(gender_url)
    age_response = requests.get(age_url)

    gender_data = gender_response.json()
    age_data = age_response.json()

    gender = gender_data.get("gender", "Unknown")
    age = age_data.get("age", "Unknown")

    return render_template(
        "guess.html",
        person_name=name,
        gender=gender,
        age=age
    )


# ---------------- BLOG PAGE ----------------
@app.route("/blog")
def get_blog():
    blog_url = "https://api.npoint.io/5abcca6f4e39b4955965"

    try:
        response = requests.get(blog_url, timeout=5)
        response.raise_for_status()
        all_posts = response.json()
    except Exception as e:
        print("API ERROR:", e)
        all_posts = []   # 👈 NEVER None

    return render_template("blog.html", posts=all_posts)



# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)
