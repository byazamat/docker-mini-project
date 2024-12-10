from flask import Flask, render_template, request
import pg8000

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get the term from the form
        term = request.form["term"]
        return render_template("timetable.html", term=term, data=[], message="Loading timetable...")
    
    return render_template("index.html")

@app.route("/timetable", methods=["GET"])
def timetable():
    term = request.args.get('term')  # Get term from the query parameters
    if not term:
        return "term not provided", 400

    # Connect to the PostgreSQL database
    conn = pg8000.connect(
        user="student", 
        password="student_pass", 
        host="localhost", 
        port=5432, 
        database="student"
    )

    cur = conn.cursor()
    query = "SELECT * FROM Timetable WHERE term = %s;"
    cur.execute(query, (term,))
    rows = cur.fetchall()

    # Pass data to the template
    if rows:
        return render_template("timetable.html", term=term, data=rows, message="")
    else:
        return render_template("timetable.html", term=term, data=[], message="No data found for this term.")


if __name__ == "__main__":
    app.run(debug=True)
