import tkinter as tk
from tkinter import filedialog, messagebox
import re
import os

from docling.document_converter import DocumentConverter
from docling.datamodel.base_models import InputFormat
from docling.document_converter import (
    DocumentConverter,
    PdfFormatOption,
    WordFormatOption,
)
from docling.pipeline.simple_pipeline import SimplePipeline
from docling.pipeline.standard_pdf_pipeline import StandardPdfPipeline
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.backend.pypdfium2_backend import PyPdfiumDocumentBackend

def process_srt(file_path, output_text):
    """Extracts text from an SRT file using the provided regex."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # The user-provided regex with multiline mode enabled
        regex = r"\n?+^\d+$\n^\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}$\n"
        extracted_text = re.sub(regex, "", content, flags=re.MULTILINE)
        return extracted_text.strip()  # Remove leading/trailing whitespace

    except FileNotFoundError:
        messagebox.showerror("Error", "File not found.")
        return None
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return None

def process_vtt(file_path, output_text):
    """Processes a VTT file using vtt2txt."""
    from vtt2txt.__main__ import vtt_to_text
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        text = vtt_to_text(content)
        return text
    except FileNotFoundError:
        messagebox.showerror("Error", "File not found.")
        return None
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return None

def process_pdf(file_path, do_ocr):
    """Processes a PDF or other (office documents, images, web pages) file using docling."""
    try:
        # previous `PipelineOptions` is now `PdfPipelineOptions`
        pipeline_options = PdfPipelineOptions()
        pipeline_options.do_ocr = do_ocr # Enable or disable OCR based on the option
        #pipeline_options.do_table_structure = True
        #...

        ## Custom options are now defined per format.
        doc_converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(
                    pipeline_options=pipeline_options, # pipeline options go here.
                    #backend=PyPdfiumDocumentBackend # optional: pick an alternative backend
                ),
                InputFormat.DOCX: WordFormatOption(
                    pipeline_cls=SimplePipeline # default for office formats and HTML
                ),
            },
        )

        #docling.utils.model_downloader.download_models()  # force download models

        result = doc_converter.convert(file_path)
        return result.document.export_to_markdown()
    except FileNotFoundError:
        messagebox.showerror("Error", "PDF file not found.")
        return None
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred processing PDF: {e}")
        return None



def process_file(input_file_path, output_text, do_ocr=False):
    """Processes the selected subtitle file."""
    if not input_file_path:
        messagebox.showwarning("Warning", "No file selected.")
        return

    base_name = os.path.splitext(os.path.basename(input_file_path))[0]
    output_file_path = os.path.join(os.path.dirname(input_file_path), f"{base_name}.txt")


    if input_file_path.lower().endswith('.srt'):
        extracted_text = process_srt(input_file_path, output_text)
    elif input_file_path.lower().endswith('.vtt'):
        extracted_text = process_vtt(input_file_path, output_text)
    elif input_file_path.lower().endswith(('.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.html', '.xhtml', '.png', '.jpeg', '.jpg', '.tiff', '.bmp')):
        extracted_text = process_pdf(input_file_path, do_ocr) # Use process_pdf for other formats
    else:
        messagebox.showerror("Error", "Unsupported file format. Please select a supported file format.")
        return

    if extracted_text is not None:
      try:
        with open(output_file_path, 'w', encoding='utf-8') as outfile:
            outfile.write(extracted_text)
        output_text.insert(tk.END, f"Successfully processed {os.path.basename(input_file_path)} and saved to {os.path.basename(output_file_path)}\n")
      except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


def select_file(output_text, do_ocr):
    """Opens a file dialog to select a subtitle file."""
    file_path = filedialog.askopenfilename(
        title="Select File",
        filetypes=[
            ("All supported files", "*.srt;*.vtt;*.pdf;*.doc;*.docx;*.xls;*.xlsx;*.ppt;*.pptx;*.html;*.xhtml;*.png;*.jpeg;*.jpg;*.tiff;*.bmp"),
            ("Subtitle files", "*.srt;*.vtt"),
            ("PDF files", "*.pdf"),
            ("Office documents", "*.doc;*.docx;*.xls;*.xlsx;*.ppt;*.pptx"),
            ("Web pages", "*.html;*.xhtml"),
            ("Image files", "*.png;*.jpeg;*.jpg;*.tiff;*.bmp"),
            ("All files", "*.*"),
        ]
    )
    if file_path:
      process_file(file_path, output_text, do_ocr)


def create_gui():
    """Creates the main application GUI."""
    root = tk.Tk()
    root.title("Subtitles2text - Subtitles Text Extractor")
    do_ocr_var = tk.BooleanVar(value=False) # Initialize BooleanVar for OCR option

    # OCR Checkbox
    do_ocr_var = tk.BooleanVar(value=False)
    ocr_check = tk.Checkbutton(root, text="Enable OCR for PDFs", variable=do_ocr_var)
    ocr_check.pack(pady=5)

    # Select File Button
    select_button = tk.Button(root, text="Select File", command=lambda: select_file(output_text, do_ocr_var.get()))
    select_button.pack(pady=20)

    # Output Text Area
    output_text = tk.Text(root, wrap=tk.WORD, width=80, height=10)
    output_text.pack(padx=20, pady=10)


    root.mainloop()

def run_gui():
    create_gui()

if __name__ == "__main__":
    run_gui()

"""
Improvements:

1. Code Readability and Maintainability:
    - Added comments to explain the purpose of functions and sections of code.
    - Improved variable names for clarity (e.g., `do_ocr_var`).

2. Performance Optimization:
    - The option to disable OCR for PDFs can improve performance when OCR is not needed.

3. Best Practices and Patterns:
    - Added an OCR option to enhance flexibility and user control.
    - Used `tk.BooleanVar` for the checkbox to properly manage boolean state in Tkinter.

4. Error Handling and Edge Cases:
    - Error handling remains consistent, with `messagebox.showerror` for exceptions.
    - Added a warning message for when no file is selected.


To further improve this code, consider:
    - Adding more robust logging instead of just displaying error messages in GUI.
    - Implementing more specific exception handling for different error types.
    - Refactoring `process_file` to use a dictionary or a more scalable approach for handling different file types.
    - Adding unit tests to ensure code reliability and prevent regressions.
    - Consider using a more modern GUI framework like `ttk` for improved look and feel.
"""
