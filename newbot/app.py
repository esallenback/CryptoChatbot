from flask import Flask, url_for, render_template, redirect, request, flash
from firstbot import *

app = Flask(__name__)
app.secret_key = "ewrqoiuckjnv"
theBot = initializeBot(False, "chatbot-development12.tsv")

@app.route("/", methods=["POST", "GET"])
def home():
    if request.method=="POST":
        userIn = request.form["response"]
        flash("Cryptocurrent: " + getResponse(theBot, userIn).text)

        return render_template("index.html")
    else:
        return render_template("index.html")

if __name__ == "__main__":
    
    app.run()