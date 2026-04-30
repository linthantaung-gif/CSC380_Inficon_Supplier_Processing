import json
import os
from similarity_test import match_questions
from fill_pdf_form import autofill_pdf, extract_pdf_fields
from fill_docx_form import autofill_docx, extract_docx_fields
from vector_embedding_model import load_embedding_model
import pandas as pd

def process_file(filepath):
    file_type = detect_file_type(filepath)

    if file_type == "docx":
        model = load_embedding_model()
        with open("confluence_data.json") as f:
            confluence_data = json.load(f)
        conf_df = pd.DataFrame(confluence_data)
        doc_fields, doc = extract_docx_fields("toy_pdf.docx")
        docx_df = pd.DataFrame([
            {
                "question_text": f["field_name"].strip().lower(),
                "field_name": f["field_name"]
            }
            for f in doc_fields
        ])
        doc_match_results = match_questions(model, docx_df, conf_df, threshold=0.8)
        autofill_docx(doc, doc_fields, doc_match_results, "output_doc.docx")

    if file_type == "pdf":
        model = load_embedding_model()
        with open("confluence_data.json") as f:
            confluence_data = json.load(f)

        conf_df = pd.DataFrame(confluence_data)
        pdf_fields, pdf = extract_pdf_fields("toy_pdf.pdf")
        pdf_df = pd.DataFrame([
            {
                "question_text": f["field_name"].strip().lower(),
                "field_name": f["field_name"]
            }
            for f in pdf_fields
        ])
        pdf_match_results = match_questions(model, pdf_df, conf_df, threshold=0.8)
        autofill_pdf(pdf, pdf_fields, pdf_match_results, "output_pdf.pdf")

    else:
        raise ValueError("Unsupported File Type")

def detect_file_type(filepath):
    ext = os.path.splitext(filepath)[1].lower()

    if ext == ".pdf":
        return "pdf"

    elif ext == ".docx":
        return "docx"

    else:
        return "unknown"
