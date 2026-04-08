import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import os
import shutil
import json
import sys
import tempfile  # Added to handle temporary file storage
from PIL import Image, ImageTk

# ── Resolve paths ────────────────────────────────────────────────────────────
if getattr(sys, "frozen", False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CONFLUENCE_JSON = os.path.join(BASE_DIR, "confluence_data.json")

BG       = "#FFFFFF"
CARD     = "#FBFBFC"
ACCENT   = "#F3F4F6"
TEXT     = "#000000"
SUBTEXT  = "#4B5563"
BORDER   = "#E5E7EB"
DISABLED = "#9CA3AF"

FONT_TITLE  = ("Segoe UI", 22, "bold")
FONT_BODY   = ("Segoe UI", 11, "bold")
FONT_SMALL  = ("Segoe UI", 9)
FONT_BUTTON = ("Segoe UI", 11, "bold")

class FormFillerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Form Filler")
        self.configure(bg=BG)
        self.resizable(False, False)
        self.geometry("520x540")

        self._selected_path = None
        self._output_path   = None
        self._build_ui()

    def _build_ui(self):
        # Header Container
        hdr = tk.Frame(self, bg=BG)
        hdr.pack(fill="x", padx=36, pady=(32, 0))

        # Left side: Titles
        title_cnt = tk.Frame(hdr, bg=BG)
        title_cnt.pack(side="left")

        tk.Label(title_cnt, text="Form Filler", font=FONT_TITLE, bg=BG, fg=TEXT).pack(anchor="w")
        tk.Label(title_cnt, text="Upload a PDF or Word form",
                 font=FONT_SMALL, bg=BG, fg=SUBTEXT).pack(anchor="w", pady=(4, 0))

        # Right side: INFICON Logo
        try:
            logo_path = os.path.join(BASE_DIR, "INFICON Company Logo.png")
            if os.path.exists(logo_path):
                img = Image.open(logo_path)
                w_pref = 110
                w_percent = (w_pref / float(img.size[0]))
                h_size = int((float(img.size[1]) * float(w_percent)))
                img = img.resize((w_pref, h_size), Image.Resampling.LANCZOS)
                
                self._logo_img = ImageTk.PhotoImage(img)
                logo_label = tk.Label(hdr, image=self._logo_img, bg=BG)
                logo_label.pack(side="right", anchor="ne")
        except Exception as e:
            print(f"Logo failed to load: {e}")

        # Divider
        tk.Frame(self, bg=BORDER, height=1).pack(fill="x", padx=36, pady=20)

        # Upload Area
        self._drop_frame = tk.Frame(self, bg=CARD, bd=0, highlightthickness=1, highlightbackground=BORDER)
        self._drop_frame.pack(fill="x", padx=36)

        inner = tk.Frame(self._drop_frame, bg=CARD)
        inner.pack(padx=24, pady=28)

        self._file_icon = tk.Label(inner, text="📄", font=("Segoe UI", 32), bg=CARD, fg=SUBTEXT)
        self._file_icon.pack()

        self._file_label = tk.Label(inner, text="No file selected", font=FONT_BODY, bg=CARD, fg=TEXT)
        self._file_label.pack(pady=(8, 0))

        self._browse_btn = self._make_button(inner, "Browse file...", ACCENT, self._browse, width=16)
        self._browse_btn.pack(pady=(14, 0))

        # Progress Bar Area
        prog_frame = tk.Frame(self, bg=BG)
        prog_frame.pack(fill="x", padx=36, pady=(24, 0))

        self._status_label = tk.Label(prog_frame, text="", font=FONT_SMALL, bg=BG, fg=TEXT)
        self._status_label.pack(anchor="w")

        self._bar_bg = tk.Canvas(prog_frame, bg=BORDER, height=6, highlightthickness=0, bd=0)
        self._bar_bg.pack(fill="x", pady=(6, 0))
        self._bar_width = 448

        # Action Buttons
        btn_row = tk.Frame(self, bg=BG)
        btn_row.pack(fill="x", padx=36, pady=32)

        self._run_btn = self._make_button(btn_row, "Fill Form", ACCENT, self._run, width=14)
        self._run_btn.pack(side="left")

        self._dl_btn = self._make_button(btn_row, "Save Output", ACCENT, self._save_output, width=14)
        self._dl_btn.pack(side="left", padx=(12, 0))
        self._dl_btn.config(state="disabled", disabledforeground=DISABLED)

        # Footer
        tk.Label(self, text="Powered by INFICON Confluence data  •  AI semantic matching",
                 font=FONT_SMALL, bg=BG, fg=SUBTEXT).pack(side="bottom", pady=20)

    def _make_button(self, parent, text, color, command, width=12):
        btn = tk.Button(parent, text=text, font=FONT_BUTTON, bg=color, fg=TEXT, 
                        activebackground=color, activeforeground=TEXT, relief="flat",
                        highlightthickness=1, highlightbackground=BORDER,
                        cursor="hand2", width=width, pady=6, command=command)
        btn.bind("<Enter>", lambda e: btn.config(bg=self._adjust_color(color, -10)))
        btn.bind("<Leave>", lambda e: btn.config(bg=color))
        return btn

    @staticmethod
    def _adjust_color(hex_color, amount):
        hex_color = hex_color.lstrip("#")
        r, g, b = (int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        r, g, b = max(0, min(255, r + amount)), max(0, min(255, g + amount)), max(0, min(255, b + amount))
        return f"#{r:02x}{g:02x}{b:02x}"

    def _set_progress(self, pct, status=""):
        self._status_label.config(text=status)
        w = self._bar_bg.winfo_width() or self._bar_width
        self._bar_bg.delete("all")
        self._bar_bg.create_rectangle(0, 0, w, 6, fill=BORDER, outline="")
        filled = int(w * pct / 100)
        if filled > 0:
            self._bar_bg.create_rectangle(0, 0, filled, 6, fill=TEXT, outline="")
        self.update_idletasks()

    def _browse(self):
        path = filedialog.askopenfilename(
            title="Select a form to fill",
            filetypes=[("Supported forms", "*.pdf *.docx"), ("PDF files", "*.pdf"), ("Word documents", "*.docx")]
        )
        if path:
            self._selected_path = path
            self._file_label.config(text=os.path.basename(path))
            self._dl_btn.config(state="disabled")
            self._output_path = None
            self._set_progress(0, "")

    def _run(self):
        if not self._selected_path:
            messagebox.showwarning("No file", "Please browse for a file first.")
            return
        self._run_btn.config(state="disabled")
        self._dl_btn.config(state="disabled")
        self._set_progress(0, "Starting...")
        threading.Thread(target=self._worker, daemon=True).start()

    def _worker(self):
        try:
            self._ui_progress(10, "Loading AI model...")
            import pandas as pd
            from similarity_test import match_questions
            from vector_embedding_model import load_embedding_model
            model = load_embedding_model()

            self._ui_progress(30, "Reading Confluence data...")
            with open(CONFLUENCE_JSON, encoding="utf-8") as f:
                conf_data = json.load(f)
            conf_df = pd.DataFrame(conf_data)
            conf_df["question_text"] = conf_df["question_text"].str.strip().str.lower()

            ext = os.path.splitext(self._selected_path)[1].lower()
            
            # Use system temp directory to avoid auto-saving in the project folder
            tmp_out = os.path.join(tempfile.gettempdir(), "inficon_temp_filled" + ext)

            if ext == ".pdf":
                self._ui_progress(50, "Extracting PDF fields...")
                from fill_pdf_form import extract_pdf_fields, autofill_pdf
                fields, pdf = extract_pdf_fields(self._selected_path)
                data_df = pd.DataFrame([{"question_text": f["field_name"].strip().lower(), 
                                         "field_name": f["field_name"]} for f in fields])
                results = match_questions(model, data_df, conf_df, threshold=0.80)
                self._ui_progress(80, "Filling PDF...")
                autofill_pdf(pdf, fields, results, tmp_out)
            else:
                self._ui_progress(50, "Extracting Word fields...")
                from fill_docx_form import extract_docx_fields, autofill_docx
                fields, doc = extract_docx_fields(self._selected_path)
                data_df = pd.DataFrame([{"question_text": f["field_name"].strip().lower(), 
                                         "field_name": f["field_name"]} for f in fields])
                results = match_questions(model, data_df, conf_df, threshold=0.80)
                self._ui_progress(80, "Filling Document...")
                autofill_docx(doc, fields, results, tmp_out)

            self._output_path = tmp_out
            self._ui_progress(100, "Form filled successfully!")
            self.after(0, lambda: self._dl_btn.config(state="normal"))
        except Exception as e:
            self._ui_error(f"Error: {e}")
        finally:
            self.after(0, lambda: self._run_btn.config(state="normal"))

    def _save_output(self):
        if not self._output_path or not os.path.exists(self._output_path):
            return
        ext = os.path.splitext(self._output_path)[1]
        dest = filedialog.asksaveasfilename(defaultextension=ext, initialfile="filled_form"+ext)
        if dest:
            shutil.copy2(self._output_path, dest)
            messagebox.showinfo("Success", f"Saved to: {os.path.basename(dest)}")

    def _ui_progress(self, pct, msg):
        self.after(0, lambda: self._set_progress(pct, msg))

    def _ui_error(self, msg):
        self.after(0, lambda: self._set_progress(0, ""))
        self.after(0, lambda: messagebox.showerror("Error", msg))

if __name__ == "__main__":
    app = FormFillerApp()
    app.mainloop()
