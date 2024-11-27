from flask import Flask, redirect, url_for, render_template, request
from flask_dance.contrib.github import make_github_blueprint, github

import random
import string

def create_app():
    app = Flask(__name__)
    app.secret_key = "4199d85f133f24efeef018c32eb56ab2b2513cdf109fcc18"  # REPLACE with a strong random key
    blueprint = make_github_blueprint(
        client_id="Ov23lia1LKASrU3jWUj3",  # REPLACE
        client_secret="621b857fc3b0d3e13204458e0c430938aca34279",  # REPLACE
    )
    app.register_blueprint(blueprint, url_prefix="/login")

    def query_rag(query):
        # TODO: Implement your actual RAG query logic here
        return "RAG query result for: " + query

    def fuzz_query_rag(app_instance, num_tests=100, max_length=100):
        for _ in range(num_tests):
            try:
                random_query = ''.join(random.choice(string.printable) for _ in range(random.randint(0, max_length)))
                result = app_instance.test_client().post("/", data={"query": random_query}).data.decode("utf-8")
                if "RAG query result for:" not in result:
                    print(f"Potential issue with query: {random_query}. Unexpected result: {result}")

            except Exception as e:
                print(f"Exception raised with query: {random_query}. Exception: {e}")

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

    fuzz_query_rag(app, num_tests=10, max_length=20)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', port=80, debug=True)
