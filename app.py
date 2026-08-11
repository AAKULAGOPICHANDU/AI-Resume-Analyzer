from flask import Flask, render_template, request
import os
from pypdf import PdfReader

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():

    file = request.files.get("resume")

    if not file or file.filename == "":
        return "Please select a PDF file."

    if not file.filename.lower().endswith(".pdf"):
        return "Only PDF files are allowed."

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        file.filename
    )

    file.save(filepath)

    # -----------------------------
    # Extract text from PDF
    # -----------------------------

    reader = PdfReader(filepath)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    text_lower = text.lower()

    # -----------------------------
    # Skills
    # -----------------------------

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
        "Data Science",
        "React",
        "Node.js",
        "AWS",
        "Docker"
    ]

    found_skills = []

    for skill in skills:
        if skill.lower() in text_lower:
            found_skills.append(skill)

    missing_skills = [
        skill for skill in skills
        if skill not in found_skills
    ]

    # -----------------------------
    # Sections
    # -----------------------------

    education = "Yes" if any(word in text_lower for word in [
        "education",
        "b.tech",
        "b.e",
        "bachelor",
        "degree",
        "college",
        "university"
    ]) else "No"

    experience = "Yes" if any(word in text_lower for word in [
        "experience",
        "work experience",
        "internship",
        "employment"
    ]) else "No"

    projects = "Yes" if any(word in text_lower for word in [
        "project",
        "projects"
    ]) else "No"

    certifications = "Yes" if any(word in text_lower for word in [
        "certification",
        "certifications",
        "certificate"
    ]) else "No"

    # -----------------------------
    # Resume Score
    # -----------------------------

    score = 0

    # Skills - 40 marks
    skill_score = min(len(found_skills) * 3, 40)
    score += skill_score

    # Education - 15 marks
    if education == "Yes":
        score += 15

    # Experience - 15 marks
    if experience == "Yes":
        score += 15

    # Projects - 15 marks
    if projects == "Yes":
        score += 15

    # Certifications - 15 marks
    if certifications == "Yes":
        score += 15

    # Maximum 100
    score = min(score, 100)

    # -----------------------------
    # Suggestions
    # -----------------------------

    suggestions = []

    if len(found_skills) < 5:
        suggestions.append(
            "Add more relevant technical skills."
        )

    if education == "No":
        suggestions.append(
            "Add a clear Education section."
        )

    if experience == "No":
        suggestions.append(
            "Add internships, work experience, or practical experience."
        )

    if projects == "No":
        suggestions.append(
            "Add 2-3 relevant projects with descriptions."
        )

    if certifications == "No":
        suggestions.append(
            "Add relevant certifications or courses."
        )

    if len(text) < 1000:
        suggestions.append(
            "Your resume appears to have limited content. Add more details."
        )

    if not suggestions:
        suggestions.append(
            "Your resume has a good structure. Keep improving your skills and projects."
        )

    return render_template(
        "result.html",
        filename=file.filename,
        score=score,
        skills=found_skills,
        missing_skills=missing_skills,
        education=education,
        experience=experience,
        projects=projects,
        certifications=certifications,
        suggestions=suggestions,
        text=text
    )


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )