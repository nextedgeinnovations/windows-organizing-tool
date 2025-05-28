import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import font as tkfont
from PIL import Image, ImageTk  # Pillow for logo and background image handling
import webbrowser
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Company information
COMPANY_NAME = "Next Edge Innovations"
COMPANY_EMAIL = "admin@nextedgeinnovations.org"
COMPANY_WEBSITE = "https://nextedgeinnovations.org/"
LOGO_PATH = "logo.png"  # Replace with your logo image path
BACKGROUND_PATH = "background.png"  # Replace with your background image path


def create_folder(folder_path):
    try:
        os.mkdir(folder_path)
        logging.info(f"Folder {folder_path} created.")
    except FileExistsError:
        logging.warning(f"Folder already exists at {folder_path}.")


def move_file(doc, subfolder_path):
    try:
        new_doc_path = os.path.join(subfolder_path, os.path.basename(doc))
        os.rename(doc, new_doc_path)
        logging.info(f"Moved file {doc} to {new_doc_path}.")
        return True
    except Exception as e:
        logging.error(f"Error moving file {doc} to {subfolder_path}: {e}")
        return False


def clean_directory(path):
    logging.info(f"Cleaning up directory {path}")

    dir_content = os.listdir(path)
    path_dir_content = [os.path.join(path, doc) for doc in dir_content]

    docs = [doc for doc in path_dir_content if os.path.isfile(doc)]
    folders = [folder for folder in path_dir_content if os.path.isdir(folder)]

    moved = 0
    for doc in docs:
        _, filetype = os.path.splitext(doc)
        filetype = filetype[1:].lower()

        if os.path.basename(doc).startswith('.') or os.path.basename(doc) == "directory_cleanup_gui.py":
            continue

        subfolder_path = os.path.join(path, filetype)
        if subfolder_path not in folders:
            create_folder(subfolder_path)

        if move_file(doc, subfolder_path):
            moved += 1

    logging.info(f"Moved {moved} of {len(docs)} files.")
    messagebox.showinfo("Cleanup Complete", f"Moved {moved} files to their respective folders.")


def select_directory():
    directory = filedialog.askdirectory()
    if directory:
        clean_directory(directory)


def open_website(event):
    webbrowser.open_new(COMPANY_WEBSITE)


def open_email(event):
    webbrowser.open_new(f"mailto:{COMPANY_EMAIL}")


# --- GUI Setup ---
root = tk.Tk()
root.title("Directory Cleanup Tool")
root.geometry("500x600")
root.configure(bg="#f5f5f5")  # Light neutral background

# Load background image
try:
    background_img = Image.open(BACKGROUND_PATH)
    background_photo = ImageTk.PhotoImage(background_img)
    background_label = tk.Label(root, image=background_photo)
    background_label.place(relwidth=1, relheight=1)  # Cover the entire window
except Exception as e:
    logging.warning(f"Background image not found or failed to load: {e}")

# Fonts
title_font = tkfont.Font(family="Helvetica", size=18, weight="bold")
info_font = tkfont.Font(family="Helvetica", size=10)

# Container frame
container = tk.Frame(root, bg="white", bd=2, relief=tk.RIDGE)
container.pack(padx=20, pady=20, fill="both", expand=True)

# Logo (load image)
try:
    logo_img = Image.open(LOGO_PATH)  # Ensure the logo is in the same folder or provide full path
    logo_img = logo_img.resize((120, 120), Image.ANTIALIAS)
    logo_photo = ImageTk.PhotoImage(logo_img)
    logo_label = tk.Label(container, image=logo_photo, bg="white")
    logo_label.pack(pady=(20,10))
except Exception as e:
    logging.warning(f"Logo not found or failed to load: {e}")
    # If logo not loaded, display company name larger
    no_logo_label = tk.Label(container, text=COMPANY_NAME, font=title_font, bg="white", fg="#333333")
    no_logo_label.pack(pady=(30,10))

# Title label
title_label = tk.Label(container, text="Directory Cleanup Tool", font=title_font, fg="#333333", bg="white")
title_label.pack(pady=(0,20))

# Instruction label
instructions = tk.Label(container, text="Click the button below to select the directory you want to clean.\nFiles will be organized into folders based on their file types.",
                        font=info_font, fg="#666666", bg="white", justify="center", wraplength=400)
instructions.pack(pady=(0,20))

# Button style
button = tk.Button(container, text="Select Directory to Clean", font=("Helvetica", 14), bg="#4CAF50", fg="white", relief="flat", padx=20, pady=10, activebackground="#45a049", cursor="hand2", command=select_directory)
button.pack()

# Footer frame
footer = tk.Frame(root, bg="#f5f5f5")
footer.pack(side="bottom", fill="x", pady=20)

# Company info labels with clickable links
company_label = tk.Label(footer, text=COMPANY_NAME, font=info_font, bg="#f5f5f5", fg="#333333")
company_label.pack()

email_label = tk.Label(footer, text=COMPANY_EMAIL, font=info_font, fg="blue", bg="#f5f5f5", cursor="hand2")
email_label.pack()
email_label.bind("<Button-1>", open_email)

website_label = tk.Label(footer, text=COMPANY_WEBSITE, font=info_font, fg="blue", bg="#f5f5f5", cursor="hand2")
website_label.pack()
website_label.bind("<Button-1>", open_website)

# Run the GUI
root.mainloop()
