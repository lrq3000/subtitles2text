import tkinter as tk
from tkinter import filedialog, messagebox
import re
import os

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


def process_file(input_file_path, output_text):
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
    else:
        messagebox.showerror("Error", "Unsupported file format. Please select a .srt or .vtt file.")
        return

    if extracted_text is not None:
      try:
        with open(output_file_path, 'w', encoding='utf-8') as outfile:
            outfile.write(extracted_text)
        output_text.insert(tk.END, f"Successfully processed {os.path.basename(input_file_path)} and saved to {os.path.basename(output_file_path)}\n")
      except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


def select_file(output_text):
    """Opens a file dialog to select a subtitle file."""
    file_path = filedialog.askopenfilename(
        title="Select Subtitle File",
        filetypes=[("Subtitle files", "*.srt;*.vtt"), ("All files", "*.*")]
    )
    if file_path:
      process_file(file_path, output_text)


def create_gui():
    """Creates the main application GUI."""
    root = tk.Tk()
    root.title("Subtitle Text Extractor")

    # Select File Button
    select_button = tk.Button(root, text="Select Subtitle File", command=lambda: select_file(output_text))
    select_button.pack(pady=20)

    # Output Text Area
    output_text = tk.Text(root, wrap=tk.WORD, width=80, height=10)
    output_text.pack(padx=20, pady=10)


    root.mainloop()

def run_gui():
    create_gui()

if __name__ == "__main__":
    run_gui()
