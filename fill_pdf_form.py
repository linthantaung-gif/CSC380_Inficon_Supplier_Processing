from pypdf import PdfReader, PdfWriter
import fitz

def extract_pdf_fields(pdf_path):
    pdf = fitz.open(pdf_path)
    fields = []

    for page_num, page in enumerate(pdf):
        if hasattr(page, "widgets") and page.widgets():
            for w in page.widgets():
                if not w.field_name:
                    continue
                fields.append({
                    "field_name": w.field_name,
                    "rect": w.rect,
                    "field_type": w.field_type.name if hasattr(w.field_type, "name") else str(w.field_type),
                    "page_num": page_num
                })

    if not fields:
        print("No fields found in this PDF")
    return fields, pdf


def autofill_pdf(pdf, fields, match_results, output_path):
    match_lookup = {m.get("form_question"): m for m in match_results}
    for f in fields:
        field_name = f["field_name"]
        page = pdf[f["page_num"]]
        rect = f["rect"]
        match = match_lookup.get(field_name)

        if not match:
            continue

        decision = match.get("decision", "").lower()

        if decision not in ["autofill"]:
            continue

        text_to_insert = str(match.get("answer", ""))

        if f["field_type"] == '2':
            x = rect.x0
            y = rect.y0 + 8
            if text_to_insert.lower() in ["yes", "true", "1", "x"]:
                page.insert_text(
                    (x, y),
                    "x",
                    fontsize=10,
                    color=(0, 0, 0)
                )
        else:
            x = rect.x0
            y = rect.y0 + 10
            page.insert_text(
                (x, y),
                text_to_insert,
                fontsize=8,
                color=(0, 0, 0),
            )

    pdf.save(output_path)
    print(f"PDF saved as {output_path}")