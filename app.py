from flask import Flask, render_template, request
import os

from pypdf import PdfReader
from sentence_transformers import SentenceTransformer, util

from job_data import JOBS


app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# --------------------------------
# Load AI model
# --------------------------------

print("Loading AI model...")

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

print("AI model loaded successfully!")


# --------------------------------
# Extract PDF text
# --------------------------------

def extract_text(filepath):

    reader = PdfReader(filepath)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:

            text += page_text + "\n"

    return text


# --------------------------------
# AI Job Recommendation
# --------------------------------

def recommend_jobs(resume_text):

    resume_embedding = model.encode(
        resume_text,
        convert_to_tensor=True
    )

    results = []

    for job in JOBS:

        job_embedding = model.encode(
            job["description"],
            convert_to_tensor=True
        )

        similarity = util.cos_sim(
            resume_embedding,
            job_embedding
        ).item()

        percentage = int(
            max(0, min(100, similarity * 100))
        )

        results.append({
            "title": job["title"],
            "percentage": percentage,
            "description": job["description"]
        })

    results.sort(
        key=lambda x: x["percentage"],
        reverse=True
    )

    return results


# --------------------------------
# Home
# --------------------------------

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# --------------------------------
# Upload Resume
# --------------------------------

@app.route(
    "/upload",
    methods=["POST"]
)
def upload():

    file = request.files.get(
        "resume"
    )

    if not file:

        return "Please select a resume."


    if file.filename == "":

        return "Please select a resume."


    if not file.filename.lower().endswith(".pdf"):

        return "Only PDF files are supported."


    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        file.filename
    )

    file.save(filepath)


    # Extract resume text

    resume_text = extract_text(
        filepath
    )


    if not resume_text.strip():

        return """
        <h2>Could not extract text from this PDF.</h2>
        <p>Please upload a text-based PDF resume.</p>
        <a href="/">Go Back</a>
        """


    # AI recommendations

    recommendations = recommend_jobs(
        resume_text
    )


    return render_template(
        "result.html",
        filename=file.filename,
        recommendations=recommendations,
        resume_text=resume_text
    )


# --------------------------------
# Run application
# --------------------------------

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )