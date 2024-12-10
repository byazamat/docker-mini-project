# docker_mini_project

Project to create simple webpage to check timetable use resources from docker

Guides

**1. Install Docker and Start PostgreSQL in Docker**

```bash
# Pull the latest PostgreSQL Docker image
docker pull postgres:latest

# Create a Docker container for the PostgreSQL database
docker run --name university-db -e POSTGRES_USER=student -e POSTGRES_PASSWORD=student_pass -d -p 5432:5432 postgres:latest

# Verify the container is running
docker ps

# Access the running PostgreSQL container
docker exec -it university-db psql -U student
```

### 2. **Set Up the PostgreSQL Database and Tables**

```sql
-- Connect to the PostgreSQL database (inside the container)
psql -U student

-- Create the Timetable table
CREATE TABLE Timetable (
    course_id SERIAL PRIMARY KEY,
    course_name VARCHAR(255),
    day VARCHAR(50),
    time VARCHAR(50),
    room VARCHAR(50),
    level INT
);

-- Insert Sample Data into the Timetable table
INSERT INTO Timetable (course_name, day, time, room, level) VALUES
('Computer Science 101', 'Monday', '9:00 AM', 'Room 101', 1),
('Operating Systems', 'Tuesday', '10:00 AM', 'Room 102', 1),
('Data Structures', 'Wednesday', '2:00 PM', 'Room 103', 2),
('Advanced Algorithms', 'Thursday', '11:00 AM', 'Room 104', 3),
('Machine Learning', 'Friday', '1:00 PM', 'Room 105', 2),
('Database Systems', 'Monday', '3:00 PM', 'Room 106', 3),
('Web Development', 'Tuesday', '11:00 AM', 'Room 107', 1),
('Networking', 'Thursday', '2:00 PM', 'Room 108', 2);
```

### 3. **Install Python and Flask Dependencies**

```bash
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use venv\Scripts\activate

# Install Flask and pg8000 for database connection
pip install flask pg8000
```

### 4. **Create Flask Application**

```python
from flask import Flask, render_template, request
import pg8000

app = Flask(__name__)

# Home route to get user input for level
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        level = request.form["level"]
        return render_template("timetable.html", level=level)
    return render_template("index.html")

# Timetable route to fetch timetable data based on the level
@app.route("/timetable", methods=["GET"])
def timetable():
    level = request.args.get("level")

    # Connect to PostgreSQL using pg8000
    conn = pg8000.connect(user="student", password="student_pass", host="localhost", port=5432, database="postgres")
    cur = conn.cursor()

    # Fetch timetable for the selected level
    query = f"SELECT * FROM Timetable WHERE level = {level};"
    cur.execute(query)
    rows = cur.fetchall()

    message = "No data found for this level." if not rows else None
    return render_template("timetable.html", data=rows, message=message)

# Run Flask app
if __name__ == "__main__":
    app.run(debug=True)
```

### 5. **HTML Templates for Flask**

#### **`index.html` (Form for term select)**

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>University Timetable</title>
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
      href="https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap"
      rel="stylesheet"
    />
    <link
      rel="stylesheet"
      href="{{ url_for('static', filename='styles.css') }}"
    />
  </head>
  <body>
    <main>
      <h1>University Timetable</h1>

      <form action="/timetable" method="GET">
        <label for="term">Select term:</label>
        <select name="term" id="term">
          <option value="Spring">Spring</option>
          <option value="Fall">Fall</option>
        </select>
        <button type="submit">Submit</button>
      </form>
    </main>
  </body>
</html>
```

#### **`timetable.html` (Displaying Timetable)**

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Timetable for term: {{ term }}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
      href="https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap"
      rel="stylesheet"
    />
    <link
      rel="stylesheet"
      href="{{ url_for('static', filename='styles.css') }}"
    />
  </head>
  <body>
    <main>
      <h1>Timetable for term: {{ term }}</h1>
      {% if data %}
      <table border="1">
        <thead>
          <tr>
            <th>Course ID</th>
            <th>Hours</th>
            <th>Name</th>
            <th>Instructor</th>
            <th>Campus</th>
            <th>Building</th>
            <th>Terms</th>
          </tr>
        </thead>
        <tbody>
          {% for row in data %}
          <tr>
            <td>{{ row[0] }}</td>
            <td>{{ row[1] }}</td>
            <td>{{ row[2] }}</td>
            <td>{{ row[3] }}</td>
            <td>{{ row[4] }}</td>
            <td>{{ row[5] }}</td>
            <td>{{ row[10] }}</td>
          </tr>
          {% endfor %}
        </tbody>
      </table>
      {% else %}
      <p>{{ message }}</p>
      {% endif %}

      <a href="/">Go back</a>
    </main>
  </body>
</html>
```

#### **`styles.css` (Styles)**

```css
* {
  left: 0;
  top: 0;
  margin: 0;
  padding: 0;
  color: var(--text);
  font-family: "Montserrat", serif;
  font-optical-sizing: auto;
  font-weight: 500;
  font-style: normal;
  transition: 0.3s ease;
}

body {
  display: grid;
  width: 100%;
  height: 100%;
  justify-items: center;
  background-color: var(--bg);

  --bg: #2b303a;
  --secondary: #232736;
  --text: #eee5e9;
  --primary: #d64933;
  --stroke: #32394f;
  --destructive: #d64933;
}

main {
  display: grid;
  gap: 24px;
  grid-auto-rows: max-content;
  width: 100%;
  max-width: 1440px;
  padding: 32px;
}

h1 {
  font-size: 32px;
  font-weight: 700;
  color: var(--primary);
}

form {
  display: grid;
  gap: 16px;
  grid-auto-rows: max-content;
}

select {
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  width: 100%;
  height: 48px;
  background-color: var(--secondary);
  padding-left: 24px;
  padding-right: 48px;
  background-image: url("data:image/svg+xml;utf8,<svg fill='white' height='24' viewBox='0 0 24 24' width='24' xmlns='http://www.w3.org/2000/svg'><path d='M7 10l5 5 5-5z'/><path d='M0 0h24v24H0z' fill='none'/></svg>");
  background-size: 24px;
  background-repeat: no-repeat;
  background-position: right 8px center;
  font-size: 16px;
  color: var(--text);
  border: 1px solid transparent;
  border-radius: 8px;
}

/* Дополнительные стили для hover или focus (опционально) */
select:hover,
select:focus {
  border-color: var(--stroke);
  outline: none;
}

button,
a {
  width: 100%;
  height: 48px;
  background: var(--primary);
  color: var(--bg);
  font-size: 16px;
  border-radius: 8px;

  outline: none;
  border: 1px solid var(--primary);
}

button:hover,
a:hover {
  border: 1px solid var(--stroke);
}

a {
  display: flex;
  justify-content: center;
  align-items: center;
  text-decoration: none;
}

table {
  border-spacing: 0;
}

th,
td {
  height: 48px;
  padding: 0 16px;
  border: 1px solid var(--primary);
}

th {
  color: var(--primary);
}

table tr:first-child th:first-child {
  border-top-left-radius: 8px;
}
table tr:first-child th:last-child {
  border-top-right-radius: 8px;
}
table tr:last-child td:first-child {
  border-bottom-left-radius: 8px;
}
table tr:last-child td:last-child {
  border-bottom-right-radius: 8px;
}
```

### 6. **Running the Flask Application**

```bash
# Make sure you're in the directory with your Flask app
# Run the Flask app
python app.py
```

### 7. **Accessing the Application**

- Navigate to `http://127.0.0.1:5000/` in your web browser to see the application in action.

### 8. **Stop the Docker Container**

```bash
# Stop the PostgreSQL Docker container after you're done
docker stop university-db
```

---

These are the commands and steps you would use to deploy and run this project. You can adapt or extend the project as needed based on additional requirements.
