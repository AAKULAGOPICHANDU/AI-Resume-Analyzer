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
        "Python", "Git", "SQL", "Flask"
    ],

    "Web Developer": [
        "HTML", "CSS", "JavaScript"
    ],

    "Backend Developer": [
        "Python", "SQL", "Flask", "Git"
    ],

    "Frontend Developer": [
        "HTML", "CSS", "JavaScript", "React"
    ],

    "Data Scientist": [
        "Python", "SQL", "Data Science", "Machine Learning"
    ],

    "Machine Learning Engineer": [
        "Python", "Machine Learning", "Data Science", "SQL"
    ],

    "AI Engineer": [
        "Python", "Machine Learning",
        "Artificial Intelligence"
    ],

    "Software Developer": [
        "Python", "Java", "C++", "SQL", "Git"
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

    found = [skill.lower() for skill in found_skills]

    for job, required_skills in JOBS.items():

        matched = []

        for skill in required_skills:

            if skill.lower() in found:
                matched.append(skill)

        percentage = int(
            (len(matched) / len(required_skills)) * 100
        )

        recommendations.append({
            "job": job,
            "percentage": percentage,
            "matched": matched
        })

    recommendations.sort(
        key=lambda x: x["percentage"],
        reverse=True
    )

    return recommendations


# -----------------------------
# ATS Analysis
# -----------------------------

def ats_analysis(text):

    text_lower = text.lower()

    # Important resume keywords
    keywords = [
        "python",
        "java",
        "sql",
        "html",
        "css",
        "javascript",
        "git",
        "github",
        "flask",
        "machine learning",
        "artificial intelligence",
        "data science",
        "react",
        "project",
        "internship",
        "experience",
        "education",
        "skills",
        "certification"
    ]

    found_keywords = []
    missing_keywords = []

    for keyword in keywords:

        if keyword in text_lower:
            found_keywords.append(keyword)
        else:
            missing_keywords.append(keyword)

    # Keyword score
    keyword_score = int(
        (len(found_keywords) / len(keywords)) * 60
    )

    # Section score
    sections = [
        "education",
        "experience",
        "skills",
        "project",
        "certification"
    ]

    section_count = 0

    for section in sections:

        if section in text_lower:
            section_count += 1

    section_score = int(
        (section_count / len(sections)) * 40
    )

    ats_score = keyword_score + section_score

    return {
        "score": ats_score,
        "found_keywords": found_keywords,
        "missing_keywords": missing_keywords
    }


# -----------------------------
# ATS suggestions
# -----------------------------

def get_suggestions(ats_result, text):

    suggestions = []

    if ats_result["score"] < 50:

        suggestions.append(
            "Your ATS score is low. Add more relevant keywords."
        )

    if len(ats_result["missing_keywords"]) > 5:

        suggestions.append(
            "Add technical skills that match your target job."
        )

    if "experience" not in text.lower():

        suggestions.append(
            "Add an Experience or Internship section."
        )

    if "project" not in text.lower():

        suggestions.append(
            "Add relevant projects with technologies used."
        )

    if "certification" not in text.lower():

        suggestions.append(
            "Add relevant certifications."
        )

    if len(text) < 1000:

        suggestions.append(
            "Your resume contains limited information. "
            "Add more details about your projects and achievements."
        )

    if not suggestions:

        suggestions.append(
            "Your resume has good ATS compatibility. "
            "Continue improving your technical skills."
        )

    return suggestions


# -----------------------------
# Home
# -----------------------------

@app.route("/")
def home():

    return render_template("index.html")


# -----------------------------
# Upload
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

    # Skills
    found_skills = find_skills(text)

    # Jobs
    recommendations = recommend_jobs(found_skills)

    # ATS
    ats_result = ats_analysis(text)

    # Suggestions
    suggestions = get_suggestions(
        ats_result,
        text
    )

    return render_template(
        "result.html",
        filename=file.filename,
        score=ats_result["score"],
        skills=found_skills,
        recommendations=recommendations,
        ats=ats_result,
        suggestions=suggestions
    )


# -----------------------------
# Run application
# -----------------------------

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )