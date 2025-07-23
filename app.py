from flask import Flask, render_template, request, make_response
import pdfkit

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        data = {
            "name": request.form["name"],
            "cgpa": float(request.form["cgpa"]),
            "discipline": float(request.form["discipline"]),
            "hackathons": int(request.form["hackathons"]),
            "internships": int(request.form["internships"]),
            "projects": int(request.form["projects"]),
            "research": int(request.form["research"]),
            "certifications": int(request.form["certifications"]),
            "extra": int(request.form["extra"]),
            "sports": int(request.form["sports"]),
            "leadership": int(request.form["leadership"])
        }

        # Weightage
        weights = {
            "cgpa": 0.40, "discipline": 0.10, "hackathons": 0.10, "internships": 0.10,
            "projects": 0.10, "research": 0.05, "certifications": 0.05,
            "extra": 0.05, "sports": 0.03, "leadership": 0.02
        }

        # Normalize scores
        hackathon_score = min(data["hackathons"] * 2, 10)
        internship_score = min(data["internships"] * 5, 10)
        project_score = min(data["projects"] * 3, 10)
        research_score = min(data["research"] * 5, 10)
        cert_score = min(data["certifications"] * 2, 10)
        extra_score = min(data["extra"] * 2, 10)
        sports_score = min(data["sports"] * 3, 10)
        leadership_score = min(data["leadership"] * 2, 10)

        scores = {
            "CGPA": data["cgpa"],
            "Discipline": data["discipline"],
            "Hackathons": hackathon_score,
            "Internships": internship_score,
            "Projects": project_score,
            "Research": research_score,
            "Certifications": cert_score,
            "Extra": extra_score,
            "Sports": sports_score,
            "Leadership": leadership_score
        }

        overall = (
            data["cgpa"] * weights["cgpa"] +
            data["discipline"] * weights["discipline"] +
            hackathon_score * weights["hackathons"] +
            internship_score * weights["internships"] +
            project_score * weights["projects"] +
            research_score * weights["research"] +
            cert_score * weights["certifications"] +
            extra_score * weights["extra"] +
            sports_score * weights["sports"] +
            leadership_score * weights["leadership"]
        )

        if overall >= 8.5:
            category = "Excellent"
        elif overall >= 7:
            category = "Good"
        elif overall >= 5:
            category = "Average"
        else:
            category = "Poor"

        return render_template("result.html", name=data["name"], overall=round(overall, 2),
                               category=category, scores=scores)
    return render_template("index.html")


@app.route("/download_pdf", methods=["POST"])
def download_pdf():
    html = request.form["html"]
    pdf = pdfkit.from_string(html, False)
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "attachment; filename=report.pdf"
    return response


if __name__ == "__main__":
    app.run(debug=True)
