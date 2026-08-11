from flask import Flask, render_template, request
import os
from pypdf import PdfReader

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# -----------------------------
# Job database
# -----------------------------

JOBS = {
    "Python Developer": [
        "Python",
        "Git",
        "SQL",
        "Flask"
    ],

    "Web Developer": [
        "HTML",
        "CSS",
        "JavaScript"
    ],

    "Backend Developer": [
        "Python",
        "SQL",
        "Flask",
        "Git"
    ],

    "Frontend Developer": [
        "HTML",
        "CSS",
        "JavaScript",
        "React"
    ],

    "Data Scientist": [
        "Python",
        "SQL",
        "Data Science",
        "Machine Learning"
    ],

    "Machine Learning Engineer": [
        "Python",
        "Machine Learning",
        "Data Science",
        "SQL"
    ],

    "AI Engineer": [
        "Python",
        "Machine Learning",
        "Artificial Intelligence"
    ],

    "Software Developer": [
        "Python",
        "Java",
        "C++",
        "SQL",
        "Git"
    ]
}


# -----------------------------
# Extract PDF text
# -----------------------------

def extract_text(filepath):

    reader = PdfReader(filepath)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


# -----------------------------
# Find skills
# -----------------------------

def find_skills(text):

    skills = [
        "Python",
        "Java",
        "C",
        "C++",
        "HTML",
        "CSS",
        "JavaScript",
        "SQL",
        "Flask",
        "Django",
        "Git",
        "GitHub",
        "Machine Learning",
        "Artificial Intelligence",
        "Data Science",
        "React",
        "Node.js",
        "AWS",
        "Docker"
    ]

    found_skills = []

    text = text.lower()

    for skill in skills:

        if skill.lower() in text:

            found_skills.append(skill)

    return found_skills


# -----------------------------
# Job recommendation
# -----------------------------

def recommend_jobs(found_skills):

    recommendations = []

    for job, required_skills in JOBS.items():

        matched = []

        for skill in required_skills:

            if skill.lower() in [
                s.lower() for s in found_skills
            ]:

                matched.append(skill)

        percentage = int(
            (len(matched) / len(required_skills)) * 100
        )

        recommendations.append({
            "job": job,
            "percentage": percentage,
            "matched": matched
        })

    # Highest match first
    recommendations.sort(
        key=lambda x: x["percentage"],
        reverse=True
    )

    return recommendations


# -----------------------------
# Home page
# -----------------------------

@app.route("/")
def home():

    return render_template("index.html")


# -----------------------------
# Upload resume
# -----------------------------

@app.route("/upload", methods=["POST"])
def upload():

    file = request.files.get("resume")

    if not file or file.filename == "":

        return "Please select a PDF resume."

    if not file.filename.lower().endswith(".pdf"):

        return "Only PDF files are allowed."

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        file.filename
    )

    file.save(filepath)

    # Extract text
    text = extract_text(filepath)

    # Find skills
    found_skills = find_skills(text)

    # Job recommendations
    recommendations = recommend_jobs(found_skills)

    # Resume score
    score = min(
        int((len(found_skills) / 20) * 100),
        100
    )

    return render_template(
        "result.html",
        filename=file.filename,
        score=score,
        skills=found_skills,
        recommendations=recommendations
    )


# -----------------------------
# Start Flask
# -----------------------------

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )