from flask import Flask, redirect, url_for, render_template, request
from flask_dance.contrib.github import make_github_blueprint, github

app = Flask(__name__)
app.secret_key = "4199d85f133f24efeef018c32eb56ab2b2513cdf109fcc18"  # REPLACE with a strong random key
blueprint = make_github_blueprint(
    client_id="Ov23lia1LKASrU3jWUj3",  # REPLACE
    client_secret="621b857fc3b0d3e13204458e0c430938aca34279",  # REPLACE
)
app.register_blueprint(blueprint, url_prefix="/login")

# Placeholder for your RAG functionality
def query_rag(query):
    # TODO: Implement your RAG query logic here
    # This should load relevant documents, process the query,
    # and return the answer.
    return "RAG query result for: " + query


@app.route("/", methods=["GET", "POST"])
def index():
    if not github.authorized:
        return redirect(url_for("github.login"))
    resp = github.get("/user")
    assert resp.ok

    if request.method == "POST":
        query = request.form.get("query")
        result = query_rag(query)
        return render_template("index.html", query=query, result=result, github_username=resp.json()["login"])
    return render_template("index.html", github_username=resp.json()["login"])



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
