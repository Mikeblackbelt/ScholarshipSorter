from flask import Flask, render_template, request
from chatloop import chatLoop

app = Flask(__name__)
messages = []

@app.route("/", methods=["GET", "POST"])
def index():
    response = ""
    if request.method == "POST":
        user_input = request.form["user_input"]
        messages.append(
            {
                "role": "user",
                "content": user_input
            }
        )
        response = chatLoop(user_input, messageHistory=messages)
    return render_template("index.html", response=response)

if __name__ == "__main__":
    app.run(debug=True)
