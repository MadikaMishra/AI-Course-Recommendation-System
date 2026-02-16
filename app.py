from flask import Flask, render_template, request
from recommendation_model import recommend_courses
import csv

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    recommendations = None
    if request.method == "POST":
        interest = request.form["interest"]
        recommendations = recommend_courses(interest).to_dict(orient="records")
    return render_template("index.html", recommendations=recommendations)


@app.route('/courses')
def courses():
    courses_list = []
    try:
        with open(r'c:/Users/madika mishra/PycharmProjects/FlaskProject/data/courses.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                courses_list.append({
                    'id': row['course_id'],
                    'name': row['course_name'],
                    'category': row['category'],
                    'difficulty': row['difficulty'],
                    'description': row['description'],
                    'image_url': ''
                })
    except Exception as e:
        return f"Error: {e}"

    # Get unique categories for filter dropdown
    categories = sorted(set(course['category'] for course in courses_list))

    # Get search and category filter from query params
    search = request.args.get('search', '').strip().lower()
    category = request.args.get('category', '').strip()

    # Filter courses
    filtered_courses = []
    for course in courses_list:
        if search and search not in course['name'].lower() and search not in course['description'].lower():
            continue
        if category and course['category'] != category:
            continue
        filtered_courses.append(course)

    return render_template('courses.html', courses=filtered_courses, categories=categories)
@app.route('/about')
def about():
    return render_template('about.html')

@app.route("/contact", methods=["GET", "POST"])
def contact():
    submitted = False
    if request.method == "POST":
        # In real app, you’d store this or send via email
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]
        submitted = True
    return render_template("contact.html", submitted=submitted)

if __name__ == "__main__":
    app.run(debug=True)
