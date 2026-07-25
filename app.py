from document_generator import create_document
from flask import send_file
import os
from flask import Flask, render_template, request

app = Flask(__name__)
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/sections")
def sections():
    return render_template("sections.html")


@app.route("/section_names", methods=["POST"])
def section_names():

    title = request.form["title"]

    count = int(request.form["count"])

    return render_template(
        "contents.html",
        title=title,
        count=count
    )
@app.route("/content_page", methods=["POST"])
def content_page():

    title = request.form["title"]

    count = int(request.form["count"])

    sections = []

    for i in range(count):
        sections.append(request.form[f"section{i}"])

    return render_template(
        "preview.html",
        title=title,
        sections=sections
    )

@app.route("/generate", methods=["POST"])
def generate():

    title = request.form["title"]

    sections = request.form.getlist("section_name")

    contents = request.form.getlist("content")

    filename = os.path.join(
        "generated_docs",
        f"{title}.docx"
    )

    create_document(
        title,
        sections,
        contents,
        filename
    )

    return send_file(
        filename,
        as_attachment=True
    )

if __name__ == "__main__":
    app.run(debug=True)
