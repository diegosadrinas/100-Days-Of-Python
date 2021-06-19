from flask import Flask, render_template, url_for
import requests

app = Flask(__name__)

posts_url = "https://api.npoint.io/e42b353ee387383898c7"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 "
                  "(KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Accept-Language": "es-xl",
    "Accept-Encoding": "gzip, deflate",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}
response = requests.get(url=posts_url, headers=headers)
response.raise_for_status()
all_posts = response.json()
print(all_posts)


@app.route("/")
def goto_home():
    return render_template("index.html", posts=all_posts)


@app.route("/about")
def goto_about():
    return render_template("about.html")


@app.route("/contact")
def goto_contact():
    return render_template("contact.html")


@app.route("/post/<int:post_id>")
def goto_post(post_id):
    requested_post = None
    for post in all_posts:
        if post["id"] == post_id:
            requested_post = post
    return render_template("post.html", post=requested_post)


if __name__ == "__main__":
    app.run(debug=True)