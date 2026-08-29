# print("Hello World")

from flask import Flask, request, jsonify
import pdfplumber

app = Flask(__name__)


@app.route("/upload-resume", methods=["POST"])
def upload_resume():

    # Frontend se PDF receive
    pdf_file = request.files.get("resume")

    if not pdf_file:
        return jsonify({
            "success": False,
            "message": "PDF file nahi mili"
        }), 400

    try:
        extracted_text = ""

        # PDF ko directly memory se read karna
        with pdfplumber.open(pdf_file) as pdf:

            for page in pdf.pages:
                text = page.extract_text()

                if text:
                    extracted_text += text + "\n"

        # Extracted text aage bhejne ke liye ready
        return jsonify({
            "success": True,
            "resume_text": extracted_text.strip()
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)