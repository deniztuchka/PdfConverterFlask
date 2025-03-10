from flask import Flask, render_template, request, send_file
import os
from PyPDF2 import PdfMerger, PdfReader
from pdf2image import convert_from_path
from io import BytesIO

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/merge', methods=['POST'])
def merge_pdfs():
    files = request.files.getlist("pdfs")
    merger = PdfMerger()

    for file in files:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        merger.append(file_path)

    output_pdf = BytesIO()
    merger.write(output_pdf)
    merger.close()
    output_pdf.seek(0)
    return send_file(output_pdf, as_attachment=True, download_name="merged.pdf", mimetype="application/pdf")


@app.route('/extract', methods=['POST'])
def extract_text():
    file = request.files['pdf']
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    reader = PdfReader(file_path)
    extracted_text = "".join([page.extract_text() for page in reader.pages if page.extract_text()])

    return render_template('index.html', extracted_text=extracted_text)


@app.route('/convert', methods=['POST'])
def convert_pdf():
    file = request.files['pdf']
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    images = convert_from_path(file_path)
    image_io = BytesIO()
    images[0].save(image_io, format='PNG')
    image_io.seek(0)

    return send_file(image_io, as_attachment=True, download_name="converted.png", mimetype="image/png")


if __name__ == '__main__':
    app.run(debug=True)
