from flask import Flask, render_template, request
import getRequirements as getRequirements
from chatloop import chatLoop

app = Flask(__name__)
messages = []

@app.route("/", methods=["GET", "POST"])
def index():
    response = ""
    if request.method == "GET":
        print("GET request received")
    if request.method == "POST":
        print("Form submitted")
        description = request.form["user_input"]
        """GPA = request.form["GPA"] or None
        Race_Req = request.form['Race Requirement'] or None
        Gender_Req = request.form['Gender Requirement'] or None
        Income_Max = request.form['Income Max'] or None
        Income_Min = request.form['Income Min'] or None
        Income_Range = [Income_Min or 0,Income_Max or 9 * 10**10]"""

        response = getRequirements.rank_students(
            getRequirements.gdf,
            description
        ).to_dict(orient='records')
        print(response)
        #response = chatLoop(user_input, messageHistory=messages)
    return render_template("index.html", response=response)

@app.route("/student_search", methods=["GET", "POST"])
def student_search():   
    response = ""
    if request.method == "POST":
        user_input = request.form["user_input"]
        response = (getRequirements.filter_students(getRequirements.get_filters(user_input))).to_dict(orient='records')
        #response = response.to_html(classes='table table-striped', index=False)
        print(response)
    return render_template("student_search.html", response=response)

if __name__ == "__main__":
    app.run(debug=True)
