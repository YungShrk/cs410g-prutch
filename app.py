from flask import Flask, redirect, url_for, render_template, request
from flask_dance.contrib.github import make_github_blueprint, github

def create_app():
    app = Flask(__name__)
    app.secret_key = "4199d85f133f24efeef018c32eb56ab2b2513cdf109fcc18"  # REPLACE with a strong random key
    blueprint = make_github_blueprint(
        client_id="Ov23lia1LKASrU3jWUj3",  # REPLACE
        client_secret="621b857fc3b0d3e13204458e0c430938aca34279",  # REPLACE
    )
    app.register_blueprint(blueprint, url_prefix="/login")

import random
import string

    # Fuzzing functionality for RAG
    def fuzz_query_rag(num_tests=100, max_length=100):
        for _ in range(num_tests):
            try:
                random_query = ''.join(random.choice(string.printable) for _ in range(random.randint(0, max_length)))
                result = query_rag(random_query)
                # Check for unexpected results here (e.g., empty strings, exceptions)
                if not result:
                    print(f"Potential issue with query: {random_query}. Empty result.")

            except Exception as e:
                print(f"Exception raised with query: {random_query}. Exception: {e}")


    def query_rag(query):
        # TODO: Implement your actual RAG query logic here
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

    return app

if __name__ == "__main__":
    fuzz_query_rag()  # Run the fuzzer before starting the app
    create_app().run(host='0.0.0.0', port=80, debug=True)
