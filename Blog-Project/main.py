from flask import Flask, render_template, request
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


@app.route("/")
def goto_home():
    return render_template("index.html", posts=all_posts)


@app.route("/about")
def goto_about():
    return render_template("about.html")


@app.route("/contact", methods=['GET', 'POST'])
def goto_contact():
    return render_template("contact.html")


@app.route("/post/<int:post_id>")
def goto_post(post_id):
    requested_post = None
    for post in all_posts:
        if post["id"] == post_id:
            requested_post = post
    return render_template("post.html", post=requested_post)


@app.route('/form_entry', methods=['GET', 'POST'])
def received_data():
    print(request.form['name'], request.form['email'], request.form['phone'], request.form['message'])
    return "<h1>Your message has been successfully submitted!</h1>"


if __name__ == "__main__":
    app.run(debug=True)